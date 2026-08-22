from httpx import AsyncClient

from app.api.dependencies import CurrentUser, get_current_user
from app.main import app
from app.policies.permissions import Permission


async def test_create_person(client: AsyncClient) -> None:
    response = await client.post(
        "/people",
        json={
            "name": "Professor Smith",
            "email": "professor@example.com",
            "relationship_label": "Research advisor",
            "usual_response_days": 3,
            "last_interaction": None,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Professor Smith"
    assert data["email"] == "professor@example.com"
    assert data["relationship_label"] == "Research advisor"
    assert data["usual_response_days"] == 3
    assert data["user_id"] == 1


async def test_list_people_only_for_current_user(client: AsyncClient) -> None:
    create_response = await client.post(
        "/people",
        json={
            "name": "User One Person",
        },
    )

    assert create_response.status_code == 201

    def override_get_current_user() -> CurrentUser:
        return CurrentUser(
            id=2,
            email="other-user@example.com",
            permissions=frozenset(
                {
                    Permission.READ_PEOPLE,
                    Permission.CREATE_PERSON,
                }
            ),
        )

    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        response = await client.get("/people")

        assert response.status_code == 200

        people = response.json()

        assert all(person["user_id"] == 2 for person in people)
    finally:
        app.dependency_overrides.pop(get_current_user, None)
