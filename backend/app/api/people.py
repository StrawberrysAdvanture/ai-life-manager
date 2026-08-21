from fastapi import APIRouter, status

from app.api.dependencies import CurrentUserDependency, DatabaseSession
from app.models.person import Person
from app.policies.access import require_permission
from app.policies.permissions import Permission
from app.repositories.person import PersonRepository
from app.schemas.person import PersonCreate, PersonRead
from app.services.person import PersonService

router = APIRouter(
    prefix="/people",
    tags=["people"],
)


@router.post(
    "",
    response_model=PersonRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_person(
    person_data: PersonCreate,
    session: DatabaseSession,
    current_user: CurrentUserDependency,
) -> Person:
    require_permission(
        current_user,
        Permission.CREATE_PERSON,
    )

    repository = PersonRepository(session)
    service = PersonService(repository)

    return await service.create_person(
        person_data,
        user_id=current_user.id,
    )


@router.get(
    "",
    response_model=list[PersonRead],
)
async def list_people(
    session: DatabaseSession,
    current_user: CurrentUserDependency,
) -> list[Person]:
    require_permission(
        current_user,
        Permission.READ_PEOPLE,
    )

    repository = PersonRepository(session)
    service = PersonService(repository)

    return await service.list_people(
        user_id=current_user.id,
    )
