from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_database_session
from app.models.task import Task
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

DatabaseSession = Annotated[
    AsyncSession,
    Depends(get_database_session),
]


@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_data: TaskCreate,
    session: DatabaseSession,
) -> Task:
    repository = TaskRepository(session)
    service = TaskService(repository)

    return await service.create_task(task_data)


@router.get(
    "",
    response_model=list[TaskRead],
)
async def list_tasks(
    session: DatabaseSession,
) -> list[Task]:
    repository = TaskRepository(session)
    service = TaskService(repository)

    return await service.list_tasks()


@router.get(
    "/{task_id}",
    response_model=TaskRead,
)
async def get_task(
    task_id: int,
    session: DatabaseSession,
) -> Task:
    repository = TaskRepository(session)
    service = TaskService(repository)

    task = await service.get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


@router.patch(
    "/{task_id}",
    response_model=TaskRead,
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: DatabaseSession,
) -> Task:
    repository = TaskRepository(session)
    service = TaskService(repository)

    task = await repository.get_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return await service.update_task(task, task_data)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    session: DatabaseSession,
) -> None:
    repository = TaskRepository(session)
    service = TaskService(repository)

    task = await repository.get_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    await service.delete_task(task)
