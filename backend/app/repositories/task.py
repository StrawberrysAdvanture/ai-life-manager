from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, task_id: int) -> Task | None:
        return await self.session.get(Task, task_id)

    async def get_all(self) -> list[Task]:
        result = await self.session.execute(
            select(Task).order_by(Task.created_at.desc())
        )

        return list(result.scalars().all())

    async def create(self, task: Task) -> Task:
        self.session.add(task)

        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def update(self, task: Task) -> Task:
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def delete(self, task: Task) -> None:
        await self.session.delete(task)
        await self.session.commit()
