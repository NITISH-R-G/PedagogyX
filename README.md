# PedagogyX

**Multimodal AI classroom intelligence and teacher optimization platform** (planning phase).

## Current Status

🟡 **Phase 0 + MVP boilerplate** — `services/` and `infra/compose.dev.yaml` runnable locally.  
**Real school / student data** requires **G2** (see [docs/README.md](docs/README.md)).

## Documentation

Start here: **[docs/README.md](docs/README.md)** · **Developing:** [DEVELOPING.md](DEVELOPING.md)

| Priority action                    | Document                                                                                                                                              |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **G2 — counsel (1-click prep)**    | [COUNSEL_OUTREACH_PACKAGE.md](docs/07-compliance-ethics/COUNSEL_OUTREACH_PACKAGE.md) · [Issue #11](https://github.com/NITISH-R-G/PedagogyX/issues/11) |
| **Run dev stack**                  | `make dev-up` or [DEVELOPING.md](DEVELOPING.md)                                                                                                       |
| Dev (works **without 5070 today**) | `./scripts/dev-verify.sh` · [DEV_WITHOUT_GPU.md](benchmarks/DEV_WITHOUT_GPU.md)                                                                       |
| Active sprint                      | [SPRINT_03_MVP_PREP.md](docs/09-agile/SPRINT_03_MVP_PREP.md)                                                                                          |
| Architecture                       | [SYSTEM_ARCHITECTURE.md](docs/05-architecture/SYSTEM_ARCHITECTURE.md)                                                                                 |

## Repository Contents

| Path                  | Contents                                |
| --------------------- | --------------------------------------- |
| `docs/`               | Phase 0 RFCs, ADRs, sprint plans        |
| `services/`           | API, worker-asr (stub), web admin shell |
| `infra/`              | `compose.dev.yaml` local stack          |
| `benchmarks/`         | RTX 5070 validation scripts (ADR-0006)  |
| `tools/mock-capture/` | Synthetic session CLI                   |

## License

TBD by founder.
