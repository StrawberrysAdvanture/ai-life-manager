from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.models.agent_action import AgentActionStatus


class AgentActionCreate(BaseModel):
    action_type: str
    tool_name: str | None = None
    input_data: dict[str, Any] | None = None
    requires_approval: bool = False


class AgentActionRead(BaseModel):
    id: int
    user_id: int
    action_type: str
    tool_name: str | None
    input_data: dict[str, Any] | None
    status: AgentActionStatus
    requires_approval: bool
    approval_id: str | None
    created_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
