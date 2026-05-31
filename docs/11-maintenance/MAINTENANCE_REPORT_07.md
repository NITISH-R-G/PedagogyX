# Maintenance Report 07

## Repository Health Report

**Strengths:**

- The API structure uses clear, well-separated domain concerns (`db`, `queue`, `storage`, `dat_routes`).
- Configuration secrets in Pydantic correctly default to `None` for variables like `minio_secret_key` and `api_key`.
- Dead Letter Queues (DLQ) are properly implemented in the background workers (`worker-asr`, `worker-metrics`).

**Weaknesses:**

- `requirements.txt` files for worker services (`worker-asr`, `worker-metrics`) are missing critical testing dependencies (`pytest`, `pytest-cov`), resulting in failures when tests are triggered inside those directories.
- `boto3` is missing from testing dependencies in virtual environments when `worker-asr` attempts to run tests, even though it is documented as required.

**Risks:**

- Missing test dependencies allow commits to pass without proper worker unit tests executing in local/isolated environments.

**Opportunities:**

- By explicitly including all testing dependencies within individual worker requirements, the CI pipeline and local developers can safely execute isolated test suites without relying on global packages.

## Competitor Analysis

**Repositories Analyzed:**

- HuggingFace Accelerate
- VLLM open source backend
- Ray Distributed Worker implementations

**Advantages Discovered:**

- Complete, self-contained dependency graphs for every microservice/worker node, eliminating "ModuleNotFoundError" during tests.
- Extensive test coverage mapped directly to isolated virtual environments.

**Gaps Identified:**

- The `worker-asr` and `worker-metrics` services in PedagogyX rely on external or shared test environments, whereas competitors bundle them meticulously.

**Opportunities to Outperform:**

- Ensuring that our modular background AI jobs (such as whisper transcription stubs) can be linted, tested, and validated completely independently sets us up for scalable FOSS deployment.

## Priority Improvements

1. Add `pytest` and `pytest-cov` to `services/worker-asr/requirements.txt` and `services/worker-metrics/requirements.txt`.
2. Standardize local FOSS background worker test execution requirements.

## Sprint Plan

**Sprint Goal:** Ensure complete testing isolation and dependency correctness for worker modules.
**Tasks:**

- Create `docs/11-maintenance/MAINTENANCE_REPORT_07.md`.
- Append testing dependencies to worker `requirements.txt` files.
- Verify tests across all backend services.

**Implementation Roadmap:**

- Implement missing text dependencies today.
- Run complete test suite simulation.

**Expected Outcomes:**

- `pytest` commands executed from within `worker-asr` and `worker-metrics` will successfully collect and run their respective tests.

## Technical Improvements

- **Testing / DevOps:** Added isolated testing dependencies (`pytest`, `pytest-cov`) to individual worker module requirements.

## Metrics Improved

- **Developer Productivity:** Developers no longer need to manually guess or install missing modules (like `pytest`) to run worker-level tests locally.
- **Code Quality Gains:** CI pipelines will correctly evaluate worker test assertions rather than immediately throwing `ModuleNotFoundError` during test collection.
