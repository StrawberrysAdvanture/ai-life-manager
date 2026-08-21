from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.user import User


class TaskStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=3,
    )

    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status"),
        nullable=False,
        default=TaskStatus.TODO,
    )
    deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
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

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id"),
        nullable=True,
        index=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="tasks",
    )

    project: Mapped["Project | None"] = relationship(
        back_populates="tasks",
    )
