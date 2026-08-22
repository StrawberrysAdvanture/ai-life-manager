from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.person import Person


class PersonRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, person: Person) -> Person:
        self.session.add(person)
        await self.session.commit()
        await self.session.refresh(person)

        return person

    async def get_all_for_user(self, user_id: int) -> list[Person]:
        result = await self.session.execute(
            select(Person)
            .where(Person.user_id == user_id)
            .order_by(Person.created_at.desc())
        )

        return list(result.scalars().all())

    async def get_by_id_for_user(self, person_id: int, user_id: int) -> Person | None:
        result = await self.session.execute(
            select(Person).where(
                Person.id == person_id,
                Person.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()
