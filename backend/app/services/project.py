from app.models.project import Project
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate


class ProjectService:
    def __init__(self, repository: ProjectRepository) -> None:
        self.repository = repository

    async def create_project(
        self,
        project_data: ProjectCreate,
        user_id: int,
    ) -> Project:
        project = Project(
            user_id=user_id,
            name=project_data.name,
            goal=project_data.goal,
            deadline=project_data.deadline,
            status=project_data.status,
            next_action=project_data.next_action,
        )

        return await self.repository.create(project)

    async def list_projects(self, user_id: int) -> list[Project]:
        return await self.repository.get_all_for_user(user_id)
