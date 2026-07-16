from fastapi import APIRouter, Query, Request

from app.schemas import SensorQueryResponse
from app.services.influx import InfluxService

router = APIRouter(prefix="/api/sensors", tags=["sensors"])


@router.get("", response_model=SensorQueryResponse)
def list_sensor_readings(
    request: Request,
    device_id: str | None = Query(default=None, description="Filter by edge device id"),
    limit: int = Query(default=50, ge=1, le=500),
    range_minutes: int = Query(default=60, ge=1, le=10_080),
) -> SensorQueryResponse:
    """Latest sensor readings from InfluxDB (written by the Rust microservice)."""
    influx: InfluxService = request.app.state.influx
    readings = influx.query_latest_sensors(
        device_id=device_id,
        limit=limit,
        range_minutes=range_minutes,
    )
    return SensorQueryResponse(count=len(readings), readings=readings)
