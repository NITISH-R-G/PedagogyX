# Forward Deployed Architecture Report v4

## Operational Problem Analysis

- **Business Context:** PedagogyX is an educational analytics platform operating under stringent budgetary constraints (targeting ₹0 edge hardware cost) by leveraging OSS-first, self-hosted AI models. Strict data handling constraints are dictated by Indian data residency laws (DPDP) and an impending G2 legal sign-off.
- **Workflow Analysis:** Teachers operate in 45-50 minute classroom sessions, necessitating a frictionless, hands-free capture process. Administrators require timely review of actionable pedagogy metrics such as talk ratio via web dashboards to guide instructional improvements.
- **Bottlenecks:** Unreliable school WAN connections, prohibitive edge compute costs, and an absolute 12GB VRAM ceiling on central RTX 5070 GPU server components.
- **Operational Constraints:** A shift to Meta Ray-Ban smart glasses as the primary v1 client demands reliable capture via the Wearables DAT SDK over Bluetooth, managed through an Android host application. The project is currently blocked pending the G2 counsel memo, restricting the use of real school and student data to synthetic datasets and the local MVP boilerplate stack.

## System Architecture

- **Major Components:**
  - _Capture Layer:_ Meta Ray-Ban smart glasses connected to an Android companion app via Wearables DAT SDK.
  - _Ingest Buffer:_ Local district/school edge nodes.
  - _Backend:_ India-hosted central OSS backend consisting of an API Gateway (FastAPI), MediaMTX ingest, Postgres DB, and MinIO object storage.
  - _Inference Layer:_ Bare-metal RTX 5070 GPU clusters running Celery Python background workers for AI processing.
- **Integrations:** Meta Wearables DAT SDK, MediaMTX/WebRTC, and local AI stack (Qwen2.5-7B, faster-whisper, PyAnnote, YOLO11n).
- **Data Flow:** Android DAT captures HTTP chunks -> Edge Buffer -> WAN -> MediaMTX/API Gateway -> MinIO. Celery queues pick up the chunks -> GPU inference workers -> Postgres -> Next.js Admin Dashboards preview metrics.
- **Infrastructure Topology:** Centralized heavy compute with lightweight decentralized edge nodes in classrooms for capturing and buffering data.

## Deployment Strategy

- **Rollout Plan:**
  - _Phase 1:_ MVP audio-only ASR processing using synthetic data and MDK, targeting initial talk-ratio metric generation for Sprint 03.
  - _Phase 2:_ Multimodal cold path (audio + video proxies) to expand analytical capabilities.
  - _Phase 3:_ Near real-time live dashboard capabilities for instant feedback.
- **Environments:** Local Docker Compose setups (`infra/compose.dev.yaml`) for founders, staging environments for dry runs, and a network-isolated India-based cloud for production.
- **CI/CD:** Automated pipelines via `.github/workflows/test.yml` running backend/frontend tests and markdown verification (`dev-verify.sh`).
- **Rollback Mechanisms:** Database ORM migrations, immutable raw payloads in MinIO, and container image reversions.

## Infrastructure Design

- **Cloud Architecture:** Bare-metal Indian data centers with strict isolation between stateful storage (Postgres, MinIO) and stateless auto-scaling workers (Celery).
- **Scaling Model:** Asymmetric scaling; horizontal CPU scaling for ingest combined with queue-driven sequential GPU worker loads to manage the 12GB VRAM constraint.
- **Observability:** Distributed tracing (OpenTelemetry) and Prometheus metrics visualized in Grafana.
- **Security:** Strict data residency (DPDP), HTTPBearer API auth, and zero raw video passage to the LLM (only extracted metadata).

## AI System Design

- **Models:** faster-whisper (quantized INT8) for ASR, PyAnnote for diarization, YOLO11n for CV proxy metrics, and Qwen2.5-7B-Instruct (Q4_K_M) for reasoning.
- **Retrieval Systems:** BGE-m3 embedding RAG pipeline indexing rubrics and curriculums for contextual assessment.
- **Orchestration:** Strict sequential processing via Celery queues (download -> ASR/diarization -> CV proxy -> alignment -> LLM) to prevent out-of-memory (OOM) errors on the 12GB GPUs.
- **Inference Strategy:** Dynamic model loading/unloading into the 12GB footprint, strictly prompting the LLM for JSON outputs derived solely from pre-processed temporal data.

## Integration Plan

- **APIs:** FastAPI backend REST endpoints (`/v1/dat-sessions/*`) handling resumable chunk uploads and session metadata.
- **Services:** Decoupled background processing workers (`worker-asr`, `worker-cv`, `worker-metrics`).
- **Data Pipelines:** Dead Letter Queues (DLQs) in workers to capture failures and facilitate manual/automatic retries.
- **Synchronization:** The audio sample clock serves as the master chronological timeline across asynchronous processes to ensure multimodal alignment.

## Operational Reliability

- **Failover Systems:** Local chunk buffering on the edge node and DLQs for stateless background tasks to handle network drops.
- **Monitoring:** OpenTelemetry integrated with strict traceback logging standards (`sys.stderr` in Celery workers).
- **Incident Recovery:** Capability to replay immutable session chunks from MinIO to re-process failed jobs.
- **Resilience Mechanisms:** Pure asynchronous decoupled design preventing API blockages during heavy load spikes from classroom captures.

## Risks & Tradeoffs

- **Operational Risks:** The single microphone array of the Meta Ray-Bans represents a high risk for accurate speaker diarization in noisy classroom environments.
- **Scaling Limitations:** The sequential per-node processing enforced by the VRAM limit creates a hard cap on concurrent session processing and increases cold path latency.
- **Deployment Risks:** Reliance on synthetic test data due to the G2 legal block could obscure production edge cases and real-world audio challenges.
- **Security Concerns:** The potential for PII leak in metadata logs remains, necessitating stringent network isolation, strict access controls, and zero-trust policies.

## Agile Sprint Plan

- **Implementation Phases:**
  1. API Skeleton & Storage Migrations
  2. Resumable Upload Path setup
  3. `worker-asr` container deployment (faster-whisper)
  4. Talk ratio calculation logic implementation
  5. UI data wiring for the admin dashboard
- **Deployment Milestones:** Complete Phase 1 audio/upload vertical slice: Android Host -> API Upload -> MinIO/Postgres -> `worker-asr` transcript -> Talk Ratio Job -> Next.js Admin Web Shell preview.
- **Operational KPIs:** System validation with a sub-30 minute processing target for a 45-minute lesson without production data violations.
- **Expected Impact:** Demonstrable, authorized prototype yielding initial pedagogical metrics matching Phase 1 MVP requirements, paving the way for Phase 2 multimodal processing upon G2 sign-off.
