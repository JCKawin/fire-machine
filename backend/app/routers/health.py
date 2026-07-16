from fastapi import APIRouter, Request

from app.config import get_settings
from app.schemas import HealthResponse
from app.services.influx import InfluxService

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health(request: Request) -> HealthResponse:
    settings = get_settings()
    influx: InfluxService = request.app.state.influx
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        influx_ok=influx.ping(),
    )


@router.get("/")
def root() -> dict[str, str]:
    settings = get_settings()
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
    }
