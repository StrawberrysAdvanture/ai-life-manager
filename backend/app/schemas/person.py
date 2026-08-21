from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PersonCreate(BaseModel):
    name: str
    email: str | None = None
    relationship_label: str | None = None
    usual_response_days: float | None = None
    last_interaction: datetime | None = None


class PersonRead(BaseModel):
    id: int
    user_id: int
    name: str
    email: str | None
    relationship_label: str | None
    usual_response_days: float | None
    last_interaction: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
