# AI System Architecture Report v3

## AI Problem Analysis

- **Use Case:** PedagogyX is an AI-powered multimodal classroom intelligence and teacher optimization platform targeting K-12 and university segments in India. The system captures live teaching sessions using Meta Ray-Ban smart glasses (POV video + audio) via an Android DAT host, processing streams to evaluate instructional quality, pedagogy, and discourse patterns.
- **Requirements:** Must operate entirely on OSS-first infrastructure (no proprietary SaaS APIs like OpenAI or Deepgram) to ensure data residency compliance in India (DPDP). The pipeline mandates dual-path execution: a fast hot path for near real-time lightweight heuristics, and a cold path for authoritative batch processing of complex ML fusion (ASR, CV, LLM-based scoring).
- **Constraints:** Compute budget is strictly constrained to RTX 5070 (12GB VRAM) for cloud workers, mandating aggressive quantization (INT4/INT8), continuous batching, and context offloading.
- **User Workflows:** Teachers record sessions seamlessly. Streams buffer at the edge and upload to the PedagogyX cloud. School administrators receive authoritative, evidence-backed pedagogical score reports derived from the cold path.
- **Failure Scenarios:** Network packet loss causing out-of-sync audio/video streams (A/V drift); GPU OOM errors on RTX 5070 workers during concurrent inference; hallucinated pedagogical feedback damaging teacher trust; and prompt injections from erratic classroom data.

## AI System Architecture

- **Models:**
  - **ASR:** Quantized Whisper v3 / Distil-Whisper optimized for English-Hindi code-switching.
  - **CV:** Lightweight YOLOv8 for hot-path engagement detection; MobileVLM or LLaVA for batch multi-modal pedagogical context.
  - **LLMs:** Locally deployed, quantized models (e.g., Llama 3 / Qwen2.5-7B-Q4) running via vLLM/Ollama for pedagogy scoring and report generation.
- **Orchestration:** Multi-stage asynchronous Directed Acyclic Graph (DAG) pipelines managed via background worker queues (Celery/Temporal-based `worker-asr`, `worker-cv`, `worker-metrics`) ensuring resilient Cold Path processing.
- **Retrieval Systems:** A hybrid vector store setup over Postgres (pgvector) to index and retrieve classroom segment templates, syllabus data, and historical pedagogical scores.
- **Memory Systems:** Short-term context and rolling stream state managed via Redis (for Hot Path tracking); long-term durability in PostgreSQL and MinIO.
- **Infrastructure Topology:** Hybrid Edge/Cloud architecture. Android DAT Host -> Edge LAN Buffer/MediaMTX -> API Gateway -> Postgres/MinIO -> RTX 5070 GPU Workers (India Cloud).

## Prompt & Reasoning Strategy

- **Prompt Structure:** Multi-shot, deterministic prompts defining clear personas (e.g., "Expert Pedagogy Evaluator"). Prompts strictly separate raw session transcripts from evaluation rubrics.
- **Grounding Strategy:** All LLM outputs must be explicitly anchored to specific timestamped evidence from the transcript or CV events. Guided decoding forces strict JSON schema outputs.
- **Hallucination Mitigation:** Employs temperature=0 decoding for scoring tasks. A secondary validation chain (self-consistency) checks proposed coaching tips against retrieved facts. Claims without transcript references are discarded.
- **Context Management:** Implement hierarchical chunking for long lectures (e.g., 45-minute sessions). Segments are recursively summarized and passed to the final evaluation prompt to remain within the LLM's context limits.

## RAG & Retrieval Design

- **Ingestion Pipeline:** School guidelines, rubrics, and best practices are periodically chunked and embedded. Transcripts are enriched with diarization and CV context before vectorization.
- **Embeddings:** Domain-adapted sentence transformers (e.g., optimized for English/Hindi instructional dialogue).
- **Vector Database:** PostgreSQL with the pgvector extension for unified ACID-compliant storage alongside structured data.
- **Reranking:** Cross-encoder reranking applied to top-K retrieved chunks to guarantee high relevance during authoritative batch scoring.
- **Retrieval Workflows:** Hybrid search combining exact keyword matches for specific classroom events with semantic search for broader pedagogical concepts.

## AI Infrastructure

- **Inference Systems:** Containerized model servers utilizing vLLM (for PagedAttention and continuous batching) and TensorRT/ONNX optimizations.
- **GPU Infrastructure:** Highly optimized pool of RTX 5070 (12GB VRAM) clusters handling both Hot and Cold inference, requiring strict workload separation.
- **Scaling Strategy:** Queue-based horizontal autoscaling. GPU worker pods scale based on Cold Path backlog; Hot Path relies on autoscaling based on concurrent stream count.
- **Deployment Systems:** Docker Compose for edge/local deployments (e.g., `infra/compose.dev.yaml`), and Kubernetes (K3s) for the central India Cloud cluster.

## Evaluation Strategy

- **Benchmarks:** Domain-specific test suites assessing ASR Word Error Rate (WER) on noisy classroom audio, Diarization Error Rate (DER), and CV precision/recall for engagement metrics.
- **Automated Evals:** LLM-as-a-judge pipelines validating structured JSON schema adherence, citation accuracy, and end-to-end synthetic session testing via `pytest`.
- **Hallucination Tracking:** Automated rubrics compare LLM-generated evidence strings against exact substring matches in the source transcript to detect ungrounded advice.
- **Quality Metrics:** p50/p95 inference latency, context utilization efficiency, WER, and user trust/satisfaction (via dashboard interactions).

## Security & Safety

- **Prompt Injection Prevention:** Input sanitization layers treat untrusted audio transcripts strictly as data payloads, separating them from internal system prompts.
- **Permission Controls:** Strict Role-Based Access Control (RBAC) via the API Gateway limits viewing raw minor student video to admins, while teachers view only actionable feedback.
- **Sandboxing:** Inference processes run in isolated, low-privilege, read-only containers.
- **Output Validation:** Rigid Pydantic/JSON schema validation forces models to return structured outputs. Failures trigger safe default "Review Needed" states.

## Observability

- **Tracing:** Full end-to-end tracing using OpenTelemetry, connecting incoming Ray-Ban streams to final pedagogical scores.
- **Monitoring:** Grafana dashboards tracking worker queue depth, API latency, and critical RTX 5070 VRAM utilization.
- **Analytics:** Tracking the ratio of hot-path heuristics vs. cold-path authoritative overrides, and product analytics on time-to-insight.
- **Diagnostics:** Comprehensive dead-letter queues (DLQs) capturing full tracebacks to `sys.stderr` for rapid debugging of worker failures.

## Performance Optimization

- **Latency Optimization:** The hot path avoids LLM calls entirely, relying on heuristics. The cold path processes audio and video concurrently before fusion.
- **Token Optimization:** Aggressive summarization and filtering of silence/non-instructional audio prior to heavy LLM invocation.
- **Inference Efficiency:** Integer quantization (4-bit AWQ/GPTQ) on LLMs to fit within the 12GB VRAM limits while leaving room for KV cache and batched processing throughput.
- **Caching Strategy:** Redis-based caching of recurrently evaluated pedagogical templates, session states, and intermediate embedding outputs.

## Risks & Tradeoffs

- **Hallucination Risks:** Evaluating teaching quality is highly subjective; quantized local models may misinterpret cultural nuances or output confident but incorrect assessments, necessitating strong deterministic verification.
- **Scalability Concerns:** The RTX 5070 12GB constraint creates a hard ceiling on concurrent LLM context size, meaning long sessions must be aggressively chunked, risking loss of global context.
- **Infrastructure Tradeoffs:** FOSS-first creates massive maintenance overhead and drastically increases DevOps complexity compared to managed proprietary APIs.
- **Operational Limitations:** Handling network instability and out-of-order chunks complicates multi-stream A/V synchronization, which is hard to correct without custom hardware timestamps.

## Agile Sprint Plan

- **Sprint 1 (Infrastructure & MVP ASR):** Setup RTX 5070 worker nodes. Deploy vLLM and quantized Whisper. Implement chunked ASR pipeline queues (`worker-asr`).
- **Sprint 2 (Data Ingestion & Hot Path):** Develop Android DAT host integration and edge LAN buffer. Implement lightweight hot-path activity detection heuristics (`worker-cv`).
- **Sprint 3 (Cold Path & LLM Reasoning):** Implement full batch ML fusion pipeline. Develop Qwen2.5-7B prompts for pedagogical scoring. Integrate pgvector for retrieval.
- **Sprint 4 (Observability & Hardening):** Implement OpenTelemetry tracing and Grafana dashboards. Establish automated evaluation pipelines for hallucination tracking and schema validation.
- **Sprint 5 (Pilot & Refinement):** Deploy to pilot schools. Conduct end-to-end latency/VRAM stress testing. Iterate on prompt grounding based on real-world classroom acoustics.
