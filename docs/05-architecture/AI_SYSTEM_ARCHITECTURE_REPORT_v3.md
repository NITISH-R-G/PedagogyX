# AI System Architecture Report v3

## AI Problem Analysis

The objective is to build a reliable, accurate, and scalable multimodal AI classroom intelligence and teacher optimization platform (PedagogyX). Current operations (Phase 0 / MVP) are constrained by India data residency and privacy regulations (G2 legal sign-off pending), mandating a strict FOSS-first software stack with centralized offline inference. Only synthetic test sessions are permitted currently. The primary v1 capture client is Meta Ray-Ban via `clients/android-capture-dat`. User workflows require splitting AI processing into two distinct tiers: a real-time Hot Path for immediate heuristic feedback and a batch Cold Path for deep, authoritative pedagogical analysis. Failure scenarios include A/V synchronization drift, latency degradation under concurrent Cold Path loads, prompt hallucinations generating false feedback, and data leakage across multi-tenant boundaries.

## AI System Architecture

The AI stack relies exclusively on a central OSS offline inference backend to guarantee data sovereignty.

- **Models:** Open-source Whisper variants (e.g., `faster-whisper`) for ASR, YOLO models for real-time engagement and object detection, and quantized LLMs (via Ollama) for text generation and reasoning.
- **Orchestration:** Directed Acyclic Graph (DAG) pipelines driven by asynchronous worker queues (`worker-asr`, `worker-cv`, `worker-metrics`), orchestrating complex data flows between audio, video, and text streams.
- **Retrieval Systems:** A vector database (Postgres + `pgvector`) architecture for indexing educational standards, curricula, and previous feedback templates.
- **Memory Systems:** Redis handles short-term context and caching for Hot Path operations; Postgres manages long-term persistence and session metadata.
- **Infrastructure Topology:** Centralized inference cluster equipped with RTX GPUs, fronted by an API Gateway routing Meta Ray-Ban capture streams to appropriate ingestion queues.

## Prompt & Reasoning Strategy

Prompts are designed to maximize reliability, contextual accuracy, and reasoning quality for pedagogical analysis.

- **Prompt Structure:** Utilize structured, few-shot prompts defining strict evaluation rubrics (e.g., K-12 pedagogical standards).
- **Grounding Strategy:** All generated feedback must trace directly to specific timeline events (ASR timestamps or CV bounding box detections).
- **Hallucination Mitigation:** Implement a secondary verification LLM pass to cross-check primary model outputs against grounded RAG contexts, filtering out unsupported assertions.
- **Context Management:** Token-limited, hierarchical chunking of classroom transcripts and event logs ensures the context window prioritizes the most relevant pedagogical moments.

## RAG & Retrieval Design

RAG anchors the system's pedagogical feedback in verifiable domain knowledge.

- **Ingestion Pipeline:** Automated ingestion of pedagogical guidelines, syllabi, and best practices into chunked representations.
- **Embeddings:** Lightweight, offline sentence-transformer models generate dense vector embeddings.
- **Vector Database:** Postgres (`pgvector`) ensures unified, transactional storage of both relational metadata and dense vectors.
- **Reranking:** Cross-encoder reranking algorithms evaluate the top-k retrieved documents to ensure maximum relevance during high-stakes batch Cold Path scoring.
- **Retrieval Workflows:** Hybrid search mechanisms (semantic similarity + keyword filtering) adapt dynamically based on the subject matter and user queries.

## AI Infrastructure

Infrastructure is optimized for inference efficiency, scalability, and operational reliability within an offline environment.

- **Inference Systems:** Containerized AI model serving (via Ollama, custom TorchServe endpoints) leveraging TensorRT and ONNX optimizations.
- **GPU Infrastructure:** Utilizing clustered RTX GPUs optimized for parallel batch processing and concurrent stream decoding.
- **Scaling Strategy:** Queue-based, horizontal autoscaling of `worker-asr` and `worker-cv` containers dynamically adjusts based on session load and hardware constraints.
- **Deployment Systems:** Docker Compose manages local development and MVP deployments (`infra/compose.dev.yaml`), mapping to containerized production deployments.

## Evaluation Strategy

A rigorous, automation-first evaluation framework prevents model regression and measures system quality.

- **Benchmarks:** Automated evaluation of ASR Word Error Rate (WER) against noisy synthetic classroom audio, and CV precision/recall against synthetic engagement datasets.
- **Automated Evals:** End-to-end `pytest` suites continuously validate prompt reliability and tool-calling accuracy.
- **Hallucination Tracking:** Automated rubrics compute a "faithfulness score," quantifying instances where the LLM deviates from grounded context.
- **Quality Metrics:** Track p50/p95 latency, GPU utilization, token throughput, context precision, and end-user satisfaction indices.

## Security & Safety

Ensuring absolute privacy, explainability, and enterprise-grade security over all AI workloads.

- **Prompt Injection Prevention:** Input sanitization layers strictly isolate potentially adversarial classroom transcripts from critical system prompts.
- **Permission Controls:** Strict Role-Based Access Control (RBAC) ensures raw synthetic data and pedagogical metrics are isolated by user and role.
- **Sandboxing:** AI inference workers execute within isolated, network-restricted containers with read-only filesystems.
- **Output Validation:** Pydantic models enforce rigid JSON schema validation; malformed LLM outputs trigger immediate fallback/retry logic rather than failing silently.

## Observability

Comprehensive observability ensures rapid debugging and operational transparency.

- **Tracing:** Distributed tracing across the Hot Path and Cold Path maps the journey from Meta Ray-Ban ingestion to final pedagogical scoring.
- **Monitoring:** Grafana dashboards visualize GPU VRAM consumption, queue depths, API latency, and model inference times.
- **Analytics:** Continuous analysis of token consumption, prompt analytics, and the frequency of Hot Path vs. Cold Path invocations.
- **Diagnostics:** Dead-Letter Queues (DLQs) capture failed AI tasks, preserving inputs and tracebacks for subsequent offline analysis.

## Performance Optimization

Continuous optimization maximizes GPU throughput and minimizes latency within hardware constraints.

- **Latency Optimization:** Implement real-time streaming architectures (YOLO heuristics) for the Hot Path to ensure immediate edge feedback.
- **Token Optimization:** Dynamic context compression and aggressive summarization reduce token payloads before reaching the intensive LLM Cold Path.
- **Inference Efficiency:** Adopt INT4/INT8 quantization strategies for LLMs to dramatically reduce VRAM requirements without significantly degrading reasoning quality.
- **Caching Strategy:** Redis caches identical retrieval queries, intermediate embedding vectors, and recurring pedagogical templates to bypass redundant computation.

## Risks & Tradeoffs

- **Hallucination Risks:** Reliance on quantized, local models increases the likelihood of subtle reasoning errors compared to frontier cloud models, demanding robust verification.
- **Scalability Concerns:** Purely offline, GPU-constrained inference limits vertical scaling; high concurrency necessitates queue queuing which may degrade Cold Path turnaround times.
- **Infrastructure Tradeoffs:** FOSS-first requirements necessitate higher maintenance overhead and complex MLOps tooling compared to managed cloud AI services.
- **Operational Limitations:** Handling extreme A/V sync drift from diverse Meta Ray-Ban clients poses significant challenges for multimodal alignment algorithms.

## Agile Sprint Plan

- **Milestone 1:** Deploy baseline offline inference stack (faster-whisper, YOLO, Ollama) and configure initial ingestion queues for synthetic Meta Ray-Ban data.
- **Milestone 2:** Implement Hot Path processing with real-time heuristic feedback caching and observability tracking.
- **Milestone 3:** Finalize RAG implementation with `pgvector` and integrate the batch Cold Path for authoritative pedagogical scoring.
- **Milestone 4:** Launch automated evaluation pipelines for WER, CV precision, and hallucination tracking.
- **Expected Improvements:** Achieve a stable, fully offline Phase 0 MVP capable of accurately processing synthetic classroom sessions with measurable quality improvements.
