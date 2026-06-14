# AI System Architecture Report v3

## AI Problem Analysis

The PedagogyX system operates as a multimodal AI classroom intelligence and teacher optimization platform under extreme constraints. The problem space necessitates capturing rich audio and visual data streams from low-end, edge-based client devices—primarily Meta Ray-Ban (DAT) smart glasses and constrained Android/Windows devices.

Key constraints include a mandate for a 100% Free and Open Source Software (FOSS) stack, offline execution to comply with India's strict data residency and privacy regulations (DPDP 2023), and the compute limitations of consumer-grade RTX 5070 (12GB VRAM) hardware.

The architecture must support two distinct operational workflows:

1. **Hot Path (Real-time):** Delivering immediate, low-latency heuristics for activity detection (via lightweight YOLO variants) and basic audio telemetry without stalling on GPU VRAM bounds.
2. **Cold Path (Batch):** Authoritative, high-precision pedagogical scoring, multi-stream A/V diarization and alignment, rigorous ASR transcription, and deep LLM reasoning.

**Failure Scenarios include:** Complete A/V desynchronization from poor edge network conditions, inference latency collapse causing queue saturation, hallucinated teacher coaching outputs from under-parameterized (7B) local LLMs, and prompt injection attacks masquerading as classroom dialogue.

## AI System Architecture

PedagogyX employs a decentralized edge-ingest, centralized FOSS-inference distributed architecture.

- **Models:**
  - _Audio Intelligence:_ Quantized `faster-whisper` optimized for constrained RTX 5070 execution, supporting high-throughput ASR.
  - _Vision Intelligence:_ Edge-optimized YOLO models for immediate heuristic engagement metrics; transformer-based CV for intensive batch multi-frame fusion and spatial analysis.
  - _LLM Reasoning:_ Locally deployed, heavily quantized (INT4/INT8) open-weight LLMs (e.g., Llama 3 / Qwen variants) orchestrating pedagogy scoring and actionable feedback generation.
- **Orchestration:** Directed Acyclic Graph (DAG) pipelines driven by discrete, horizontally scalable Python workers (e.g., `worker-asr`, `worker-cv`, `worker-metrics`). Redis manages the transient hot queues, while Postgres handles durable workflow state.
- **Retrieval Systems:** A pgvector-backed Postgres instance serving as the unified semantic vector store, indexing pedagogical rubrics, institutional policies, and historical coaching context.
- **Memory Systems:** Short-term cache (Redis) for Hot Path metrics and diarization tracking; durable, ACID-compliant long-term memory in Postgres.
- **Infrastructure Topology:** A Hub-and-Spoke model where Edge nodes (local school LAN ingest points) securely buffer and transmit streams to a centralized FOSS backend in an India-based bare-metal/IaaS data center. Ingestion routing is handled via API Gateways and MediaMTX.

## Prompt & Reasoning Strategy

Given the constraints of running 7B-8B parameter models locally, prompt engineering must be exceptionally rigorous to prevent reasoning collapse and hallucinations.

- **Prompt Structure:** Utilize strict, instruction-tuned few-shot templates. Each prompt explicitly binds the model to defined pedagogical templates (K-12 vs. University) and enforces step-by-step reasoning (Chain-of-Thought) before generating a final score.
- **Grounding Strategy:** All generated feedback must be deterministically grounded. LLM assertions must contain cryptographic-style citations back to specific transcript timestamps or detected CV event bounds. No sentiment or intent can be assumed unless explicitly observed in the multimodal data.
- **Hallucination Mitigation:** Implement a secondary "Validator" LLM loop. The proposed coaching tip is routed back through a lightweight verification prompt against the retrieved ground-truth rubrics and diarization confidence scores. If the validation fails, the output defaults to "Human Review Required."
- **Context Management:** RTX 5070 VRAM limits necessitate aggressive chunking. Long 45-minute sessions are processed via a Map-Reduce summarization hierarchy, ensuring the final evaluative context window does not exceed the model's effective limits.

## RAG & Retrieval Design

To ensure coaching feedback aligns with specific institutional policies and pedagogical science, the system relies on a robust RAG architecture.

- **Ingestion Pipeline:** School guidelines, pedagogical best practices, and anonymized baseline templates are periodically chunked, embedded, and indexed.
- **Embeddings:** Utilizing highly efficient, locally hosted `sentence-transformers` models optimized for semantic clustering of educational texts.
- **Vector Database:** PostgreSQL augmented with the `pgvector` extension provides unified, transactionally safe storage for both application state and dense vectors, strictly adhering to the FOSS mandate.
- **Reranking:** Critical high-stakes policy queries pass through a local cross-encoder reranker to maximize retrieval precision before being injected into the LLM context.
- **Retrieval Workflows:** A hybrid search implementation combining exact-match keyword filtering (for specific classroom events or subject matter) with dense semantic search (for abstract pedagogical concepts).

## AI Infrastructure

PedagogyX's infrastructure strictly avoids managed proprietary APIs in favor of a resilient self-hosted environment.

- **Inference Systems:** Containerized model servers leveraging optimization frameworks like vLLM, TensorRT, and ONNX Runtime to maximize throughput on consumer silicon.
- **GPU Infrastructure:** A compute tier entirely composed of RTX 5070 clusters, managing both lightweight Hot Path heuristics and heavy Cold Path batch inference through strict VRAM partitioning.
- **Scaling Strategy:** Queue-based horizontal scaling. Hot Path workers dynamically scale against active stream ingestion rates; Cold Path jobs are scheduled via a durable batch scheduler to maximize overnight GPU utilization.
- **Deployment Systems:** Development and Phase 0/MVP environments utilize standard `docker compose`, with a planned trajectory toward lightweight Kubernetes (K3s) for robust multi-node orchestration as the system matures.

## Evaluation Strategy

AI quality cannot be assumed; it must be continuously and rigorously measured against objective baselines.

- **Benchmarks:** Implement continuous regression testing evaluating ASR Word Error Rate (WER) against noisy, real-world Indian classroom audio datasets, and precision/recall metrics for CV engagement models.
- **Automated Evals:** A deterministic CI/CD pipeline simulating end-to-end synthetic sessions via `pytest`, ensuring pipeline integrity from MediaMTX ingestion to final pedagogical scoring.
- **Hallucination Tracking:** Utilizing automated rubrics (LLM-as-a-Judge) to score the generated coaching tips for faithfulness to the transcript and the absence of unsupported inferences.
- **Quality Metrics:** Track p50/p95 inference latency, VRAM utilization, token generation efficiency (tokens/sec), WER, and aggregate user satisfaction derived from dashboard telemetry.

## Security & Safety

Protecting sensitive minor data and maintaining model integrity are paramount.

- **Prompt Injection Prevention:** Implement rigid input sanitization and abstraction layers. Untrusted audio transcripts are isolated from system prompts using strict delimiters and data-only formatting.
- **Permission Controls:** Enforce rigorous Role-Based Access Control (RBAC). Raw A/V data is highly restricted (Admin/Compliance only), while teachers only interact with abstract pedagogical scores and anonymized feedback.
- **Sandboxing:** All worker nodes and inference processes execute in isolated, non-privileged, read-only Docker containers with strictly defined network egress policies.
- **Output Validation:** Force LLMs to generate responses conforming to strict JSON Schemas. Outputs failing schema validation are automatically rejected and routed to a Dead Letter Queue (DLQ) for manual review.

## Observability

In a FOSS-first offline environment, deep observability is the only mechanism to debug complex multimodal failures.

- **Tracing:** Implement OpenTelemetry to provide distributed traces connecting edge ingestion events (Ray-Ban streams) through to the final Postgres data insertions, bridging the gap between Node.js/FastAPI gateways and Python workers.
- **Monitoring:** Deploy a comprehensive Prometheus/Grafana stack to visualize queue depths, RTX 5070 VRAM pressure, GPU utilization, and end-to-end API latency.
- **Analytics:** Monitor the operational ratio between immediate Hot Path heuristic resolutions and Cold Path authoritative overrides to evaluate system efficiency.
- **Diagnostics:** Maintain robust Dead Letter Queues (DLQ) capturing full stack traces, input payloads, and model state for all worker failures to enable rapid debugging.

## Performance Optimization

Maximizing the utility of constrained RTX 5070 hardware requires relentless optimization.

- **Latency Optimization:** Implement streaming ASR at the edge where feasible, and utilize micro-batching (e.g., 2-second windows) for Hot Path heuristics to provide immediate UI feedback.
- **Token Optimization:** Aggressively summarize and truncate context before passing it to the reasoning LLM to minimize compute overhead and prevent KV cache exhaustion.
- **Inference Efficiency:** Utilize aggressive integer quantization (INT4/INT8) and continuous batching (via vLLM) to squeeze maximum throughput out of the 12GB VRAM limit.
- **Caching Strategy:** Employ Redis to cache recurrent retrieval embeddings, intermediate Hot Path results, and overlapping session contexts to avoid redundant compute.

## Risks & Tradeoffs

- **Hallucination Risks:** Relying on small (7B-8B), locally quantized LLMs significantly increases the risk of subtle hallucinations compared to proprietary foundation models. This trade-off requires heavy investment in the Validator loop and strict schema enforcement.
- **Scalability Concerns:** The physical constraint of offline, self-hosted RTX 5070 clusters imposes a rigid ceiling on concurrent processing. Extreme load spikes will inherently delay Cold Path authoritative scoring.
- **Infrastructure Tradeoffs:** Adhering strictly to a FOSS-first, self-hosted architecture introduces immense operational and maintenance overhead, requiring dedicated expertise to manage CUDA/GPU driver compatibility and cluster orchestration.
- **Operational Limitations:** Managing complex A/V synchronization across diverse, low-end edge hardware over unstable networks remains a critical challenge, likely necessitating sophisticated, software-based timecode alignment.

## Agile Sprint Plan

- **Sprint 1 (Core Infrastructure & MVP ASR):** Provision local RTX 5070 worker environments. Deploy `faster-whisper` and establish the foundational `worker-asr` ingestion queue.
- **Sprint 2 (Hot Path & Edge Ingest):** Finalize Meta Ray-Ban DAT integration. Implement the Edge LAN buffer and lightweight YOLO-based Hot Path heuristics for real-time engagement metrics.
- **Sprint 3 (Cold Path & Reasoning):** Implement the multi-stream batch alignment pipeline. Deploy and fine-tune quantized LLM reasoning prompts for pedagogical scoring. Integrate pgvector for policy retrieval.
- **Sprint 4 (Hardening & Observability):** Deploy the OpenTelemetry/Grafana observability stack. Establish the automated evaluation pipeline for continuous tracking of hallucinations, WER, and latency.
- **Sprint 5 (Pilot & Refinement):** Execute Phase 0 pilot in controlled environments. Monitor model drift and refine context management based on real-world classroom acoustics and edge case failures.
