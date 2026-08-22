from fastapi import APIRouter

from app.api.dependencies import CurrentUserDependency, DatabaseSession
from app.models.agent_action import AgentAction
from app.policies.access import require_permission
from app.policies.permissions import Permission
from app.repositories.agent_action import AgentActionRepository
from app.schemas.agent_action import AgentActionRead
from app.services.agent_action import AgentActionService

router = APIRouter(
    prefix="/agent-actions",
    tags=["agent-actions"],
)


@router.get(
    "",
    response_model=list[AgentActionRead],
)
async def list_agent_actions(
    session: DatabaseSession,
    current_user: CurrentUserDependency,
) -> list[AgentAction]:
    require_permission(
        current_user,
        Permission.READ_AGENT_ACTIONS,
    )

    repository = AgentActionRepository(session)
    service = AgentActionService(repository)

    return await service.list_actions(
        user_id=current_user.id,
    )
