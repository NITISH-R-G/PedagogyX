# Sprint 02 — Legal Gate & Dev Validation

| Field                   | Value                                                              |
| ----------------------- | ------------------------------------------------------------------ |
| **Depends on**          | Sprint 01 ✅ (docs complete)                                       |
| **Goal**                | **G2 legal path** + run RTX 5070 benchmarks on founder dev machine |
| **Implementation code** | **Forbidden** until G2 sign-off                                    |

---

## Backlog

| ID     | Deliverable                                                                                                                                   | Owner   | Status                                                                    |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------- |
| S02-01 | Send counsel brief — [COUNSEL_OUTREACH_PACKAGE.md](../07-compliance-ethics/COUNSEL_OUTREACH_PACKAGE.md) + `./scripts/build-counsel-packet.sh` | Founder | 📋 Ready — [Issue #11](https://github.com/NITISH-R-G/PedagogyX/issues/11) |
| S02-02 | Receive signed legal memo → unlock **G2**                                                                                                     | Founder | 🔴 Blocked                                                                |
| S02-03 | Run `benchmarks/bench_full_pipeline.sh` on RTX 5070                                                                                           | ML/Dev  | 🟡 CPU baseline done; CUDA pending                                        |
| S02-04 | Update [GPU_PILOT_COST_MODEL.md](../05-architecture/GPU_PILOT_COST_MODEL.md) with measured RTF                                                | Arch    | 🟡 Partial (CPU baseline linked)                                          |
| S02-05 | Privacy notice + consent flow wireframes (post-counsel)                                                                                       | Product |                                                                           |
| S02-06 | Pilot school named + D-DEV device checklist filled                                                                                            | Founder |                                                                           |
| S02-07 | RFC-0002 formal acceptance sign-off                                                                                                           | Arch    |                                                                           |

---

## Exit criteria (Sprint 02)

- **G2** 🟢 Legal memo received
- Benchmark JSON in `benchmarks/results/` from real GPU (not CPU smoke test)
- Pilot school identified
- Ready to authorize **MVP codebase** (Sprint 03+)

---

## After G2 — first code vertical slice (preview)

1. Docker Compose `dev` profile from [DOCKER_COMPOSE_PILOT_STACK.md](../06-stack-evaluation/DOCKER_COMPOSE_PILOT_STACK.md)
2. Mock capture agent uploading test chunks
3. API + worker-asr hello path
4. Admin dashboard static shell (wireframes)

See [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md).
