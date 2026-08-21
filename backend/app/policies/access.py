from fastapi import HTTPException, status

from app.api.dependencies import CurrentUser
from app.policies.permissions import Permission


def require_permission(
    user: CurrentUser,
    permission: Permission,
) -> None:
    if permission not in user.permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )
