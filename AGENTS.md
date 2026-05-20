# AGENTS.md

## Repository overview

PedagogyX is currently a **documentation-only** repository (Phase 0 — Research & Architecture). It contains RFCs, ADRs, competitive intelligence, research summaries, compliance drafts, and agile artifacts. There is no application source code, no services to run, and no automated test suite.

## Cursor Cloud specific instructions

- **Lint command:** `markdownlint '**/*.md'` from workspace root. Configuration lives in `.markdownlint.json`.
- **No build/run/test targets exist.** The repo has no `package.json`, `Makefile`, `Dockerfile`, or source code. The only development activity is editing Markdown documentation.
- **Do not create application code** unless the founder explicitly authorizes moving past Phase 0 gates (see `docs/README.md` for gate status).
- The documentation uses long lines (>80 chars) intentionally; `MD013` (line-length) is disabled in `.markdownlint.json`.
- Bare URLs in reference sections are intentional; `MD034` (no-bare-urls) is disabled.
