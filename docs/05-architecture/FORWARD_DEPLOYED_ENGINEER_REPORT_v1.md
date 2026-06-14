# Strategic AI Systems & Forward Deployed Engineering Architecture

## Operational Problem Analysis

PedagogyX is currently in a pre-production "Phase 0" moving towards an MVP deployment for school environments. We are fundamentally integrating computer vision, speech intelligence, and multimodal transformers into edge hardware (Meta Ray-Ban devices via DAT clients) and deploying it reliably in complex field operations.

**Business Context & Workflows:**

- Target operators are teachers/educators in dynamic, noisy, and rapidly changing classroom environments.
- Decision-making latency must be low (near real-time feedback).
- Data collection from the field is heavily impacted by strict PII limitations (India legal sign-off G2 gate pending) and relies entirely on synthetic test sessions for development.

**Bottlenecks & Operational Constraints:**

- Field hardware involves wearables and mobile clients under unpredictable network conditions.
- Strict data privacy compliance mandates aggressive segregation and careful handling of testing data.
- Rapid iteration velocity is constrained by complex integrations across AI models, wearable SDKs, and mobile capture constraints.
- Real-world environments are inherently "messy," with unstructured audio and video.

## System Architecture

The overarching system operates across an edge-client footprint and a cloud-backend processing layer to enable AI-powered classroom analytics.

**Major Components:**

- **Edge Clients:** Meta Ray-Ban devices connected to Android via DAT client (`clients/android-capture-dat`).
- **Core Backend (Cloud):** A FastAPI-based core service layer (`services/api`).
- **Processing Workers:** Asynchronous processing microservices executing offline/AI inference tasks: `worker-cv`, `worker-metrics`, `worker-asr`.
- **Frontend Layer:** React/Next.js ecosystem.

**Data Flow:**

1. Capture client pushes sensor telemetry and AV captures via API Gateway to FastAPI.
2. The core API dispatches payloads asynchronously to specialized worker queues (`worker-cv`, `worker-asr`).
3. Workers process audio/visual data through respective AI pipelines.
4. Extracted metrics sync to `worker-metrics` for higher-order aggregation and are cached/stored before surfacing to web portals.

## Deployment Strategy

Deployment is focused on high-velocity iteration, operational validation through synthetic data, and reducing time-to-deployment on field systems.

**Rollout Plan:**

- **Phase 0:** Synthetic data and mock captures (`mock_capture.py`, `make dat-session`) to test architecture and workflows locally without requiring field hardware.
- **Phase 1 (MVP Prep):** Deploying API and worker scaffolding to development environments while testing wearable workflows securely.
- **Phase 2:** Controlled pilot with real pilot hardware leveraging G2 cleared legal environments.

**Environments & CI/CD:**

- Docker Compose dev stack (`infra/compose.dev.yaml`) ensuring local replication of production state.
- Automated linting, test validation, and build staging through GitHub Actions (`.github/workflows/dev-verify.yml`).
- Staging environment matches production but operates strictly on synthetic PII payloads.

**Rollback Mechanisms:**

- Containerized microservices ensure fast rollback via atomic version downgrades.
- Blue/green rollout for core API instances to prevent edge-client timeouts during updates.

## Infrastructure Design

PedagogyX requires an infrastructure design optimized for high-throughput multimodal processing with strong container orchestration.

**Cloud Architecture & Scaling Model:**

- Kubernetes-based backend deployment enabling auto-scaling of `worker-*` nodes based on queue depth during active capture sessions.
- Core data layers (Postgres, Redis, MinIO) handling varying latency profiles: object storage for media, Redis for high-speed pub/sub routing, and Postgres for relational application states.
- Local deployment proxy mirrors these systems to allow continuous testing (founder machine MVP stack).

**Observability & Security:**

- Centralized logging pipeline across all FastAPI and Python worker containers.
- Security boundary explicitly around the MVP boilerplate with Zero-Trust ingress for capturing clients to prevent rogue telemetry ingestion.
- Strict network isolation for data processing workers to protect potential future PII flows.

## AI System Design

This system incorporates complex, heavy-inference pipelines operating on asynchronous flows to optimize latency while ensuring high-fidelity insight generation.

**Models & Orchestration:**

- **ASR & CV Pipelines:** Segregated `worker-asr` and `worker-cv` allow targeted scaling of transcription and visual models.
- **Inference Strategy:** Offloaded and asynchronous inference ensures that edge devices simply capture and transmit, offloading compute constraints to horizontally scalable cloud workers.
- **Retrieval & Analysis:** A RAG system provides contextually relevant pedagogical insights based on incoming metrics and historical student/teacher interaction patterns.

## Integration Plan

Unifying fragmented ecosystems is critical to rapid deployment and operational leverage.

**APIs & Services:**

- The Android Capture DAT client acts as the central ingestion point, converting Meta Wearable data into structured REST/WebSocket streams for the backend.
- `services/api` acts as the system-of-record orchestrator.

**Data Pipelines & Synchronization:**

- Asynchronous Celery/Redis-style queues route capture events.
- Synchronization logic implemented on mobile capture handles network drop-outs by buffering and securely flushing payloads when connectivity resumes.

## Operational Reliability

We are engineering for environments where networks fail, devices overheat, and data gets dropped.

**Resilience Mechanisms:**

- Offline capture buffering at the edge client (`clients/android-capture-dat`) to maintain data integrity during WiFi disconnections.
- Idempotent API endpoints ensure no duplicate processing if edge devices retry failed uploads.

**Monitoring & Incident Recovery:**

- Rapid detection of "dead letters" or stalled AI processing pipelines.
- Synthetic smoke tests (`./scripts/compose-smoke.sh`) run continuously against deployment endpoints to guarantee end-to-end integration viability.
- Automated failover strategies across worker instances in case of GPU exhaustion or container faults.

## Risks & Tradeoffs

- **Operational Risks:** Relying on unreleased or volatile Meta SDK endpoints might cause abrupt breakage in the `android-capture-dat` client.
- **Scaling Limitations:** Processing multimodal video/audio streams requires substantial GPU capacity which introduces high scaling costs. CPU/Mock execution reduces testing costs but masks real-world latency profiles until pilot execution.
- **Deployment Risks:** Regulatory constraints (G2 gate) heavily gate any live testing, leading to a risk of optimizing too deeply against synthetic instead of real data workflows.
- **Security Concerns:** The handling of sensitive student PII necessitates strict auditing mechanisms and complicates rapid prototyping without robust synthetic data strategies.

## Agile Sprint Plan

Operating as an elite embedded engineering team tracking towards a pilot launch.

- **Sprint 1 (Infrastructure Foundation):** Cement Docker Compose Dev stack, finalize `dev-verify.sh`, and stabilize the FastAPI core backend and worker-scaffolding endpoints.
- **Sprint 2 (Edge-to-Cloud Integration):** Implement Meta Wearable DAT client endpoints, establishing robust offline-buffering and telemetry synchronization against the API.
- **Sprint 3 (AI Pipeline Instantiation):** Activate asynchronous Python workers for `asr` and `cv`. Deploy synthetic evaluation to ensure inference pipelines accurately parse mock data (`mock_capture.py`).
- **Sprint 4 (Operational Scale & Security Audit):** End-to-end staging deployment, simulated high-traffic capture sessions, PII data isolation tests, and finalize go-live metrics.
