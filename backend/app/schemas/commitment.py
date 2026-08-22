from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.commitment import (
    CommitmentOwner,
    CommitmentStatus,
)


class CommitmentCreate(BaseModel):
    description: str
    owner: CommitmentOwner
    person_id: int | None = None
    due_at: datetime | None = None
    source_message_id: str | None = None


class CommitmentRead(BaseModel):
    id: int
    user_id: int
    person_id: int | None
    description: str
    owner: CommitmentOwner
    status: CommitmentStatus
    due_at: datetime | None
    source_message_id: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
