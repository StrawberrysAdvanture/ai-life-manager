from fastapi import APIRouter, status

from app.api.dependencies import CurrentUserDependency, DatabaseSession
from app.models.project import Project
from app.policies.access import require_permission
from app.policies.permissions import Permission
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectRead
from app.services.project import ProjectService

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post(
    "",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    project_data: ProjectCreate,
    session: DatabaseSession,
    current_user: CurrentUserDependency,
) -> Project:
    require_permission(
        current_user,
        Permission.CREATE_PROJECT,
    )

    repository = ProjectRepository(session)
    service = ProjectService(repository)

    return await service.create_project(
        project_data,
        user_id=current_user.id,
    )


@router.get(
    "",
    response_model=list[ProjectRead],
)
async def list_projects(
    session: DatabaseSession,
    current_user: CurrentUserDependency,
) -> list[Project]:
    require_permission(
        current_user,
        Permission.READ_PROJECTS,
    )

    repository = ProjectRepository(session)
    service = ProjectService(repository)

    return await service.list_projects(current_user.id)
