# Testing & Eval Strategy

**Date:** 2026-05-24

## 1. Unit & Integration Testing

- **Framework:** Pytest will be used for all Python backend services.
- **Coverage Target:** Minimum 85% line coverage on core API and business logic.
- **Database Testing:** Use `pytest-postgresql` or dedicated Docker containers for isolated test databases.
- **Mocking:** Network calls to the AI inference workers or external services (if any) must be mocked using `unittest.mock` or `responses`.

## 2. Infrastructure Validation (Smoke Tests)

- A dedicated bash script (`./scripts/compose-smoke.sh`) will be maintained to verify that all containers defined in `infra/compose.dev.yaml` spin up correctly and are reachable.
- This script must run in CI prior to any merge to the main branch.

## 3. AI Pipeline Evaluation (EvalOps)

Before any AI model replaces the mock implementations in the pipeline, it must pass an automated evaluation suite:

- **ASR Evaluation:** Use Word Error Rate (WER) against a gold-standard dataset of Indian classroom recordings (mix of English/Hindi).
- **Pedagogical Evaluation:** Compare LLM-generated pedagogical insights against human-annotated transcripts.
- **Benchmarking:** Maintain a `benchmarks/` directory with scripts to measure inference latency and VRAM usage on the target hardware (RTX 5070).

## 4. Frontend & Edge Testing

- **Web Dashboard:** End-to-end testing using Playwright to verify critical user journeys (e.g., admin viewing a pedagogy score).
- **Edge Client (Android):** Emulated network degradation testing (e.g., simulating a 2G connection drop during upload) is mandatory for the chunked upload logic.
