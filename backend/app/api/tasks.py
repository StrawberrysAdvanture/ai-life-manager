from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import CurrentUserDependency, DatabaseSession
from app.models.task import Task
from app.policies.access import require_permission
from app.policies.permissions import Permission
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_data: TaskCreate,
    session: DatabaseSession,
    current_user: CurrentUserDependency,
) -> Task:
    require_permission(current_user, Permission.CREATE_TASK)
    repository = TaskRepository(session)
    service = TaskService(repository)

    return await service.create_task(
        task_data,
        user_id=current_user.id,
    )


@router.get(
    "",
    response_model=list[TaskRead],
)
async def list_tasks(
    session: DatabaseSession, current_user: CurrentUserDependency
) -> list[Task]:
    require_permission(current_user, Permission.READ_TASKS)

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
    current_user: CurrentUserDependency,
) -> Task:
    require_permission(current_user, Permission.READ_TASKS)
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
    current_user: CurrentUserDependency,
) -> Task:
    require_permission(current_user, Permission.UPDATE_TASK)
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
    current_user: CurrentUserDependency,
) -> None:
    require_permission(current_user, Permission.DELETE_TASK)

    repository = TaskRepository(session)
    service = TaskService(repository)

    task = await repository.get_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    await service.delete_task(task)
