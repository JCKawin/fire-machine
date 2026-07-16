# Frontend — React (Vite)

Operations dashboard for Fire Machine.

## Scripts

```powershell
npm install
npm run dev      # http://localhost:5173
npm run build    # production bundle → dist/
```

## Environment

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | FastAPI base URL (default `http://localhost:8000`) |

In Docker Compose this is passed as a **build arg** so it is baked into the static bundle.

## Docker

```powershell
docker compose up --build react
```

Served by nginx on host port **3001**.
