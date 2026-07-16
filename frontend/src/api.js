const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed (${response.status})`);
  }

  return response.json();
}

export function getHealth() {
  return request("/health");
}

export function getSensors({ deviceId, limit = 20 } = {}) {
  const params = new URLSearchParams({ limit: String(limit) });
  if (deviceId) params.set("device_id", deviceId);
  return request(`/api/sensors?${params.toString()}`);
}

export function predictRisk(payload) {
  return request("/api/predictions/risk", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function sendControlCommand(payload) {
  return request("/api/control/command", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export { API_URL };
