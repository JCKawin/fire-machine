# AI model artifacts

Place trained model files here, for example:

- `model.joblib`
- `model.onnx`
- `model.pt`

The backend loads from `AI_MODEL_PATH` (default `/app/models` in Docker).
Until a real model is present, a rule-based fire-risk scorer is used.
