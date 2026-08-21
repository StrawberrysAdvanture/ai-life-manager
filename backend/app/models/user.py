from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.agent_action import AgentAction
    from app.models.commitment import Commitment
    from app.models.person import Person
    from app.models.project import Project
    from app.models.task import Task


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    people: Mapped[list["Person"]] = relationship(
        back_populates="user",
    )

    commitments: Mapped[list["Commitment"]] = relationship(
        back_populates="user",
    )

    agent_actions: Mapped[list["AgentAction"]] = relationship(
        back_populates="user",
    )

    projects: Mapped[list["Project"]] = relationship(
        back_populates="user",
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str | None] = mapped_column(
        String(255),
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
        back_populates="user",
    )
