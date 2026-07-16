from fastapi import APIRouter, Request

from app.schemas import PredictionRequest, PredictionResponse
from app.services.ai_model import FireRiskModel
from app.services.influx import InfluxService

router = APIRouter(prefix="/api/predictions", tags=["predictions"])


@router.post("/risk", response_model=PredictionResponse)
def predict_fire_risk(payload: PredictionRequest, request: Request) -> PredictionResponse:
    """
    Run the AI fire-risk model.

    If sensor fields are omitted and a device_id is provided, the latest
    InfluxDB reading for that device is used when available.
    """
    influx: InfluxService = request.app.state.influx
    model: FireRiskModel = request.app.state.ai_model

    data = payload.model_copy()
    if data.device_id and all(
        v is None for v in (data.temperature, data.humidity, data.smoke, data.flame)
    ):
        latest = influx.query_latest_sensors(device_id=data.device_id, limit=1)
        if latest:
            reading = latest[0]
            data.temperature = reading.temperature
            data.humidity = reading.humidity
            data.smoke = reading.smoke
            data.flame = reading.flame

    result = model.predict(data)

    try:
        influx.write_prediction(
            device_id=result.device_id,
            risk_level=result.risk_level.value,
            fire_probability=result.fire_probability,
        )
    except Exception:
        # Prediction still succeeds even if telemetry write fails
        pass

    return result
