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
