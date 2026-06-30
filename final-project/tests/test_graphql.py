import uuid

import httpx
import pytest

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


async def test_register_mutation(client):
    unique_email = f"alice_{uuid.uuid4().hex[:8]}@test.com"
    resp = await gql(
        client,
        """
        mutation($email: String!) {
            register(input: {name: "Alice", email: $email, age: 25, password: "secret123"}) {
                accessToken
                tokenType
            }
        }
    """,
        variables={"email": unique_email},
    )
    assert "errors" not in resp
    assert resp["data"]["register"]["tokenType"] == "bearer"
    assert resp["data"]["register"]["accessToken"] != ""


async def test_register_duplicate_email_returns_error(client):
    unique_email = f"bob_{uuid.uuid4().hex[:8]}@test.com"
    mutation = f"""
        mutation {{
            register(input: {{name: "Bob", email: "{unique_email}", age: 30, password: "pass123"}}) {{
                accessToken
            }}
        }}
    """
    await gql(client, mutation)
    resp = await gql(client, mutation)
    assert "errors" in resp


async def test_login_mutation(client):
    unique_email = f"carol_{uuid.uuid4().hex[:8]}@test.com"
    await gql(
        client,
        f"""
        mutation {{
            register(input: {{name: "Carol", email: "{unique_email}", age: 28, password: "mypassword"}}) {{
                accessToken
            }}
        }}
    """,
    )
    resp = await gql(
        client,
        f"""
        mutation {{
            login(input: {{email: "{unique_email}", password: "mypassword"}}) {{
                accessToken
                tokenType
            }}
        }}
    """,
    )
    assert "errors" not in resp
    assert resp["data"]["login"]["tokenType"] == "bearer"


async def test_login_wrong_password_returns_error(client):
    unique_email = f"dave_{uuid.uuid4().hex[:8]}@test.com"
    await gql(
        client,
        f"""
        mutation {{
            register(input: {{name: "Dave", email: "{unique_email}", age: 22, password: "rightpass"}}) {{
                accessToken
            }}
        }}
    """,
    )
    resp = await gql(
        client,
        f"""
        mutation {{
            login(input: {{email: "{unique_email}", password: "wrongpass"}}) {{
                accessToken
            }}
        }}
    """,
    )
    assert "errors" in resp


@pytest.fixture
async def auth_token(client):
    unique_email = f"eve_{uuid.uuid4().hex[:8]}@test.com"
    resp = await gql(
        client,
        f"""
        mutation {{
            register(input: {{name: "Eve", email: "{unique_email}", age: 27, password: "evepass"}}) {{
                accessToken
            }}
        }}
    """,
    )
    return resp["data"]["register"]["accessToken"]


async def test_me_query_returns_current_user(client, auth_token):
    resp = await gql(client, "query { me { id name email role } }", token=auth_token)
    assert "errors" not in resp
    assert resp["data"]["me"]["name"] == "Eve"
    assert resp["data"]["me"]["role"] == "member"


async def test_me_query_without_token_returns_error(client):
    resp = await gql(client, "query { me { id name } }")
    assert "errors" in resp


# --- Project mutations ---


async def test_create_project(client, auth_token):
    resp = await gql(
        client,
        """
        mutation {
            createProject(input: {name: "My Project"}) {
                id
                name
            }
        }
    """,
        token=auth_token,
    )
    assert "errors" not in resp
    assert resp["data"]["createProject"]["name"] == "My Project"


async def test_update_project(client, auth_token):
    created = await gql(
        client,
        """
        mutation {
            createProject(input: {name: "Old Name"}) { id }
        }
    """,
        token=auth_token,
    )
    assert "errors" not in created
    project_id = created["data"]["createProject"]["id"]

    resp = await gql(
        client,
        """
        mutation($id: Int!) {
            updateProject(id: $id, input: {name: "New Name"}) { id name }
        }
    """,
        variables={"id": project_id},
        token=auth_token,
    )
    assert "errors" not in resp
    assert resp["data"]["updateProject"]["name"] == "New Name"


async def test_delete_project(client, auth_token):
    created = await gql(
        client,
        """
        mutation {
            createProject(input: {name: "To Delete"}) { id }
        }
    """,
        token=auth_token,
    )
    assert "errors" not in created
    project_id = created["data"]["createProject"]["id"]

    resp = await gql(
        client,
        """
        mutation($id: Int!) {
            deleteProject(id: $id)
        }
    """,
        variables={"id": project_id},
        token=auth_token,
    )
    assert "errors" not in resp
    assert resp["data"]["deleteProject"] is True


async def test_create_task(client, auth_token):
    project = await gql(
        client,
        """
        mutation {
            createProject(input: {name: "Task Project"}) { id }
        }
    """,
        token=auth_token,
    )
    assert "errors" not in project
    project_id = project["data"]["createProject"]["id"]

    resp = await gql(
        client,
        """
        mutation($pid: Int!) {
            createTask(input: {title: "First Task", projectId: $pid}) {
                id title done
            }
        }
    """,
        variables={"pid": project_id},
        token=auth_token,
    )
    assert "errors" not in resp
    assert resp["data"]["createTask"]["title"] == "First Task"
    assert resp["data"]["createTask"]["done"] is False


async def test_change_task_status(client, auth_token):
    project = await gql(
        client,
        """
        mutation { createProject(input: {name: "Status Project"}) { id } }
    """,
        token=auth_token,
    )
    assert "errors" not in project
    project_id = project["data"]["createProject"]["id"]

    task = await gql(
        client,
        """
        mutation($pid: Int!) {
            createTask(input: {title: "Toggle Me", projectId: $pid}) { id }
        }
    """,
        variables={"pid": project_id},
        token=auth_token,
    )
    assert "errors" not in task
    task_id = task["data"]["createTask"]["id"]

    resp = await gql(
        client,
        """
        mutation($id: Int!) {
            changeTaskStatus(id: $id, done: true) { id done }
        }
    """,
        variables={"id": task_id},
        token=auth_token,
    )
    assert "errors" not in resp
    assert resp["data"]["changeTaskStatus"]["done"] is True


async def test_projects_query(client, auth_token):
    resp = await gql(client, "query { projects { id name } }", token=auth_token)
    assert "errors" not in resp
    assert isinstance(resp["data"]["projects"], list)


async def test_tasks_query(client, auth_token):
    resp = await gql(client, "query { tasks { id title done } }", token=auth_token)
    assert "errors" not in resp
    assert isinstance(resp["data"]["tasks"], list)


async def test_user_cannot_access_another_users_task(client, auth_token):
    project = await gql(
        client,
        """
        mutation { createProject(input: {name: "Owner Project"}) { id } }
    """,
        token=auth_token,
    )
    assert "errors" not in project
    project_id = project["data"]["createProject"]["id"]

    task = await gql(
        client,
        """
        mutation($pid: Int!) {
            createTask(input: {title: "Owner's Task", projectId: $pid}) { id }
        }
    """,
        variables={"pid": project_id},
        token=auth_token,
    )
    assert "errors" not in task
    task_id = task["data"]["createTask"]["id"]

    unique_email = f"intruder_{uuid.uuid4().hex[:8]}@test.com"
    intruder = await gql(
        client,
        f"""
        mutation {{
            register(input: {{name: "Intruder", email: "{unique_email}", age: 20, password: "intruderpass"}}) {{
                accessToken
            }}
        }}
    """,
    )
    assert "errors" not in intruder
    intruder_token = intruder["data"]["register"]["accessToken"]

    resp = await gql(
        client,
        """
        query($id: Int!) { task(id: $id) { id title } }
    """,
        variables={"id": task_id},
        token=intruder_token,
    )
    assert "errors" in resp
