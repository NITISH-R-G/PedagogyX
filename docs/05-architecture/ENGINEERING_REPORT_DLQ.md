# Engineering Task Report: DLQ Implementation for Worker Services

## Problem Analysis

- **Requirements:** Background worker tasks (e.g., ASR, metrics) fetching from Redis queues must implement a Dead Letter Queue (DLQ) pattern. When encountering an exception, the worker must catch the exception, log the full traceback to `sys.stderr` using `traceback.print_exc()`, and push the raw payload to the corresponding DLQ (e.g., `f"{JOB_QUEUE}:dlq"`).
- **Constraints:** The DLQ implementation must be applied to both `worker-asr` and `worker-metrics` services. Error handling around the DLQ push itself is required to prevent a crash during exception handling.
- **Edge cases:** The push to the Redis DLQ might fail (e.g., Redis goes down right after the job was pulled). The exception during the DLQ push must be caught and logged so the worker doesn't crash.
- **Scalability considerations:** By capturing failed messages in a DLQ, the system ensures data is not lost and can be reprocessed later, preventing single poisoned messages from repeatedly crashing the worker and ensuring stable operation at scale.

## Architecture Design

- **Components:** Redis, `worker-asr` (main execution loop), `worker-metrics` (main execution loop).
- **Data flow:** Redis Queue -> Worker (JSON parsing, job processing). If exception -> Worker prints traceback -> Worker pushes raw string to Redis DLQ.
- **APIs:** Redis `blpop` (pull), `rpush` (push to DLQ).
- **Abstractions:** Redis Queue and DLQ are separated by convention (`<queue_name>:dlq`).
- **Service boundaries:** Workers independently manage their own DLQ logic within their process boundaries.

## Implementation Strategy

- **Step by step plan:**
  1. Modify `services/worker-metrics/worker/main.py` to import `traceback`.
  2. Add `traceback.print_exc(file=sys.stderr)` in the exception handler of the worker loop.
  3. Attempt to `rpush` the `raw` payload to `f"{JOB_QUEUE}:dlq"`. Catch any exceptions raised during this push and log them.
  4. Repeat the exact same modifications for `services/worker-asr/worker/main.py`.
- **Modules:** `worker-asr/worker/main.py`, `worker-metrics/worker/main.py`.
- **Dependencies:** Built-in `traceback` and `sys` modules, `redis` package.
- **Workflows:** Long-running `while True` loop processing background jobs.

## Code Quality Strategy

- **Testing:** Validating syntax via test execution. (Unit testing the loop itself is typically done via end-to-end integration or mocked queue tests; ensuring syntax is correct is paramount).
- **Validation:** Visual code inspection and execution of existing unit tests to ensure no regressions were introduced.
- **Linting:** Code conforms to PEP 8 standards, matching the surrounding file structure.
- **Type safety:** N/A (minor exception handling additions).

## Performance Optimization

- **Bottlenecks:** Pushing to the DLQ is synchronous. Given it only happens on the exceptional path, it will not bottleneck the hot path processing.
- **Caching:** N/A
- **Concurrency:** Single-threaded pulling. Redis handles concurrent pushes to the DLQ if multiple workers are running.
- **Optimization strategy:** Ensuring the DLQ push does not crash the worker, maintaining high uptime.

## Security Considerations

- **Authentication:** Redis connection uses standard configuration.
- **Authorization:** Handled at the infrastructure layer (Redis VPC/Auth).
- **Validation:** The raw payload is pushed to the DLQ. It is not re-evaluated during the failure path, preventing injection vulnerabilities.
- **Vulnerability mitigation:** The worker handles malformed JSON separately from logic failures, but both could result in dropped messages if not for the robust logging and catching.

## Observability

- **Logging:** Added full traceback printing to `sys.stderr`, improving observability over the previous generic error message. Added error logging for DLQ push failures.
- **Monitoring:** The length of the DLQ can now be monitored in Redis to trigger alerts for failed jobs.
- **Diagnostics:** Full tracebacks are now available in worker logs for post-mortem debugging.

## Refactoring Opportunities

- **Simplifications:** The loop structure is currently duplicated across `worker-metrics` and `worker-asr`. A shared worker framework/class could be abstracted into a common package to standardize error handling and queueing logic across all PedagogyX workers.
- **Modularization:** Move the polling loop to a base worker class.
- **Maintainability improvements:** Consolidating the loop would reduce code duplication and enforce consistency.

## Risks & Tradeoffs

- **Technical risks:** Redis connectivity issues during DLQ push. Handled by a nested `try-except`.
- **Scaling limitations:** If jobs fail at a massive rate, the DLQ could grow large in Redis, consuming memory. Alerting must be established on DLQ size.
- **Complexity tradeoffs:** Added nested try-except blocks slightly reduce readability, but are necessary for robustness.

## Agile Sprint Plan

- **Milestones:** Implement DLQ, Deploy to staging, Monitor DLQ.
- **Priorities:** High priority for operational stability.
- **Implementation phases:** Code changes (done), Testing (done).
- **Expected outcomes:** No dropped messages due to processing exceptions. Tracebacks visible in logs. Failed messages stored in DLQs for retry.
