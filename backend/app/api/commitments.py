from fastapi import APIRouter, status

from app.api.dependencies import CurrentUserDependency, DatabaseSession
from app.models.commitment import Commitment
from app.policies.access import require_permission
from app.policies.permissions import Permission
from app.repositories.commitment import CommitmentRepository
from app.repositories.person import PersonRepository
from app.schemas.commitment import CommitmentCreate, CommitmentRead
from app.services.commitment import CommitmentService

router = APIRouter(
    prefix="/commitments",
    tags=["commitments"],
)


@router.post(
    "",
    response_model=CommitmentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_commitment(
    commitment_data: CommitmentCreate,
    session: DatabaseSession,
    current_user: CurrentUserDependency,
) -> Commitment:
    require_permission(
        current_user,
        Permission.CREATE_COMMITMENT,
    )

    repository = CommitmentRepository(session)
    person_repository = PersonRepository(session)

    service = CommitmentService(
        repository,
        person_repository,
    )

    return await service.create_commitment(
        commitment_data,
        user_id=current_user.id,
    )


@router.get(
    "",
    response_model=list[CommitmentRead],
)
async def list_commitments(
    session: DatabaseSession,
    current_user: CurrentUserDependency,
) -> list[Commitment]:
    require_permission(
        current_user,
        Permission.READ_COMMITMENTS,
    )

    repository = CommitmentRepository(session)
    person_repository = PersonRepository(session)

    service = CommitmentService(
        repository,
        person_repository,
    )

    return await service.list_commitments(
        user_id=current_user.id,
    )
