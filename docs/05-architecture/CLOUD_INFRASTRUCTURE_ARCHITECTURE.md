# Cloud Infrastructure Architecture (v0.2)

**Status:** Draft — Implementation of Hybrid D-PROC (ADR-0008)
**Owner:** Cloud Infrastructure Architecture
**Date:** 2026-05-20

## Cloud Problem Analysis

- **Business Requirements:** Deliver a multimodal AI classroom intelligence platform prioritizing India data residency (DPDP compliance), K-12/University segment operations, and complete operational self-sufficiency without proprietary cloud APIs (ADR-0005). Must support massive-scale inference via OSS models.
- **Scale Assumptions:** Must seamlessly scale to district-wide deployments (10,000+ simultaneous streams). Assumes multiple K-12 classrooms pushing concurrent video streams (480p/720p) and audio simultaneously. Requires dynamic scaling of distributed worker pools under high load.
- **Operational Constraints:** Total customer hardware budget is ₹0 (D-10). Cloud processing must remain intensely cost-efficient and run on generic hardware or highly optimized cloud GPU instances (RTX 5070 equivalent or Data Center GPU alternatives). High dependency on local network (2-15 Mbps) for K-12 classroom environments limits synchronous real-time cloud capabilities, necessitating a Hybrid Edge-Cloud architecture.
- **Failure Scenarios:** Unstable classroom internet, frequent edge node disconnections, total regional ISP failures, local power outages, instance termination, container runtime crashes, and potential central pool GPU exhaustion. We must design for failure at every tier.

## Cloud Architecture

- **Infrastructure Topology:** Hub-and-Spoke model mapping distributed Edge nodes (LAN ingest points at schools) into a central AWS `ap-south-1` (Mumbai) region or equivalent FOSS VPS infrastructure.
- **Cloud Services:**
  - **Compute:** Kubernetes (EKS or pure k3s/RKE2) for container orchestration, scaling stateless API and worker pods dynamically. Dedicated GPU node groups (e.g., NVIDIA L4/T4 or bare metal RTX 5070 equivalents) for cold-path ML evaluation.
  - **Storage:** S3-compatible Object Storage (MinIO) for immutable, chunked media storage. Managed PostgreSQL (or clustered Patroni) for state, metadata, and pedagogy scores.
  - **Messaging:** High-throughput event streaming via Kafka (or RabbitMQ) for decoupled, reliable message queuing and task distribution.
- **Networking:** Multi-tier VPC structure isolating Edge ingestion (DMZ) from internal ML processing and persistence layers.
- **Deployment Layout:** Multi-AZ Kubernetes worker pools ensuring fault tolerance. Strict decoupling of web/ingest tiers from async ML inference workers.

## Infrastructure Automation

- **IaC Strategy:** Fully declarative infrastructure via Terraform (or Pulumi). State stored securely in a centralized backend with state locking and versioning.
- **Provisioning Workflows:** Automated base AMIs and node images built via Packer to eliminate infrastructure drift and ensure rapid node bootstrapping.
- **Deployment Automation:** GitOps driven deployments using ArgoCD. Infrastructure and application states are perfectly mirrored in Git.
- **Environment Management:** Explicitly defined environments (`dev`, `staging`, `prod`) driven by strictly separated parameter files. Complete environment reproducibility from code.

## Networking Architecture

- **VPC Layout:** Isolated VPC in `ap-south-1` with public subnets for Ingress Controllers/API Gateways, and private subnets for DB, Queue, and GPU Workers. No direct internet access for backend workloads.
- **Ingress/Egress:** Cloudflare (or NGINX/HAProxy FOSS equivalent) protecting public endpoints with WAF. Strict NAT Gateways egress traffic from private subnets.
- **Load Balancing:** Layer 7 HTTP/gRPC ingress routing WebRTC traffic and API requests dynamically to healthy ingest pods.
- **DNS Strategy:** Global Anycast DNS routing for low latency resolution with geo-fencing policies for India localization to enforce data sovereignty.

## Reliability Strategy

- **Failover Systems:** Cross-AZ deployments for critical control plane components (Postgres, Kafka, API).
- **Redundancy:** Multi-node replication for Postgres (Patroni). MinIO cluster with strict erasure coding.
- **Disaster Recovery:** Automated daily volume snapshots and continuous Write-Ahead Log (WAL) archiving for Postgres to offsite, immutable object storage. Defined RTO of < 1 hour and RPO of < 15 mins.
- **Self Healing Mechanisms:** Kubernetes auto-scaling groups tied to node health checks; automatic pod eviction and rescheduling of orphaned ML tasks from dropped instances. Circuit breakers on API endpoints.

## Security Architecture

- **IAM:** Principle of least privilege enforced via IAM roles and Kubernetes RBAC. Edge nodes authenticate via mutual TLS (mTLS) or strictly scoped short-lived JWTs.
- **Encryption:** TLS 1.3 everywhere in transit. AES-256 server-side encryption for MinIO and Postgres volumes at rest.
- **Secrets Management:** HashiCorp Vault for dynamic credential injection and rotation. Absolutely no static secrets in source code, CI, or ConfigMaps.
- **Network Security:** Zero-trust principles with strictly restricted Security Groups and Kubernetes Network Policies limiting intra-cluster lateral movement.

## Observability

- **Monitoring:** Prometheus stack polling metrics from all cloud services, Kubernetes nodes, and remote Edge nodes.
- **Logging:** FluentBit/Promtail gathering structured JSON logs into Loki or Elasticsearch for centralized indexing, searching, and anomaly detection.
- **Tracing:** OpenTelemetry (OTel) instrumented across Edge proxies, API Gateways, and Worker daemons to trace the complete lifecycle of video/audio chunks.
- **Alerting:** Alertmanager routing actionable, critical failures (e.g., `Queue Backlog > 1hr`, `Node Offline`, `GPU OOM`) to PagerDuty/Slack. Low alert fatigue by tuning thresholds.

## Performance & Cost Optimization

- **Autoscaling:** KEDA (Kubernetes Event-driven Autoscaling) scaling GPU workers predictively and reactively based on Kafka queue depth. Scale-to-zero capabilities for ML workers during K-12 off-hours (nighttime in India).
- **Resource Optimization:** Right-sizing cloud instances. Priority use of Spot/Preemptible GPU instances for cold path tasks given their asynchronous, batch nature to slash compute costs by up to 70%.
- **Caching:** Redis-backed caching for frequent API lookups, session state, and dashboard metadata.
- **Infrastructure Efficiency:** Aggressive automated garbage collection of processed media chunks post-retention window via MinIO lifecycle policies.

## Risks & Tradeoffs

- **Operational Risks:** Hybrid Edge/Cloud synchronization failure causing data loss. Requires extreme care in resumable upload logic and local buffer management on Android/Windows clients.
- **Scaling Concerns:** Cloud GPU scarcity in specific regions or sudden spikes in processing queues blocking authoritative scoring SLAs.
- **Vendor Tradeoffs:** Prioritizing FOSS tools (MinIO, Postgres, Kafka) over managed cloud services increases operational management overhead but guarantees absolute compliance, portability, and eliminates vendor lock-in.
- **Cost Implications:** While the customer budget is ₹0, the central architecture runs high inherent costs due to GPU compute and WAN egress. Needs constant optimization via intelligent batching and Spot instance utilization.

## Agile Sprint Plan

- **Milestones:**
  1. Complete Cloud Base Architecture mapping and GitOps strategy.
  2. Implement Terraform IaC for `staging` VPC, EKS/k3s, and networking.
  3. Deploy base control plane (Postgres, MinIO, Kafka) via ArgoCD.
  4. Integrate comprehensive observability stack (Prometheus, OTel, Vault).
- **Implementation Phases:**
  - Sprint 03: Establish IaC repository and CI/CD pipelines. Stand up Cloud VPC and Kubernetes clusters.
  - Sprint 04: Deploy Core Data, Secrets Management, and Queuing Services.
  - Sprint 05: Establish Edge-to-Cloud mTLS connection, Ingress, and Observability tracing.
- **Priorities:** Base networking security, automated provisioning, secrets management, and reliable queuing before any GPU compute is provisioned.
- **Expected Infrastructure Improvements:** Transition from local/dev mockups into a highly scalable, reproducible, secure, and compliant cloud foundation ready to ingest Edge data globally.
