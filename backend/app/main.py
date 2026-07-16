from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import control, health, predictions, sensors
from app.services.ai_model import FireRiskModel
from app.services.influx import InfluxService


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.influx = InfluxService(settings)
    app.state.ai_model = FireRiskModel(settings.ai_model_path)
    yield
    app.state.influx.close()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Fire Machine backend: sensor queries, fire-risk AI predictions, "
            "and pump/servo control commands. Reads/writes InfluxDB."
        ),
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(sensors.router)
    app.include_router(predictions.router)
    app.include_router(control.router)

    return app


app = create_app()
