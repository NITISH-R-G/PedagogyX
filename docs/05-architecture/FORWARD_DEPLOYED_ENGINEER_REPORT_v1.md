# FORWARD DEPLOYED ENGINEER REPORT v1

## Operational Problem Analysis

The PedagogyX system faces the complex operational challenge of bridging edge capture devices in real-world educational environments with robust, scalable cloud infrastructure. The core bottleneck lies in capturing unstructured data from Meta Ray-Ban smart glasses (via the Android DAT client) in the field—where network reliability is variable—and transmitting it seamlessly to a cloud backend for rapid AI processing.

Currently, the workflow relies heavily on the physical constraints of deployment and the necessity to avoid operational friction for end users who are focused on pedagogy, not technology. The operational constraints demand a system that can gracefully handle intermittent connectivity using Go-based LAN edge buffers for initial ingestion before funneling data into the OSS-first AI backend in India. Delaying processing or dropping data creates direct user friction; thus, eliminating these bottlenecks through highly robust queuing mechanisms and failover strategies is paramount to maximizing business impact.

## System Architecture

The overarching design of PedagogyX follows a Hybrid Edge-Cloud model, optimized for simplicity and maintainability while addressing the fragmentation of edge vs. cloud execution.

1. **Edge Client Tier:** Meta Ray-Ban smart glasses serve as the primary capture vector, functioning through an Android client app utilizing the Wearables DAT SDK.
2. **Ingestion & Buffering Tier:** Go-based LAN edge buffers locally absorb data spikes and handle offline scenarios to prevent data loss in degraded network environments.
3. **Core Services Tier (Cloud):**
   - A `services/web` frontend powered by React and Next.js 15 (App Router).
   - A `services/api` RESTful backend leveraging FastAPI.
4. **Asynchronous Worker Tier:** Background processing units handle heavy lifting, communicating with the API via Redis queues and MinIO storage. Notable workers include:
   - `worker-metrics` (entry point: `worker.metrics_main`)
   - `worker-asr` (entry point: `worker.asr_main`)
   - `worker-cv`

Data flows continuously from the edge, through local buffers, to the cloud API, which then orchestrates the state and delegates asynchronous workloads via Redis to the workers for processing and persistence in MinIO.

## Deployment Strategy

Rapid deployment velocity and deployment simplicity are prioritized to support continuous field testing.

- **Environments:** The current baseline utilizes a local Docker Compose stack (`infra/compose.dev.yaml`) tailored for founder/developer iteration and rapid prototyping.
- **Rollout Plan:** The immediate objective focuses on validating synthetic sessions (`make dat-session`) before transitioning to pilot deployments. The real-world deployment strategy will deploy the API and Web services to robust cloud environments while ensuring edge clients are sideloaded or MDM-managed for field testers.
- **CI/CD:** Automated validation is handled via GitHub Actions (`.github/workflows/dev-verify.yml`) for documentation and basic smoke testing. The deployment pipeline will be extended to automate Docker image builds and immutable deployments.
- **Rollback Mechanisms:** Leveraging container orchestration, rollback procedures will rely on reverting to prior verified image tags if operational metrics degrade post-deployment, ensuring rapid recovery.

## Infrastructure Design

The infrastructure is designed for low operational complexity while supporting necessary scale and security.

- **Cloud Architecture:** Centralized cloud deployment relies on containerized microservices (API, Web, Workers) working alongside managed infrastructure data stores (Redis, MinIO).
- **Scaling Model:** The system scales horizontally at the worker tier. As AI processing demands increase, additional `worker-cv`, `worker-metrics`, or `worker-asr` instances can be provisioned independently.
- **Observability:** Current validation involves benchmark scripts (`benchmarks/bench_full_pipeline.sh`) and local logging. Production observability will require centralizing logs across the Android clients, LAN buffers, and containerized cloud services.
- **Security:** Security is foundational, currently enforced via API key authentication (`API_KEY`) for API testing and service communication. Future expansion will focus on securing data in transit between the edge buffers and the cloud, and strictly adhering to G2 compliance rules for school data processing.

## AI System Design

The AI architecture is structured to support multimodal processing while mitigating latency and hallucination risks.

- **Models:** The system primarily integrates with OSS-first AI backend systems situated in India, optimizing for both hot and cold path processing based on operational urgency.
- **Orchestration:** FastAPI acts as the central orchestrator, determining which tasks (e.g., computer vision, speech recognition) require immediate action and queuing them appropriately.
- **Inference Strategy:** Inference execution is heavily asynchronous. Audio streams are routed to `worker-asr` and image/video streams to `worker-cv`. Intermediate outputs are stored in MinIO, while Redis handles state tracking to ensure the web frontend can asynchronously poll for or receive processing updates.
- **Retrieval Systems:** The architecture prepares for robust retrieval mechanics by isolating processing logic, ensuring that synthesized educational metrics are rapidly accessible without re-running expensive inference pipelines.

## Integration Plan

Unifying this fragmented ecosystem requires deliberate integration interfaces.

- **APIs:** The `services/api` layer provides standard REST endpoints. Fast failure and structured HTTP exceptions (using `fastapi.status` constants) are enforced to maintain a clear boundary and reliable communication.
- **Data Pipelines:** Raw sensor data (audio/video) from the Meta Ray-Bans moves through Android capturing APIs -> Go-based LAN edge buffers -> FastAPI -> MinIO/Redis -> Background Workers.
- **Services:** Inter-service integration is decoupled via Redis. The FastAPI service publishes tasks; `worker-metrics` (`worker.metrics_main`) and `worker-asr` (`worker.asr_main`) subscribe to these queues, ensuring that failure in one worker does not cascade to the core API.
- **Synchronization:** Event-driven polling and state tracking will keep the Next.js 15 frontend synchronized with backend AI processing states.

## Operational Reliability

Reliability is paramount, given the real-world deployment constraints.

- **Resilience Mechanisms:** The Go-based LAN edge buffer acts as the primary defense against network failures, ensuring data is not lost if the cloud is unreachable.
- **Monitoring:** While comprehensive distributed tracing is to be implemented, current mechanisms rely on CI checks and synthetic smoke tests (`./scripts/compose-smoke.sh`, `make dat-session`).
- **Failover Systems:** The decoupled worker architecture means if `worker-asr` fails, `worker-metrics` continues to function. Redis queues ensure tasks are not dropped but remain pending until a worker restarts.
- **Incident Recovery:** The local-first fallback mechanisms on the Android client and the LAN buffer provide sufficient time to restore cloud API availability without catastrophic data loss during operational field hours.

## Risks & Tradeoffs

To move fast with reliability, specific architectural tradeoffs have been accepted.

- **Operational Risks:** Relying on experimental hardware (Meta Ray-Ban) introduces dependency on third-party SDK stability (Wearables DAT SDK).
- **Deployment Risks:** Field deployment of LAN edge buffers adds physical infrastructure complexity that must be managed remotely.
- **Scaling Limitations:** Centralized MinIO and Redis instances represent potential single points of failure under extreme load if not clustered effectively in the future.
- **Tradeoffs:** Choosing a Hybrid Edge-Cloud model increases system complexity compared to a purely cloud-native approach, but it is necessary to overcome the physical reality of poor school networks and ensure immediate data capture reliability.

## Agile Sprint Plan

Operating as a high-velocity embedded engineering team, the next tactical steps are defined:

- **Phase 1: Validation & Smoke Testing:**
  - Complete the integration of the DAT session simulator (`tools/dat-session-sim/dat_session_cli.py`) to connect reliably against the FastAPI container at `http://localhost:8080`.
  - Expected Impact: Validates the core data ingestion pipeline before field deployment.
- **Phase 2: Worker Tier Hardening:**
  - Ensure the `worker-metrics` and `worker-asr` entry points successfully consume and process synthetic payloads from Redis and store artifacts in MinIO.
  - Expected Impact: Confirms asynchronous processing reliability.
- **Phase 3: Frontend Synchronization:**
  - Deploy the Next.js 15 frontend (`services/web`) and ensure dependencies resolve correctly (using `--legacy-peer-deps` during installation).
  - Expected Impact: Achieves end-to-end visibility of system health and processed metrics.
- **Phase 4: Field Ready Deployment:**
  - Sideload the `clients/android-capture-dat` application and test offline edge buffering.
  - Operational KPIs: Measure API error rates, edge-to-cloud latency, and synthetic session success rate.
