# Developing PedagogyX (quick reference)

**MVP boilerplate** is in `services/` + `infra/` (founder-authorized scaffold). **Real school data** still requires **G2** counsel sign-off.

---

## Run the dev stack (Docker)

```bash
docker compose -f infra/compose.dev.yaml up --build
# or: make dev-up
```

| URL                          | Service         |
| ---------------------------- | --------------- |
| http://localhost:8080/health | API             |
| http://localhost:3000        | Admin web shell |
| http://localhost:9001        | MinIO console   |

Smoke test: `./scripts/compose-smoke.sh` · Mock session: `make mock-capture` · DAT + camera: `make dat-session`

---

## Today (no RTX 5070)

```bash
./scripts/dev-verify.sh          # lint + CPU benchmarks (~2–5 min)
./scripts/dev-verify.sh --docs-only   # lint only (~30 s)
```

Details: [benchmarks/DEV_WITHOUT_GPU.md](benchmarks/DEV_WITHOUT_GPU.md)

---

## Tomorrow (RTX 5070)

```bash
cd benchmarks
ollama pull qwen2.5:7b-instruct-q4_K_M
./bench_full_pipeline.sh gpu
```

---

## Founder actions (unblock MVP)

| Action                   | Doc / link                                                                                                                                            |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| G2 checklist (all steps) | [G2_READINESS_CHECKLIST.md](docs/07-compliance-ethics/G2_READINESS_CHECKLIST.md)                                                                      |
| Send counsel email       | [COUNSEL_OUTREACH_PACKAGE.md](docs/07-compliance-ethics/COUNSEL_OUTREACH_PACKAGE.md) · [Issue #11](https://github.com/NITISH-R-G/PedagogyX/issues/11) |
| Name pilot school        | [PILOT_SCHOOL_INTAKE.md](docs/01-phase0-founder-interrogation/PILOT_SCHOOL_INTAKE.md)                                                                 |

---

## Sprint 03 next steps

Boilerplate is live — see [SPRINT_03_MVP_PREP.md](docs/09-agile/SPRINT_03_MVP_PREP.md) for upload, ASR, talk ratio, admin UI.

Hub: [docs/README.md](docs/README.md)
