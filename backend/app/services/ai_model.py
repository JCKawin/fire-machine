from __future__ import annotations

from pathlib import Path

from app.schemas import PredictionRequest, PredictionResponse, RiskLevel


class FireRiskModel:
    """
    Placeholder AI model for fire-risk scoring.

    Swap `_score` with a real model loaded from `model_path`
    (e.g. scikit-learn, ONNX Runtime, or a neural net).
    """

    def __init__(self, model_path: str) -> None:
        self.model_path = Path(model_path)
        self.model_name = "fire-risk-v0-rules"
        self._weights_loaded = self._try_load_weights()

    def _try_load_weights(self) -> bool:
        """Look for a real model artifact; fall back to rules if missing."""
        candidates = [
            self.model_path / "model.joblib",
            self.model_path / "model.onnx",
            self.model_path / "model.pt",
        ]
        return any(path.exists() for path in candidates)

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        temperature = request.temperature if request.temperature is not None else 25.0
        humidity = request.humidity if request.humidity is not None else 50.0
        smoke = request.smoke if request.smoke is not None else 0.0
        flame = request.flame if request.flame is not None else 0.0

        score, reasons = self._score(temperature, humidity, smoke, flame)
        risk = self._risk_from_score(score)
        actions = self._recommend(risk)

        return PredictionResponse(
            device_id=request.device_id,
            risk_level=risk,
            fire_probability=round(score, 3),
            reasons=reasons,
            recommended_actions=actions,
            model=self.model_name + ("+weights" if self._weights_loaded else "+rules"),
        )

    def _score(
        self,
        temperature: float,
        humidity: float,
        smoke: float,
        flame: float,
    ) -> tuple[float, list[str]]:
        score = 0.0
        reasons: list[str] = []

        # Flame sensor dominates
        if flame >= 0.7:
            score += 0.55
            reasons.append("Strong flame signal detected")
        elif flame >= 0.3:
            score += 0.25
            reasons.append("Elevated flame signal")

        # Smoke concentration
        if smoke >= 0.6:
            score += 0.3
            reasons.append("High smoke level")
        elif smoke >= 0.25:
            score += 0.15
            reasons.append("Moderate smoke level")

        # Temperature
        if temperature >= 70:
            score += 0.25
            reasons.append(f"Very high temperature ({temperature:.1f}°C)")
        elif temperature >= 50:
            score += 0.12
            reasons.append(f"Elevated temperature ({temperature:.1f}°C)")

        # Dry air increases risk slightly
        if humidity <= 20 and temperature >= 40:
            score += 0.08
            reasons.append("Low humidity with heat")

        score = min(max(score, 0.0), 1.0)
        if not reasons:
            reasons.append("Readings within normal operating range")

        return score, reasons

    @staticmethod
    def _risk_from_score(score: float) -> RiskLevel:
        if score >= 0.8:
            return RiskLevel.critical
        if score >= 0.55:
            return RiskLevel.high
        if score >= 0.3:
            return RiskLevel.medium
        return RiskLevel.low

    @staticmethod
    def _recommend(risk: RiskLevel) -> list[str]:
        if risk == RiskLevel.critical:
            return ["pump_on", "servo_open", "alert_operators"]
        if risk == RiskLevel.high:
            return ["pump_on", "alert_operators"]
        if risk == RiskLevel.medium:
            return ["increase_monitoring", "prepare_pump"]
        return ["continue_monitoring"]
