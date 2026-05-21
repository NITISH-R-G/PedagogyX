# Cloud Infrastructure Architecture (v0.1)

**Status:** Draft — Implementation of Hybrid D-PROC (ADR-0008)
**Owner:** Cloud Infrastructure Architecture
**Date:** 2026-05-20

---

## Cloud Problem Analysis

- **Business Requirements:** Deliver a multimodal AI classroom intelligence platform prioritizing India data residency, K-12/University segment operations, and complete operational self-sufficiency without proprietary cloud APIs (ADR-0005).
- **Scale Assumptions:** Must scale to district-wide deployments seamlessly. Assumes multiple K-12 classrooms pushing concurrent video streams (480p/720p) simultaneously, necessitating significant parallel processing and robust ingestion points.
- **Operational Constraints:** Total customer hardware budget is ₹0 (D-10). Cloud processing must remain intensely cost-efficient. High dependency on local network (5-15 Mbps) for K-12 classroom environments limits synchronous real-time cloud capabilities.
- **Failure Scenarios:** Unstable classroom internet, frequent edge node disconnections, total regional ISP failures, local power outages, and potential central pool GPU exhaustion.

## Cloud Architecture

- **Infrastructure Topology:** Hub-and-Spoke model mapping distributed Edge nodes (LAN ingest points at schools) into a central AWS `ap-south-1` region (or equivalent localized FOSS VPS).
- **Cloud Services:**
  - Compute: Scalable Virtual Machines for generic processing (API/Queues) with dedicated GPU instances (12GB VRAM class) for cold-path ML evaluation.
  - Storage: S3-compatible Object Storage (MinIO) for immutable, chunked media; PostgreSQL (managed or clustered) for state, metadata, and pedagogy scores.
  - Messaging: High-throughput broker (RabbitMQ or Kafka) for reliable message queuing.
- **Networking:** Multi-tier VPC structure isolating Edge ingestion (DMZ) from internal ML processing and persistence layers.
- **Deployment Layout:** Stateless worker pools spanning availability zones to ensure fault tolerance. Decoupled ingest vs. inference modules.

## Infrastructure Automation

- **IaC Strategy:** Fully declarative infrastructure via Terraform (or Pulumi). State stored securely in centralized backend with state locking.
- **Provisioning Workflows:** Automated base AMIs built via Packer to eliminate drift and ensure rapid instance scaling.
- **Deployment Automation:** GitOps driven deployments (ArgoCD or Flux) reacting to container image updates on main branch tags.
- **Environment Management:** Explicitly defined environments (`dev`, `staging`, `prod`) driven by strictly separated parameter files. Founder dev occurs on local RTX 5070; cloud mimics target architecture.

## Networking Architecture

- **VPC Layout:** Isolated VPC in `ap-south-1` with public subnets for ingress controllers/API Gateways, and private subnets for DB, Queue, and GPU Workers.
- **Ingress/Egress:** Cloudflare (or NGINX/HAProxy FOSS equivalent) protecting public endpoints. Strict NAT Gateways controlling outbound traffic from private resources.
- **Load Balancing:** Layer 7 HTTP/gRPC load balancing routing WebRTC traffic and API requests dynamically to healthy ingest nodes.
- **DNS Strategy:** Global Anycast DNS routing for low latency resolution with geo-fencing policies for India localization.

## Reliability Strategy

- **Failover Systems:** Cross-AZ deployments for critical control plane nodes (Postgres, RabbitMQ).
- **Redundancy:** Multi-node replication for Postgres (e.g., Patroni). MinIO cluster with strict erasure coding.
- **Disaster Recovery:** Automated daily volume snapshots and continuous Write-Ahead Log (WAL) archiving for Postgres to offsite object storage. Defined RTO of < 1 hour and RPO of < 15 mins.
- **Self Healing Mechanisms:** Auto-Scaling Groups tied to node health checks; automatic rescheduling of orphaned ML tasks from dropped GPU instances.

## Security Architecture

- **IAM:** Principle of least privilege enforced via IAM roles (or Keycloak if purely FOSS). Edge nodes receive temporary, strictly-scoped access tokens.
- **Encryption:** TLS 1.3 everywhere in transit. AES-256 server-side encryption for MinIO and Postgres volumes at rest.
- **Secrets Management:** HashiCorp Vault (or native cloud secret manager) for dynamic credential injection; no static secrets in source code or CI.
- **Network Security:** Zero-trust principles with strictly restricted Security Groups/Network Policies limiting intra-cluster lateral movement.

## Observability

- **Monitoring:** Prometheus stack polling metrics from all cloud services and remote Edge nodes.
- **Logging:** Promtail/FluentBit gathering structured JSON logs into Loki for centralized indexing and queries.
- **Tracing:** OpenTelemetry (OTel) instrumented across Edge proxies, API Gateways, and Worker daemons to trace the complete chunk lifecycle.
- **Alerting:** Alertmanager routing critical failures (e.g., `Queue Backlog > 1hr`, `Node Offline`) to PagerDuty/Slack.

## Performance & Cost Optimization

- **Autoscaling:** Predictive and reactive scaling on GPU workers tied to queue depth. Scale-to-zero capabilities for ML workers during K-12 off-hours (nighttime).
- **Resource Optimization:** Right-sizing cloud instances. Priority use of spot/preemptible GPU instances for cold path tasks given their asynchronous nature.
- **Caching:** Redis-backed caching for frequent API lookups and dashboard metadata.
- **Infrastructure Efficiency:** Aggressive garbage collection of processed media chunks post-retention window.

## Risks & Tradeoffs

- **Operational Risks:** Hybrid Edge/Cloud synchronization failure causing data loss or silent chunk drops. Requires extreme care in resumable upload logic.
- **Scaling Concerns:** Cloud GPU scarcity or sudden spike in processing queues blocking authoritative scoring.
- **Vendor Tradeoffs:** Prioritizing FOSS tools over managed cloud services increases operational management overhead but guarantees absolute compliance and portability.
- **Cost Implications:** While the customer budget is ₹0, the central architecture runs high inherent costs due to GPU compute and WAN egress. Needs constant optimization via intelligent batching.

## Agile Sprint Plan

- **Milestones:**
  1. Complete Cloud Base Architecture mapping.
  2. Implement Terraform IaC for `staging`.
  3. Deploy base control plane (Postgres, MinIO, RabbitMQ).
  4. Integrate monitoring (Prometheus/Grafana).
- **Implementation Phases:**
  - Sprint 03: Establish IaC repository and CI/CD pipelines. Stand up Cloud VPC.
  - Sprint 04: Deploy Core Data and Queuing Services.
  - Sprint 05: Establish Edge-to-Cloud mTLS connection and Observability tracing.
- **Priorities:** Base networking security, automated provisioning, and reliable queuing before any GPU compute is provisioned.
- **Expected Infrastructure Improvements:** Transition from local/dev mockups into a formalized, reproducible, and compliant cloud foundation ready to ingest Edge data safely.
