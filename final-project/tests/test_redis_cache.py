import uuid

import pytest
import httpx

from app.db.redis import redis_client
from app.main import app


@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


async def gql(client, query, variables=None, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = await client.post(
        "/graphql/",
        json={"query": query, "variables": variables or {}},
        headers=headers,
    )
    return resp.json()


@pytest.fixture
async def auth_token(client):
    unique_email = f"redis_{uuid.uuid4().hex[:8]}@test.com"
    resp = await gql(
        client,
        f"""
        mutation {{
            register(input: {{name: "RedisTester", email: "{unique_email}", age: 25, password: "redispass"}}) {{
                accessToken
            }}
        }}
        """,
    )
    return resp["data"]["register"]["accessToken"]


async def test_first_query_misses_cache_and_populates_it(client, auth_token):
    """First call to `tasks` should hit the database and write a cache key."""
    resp = await gql(client, "query { tasks { id title done } }", token=auth_token)
    assert "errors" not in resp

    # the cache key includes the user's id, which we get from `me`
    me_resp = await gql(client, "query { me { id } }", token=auth_token)
    user_id = me_resp["data"]["me"]["id"]

    keys = [key async for key in redis_client.scan_iter(match=f"tasks:{user_id}:list:*")]
    assert len(keys) > 0


async def test_second_query_hits_cache(client, auth_token):
    """A second identical call should reuse the cached entry rather than recomputing it."""
    await gql(client, "query { tasks { id title done } }", token=auth_token)

    me_resp = await gql(client, "query { me { id } }", token=auth_token)
    user_id = me_resp["data"]["me"]["id"]
    cache_key = f"tasks:{user_id}:list:None:None:None"

    cached_value_before = await redis_client.get(cache_key)
    assert cached_value_before is not None

    # call again - should still be served from the same cache entry, not overwritten
    resp = await gql(client, "query { tasks { id title done } }", token=auth_token)
    assert "errors" not in resp

    cached_value_after = await redis_client.get(cache_key)
    assert cached_value_after == cached_value_before


async def test_creating_a_task_invalidates_the_cache(client, auth_token):
    """Creating a task should wipe the cached tasks list for that user."""
    # populate the cache first
    await gql(client, "query { tasks { id title done } }", token=auth_token)

    me_resp = await gql(client, "query { me { id } }", token=auth_token)
    user_id = me_resp["data"]["me"]["id"]

    keys_before = [key async for key in redis_client.scan_iter(match=f"tasks:{user_id}:list:*")]
    assert len(keys_before) > 0

    # create a project and a task - this should trigger cache invalidation
    project = await gql(
        client,
        """
        mutation { createProject(input: {name: "Cache Test Project"}) { id } }
        """,
        token=auth_token,
    )
    project_id = project["data"]["createProject"]["id"]

    await gql(
        client,
        """
        mutation($pid: Int!) {
            createTask(input: {title: "Cache Test Task", projectId: $pid}) { id }
        }
        """,
        variables={"pid": project_id},
        token=auth_token,
    )

    keys_after = [key async for key in redis_client.scan_iter(match=f"tasks:{user_id}:list:*")]
    assert len(keys_after) == 0