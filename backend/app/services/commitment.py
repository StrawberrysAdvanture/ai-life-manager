from fastapi import HTTPException, status

from app.models.commitment import Commitment, CommitmentStatus
from app.repositories.commitment import CommitmentRepository
from app.repositories.person import PersonRepository
from app.schemas.commitment import CommitmentCreate


class CommitmentService:
    def __init__(
        self, repository: CommitmentRepository, person_repository: PersonRepository
    ) -> None:
        self.repository = repository
        self.person_repository = person_repository

    async def create_commitment(
        self,
        commitment_data: CommitmentCreate,
        user_id: int,
    ) -> Commitment:
        if commitment_data.person_id is not None:
            person = await self.person_repository.get_by_id_for_user(
                person_id=commitment_data.person_id,
                user_id=user_id,
            )

            if person is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Person not found",
                )

        commitment = Commitment(
            user_id=user_id,
            person_id=commitment_data.person_id,
            description=commitment_data.description,
            owner=commitment_data.owner,
            status=CommitmentStatus.OPEN,
            due_at=commitment_data.due_at,
            source_message_id=commitment_data.source_message_id,
        )

        return await self.repository.create(commitment)

    async def list_commitments(
        self,
        user_id: int,
    ) -> list[Commitment]:
        return await self.repository.get_all_for_user(user_id)
