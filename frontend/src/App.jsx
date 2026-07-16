import { useCallback, useEffect, useState } from "react";
import {
  API_URL,
  getHealth,
  getSensors,
  predictRisk,
  sendControlCommand,
} from "./api";
import "./App.css";

const DEVICES = ["device-1", "device-2", "device-3"];
const ACTIONS = [
  { value: "pump_on", label: "Pump ON" },
  { value: "pump_off", label: "Pump OFF" },
  { value: "servo_open", label: "Servo open" },
  { value: "servo_close", label: "Servo close" },
];

function riskClass(level) {
  if (!level) return "";
  return `risk-${level}`;
}

export default function App() {
  const [health, setHealth] = useState(null);
  const [sensors, setSensors] = useState([]);
  const [deviceId, setDeviceId] = useState("device-1");
  const [prediction, setPrediction] = useState(null);
  const [controlMsg, setControlMsg] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Manual prediction form (when no live data yet)
  const [form, setForm] = useState({
    temperature: 45,
    humidity: 30,
    smoke: 0.2,
    flame: 0.1,
  });

  const refresh = useCallback(async () => {
    setError("");
    try {
      const [h, s] = await Promise.all([
        getHealth(),
        getSensors({ deviceId, limit: 15 }),
      ]);
      setHealth(h);
      setSensors(s.readings || []);
    } catch (err) {
      setError(err.message || "Failed to reach API");
    }
  }, [deviceId]);

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, 10_000);
    return () => clearInterval(id);
  }, [refresh]);

  async function onPredict() {
    setLoading(true);
    setError("");
    try {
      const payload = {
        device_id: deviceId,
        temperature: Number(form.temperature),
        humidity: Number(form.humidity),
        smoke: Number(form.smoke),
        flame: Number(form.flame),
      };
      const result = await predictRisk(payload);
      setPrediction(result);
    } catch (err) {
      setError(err.message || "Prediction failed");
    } finally {
      setLoading(false);
    }
  }

  async function onPredictFromDevice() {
    setLoading(true);
    setError("");
    try {
      const result = await predictRisk({ device_id: deviceId });
      setPrediction(result);
    } catch (err) {
      setError(err.message || "Prediction failed");
    } finally {
      setLoading(false);
    }
  }

  async function onControl(action) {
    setLoading(true);
    setError("");
    setControlMsg("");
    try {
      const result = await sendControlCommand({
        device_id: deviceId,
        action,
      });
      setControlMsg(result.message);
    } catch (err) {
      setError(err.message || "Control command failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header className="header">
        <div>
          <p className="eyebrow">Fire Machine</p>
          <h1>Operations dashboard</h1>
          <p className="muted">
            React → FastAPI → InfluxDB · Edge devices via Rust gateway
          </p>
        </div>
        <div className="status-card">
          <div className="status-row">
            <span>API</span>
            <strong>{API_URL}</strong>
          </div>
          <div className="status-row">
            <span>Backend</span>
            <strong className={health?.status === "ok" ? "ok" : "bad"}>
              {health?.status || "offline"}
            </strong>
          </div>
          <div className="status-row">
            <span>InfluxDB</span>
            <strong className={health?.influx_ok ? "ok" : "bad"}>
              {health ? (health.influx_ok ? "connected" : "down") : "…"}
            </strong>
          </div>
          <button type="button" className="ghost" onClick={refresh}>
            Refresh
          </button>
        </div>
      </header>

      {error ? <div className="banner error">{error}</div> : null}
      {controlMsg ? <div className="banner ok">{controlMsg}</div> : null}

      <section className="grid">
        <article className="card">
          <h2>Device</h2>
          <label className="field">
            <span>Edge unit</span>
            <select
              value={deviceId}
              onChange={(e) => setDeviceId(e.target.value)}
            >
              {DEVICES.map((id) => (
                <option key={id} value={id}>
                  {id}
                </option>
              ))}
            </select>
          </label>

          <h3>Control</h3>
          <div className="btn-row">
            {ACTIONS.map((a) => (
              <button
                key={a.value}
                type="button"
                disabled={loading}
                onClick={() => onControl(a.value)}
              >
                {a.label}
              </button>
            ))}
          </div>
        </article>

        <article className="card">
          <h2>Fire-risk AI</h2>
          <div className="form-grid">
            {["temperature", "humidity", "smoke", "flame"].map((key) => (
              <label key={key} className="field">
                <span>{key}</span>
                <input
                  type="number"
                  step="0.01"
                  value={form[key]}
                  onChange={(e) =>
                    setForm((prev) => ({ ...prev, [key]: e.target.value }))
                  }
                />
              </label>
            ))}
          </div>
          <div className="btn-row">
            <button type="button" disabled={loading} onClick={onPredict}>
              Predict from form
            </button>
            <button
              type="button"
              className="ghost"
              disabled={loading}
              onClick={onPredictFromDevice}
            >
              Predict from latest device data
            </button>
          </div>

          {prediction ? (
            <div className={`prediction ${riskClass(prediction.risk_level)}`}>
              <div className="prediction-head">
                <strong>{prediction.risk_level.toUpperCase()}</strong>
                <span>
                  {(prediction.fire_probability * 100).toFixed(1)}% probability
                </span>
              </div>
              <p className="muted">Model: {prediction.model}</p>
              <ul>
                {prediction.reasons.map((r) => (
                  <li key={r}>{r}</li>
                ))}
              </ul>
              <p>
                <strong>Actions:</strong>{" "}
                {prediction.recommended_actions.join(", ")}
              </p>
            </div>
          ) : null}
        </article>

        <article className="card wide">
          <h2>Recent sensor readings</h2>
          {sensors.length === 0 ? (
            <p className="muted">
              No data yet. Once the Rust microservice writes sensor points to
              InfluxDB (measurement <code>sensor</code>), they appear here.
            </p>
          ) : (
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>Device</th>
                    <th>Temp</th>
                    <th>Humidity</th>
                    <th>Smoke</th>
                    <th>Flame</th>
                  </tr>
                </thead>
                <tbody>
                  {sensors.map((row, idx) => (
                    <tr key={`${row.device_id}-${row.timestamp}-${idx}`}>
                      <td>
                        {row.timestamp
                          ? new Date(row.timestamp).toLocaleString()
                          : "—"}
                      </td>
                      <td>{row.device_id}</td>
                      <td>{fmt(row.temperature)}</td>
                      <td>{fmt(row.humidity)}</td>
                      <td>{fmt(row.smoke)}</td>
                      <td>{fmt(row.flame)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </article>
      </section>

      <footer className="footer">
        <span>Grafana: http://localhost:3000</span>
        <span>InfluxDB: http://localhost:8086</span>
        <span>API docs: {API_URL}/docs</span>
      </footer>
    </div>
  );
}

function fmt(value) {
  if (value === null || value === undefined) return "—";
  return Number(value).toFixed(2);
}
