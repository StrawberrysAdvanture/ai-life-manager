from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.person import Person
    from app.models.user import User


class CommitmentOwner(StrEnum):
    USER = "user"
    OTHER = "other"


class CommitmentStatus(StrEnum):
    OPEN = "open"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Commitment(Base):
    __tablename__ = "commitments"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    person_id: Mapped[int | None] = mapped_column(
        ForeignKey("people.id"),
        nullable=True,
        index=True,
    )

    description: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )

    owner: Mapped[CommitmentOwner] = mapped_column(
        Enum(CommitmentOwner, name="commitment_owner"),
        nullable=False,
    )

    status: Mapped[CommitmentStatus] = mapped_column(
        Enum(CommitmentStatus, name="commitment_status"),
        nullable=False,
        default=CommitmentStatus.OPEN,
    )

    due_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    source_message_id: Mapped[str | None] = mapped_column(
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

    user: Mapped["User"] = relationship(
        back_populates="commitments",
    )

    person: Mapped["Person | None"] = relationship(
        back_populates="commitments",
    )
