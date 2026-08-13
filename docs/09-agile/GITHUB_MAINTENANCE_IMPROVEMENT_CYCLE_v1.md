# GitHub Repository Maintenance & Improvement Cycle v1

## Repository Health Report

**Strengths:**

- Basic project structure with services, docs, and benchmarks is established.
- Documentation standards are mostly configured (markdownlint, prettier).
- Testing infrastructure is partially set up.

**Weaknesses:**

- The `pytest-asyncio` library was missing from `services/api/requirements.txt`, which skipped critical asynchronous tests in API tests.
- React types `@types/jest` were missing in `services/web/package.json`, causing type checking errors.
- Python virtual environment `.venv_api` was incorrectly left untracked in `.gitignore`.

**Risks:**

- Skipped async tests could hide regression bugs in CI.
- Type errors in Next.js might block future builds or developer work.
- Incomplete `.gitignore` could lead to giant unwanted commits.

**Opportunities:**

- Better tracking of Python and Node toolchains.
- Ensuring local validation closely mirrors CI to prevent "it works on my machine" issues.

## Competitor Analysis

**Repositories Analyzed:**

- Typical modern Next.js/FastAPI monorepos (e.g. Vercel templates, Tiangolo's full-stack-fastapi).
  **Advantages Discovered:**
- More complete development environments with strict TypeScript tracking.
- Pre-configured dev environments that prevent missing dependencies.
  **Gaps Identified:**
- This repo missed crucial typing and testing plugins.
  **Opportunities to Outperform:**
- Build an ultra-reliable standard tooling set ensuring strict, un-ignorable type checking and fully robust test execution.

## Priority Improvements

1. Fix Python API tests by adding `pytest-asyncio` to `services/api/requirements.txt`.
2. Fix Next.js type checking by adding `@types/jest` to `services/web/package.json`.
3. Add `venv_api/` to `.gitignore`.
4. Ensure all linters and formatters pass perfectly across both Python and frontend spaces.

## Sprint Plan

**Sprint Goal:** Restore local and CI test reliability and correctness.
**Tasks:**

- Add `pytest-asyncio` dependency.
- Add `@types/jest` dependency.
- Update `.gitignore` to prevent tracking of local `venv_api/` directories.
- Run `tsc` to verify frontend types.
- Run `pytest` to verify all async tests pass without skipping.

## Technical Improvements

- **Testing:** Ensured asynchronous test execution in FastAPI tests instead of silently skipping them.
- **Frontend Types:** Resolved missing `describe`, `it`, and `expect` types by explicitly adding the correct definitions to standard development tools.
- **DevOps:** Cleaned up git tracking semantics to improve developer experience.

## Metrics Improved

- `pytest` coverage went from 65 passed / 2 skipped to 67 passed / 0 skipped.
- `npx tsc` went from 16 type errors to 0 type errors.
