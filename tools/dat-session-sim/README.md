# DAT session simulator

Dev harness for **Meta Wearables DAT–style** lifecycle (session + camera stream) wired to PedagogyX API.

Maps to [RFC-0002](../../docs/08-rfc-adr/RFC-0002-capture-agent-sync-protocol.md) hot-path states.

## Prerequisites

```bash
docker compose -f infra/compose.dev.yaml up --build
pip install -r tools/dat-session-sim/requirements.txt
```

Fresh DB if `003_dat_sessions.sql` is new:

```bash
docker compose -f infra/compose.dev.yaml down -v && docker compose -f infra/compose.dev.yaml up --build
```

## Run

```bash
python tools/dat-session-sim/dat_session_cli.py run
python tools/dat-session-sim/dat_session_cli.py run --no-camera --frames 5
```

## API (manual)

| Step | Endpoint |
| ---- | -------- |
| Create | `POST /v1/dat-sessions` |
| Start session | `POST /v1/dat-sessions/{id}/start` |
| Start stream | `POST /v1/dat-sessions/{id}/stream/start` |
| Custom event | `POST /v1/dat-sessions/{id}/lifecycle` |
| Stop (cascade) | `POST /v1/dat-sessions/{id}/stop` |
| Audit log | `GET /v1/dat-sessions/{id}` |

When stream reaches **STREAMING**, API links a `pedagogy_session_id` for chunk upload.

## Production Android (Meta DAT)

On device, use [Meta Wearables DAT SDK](https://wearables.developer.meta.com/) (`DeviceSession` + `addStream`). Point lifecycle webhooks at these API routes from your capture agent.
