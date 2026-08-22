from httpx import AsyncClient

from app.api.dependencies import CurrentUser, get_current_user
from app.main import app
from app.policies.permissions import Permission


async def test_cannot_create_commitment_for_another_users_person(
    client: AsyncClient,
) -> None:
    # User 1 creates a person
    create_person_response = await client.post(
        "/people",
        json={"name": "User one Person"},
    )

    assert create_person_response.status_code == 201

    person_id = create_person_response.json()["id"]

    def override_get_current_user() -> CurrentUser:
        return CurrentUser(
            id=2,
            email="other-user@example.com",
            permissions=frozenset(
                {
                    Permission.READ_COMMITMENTS,
                    Permission.CREATE_COMMITMENT,
                }
            ),
        )

    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        response = await client.post(
            "commitments",
            json={
                "description": "Should not be allowed",
                "owner": "other",
                "person_id": person_id,
                "due_at": None,
                "source_message_id": None,
            },
        )
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Person not found",
        }

    finally:
        app.dependency_overrides.pop(get_current_user, None)
