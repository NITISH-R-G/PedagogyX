# AI System Architecture Report v3

## AI Problem Analysis

The core objective of PedagogyX is to provide an elite multimodal AI classroom intelligence and teacher optimization platform. The system operates within highly constrained boundaries: it must utilize a FOSS-first software stack, run inference offline due to India data residency regulations, and process incoming audio/visual streams captured from low-end clients, primarily Meta Ray-Ban (DAT) smart glasses and basic Android/Windows devices. We must scale to hundreds of classrooms, while strictly bounding context to prevent hallucinations. We cannot rely on proprietary APIs, mandating rigorous efficiency in local hardware.

Requirements dictate two operational modes:

- **Hot Path (Real-time):** Fast, low-latency heuristics for activity detection (YOLO), talk ratios, and basic live analytics to give immediate feedback.
- **Cold Path (Batch):** High-precision, authoritative pedagogy scoring, complete multi-cam alignment, thorough transcription via ASR, and full diarization powered by advanced GPU (RTX 5070) inference workers.

Failure scenarios involve out-of-sync audio/video streams, severe latency during the cold path processing leading to outdated reports, hallucinated coaching suggestions from the language models disconnected from actual transcripts, and prompt injections by adversarial users or erratic classroom data.

## AI System Architecture

The AI stack separates into edge processing and centralized FOSS inference components, organized using a strictly decoupled microservices pattern.

- **Models:**
  - Speech-to-Text: Open-source Whisper variants optimized for RTX 5070 constraints (e.g., Whisper-v3-Turbo or distil-whisper) via fast whisper.
  - Computer Vision: Lightweight YOLO models for real-time engagement and transformer models for batch multi-frame fusion.
  - LLMs: Locally deployed quantized LLMs (e.g., Llama 3 8B or Mistral v0.3) focusing on summarization, pedagogical feedback, and report generation via vLLM.
- **Orchestration:** Directed Acyclic Graph (DAG) pipelines managed via background worker queues (Python-based worker-asr, worker-cv, etc.) using Celery/Redis, ensuring that the Cold Path processing handles complex sync and fusion systematically.
- **Retrieval Systems:** A vector store setup over Postgres (pgvector) to index and retrieve classroom segment templates, syllabus data, and historical pedagogical scores.
- **Memory Systems:** Short-term cache (Redis) for Hot Path diarization tracking; long-term durability in Postgres, tracking entity relationships.
- **Infrastructure Topology:** Centralized FOSS backend inside an Indian data center or district-level edge nodes utilizing hybrid processing. The API Gateway routes capture data via MediaMTX to ingest queues.

## Prompt & Reasoning Strategy

Prompts are structured to maintain strict instructional boundaries and contextual accuracy when analyzing transcripts for teacher feedback. System prompts define a hardened persona.

- **Prompt Structure:** Utilize few-shot prompting containing pedagogical templates (K-12 vs university) explicitly bounded by system guidelines. We use strict `<context>` XML boundaries.
- **Grounding Strategy:** All LLM outputs must trace back to explicit transcript timestamps or CV events. The models are instructed never to guess user sentiment if not explicitly present.
- **Hallucination Mitigation:** Implement a secondary validation chain where an LLM checks the proposed coaching tip against the retrieved facts and diarization confidence scores. "I don't know" logic is explicitly mapped to missing contextual data.
- **Context Management:** Transcript chunks are strictly bounded and token-limited via a rolling window approach with 15% overlap. Long sessions are summarized hierarchically before generating a final pedagogical score.

## RAG & Retrieval Design

To anchor AI feedback to specific curricula or institutional policies, RAG is utilized. We prioritize precision over pure recall to guarantee high-fidelity pedagogy mapping.

- **Ingestion Pipeline:** School guidelines and best practices are periodically embedded into the system. Chunking is done semantically by pedagogical rules rather than fixed length.
- **Embeddings:** Utilizing lightweight, sentence-transformers models (e.g., BGE-m3 or MiniLM) to produce vector embeddings.
- **Vector Database:** Postgres with the pgvector extension for unified ACID-compliant storage alongside structured data.
- **Reranking:** Cross-encoder reranking is applied for high-stakes policy matches during the authoritative batch scoring to ensure top-K results are strictly relevant.
- **Retrieval Workflows:** Hybrid search combines exact keyword matches (BM25) for specific classroom events with semantic search for pedagogical concepts.

## AI Infrastructure

Infrastructure strictly targets local, self-hosted environments. Every hardware constraint is a hard boundary.

- **Inference Systems:** Containerized model servers optimized using vLLM for high throughput and continuous batching.
- **GPU Infrastructure:** Relying on RTX 5070 clusters (12GB VRAM) for both Hot (lightweight) and Cold (intensive) inference.
- **Scaling Strategy:** Queue-based horizontal scaling of worker nodes. Hot Path workers use autoscaling based on stream count; Cold Path operates on a batch job scheduler to maximize GPU utilization 24/7.
- **Deployment Systems:** Docker Compose for the current phase, heavily relying on the `compose.dev.yaml` for testing local deployments. Future production targets bare-metal Kubernetes.

## Evaluation Strategy

A strong automated evaluation suite ensures safety and accuracy without relying purely on human intuition. AI quality must be measured systematically.

- **Benchmarks:** Test suites assessing ASR word error rate (WER) on noisy classroom audio and CV precision/recall on student engagement metrics.
- **Automated Evals:** Unit testing via `pytest` simulating end-to-end synthetic sessions. LLM-as-a-judge frameworks specifically tuned to evaluate pedagogical rubric alignment.
- **Hallucination Tracking:** Utilizing specific automated rubrics to detect and score instances where the LLM produces advice without supporting transcript data.
- **Quality Metrics:** p50/p95 inference latency, WER, context utilization efficiency, structured output failure rate, and user satisfaction (measured via dashboard interactions).

## Security & Safety

Ensuring the security of minor student data and the integrity of the models is a baseline requirement.

- **Prompt Injection Prevention:** Input sanitization layers separate untrusted audio transcripts from internal system prompts. System prompts are immutable at runtime.
- **Permission Controls:** Strict RBAC limits viewing raw student video to admins, while teachers only see preview scores and actionable feedback.
- **Sandboxing:** Inference processes run in isolated, read-only containers with no external network access.
- **Output Validation:** Rigid JSON schema validation forces the LLMs to return strict structured outputs. Failures trigger default "Review Needed" states rather than hallucinations. Outlines schema validation via pydantic.

## Observability

Critical for tracking FOSS offline model performance and resolving production bottlenecks rapidly.

- **Tracing:** Full trace logs connecting incoming Ray-Ban streams to final pedagogical scores using OpenTelemetry.
- **Monitoring:** Grafana dashboards detailing worker queue depth, RTX 5070 VRAM usage, KV cache utilization, and API latency.
- **Analytics:** Tracking the ratio of hot path heuristics vs cold path authoritative overrides, tracking token consumption.
- **Diagnostics:** Comprehensive dead-letter queue (DLQ) implementations capturing full tracebacks for worker failures.

## Performance Optimization

Operating within strict offline and edge hardware limitations demands aggressive optimization.

- **Latency Optimization:** Streaming transcription where possible on the edge; separating logic into distinct micro-batches (e.g., 2s windows) for the hot path.
- **Token Optimization:** Summarizing text aggressively before invoking the heavy LLM. Caching frequent pedagogical rule explanations.
- **Inference Efficiency:** Using AWQ/GPTQ 4-bit integer quantization on LLMs to fit comfortably within the RTX 5070 12GB VRAM limits while leaving room for the context window.
- **Caching Strategy:** Redis-based caching of recurrently evaluated templates and intermediate embedding outputs.

## Risks & Tradeoffs

- **Hallucination Risks:** Utilizing smaller local models (8B class) increases the risk of subtle hallucinations compared to proprietary large models, necessitating stronger verification checks and validation layers.
- **Scalability Concerns:** Offline GPU provisioning means rigid scaling limits; high-load scenarios will inevitably delay cold-path authoritative scoring. Queue depths may spike.
- **Infrastructure Tradeoffs:** FOSS-first creates maintenance overhead and reduces access to state-of-the-art managed models. We trade operational simplicity for absolute data privacy and offline capability.
- **Operational Limitations:** Complex multi-stream synchronization (A/V drift) is hard to correct robustly without custom hardware timestamps. We must rely heavily on heuristics.

## Agile Sprint Plan

- **Milestone 1:** Finalize integration of open-source whisper models and deploy basic worker-asr queues with GPU limits enforced.
- **Milestone 2:** Implement Hot Path lightweight YOLO inference and basic dashboard metrics, ensuring realtime latency constraints.
- **Milestone 3:** Deploy initial RAG framework using pgvector and establish basic prompt structures for pedagogical rule adherence.
- **Milestone 4:** Full integration of Cold Path multi-stream batch processing and deployment of comprehensive evaluation test suites (WER, latency, hallucination tracking).
- **Milestone 5:** Harden observability pipelines and implement LLM-as-a-judge automated regression testing.
- **Expected AI Improvements:** A fully FOSS AI pipeline achieving baseline pedagogical scoring with zero external API calls, highly optimized for RTX 5070, and mathematically bounded hallucination rates.
