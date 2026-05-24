# Autonomous Cloud Engineering Report

**Status:** Draft v1.0
**Date:** 2026-05-24
**Role:** Senior Cloud Engineer & Cloud Infrastructure Architect

## Cloud Problem Analysis

- **Business Requirements:** Deliver a multimodal AI classroom intelligence platform that strictly adheres to the Digital Personal Data Protection Act (DPDP), mandating Indian data residency. It must support high-scale audio/video ingest, real-time ML processing, and robust supervision dashboards.
- **Scale Assumptions:** Tens of thousands of concurrent capture streams (video/audio/screen) from distributed K-12 and University classrooms, requiring elastic scaling of both ingest gateways and backend GPU workers (e.g., RTX 5070 pools) during peak school hours.
- **Operational Constraints:** A rigid customer hardware budget of ₹0 dictates a Hybrid Edge-Cloud architecture (D-PROC=C) utilizing ultra-low-end clients (Android/Windows) merely for capture. Complete reliance on OSS models (faster-whisper, YOLO+TensorRT, Ollama) and self-hosted infrastructure to avoid proprietary cloud API lock-in.
- **Failure Scenarios:** Must tolerate degraded and flaky school edge networks (resumable streams), inevitable node failures within the ephemeral GPU cluster, large-scale traffic bursts during lesson starts, and regional ISP outages, ensuring zero data loss and eventual consistency for analytical scores.

## Cloud Architecture

- **Infrastructure Topology:** A highly resilient Hybrid Hub-and-Spoke model. The lightweight "Spokes" (Edge clients) ingest data which is buffered and transmitted securely over WAN to a centralized, self-hosted "Hub" in an Indian region.
- **Cloud Services:**
  - Control Plane: Managed Kubernetes (or K3s/RKE2) across multiple availability zones (AZs) running stateless API tier, UI, and Ingress.
  - Stateful Backing Services: Clustered PostgreSQL (Patroni) for metadata, MinIO for S3-compatible chunked media storage, and Kafka for high-throughput decoupled message queuing.
  - ML Inference Pool: Dedicated node groups of optimized GPU instances (e.g., 12GB VRAM classes) running containerized OSS ML workloads consuming from Kafka.
- **Networking:** Strict isolation between tiers. Ingestion traffic hits a DMZ VPC, passing through a robust WAF/API Gateway, before entering private subnet queues. ML workers and databases reside in private VPCs with no direct public ingress.
- **Deployment Layout:** N+1 redundancy for stateless components. Stateful clusters span multiple fault domains. The cold-path ML processing is explicitly decoupled from the hot-path stream ingest to prevent bottlenecks.

## Infrastructure Automation

- **IaC Strategy:** 100% declarative infrastructure using Terraform to provision the foundational cloud resources (VPCs, Subnets, Kubernetes clusters, Object Storage, DB instances). State is versioned and secured in a centralized backend.
- **Provisioning Workflows:** Immutable base machine images constructed via Packer. Ansible is utilized for automated bootstrapping of bare-metal or self-managed nodes with strict, hardened configurations (NVIDIA drivers, Containerd, VPN agents).
- **Deployment Automation:** Fully GitOps-driven application deployment via ArgoCD. All Kubernetes manifests, Helm charts, and environment-specific configuration maps are versioned in Git.
- **Environment Management:** Distinct, identically provisioned environments (`dev`, `staging`, `prod`) driven by parameterized configurations, preventing drift and enabling confident, reproducible deployments.

## Networking Architecture

- **VPC Layout:** Multi-tier Virtual Private Cloud architecture. Public subnets strictly reserved for load balancers and NAT gateways. All compute nodes, queues, and databases reside in private, isolated subnets.
- **Ingress/Egress:** Layer 7 Ingress Controllers (NGINX/Traefik) handle TLS termination and intelligent request routing. Strict Egress filtering via NAT Gateways ensures worker nodes cannot initiate arbitrary external connections.
- **Load Balancing:** Global HTTP/gRPC load balancing across active ingestion gateways, ensuring low-latency stream termination.
- **DNS Strategy:** Geo-fenced anycast DNS to ensure traffic routing exclusively to Indian data centers, tightly enforcing DPDP sovereignty requirements.

## Reliability Strategy

- **Failover Systems:** Cross-AZ deployment of the control plane and database layers. Postgres configured for automated failover.
- **Redundancy:** MinIO deployed with robust erasure coding. Kafka topics partitioned and replicated across brokers to tolerate node loss.
- **Disaster Recovery:** Automated, continuous point-in-time recovery (PITR) for PostgreSQL via WAL archiving. Scheduled, cross-region (within India) backups for critical MinIO buckets. Well-defined, tested RTO and RPO targets.
- **Self Healing Mechanisms:** Aggressive Kubernetes readiness and liveness probes. Kubelet automatically evicts and reschedules pods on unhealthy nodes. Circuit breakers implemented on inter-service communication to prevent cascading failures.

## Security Architecture

- **IAM:** Strict adherence to the Principle of Least Privilege (PoLP). Granular IAM roles assigned to Kubernetes Service Accounts via OIDC (IRSA).
- **Encryption:** AES-256 encryption at rest for all block storage, database volumes, and MinIO buckets. TLS 1.3 enforced for all in-transit communications.
- **Secrets Management:** Centralized secrets management via HashiCorp Vault. Dynamic credential generation where possible, with zero secrets hardcoded in configurations or code repositories.
- **Network Security:** Kubernetes Network Policies enforce zero-trust intra-cluster communication (e.g., frontend pods cannot communicate with the database). Cloud WAF protects against common CVEs and volumetric attacks.

## Observability

- **Monitoring:** Comprehensive Prometheus stack scraping metrics across all layers (node, network, container, application). Grafana dashboards provide operational visibility into queue depth, GPU utilization, and API throughput.
- **Logging:** Promtail/Fluent Bit deployed as DaemonSets to collect structured JSON logs from all workloads, shipping to a centralized Loki cluster for rapid querying and correlation.
- **Tracing:** OpenTelemetry (OTel) instrumentation spans the request lifecycle, from edge ingest to backend ML worker completion, identifying latency bottlenecks in the distributed system.
- **Alerting:** Alertmanager configured with distinct routing trees. Actionable, symptom-based alerts (e.g., `Inference Queue Backlog > SLA`) page on-call engineers via PagerDuty, while low-priority warnings are routed to Slack.

## Performance & Cost Optimization

- **Autoscaling:** KEDA (Kubernetes Event-driven Autoscaling) dynamically scales the GPU inference worker pool based on the length of the Kafka message queue, optimizing expensive compute resource usage.
- **Resource Optimization:** Meticulous tuning of Kubernetes CPU/Memory requests and limits. Tight packing of ML containers to maximize the utilization of 12GB VRAM instances.
- **Caching:** Redis clusters deployed to cache frequent administrative API queries, dashboard metadata, and session state, significantly offloading the primary Postgres database.
- **Infrastructure Efficiency:** Automated S3 lifecycle policies to purge raw capture media immediately after ML processing and DPDP retention requirements are met, minimizing storage footprint. Use of preemptible/spot GPU instances for the asynchronous batch-processing (cold path).

## Risks & Tradeoffs

- **Operational Risks:** The mandate for an entirely self-hosted, OSS-based data plane (MinIO, Kafka, Postgres) significantly increases operational overhead compared to managed cloud services. This requires a mature Platform Engineering posture.
- **Scaling Concerns:** The global scarcity and varying costs of GPU compute. The system relies heavily on the asynchronous "cold path" to buffer workload spikes.
- **Vendor Tradeoffs:** Avoidance of proprietary cloud APIs ensures portability and predictable costs but shifts the burden of maintenance, patching, and high-availability engineering directly onto the internal team.
- **Cost Implications:** While the client hardware budget is ₹0, the backend cloud infrastructure (particularly GPU instances and network egress) represents a substantial operational expense. Aggressive autoscaling and lifecycle management are non-negotiable.

## Agile Sprint Plan

- **Sprint 1: Cloud Foundation & IaC (Priority: High)**
  - Establish Terraform repository structure.
  - Provision base AWS `ap-south-1` infrastructure: VPC, Subnets, NAT Gateways, EKS/K3s clusters.
  - Setup core IAM roles and security groups.
- **Sprint 2: Core Data Services & GitOps (Priority: High)**
  - Deploy ArgoCD for declarative GitOps continuous delivery.
  - Deploy and configure stateful services: MinIO (Object Storage) and Postgres (Metadata) via Helm/Operator.
  - Validate internal network policies and encryption.
- **Sprint 3: Observability Stack & Ingest Gateway (Priority: Medium)**
  - Deploy Prometheus, Loki, and Grafana stack.
  - Implement basic API gateway / Ingress controllers with WAF.
  - Setup initial alerting rules (Alertmanager).
- **Sprint 4: Async Processing & GPU Workers (Priority: Medium)**
  - Deploy Kafka message brokers.
  - Configure KEDA for queue-based autoscaling of the GPU worker nodes.
  - End-to-End test of the mock data flow: Edge Ingest -> MinIO -> Kafka -> GPU Worker.
