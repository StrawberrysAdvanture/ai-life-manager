from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.tasks import router as tasks_router
from app.database import get_database_session

app = FastAPI(
    title="Ai Life Manager API",
    description="Backend API for AI life manager project.",
    version="0.1.0",
)
DatabaseSession = Annotated[AsyncSession, Depends(get_database_session)]

app.include_router(tasks_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": "AI Life Manager",
        "status": "running",
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/health/database")
async def database_health_check(
    session: DatabaseSession,
) -> dict[str, str]:
    await session.execute(text("SELECT 1"))

    return {"status": "healthy"}
