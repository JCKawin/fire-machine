# Database & observability

This folder holds **provisioning config** for services that run as Docker images (not custom app code).

## InfluxDB 2.x

Configured in root `docker-compose.yml`:

| Setting | Default |
|---------|---------|
| URL | http://localhost:8086 |
| Org | `fire-machine` |
| Bucket | `sensors` |
| User | `admin` |
| Token | see `.env` / `.env.example` |

### Expected measurements

| Measurement | Written by | Fields / tags |
|-------------|------------|----------------|
| `sensor` | Rust microservice (IoT) | tags: `device_id`; fields: `temperature`, `humidity`, `smoke`, `flame`, … |
| `control` | FastAPI | tags: `device_id`, `action`; field: `issued` |
| `prediction` | FastAPI AI | tags: `device_id`, `risk_level`; field: `fire_probability` |

## Grafana

- UI: http://localhost:3000  
- Default login: `admin` / `admin`  
- Datasource and dashboard are auto-provisioned from:

```
database/grafana/provisioning/
  datasources/influxdb.yml
  dashboards/dashboards.yml
  dashboards/json/fire-machine-overview.json
```
