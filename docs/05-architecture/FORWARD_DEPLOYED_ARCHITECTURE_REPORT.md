# Forward Deployed Architecture Report

**Role:** Autonomous Forward Deployed Engineer & Strategic AI Systems Operator
**Status:** Operational Execution Draft

## Operational Problem Analysis

- **Business Context:** PedagogyX aims to deploy multimodal AI classroom intelligence to optimize teacher performance across Indian schools, navigating strict budget constraints (₹0 edge hardware), latency targets, and data residency laws.
- **Workflow Analysis:** Teachers run 45-50 minute sessions. They require frictionless capture. Administrators need actionable pedagogy metrics (talk ratio, interaction density, wait time) via web dashboards. Wait time between capturing a session and generating actionable insights needs to be minimized.
- **Bottlenecks:** Unreliable school WAN connections, high edge compute costs, the operational complexity of syncing multiple streams (audio, screen, video), and the 12GB VRAM constraint on the central RTX 5070 GPU servers.
- **Operational Constraints:** India-specific legal compliance (DPDP, pending G2 sign-off), zero hardware budget at the edge, requiring OSS-first AI pipelines rather than proprietary APIs to control unit economics.

## System Architecture

- **Major Components:**
  - **Capture Edge:** Meta Ray-Ban (DAT) primary client (Android companion app) and fallback Windows smartboards.
  - **Ingest Buffer:** District/school LAN edge node running a lightweight buffer.
  - **Central OSS Backend:** API Gateway, MediaMTX ingest, Postgres, MinIO.
  - **Inference Workers:** Celery-driven Python background workers running on bare-metal RTX 5070 GPU clusters.
- **Integrations:** Meta DAT SDK for wearable capture, WebRTC/SFU for potential live supervision paths, and Ollama/vLLM for local AI model serving.
- **Data Flow:** Capture Agent (Android DAT) -> Edge Buffer -> (WAN) -> MediaMTX Ingest -> Fast Storage (MinIO) -> Processing Queue (Celery) -> GPU AI Workers (ASR, CV, LLM) -> Insights Database (Postgres) -> Next.js Admin Dashboards.
- **Infrastructure Topology:** Hybrid Edge-Cloud. Low-spec edge clients stream to a central high-density OSS-based cloud infrastructure.

## Deployment Strategy

- **Rollout Plan:**
  - Phase 1: MVP audio-only ASR processing using Meta Ray-Ban DAT capture, targeting synthetic testing until G2 legal gate clears.
  - Phase 2: Full multimodal cold path processing.
  - Phase 3: Rollout of Hot Path heuristics for live dashboards.
- **Environments:** Local Docker Compose for development (`infra/compose.dev.yaml`), staging cloud for pilot dry runs, and a fully network-isolated production India cloud pool.
- **CI/CD:** GitHub Actions `.github/workflows/test.yml` running Pytest (backend), Vitest (frontend), and worker integration tests. Automated markdown linting.
- **Rollback Mechanisms:** Database migrations managed via standard ORM rollbacks. Immutable object storage allows re-processing of raw payloads if AI models are rolled back. Containerized workers allow rapid reversion of model weights/versions.

## Infrastructure Design

- **Cloud Architecture:** Bare-metal instances in India data centers. Stateful workloads (MinIO, Postgres) isolated from stateless, auto-scaling GPU worker pools.
- **Scaling Model:** Asymmetric scaling. CPU ingest nodes scale out horizontally based on concurrent classroom sessions. GPU workers process asynchronously via a distributed queue (Celery/Redis) to maximize throughput and smooth out spikes.
- **Observability:** OpenTelemetry traces across API and workers. Prometheus for GPU/VRAM monitoring and queue depth. Grafana for system health and model latency dashboards.
- **Security:** Strict data residency (India). Ephemeral, network-isolated inference containers. Implicit API Key authentication (via `HTTPBearer`) for initial DAT interactions. Data minimization: no raw video faces passed to the LLM.

## AI System Design

- **Models:** `faster-whisper` (ASR), PyAnnote (Diarization), YOLO11n (CV for tracking proxies), and `Qwen2.5-7B-Instruct` (LLM Reasoning).
- **Retrieval Systems:** `BGE-m3` embedding model indexing district curriculums into Qdrant/pgvector for RAG during LLM reasoning.
- **Orchestration:** Orchestrated via the Celery task queue, executing discrete synchronous steps: fetch session, download chunk, transcribe/diarize, extract CV proxies, run alignment logic, and perform LLM synthesis.
- **Inference Strategy:** Quantized models (e.g., INT8 for whisper, Q4_K_M for Qwen) to fit within the 12GB VRAM constraint. Strict VRAM management: sequentially load ASR then LLM to prevent OOM errors. Deep constraint on the LLM: output structured JSON using temporal metadata rather than direct raw video analysis to mitigate hallucination.

## Integration Plan

- **APIs:** FastAPI backend exposing REST endpoints for session lifecycle (`/v1/dat-sessions/*`) and multipart chunk uploads.
- **Services:** Decoupled `worker-asr`, `worker-cv`, and `worker-llm` connected via Redis queues.
- **Data Pipelines:** Dead Letter Queues (DLQs) implemented on Redis to capture failed job payloads and stack traces for operational recovery.
- **Synchronization:** The backend implements alignment logic, using audio sample clocks as the master timestamp to correlate screen OCR and video tracking metadata.

## Operational Reliability

- **Failover Systems:** The edge buffer holds raw capture chunks during WAN outages. Stateless worker architecture ensures that failed jobs are pushed to a DLQ and retried automatically.
- **Monitoring:** OpenTelemetry instrumented API. Strict enforcement of logging tracebacks to `sys.stderr` for rapid operational debugging.
- **Incident Recovery:** Operations can replay raw session data stored in MinIO through updated inference pipelines if initial extraction fails or models hallucinate.
- **Resilience Mechanisms:** The Cold Path architecture is fundamentally resilient to temporal spikes, as all computationally heavy tasks are queued rather than executed synchronously against user requests.

## Risks & Tradeoffs

- **Operational Risks:** Single-microphone audio capture in noisy classrooms makes accurate diarization extremely difficult.
- **Scaling Limitations:** 12GB VRAM ceiling prevents concurrent model execution on a single node, necessitating sequential processing, which limits peak throughput per node.
- **Deployment Risks:** Regulatory compliance (G2) blocking access to real-world training data limits immediate system validation to synthetic environments.
- **Security Concerns:** While raw videos are blurred, any leak of unencrypted intermediate features could violate strict Indian data protection mandates. Storage must be fiercely access-controlled.

## Agile Sprint Plan

- **Sprint 03 (MVP Prep - Post-G2):** Deploy initial API ingest framework, set up Postgres and MinIO, and establish the `worker-asr` skeleton for processing DAT audio chunks.
- **Sprint 04:** Implement DLQ reliability patterns in worker services, validate hot-path ingestion throughput, and run end-to-end simulated DAT tests via CLI.
- **Sprint 05:** Integrate the Cold Path inference (ASR + Diarization) and wire the output to the Next.js admin dashboard to generate preliminary pedagogical insight metrics.
- **Sprint 06:** Finalize LLM integration (`Qwen2.5-7B`), implementing RAG retrieval of curriculum rubrics to generate hallucination-resistant pedagogical scoring.
