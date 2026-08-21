from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_database_session
from app.policies.permissions import Permission


@dataclass(frozen=True)
class CurrentUser:
    id: int
    email: str
    permissions: frozenset[Permission]


def get_current_user() -> CurrentUser:
    return CurrentUser(
        id=1,
        email="local-user@ai-life-manager.invalid",
        permissions=frozenset(
            {
                Permission.READ_TASKS,
                Permission.CREATE_TASK,
                Permission.UPDATE_TASK,
                Permission.DELETE_TASK,
                Permission.READ_PROJECTS,
                Permission.CREATE_PROJECT,
            }
        ),
    )


CurrentUserDependency = Annotated[
    CurrentUser,
    Depends(get_current_user),
]

DatabaseSession = Annotated[
    AsyncSession,
    Depends(get_database_session),
]
