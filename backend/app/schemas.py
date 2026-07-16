from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DeviceId(str, Enum):
    device_1 = "device-1"
    device_2 = "device-2"
    device_3 = "device-3"


class SensorReading(BaseModel):
    device_id: str
    temperature: float | None = None
    humidity: float | None = None
    smoke: float | None = None
    flame: float | None = None
    timestamp: datetime | None = None
    fields: dict[str, Any] = Field(default_factory=dict)


class SensorQueryResponse(BaseModel):
    count: int
    readings: list[SensorReading]


class ControlAction(str, Enum):
    pump_on = "pump_on"
    pump_off = "pump_off"
    servo_open = "servo_open"
    servo_close = "servo_close"


class ControlCommand(BaseModel):
    device_id: str = Field(..., examples=["device-1"])
    action: ControlAction
    note: str | None = None


class ControlResponse(BaseModel):
    accepted: bool
    device_id: str
    action: ControlAction
    message: str
    timestamp: datetime


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class PredictionRequest(BaseModel):
    device_id: str | None = None
    temperature: float | None = None
    humidity: float | None = None
    smoke: float | None = None
    flame: float | None = None


class PredictionResponse(BaseModel):
    device_id: str | None
    risk_level: RiskLevel
    fire_probability: float = Field(..., ge=0.0, le=1.0)
    reasons: list[str]
    recommended_actions: list[str]
    model: str


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    influx_ok: bool
