# Infrastructure Baseline Report (Phase 0)

**Status:** Draft
**Owner:** Architecture
**Date:** 2026-05-19
**Context:** Initial baseline assessment generated upon activation of the Senior DevOps Engineer persona, based on `SYSTEM_ARCHITECTURE.md` (v0.4) and `CENTRAL_OSS_BACKEND_SPEC.md`.

---

## Infrastructure Overview

- **Current architecture:** Hub-and-spoke model. Thin clients (Android/Windows) in classrooms capture audio/video. A LAN Edge Node (D-PROC hybrid) buffers and ingests the data. The data is then transmitted over WAN to a Central OSS Backend in an India cloud region (ap-south-1).
- **Environment topology:**
  - `dev`: Founder RTX 5070
  - `staging`: Cloud VPS + 1 GPU
  - `prod`: Cloud VPS + auto-scaled GPU workers
- **Deployment model:** Edge Nodes pull Docker container images via watchtower/managed fleet operator. Central backend deployed via Kubernetes/Docker Swarm (TBD based on scale, currently containerized).
- **Operational goals:** Zero customer hardware budget (D-10), strict OSS-first approach (no proprietary APIs), India data residency (DPDP compliance), and tolerance for weak school internet (5-15 Mbps).

## CI/CD Architecture

- **Pipeline structure:** GitHub Actions building Docker images.
- **Automation strategy:** Automated builds on commit. `.github/workflows/dev-verify.yml` for linting.
- **Deployment flow:** Edge nodes pull new container tags automatically or via managed fleet operators.
- **Rollback mechanisms:** Immutable container tags. Edge nodes support graceful fallback to the previous known-good image on health check failure.

## Cloud Infrastructure

- **Cloud services:** India-based ap-south-1 Virtual Private Cloud (VPC) to meet DPDP compliance.
- **Networking:** Secure tunnels from multiple Edge Nodes to the central VPC. API Gateway / Load balancer handles ingress.
- **Infrastructure layout:** MediaMTX cluster for media ingest. MinIO (S3-compatible) for chunked storage. PostgreSQL for metadata and pedagogy scores. Redis for signaling. RabbitMQ/Kafka for message queuing.
- **Scaling architecture:** CPU workers auto-scale on ingest load. GPU workers scale based on cold-path queue depth.

## Kubernetes Architecture

- **Cluster topology:** (Planned/Recommended) Central cloud cluster for backend microservices (API, ML Workers, Ingest Gateway).
- **Deployment strategy:** Declarative manifests / Helm charts for stateless workers. Stateful sets for MinIO and Postgres (or managed equivalents if permitted by budget).
- **Autoscaling:** Horizontal Pod Autoscaler (HPA) configured on CPU metrics for ingest gateways, and custom metrics (queue length) for ML GPU workers.
- **Ingress architecture:** NGINX Ingress or similar handling API Gateway duties, terminating TLS, and routing WebRTC/RTSP and REST traffic.

## Observability Stack

- **Metrics:** Prometheus collecting node, container, and application metrics.
- **Logging:** Centralized logging (e.g., Loki or ELK) aggregating logs from Edge Nodes and Central Backend.
- **Tracing:** OpenTelemetry (OTel) tracing distributed requests across Capture Agent -> Edge Node -> Central Backend.
- **Alerting:** Grafana alerts configured for edge node disconnection, queue backlog > 1 hour, and GPU Out-Of-Memory (OOM) errors.

## Security Architecture

- **IAM:** Keycloak for Role-Based Access Control (RBAC) (Teacher, Coach, Admin).
- **Secret management:** Sealed secrets in GitOps, injected securely into containers. No sensitive keys stored on Edge Nodes.
- **Network security:** mTLS between Edge and Central Backend. Strict network policies isolating namespaces in the central cluster.
- **Vulnerability management:** Container scanning integrated into CI pipelines. Automated dependency updates.

## Reliability Strategy

- **Redundancy:** Central Postgres in High Availability (HA) mode. MinIO erasure coding for durable object storage.
- **Failover:** Cloud fallback available if Edge Node hardware fails (subject to WAN bandwidth limits).
- **Disaster recovery:** Automated backups of Postgres and MinIO metadata to isolated cold storage.
- **Self healing mechanisms:** Edge nodes cache encrypted chunks locally (up to 2GB). If central goes down, edge buffers and resumes upon recovery with exponential backoff.

## Cost Optimization

- **Infrastructure savings:** Strict reliance on FOSS (faster-whisper, YOLO, Qwen) avoids costly proprietary APIs.
- **Resource optimization:** Splitting into Hot Path (lightweight CPU/proxy models) and Cold Path (heavy GPU models) maximizes utilization of expensive GPU hours.
- **Scaling efficiency:** GPU workers process heavy models sequentially per stream to respect VRAM limits (12GB baseline), scaling only when the batch queue demands it.

## Risks & Bottlenecks

- **Operational risks:** Hardware failure of the LAN Edge Node at physical school locations.
- **Scaling limitations:** The central GPU pool is the primary cost bottleneck; batch processing introduces latency for authoritative scores.
- **Security risks:** Physical access to Edge Nodes in schools requires full disk encryption and short-lived tokens.
- **Deployment risks:** School firewalls blocking required ports (WebRTC/RTSP) necessitates fallback mechanisms (HTTPS chunked upload).

## Agile Sprint Plan

- **Implementation phases:**
  - Sprint 02 (Current): Spin up Cloud VPC, Postgres, MinIO. Stand up MediaMTX.
  - Sprint 03: Develop Python ML worker daemon. Integrate with Ollama and faster-whisper.
  - Sprint 04: Edge node Docker Compose profile validation. End-to-end test with mock Agent.
- **Priorities:** Validate edge-to-cloud ingress and storage layers before optimizing ML workers.
- **Milestones:** E2E system functional in `staging` by end of Sprint 04.
- **Expected operational improvements:** Establishing the baseline deployment capability and verifying the hybrid edge-cloud architecture under constrained network conditions.
