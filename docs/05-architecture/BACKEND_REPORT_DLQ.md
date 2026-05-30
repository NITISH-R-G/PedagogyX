# Backend Architecture Task Report: DLQ Pattern Implementation

## System & Requirement Analysis

- **Goal:** Implement a Dead Letter Queue (DLQ) pattern for background worker services (`worker-asr` and `worker-metrics`).
- **Functional Requirements:** When a worker encounters an exception while processing a job payload, it must catch the exception, print the full traceback to `sys.stderr`, and securely queue the failed raw payload into a Redis DLQ to prevent data loss.
- **Non-Functional Requirements:** The system must be robust; an exception occurring during the DLQ enqueue operation itself must not crash the worker loop.
- **Target Audience:** Distributed background processing systems consuming from Redis.

## Backend Architecture

- **Overall Design:** The architecture utilizes a single-threaded blocking pop (`blpop`) from a primary Redis queue. Upon processing failure, the architecture branches to a secondary Redis list designated as the DLQ (`<queue_name>:dlq`).
- **Component Interaction:**
  1. Worker -> Redis: Pulls job from `JOB_QUEUE`.
  2. Worker -> Local Function: Executes business logic (`process_job`).
  3. Worker -> STDERR: Logs exceptions and full stack trace.
  4. Worker -> Redis: Pushes to `JOB_QUEUE:dlq`.
- **Failure Domains:** Job parsing failures and job processing failures.

## Database Design

- **Persistence Layer:** Redis serves as both the primary message broker and the DLQ store.
- **Data Structure:** The DLQ is implemented as a standard Redis List data structure, allowing O(1) appends (`rpush`) and sequential retrieval for potential reprocessing operations.
- **Schema:** Payloads are stored as raw JSON strings, preserving their exact state at the time of failure.

## API Strategy

- **Internal APIs:** Interaction with Redis utilizes the standard `redis-py` library. No new HTTP APIs are exposed.
- **Contract:** The worker assumes a JSON contract for valid messages, but the DLQ pattern treats all failed messages as opaque strings, ensuring no assumptions are made about corrupted data during the failure recovery phase.

## Scalability Strategy

- **Horizontal Scaling:** The DLQ pattern scales horizontally. Multiple workers pulling from the same queue will independently push their failed jobs to the shared DLQ list without lock contention, thanks to Redis' atomic operations.
- **Throughput:** Pushing to the DLQ is extremely fast and will not degrade overall system throughput under normal conditions.

## Reliability Strategy

- **Fault Tolerance:** By catching all `Exception` classes and nesting a secondary `try-except` block around the DLQ push, the worker process is highly resilient to transient network errors and unexpected data formats.
- **Data Durability:** Failed jobs are now persisted in Redis rather than being silently dropped and lost.

## Security Strategy

- **Data Integrity:** Raw payloads are moved untouched to the DLQ. This prevents potential malicious payloads that cause exceptions from being inadvertently executed during a re-parse attempt in the error handling path.
- **Access Control:** Dependent on Redis infrastructure security.

## Observability

- **Visibility:** Full tracebacks are printed to `sys.stderr`, ensuring aggregation tools (e.g., Datadog, ELK) capture the exact line of failure.
- **Queue Monitoring:** The DLQ can be actively monitored (e.g., via Prometheus exporters querying Redis List lengths) to trigger alerts when the failure rate spikes.

## Performance Optimization

- **Execution Path:** The DLQ logic only executes on the cold path (error conditions), meaning the hot path (successful job processing) remains perfectly optimized with zero additional overhead.

## Risks & Tradeoffs

- **Redis Memory Growth:** A persistent bug causing 100% of jobs to fail will rapidly fill the Redis DLQ list, potentially causing OOM errors on the Redis node. Mitigated by setting appropriate alerting on DLQ lengths and implementing retention policies.
- **Reprocessing Strategy:** This implementation only stores the dead letters; it does not implement the retry/reprocessing mechanism, which must be built subsequently.

## Agile Sprint Plan

- **Sprint Goal:** Enhance worker robustness and prevent job loss.
- **Tasks Completed:** Updated error handling in `worker-asr` and `worker-metrics`. Added DLQ pushing logic.
- **Next Steps:** Implement a DLQ monitoring dashboard and a CLI tool to inspect and replay DLQ messages.
