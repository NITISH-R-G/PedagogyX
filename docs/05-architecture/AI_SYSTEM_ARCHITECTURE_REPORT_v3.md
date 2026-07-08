# AI System Architecture Report v3

## AI Problem Analysis

The objective is to deploy a world-class multimodal AI classroom intelligence platform (PedagogyX) at production scale. The system operates under extreme constraints: utilizing a strictly FOSS-first software stack, offline inference mandated by data residency regulations (specifically for G2/India legal sign-off), and relying on incoming AV streams from edge devices (Meta Ray-Ban via `android-capture-dat`, standard Android, or Windows devices).
The primary AI engineering challenges revolve around maintaining high reliability, contextual accuracy, and inference efficiency while managing the split between a low-latency "Hot Path" (real-time heuristics) and a high-precision "Cold Path" (authoritative batch processing). We must handle unpredictable classroom audio environments, dynamic multi-camera sync drifts, hallucination risks from local models, and strict pedagogical evaluation workflows. We optimize aggressively for Reliability, Accuracy, Scalability, Maintainability, Inference Efficiency, User Value, Observability, Security, Extensibility, and Long Term Sustainability.

## AI System Architecture

The AI infrastructure is designed to isolate real-time streaming operations from asynchronous heavy lifting, built on a central OSS offline inference backend.

- **Hot Path (Real-time):** Fast, low-latency processing edge streams for initial activity detection (YOLO), talk ratios, and basic engagement analytics.
- **Cold Path (Batch):** Complete multi-cam alignment, thorough transcription (Faster-Whisper), authoritative pedagogy scoring, and complex LLM orchestration (Ollama serving quantized models) powered by RTX 5070 GPU clusters.
- **Microservices:** The workload is managed by core workers: `worker-asr` for speech-to-text, `worker-cv` for computer vision, and `worker-metrics` for aggregation, coordinated via background queues.
- **Memory Systems:** Redis for hot-path caching/diarization tracking, with Postgres providing long-term authoritative storage.

## Prompt & Reasoning Strategy

Prompts are engineered to enforce strict determinism and contextual grounding within the educational domain.

- **Prompt Structure:** Multi-turn conversational setups are replaced with zero-shot/few-shot instructional templates tailored for K-12 and university pedagogy. Prompts explicitly define output schema (JSON) boundaries.
- **Grounding Strategy:** All generative outputs must trace back to explicit transcript timestamps, ASR segments, or computer vision events. Models are strictly forbidden from inferring emotional state or pedagogical intent not evidenced in the data.
- **Hallucination Mitigation:** We implement an evaluation chain (LLM-as-a-judge) that cross-verifies the primary LLM's pedagogical suggestions against retrieved syllabus facts and raw transcript data before surface-level generation.
- **Context Management:** Token windows are tightly controlled. Long sessions are segmented and summarized hierarchically, preserving chronological continuity for the final pedagogy assessment.

## RAG & Retrieval Design

Our Knowledge Systems mode integrates educational rubrics and school-specific guidelines into the inference pipeline.

- **Ingestion Pipeline:** Pedagogical rubrics, curricula, and historical coaching templates are systematically chunked and embedded.
- **Embeddings & Vector Database:** Sentence-transformers generate embeddings, stored and queried using Postgres with the `pgvector` extension, maintaining ACID compliance alongside transactional data.
- **Reranking & Retrieval Workflows:** A hybrid search approach uses exact semantic matches for pedagogical concepts and cross-encoder reranking for high-stakes policy matches, guaranteeing that coaching feedback is faithfully anchored to actual district guidelines.

## AI Infrastructure

Designed for high-throughput, FOSS-centric offline operations.

- **Inference Systems:** Deep integration with Ollama for LLMs and Triton/TensorRT for computer vision models, maximizing the throughput of our centralized FOSS backend.
- **GPU Infrastructure:** Inference queues are highly optimized for the constrained budget of RTX 5070 clusters, employing dynamic batching and memory pooling to maximize GPU utilization.
- **Scaling Strategy:** Horizontal scaling of `worker-asr` and `worker-cv` nodes via Redis/Celery task queues, with autoscaling triggers based on queue depth and stream ingestion volume.
- **Deployment Systems:** Containerized (Docker Compose/Kubernetes) deployment pipelines designed for robust, reproducible deployments in edge data centers or localized hubs.

## Evaluation Strategy

We employ a rigorous, automation-first evaluation methodology.

- **Automated Evals:** Unit and integration testing via `pytest` simulating end-to-end synthetic sessions across the API service and AI workers.
- **Benchmarks:** We track Word Error Rate (WER) for ASR under noisy conditions, precision/recall for CV metrics, and hallucination rates for LLM outputs. Benchmark code is maintained in `benchmarks/` utilizing dedicated Python environments.
- **Quality Metrics:** Continuous tracking of response faithfulness, latency, token usage efficiency, and pedagogical value of the final insights provided to teachers.

## Security & Safety

Strict isolation and data protection mechanisms given the highly sensitive nature of classroom recordings.

- **Prompt Injection Prevention:** Aggressive input sanitization separating untrusted ASR transcripts from core system prompts.
- **Permission Controls:** Enforced RBAC to ensure raw audio/video data is isolated from general user access; teachers view only aggregated metrics and generated reports.
- **Sandboxing & Isolation:** AI worker processes execute in isolated, restricted-permission containers with no outgoing internet access to adhere to data residency laws.
- **Output Validation:** Hard enforcement of structured outputs (JSON schema) ensures any unsafe or misaligned generation fails gracefully rather than propagating to the frontend.

## Observability

Comprehensive telemetry is essential for debugging our FOSS stack and maintaining inference quality.

- **Tracing & Monitoring:** Full-stack distributed tracing via OpenTelemetry, mapping requests from `android-capture-dat` through MediaMTX and into the AI worker queues.
- **Analytics:** Dashboards tracking inference p50/p95 latency, GPU utilization, memory usage, and queue lengths for both Hot and Cold paths.
- **Diagnostics:** Systematic tracking of API failures, ASR confidence scores, and LLM retry rates to swiftly identify hardware bottlenecks or model drift.

## Performance Optimization

Maximizing the capability of the RTX 5070 hardware through relentless efficiency improvements.

- **Inference Efficiency:** Using integer quantization (INT4/INT8) on LLMs and ONNX runtime for CV models to fit entirely within VRAM limits.
- **Latency Optimization:** Strategic caching of intermediate RAG embeddings and recurrent pedagogical heuristics. Hot Path metrics are streamed incrementally while Cold Path processes execute asynchronously.
- **Token Optimization:** Aggressive summarization protocols reduce the context overhead before invoking the heavier analytical models.

## Risks & Tradeoffs

- **Model Accuracy vs. Hardware Constraints:** Relying solely on local FOSS models (e.g., Llama 3 8B, Faster-Whisper) within RTX 5070 constraints inherently risks lower reasoning capability compared to frontier proprietary models, demanding stricter prompt engineering.
- **Complexity of Multi-Modal Sync:** Accurate Cold Path processing requires flawless synchronization of audio and video streams; edge network instability can lead to complex A/V drift requiring expensive software alignment.
- **Maintenance Overhead:** The FOSS-first approach necessitates internal management of model versions, inference servers, and bug fixes rather than relying on managed cloud services.

## Agile Sprint Plan

- **Sprint 1:** Finalize the deployment and optimization of the `worker-asr` and `worker-cv` inference pipelines on the RTX 5070 centralized OSS backend.
- **Sprint 2:** Implement and benchmark the pgvector RAG pipeline, ensuring strict grounding for pedagogical feedback generation.
- **Sprint 3:** Develop the evaluation suite (benchmarks/pytest) targeting hallucination mitigation and latency optimization for the Cold Path authoritative scoring.
- **Sprint 4:** Solidify the observability stack and establish end-to-end security sandboxing, preparing the system for India G2 legal data residency sign-off.
