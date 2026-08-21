from app.models.task import Task
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    async def create_task(self, task_data: TaskCreate, user_id: int) -> Task:
        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            status=task_data.status,
            deadline=task_data.deadline,
            user_id=user_id,
            project_id=None,
        )

        return await self.repository.create(task)

    async def get_task(self, task_id: int) -> Task | None:
        return await self.repository.get_by_id(task_id)

    async def list_tasks(self) -> list[Task]:
        return await self.repository.get_all()

    async def update_task(
        self,
        task: Task,
        task_data: TaskUpdate,
    ) -> Task:
        update_data = task_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(task, field, value)

        return await self.repository.update(task)

    async def delete_task(self, task: Task) -> None:
        await self.repository.delete(task)
