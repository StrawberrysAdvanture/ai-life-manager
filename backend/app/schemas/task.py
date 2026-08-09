from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.task import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: int = 3
    status: TaskStatus = TaskStatus.TODO
    deadline: datetime | None = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None
    priority: int
    status: TaskStatus
    deadline: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
