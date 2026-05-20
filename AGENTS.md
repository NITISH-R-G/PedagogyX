# AGENTS.md

## Repository overview

PedagogyX is in **Phase 0** (Research & Architecture). Primary artifacts are Markdown docs (RFCs, ADRs, sprint plans). **MVP application code is blocked until G2** (India legal sign-off).

**Allowed before G2:** documentation, `benchmarks/` dev scripts (ADR-0006 RTX 5070 validation only).

## Cursor Cloud specific instructions

### Documentation

- **Lint:** `npx markdownlint-cli 'docs/**/*.md'` (config: `.markdownlint.json`)
- **Format check:** `npx prettier --check 'docs/**/*.md'`
- **CI:** `.github/workflows/docs-lint.yml` runs on PRs to `main`

### Benchmarks (dev GPU host — not cloud VM)

- **Location:** `benchmarks/`
- **Run:** `cd benchmarks && ./bench_full_pipeline.sh` (needs `python3-venv`, NVIDIA GPU, optional Ollama)
- **Smoke on CPU:** `python3 benchmarks/bench_whisper.py --model tiny --device cpu --duration-sec 5`
- Cloud Agent VMs typically **lack GPU** — do not treat CPU results as production sizing; copy JSON from founder RTX 5070 machine into `benchmarks/results/` manually or via PR.

### Gates

- **G0** complete (founder Tier-1)
- **G2** blocks implementation — counsel brief: `docs/07-compliance-ethics/INDIA_DPDP_COUNSEL_ENGAGEMENT_BRIEF.md`
- **Sprint plan:** `docs/09-agile/SPRINT_02_PLAN.md`

### Markdown lint notes

- `MD013` (line-length) disabled — long prose intentional
- `MD034` (bare URLs) disabled in reference sections
