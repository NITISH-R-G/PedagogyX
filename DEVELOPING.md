# Developing PedagogyX (quick reference)

**Phase 0** — documentation + dev tooling. **No MVP app code until G2 legal sign-off.**

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

| Action | Doc / link |
| ------ | ---------- |
| Send counsel email | [COUNSEL_OUTREACH_PACKAGE.md](docs/07-compliance-ethics/COUNSEL_OUTREACH_PACKAGE.md) · [Issue #11](https://github.com/NITISH-R-G/PedagogyX/issues/11) |
| Name pilot school | [INDIA_PILOT_DEVICE_REFERENCE.md](docs/01-phase0-founder-interrogation/INDIA_PILOT_DEVICE_REFERENCE.md) checklist |

---

## After G2

[Sprint 03 MVP prep](docs/09/agile/SPRINT_03_MVP_PREP.md) — first code vertical slice.

Hub: [docs/README.md](docs/README.md)
