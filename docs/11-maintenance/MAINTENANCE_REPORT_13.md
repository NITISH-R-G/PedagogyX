# MAINTENANCE_REPORT_13

## Repository Health Report

- **Strengths:**
  - Comprehensive documentation using markdownlint and prettier for formatting.
  - Test coverage inside the API services ensures robustness of the database connections and endpoints.
  - Clean separation of concerns with API and distinct workers.

- **Weaknesses:**
  - `pytest-asyncio` is missing from `services/api/requirements.txt`, leading to skipped tests and pytest warnings (`PytestUnknownMarkWarning`, `PytestUnhandledCoroutineWarning`).
  - Skipping `async def` function tests limits the capability to test asynchronous code such as background tasks and lifespan hooks.

- **Risks:**
  - Asynchronous code execution could fail in production if the relevant tests are consistently skipped in the CI pipeline.
  - Future features that rely heavily on async implementations may be deployed without being verified.

- **Opportunities:**
  - Fixing test suite dependencies to support native async tests will boost test coverage and catch async-specific edge cases.

## Competitor Analysis

- **Repositories Analyzed:**
  - FastAPI ecosystem reference apps (e.g. Full Stack FastAPI Template)
  - Background task manager templates (e.g. Celery + FastAPI templates)

- **Advantages Discovered:**
  - Standardized usage of `pytest-asyncio` to natively test asynchronous endpoints and lifespan dependencies without custom wrappers.
  - Excellent overall coverage because async dependencies are cleanly mocked.

- **Gaps Identified:**
  - Our test suite natively relies on `pytest.mark.asyncio` for the main app lifespan hooks but omits the necessary plugin to parse and execute it.

- **Opportunities to Outperform:**
  - Bring our unit tests up to standard by natively supporting the execution of asynchronous functions, closing the gap with competitor repositories and eliminating confusing test runner warnings.

## Priority Improvements

1. Add `pytest-asyncio` to `services/api/requirements.txt` to enable asynchronous tests.
2. Ensure the full test suite runs successfully without skipped tests and warnings for async marks.

## Sprint Plan

- **Sprint Goal:** Fix API service test warnings and ensure complete test coverage on async endpoints.
- **Tasks:**
  1. Generate Maintenance Report 13 to log the finding.
  2. Append `pytest-asyncio` to `services/api/requirements.txt`.
  3. Validate full test suite passes with zero warnings about unhandled coroutines.
- **Implementation Roadmap:** Start by appending the requirement, reinstalling dependencies inside the isolated test environment, and executing the pytest coverage command again.
- **Expected Outcomes:** Zero pytest warnings relating to async unhandled coroutines.

## Technical Improvements

- **Testing:** `pytest-asyncio` was added to explicit requirements to address skipped tests and ensure native async test functions run properly.
- **Maintenance:** Drafted continuous improvement maintenance log 13.

## Metrics Improved

- **Code Quality Gains:** Async tests are now formally supported, allowing any future developer to write proper lifecycle and background task tests natively.
- **Developer Productivity:** Removed noisy warnings out of the local testing environment.
