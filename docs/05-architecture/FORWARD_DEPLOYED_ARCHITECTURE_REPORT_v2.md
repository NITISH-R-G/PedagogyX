# Forward Deployed Architecture Report v2

## Operational Problem Analysis

The core mission of PedagogyX is to rapidly deploy multimodal AI classroom intelligence to optimize teacher performance across Indian schools.

- **Business Context:** Operating under strict budgetary constraints, the platform targets a ₹0 edge hardware cost by leveraging OSS-first, self-hosted AI models rather than expensive proprietary APIs. Compliance with Indian data residency laws (DPDP) and an impending G2 legal sign-off dictate stringent data handling.
- **Workflow Analysis:** Teachers run 45-50 minute sessions requiring frictionless, hands-free capture. Administrators and coaches need to review actionable pedagogy metrics (e.g., talk ratio, interaction density) via web dashboards without extended delays.
- **Bottlenecks:** The primary bottlenecks are the unreliable nature of school WAN connections, high compute costs at the edge, and the strict 12GB VRAM constraint on central RTX 5070 GPU servers hosting the AI models.
- **Operational Constraints:** The pivot to Meta Ray-Ban smart glasses (ADR-0009) as the primary v1 client introduces new constraints on capture via the Wearables DAT SDK over Bluetooth, requiring a companion Android app to manage the data lifecycle.

## System Architecture

The architecture relies on a Hybrid Edge-Cloud model, separating lightweight edge capture from heavy centralized inference.

- **Major Components:**
  - **Capture Layer:** Meta Ray-Ban smart glasses connected to an Android companion app via the Wearables DAT SDK. Fallback/legacy support for Windows smartboards remains.
  - **Ingest Buffer:** A district or school LAN edge node that locally buffers data before WAN transmission.
  - **Central OSS Backend:** An India-hosted cloud backend comprising an API Gateway, MediaMTX ingest, Postgres DB, and MinIO object storage.
  - **Inference Layer:** Bare-metal RTX 5070 GPU clusters running Celery-driven Python background workers.
- **Integrations:**
  - Meta Wearables DAT SDK for POV video and audio capture.
  - MediaMTX / WebRTC for live stream capabilities.
  - Qwen2.5-7B, faster-whisper, PyAnnote, and YOLO11n for local AI inference.
- **Data Flow:** The Android DAT app captures chunks -> routes through the Edge Buffer to the WAN -> MediaMTX / API Gateway -> stored in MinIO. Celery background queues pick up jobs -> GPU AI workers process the payload -> structured insights are saved to Postgres -> Next.js Admin Dashboards present the data.
- **Infrastructure Topology:** Centralized heavy compute (India cloud) supported by lightweight, decentralized edge nodes in classrooms.

## Deployment Strategy

The deployment strategy emphasizes rapid iteration, validation, and incremental rollout to mitigate risk.

- **Rollout Plan:**
  - _Phase 1:_ Focus on MVP audio-only ASR processing using synthetic data and Mock Device Kit (MDK) for the Meta Ray-Ban capture, pending G2 sign-off.
  - _Phase 2:_ Deploy the full multimodal cold path (audio + video proxies) to a pilot environment.
  - _Phase 3:_ Introduce Hot Path capabilities for near real-time live dashboard metrics.
- **Environments:**
  - Local: Docker Compose (`infra/compose.dev.yaml`) and MDK for developers.
  - Staging: Cloud environment for pilot schools to dry run without real student data.
  - Production: Network-isolated, India-based cloud.
- **CI/CD:** Automated pipelines (`.github/workflows/test.yml`) running backend `pytest`, frontend `vitest`, worker integration tests, and strict markdown linting (`dev-verify.sh`).
- **Rollback Mechanisms:** Database changes can be rolled back via ORM migrations. Immutable raw session payloads in MinIO enable reprocessing if a new AI model version regresses. Containerized worker deployments ensure quick reversion to stable image tags.

## Infrastructure Design

Infrastructure design prioritizes scalable orchestration while managing tight hardware limits.

- **Cloud Architecture:** Bare-metal instances in India data centers. A clear separation is maintained between stateful data stores (MinIO, Postgres) and stateless, auto-scaling inference worker pools.
- **Scaling Model:** Asymmetric. CPU-bound ingest nodes (API, Gateway) scale horizontally to handle concurrent classroom uploads. GPU workers rely on distributed queues (Celery/Redis) to process heavy inference workloads asynchronously, preventing system overload during peak school hours.
- **Observability:** Distributed tracing via OpenTelemetry spanning the API and workers. Prometheus monitors critical hardware metrics (GPU VRAM, queue depth), while Grafana visualizes system health, latency, and throughput.
- **Security:** Strict data residency enforcement in India. Inference workers operate in ephemeral, network-isolated containers. API access requires HTTPBearer token authentication. To ensure data privacy, raw video is never passed directly to the LLM; only extracted, blurred metadata is analyzed.

## AI System Design

The AI system is tuned to run entirely on the OSS-first RTX 5070 (12GB VRAM) budget.

- **Models:**
  - ASR: `faster-whisper` (quantized INT8).
  - Diarization: PyAnnote.
  - Computer Vision: YOLO11n (for activity detection/tracking proxies).
  - Reasoning LLM: `Qwen2.5-7B-Instruct` (quantized Q4_K_M).
- **Retrieval Systems:** `BGE-m3` embedding models feed a RAG system indexing pedagogical rubrics and district curriculums (stored via pgvector or Qdrant) to ground LLM reasoning.
- **Orchestration:** Orchestrated sequentially via Celery queues to avoid OOM on the 12GB VRAM limit. Steps include: fetching session, downloading chunks, ASR/diarization, CV proxy extraction, metadata alignment, and finally LLM generation.
- **Inference Strategy:** Models are dynamically loaded and unloaded to stay within memory limits. The LLM is strictly prompted to output structured JSON based only on pre-processed temporal metadata, effectively mitigating hallucination and reducing the compute burden.

## Integration Plan

The platform unites fragmented capture sources into a unified analytical backend.

- **APIs:** A FastAPI backend offering REST endpoints (e.g., `/v1/dat-sessions/*`) to manage the lifecycle of wearable sessions and handle chunked multipart uploads.
- **Services:** Processing is decoupled into specialized background workers (`worker-asr`, `worker-cv`, `worker-metrics`, `worker-llm`) connected via Redis task queues.
- **Data Pipelines:** Dead Letter Queues (DLQs) are strictly implemented in all worker services to capture exceptions, raw payloads, and stack traces, ensuring no data loss and facilitating rapid recovery.
- **Synchronization:** The backend utilizes the audio sample clock as the master timestamp, aligning asynchronous OCR events, screen captures, and video metadata to maintain a coherent chronological timeline.

## Operational Reliability

Resilience is built into both the edge and cloud components.

- **Failover Systems:** The edge ingest buffer stores chunks locally during WAN disruption, automatically syncing once connectivity returns. Stateless background workers push failed tasks to DLQs for automatic or manual retries.
- **Monitoring:** OpenTelemetry provides comprehensive insights into request flows. Strict logging standards (e.g., `traceback.print_exc()` to `sys.stderr` in workers) enable fast operational debugging.
- **Incident Recovery:** In the event of a catastrophic model hallucination or pipeline failure, operations can replay the original immutable session chunks from MinIO through corrected models to regenerate insights.
- **Resilience Mechanisms:** The asynchronous cold path design inherently decouples ingest from inference, ensuring that the system remains responsive even under massive spikes in capture volume.

## Risks & Tradeoffs

Architectural decisions prioritize operational impact but introduce specific constraints.

- **Operational Risks:** Relying on the single microphone array of the Meta Ray-Ban glasses in a noisy, chaotic Indian classroom environment presents a severe challenge for accurate speaker diarization.
- **Scaling Limitations:** The 12GB VRAM ceiling mandates sequential processing per node. This increases the latency of the cold path and limits the number of concurrent sessions a single node can process.
- **Deployment Risks:** The pending G2 legal sign-off restricts the use of real school and student data. This forces the team to rely heavily on synthetic data and the Mock Device Kit, potentially obscuring real-world deployment issues.
- **Security Concerns:** Even with strict data policies, intermediate AI features or metadata logs could theoretically leak PII. Robust access controls and network isolation for all storage layers are paramount.

## Agile Sprint Plan

The sprint plan is structured to aggressively validate the primary architecture while respecting regulatory blockers.

- **Sprint 04:** Focus on operational hardening. Implement DLQ patterns across all Redis-backed worker services, validate hot-path ingestion throughput, and run exhaustive end-to-end simulated DAT tests using the Mock Device Kit.
- **Sprint 05:** Deploy the Cold Path inference (ASR + Diarization) and wire the resulting data structure to the Next.js admin dashboard to generate and display preliminary pedagogical insights.
- **Sprint 06:** Finalize and deploy the Qwen2.5-7B LLM integration. Implement the RAG pipeline to retrieve curriculum rubrics, generating robust, hallucination-resistant pedagogical scoring.
- **Sprint 07:** Validate system performance on the physical Meta Ray-Ban glasses and Android companion app in a controlled staging environment, preparing for the initial post-G2 pilot.
