# AI System Architecture Report

## AI Problem Analysis

- **Use case:** PedagogyX captures classroom sessions via Meta Ray-Ban DAT (v1 primary client) to transcribe and analyze pedagogical insights for educational improvement.
- **Requirements:** High accuracy in Automatic Speech Recognition (ASR) in noisy classroom environments, robust computer vision (CV) for non-verbal cues, strict compliance with India DPDP (data residency in ap-south-1), and operation restricted to synthetic data until G2 legal sign-off.
- **Constraints:** Must operate without real production school data initially. AI components must be highly scalable and localized to India regions to ensure data privacy. High latency from edge devices (Meta Ray-Ban DAT) must be minimized.
- **User workflows:** Instructors wear Ray-Ban DAT glasses to record sessions. Audio and video are streamed/uploaded to the PedagogyX platform, where AI models extract transcripts, analyze pedagogy metrics (e.g., student engagement, teacher talking time), and generate actionable feedback dashboards.
- **Failure scenarios:** High ambient noise corrupting ASR transcripts, occlusion blocking CV analysis, network drops during streaming from wearable DAT, hallucinations in LLM-generated pedagogical feedback, or accidental ingestion of real PII prior to G2 clearance.

## AI System Architecture

- **Models:** Whisper (or equivalent) for ASR tuned for classroom acoustics, Llama-3/Mistral via localized inference for pedagogical analysis and summarization, and optimized CV models (e.g., YOLO/ViT) for engagement metrics.
- **Orchestration:** FastAPI-based backend APIs managing asynchronous worker queues (`worker-asr`, `worker-cv`, `worker-metrics`). LangChain or LlamaIndex for LLM orchestration and RAG workflows.
- **Retrieval systems:** Qdrant or Milvus deployed in ap-south-1 for semantic search over pedagogical guidelines, curriculum standards, and past session summaries.
- **Memory systems:** Redis for short-term session state caching and contextual memory during long-running pedagogical analyses.
- **Infrastructure topology:** AWS/GCP ap-south-1 region. EKS/GKE for container orchestration, GPU-accelerated nodes (e.g., RTX 5070 / L4) for model inference, and localized object storage (MinIO/S3) for media assets.

## Prompt & Reasoning Strategy

- **Prompt structure:** Structured system prompts enforcing pedagogical frameworks (e.g., Bloom's Taxonomy, CLASS). Explicit instructions to anchor analysis strictly in the provided transcript and visual metrics.
- **Grounding strategy:** Inject relevant educational standards and validated pedagogical theories via RAG. Force LLMs to cite transcript timestamps when suggesting improvements.
- **Hallucination mitigation:** Multi-step reasoning (Chain-of-Thought) for feedback generation, with an independent LLM evaluation pass to verify claims against the source transcript. Strict temperature settings (T=0.1) for analytical tasks.
- **Context management:** Chunking long 45-minute classroom transcripts into thematic segments. Summarize rolling context to maintain LLM memory without exceeding context window limits.

## RAG & Retrieval Design

- **Ingestion pipeline:** Parse educational standards, research papers, and anonymized baseline session data. Chunk text hierarchically (e.g., by topic or grade level) and extract metadata (domain, subject).
- **Embeddings:** Domain-adapted embedding models optimized for educational and pedagogical terminology.
- **Vector database:** Highly available vector database (Qdrant) running in ap-south-1, partitioned by school district or organization to enforce strict multi-tenant isolation.
- **Reranking:** Cross-encoder reranking to ensure top retrieved pedagogical strategies highly match the specific classroom scenario (e.g., "managing disruptive behavior in middle school math").
- **Retrieval workflows:** Hybrid search combining semantic similarity (embeddings) with keyword filtering (e.g., filtering by subject and grade level).

## AI Infrastructure

- **Inference systems:** vLLM or TensorRT-LLM for serving Llama models with high throughput. Optimized ONNX/TensorRT runtimes for CV and ASR workers.
- **GPU infrastructure:** Cost-effective edge-to-cloud GPU allocation. Initial dev scaling on CPU/RTX 5070, moving to localized cloud GPUs (A10G/L4) for production scale.
- **Scaling strategy:** Kubernetes Horizontal Pod Autoscaler (HPA) based on custom queue depth metrics (e.g., number of pending ASR tasks). Scale-to-zero for non-school hours.
- **Deployment systems:** GitOps via ArgoCD or Flux. Automated CI/CD pipelines deploying immutable container images to ap-south-1 clusters.

## Evaluation Strategy

- **Benchmarks:** Custom benchmark suite (`benchmarks/bench_full_pipeline.sh`) evaluating ASR Word Error Rate (WER) on noisy synthetic classroom audio, and LLM adherence to pedagogical rubrics.
- **Automated evals:** LLM-as-a-judge pipelines validating the helpfulness, tone, and accuracy of generated feedback against human-annotated gold standards.
- **Hallucination tracking:** Automated factual consistency checks between generated summaries and source transcripts.
- **Quality metrics:** Precision/Recall for CV engagement detection, RAG retrieval accuracy (MRR, NDCG), and user acceptance rate of AI suggestions.

## Security & Safety

- **Prompt injection prevention:** Input sanitization and pre-flight LLM checks to detect adversarial inputs from potentially malformed or malicious transcripts.
- **Permission controls:** Strict RBAC enforcing that only authorized educators can view session analysis. Multi-tenant data segregation at the database level.
- **Sandboxing:** Executing third-party integrations or code-generation (if any) in isolated, ephemeral gVisor/Firecracker microVMs.
- **Output validation:** Rule-based heuristics and secondary safety models filtering inappropriate, biased, or overly critical feedback before presenting it to the teacher.

## Observability

- **Tracing:** OpenTelemetry instrumentation across API, ASR, CV, and Metrics workers to visualize the end-to-end latency of session processing.
- **Monitoring:** Prometheus/Grafana dashboards tracking GPU utilization, queue depths, ASR real-time factors (RTF), and API error rates.
- **Analytics:** PostHog or custom dashboards tracking which pedagogical insights are most frequently viewed and acted upon by educators.
- **Diagnostics:** Centralized logging (ELK/Loki) with correlation IDs tying video chunks, ASR transcripts, and LLM inferences to specific Ray-Ban DAT sessions.

## Performance Optimization

- **Latency optimization:** Streaming ASR transcripts via WebSockets back to the client. Overlapping ASR, CV, and LLM processing via asynchronous task DAGs.
- **Token optimization:** Prompt compression and strict output schemas (JSON mode) to minimize redundant token generation during LLM inference.
- **Inference efficiency:** Model quantization (INT8/FP8) for LLMs and Whisper models to maximize throughput on limited GPU budgets.
- **Caching strategy:** Semantic caching (Redis) for repeated RAG queries (e.g., standard curriculum lookups) to bypass redundant vector search and LLM synthesis.

## Risks & Tradeoffs

- **Hallucination risks:** Risk of LLMs generating inaccurate pedagogical feedback, which could demoralize educators. Mitigated by strict grounding and human-in-the-loop review.
- **Scalability concerns:** Handling peak loads at the end of the school day when thousands of sessions are uploaded simultaneously. Tradeoff: higher queue latency during peak vs. overprovisioning idle GPUs.
- **Infrastructure tradeoffs:** Strict data residency (ap-south-1) limits access to the absolute latest GPU hardware sometimes available only in us-east-1.
- **Operational limitations:** Operating purely on synthetic data until G2 restricts the ability to fine-tune models on real-world edge cases (e.g., unique classroom acoustics or regional accents).

## Agile Sprint Plan

- **Milestones:**
  1. MVP Local Backend & Synthetic Worker Pipeline (Completed G0).
  2. Implement RAG Evaluation and E2E Pipeline Benchmarking (Sprint 03).
  3. Deploy scalable ap-south-1 infrastructure.
  4. G2 legal clearance and real data ingestion.
- **Implementation phases:** Current phase focuses on boilerplate maturity, ASR/CV stub replacement with real models, and robust prompt engineering on synthetic data.
- **Evaluation checkpoints:** Weekly review of `bench_full_pipeline` metrics (WER, Latency). Post-G2 model drift analysis.
- **Expected AI improvements:** 30% reduction in ASR latency via TensorRT optimization. 50% improvement in feedback accuracy via localized RAG curriculum integration.
