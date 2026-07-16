from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from app.config import Settings
from app.schemas import ControlAction, SensorReading


class InfluxService:
    """Read/write sensor and control data in InfluxDB 2.x."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = InfluxDBClient(
            url=settings.influx_url,
            token=settings.influx_token,
            org=settings.influx_org,
            timeout=10_000,
        )
        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)
        self._query_api = self._client.query_api()

    def close(self) -> None:
        self._client.close()

    def ping(self) -> bool:
        try:
            return bool(self._client.ping())
        except Exception:
            return False

    def query_latest_sensors(
        self,
        device_id: str | None = None,
        limit: int = 50,
        range_minutes: int = 60,
    ) -> list[SensorReading]:
        device_filter = ""
        if device_id:
            device_filter = f'  |> filter(fn: (r) => r["device_id"] == "{device_id}")\n'

        flux = f'''
from(bucket: "{self._settings.influx_bucket}")
  |> range(start: -{range_minutes}m)
  |> filter(fn: (r) => r._measurement == "sensor")
{device_filter}  |> pivot(rowKey: ["_time", "device_id"], columnKey: ["_field"], valueColumn: "_value")
  |> sort(columns: ["_time"], desc: true)
  |> limit(n: {limit})
'''
        try:
            tables = self._query_api.query(flux, org=self._settings.influx_org)
        except Exception:
            return []

        readings: list[SensorReading] = []
        for table in tables:
            for record in table.records:
                values = record.values
                readings.append(
                    SensorReading(
                        device_id=str(values.get("device_id", "unknown")),
                        temperature=_as_float(values.get("temperature")),
                        humidity=_as_float(values.get("humidity")),
                        smoke=_as_float(values.get("smoke")),
                        flame=_as_float(values.get("flame")),
                        timestamp=record.get_time(),
                        fields={
                            k: v
                            for k, v in values.items()
                            if not k.startswith("_") and k not in {"result", "table", "device_id"}
                        },
                    )
                )
        return readings

    def write_control_event(
        self,
        device_id: str,
        action: ControlAction,
        note: str | None = None,
    ) -> datetime:
        now = datetime.now(timezone.utc)
        point = (
            Point("control")
            .tag("device_id", device_id)
            .tag("action", action.value)
            .field("issued", 1)
            .time(now, WritePrecision.NS)
        )
        if note:
            point = point.field("note", note)

        self._write_api.write(
            bucket=self._settings.influx_bucket,
            org=self._settings.influx_org,
            record=point,
        )
        return now

    def write_prediction(
        self,
        device_id: str | None,
        risk_level: str,
        fire_probability: float,
    ) -> None:
        point = (
            Point("prediction")
            .tag("risk_level", risk_level)
            .field("fire_probability", float(fire_probability))
            .time(datetime.now(timezone.utc), WritePrecision.NS)
        )
        if device_id:
            point = point.tag("device_id", device_id)

        self._write_api.write(
            bucket=self._settings.influx_bucket,
            org=self._settings.influx_org,
            record=point,
        )


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
