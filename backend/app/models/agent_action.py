from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, Boolean, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class AgentActionStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentAction(Base):
    __tablename__ = "agent_actions"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    action_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    tool_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    input_data: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    status: Mapped[AgentActionStatus] = mapped_column(
        Enum(AgentActionStatus, name="agent_action_status"),
        nullable=False,
        default=AgentActionStatus.PENDING,
    )

    requires_approval: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    approval_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="agent_actions",
    )
