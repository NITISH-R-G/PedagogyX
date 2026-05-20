# RFC-0003 — Monorepo Scaffold (Post-G2)

| Field       | Value                                                                                                                                             |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Status**  | Draft — **no implementation until G2**                                                                                                            |
| **Author**  | Platform (Phase 0)                                                                                                                                |
| **Depends** | [SPRINT_03_MVP_PREP.md](../09-agile/SPRINT_03_MVP_PREP.md), [DOCKER_COMPOSE_PILOT_STACK.md](../06-stack-evaluation/DOCKER_COMPOSE_PILOT_STACK.md) |

---

## Summary

Define the **first-commit** repository layout and CI expectations for the MVP vertical slice. This RFC authorizes structure only; creating directories under `services/` waits for **G2** (India DPDP counsel memo).

---

## Goals

- One `docker compose -f infra/compose.dev.yaml up` brings Postgres, MinIO, API, worker-asr, and web shell.
- Capture agents remain **out-of-repo** spikes until RFC-0002 is accepted (Win/Android).
- Pedagogy metrics v1: **talk ratio** only (M-A dashboard widget, M-B latency target).

---

## Proposed layout

```text
services/
  api/                 # REST + upload ingest; Go or FastAPI (decide at G2+ kickoff)
  worker-asr/          # faster-whisper container; EN first
  worker-cv/           # empty README stub — no jobs until Phase 2
  web/                 # Next.js admin (wireframes 1–3)
packages/
  capture-core/        # optional shared types; Rust FFI deferred
infra/
  compose.dev.yaml     # local all-in-one
  compose.edge.yaml    # LAN buffer profile (Hybrid D-PROC)
  compose.cloud.yaml   # GPU worker profile (pilot)
benchmarks/              # existing ADR-0006 validation (unchanged)
docs/                  # Phase 0 corpus (unchanged)
scripts/
  dev-verify.sh        # extend with compose health when code exists
```

---

## CI (post-scaffold)

| Job             | Trigger | Scope                              |
| --------------- | ------- | ---------------------------------- |
| `docs-verify`   | PR      | markdownlint + prettier (existing) |
| `dev-verify`    | PR      | docs + optional CPU benchmarks     |
| `compose-smoke` | PR/main | `docker compose up` + `/health`    |

**Cloud Agent VMs:** run `docs-verify` only until GPU host publishes CUDA JSON.

---

## Service boundaries (v0)

| Service      | Owns                             | Must not own (v0)    |
| ------------ | -------------------------------- | -------------------- |
| `api`        | sessions, upload URLs, auth stub | ASR, talk ratio math |
| `worker-asr` | transcript JSON, RTF logs        | UI, consent records  |
| `web`        | admin read models                | direct MinIO writes  |

Event contract: JSON job envelope on Redis or Postgres queue — detail in API OpenAPI draft (Sprint 03 S03-04).

---

## Non-goals (RFC-0003)

- Student identification, grade export, district heatmaps
- LLM coaching narrative (defer to Phase 2)
- Production K8s / Terraform (pilot = Compose on founder VPS)

---

## Acceptance (RFC)

- [ ] Founder / arch sign-off recorded in PR or ADR comment
- [ ] G2 gate 🟢 in [docs/README.md](../README.md)
- [ ] First PR creating `services/` references this RFC in description

---

## References

- [ADR-0008](ADR-0008-d-proc-hybrid-central-ml.md) — Hybrid edge + cloud
- [CENTRAL_OSS_BACKEND_SPEC.md](../05-architecture/CENTRAL_OSS_BACKEND_SPEC.md)
- [PRODUCTION_CLIENT_SPEC.md](../05-architecture/PRODUCTION_CLIENT_SPEC.md)
