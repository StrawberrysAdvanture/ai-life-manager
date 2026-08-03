from fastapi import FastAPI

app = FastAPI(
    title="Ai Life Manager API",
    description="Backend API for AI life manager project.",
    version="0.1.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"name": "AI life Manager", "status": "running"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}
