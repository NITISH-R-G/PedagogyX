# AI System Architecture Report (v3)

## AI Problem Analysis

**PedagogyX Context:** PedagogyX is an educational analytics tool utilizing Meta Ray-Ban smart glasses (via the Wearables Device Access Toolkit and an Android companion app) as the primary v1 capture client.

- **Use Case:** Automating the analysis of educational interactions, teaching methods, and classroom dynamics through multimodal capture (audio, visual, contextual) from wearable devices to provide actionable insights for educators.
- **Requirements:** Real-time and asynchronous processing of first-person viewpoint audio/video, high accuracy in speech-to-text (ASR) in noisy classroom environments, robust computer vision (CV) for identifying teaching aids and student engagement, and advanced natural language reasoning to synthesize educational metrics.
- **Constraints:** Battery and thermal limitations of Meta Ray-Bans, variable network connectivity via the Android companion app, strict privacy boundaries regarding student data (especially minors), and latency requirements for live feedback loop potential.
- **User Workflows:** Educators capture sessions seamlessly during teaching. The Android app streams/uploads data. The AI system processes ASR, applies CV, chunks context, and utilizes LLMs to generate a post-class pedagogical analysis dashboard.
- **Failure Scenarios:** Hallucinations in pedagogical critique, missed transcription due to background noise (students talking), misinterpretation of visual context (e.g., mistaking a presentation slide for a physical object), and failure to process prolonged sessions due to context length limits.

## AI System Architecture

- **Models:**
  - Vision/Multimodal: Proprietary models (e.g., GPT-4o or Claude 3.5 Sonnet) for complex pedagogical scene understanding, complemented by lighter edge/on-device CV models where possible.
  - ASR: Whisper v3 (or equivalent optimized models) for robust, noisy-environment transcription.
  - Reasoning/Text: Top-tier LLMs for orchestrating the final pedagogical analysis.
- **Orchestration:** LangChain/LlamaIndex or a custom robust DAG orchestrator built on FastAPI (e.g., `services/api`, `services/worker-cv`, `services/worker-asr`) to route audio/video streams, synchronize multimodal timestamps, and trigger reasoning chains.
- **Retrieval Systems:** Hybrid retrieval systems combining dense vector search and BM25 to surface relevant educational frameworks, past educator performance history, and best practices.
- **Memory Systems:** Session-scoped memory for intra-class context, and long-term educator-scoped memory stored in vector DBs to track pedagogical growth over time.
- **Infrastructure Topology:** The Android app offloads heavy capture data via a secure API gateway. Asynchronous workers (`worker-asr`, `worker-cv`) process raw media into structured metadata. A central `worker-metrics` service aggregates this and uses LLMs to compile the final analysis.

## Prompt & Reasoning Strategy

- **Prompt Structure:** Complex, structured prompts enforcing JSON outputs. Prompts are contextualized with established educational rubrics (e.g., Danielson Framework) to ensure grounded and standardized evaluations.
- **Grounding Strategy:** All LLM reasoning must cite specific timestamps from the captured audio/video transcripts. No pedagogical claims can be made without explicit multimodal evidence.
- **Hallucination Mitigation:** Implement a "Critic" agent pattern where a secondary prompt validates the primary analysis against the raw transcript. If the critic cannot find evidence in the transcript, the insight is discarded.
- **Context Management:** Hierarchical summarization. 5-minute chunks of class time are summarized independently, then a final pass aggregates these summaries into the overall session report, avoiding massive context bloat.

## RAG & Retrieval Design

- **Ingestion Pipeline:** Pedagogical standards, school curriculums, and past session reports are ingested, chunked by topic/standard, and embedded.
- **Embeddings:** High-dimensional dense embeddings optimized for semantic educational terminology (e.g., text-embedding-3-large).
- **Vector Database:** Scalable vector store (e.g., Pinecone or Milvus) integrated with the backend API to retrieve relevant teaching strategies.
- **Reranking:** Cross-encoder reranking applied to ensure the retrieved educational frameworks perfectly match the specific pedagogical scenario detected in the classroom.
- **Retrieval Workflows:** When an educator asks the PedagogyX dashboard for improvement tips, the system retrieves past low-engagement moments and maps them against proven strategies for that specific subject/age group.

## AI Infrastructure

- **Inference Systems:** Self-hosted vLLM or Triton Inference Server for open-weights models (ASR, CV) to minimize latency and cost. API-based routing for heavy reasoning LLMs.
- **GPU Infrastructure:** A mix of A100/H100 instances for heavy training/fine-tuning tasks and optimized L4/T4 instances for continuous, high-throughput asynchronous inference in `worker-cv` and `worker-asr`.
- **Scaling Strategy:** Kubernetes-based auto-scaling based on queue depth (e.g., Celery/RabbitMQ) since classroom recordings typically arrive in massive spikes (e.g., end of the school day).
- **Deployment Systems:** Containerized microservices (as seen in `infra/compose.dev.yaml`) deployed via CI/CD pipelines with model registry integration for seamless rollouts of updated ASR or CV weights.

## Evaluation Strategy

- **Benchmarks:** Custom PedagogyX benchmark dataset containing 1,000+ hours of annotated classroom interactions (synthetic/anonymized for v1).
- **Automated Evals:** LLM-as-a-judge pipelines comparing the generated pedagogical feedback against expert human (master teacher) evaluations.
- **Hallucination Tracking:** Automated scripts tracking the ratio of unsupported claims (insights without valid transcript citations) over time.
- **Quality Metrics:** ASR Word Error Rate (WER) in noisy environments, CV object detection mean Average Precision (mAP), and LLM feedback usefulness scores.

## Security & Safety

- **Prompt Injection Prevention:** Input sanitization and strict system prompt boundaries to prevent users from manipulating the pedagogical assessment engine.
- **Permission Controls:** Strict RBAC. Educators can only access their own sessions; administrators get aggregated, anonymized metrics.
- **Sandboxing:** Code execution and tool-calling by LLMs (if implemented for data analysis) must occur in isolated, ephemeral Docker containers.
- **Output Validation:** PII redaction (especially student names/faces) at the edge or immediately upon ingestion before any LLM processing occurs.

## Observability

- **Tracing:** LangSmith or Arize AI integration for full LLM call tracing, allowing engineers to visualize exactly which prompt or retrieval step failed.
- **Monitoring:** Grafana dashboards tracking GPU utilization, queue latency in asynchronous workers, and API response times.
- **Analytics:** Tracking which pedagogical insights educators click on or implement, providing a feedback loop to improve the system's value.
- **Diagnostics:** Comprehensive logging with unique session trace IDs spanning from the Android app, through the API, to the asynchronous workers.

## Performance Optimization

- **Latency Optimization:** Streaming ASR responses back to the app for immediate processing, rather than waiting for the entire recording to finish.
- **Token Optimization:** Aggressive prompt compression and utilizing structured schema to minimize output tokens.
- **Inference Efficiency:** Int8/FP8 quantization for on-premise models, reducing VRAM requirements and increasing throughput.
- **Caching Strategy:** Semantic caching (e.g., Redis) for identical retrieval queries (e.g., standard curriculum lookups) to avoid redundant LLM calls.

## Risks & Tradeoffs

- **Hallucination Risks:** Providing an educator with false or hyper-critical feedback could damage their confidence and trust in PedagogyX. This necessitates the heavy reliance on the evidence-based "Critic" pattern, at the cost of double inference expenses.
- **Scalability Concerns:** Processing HD video from Meta Ray-Bans is incredibly bandwidth and compute-intensive. Tradeoff: Downsampling video or reducing frame rates significantly before cloud ingestion.
- **Infrastructure Tradeoffs:** Using managed LLM APIs (OpenAI/Anthropic) vs. self-hosting. Managed APIs offer better reasoning but introduce privacy risks and unpredictable latency. The current architecture balances this by keeping ASR/CV open-weights and isolated, and strictly controlling data sent to reasoning LLMs.
- **Operational Limitations:** Wearables battery life limits recording lengths. AI systems must be resilient to abrupt disconnections or corrupted files.

## Agile Sprint Plan

- **Milestone 1 (Sprint 1-2):** Establish the secure ingestion pipeline from the Android app to the API. Deploy foundational `worker-asr` with Whisper v3.
- **Milestone 2 (Sprint 3-4):** Integrate multimodal LLM orchestration. Implement the Critic agent pattern and prompt structure for basic pedagogical feedback.
- **Milestone 3 (Sprint 5-6):** Build the RAG system for educational frameworks. Connect vector DB and finalize the `worker-metrics` synthesis service.
- **Milestone 4 (Sprint 7-8):** Security audits (PII redaction validation), rigorous benchmarking against human expert datasets, and performance optimization (quantization).
- **Implementation Phases:** Architecture -> Ingestion -> Perception (ASR/CV) -> Reasoning (LLM) -> Presentation (Web).
- **Evaluation Checkpoints:** End-of-sprint WER evaluation, LLM-as-a-judge correlation tests, and system load tests.
- **Expected AI Improvements:** 30% reduction in ungrounded claims via Critic pattern, 40% reduction in processing latency through downsampling and batching optimization.
