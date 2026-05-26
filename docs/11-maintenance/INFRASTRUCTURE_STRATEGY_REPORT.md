# PedagogyX Infrastructure Strategy Report

**Status:** Draft / Active Strategy
**Author:** Autonomous Senior DevOps Engineer & Platform Infrastructure Architect
**Context:** Phase 0 / MVP Preparation, aligning with OSS-first, self-hosted, central inference architecture.

## Infrastructure Overview

- **Current Architecture:** PedagogyX operates on a Hybrid Edge-Cloud (D-PROC=C) architecture. It consists of thin clients (Meta Ray-Ban Android DAT and Windows Smartboards) that capture A/V and upload to an edge/LAN ingest buffer. This buffer forwards chunks over WAN to a central, OSS-first inference backend hosted in an India-based cloud.
- **Environment Topology:**
  - _Local/Dev:_ Managed via Docker Compose (`infra/compose.dev.yaml`), featuring PostgreSQL, Redis, MinIO, API, Next.js web shell, and worker stubs (ASR/metrics).
  - _Edge:_ District/school edge node for stream buffer and offline resilience.
  - _Cloud (India):_ Central PedagogyX OSS backend handling batch/hot-path jobs with MediaMTX, GPU workers (faster-whisper, YOLO with TensorRT, Ollama), PostgreSQL, and MinIO.
- **Deployment Model:** Containerized microservices. Core infrastructure is structured for reproducibility and declarative management.
- **Operational Goals:** Ensure maximum reliability, seamless data capture across intermittent LAN/WAN boundaries, strict compliance with India DPDP privacy laws, zero proprietary cloud API dependencies, and scalability across large-scale K-12 deployment endpoints.

## CI/CD Architecture

- **Pipeline Structure:** GitHub Actions handles CI automation (e.g., `.github/workflows/test.yml`, `dev-verify.yml`). It runs Python backend testing (`pytest`) and Next.js frontend testing (`vitest`), as well as markdown linting (`markdownlint` and `prettier`).
- **Automation Strategy:** Enforce declarative, immutable infrastructure. All merges to `main` undergo automated test suites, linting (Ruff for Python, Prettier for markdown), and build validations.
- **Deployment Flow:** Moving towards GitOps (e.g., ArgoCD) for syncing cloud states with the repository configuration. E2E tests mock production traffic using synthetic sessions (`tools/mock-capture/mock_capture.py`).
- **Rollback Mechanisms:** Container tagging and versioned Helm charts will ensure single-click rollback capabilities. Database migrations are strictly versioned to prevent state drift during rollbacks.

## Cloud Infrastructure

- **Cloud Services:** Bare-metal or IaaS VMs in an India data center for data residency compliance. FOSS infrastructure stack is used instead of managed proprietary services to strictly limit lock-in and vendor costs.
- **Networking:** Hub-and-spoke VPC model. Edge nodes connect via secure TLS/VPN tunnels. Internal microservices communicate over isolated private subnets.
- **Infrastructure Layout:**
  - _Ingress:_ NGINX/HAProxy API gateways and MediaMTX for streaming.
  - _Compute:_ Auto-scaling GPU VM pools for inference, CPU pools for Next.js web and API servers.
  - _Storage:_ MinIO for S3-compatible cold object storage, PostgreSQL 16+ for relational state.
- **Scaling Architecture:** Horizontal scaling of API and worker nodes via queue length metrics (Redis/Celery). GPU scaling is optimized for 12GB VRAM class limits (RTX 5070 profile).

## Kubernetes Architecture

- **Cluster Topology:** High-availability control plane distributed across multiple availability zones within the India region. Dedicated node pools for GPU-intensive workloads and CPU-bound microservices.
- **Deployment Strategy:** Declarative Helm charts and Kustomize manifests managed via GitOps. Immutable container images pushed to a private registry.
- **Autoscaling:** HPA (Horizontal Pod Autoscaler) based on CPU/Memory and custom metrics (e.g., Redis queue backlog for ASR and YOLO jobs). Cluster Autoscaler to provision additional GPU nodes during peak school hours.
- **Ingress Architecture:** NGINX Ingress Controller with cert-manager for automated TLS provisioning. WebRTC streaming requires specific UDP port exposure optimized at the edge.

## Observability Stack

- **Metrics:** Prometheus for scraping system, application, and infrastructure metrics. Node Exporter and cAdvisor for host/container level visibility. GPU metrics collected via NVIDIA DCGM Exporter.
- **Logging:** Promtail + Loki + Grafana (PLG stack) or OpenSearch for centralized log aggregation. Structured JSON logging enforced across API and workers.
- **Tracing:** OpenTelemetry instrumentation within FastAPI and Next.js apps to map distributed trace contexts, especially across asynchronous Celery/Redis task queues.
- **Alerting:** Alertmanager configured for critical thresholds (e.g., failed uploads, GPU queue starvation, high worker latency, DB connection drops). Alerts routed to PagerDuty/Slack.

## Security Architecture

- **IAM:** Strict Role-Based Access Control (RBAC) enforced. Administrative Supervision Mode maps permissions hierarchically (Teacher, Coach, School Admin, District Admin). Least-privilege service accounts for Pods.
- **Secret Management:** Secrets managed via External Secrets Operator integrating with HashiCorp Vault. No credentials committed to source code.
- **Network Security:** Network Policies enforce default-deny ingress/egress. Zero Trust principles applied inside the cluster. TLS 1.3 enforced for all WAN transit.
- **Vulnerability Management:** Automated container scanning (Trivy) in CI/CD. Continuous dependency auditing for Python/Node ecosystem (Dependabot/Renovate).

## Reliability Strategy

- **Redundancy:** Multi-replica deployments for stateless APIs. PostgreSQL deployed with synchronous streaming replication (primary-standby). MinIO configured in distributed mode with erasure coding.
- **Failover:** Automated leader election for DBs and Redis. Stateless apps self-heal via Kubernetes deployment replica health checks.
- **Disaster Recovery:** Automated daily volume snapshots and continuous WAL archiving for PostgreSQL to secure off-site object storage. Disconnected edge buffer guarantees no data loss during WAN outages.
- **Self-Healing Mechanisms:** Liveness and Readiness probes configured for all containers. Circuit breakers and retries built into the upload API to handle network flakiness from edge clients.

## Cost Optimization

- **Infrastructure Savings:** Utilizing central OSS compute instead of per-classroom smartboard GPUs (reducing edge hardware budget to ₹0). Utilizing spot instances for batch (cold path) processing tasks where feasible.
- **Resource Optimization:** Consolidating inference into efficient multi-model streams (batching YOLO inference natively). Strict CPU/RAM limits set via Kubernetes ResourceQuotas to prevent noisy neighbors.
- **Scaling Efficiency:** Scale-to-zero capabilities for GPU nodes during nights/weekends (non-school hours). Caching aggregated analytics at the Redis layer to minimize repeated database queries.

## Risks & Bottlenecks

- **Operational Risks:** Hybrid Edge-Cloud management complexity. Ensuring edge nodes (LAN buffers) remain reliable and sync successfully under variable local power/network conditions.
- **Scaling Limitations:** GPU availability in the India region. As capture volume scales, the asynchronous queue processing (faster-whisper/YOLO) could bottleneck if auto-scaling bounds are reached.
- **Security Risks:** Deep integration with Ray-Ban Android DAT requires strict sandbox boundaries on the host Android device. Handling PII (student data) necessitates zero-trust compliance prior to G2 sign-off.
- **Deployment Risks:** Rollouts touching stateful schema changes. Database migrations require careful backward-compatible execution to ensure zero downtime.

## Agile Sprint Plan

- **Implementation Phases:**
  - _Phase 1 (Sprint 03/04):_ Finalize foundational DevOps infra (Terraform for Cloud, Kubernetes baseline). Setup robust CI validation. Validate RTX 5070 cost models and E2E E2E pipeline for Android DAT.
  - _Phase 2 (Sprint 05):_ Deploy Observability stack (Prometheus/Grafana). Instrument FastAPI/Workers with OpenTelemetry.
  - _Phase 3 (Sprint 06):_ Implement production GitOps workflow. Harden security policies, NetworkPolicies, and Vault integration.
- **Priorities:** 1. Reproducible Infrastructure (IaC), 2. Observability Basics, 3. Autoscaling configuration for GPU/workers.
- **Milestones:**
  - Milestone A: E2E capture from DAT uploaded to a fully automated cloud backend with functional ASR/worker stubs.
  - Milestone B: Production-ready Kubernetes cluster provisioned entirely via code.
- **Expected Operational Improvements:** Transitioning from manual `docker compose` to a fully automated, scalable, reliable cloud-native footprint, significantly reducing developer friction and accelerating Phase 1 readiness.
