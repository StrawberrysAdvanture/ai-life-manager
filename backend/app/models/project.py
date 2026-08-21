from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User


class ProjectStatus(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)

    user: Mapped["User"] = relationship(
        back_populates="projects",
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    goal: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )

    deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, name="project_status"),
        nullable=False,
        default=ProjectStatus.ACTIVE,
    )

    next_action: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project",
    )
