from datetime import datetime, timezone

from fastapi import APIRouter, Request

from app.schemas import ControlCommand, ControlResponse
from app.services.influx import InfluxService

router = APIRouter(prefix="/api/control", tags=["control"])


@router.post("/command", response_model=ControlResponse)
def issue_control_command(command: ControlCommand, request: Request) -> ControlResponse:
    """
    Record a control command (pump / servo).

    Edge devices (or the Rust gateway) can poll / subscribe to act on these.
    For now we log the event into InfluxDB measurement `control`.
    """
    influx: InfluxService = request.app.state.influx

    try:
        ts = influx.write_control_event(
            device_id=command.device_id,
            action=command.action,
            note=command.note,
        )
        return ControlResponse(
            accepted=True,
            device_id=command.device_id,
            action=command.action,
            message=f"Command '{command.action.value}' queued for {command.device_id}",
            timestamp=ts,
        )
    except Exception as exc:
        return ControlResponse(
            accepted=False,
            device_id=command.device_id,
            action=command.action,
            message=f"Failed to persist command: {exc}",
            timestamp=datetime.now(timezone.utc),
        )
