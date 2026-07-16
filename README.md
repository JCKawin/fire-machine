# Fire Machine

IoT fire-safety stack: edge devices → Rust ingestion → InfluxDB → FastAPI (AI) → React UI + Grafana.

```
[ sensors / servo / water pump ]  x3
              │ WiFi
              ▼
         ┌─ SERVER ──────────────────┐
         │  Rust microservice :8081  │──► InfluxDB :8086
         │  Python FastAPI    :8000  │◄─┘     │
         │    └─ AI model            │        ▼
         └───────────┬───────────────┘    Grafana :3000
                     │
                     ▼
              React app :3001
```

## Projects

| Path | Role | Status in this setup |
|------|------|----------------------|
| `backend/` | FastAPI + fire-risk AI | Scaffolded |
| `frontend/` | React (Vite) dashboard | Scaffolded |
| `database/` | Influx/Grafana provisioning | Scaffolded |
| `rust-microservice/` | IoT WiFi gateway | Separate (your work) |
| `emmbedded/` | Edge firmware | Separate (your work) |

## Quick start (Docker)

```powershell
copy .env.example .env
docker compose up --build
```

| Service | URL |
|---------|-----|
| React UI | http://localhost:3001 |
| FastAPI docs | http://localhost:8000/docs |
| Grafana | http://localhost:3000 (`admin` / `admin`) |
| InfluxDB | http://localhost:8086 |

> **Note:** The `rust` service is behind Compose profile `iot` so the rest of the stack starts without it:
>
> ```powershell
> docker compose up --build                    # influxdb, grafana, fastapi, react
> docker compose --profile iot up --build      # also start rust
> ```

## Local development

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:INFLUX_URL = "http://localhost:8086"
uvicorn app.main:app --reload --port 8000
```

### Frontend

```powershell
cd frontend
npm install
$env:VITE_API_URL = "http://localhost:8000"
npm run dev
```

## API surface (initial)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness + Influx ping |
| `GET` | `/api/sensors` | Query latest sensor rows from Influx |
| `POST` | `/api/predictions/risk` | Fire-risk AI inference |
| `POST` | `/api/control/command` | Queue pump/servo command |

## Environment

See `.env.example` for Influx, Grafana, CORS, and API URL variables.
