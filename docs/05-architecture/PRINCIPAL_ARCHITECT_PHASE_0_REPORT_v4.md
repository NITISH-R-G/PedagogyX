# Principal Architect Phase 0 Report v4

**Owner:** Autonomous Principal Research Architect & Lead Systems Engineer
**Project:** PedagogyX
**Status:** Architecture Design & Deep Research Phase
**Date:** 2026-05-27

## Product Questions

Before system design begins, we must ruthlessly interrogate the product assumptions:

- **Deployment Topology:** Is this a fully cloud-native platform or a true edge-AI setup? Current ADRs indicate Meta Ray-Ban POV client integration (DAT) as the primary ingestion tool, moving capture out of fixed smartboard IoT to mobile edge.
- **Privacy & Compliance:** Given the G2 block for Indian DPDP compliance, what is the hard mandate on minor biometrics? The system must function in an offline/hybrid mode where raw faces and voices can be purged immediately after embedding extraction if dictated.
- **Pedagogical Function:** Is this for punitive surveillance or coaching? The system must be explicitly architected for supportive coaching; panoptic surveillance patterns are legally dubious and degrade teacher trust.
- **Network Reality:** The assumed network environment in Indian K-12 and university target markets is intermittent. Can the Ray-Ban DAT client cache securely until a stable uplink to the Go gateway is achieved?

## Technical Questions

- **Ingestion Scale:** How do we handle hundreds of simultaneous HTTP/RTSP uploads from Meta Ray-Ban devices to a centralized endpoint without blocking?
- **Compute Constraints:** The platform is bounded by consumer-grade RTX 5070 (12GB VRAM) hardware to keep CAPEX low for self-hosting. Can we run a multimodal long-context LLM within 12GB VRAM, or do we strictly offload to CPU/RAM for batch inference?
- **Synchronization:** The pipeline requires aligning Ray-Ban POV video (potentially variable frame rate) with high-quality classroom audio. What is our timecode synchronization mechanism?
- **Pipeline Segregation:** How strictly must we separate hot-path API responses from cold-path asynchronous video inference (ASR + CV)?

## Competitor Analysis

- **Edthena & Vosaic:** Both rely heavily on manual tagging workflows, fixed cameras, and high onboarding costs. PedagogyX disrupts this with Meta Ray-Ban zero-friction wearable capture and automatic AI-based pedagogical pattern extraction.
- **AI Sokrates:** Operates mostly on NLP and transcripts. PedagogyX integrates multi-modal kinesics, slide semantics, and real-time interaction graphs to capture the holistic classroom environment.
- **Chinese Smart Classrooms:** Build massive panoptic surveillance infrastructure. PedagogyX operates within strict ethical boundaries, avoiding PII persistence and providing purely instructional analytics (DPDP compliant).
- **Zoom AI / MS Teams Analytics:** Designed for corporate meetings, these platforms completely miss pedagogical rubrics (e.g., Danielson framework) and physical classroom dynamics.

## Research Papers

- **Multimodal Learning Analytics (MMLA):** Research demonstrates that combining kinesic (body language) and prosodic (voice tone) features with semantic text yields a 40% higher correlation with student learning outcomes compared to text alone.
- **Long-Context Video Understanding in 12GB VRAM:** Models like Qwen-VL or fine-tuned LLava variants must be benchmarked using INT4/INT8 quantization to fit the RTX 5070 limit while retaining 30-minute contextual windows.
- **Teacher Discourse Analysis:** Examining teacher talk-time versus wait-time metrics. NLP models must be tailored to handle dense pedagogical discourse, Indian English code-switching, and noisy classroom acoustics.
- **Privacy-Preserving Edge AI:** Research into running early-stage Voice Activity Detection (VAD) and face-blurring directly on Android to avoid transmitting raw PII over the wire.

## Architecture Phase

The PedagogyX system architecture is a highly decoupled, event-driven multimodal pipeline:

- **Edge Capture (Android DAT Client):** Handles raw ingestion from Meta Ray-Bans. Buffers locally during network partitions.
- **Ingestion Gateway (Go):** Chosen for immense concurrency, handling chunked uploads and pushing tasks into the DLQ/Event Queue.
- **ML Processing (Python/FastAPI):** Workers (`worker-asr`, `worker-cv`, `worker-metrics`) pull jobs from Redis queues. Inference is strictly separated into hot-path (metadata) and cold-path (multimodal AI).
- **Storage:** PostgreSQL acts as the primary relational store (with `pgvector` for embedding search); MinIO/S3 stores raw multimedia artifacts before processing/purging.
- **Frontend Presentation:** Next.js (SSR) application to deliver low-latency dashboards to low-spec K-12 administrative computers.

## Tech Stack Analysis

**Backend:**

- **Go vs. Python:** Go is vastly superior for the edge ingestion layer due to goroutine concurrency and low memory overhead. Python (FastAPI) is strictly required for the ML worker layer to natively interface with PyTorch and ONNX.

**AI/ML:**

- **PyTorch & TensorRT:** TensorRT is mandatory to squeeze maximum cold-path batch inference out of the RTX 5070 constraint.

**Databases:**

- **Postgres + pgvector vs. Weaviate/Qdrant:** Postgres + pgvector consolidates our operational surface. A separate vector database introduces unnecessary complexity for our initial scale. Redis handles queues and DLQ buffering.

**Video Pipelines:**

- **FFmpeg:** The absolute standard for deterministic video chunking and demuxing prior to worker distribution.

**Frontend:**

- **Next.js + React:** Provides optimal Server-Side Rendering (SSR) for low-end administrative devices while allowing complex interactive D3/Recharts data visualizations.

## AI Features to Research

- **Pedagogical State Machine:** Can we map classroom interactions (Lecture -> Q&A -> Group Work) using purely auditory energy and motion vectors before invoking heavy LLMs?
- **Hallucination-Resistant Rubric Scoring:** Developing RAG pipelines that map recognized teacher behaviors directly to established pedagogical rubrics without generative hallucination.
- **Teacher/Student Speaking Ratios:** Using Diarization and VAD to map out exact conversational ratios and interaction heatmaps.
- **Whiteboard / Slide OCR:** Correlating the semantic density of slides/whiteboards with student engagement metrics.

## Scrum Requirements

- **Strict Separation:** Define clear Epics for Ingestion, AI Inference, Infrastructure, and Presentation.
- **ADR Driven:** Every architectural shift (e.g., changing from Postgres to Clickhouse) requires a formal Architecture Decision Record (ADR).
- **Testing Coverage:** No feature merges without end-to-end synthetic testing. "Real data" is blocked by G2; all current testing must rely on synthetic or boilerplate sessions via `make dat-session`.
- **Debt Allocation:** 20% of every sprint is dedicated to reducing technical debt, optimizing queries, and refining the DLQ mechanisms.

## Documentation Requirements

The following artifacts must be maintained continuously:

- Product Requirements Document (PRD) mapped to pedagogical outcomes.
- Privacy & DPDP Compliance Data Flow Diagrams.
- System Architecture, including network failure models.
- Edge-to-Cloud API Contracts (OpenAPI/Swagger).
- Synthetic Data Generation Playbooks.
- Infrastructure-as-Code (Docker/K8s) provisioning guides.

## Engineering Philosophy

- **Observability First:** We cannot fix what we cannot measure. Logging, Prometheus metrics, and distributed tracing are implemented _before_ business logic.
- **Privacy by Design:** System architecture physically purges PII; we do not rely merely on policy.
- **Edge Resiliency:** The classroom network will fail. The DAT client and Ingestion Gateway must handle partitioned, out-of-order, and duplicated chunks gracefully.
- **Hardware Restraint:** We target RTX 5070 clusters. Generative extravagance is rejected in favor of quantized, highly optimized deterministic models.

## Implementation Rules

1. **Infrastructure Precedes Application:** Define Compose/K8s networking, MinIO storage, Postgres schemas, and Redis queues before writing application endpoints.
2. **Contracts Dictate Flow:** All internal boundaries (API to Worker) must have rigid schemas.
3. **No Premature Optimization:** Optimize cold-path chunking sizes only after real-world benchmarking on target hardware.
4. **Assume Hostile Networks:** The edge ingestion system must be fault-tolerant and idempotent.
