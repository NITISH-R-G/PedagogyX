# AI System Architecture Report v3

## AI Problem Analysis

The PedagogyX platform aims to provide an advanced, multimodal AI classroom intelligence and teacher optimization system. Operating under stringent constraints, the platform requires a FOSS-first software stack and local, offline inference due to India data residency regulations (G2 legal sign-off pending for production data). The system ingests audio/visual streams from clients, primarily Meta Ray-Ban smart glasses (via Android DAT), and performs both real-time (Hot Path) activity detection and batch (Cold Path) high-precision pedagogical scoring, transcription, and multi-cam alignment. The primary challenges involve maintaining accurate diarization, robustly synchronizing multimodal streams, mitigating LLM hallucinations in pedagogical coaching, and achieving high throughput under hardware constraints (RTX 5070 dev GPU targets). Currently, the system is in the MVP boilerplate phase using synthetic test sessions.

## AI System Architecture

The system architecture separates ingestion and orchestration from core inference components:

- **Models:** Open-source Whisper variants for ASR, lightweight YOLO models for Hot Path CV (student engagement), and quantized Llama 3 or Mistral variants for Cold Path LLM summarization and coaching.
- **Orchestration:** Directed Acyclic Graph (DAG) pipelines orchestrated through queue-based workers (e.g., `services/worker-asr`, `services/worker-cv`, `services/worker-metrics`) to handle Cold Path processing systematically and ensure stream synchronization.
- **Retrieval Systems:** A vector store setup over Postgres (pgvector) to index educational guidelines and syllabus data for contextual grounding.
- **Memory Systems:** Short-term cache (Redis) for real-time diarization state and Hot Path metrics, with long-term durable storage in Postgres.
- **Infrastructure Topology:** Centralized FOSS backend via `services/api` (FastAPI), routing capture streams to ingestion queues, running on local/district edge nodes to comply with data residency rules.

## Prompt & Reasoning Strategy

Prompts are meticulously engineered to prevent hallucinations and enforce strict pedagogical boundaries:

- **Prompt Structure:** Few-shot templates bound the LLMs strictly to specific educational paradigms (e.g., K-12 vs university) based on the retrieved context.
- **Grounding Strategy:** All generated feedback must trace back to explicit transcript timestamps or CV events. The models are instructed never to guess user sentiment or unobserved context.
- **Hallucination Mitigation:** A secondary validation step involves an LLM checking the proposed coaching tip against retrieved facts and confidence scores before surfacing it to the user.
- **Context Management:** Audio transcripts are chunked with hard token limits. Long sessions are summarized hierarchically before passing context to the final pedagogical evaluation prompt.

## RAG & Retrieval Design

To anchor AI feedback to specific district policies and educational best practices, a structured RAG pipeline is implemented:

- **Ingestion Pipeline:** School guidelines, pedagogical rubrics, and best practices are periodically embedded into the vector database.
- **Embeddings:** Lightweight sentence-transformer models create dense vector embeddings.
- **Vector Database:** Postgres equipped with the pgvector extension provides unified, ACID-compliant storage for both structured metadata and embeddings.
- **Reranking:** Cross-encoder reranking is applied during high-stakes batch scoring to maximize retrieval precision for policy matching.
- **Retrieval Workflows:** Hybrid search mechanisms combine exact keyword matches for specific classroom events with semantic search for pedagogical themes.

## AI Infrastructure

The infrastructure design targets local, FOSS, self-hosted environments:

- **Inference Systems:** Containerized model servers optimized using TensorRT or ONNX Runtime to maximize GPU utilization.
- **GPU Infrastructure:** Targeted for RTX 5070 clusters (or CPU dev targets for benchmarks `bench_full_pipeline.sh cpu`), handling both lightweight real-time tasks and intensive batch inference.
- **Scaling Strategy:** Queue-based horizontal scaling of worker nodes. Hot Path workers use autoscaling based on incoming stream count, while Cold Path workers operate on a managed batch job scheduler.
- **Deployment Systems:** Containerized setup using `infra/compose.dev.yaml` for MVP boilerplate local development and testing.

## Evaluation Strategy

Given the critical nature of the AI feedback, a comprehensive evaluation suite is mandatory:

- **Benchmarks:** Test suites in `benchmarks/` evaluate ASR word error rate (WER) on noisy classroom audio and CV precision/recall on synthetic student engagement data.
- **Automated Evals:** Unit and integration testing via `pytest`, simulating end-to-end synthetic sessions (e.g., `make dat-session`).
- **Hallucination Tracking:** Automated rubrics score the LLM's adherence to transcript data, flagging instances where ungrounded advice is produced.
- **Quality Metrics:** System performance is tracked via p50/p95 inference latency, WER, context utilization efficiency, and retrieval accuracy.

## Security & Safety

Ensuring the security of minor student data and the safety of the AI execution boundaries:

- **Prompt Injection Prevention:** Strict input sanitization layers separate untrusted audio transcripts from internal system prompts.
- **Permission Controls:** Granular RBAC ensures that only authorized administrators can access raw streams, while teachers view anonymized scores and actionable feedback.
- **Sandboxing:** All inference and tool-execution processes run within isolated, read-only Docker containers.
- **Output Validation:** Rigid JSON schema enforcement forces LLMs to return structured outputs. Parsing failures trigger a default "Review Needed" state rather than surfacing anomalous text.

## Observability

Comprehensive observability is essential for operating the offline, edge-deployed models:

- **Tracing:** End-to-end trace logs link incoming Meta Ray-Ban streams to final pedagogical scores using OpenTelemetry.
- **Monitoring:** Grafana dashboards monitor background worker queue depth, API latency, and RTX 5070 VRAM utilization.
- **Analytics:** Tracking the distribution between Hot Path heuristic triggers and Cold Path authoritative overrides.
- **Diagnostics:** Comprehensive dead-letter queues (DLQs) capture full tracebacks and context for worker failures to facilitate rapid debugging.

## Performance Optimization

Operating within strict offline and edge hardware limitations necessitates aggressive optimization:

- **Latency Optimization:** Edge-based streaming transcription where feasible, chunking logic into micro-batches (e.g., 2-second windows) for near real-time feedback.
- **Token Optimization:** Aggressive summarization and context compression before invoking heavy LLMs for final pedagogical scoring.
- **Inference Efficiency:** Leveraging integer quantization (INT4/INT8) on LLMs to fit within VRAM limits while maintaining reasoning quality.
- **Caching Strategy:** Redis-based caching of recurrently evaluated pedagogical templates, intermediate embeddings, and frequently requested metrics.

## Risks & Tradeoffs

- **Hallucination Risks:** Utilizing quantized, local LLMs increases the probability of subtle reasoning errors compared to proprietary cloud models, requiring robust secondary validation.
- **Scalability Concerns:** Offline GPU provisioning inherently limits burst capacity; high-load scenarios during peak school hours will inevitably delay cold-path scoring.
- **Infrastructure Tradeoffs:** Adhering to a FOSS-first, offline architecture introduces maintenance overhead and limits access to state-of-the-art managed cloud infrastructure.
- **Operational Limitations:** Multi-stream synchronization (addressing audio/video drift) from disconnected mobile devices is complex and hard to correct without custom hardware timestamps.

## Agile Sprint Plan

- **Milestone 1:** Finalize the deployment of open-source Whisper ASR variants and stabilize the `worker-asr` pipeline on synthetic data.
- **Milestone 2:** Implement Hot Path lightweight YOLO inference and integrate basic activity metrics into `worker-cv` and `worker-metrics`.
- **Milestone 3:** Deploy the initial RAG framework using pgvector, establishing secure prompt structures and schema validation for structured outputs.
- **Milestone 4:** Complete integration of Cold Path multi-stream batch processing and expand the automated evaluation test suites in `benchmarks/`.
- **Expected Improvements:** A robust, fully FOSS MVP AI pipeline capable of reliable pedagogical scoring with zero external API dependencies, ready for real-world pilot data upon G2 clearance.
