# Sprint 02 — Legal Gate & Dev Validation

| Field                   | Value                                                                                    |
| ----------------------- | ---------------------------------------------------------------------------------------- |
| **Depends on**          | Sprint 01 ✅ (docs complete)                                                             |
| **Goal**                | **G2 legal path** + benchmarks (**CPU OK today**, GPU profile on RTX 5070 from tomorrow) |
| **Implementation code** | **Forbidden** until G2 sign-off                                                          |

---

## Backlog

| ID     | Deliverable                                                                                                                                   | Owner   | Status                                                                    |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------- |
| S02-01 | Send counsel brief — [COUNSEL_OUTREACH_PACKAGE.md](../07-compliance-ethics/COUNSEL_OUTREACH_PACKAGE.md) + `./scripts/build-counsel-packet.sh` | Founder | 📋 Ready — [Issue #11](https://github.com/NITISH-R-G/PedagogyX/issues/11) |
| S02-02 | Receive signed legal memo → unlock **G2**                                                                                                     | Founder | 🔴 Blocked                                                                |
| S02-03 | `./bench_full_pipeline.sh cpu` (today) · `gpu` (RTX 5070 tomorrow) — see [DEV_WITHOUT_GPU.md](../../benchmarks/DEV_WITHOUT_GPU.md)            | ML/Dev  | ✅ CPU profile passing                                                    |
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

**Next sprint (after G2):** [SPRINT_03_MVP_PREP.md](SPRINT_03_MVP_PREP.md) · [RFC-0003](../08-rfc-adr/RFC-0003-monorepo-scaffold-post-g2.md).
