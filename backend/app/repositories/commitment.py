from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.commitment import Commitment


class CommitmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, commitment: Commitment) -> Commitment:
        self.session.add(commitment)
        await self.session.commit()
        await self.session.refresh(commitment)

        return commitment

    async def get_all_for_user(self, user_id: int) -> list[Commitment]:
        result = await self.session.execute(
            select(Commitment)
            .where(Commitment.user_id == user_id)
            .order_by(Commitment.created_at.desc())
        )

        return list(result.scalars().all())
