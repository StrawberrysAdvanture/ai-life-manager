from app.models.agent_action import AgentAction, AgentActionStatus
from app.repositories.agent_action import AgentActionRepository
from app.schemas.agent_action import AgentActionCreate


class AgentActionService:
    def __init__(
        self,
        repository: AgentActionRepository,
    ) -> None:
        self.repository = repository

    async def create_action(
        self,
        action_data: AgentActionCreate,
        user_id: int,
    ) -> AgentAction:
        action = AgentAction(
            user_id=user_id,
            action_type=action_data.action_type,
            tool_name=action_data.tool_name,
            input_data=action_data.input_data,
            status=AgentActionStatus.PENDING,
            requires_approval=action_data.requires_approval,
            approval_id=None,
            completed_at=None,
        )

        return await self.repository.create(action)

    async def list_actions(
        self,
        user_id: int,
    ) -> list[AgentAction]:
        return await self.repository.get_all_for_user(user_id)
