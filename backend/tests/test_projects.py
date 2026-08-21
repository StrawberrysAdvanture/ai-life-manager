from httpx import AsyncClient

from app.api.dependencies import CurrentUser, get_current_user
from app.main import app
from app.policies.permissions import Permission


async def test_create_project(client: AsyncClient) -> None:
    response = await client.post(
        "/projects",
        json={
            "name": "Test Project",
            "goal": "Test project creation",
            "deadline": None,
            "status": "active",
            "next_action": "Write tests",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Project"
    assert data["goal"] == "Test project creation"
    assert data["status"] == "active"
    assert data["user_id"] == 1


async def test_list_projects(client: AsyncClient) -> None:
    create_response = await client.post(
        "/projects",
        json={
            "name": "Visible Project",
        },
    )

    assert create_response.status_code == 201

    response = await client.get("/projects")

    assert response.status_code == 200

    projects = response.json()

    assert any(project["name"] == "Visible Project" for project in projects)


async def test_list_projects_only_for_current_user(
    client: AsyncClient,
) -> None:
    first_response = await client.post(
        "/projects",
        json={
            "name": "User One Project",
        },
    )

    assert first_response.status_code == 201

    def override_get_current_user() -> CurrentUser:
        return CurrentUser(
            id=2,
            email="other-user@example.com",
            permissions=frozenset(
                {
                    Permission.READ_PROJECTS,
                    Permission.CREATE_PROJECT,
                }
            ),
        )

    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        response = await client.get("/projects")

        assert response.status_code == 200

        projects = response.json()

        assert all(project["user_id"] == 2 for project in projects)
    finally:
        app.dependency_overrides.pop(get_current_user, None)
