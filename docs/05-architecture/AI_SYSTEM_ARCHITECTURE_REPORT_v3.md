# AI System Architecture Report v3

## AI Problem Analysis

- **Use Case:** PedagogyX acts as an elite multimodal AI classroom intelligence and teacher optimization platform for K-12 and university education in India. It captures continuous teaching sessions via Meta Ray-Ban smart glasses (POV video + audio) through an Android DAT host.
- **Requirements:** The system must run on a fully FOSS-first software stack and execute inference entirely offline/on-premises to comply with strict India DPDP data residency regulations. It demands a dual-path pipeline: a hot path for near real-time heuristics (activity detection, talk ratios) and a cold path for authoritative batch pedagogical scoring, multi-cam alignment, and deep diarization.
- **Constraints:** Compute is strictly capped at RTX 5070 (12GB VRAM) for local/edge cloud workers. High-throughput edge LAN ingestion with offline resilience is required.
- **User Workflows:** Teachers record sessions without friction. Streams buffer at the school edge and sync to the PedagogyX central nodes. Administrators receive detailed, reliable, evidence-backed pedagogical reports.
- **Failure Scenarios:** Unpredictable network environments causing severe packet loss, A/V synchronization drift, GPU Out-of-Memory (OOM) during concurrent ML fusion, and model hallucinations leading to loss of teacher trust.

## AI System Architecture

- **Models:** Open-source models constrained to RTX 5070. ASR relies on quantized Whisper variants (English + Hindi code-switching). CV utilizes lightweight YOLOv8 for hot-path detection and 4-bit LLaVA/MobileVLM for batch multi-modal understanding. LLM reasoning uses quantized Llama 3 or Qwen2.5-7B-Q4.
- **Orchestration:** Managed via asynchronous DAG pipelines (e.g., Celery/Temporal). Discrete worker nodes (worker-asr, worker-cv, worker-metrics) ensure fault-tolerant cold path processing.
- **Retrieval Systems:** A highly optimized RAG system powered by Postgres + pgvector indexing classroom segment templates, syllabus data, and historical teacher scoring to provide grounded context.
- **Memory Systems:** Redis handles short-term context cache and hot path diarization tracking. Long-term durability and session artifacts are retained in MinIO and Postgres.
- **Infrastructure Topology:** Android DAT Host -> Edge LAN Buffer/Ingest -> MediaMTX (WebRTC/Stream) -> API Gateway -> Postgres/MinIO & Queue -> RTX 5070 GPU Workers (Central India Cloud).

## Prompt & Reasoning Strategy

- **Prompt Structure:** Multi-shot, deterministic prompts employing persona structures bounded by explicit K-12/University pedagogical guidelines.
- **Grounding Strategy:** All LLM outputs must be explicitly anchored to specific timestamped evidence from the transcript and diarization pipeline. Output is restricted via constrained decoding (JSON schema validation).
- **Hallucination Mitigation:** Stringent secondary validation chains where an evaluator LLM cross-references proposed coaching tips against retrieved facts, exact transcript snippets, and diarization confidence scores.
- **Context Management:** Implementation of hierarchical chunking. Long lectures are recursively summarized, retaining critical pedagogical events before generating the final comprehensive score.

## RAG & Retrieval Design

- **Ingestion Pipeline:** School guidelines, pedagogical best practices, and chunked ASR transcripts enriched with CV bounding-box context are periodically embedded.
- **Embeddings:** Domain-adapted sentence transformers optimized for code-switched instructional dialogue (English/Hindi) and low-latency vector generation.
- **Vector Database:** Postgres with the pgvector extension for unified, ACID-compliant vector and relational data storage.
- **Reranking:** Cross-encoder reranking is applied to top-K retrieved chunks to ensure absolute highest relevance during authoritative batch scoring.
- **Retrieval Workflows:** Hybrid search combines exact keyword matching for explicit pedagogical events with semantic search for broader instructional concepts.

## AI Infrastructure

- **Inference Systems:** Containerized model servers optimized using TensorRT/ONNX and vLLM for high-throughput, continuous batching and PagedAttention.
- **GPU Infrastructure:** A strictly homogeneous pool of RTX 5070 12GB GPUs. Workloads (ASR, CV, LLM) are aggressively isolated or utilize context offloading to avoid OOM limits.
- **Scaling Strategy:** Queue-based horizontal autoscaling. GPU worker pods scale based on the Cold Path backlog. Hot path operations default to lightweight CPU/edge models where applicable.
- **Deployment Systems:** Docker Compose for edge nodes and MVP boilerplates, with Kubernetes (K3s) for the central India Cloud cluster.

## Evaluation Strategy

- **Benchmarks:** Rigorous test suites measuring ASR Word Error Rate (WER) and Diarization Error Rate (DER) on noisy Indian classroom audio. CV precision/recall on student engagement tracking.
- **Automated Evals:** End-to-end `pytest` simulations and LLM-as-a-judge pipelines validating JSON schema adherence, citation accuracy, and hallucination rates on nightly builds.
- **Hallucination Tracking:** Automated rubrics compare LLM generated evidence strings against exact substring matches in the source transcript, logging failure rates in observability dashboards.
- **Quality Metrics:** Track p50/p95 inference latency, context utilization efficiency, token limits, and product usage (time-to-insight).

## Security & Safety

- **Prompt Injection Prevention:** Input sanitization layers strictly separate untrusted student/teacher audio transcripts from internal system prompts.
- **Permission Controls:** Enforced Role-Based Access Control (RBAC). Teachers can only view their own insights, while school admins access aggregate reports. Raw video access is heavily restricted.
- **Sandboxing:** Inference and data parsing processes run inside isolated, read-only containers with low privileges.
- **Output Validation:** Rigid Pydantic/JSON schema validation ensures models return structured outputs. Failures trigger safe "Review Needed" fallback states.

## Observability

- **Tracing:** Full trace logs connecting incoming Ray-Ban streams to the final pedagogical scores using OpenTelemetry.
- **Monitoring:** Comprehensive Grafana dashboards tracking worker queue depth, specific RTX 5070 VRAM utilization, and API endpoint p95 latencies.
- **Analytics:** Tracking the ratio of hot path heuristic events versus cold path authoritative overrides.
- **Diagnostics:** Centralized dead-letter queue (DLQ) implementations capturing full tracebacks for worker failures to enable rapid debugging.

## Performance Optimization

- **Latency Optimization:** Separating logic into micro-batches (e.g., 2s windows) for edge processing. Hot path relies purely on heuristics and lightweight CV models.
- **Token Optimization:** Aggressive filtering of silence and non-instructional audio prior to ASR. Summarizing text significantly before invoking heavy LLM reasoning.
- **Inference Efficiency:** Using 4-bit integer quantization (INT4/AWQ/GPTQ) on LLMs to strictly operate within the 12GB VRAM limit while maintaining reasoning quality.
- **Caching Strategy:** Redis-based caching of recurrently evaluated pedagogical templates and MinIO caching of intermediate ML representations (ASR transcripts).

## Risks & Tradeoffs

- **Hallucination Risks:** Using smaller, 7B-class local quantized models elevates the risk of subtle hallucinations in complex pedagogical reasoning compared to proprietary frontier models. Requires extensive verification checks.
- **Scalability Concerns:** Offline, RTX 5070 GPU hardware provisioning implies rigid scaling ceilings. High-load scenarios will queue deeply and delay the cold-path authoritative scoring.
- **Infrastructure Tradeoffs:** FOSS-first stack provides zero external dependencies and ensures data residency but creates massive maintenance overhead and limits access to SOTA capabilities.
- **Operational Limitations:** Correcting multi-stream A/V drift is inherently complex without custom hardware clock sync on the capture devices, leading to potential alignment issues.

## Agile Sprint Plan

- **Milestones:**
  - Milestone 1: Finalize integration of FOSS models (Whisper, YOLO, Qwen2.5-7B) on RTX 5070 hardware constraints and deploy worker queues.
  - Milestone 2: Complete the edge LAN ingestion buffer and hot path real-time metrics generation.
  - Milestone 3: Implement pgvector RAG pipeline and the cold path multi-modal batch fusion.
  - Milestone 4: Establish automated LLM-as-a-judge evaluation pipelines, hallucination tracking, and OpenTelemetry observability.
- **Implementation Phases:** Iterative testing of A/V sync, RAG retrieval accuracy, and prompt robustness against adversarial/noisy inputs.
- **Evaluation Checkpoints:** Bi-weekly reviews of WER/DER metrics, P95 latency reports, and hallucination rate tracking.
- **Expected AI Improvements:** A fully autonomous, zero-API FOSS pipeline delivering high-precision pedagogical scoring at the edge.
