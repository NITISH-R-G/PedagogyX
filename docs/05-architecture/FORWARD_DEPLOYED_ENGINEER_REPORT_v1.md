# Forward Deployed Engineer & Strategic AI Systems Operator Report v1

## Operational Problem Analysis

- **Business Context:** Operating under strict budget constraints, PedagogyX aims for ₹0 edge hardware cost by leveraging self-hosted OSS AI models. Stringent data privacy constraints due to Indian data residency laws (DPDP) and an impending G2 legal sign-off require utilizing synthetic data sets.
- **Workflow Analysis:** Teachers run 45-50 minute sessions needing frictionless, hands-free capture via Meta Ray-Ban glasses, shifting from the traditional smartboards strategy. Administrators need actionable, near real-time pedagogy metrics like talk-ratio.
- **Bottlenecks:** Unreliable school WAN connections, high edge compute costs, and a strict 12GB VRAM ceiling on the centralized RTX 5070 GPU servers.
- **Operational Constraints:** The new v1 capture client consists of Meta Ray-Ban smart glasses (ADR-0009) communicating via Bluetooth to an Android host, utilizing the Wearables DAT SDK. Development requires use of Mock Device Kits (MDK) in CI without requiring physical glasses.

## System Architecture

- **Major Components:**
  - _Capture Layer:_ Meta Ray-Ban smart glasses and an Android host running the PedagogyX capture app (DAT host).
  - _Backend Infrastructure:_ Central OSS backend hosted in India to comply with DPDP, incorporating an API Gateway, Postgres DB, and MinIO object storage.
  - _Inference Layer:_ Bare-metal clusters equipped with RTX 5070 GPUs utilizing Celery queues for processing.
- **Integrations:** Meta Wearables DAT SDK (`mwdat-core`, `mwdat-camera`), chunked HTTP uploads for slow connections, and locally hosted AI pipelines (Qwen2.5-7B, faster-whisper, PyAnnote, YOLO11n).
- **Data Flow:** Video/Audio captured by Meta Ray-Ban POV cameras/mics -> Bluetooth to Android Host -> HTTP chunks -> API Gateway -> MinIO. Celery workers fetch tasks -> GPU inference -> Postgres -> Next.js Admin Dashboards.
- **Infrastructure Topology:** Centralized scalable heavy compute with lightweight edge clients via smart glasses.

## Deployment Strategy

- **Rollout Plan:**
  - _Phase 1:_ Synthetic data MVP audio-only ASR processing using the MDK for initial talk-ratio metrics.
  - _Phase 2:_ Multimodal cold-path processing incorporating both audio and video proxies.
  - _Phase 3:_ Optimization for real-time live dashboard capabilities.
- **Environments:** Docker Compose setups for rapid local MVP validation, shifting to network-isolated India-based cloud for production deployments.
- **CI/CD:** Automated testing using GitHub Actions testing backend (`pytest`) with mock data and verifying documentation with markdown linters.
- **Rollback Mechanisms:** Immutable MinIO blob storage allowing reprocessing of session chunks, coupled with DB ORM migrations.

## Infrastructure Design

- **Cloud Architecture:** India-based bare-metal deployment featuring strict separation between stateful storage (MinIO/Postgres) and stateless scalable Celery workers.
- **Scaling Model:** Asymmetric scaling: lightweight API horizontally scales for ingestion while asynchronous queue limits GPU workloads to avoid OOM due to the 12GB VRAM limit.
- **Observability:** Centralized tracing via OpenTelemetry with Prometheus metrics on Grafana dashboards for continuous monitoring of infrastructure health.
- **Security:** Complete DPDP alignment. Strong API HTTPBearer authentication, zero raw videos sent to the LLM layer, and zero PII exposure until the G2 block is lifted.

## AI System Design

- **Models:**
  - Quantized ASR: `faster-whisper` (INT8)
  - Diarization: `PyAnnote`
  - Vision Proxies: `YOLO11n`
  - LLM: `Qwen2.5-7B-Instruct` (Q4_K_M)
- **Retrieval Systems:** BGE-m3 RAG pipelines to enrich insights using curriculums and rubrics.
- **Orchestration:** Strict sequential task chaining (Download -> ASR/Diarization -> Vision Proxy -> Alignment -> LLM) managed by Celery queues to protect VRAM.
- **Inference Strategy:** Dynamic model memory allocation/swapping inside the 12GB footprint. The LLM produces strict JSON from proxy metadata only.

## Integration Plan

- **APIs:** FastAPI implementation exposing `/v1/dat-sessions/*` to simulate DAT callbacks and accept multipart chunk uploads.
- **Services:** Decoupled Celery worker architecture handling specific processing steps (`worker-asr`, `worker-cv`, `worker-metrics`).
- **Data Pipelines:** Integrated Dead Letter Queues (DLQs) to capture processing failures and allow seamless chunk reprocessing.
- **Synchronization:** The primary clock is derived from the audio samples on the smart glasses, ensuring all asynchronous tasks can synchronize metadata downstream.

## Operational Reliability

- **Failover Systems:** The Android Host app stores offline local buffers and pushes chunks when WAN connects.
- **Monitoring:** OpenTelemetry implementations combined with rigorous traceback policies in Celery components.
- **Incident Recovery:** Built-in capability to replay session streams directly from immutable MinIO sources.
- **Resilience Mechanisms:** The asynchronous worker model insulates the API ingest gateway from performance spikes during heavy computational workloads.

## Risks & Tradeoffs

- **Operational Risks:** Real-world acoustic variables may heavily impact diarization from the Ray-Ban's single microphone array.
- **Scaling Limitations:** Constraining inference into the 12GB RTX 5070 footprint introduces processing caps, increasing cold path latency under high load.
- **Deployment Risks:** Relying heavily on synthetic data (due to the G2 block) masks unknown edge cases related to school network latency and real-world noise.
- **Security Concerns:** Although no raw video reaches the LLM, the derived metadata might still inadvertently contain PII requiring careful string-scrubbing.

## Agile Sprint Plan

- **Sprint Goal:** Validate the primary capture path vertically using the DAT Mock Device Kit with synthetic data pending the G2 legal memo.
- **Implementation Phases:**
  1. Solidify the `/v1/dat-sessions/*` endpoints mapping to DAT lifecycle hooks.
  2. Complete the Android host app integrating the Meta Wearables DAT SDK via Mock Device Kit (MDK).
  3. Finalize the `worker-asr` implementation to generate transcripts from audio chunks.
  4. Display synthetic talk-ratio metrics on the Next.js web dashboard.
- **Operational KPIs:** Achieve end-to-end processing of a synthetic 45-minute audio session within 30 minutes.
- **Expected Impact:** Demonstrates a functional MVP with Ray-Ban capture, securing confidence for full rollout once G2 constraints are lifted.
