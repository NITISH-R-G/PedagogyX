# AI System Architecture Report v3

## AI Problem Analysis

The core objective of PedagogyX is to provide a world-class multimodal AI classroom intelligence and teacher optimization platform. The system operates within highly constrained boundaries: it must utilize a FOSS-first software stack, run inference offline due to India data residency regulations, and process incoming audio/visual streams captured from low-end clients, primarily Meta Ray-Ban (DAT) smart glasses and basic Android/Windows devices.
We aim to solve the high-latency and reliability issues inherent in edge computing by splitting workloads.
Requirements dictate two operational modes:

- **Hot Path (Real-time):** Fast, low-latency heuristics for activity detection (YOLO), talk ratios, and basic live analytics.
- **Cold Path (Batch):** High-precision, authoritative pedagogy scoring, complete multi-cam alignment, thorough transcription via ASR, and full diarization powered by advanced GPU (RTX 5070) inference workers.

Failure scenarios involve out-of-sync audio/video streams, severe latency during the cold path processing, hallucinated coaching suggestions from the language models, prompt injections by adversarial users, and drift in long-term tracking.

## AI System Architecture

The AI stack separates into edge processing and centralized FOSS inference components, designed for production reliability and multi-tenant scaling.

- **Models:**
  - Speech-to-Text: Open-source Whisper variants optimized for RTX 5070 constraints.
  - Computer Vision: Lightweight YOLO models for real-time engagement and transformer models for batch multi-frame fusion.
  - LLMs: Locally deployed quantized LLMs (e.g., Llama 3/Mistral variants) focusing on summarization, pedagogical feedback, and report generation.
- **Orchestration:** Directed Acyclic Graph (DAG) pipelines managed via background worker queues (Python-based worker-asr, worker-cv, etc.) ensuring that the Cold Path processing handles complex sync and fusion systematically.
- **Retrieval Systems:** A vector store setup over Postgres (pgvector) to index and retrieve classroom segment templates, syllabus data, and historical pedagogical scores.
- **Memory Systems:** Short-term cache (Redis) for Hot Path diarization tracking; long-term durability in Postgres. Multi-turn context persistence for LLM memory.
- **Infrastructure Topology:** Centralized FOSS backend inside an Indian data center or district-level edge nodes utilizing hybrid processing. The API Gateway routes capture data via MediaMTX to ingest queues.

## Prompt & Reasoning Strategy

Prompts are structured to maintain strict instructional boundaries and contextual accuracy when analyzing transcripts for teacher feedback.

- **Prompt Structure:** Utilize few-shot prompting containing pedagogical templates (K-12 vs university) explicitly bounded by system guidelines. System prompts are rigid and declarative.
- **Grounding Strategy:** All LLM outputs must trace back to explicit transcript timestamps or CV events. The models are instructed never to guess user sentiment if not explicitly present. Output relies strictly on retrieval context.
- **Hallucination Mitigation:** Implement a secondary validation chain where a separate LLM checks the proposed coaching tip against the retrieved facts and diarization confidence scores.
- **Context Management:** Transcript chunks are strictly bounded and token-limited. Long sessions are summarized hierarchically before generating a final pedagogical score, avoiding middle-context loss.

## RAG & Retrieval Design

To anchor AI feedback to specific curricula or institutional policies, RAG is utilized.

- **Ingestion Pipeline:** School guidelines and best practices are periodically embedded into the system. Automated chunking splits policies logically by section.
- **Embeddings:** Utilizing lightweight, sentence-transformers models optimized for dense semantic representation.
- **Vector Database:** Postgres with the pgvector extension for unified ACID-compliant storage alongside structured data.
- **Reranking:** Cross-encoder reranking is applied for high-stakes policy matches during the authoritative batch scoring.
- **Retrieval Workflows:** Hybrid search combines exact keyword matches for specific classroom events with semantic search for pedagogical concepts.

## AI Infrastructure

Infrastructure strictly targets local, self-hosted environments.

- **Inference Systems:** Containerized model servers optimized using TensorRT/ONNX. vLLM or similar engines used for high-throughput LLM serving.
- **GPU Infrastructure:** Relying on RTX 5070 clusters for both Hot (lightweight) and Cold (intensive) inference.
- **Scaling Strategy:** Queue-based horizontal scaling of worker nodes. Hot Path workers use autoscaling based on stream count; Cold Path operates on a batch job scheduler.
- **Deployment Systems:** Docker Compose for the current phase, heavily relying on the `compose.dev.yaml` for testing local deployments, moving toward a localized Kubernetes approach for multi-node deployments.

## Evaluation Strategy

A strong automated evaluation suite ensures safety and accuracy without relying purely on human intuition.

- **Benchmarks:** Test suites assessing ASR word error rate (WER) on noisy classroom audio and CV precision/recall on student engagement metrics.
- **Automated Evals:** Unit testing via `pytest` simulating end-to-end synthetic sessions. Automated reliability scoring for LLM responses.
- **Hallucination Tracking:** Utilizing specific automated rubrics to detect and score instances where the LLM produces advice without supporting transcript data.
- **Quality Metrics:** p50/p95 inference latency, WER, context utilization efficiency, prompt robustness, and user satisfaction (measured via dashboard interactions).

## Security & Safety

Ensuring the security of minor student data and the integrity of the models.

- **Prompt Injection Prevention:** Input sanitization layers separate untrusted audio transcripts from internal system prompts.
- **Permission Controls:** Strict RBAC limits viewing raw student video to admins, while teachers only see preview scores and actionable feedback.
- **Sandboxing:** Inference processes run in isolated, read-only containers without external network access.
- **Output Validation:** Rigid JSON schema validation forces the LLMs to return strict structured outputs. Failures trigger default "Review Needed" states rather than hallucinations.

## Observability

Critical for tracking FOSS offline model performance.

- **Tracing:** Full trace logs connecting incoming Ray-Ban streams to final pedagogical scores using OpenTelemetry.
- **Monitoring:** Grafana dashboards detailing worker queue depth, RTX 5070 VRAM usage, GPU utilization, and API latency.
- **Analytics:** Tracking the ratio of hot path heuristics vs cold path authoritative overrides, token consumption, and retrieval failures.
- **Diagnostics:** Comprehensive dead-letter queue (DLQ) implementations capturing full tracebacks for worker failures.

## Performance Optimization

Operating within strict offline and edge hardware limitations.

- **Latency Optimization:** Streaming transcription where possible on the edge; separating logic into distinct micro-batches (e.g., 2s windows). Speculative decoding where applicable.
- **Token Optimization:** Summarizing text aggressively before invoking the heavy LLM. Batching requests for higher throughput.
- **Inference Efficiency:** Using integer quantization (INT4/INT8) on LLMs to fit within the RTX 5070 VRAM limits and accelerate decoding.
- **Caching Strategy:** Redis-based caching of recurrently evaluated templates and intermediate embedding outputs.

## Risks & Tradeoffs

- **Hallucination Risks:** Utilizing smaller local models increases the risk of subtle hallucinations compared to proprietary large models, necessitating stronger verification checks.
- **Scalability Concerns:** Offline GPU provisioning means rigid scaling limits; high-load scenarios will inevitably delay cold-path authoritative scoring.
- **Infrastructure Tradeoffs:** FOSS-first creates maintenance overhead and reduces access to state-of-the-art managed models.
- **Operational Limitations:** Complex multi-stream synchronization (A/V drift) is hard to correct robustly without custom hardware timestamps.

## Agile Sprint Plan

- **Milestone 1:** Upgrade the RAG pipeline with cross-encoder reranking to improve grounding.
- **Milestone 2:** Implement hierarchical summarization to handle long transcripts within token limits.
- **Milestone 3:** Deploy observability dashboards tracking p50/p95 inference latency, WER, and token efficiency.
- **Milestone 4:** Conduct rigorous automated evals on hallucination rates and prompt injection vulnerabilities.
- **Expected Improvements:** Improved model reliability, lower hallucination rates, enhanced context management, and better production-readiness of the offline inference pipeline.
