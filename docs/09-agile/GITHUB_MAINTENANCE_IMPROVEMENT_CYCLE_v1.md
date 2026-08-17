# GitHub Maintenance & Improvement Cycle v1

## Repository Health Report

- **Strengths:** Detailed architecture planning, clear documentation constraints, structured Sprint planning, well-defined metrics, existing CI/CD boilerplate. Good foundational Phase 0 research, ADRs, compliance constraints documented.
- **Weaknesses:** Missing live implementation for the complete pipeline, GPU benchmarking missing, unverified device capture. High dependency on strict, potentially slow legal processes (G2).
- **Risks:** The project is blocked from writing services code pending legal (G2) memo. In the meantime, dev velocity could stagnate or architectural plans could diverge from the reality of development.
- **Opportunities:** Improve automation of boilerplate generation, setup end-to-end synthetic testing of the pipeline with synthetic non-production data, ensure seamless client integrations (e.g., mock capture). Focus on reducing manual verification.

## Competitor Analysis

- **Repositories Analyzed:** `learning-commons-org/evaluators`, `mrdavola/RedesignEd-Classroom`, `pblsketch/k-teacher-skills`, `ML9-FORCES/classroom-x`.
- **Advantages Discovered:** Strong community ecosystems and simple onboarding guides for open-source alternatives. Lightweight frontends.
- **Gaps Identified:** Lack of complex multimodal (audio/video) integration in competitor repos, many focus purely on textual chat or single modality. Missing robust multi-cam/audio sync architecture like PedagogyX. Lack of enterprise-grade compliance features out of the box.
- **Opportunities to Outperform:** Our strong architectural focus on privacy (India data residency, local on-prem processing), rigorous edge/cloud ML pipeline, and precise metrics (Pedagogy Score, Talk Ratio). We can dominate the market with a true enterprise-grade open-source classroom intelligence solution.

## Priority Improvements

1. Set up synthetic data pipeline for End-to-End integration testing of API, CV, and ASR workers.
2. Complete RTX 5070 GPU benchmark validation for realistic cost model and production sizing.
3. Fully document and unblock the legal G2 process to move into actual code implementation.

## Sprint Plan

- **Sprint Goal:** Finalize the baseline implementation of the `worker-asr` and `worker-cv` modules, validating performance locally on CPU, while setting up the GPU profiling pipeline for the upcoming hardware test. Validate the core API endpoints with synthetic data.
- **Tasks:**
  - Create synthetic test cases for multimodal inputs (audio + multi-cam video).
  - Benchmark YOLO and Whisper pipelines on standard mock datasets.
  - Finalize Docker dev environment for full pipeline.
  - Draft and finalize the G2 Readiness package for founder sign-off.
- **Implementation Roadmap:** Focus on `benchmarks/` and `services/worker-*` (stub mode) until G2 sign-off. Validate API and frontend boilerplate using mock capture tools.
- **Expected Outcomes:** A verified, robust synthetic testing pipeline, clear metrics on local CPU runs, and green light for G2.

## Technical Improvements

- **Architecture:** Move towards a robust microservices layout with clear containerized boundaries. Implement strict type safety using Pydantic for APIs.
- **Performance:** Ensure worker queues can handle chunks optimally. Start benchmarking edge workers vs central cloud nodes for latency reduction.
- **Scalability:** Validate MinIO scalable bucket policies for tenant-based isolation (K-12 vs Univ).
- **Security:** Ensure strong local RBAC and no external internet dependencies for core processing.
- **Testing:** Improve CPU benchmarks; transition to GPU test scripts.
- **Documentation:** Continue expanding the ADRs for emerging requirements.
- **DevOps:** Strengthen `compose.dev.yaml` to ensure zero friction onboarding for new developers.

## Metrics Improved

- **Code Quality Gains:** Python linters (`black`, `ruff`) enforced; Markdown docs linting added.
- **Coverage Improvements:** CPU benchmarks added for Whisper and YOLO processing, validating the stub workflow.
- **Developer Productivity Improvements:** Centralized testing scripts (`scripts/dev-verify.sh`) to consolidate linting, formatting, and profiling.
