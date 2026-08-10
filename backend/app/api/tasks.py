from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_database_session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate

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
    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        status=task_data.status,
        deadline=task_data.deadline,
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


@router.get(
    "",
    response_model=list[TaskRead],
)
async def list_tasks(
    session: DatabaseSession,
) -> list[Task]:
    result = await session.execute(select(Task).order_by(Task.created_at.desc()))

    return list(result.scalars().all())


@router.get(
    "/{task_id}",
    response_model=TaskRead,
)
async def get_task(
    task_id: int,
    session: DatabaseSession,
) -> Task:
    task = await session.get(Task, task_id)

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
    task = await session.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    await session.commit()
    await session.refresh(task)

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    session: DatabaseSession,
) -> None:
    task = await session.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    await session.delete(task)
    await session.commit()
