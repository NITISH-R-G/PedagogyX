# AI System Architecture Report v3

## AI Problem Analysis

PedagogyX requires a multimodal AI platform to evaluate classroom intelligence and provide pedagogical optimization feedback. Operating strictly under a FOSS-first software stack and offline execution model for India data residency compliance, the system captures audio/visual streams from primarily Meta Ray-Ban (DAT) smart glasses and basic Android/Windows devices.
Constraints include running on a consumer-grade RTX 5070 (12GB VRAM).
**Use Case:** Real-time activity detection and batch-processed authoritative pedagogical scoring.
**Requirements:** Multimodal alignment, offline local execution, high reliability, and data privacy.
**User Workflows:** Teachers record sessions via DAT clients; Hot Path provides real-time heuristic metrics, while Cold Path produces deep analytical feedback offline.
**Failure Scenarios:** Multimodal A/V desynchronization, long latency loops in the batch system, LLM hallucinations providing inaccurate coaching, and prompt injections via classroom audio.

## AI System Architecture

The AI stack separates processing into edge capture and centralized FOSS inference layers.

- **Models:**
  - _Speech-to-Text:_ Whisper-v3 variants optimized with Faster-Whisper/CTranslate2 for constraints (INT8).
  - _Computer Vision:_ YOLOv10 (nano/small) for real-time hot path; specialized ViT models for cold-path batch alignment.
  - _LLMs:_ Quantized (GGUF/AWQ) Llama-3-8B-Instruct or Mistral-7B, strictly constrained to 12GB VRAM alongside other models.
- **Orchestration:** Python-based worker queues (worker-asr, worker-cv, worker-metrics) utilizing a Directed Acyclic Graph (DAG) for multi-step pipeline processing.
- **Retrieval Systems:** Local pgvector (Postgres) enabling semantic search of historical classroom data and pedagogical templates.
- **Memory Systems:** Redis for hot-path caching and real-time state management; Postgres for durable, long-term multi-session memory and diarization tracking.
- **Infrastructure Topology:** Centralized edge node topology deployed inside district-level data centers via Docker Compose, isolated from public internet access. MediaMTX handles stream ingestion.

## Prompt & Reasoning Strategy

Prompts are rigorously designed to output structured evaluations and limit imaginative variance.

- **Prompt Structure:** Few-shot templates bound by system directives, providing specific context snippets (K-12 vs. university).
- **Grounding Strategy:** All generated feedback must trace back to concrete timestamped evidence from the transcript or CV events. No speculative sentiment analysis.
- **Hallucination Mitigation:** "Check-and-Balance" workflows where a secondary validation prompt validates the primary output against the retrieved factual context before storing the pedagogical score.
- **Context Management:** Transcript chunks are strictly windowed. Long session transcripts are hierarchically summarized to avoid context limit saturation and token overflow.

## RAG & Retrieval Design

RAG ensures the AI feedback aligns with local educational standards and curricula.

- **Ingestion Pipeline:** School-specific guidelines are parsed, chunked, and embedded locally into pgvector.
- **Embeddings:** Lightweight Sentence Transformers (e.g., all-MiniLM-L6-v2) for ultra-fast, low-memory vector generation.
- **Vector Database:** PostgreSQL with pgvector extension ensuring unified ACID transactions with relational student/teacher data.
- **Reranking:** Local cross-encoder reranker models applied exclusively in the Cold Path for high-stakes curriculum alignment.
- **Retrieval Workflows:** Hybrid Search strategies combining BM25 exact keyword matching (for explicit educational terminology) with semantic vector search for conceptual teaching strategies.

## AI Infrastructure

Infrastructure strictly targets local offline execution for full data residency compliance.

- **Inference Systems:** Containerized vLLM or Ollama for LLM serving; customized ONNX runtime for CV models to maximize RTX 5070 efficiency.
- **GPU Infrastructure:** Shared 12GB VRAM on RTX 5070 demands aggressive memory multiplexing and model offloading/swapping.
- **Scaling Strategy:** Queue-based horizontal scaling of worker processes. Autoscaling is limited by physical node constraints; batch job scheduling handles traffic spikes during off-hours.
- **Deployment Systems:** Fully containerized setup via `infra/compose.dev.yaml` ensuring deployment reproducibility without Kubernetes overhead for MVP phase.

## Evaluation Strategy

A strong automated evaluation suite prevents drift and ensures rigorous AI quality control.

- **Benchmarks:** Continuous assessment of ASR Word Error Rate (WER) and CV bounding-box mean Average Precision (mAP) against a synthetic test set.
- **Automated Evals:** End-to-end `pytest` pipelines mimicking client interactions and evaluating final pedagogical JSON outputs.
- **Hallucination Tracking:** Automated rubrics measuring the faithfulness of AI-generated advice to the provided transcript data.
- **Quality Metrics:** p50/p95 inference latency tracking, retrieval precision/recall, and end-user (teacher) dashboard acceptance rates.

## Security & Safety

Offline execution natively provides high security, supplemented by strict logical isolation.

- **Prompt Injection Prevention:** Complete sanitization and encapsulation of untrusted audio transcripts to prevent audio-driven prompt injection.
- **Permission Controls:** Strict Role-Based Access Control (RBAC). Only system admins can access raw video; teachers access anonymized or preview summaries.
- **Sandboxing:** Container-level isolation and read-only file system mounts for worker services to prevent arbitrary execution.
- **Output Validation:** All LLM responses are constrained to Pydantic/JSON schemas. Failures fallback to a "Human Review Needed" flag instead of propagating malformed or unsafe advice.

## Observability

Comprehensive internal metrics gathering for FOSS offline tracking.

- **Tracing:** OpenTelemetry traces span from MediaMTX ingestion through API gateway to final worker completion.
- **Monitoring:** Grafana dashboards detailing VRAM utilization on the RTX 5070, worker queue depths, and API request latency.
- **Analytics:** Tracking heuristic Hot Path acceptance rates against Cold Path overrides.
- **Diagnostics:** Robust Dead Letter Queues (DLQ) for worker crashes, with full tracebacks and state-dumps for swift local debugging.

## Performance Optimization

Operating within strict edge hardware boundaries demands extreme efficiency.

- **Latency Optimization:** Real-time stream chunking into micro-batches for immediate engagement tracking.
- **Token Optimization:** Aggressive pre-processing and extractive summarization prior to LLM invocation.
- **Inference Efficiency:** Enforced INT4 quantization (AWQ/GGUF) for LLMs and INT8 for ASR models to remain under the 12GB VRAM RTX 5070 ceiling.
- **Caching Strategy:** Redis caching of recurrent template embeddings and previously answered queries to bypass repetitive inference.

## Risks & Tradeoffs

- **Hallucination Risks:** Using local, constrained 8B models inherently carries a higher risk of hallucination than proprietary GPT-4 class models.
- **Scalability Concerns:** Fixed physical GPU limits mean scaling must be handled chronologically (queuing) rather than horizontally, delaying Cold Path results during peak school hours.
- **Infrastructure Tradeoffs:** Maintaining a 100% FOSS offline stack drastically increases maintenance overhead and delays feature velocity compared to managed cloud services.
- **Operational Limitations:** Accurate multi-camera/multi-stream synchronization is mathematically complex without embedded hardware timestamps from diverse edge devices.

## Agile Sprint Plan

- **Sprint 1:** Stabilize local inference stack (Whisper INT8, Llama-3-8B INT4) and validate RTX 5070 memory budget utilization.
- **Sprint 2:** Implement robust worker queues (worker-asr, worker-cv) and establish the DAG orchestrator for Cold Path processing.
- **Sprint 3:** Deploy local pgvector RAG pipeline, ingest synthetic curricula, and integrate hybrid search with prompt validation.
- **Sprint 4:** Construct comprehensive evaluation metrics (WER, mAP, hallucination rates) and complete OpenTelemetry observability dashboard.
- **Expected AI Improvements:** A resilient, fully offline, FOSS-compliant AI pipeline capable of generating accurate pedagogical insights strictly constrained to local evidence.
