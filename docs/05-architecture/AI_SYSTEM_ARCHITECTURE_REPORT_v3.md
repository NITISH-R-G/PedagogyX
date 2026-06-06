# AI System Architecture Report v3

## AI Problem Analysis

The core objective of PedagogyX is to provide an elite multimodal AI classroom intelligence and teacher optimization platform. The system operates within highly constrained boundaries: it must utilize a FOSS-first software stack, run inference offline due to India data residency regulations, and process incoming audio/visual streams captured from low-end clients, primarily Meta Ray-Ban (DAT) smart glasses and basic Android/Windows devices.

- **Use case:** Real-time and batch pedagogical analysis to provide actionable insights and coaching to educators in classroom settings.
- **Requirements:** Support two operational modes: Hot Path (real-time low latency heuristics) and Cold Path (high-precision authoritative batch scoring).
- **Constraints:** Must use open-source models, run on local GPU infrastructure (RTX 5070), and operate fully offline without external API calls for data privacy.
- **User workflows:** Teachers wear Ray-Bans or use basic Android devices to capture classroom sessions, later reviewing their personalized pedagogical feedback and analytics on a dashboard.
- **Failure scenarios:** Out-of-sync audio/video streams, severe latency during the cold path processing, hallucinated coaching suggestions from the language models, prompt injections by adversarial users, and erratic classroom data.

## AI System Architecture

The AI stack separates into edge processing and centralized FOSS inference components.

- **Models:**
  - Speech-to-Text: Open-source Whisper variants optimized for RTX 5070 constraints.
  - Computer Vision: Lightweight YOLO models for real-time engagement and transformer models for batch multi-frame fusion.
  - LLMs: Locally deployed quantized LLMs (e.g., Llama 3/Mistral variants) focusing on summarization, pedagogical feedback, and report generation.
- **Orchestration:** Directed Acyclic Graph (DAG) pipelines managed via background worker queues (Python-based worker-asr, worker-cv, etc.) ensuring that the Cold Path processing handles complex sync and fusion systematically.
- **Retrieval Systems:** A vector store setup over Postgres (pgvector) to index and retrieve classroom segment templates, syllabus data, and historical pedagogical scores.
- **Memory Systems:** Short-term cache (Redis) for Hot Path diarization tracking; long-term durability in Postgres.
- **Infrastructure Topology:** Centralized FOSS backend inside an Indian data center or district-level edge nodes utilizing hybrid processing. The API Gateway routes capture data via MediaMTX to ingest queues.

## Prompt & Reasoning Strategy

Prompts are structured to maintain strict instructional boundaries and contextual accuracy when analyzing transcripts for teacher feedback.

- **Prompt structure:** Utilize few-shot prompting containing pedagogical templates (K-12 vs university) explicitly bounded by system guidelines.
- **Grounding strategy:** All LLM outputs must trace back to explicit transcript timestamps or CV events. The models are instructed never to guess user sentiment if not explicitly present.
- **Hallucination mitigation:** Implement a secondary validation chain where an LLM checks the proposed coaching tip against the retrieved facts and diarization confidence scores.
- **Context management:** Transcript chunks are strictly bounded and token-limited. Long sessions are summarized hierarchically before generating a final pedagogical score.

## RAG & Retrieval Design

To anchor AI feedback to specific curricula or institutional policies, RAG is utilized.

- **Ingestion pipeline:** School guidelines, rubrics, and best practices are periodically parsed and embedded into the system.
- **Embeddings:** Utilizing lightweight, sentence-transformers models to produce vector embeddings efficiently.
- **Vector database:** Postgres with the pgvector extension for unified ACID-compliant storage alongside structured data.
- **Reranking:** Cross-encoder reranking is applied for high-stakes policy matches during the authoritative batch scoring.
- **Retrieval workflows:** Hybrid search combines exact keyword matches for specific classroom events with semantic search for broader pedagogical concepts.

## AI Infrastructure

Infrastructure strictly targets local, self-hosted environments.

- **Inference systems:** Containerized model servers (e.g., vLLM or TGI) optimized using TensorRT/ONNX.
- **GPU infrastructure:** Relying on RTX 5070 clusters for both Hot (lightweight) and Cold (intensive) inference.
- **Scaling strategy:** Queue-based horizontal scaling of worker nodes. Hot Path workers use autoscaling based on stream count; Cold Path operates on a batch job scheduler.
- **Deployment systems:** Docker Compose for the current phase, heavily relying on the `compose.dev.yaml` for testing local deployments.

## Evaluation Strategy

A strong automated evaluation suite ensures safety and accuracy without relying purely on human intuition.

- **Benchmarks:** Test suites assessing ASR word error rate (WER) on noisy classroom audio and CV precision/recall on student engagement metrics.
- **Automated evals:** Unit testing via `pytest` simulating end-to-end synthetic sessions.
- **Hallucination tracking:** Utilizing specific automated rubrics to detect and score instances where the LLM produces advice without supporting transcript data.
- **Quality metrics:** p50/p95 inference latency, WER, context utilization efficiency, and user satisfaction (measured via dashboard interactions).

## Security & Safety

Ensuring the security of minor student data and the integrity of the models.

- **Prompt injection prevention:** Input sanitization layers separate untrusted audio transcripts from internal system prompts.
- **Permission controls:** Strict RBAC limits viewing raw student video to admins, while teachers only see preview scores and actionable feedback.
- **Sandboxing:** Inference processes run in isolated, read-only containers.
- **Output validation:** Rigid JSON schema validation forces the LLMs to return strict structured outputs. Failures trigger default "Review Needed" states rather than hallucinations.

## Observability

Critical for tracking FOSS offline model performance.

- **Tracing:** Full trace logs connecting incoming Ray-Ban streams to final pedagogical scores using OpenTelemetry.
- **Monitoring:** Grafana dashboards detailing worker queue depth, RTX 5070 VRAM usage, and API latency.
- **Analytics:** Tracking the ratio of hot path heuristics vs cold path authoritative overrides.
- **Diagnostics:** Comprehensive dead-letter queue (DLQ) implementations capturing full tracebacks for worker failures.

## Performance Optimization

Operating within strict offline and edge hardware limitations.

- **Latency optimization:** Streaming transcription where possible on the edge; separating logic into distinct micro-batches (e.g., 2s windows).
- **Token optimization:** Summarizing text aggressively before invoking the heavy LLM.
- **Inference efficiency:** Using integer quantization (INT4/INT8) on LLMs to fit within the RTX 5070 VRAM limits.
- **Caching strategy:** Redis-based caching of recurrently evaluated templates and intermediate embedding outputs.

## Risks & Tradeoffs

- **Hallucination risks:** Utilizing smaller local models increases the risk of subtle hallucinations compared to proprietary large models, necessitating stronger verification checks.
- **Scalability concerns:** Offline GPU provisioning means rigid scaling limits; high-load scenarios will inevitably delay cold-path authoritative scoring.
- **Infrastructure tradeoffs:** FOSS-first creates maintenance overhead and reduces access to state-of-the-art managed models.
- **Operational limitations:** Complex multi-stream synchronization (A/V drift) is hard to correct robustly without custom hardware timestamps.

## Agile Sprint Plan

- **Milestones:** Finalize integration of open-source whisper models, implement Hot Path inference, deploy RAG framework, and fully integrate Cold Path processing.
- **Implementation phases:** Phase 1 (Baseline ASR), Phase 2 (Real-time heuristics), Phase 3 (RAG + Prompting), Phase 4 (Evaluation + Refinement).
- **Evaluation checkpoints:** Weekly reviews of WER, p50/p95 latency, and automated hallucination scores.
- **Expected AI improvements:** A fully FOSS AI pipeline achieving baseline pedagogical scoring with zero external API calls and continuously improving model alignment with school guidelines.
