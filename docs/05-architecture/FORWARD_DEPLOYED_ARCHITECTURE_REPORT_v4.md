# Forward Deployed Architecture Report v4

## Operational Problem Analysis

- **Business Context:** PedagogyX aims to analyze classroom sessions using multimodal AI (voice, video, slides, engagement) to measure pedagogical efficiency.
- **Workflow Analysis:** Teachers operate in dynamic classroom environments. Our v1 client utilizes Meta Ray-Ban glasses via Android DAT to capture ongoing sessions seamlessly, minimizing operational friction.
- **Bottlenecks:** The primary operational bottleneck is the current legal block on production school data (pending G2 India legal sign-off), forcing reliance on synthetic data. Additionally, handling high-bandwidth multimodal capture in real-world, unreliable school networks poses a significant data ingestion challenge.
- **Operational Constraints:** Deployments must account for limited network connectivity and edge device constraints. The separation between real-time inference (Hot Path) and batch processing (Cold Path) must be handled gracefully to ensure operators still receive actionable insights within acceptable timeframes.

## System Architecture

- **Major Components:**
  - Edge Capture Client (Meta Ray-Ban via Android DAT).
  - API Gateway and Core Backend (FastAPI).
  - Frontend Web Dashboard (React, Next.js).
  - Central OSS Offline Inference Backend.
  - Microservices: `worker-asr`, `worker-cv`, `worker-metrics`.
- **Integrations:** Meta Wearables DAT SDK integration for hardware-level capture. Event-driven message broker to bridge FastAPI with backend AI worker nodes.
- **Data Flow:** Multimodal data is captured at the edge (Ray-Ban glasses), sent to the Android DAT client, and synchronized via FastAPI to the backend. It is then bifurcated: immediate CV analysis (YOLO) via the Hot Path, and deferred complex multimodal analysis (faster-whisper, Ollama) via the Cold Path.
- **Infrastructure Topology:** Centralized, on-prem/cloud hybrid designed for offline OSS inference to guarantee data privacy and handle network disconnections gracefully.

## Deployment Strategy

- **Rollout Plan:**
  - Phase 1: Internal synthetic data validation (Sprint 03 MVP).
  - Phase 2: Limited pilot deployments (post-G2 sign-off).
  - Phase 3: Broad institutional rollout.
- **Environments:** Local Docker Compose for development (`compose.dev.yaml`), staged cloud environments for UAT, and production-ready Kubernetes/hybrid clusters for central processing.
- **CI/CD:** Automated verification pipelines utilizing GitHub Actions (`.github/workflows/dev-verify.yml`) to enforce code quality (`ruff`, `mypy`, `markdownlint`, `prettier`).
- **Rollback Mechanisms:** Blue/Green deployments for API and frontend. Immutable worker container versioning to allow instant reversion of faulty inference paths.

## Infrastructure Design

- **Cloud Architecture:** Scalable, centralized compute capable of hosting intensive OSS offline inference models. Designed for GPU optimization (handling until RTX 5070 limitations and scaling out horizontally).
- **Scaling Model:** Asynchronous worker scaling. Web and API tiers scale based on HTTP load, whereas ASR/CV/Metrics workers scale based on queue depth to optimize GPU/CPU utilization.
- **Observability:** Centralized logging, distributed tracing across Hot and Cold paths, and operational dashboards monitoring capture success rates, network dropouts, and inference latency.
- **Security:** Strict separation of synthetic vs. production data. End-to-end encryption for edge-to-cloud synchronization. Role-based access control and compliance with impending G2 requirements.

## AI System Design

- **Models:**
  - Hot Path: YOLO for real-time engagement and computer vision metrics.
  - Cold Path: faster-whisper for accurate ASR, Ollama for advanced pedagogical reasoning.
- **Retrieval Systems:** Knowledge graph and RAG optimizations for long-term session context retrieval and educational insights.
- **Orchestration:** Event-driven architecture managing pipeline dependencies between speech-to-text, vision, and NLP consolidation.
- **Inference Strategy:** Centralized OSS backend to strictly maintain data ownership and reduce recurring API costs. Optimization for batch processing off-peak to manage hardware budget.

## Integration Plan

- **APIs:** RESTful endpoints via FastAPI for capture synchronization, metadata management, and client state orchestration.
- **Services:** Inter-service communication via message queues connecting API layer to `worker-asr`, `worker-cv`, and `worker-metrics`.
- **Data Pipelines:** Resilient synchronization pipelines that buffer capture data on the Android DAT client during network outages and flush upon reconnection.
- **Synchronization:** Conflict-free delta sync for classroom metrics, ensuring dashboards (Next.js) reflect accurate aggregations once Cold Path processing concludes.

## Operational Reliability

- **Failover Systems:** Stateless API design allowing rapid container rescheduling. Offline-first client architecture ensures capture continues even if the central API goes down.
- **Monitoring:** Proactive monitoring of edge connectivity, model hallucination rates, processing lag, and hardware utilization on central inference nodes.
- **Incident Recovery:** Automated alerting on queue stagnation. Documented runbooks for resetting stalled worker states without data loss.
- **Resilience Mechanisms:** Circuit breakers between FastAPI and AI workers. Retry logic with exponential backoff on the Android DAT client.

## Risks & Tradeoffs

- **Operational Risks:** Delays in G2 sign-off could prolong reliance on synthetic data, risking mismatch with real-world complexities.
- **Scaling Limitations:** Centralized OSS inference is cost-effective and private but requires significant upfront hardware provisioning and active queue management.
- **Deployment Risks:** Physical constraints and hardware reliability of Meta Ray-Ban glasses in diverse classroom environments.
- **Security Concerns:** Handling highly sensitive PII (children in classrooms) necessitates flawless execution of the Cold Path data isolation and eventual legal compliance guardrails.

## Agile Sprint Plan

- **Implementation Phases:**
  - Sprint 1-2: Establish boilerplate, edge capture mechanics, and mock API sync.
  - Sprint 3 (Current): Validate MVP pipeline with synthetic data (G0 complete).
  - Sprint 4: Harden AI orchestration between Hot and Cold paths.
- **Deployment Milestones:** Complete end-to-end DAT capture simulation (`make dat-session`); fully verify central OSS offline inference backend on dev GPUs.
- **Operational KPIs:** End-to-end latency for Hot Path (< 2s), capture success rate (> 99%), and 0% PII leakage into unauthorized environments.
- **Expected Impact:** Deliver a production-ready, highly observable pipeline that proves the technical validity of the PedagogyX multimodal architecture ahead of the G2 legal milestone.
