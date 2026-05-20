# Central OSS Backend Specification (S01-11)

**Status:** Draft — Implementation of Hybrid D-PROC (ADR-0008)
**Owner:** Architecture
**Date:** 2026-05-19

---

## Operational Problem Analysis

- **Business Context:** PedagogyX requires an India-first, multimodal real-time supervision platform for K-12 and university segments. The founder mandated zero customer hardware budget (D-10) and an OSS-first approach (ADR-0005).
- **Workflow Analysis:** Classrooms have low-end clients (Android/Windows) and weak internet (5-15 Mbps). Teachers cannot be burdened with complex setups. Principals need reliable, automated pedagogy index scores.
- **Bottlenecks:** Centralizing all raw video processing from hundreds of schools creates massive WAN bandwidth bottlenecks and single points of failure.
- **Operational Constraints:** Strict data privacy (India DPDP) requiring localized storage. Hybrid D-PROC (ADR-0008) dictates LAN edge ingest but central cloud GPU analytics.

## System Architecture

- **Major Components:**
  - **Capture Agent:** Thin client (Android/Windows) pushing chunks/streams.
  - **LAN Edge Node (Buffer/Ingest):** District/school-hosted lightweight server (NUC/mini-PC).
  - **Central OSS Backend (India Cloud):** Ingestion Gateway, ML Worker Pool, Data Store.
- **Integrations:**
  - Edge Node synchronizes with Central API for authorization and stream registration.
  - WebRTC (hot path) and Resumable Chunk Upload (cold path).
- **Data Flow:**
  - Agent -> Edge Node (Local LAN, high speed).
  - Edge Node -> Central Backend (WAN, asynchronous or real-time relayed).
  - Central Backend -> Hot Path (Preview Dashboards) & Cold Path (Authoritative Score DB).
- **Infrastructure Topology:** Hub-and-spoke. Multiple Edge Nodes securely tunnel to a central ap-south-1 Virtual Private Cloud (VPC).

## Deployment Strategy

- **Rollout Plan:**
  1. Internal validation on single Edge Node mock.
  2. Pilot deployment in one school archetype (K-12).
  3. Scale to district-level rollout.
- **Environments:** `dev` (Founder RTX 5070), `staging` (Cloud VPS + 1 GPU), `prod` (Cloud VPS + auto-scaled GPU workers).
- **CI/CD:** GitHub Actions building Docker images. Edge nodes pull images via watchtower or managed fleet operator.
- **Rollback Mechanisms:** Immutable container tags. Edge nodes support graceful fallback to previous known-good image on health check failure.

## Infrastructure Design

- **Cloud Architecture:**
  - **Ingress:** API Gateway / Load Balancer.
  - **Media Ingest:** MediaMTX cluster.
  - **Storage:** MinIO (S3-compatible) for video/audio chunks; PostgreSQL for metadata and pedagogy scores.
  - **Message Broker:** Redis for real-time signaling; RabbitMQ/Kafka for cold-path batch jobs.
- **Scaling Model:** CPU workers auto-scale on ingest load. GPU workers (RTX series or equivalent cloud GPUs) scale based on cold-path queue depth.
- **Observability:** Prometheus + Grafana. OpenTelemetry (OTel) tracing across Agent -> Edge -> Central.
- **Security:** mTLS between Edge and Central. AES-256 encryption at rest in MinIO. Keycloak for RBAC.

## AI System Design

- **Models (OSS):**
  - Audio: `faster-whisper` (medium/large-v3).
  - CV: `YOLO11n` (TensorRT optimized for 480p/720p).
  - LLM: `Qwen2.5-7B-Instruct` Q4 via Ollama.
- **Retrieval Systems:** Postgres vector extension (pgvector) for coaching tips and historical pedagogy index comparisons.
- **Orchestration:** Custom Python worker daemon pulling from RabbitMQ.
- **Inference Strategy:**
  - Hot path executes lightweight proxies (audio VAD, simple YOLO).
  - Cold path executes full heavy models sequentially per stream to respect GPU VRAM limits (12GB baseline).

## Integration Plan

- **APIs:** RESTful control plane APIs. WebSocket for real-time live dashboard telemetry.
- **Services:** External integration with School Information Systems (SIS) deferred to Phase 2.
- **Data Pipelines:**
  - Sync Service (cross-correlating audio/video timestamps).
  - Transcoding Service (normalizing variable framerate uploads).
- **Synchronization:** Master clock derived from the audio stream (RFC-0002).

## Operational Reliability

- **Failover Systems:** Central Postgres in High Availability (HA) mode. MinIO erasure coding.
- **Monitoring:** Alerts on edge node disconnection, queue backlog > 1 hour, and GPU OOM errors.
- **Incident Recovery:** Edge nodes cache encrypted chunks locally (up to 2GB). If central goes down, edge buffers and resumes when central recovers.
- **Resilience Mechanisms:** Exponential backoff on all client and edge-to-cloud communications.

## Risks & Tradeoffs

- **Operational Risks:** Edge node hardware failure at the school. (Mitigation: Cloud fallback if WAN allows).
- **Scaling Limitations:** Central GPU pool is expensive. Relying on batch processing introduces latency for authoritative scores.
- **Deployment Risks:** School firewall blocking WebRTC/RTSP ports. (Mitigation: Fallback to HTTPS chunked upload only, degrading hot path).
- **Security Concerns:** Physical access to the Edge Node at the school. (Mitigation: Full disk encryption, no sensitive keys stored, only short-lived tokens).

## Agile Sprint Plan

- **Implementation Phases:**
  - Sprint 02: Spin up Cloud VPC, Postgres, MinIO. Stand up MediaMTX.
  - Sprint 03: Develop Python ML worker daemon. Integrate with Ollama and faster-whisper.
  - Sprint 04: Edge node Docker Compose profile validation. End-to-end test with mock Agent.
- **Deployment Milestones:** E2E system functional in `staging` by end of Sprint 04.
- **Operational KPIs:**
  - Time-to-insight (M-B): Target < 30 mins for cold path.
  - Uptime of Edge-to-Central sync: Target 99.9%.
- **Expected Impact:** Unlocks the capability to securely process multi-stream video from schools while respecting the founder's strict OSS and cost constraints.
