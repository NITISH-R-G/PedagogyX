# Senior Cloud Infrastructure Architecture Report v3

**Role:** Autonomous Senior Cloud Engineer & Cloud Infrastructure Architect
**Context:** PedagogyX - Multimodal AI Classroom Intelligence Platform
**Date:** 2026-05-23

## Cloud Problem Analysis

- **Business Requirements:** Deliver a multimodal AI classroom intelligence platform tailored for the K-12 and University segments in India. Must strictly adhere to the Digital Personal Data Protection Act (DPDP) through strict India data residency. The system relies entirely on open-source software (OSS-first) to avoid proprietary cloud AI API costs.
- **Scale Assumptions:** Must seamlessly support massive-scale inference with district-wide deployments (10,000+ simultaneous classrooms during school hours). Edge nodes on school LANs will ingest concurrent high-resolution video streams (screen, multi-cam, Android POV) and audio before asynchronous WAN upload.
- **Operational Constraints:** Total client hardware budget is strictly ₹0 (D-10 constraint), meaning edge devices are low-end. Cloud processing relies on highly optimized GPU instances (RTX 5070 budget equivalent). Erratic school network uplinks necessitate robust asynchronous handling.
- **Failure Scenarios:** Unstable classroom internet, hardware degradation at edge nodes, regional cloud ISP failures, container runtime crashes, centralized GPU worker starvation under spiky loads, and split-brain scenarios in stateful datastores.

## Cloud Architecture

- **Infrastructure Topology:** Hub-and-Spoke model mapping distributed Edge nodes (LAN ingest buffers) into a centralized, highly-available OSS-first inference backend hosted in an India-based cloud region (e.g., `ap-south-1`).
- **Cloud Services:**
  - **Compute:** Multi-AZ Kubernetes clusters for stateless API endpoints, ingest proxies, and administrative dashboard backends. Dedicated autoscale-enabled GPU node groups for computationally intensive batch ML (faster-whisper, YOLO, Ollama).
  - **Storage:** S3-compatible Object Storage (MinIO) for chunked, immutable media storage. Highly available PostgreSQL (Patroni) for metadata, state, and finalized pedagogical scores.
  - **Messaging:** High-throughput event streaming via Redis or Kafka for decoupled reliable message queuing between the ingest layer and inference workers.
- **Networking:** Strict VPC tiering separating public ingress traffic from internal ML processing and persistence layers.
- **Deployment Layout:** Stateless components spread across multiple availability zones. Asynchronous workers and databases deployed in private, non-routable subnets.

## Infrastructure Automation

- **IaC Strategy:** Fully declarative infrastructure via Terraform provisioning all base cloud environments, VPCs, IAM roles, and Managed Kubernetes clusters. Zero manual configuration via UI consoles.
- **Provisioning Workflows:** Automated base node images built via Packer for rapid node bootstrapping and drift elimination.
- **Deployment Automation:** Strict GitOps workflows driven by ArgoCD or Flux. Infrastructure states and Helm charts are perfectly mirrored in Git, enabling reproducible deployments and immediate automated rollbacks on failure.
- **Environment Management:** Completely reproducible environments (`dev`, `staging`, `prod`) driven by explicit, parameterized configurations.

## Networking Architecture

- **VPC Layout:** Multi-tier VPC structure in an India-based region. Public subnets host Ingress Controllers (Traefik/NGINX) and API Gateways. Private subnets are reserved for databases, message queues, and GPU ML workers.
- **Ingress/Egress:** WAF-protected ingress traffic. Egress traffic strictly controlled via NAT Gateways, avoiding direct internet exposure for backend workloads.
- **Load Balancing:** Layer 7 HTTP/gRPC load balancers dynamically route traffic to healthy API and WebRTC ingest pods.
- **DNS Strategy:** Global Anycast DNS resolution with geo-fencing policies to ensure data sovereignty and compliance with DPDP.

## Reliability Strategy

- **Failover Systems:** Cross-AZ replication for stateful components (Postgres via Patroni, multi-node MinIO). Stateless API tiers auto-recover dynamically via Kubernetes ReplicaSets.
- **Redundancy:** N+1 redundancy across all essential control plane elements and edge proxies to absorb component failures gracefully.
- **Disaster Recovery:** Automated continuous WAL archiving for Postgres to offsite, encrypted object storage. Defined RTO < 1 hour and RPO < 15 mins.
- **Self Healing Mechanisms:** Aggressive liveness and readiness probes in Kubernetes. Failed pods are aggressively evicted. Background worker tasks utilize a Dead Letter Queue (DLQ) pattern for failed payload recovery.

## Security Architecture

- **IAM:** Principle of least privilege enforced via Cloud IAM and Kubernetes RBAC. Workloads use strictly scoped short-lived identity tokens (e.g., IRSA or equivalent).
- **Encryption:** TLS 1.3 mandated for all data in transit (edge-to-cloud and internal service mesh). AES-256 server-side encryption for all at-rest volumes, databases, and MinIO buckets.
- **Secrets Management:** External Secrets Operator backed by HashiCorp Vault for dynamic secret injection and rotation. Zero static credentials stored in code or ConfigMaps.
- **Network Security:** Zero-trust architecture with Kubernetes NetworkPolicies restricting intra-cluster lateral movement by default.

## Observability

- **Monitoring:** Prometheus clusters polling metrics from cloud infrastructure, Kubernetes nodes, and custom ML worker queue depths.
- **Logging:** Promtail and FluentBit aggregating structured JSON logs to Loki, enabling fast querying of ingestion flow and worker errors without heavy operational overhead.
- **Tracing:** OpenTelemetry (OTel) instrumentation tracking end-to-end payload lifecycles from Edge client upload to finalized Postgres score insertion.
- **Alerting:** Alertmanager integrated with PagerDuty for critical, actionable alerts (e.g., `GPU OOM`, `Queue Backlog SLA breach`). Low alert fatigue through aggressively tuned thresholds.

## Performance & Cost Optimization

- **Autoscaling:** KEDA (Kubernetes Event-driven Autoscaling) configured to proactively scale GPU worker deployments based on queue depth metrics, scaling to zero during off-peak hours (nights/weekends).
- **Resource Optimization:** Strict memory and CPU limits defined for all workloads. Efficient tight packing of ML tasks to maximize the RTX 5070 equivalent VRAM utilization.
- **Caching:** Redis-backed caching strategies applied to API queries and hot-path administration dashboard loads.
- **Infrastructure Efficiency:** Aggressive object lifecycle management in MinIO automatically expunging raw data post-processing to minimize storage waste. Spot and preemptible instances utilized for cold-path batch jobs to achieve up to 70% cost reduction.

## Risks & Tradeoffs

- **Operational Risks:** Operating a hybrid edge-cloud infrastructure increases complexity in debugging edge failures and WAN sync issues across distributed Indian schools.
- **Scaling Concerns:** Cloud GPU scarcity or localized capacity limits during peak school hours could delay authoritative scoring SLAs.
- **Vendor Tradeoffs:** Prioritizing an OSS-first, self-hosted stack completely circumvents proprietary API costs and vendor lock-in but significantly elevates internal platform operational burden and SRE overhead.
- **Cost Implications:** Maintaining large GPU node pools is natively expensive. The strict ₹0 client hardware budget mandates hyper-optimized batching, aggressive Spot instance usage, and rigorous scale-to-zero enforcement to maintain financial viability.

## Agile Sprint Plan

- **Sprint 01:** Establish core declarative infrastructure (Terraform) for India-based VPCs and managed Kubernetes base layers.
- **Sprint 02:** Deploy base control plane via ArgoCD GitOps, encompassing MinIO, PostgreSQL, and foundational API gateways.
- **Sprint 03:** Implement full observability stack (Prometheus, Loki, OpenTelemetry) and validate custom ML queue metrics.
- **Sprint 04:** Configure robust KEDA-based autoscaling rules for GPU workloads and test dynamic scale-to-zero capabilities with simulated traffic.
- **Sprint 05:** Execute comprehensive disaster recovery simulations (e.g., node loss, DB failover) and finalize robust alerting integrations.
