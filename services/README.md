# PedagogyX services (MVP boilerplate)

| Service        | Path          | Role                          |
| -------------- | ------------- | ----------------------------- |
| **api**        | `api/`        | Sessions, health, job enqueue |
| **worker-asr** | `worker-asr/` | ASR queue (stub → whisper)    |
| **worker-cv**  | `worker-cv/`  | Phase 2 stub                  |
| **web**        | `web/`        | Admin UI shell                |

Run full stack: [infra/README.md](../infra/README.md)

RFC: [RFC-0003](../docs/08-rfc-adr/RFC-0003-monorepo-scaffold-post-g2.md)
