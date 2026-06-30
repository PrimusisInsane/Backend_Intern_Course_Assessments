import httpx
import pytest

from app.main import app


@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


async def test_rest_health_check_reports_ok(client):
    response = await client.get("/health/db")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


async def test_graphql_db_health_reports_ok(client):
    query = "{ dbHealth }"
    response = await client.post("/graphql/", json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["dbHealth"] == "ok"


async def test_graphql_redis_health_reports_ok(client):
    query = "{ redisHealth }"
    response = await client.post("/graphql/", json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["redisHealth"] == "ok"
