# Autonomous Senior AI Engineer & Applied Intelligence Systems Architect Report: Dead Letter Queue (DLQ) Implementation

## AI Problem Analysis

- **Use Case:** Processing asynchronous background tasks for AI operations, such as Automatic Speech Recognition (ASR) transcriptions and computing talk ratio metrics for teacher pedagogy evaluation.
- **Requirements:** Both `worker-asr` and `worker-metrics` must have a mechanism to gracefully handle unexpected processing exceptions without losing the job payload entirely.
- **Constraints:** Background workers must be resilient. Since these tasks process unstructured inputs (audio chunks) and interact with databases, transient errors, corrupted files, and system timeouts can occur. The system must not drop jobs silently.
- **User Workflows:** A teacher records a session via Ray-Ban DAT; chunks are uploaded and sent for processing. If a job fails during transcription or metric computation, the payload must be retained for debugging, retries, or alerts.
- **Failure Scenarios:** A database connection drops, MinIO fails to serve an object, or an AI model out-of-memory error happens during inference. Without a DLQ, the Redis job is lost once popped.

## AI System Architecture

- **Models:** Whisper (faster-whisper) for ASR, stub models for MVP fallbacks.
- **Orchestration:** FastAPI backend enqueueing jobs into Redis queues (`jobs:asr`, `jobs:talk_ratio`).
- **Retrieval Systems:** MinIO for raw audio chunks; PostgreSQL for fetching session states and storing transcripts.
- **Memory Systems:** Redis lists as task queues; a dead-letter queue (DLQ) system (`jobs:asr:dlq`, `jobs:talk_ratio:dlq`) is now implemented as secondary Redis lists to catch unprocessable payloads.
- **Infrastructure Topology:** Docker Compose stack with isolated Python worker containers. The addition of the DLQ mechanism requires no new external services, leveraging the existing Redis infrastructure.

## Prompt & Reasoning Strategy

- **Prompt Structure:** Not applicable to the DLQ layer itself, but ensures that prompts processed by models do not fail silently if they trigger unexpected backend state.
- **Grounding Strategy:** The DLQ provides "ground truth" for failed operations, enabling deterministic debugging instead of guessing why a task disappeared.
- **Hallucination Mitigation:** Debugging hallucinations and parsing errors in structured outputs is easier when failing payloads are retained in the DLQ.
- **Context Management:** Failed contexts (session IDs) are preserved precisely as they were dispatched by the API.

## RAG & Retrieval Design

- **Ingestion Pipeline:** Asynchronous audio chunks from edge devices to MinIO.
- **Embeddings:** N/A for this scope.
- **Vector Database:** N/A for this scope.
- **Reranking:** N/A for this scope.
- **Retrieval Workflows:** The retrieval of audio chunks in `worker-asr` can fail. If it does, the job goes to the DLQ.

## AI Infrastructure

- **Inference Systems:** CPU-based Faster Whisper (with RTX 5070 GPU benchmarking planned).
- **GPU Infrastructure:** Planned RTX 5070 compute. The DLQ is critical here because GPU out-of-memory errors will result in job crashes. The DLQ saves the payload to retry when memory is available.
- **Scaling Strategy:** The Redis queue allows workers to scale horizontally. The DLQ collects errors centrally from all worker instances.
- **Deployment Systems:** Dockerized Python environments (`services/worker-asr`, `services/worker-metrics`).

## Evaluation Strategy

- **Benchmarks:** The DLQ addition does not impact inference latency but improves system resilience.
- **Automated Evals:** Evals will not stall indefinitely due to dropped jobs; failed eval jobs will land in the DLQ.
- **Hallucination Tracking:** Preserving payloads that cause parsing errors helps track unexpected model formats.
- **Quality Metrics:** Reliability and uptime metrics are directly improved by preventing silent job failures.

## Security & Safety

- **Prompt Injection Prevention:** If an injection payload causes a downstream crash, it is securely trapped in the DLQ for analysis rather than executing repeatedly or vanishing.
- **Permission Controls:** The Redis connection retains the same permissions.
- **Sandboxing:** Workers run in separate containers. The DLQ allows inspection without running the payload again.
- **Output Validation:** Model outputs that fail subsequent validation and raise exceptions are now caught.

## Observability

- **Tracing:** Full tracebacks are now printed to `sys.stderr` using `traceback.print_exc()`, linking exception details directly to the worker container logs.
- **Monitoring:** The size of the `*:dlq` lists in Redis can be monitored using `LLEN` to trigger alerts on high failure rates.
- **Analytics:** Allows operators to compute the exact failure rate of transcription and metrics jobs.
- **Diagnostics:** Immediate access to the raw JSON payload in the DLQ paired with the stderr traceback allows for rapid triage.

## Performance Optimization

- **Latency Optimization:** Immediate fallback to the DLQ prevents workers from getting stuck in infinite loops trying to process malformed data, freeing them for valid jobs.
- **Token Optimization:** N/A
- **Inference Efficiency:** The worker moves on efficiently to the next valid task.
- **Caching Strategy:** N/A

## Risks & Tradeoffs

- **Hallucination Risks:** N/A for the queueing infrastructure.
- **Scalability Concerns:** If a systemic failure occurs (e.g., database goes offline), the DLQ will rapidly fill up. The Redis memory capacity could be exhausted if millions of jobs fail simultaneously. A TTL or DLQ size limit strategy might be needed later.
- **Infrastructure Tradeoffs:** Memory usage on Redis slightly increases to store failed payloads, which is an acceptable tradeoff for improved observability and reliability.
- **Operational Limitations:** Requires manual intervention to drain or retry jobs from the DLQ (e.g., a script to move jobs from `jobs:asr:dlq` back to `jobs:asr`).

## Agile Sprint Plan

- **Milestones:** Implemented DLQ in `worker-asr` and `worker-metrics` using `client.rpush` and `traceback.print_exc`.
- **Implementation Phases:**
  1. Add traceback logging and DLQ pushing to `worker-asr/worker/main.py`.
  2. Add traceback logging and DLQ pushing to `worker-metrics/worker/main.py`.
  3. Format documentation and ensure test coverage.
- **Evaluation Checkpoints:** Check worker logs for tracebacks during simulated failures. Monitor Redis keys `jobs:asr:dlq` and `jobs:talk_ratio:dlq`.
- **Expected AI Improvements:** System resilience and Mean Time To Recovery (MTTR) for AI inference jobs significantly improved.
