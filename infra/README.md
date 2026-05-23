# Infrastructure (Compose)

## Dev stack

```bash
docker compose -f infra/compose.dev.yaml up --build
```

| Service   | URL                             |
| --------- | ------------------------------- |
| API       | http://localhost:8080/health    |
| Admin web | http://localhost:3000           |
| MinIO     | http://localhost:9001 (console) |
| Postgres  | localhost:5432                  |

Stop:

```bash
docker compose -f infra/compose.dev.yaml down
```

Smoke test (requires Docker):

```bash
./scripts/compose-smoke.sh
```

**Production pilot data** still requires G2 sign-off — use synthetic fixtures only until counsel memo is on file.

**Schema migrations:** SQL files in `sql/` run on first Postgres volume init. After pulling new migrations, reset dev DB:

```bash
docker compose -f infra/compose.dev.yaml down -v
docker compose -f infra/compose.dev.yaml up --build
```

## Vertical slice (Sprint 03)

1. `make dev-up`
2. `make mock-capture` — upload → ASR stub → talk ratio → admin UI
3. Open http://localhost:3000 for M-A / M-B widgets

Optional ASR: set `WORKER_MODE=whisper` and `WHISPER_MODEL=tiny` on `worker-asr` (CPU).
