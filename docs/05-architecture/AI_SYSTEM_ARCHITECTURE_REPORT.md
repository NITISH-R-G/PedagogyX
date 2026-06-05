# Autonomous Senior AI Engineer & Applied Intelligence Systems Architect Report

## AI Problem Analysis

- **Use Case:** PedagogyX is an AI-powered classroom intelligence and teacher optimization platform targeting K-12 and university segments in India. The system captures live teaching sessions using Meta Ray-Ban smart glasses (POV video + audio) via an Android DAT host, processing streams to evaluate teacher pedagogy, instructional quality, and discourse patterns.
- **Requirements:** Must operate entirely on OSS-first infrastructure (no proprietary SaaS APIs like OpenAI/Deepgram), ensuring data residency in India. Must handle high-throughput edge LAN ingestion with offline resilience. Must provide a dual-path pipeline: a hot path for near real-time lightweight activity detection, and a cold path for authoritative batch processing of ML fusion, ASR, CV, and LLM-based pedagogical scoring.
- **Constraints:** Compute budget is strictly constrained to RTX 5070 (12GB VRAM) for cloud workers. The system requires real-time capabilities without exorbitant hardware scaling, mandating heavy quantization and efficient batching for heavy models. Legal compliance (DPDP) and strict role-based access control (RBAC) are required for teacher supervision modes.
- **User Workflows:** Teachers record sessions seamlessly using smart glasses. Streams are buffered at the school edge and uploaded to the PedagogyX cloud. School administrators and deans receive authoritative pedagogical score reports and evidence-backed insights derived from the cold path.
- **Failure Scenarios:** Unpredictable network environments causing packet loss and A/V drift; edge buffering failure; GPU OOM errors on RTX 5070 workers during concurrent transcode/inference; hallucinated pedagogical feedback damaging teacher trust; privacy leaks via unauthorized stream access.

## AI System Architecture

- **Models:**
  - **ASR:** Distil-Whisper or Whisper v3 (quantized) for English + Hindi code-switching.
  - **CV:** Lightweight YOLOv8 for hot-path activity detection; MobileVLM or LLaVA (4-bit quantization) for batch multi-modal pedagogical understanding.
  - **LLM/Reasoning:** Qwen2.5-7B-Q4 (running on vLLM/Ollama) for generating pedagogy scores, instructional quality metrics, and structured reports.
- **Orchestration:** Multi-stage asynchronous pipeline orchestrated via Celery or Temporal. Jobs are enqueued from the API gateway, distributed to specialized GPU workers (ASR vs CV vs LLM), with explicit Dead Letter Queues (DLQs) for failed processing.
- **Retrieval Systems:** A hybrid architecture where session metadata and pedagogical templates are retrieved via pgvector (PostgreSQL) combined with standard relational queries, ensuring responses are grounded in institution-specific rubrics.
- **Memory Systems:** Short-term context managed via Redis for the hot path and rolling stream state. Long-term session artifacts, diarization maps, and embeddings stored in MinIO and Postgres.
- **Infrastructure Topology:** Android DAT Host -> Edge LAN Buffer/Ingest -> MediaMTX (WebRTC/Stream) -> API Gateway -> Postgres/MinIO & Queue -> RTX 5070 GPU Workers (India Cloud).

## Prompt & Reasoning Strategy

- **Prompt Structure:** Multi-shot, deterministic prompts defining clear personas (e.g., "Expert Pedagogy Evaluator"). Prompts strictly separate session transcripts (ASR context) from the task instructions (pedagogical rubric evaluation) to prevent prompt injection or drift.
- **Grounding Strategy:** All LLM conclusions must be explicitly linked to specific timestamped evidence from the transcript and diarization pipeline. Output is restricted to JSON schemas via constrained decoding (e.g., Guidance/Outlines or vLLM guided decoding).
- **Hallucination Mitigation:** Implement strict temperature=0 decoding for scoring tasks. Use self-consistency checks for complex inferences. Any claim without a direct reference to the ASR transcript is flagged and discarded.
- **Context Management:** Implement hierarchical chunking for long lectures (e.g., 45-minute sessions). Summarize smaller segments recursively, passing segment summaries and key transcript chunks to the final evaluation prompt to fit within the 8k-32k context limits of the 7B model.

## RAG & Retrieval Design

- **Ingestion Pipeline:** Chunked ASR transcripts are enriched with speaker diarization tags and CV bounding-box context. These chunks are normalized and processed into dense embeddings.
- **Embeddings:** Domain-adapted sentence transformers optimized for code-switched instructional dialogue (English/Hindi).
- **Vector Database:** pgvector extension in the primary PostgreSQL database to reduce infrastructure complexity while supporting hybrid semantic/keyword search.
- **Reranking:** Lightweight cross-encoder applied to top-K retrieved chunks to ensure highest relevance when extracting evidence for the final pedagogical report.
- **Retrieval Workflows:** When generating feedback on a specific rubric dimension (e.g., "Student Talk Ratio"), query the vector store for relevant pedagogical segments, retrieve exact transcript chunks, and pass to the LLM.

## AI Infrastructure

- **Inference Systems:** vLLM deployed on bare-metal or K3s nodes to maximize throughput for the Qwen2.5-7B model using continuous batching and PagedAttention.
- **GPU Infrastructure:** Highly optimized, homogenous pool of RTX 5070 12GB GPUs. Memory boundaries strictly enforced: ASR, CV, and LLM workloads must either run on separate dedicated workers or utilize aggressive context offloading to avoid OOM.
- **Scaling Strategy:** Queue-based horizontal autoscaling. Scale GPU worker pods based on queue length (Cold Path backlog). Hot path utilizes lightweight non-GPU or CPU-optimized models where possible.
- **Deployment Systems:** Docker Compose for Edge nodes; Kubernetes (K3s) for the central India Cloud cluster. CI/CD pipelines automate model fetching, quantization validation, and container registry publishing.

## Evaluation Strategy

- **Benchmarks:** Evaluate model performance on domain-specific test sets for English-Hindi code-switched ASR Word Error Rate (WER), Diarization Error Rate (DER), and pedagogical scoring correlation with human expert baselines.
- **Automated Evals:** LLM-as-a-judge pipelines validating structured JSON schema adherence, citation accuracy, and hallucination rates on nightly builds.
- **Hallucination Tracking:** Compare LLM generated evidence strings against exact substring matches in the source transcript. Track failure rates in observability dashboards.
- **Quality Metrics:** Maintain precision/recall metrics for activity detection. Monitor the distribution of pedagogical scores to detect model drift or bias over time.

## Security & Safety

- **Prompt Injection Prevention:** Sanitize ASR transcripts to neutralize malicious user speech attempting to hijack the evaluator prompt (e.g., treating transcripts strictly as data payloads, not executable instructions).
- **Permission Controls:** Implement strict RBAC via the API Gateway. Teachers can access their own data; Deans/Admins access aggregate scores. Models never access cross-tenant data.
- **Sandboxing:** Run all data parsing and multi-modal pre-processing in isolated, low-privilege containers.
- **Output Validation:** Pydantic models validate all LLM outputs before they are saved to the pedagogical score store.

## Observability

- **Tracing:** Implement OpenTelemetry across the capture agent, ingest edge, API, and GPU workers to trace end-to-end latency from chunk capture to final score generation.
- **Monitoring:** Grafana dashboards tracking GPU utilization (VRAM, compute), Celery queue lengths, DLQ failure rates, and endpoint p95 latencies.
- **Analytics:** Product analytics on time-to-insight, capturing the delay between session end and availability of the authoritative batch report.
- **Diagnostics:** Full tracebacks logged to `sys.stderr` and captured in centralized logging for DLQ events, enabling rapid debugging of failed pipeline stages.

## Performance Optimization

- **Latency Optimization:** The hot path avoids LLM calls entirely, relying on heuristics and lightweight CV models. The cold path processes audio and video concurrently before the fusion step.
- **Token Optimization:** Filter out silence and non-instructional audio prior to ASR. Use prompt caching techniques in vLLM for the static portions of the pedagogical evaluation prompt.
- **Inference Efficiency:** Utilize 4-bit AWQ/GPTQ quantization for the 7B LLM to fit comfortably in 12GB VRAM while leaving room for KV cache and context. Use batched processing in vLLM to maximize throughput over latency for the cold path.
- **Caching Strategy:** Cache intermediate ML representations (e.g., ASR transcripts) in MinIO. Use Redis for fast lookup of session states and deduplication of repeated inference requests.

## Risks & Tradeoffs

- **Hallucination Risks:** Evaluating teaching quality is highly subjective; the 7B model may confidently output incorrect assessments or misinterpret sarcasm/cultural nuances in Indian classrooms. Requires heavy reliance on deterministic rules alongside LLM outputs.
- **Scalability Concerns:** The RTX 5070 12GB constraint creates a hard ceiling on concurrent LLM context size. Long 45-minute sessions must be aggressively chunked, risking loss of global context.
- **Infrastructure Tradeoffs:** Self-hosting OSS models saves operational expenditure but drastically increases DevOps complexity and deployment friction compared to managed APIs.
- **Operational Limitations:** Handling network instability from edge to central cloud means the system must gracefully handle out-of-order chunks and incomplete sessions, complicating the A/V sync logic.

## Agile Sprint Plan

- **Sprint 1 (Infrastructure & MVP ASR):** Setup RTX 5070 worker nodes. Deploy vLLM and Whisper. Implement the chunked ASR pipeline and basic audio processing queue.
- **Sprint 2 (Data Ingestion & Hot Path):** Develop the Android DAT host integration. Build the edge LAN buffer. Implement lightweight hot-path activity detection heuristics.
- **Sprint 3 (Cold Path & LLM Reasoning):** Implement the full batch ML fusion pipeline. Develop and evaluate the Qwen2.5-7B prompts for pedagogical scoring. Integrate pgvector for template retrieval.
- **Sprint 4 (Observability & Hardening):** Implement OpenTelemetry and Grafana dashboards. Establish the automated evaluation pipeline for hallucination tracking and schema validation. Conduct end-to-end latency and VRAM stress testing.
- **Sprint 5 (Pilot & Refinement):** Deploy to pilot schools. Monitor model drift. Iterate on prompt grounding based on real-world classroom acoustics and edge cases.
