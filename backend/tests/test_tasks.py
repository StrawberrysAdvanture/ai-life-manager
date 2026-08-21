from httpx import AsyncClient

from app.api.dependencies import CurrentUser, get_current_user
from app.main import app
from app.policies.permissions import Permission


async def test_create_task(client: AsyncClient) -> None:
    response = await client.post(
        "/tasks",
        json={
            "title": "Test task",
            "description": "Created by pytest",
            "priority": 4,
            "status": "todo",
            "deadline": None,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test task"
    assert data["description"] == "Created by pytest"
    assert data["priority"] == 4
    assert data["status"] == "todo"
    assert data["deadline"] is None

    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


async def test_list_tasks(client: AsyncClient) -> None:
    response = await client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_task(client: AsyncClient) -> None:
    create_response = await client.post(
        "/tasks",
        json={
            "title": "Task to retrieve",
            "priority": 3,
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = await client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Task to retrieve"
    assert data["priority"] == 3


async def test_get_missing_task(client: AsyncClient) -> None:
    response = await client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found",
    }


async def test_update_task(client: AsyncClient) -> None:
    create_response = await client.post(
        "/tasks",
        json={
            "title": "Task to update",
            "priority": 2,
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = await client.patch(
        f"/tasks/{task_id}",
        json={
            "priority": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Task to update"
    assert data["priority"] == 5


async def test_delete_task(client: AsyncClient) -> None:
    create_response = await client.post(
        "/tasks",
        json={
            "title": "Task to delete",
            "priority": 1,
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    delete_response = await client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 204

    get_response = await client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404


async def test_delete_task_without_permission(client: AsyncClient) -> None:
    def override_get_current_user() -> CurrentUser:
        return CurrentUser(
            id=1,
            email="local-user@ai-life-manager.invalid",
            permissions=frozenset(
                {
                    Permission.READ_TASKS,
                    Permission.CREATE_TASK,
                    Permission.UPDATE_TASK,
                }
            ),
        )

    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        response = await client.delete("/tasks/1")

        assert response.status_code == 403
        assert response.json() == {
            "detail": "Permission denied",
        }
    finally:
        app.dependency_overrides.pop(get_current_user, None)
