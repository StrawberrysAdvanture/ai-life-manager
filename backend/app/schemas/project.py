from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.project import ProjectStatus


class ProjectCreate(BaseModel):
    name: str
    goal: str | None = None
    deadline: datetime | None = None
    status: ProjectStatus = ProjectStatus.ACTIVE
    next_action: str | None = None


class ProjectRead(BaseModel):
    id: int
    user_id: int
    name: str
    goal: str | None
    deadline: datetime | None
    status: ProjectStatus
    next_action: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
