# PedagogyX API (boilerplate)

FastAPI service: sessions, health, ASR job enqueue (stub worker).

## Local (without Docker)

```bash
cd services/api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://pedagogyx:pedagogyx_dev@localhost:5432/pedagogyx
uvicorn app.main:app --reload --port 8080
```

Requires Postgres/Redis/MinIO from `infra/compose.dev.yaml`.

## Endpoints

- `GET /health`
- `POST /v1/sessions`
- `GET /v1/sessions/{id}`
- `POST /v1/sessions/{id}/complete`
