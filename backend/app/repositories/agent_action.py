from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent_action import AgentAction


class AgentActionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        action: AgentAction,
    ) -> AgentAction:
        self.session.add(action)
        await self.session.commit()
        await self.session.refresh(action)

        return action

    async def get_all_for_user(self, user_id: int) -> list[AgentAction]:
        result = await self.session.execute(
            select(AgentAction)
            .where(AgentAction.user_id == user_id)
            .order_by(AgentAction.created_at.desc())
        )

        return list(result.scalars().all())
