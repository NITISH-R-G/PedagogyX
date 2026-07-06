# AI System Architecture Report v3

## AI Problem Analysis

The objective is to build PedagogyX, an elite multimodal AI classroom intelligence and teacher optimization platform. The constraints include an India-focused deployment requiring strict offline/FOSS inference for data residency compliance and operating on low-end client captures (Meta Ray-Ban smart glasses, basic Android/Windows devices).
The system processes noisy classroom audio and video, characterized by Hindi-English code-switching and dynamic visual environments.
Key failure scenarios involve heavy hallucinations in pedagogical feedback, severe latency under load, prompt injections from untrusted audio inputs, and synchronization loss in multi-modal streams.

## AI System Architecture

The AI stack handles multimodal ingestion and relies exclusively on self-hosted FOSS models.

- Models: `faster-whisper large-v3` for robust Hindi-English code-switching ASR; lightweight YOLO and vision transformers for engagement metrics; quantized Llama 3 / Mistral variants for pedagogical analysis.
- Orchestration: Asynchronous event-driven architecture utilizing Redis Streams/Celery for the Cold Path AI inference pipeline to manage long-running video alignment, transcription, and scoring tasks.
- Retrieval Systems: A pgvector-powered semantic retrieval system linking transcript segments to pedagogical best practices.
- Memory Systems: Redis for short-term caching of hot-path heuristic data, and PostgreSQL for long-term durable storage of classroom sessions.
- Infrastructure Topology: Containerized microservices deployed on centralized Indian datacenters equipped with RTX 5070 GPUs. The setup bridges real-time stream ingestion and batch AI processing.

## Prompt & Reasoning Strategy

A highly constrained and deterministic interaction model with LLMs ensures the pedagogical value remains high.

- Prompt Structure: Chain-of-Thought (CoT) prompting focused on evidence-based pedagogical rubrics, leveraging few-shot examples for K-12 and university settings.
- Grounding Strategy: Every AI assertion must be grounded in specific timestamps from the ASR transcript or CV event timeline. Unsubstantiated claims are programmatically rejected.
- Hallucination Mitigation: Multi-step validation chains where a secondary "critic" model assesses the initial output against the source transcripts before finalizing the pedagogical report.
- Context Management: Long audio transcripts are chunked with overlap and processed hierarchically to maintain global classroom context without exceeding token limits.

## RAG & Retrieval Design

To contextualize feedback, the platform embeds curriculum standards and teaching frameworks.

- Ingestion Pipeline: Automated chunking and embedding of institutional guidelines, syllabi, and historical highly-rated pedagogical responses.
- Embeddings: Lightweight multilingual sentence transformers (e.g., `BGE-m3`) optimized for CPU/GPU efficiency.
- Vector Database: PostgreSQL augmented with the `pgvector` extension for unified storage of relational data and embeddings.
- Reranking: Cross-encoder reranking models apply high-precision filtering to the top-k retrieved documents to ensure relevance.
- Retrieval Workflows: Hybrid search combining exact keyword matching (for specific terms or syllabus topics) with semantic similarity.

## AI Infrastructure

Designed for high throughput and reliability on constrained edge/FOSS environments.

- Inference Systems: Dedicated model serving engines like vLLM for LLMs and TensorRT-optimized servers for vision and ASR models.
- GPU Infrastructure: Clusters of RTX 5070 GPUs maximizing memory bandwidth and compute for INT8/INT4 quantized workloads.
- Scaling Strategy: Queue-based autoscaling of Celery/Redis Stream workers based on backlog depth, ensuring predictable cold-path processing times.
- Deployment Systems: Docker Compose and Kubernetes configurations optimized for air-gapped or restricted Indian datacenter deployments.

## Evaluation Strategy

Continuous, rigorous evaluation prevents regressions in model quality and reliability.

- Benchmarks: Custom benchmark datasets reflecting noisy Indian classroom environments to measure Word Error Rate (WER) and CV precision/recall.
- Automated Evals: CI/CD pipelines executing LLM-as-a-judge rubrics to score generation quality, tone, and contextual accuracy on synthetic sessions.
- Hallucination Tracking: Automated metrics flagging occurrences where generated insights lack exact matching timestamp evidence.
- Quality Metrics: p50 and p95 inference latency, GPU utilization, context precision/recall, and end-user teacher acceptance rates.

## Security & Safety

Ensuring absolute data privacy and model robustness.

- Prompt Injection Prevention: Strict input sanitization of ASR outputs before they are passed as context to the LLM.
- Permission Controls: RBAC implemented at the API gateway layer to prevent unauthorized access to sensitive raw video/audio data.
- Sandboxing: AI inference workers run in isolated, read-only Docker containers without outbound internet access.
- Output Validation: Enforced structured JSON generation (e.g., via Outlines/Guidance) to guarantee API compatibility and prevent safety boundary violations.

## Observability

Comprehensive visibility into AI operations and model health.

- Tracing: Distributed tracing via OpenTelemetry to track requests from Ray-Ban client ingestion through the async Celery pipelines to final LLM generation.
- Monitoring: Grafana dashboards tracking Redis queue depth, Celery task failure rates, GPU VRAM usage, and API latencies.
- Analytics: Tracking token consumption, average audio length processed, and model fallback rates.
- Diagnostics: Detailed DLQ (Dead Letter Queue) logging for failed AI inference jobs to enable rapid debugging.

## Performance Optimization

Maximizing hardware efficiency to lower operational costs.

- Latency Optimization: Pipelining ASR, CV, and LLM tasks to execute concurrently where data dependencies allow.
- Token Optimization: Smart truncation and dynamic summarization of redundant transcript segments (e.g., prolonged silence or repetitive ambient noise).
- Inference Efficiency: Deploying `faster-whisper large-v3` with optimized precision and utilizing KV-cache optimization in vLLM for language models.
- Caching Strategy: Caching frequent embedding requests and pedagogical rubric structures in Redis to bypass redundant model executions.

## Risks & Tradeoffs

- Hallucination Risks: Using heavily quantized smaller open-weight models increases the probability of nuanced reasoning errors compared to API-based frontier models.
- Scalability Concerns: Scaling async GPU workers is constrained by physical hardware availability in local data centers, potentially leading to queue buildup during peak school hours.
- Infrastructure Tradeoffs: Maintaining custom model serving infrastructure requires significant DevOps overhead compared to fully managed cloud AI services.
- Operational Limitations: Handling real-time multi-speaker diarization in noisy environments remains a persistent challenge with current FOSS tools.

## Agile Sprint Plan

- Milestone 1: Finalize integration of `faster-whisper large-v3` in the `worker-asr` service and establish Redis Streams orchestration.
- Milestone 2: Deploy and benchmark quantized Llama 3 / Mistral serving via vLLM on the RTX 5070 infrastructure.
- Milestone 3: Implement the `pgvector` RAG pipeline with curriculum ingestion and hybrid search capabilities.
- Milestone 4: Construct the fully async Cold Path pipeline uniting ASR, CV, and LLM rubrics, validated against the automated evaluation suite.
