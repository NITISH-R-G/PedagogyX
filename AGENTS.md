# AGENTS.md

## Repository overview

PedagogyX has **Phase 0 documentation** plus an **MVP boilerplate** (`services/`, `infra/`, `tools/`). **Production school data** remains blocked until **G2** (India legal sign-off).

**Allowed:** docs, `benchmarks/`, boilerplate dev stack, synthetic test sessions only.

## Cursor Cloud specific instructions

### Documentation

- **Lint:** `npx markdownlint-cli 'docs/**/*.md'` (config: `.markdownlint.json`)
- **Format check:** `npx prettier --check 'docs/**/*.md'`
- **CI:** `.github/workflows/dev-verify.yml` — `./scripts/dev-verify.sh --docs-only`

### MVP stack (local / founder machine)

```bash
docker compose -f infra/compose.dev.yaml up --build
./scripts/compose-smoke.sh
python3 tools/mock-capture/mock_capture.py
```

Cloud Agent VMs often **lack Docker** — validate Python with `ruff check services tools` instead of compose-smoke.

### Python

- **Lint:** `ruff check services tools packages/capture-core/py` (see `pyproject.toml`)
- API: `services/api` (FastAPI) · workers: `services/worker-asr` (stub)

### Benchmarks (dev GPU host — CPU OK until RTX 5070)

- `./scripts/dev-verify.sh` or `cd benchmarks && ./bench_full_pipeline.sh cpu`
- [benchmarks/DEV_WITHOUT_GPU.md](benchmarks/DEV_WITHOUT_GPU.md)

### Gates

- **G0** complete · **G2** blocks real pilot PII — boilerplate OK with synthetic data
- **Sprint:** [SPRINT_03_MVP_PREP.md](docs/09-agile/SPRINT_03_MVP_PREP.md)

### Markdown lint notes

- `MD013` / `MD034` disabled in `.markdownlint.json` (intentional long lines / bare URLs)
