from typing import Any, Dict

from fastapi import FastAPI, status

from src.config import settings


app = FastAPI(
    title="AI Gateway",
    version="0.1.0",
    description="",
)


@app.get("/health", status_code=status.HTTP_200_OK)
async def system_health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }
