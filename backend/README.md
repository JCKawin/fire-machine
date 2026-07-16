# Backend — Python FastAPI + AI

Serves the React app, talks to InfluxDB, and runs fire-risk scoring.

## Layout

```
backend/
  app/
    main.py              # FastAPI entry
    config.py            # Settings from env
    schemas.py           # Pydantic models
    routers/
      health.py
      sensors.py
      predictions.py
      control.py
    services/
      influx.py          # InfluxDB client
      ai_model.py        # Rule-based model (swap for real weights)
  models/                # Drop trained artifacts here
  Dockerfile
  requirements.txt
```

## Run with Docker

From repo root:

```powershell
docker compose up --build fastapi
```

## Run locally

Requires InfluxDB (e.g. `docker compose up influxdb`).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Env vars

| Variable | Default |
|----------|---------|
| `INFLUX_URL` | `http://localhost:8086` |
| `INFLUX_ORG` | `fire-machine` |
| `INFLUX_BUCKET` | `sensors` |
| `INFLUX_TOKEN` | (see `.env.example`) |
| `AI_MODEL_PATH` | `./models` |
| `CORS_ORIGINS` | `http://localhost:5173,http://localhost:3001` |
