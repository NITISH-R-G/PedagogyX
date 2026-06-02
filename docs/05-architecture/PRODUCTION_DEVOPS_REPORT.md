# DevOps Platform Architecture Report

## Infrastructure Overview

PedagogyX employs a Hybrid Edge-Cloud (D-PROC=C) architecture meticulously designed for high reliability and rapid scaling in low-connectivity K-12 environments. The system leverages lightweight edge clients—Android companion apps combined with Meta Ray-Ban glasses (DAT)—for raw capture, effectively shifting heavy processing to a robust, self-hosted, centralized cloud backend. This architecture guarantees a strict ₹0 customer hardware budget by running multimodal inference (faster-whisper, YOLO, Ollama) on centralized RTX 5070 compute pools rather than expensive edge devices. The infrastructure targets 99.99% API availability, enforces complete DPDP data residency compliance in India, and utilizes declarative configuration to ensure zero-touch disaster recovery and scale-to-zero capabilities.

## CI/CD Architecture

The CI/CD pipeline is engineered for deployment safety, automation, and speed.

- **Pipeline Structure:** GitHub Actions orchestrates the trunk-based CI lifecycle, heavily gated by static analysis (ruff, eslint, black, prettier), automated test suites, and strict container immutability checks before merging.
- **Automation Strategy:** Deterministic builds guarantee that container images are built once, signed (e.g., Sigstore), and promoted across environments. Infrastructure as Code (IaC) is strictly enforced using Terraform for cloud resources and Helm for Kubernetes workloads.
- **Deployment Flow:** GitOps drives continuous deployment via ArgoCD. Commits to the main branch seamlessly reconcile cluster state without direct human intervention, preventing configuration drift and snowflakes.
- **Rollback Mechanisms:** Automated, telemetry-driven rollouts via progressive delivery tools (e.g., Argo Rollouts/Flagger). Canary deployments automatically revert to the previous known-good state if SLIs (like error rates or latency) breach defined thresholds, ensuring zero-downtime deployments.

## Cloud Infrastructure

The cloud environment strictly prohibits proprietary APIs (e.g., OpenAI, AWS Rekognition) to maintain complete OSS independence and cost control.

- **Cloud Services:** Cloud-agnostic deployments utilize India-based cloud regions or bare metal nodes to comply with DPDP regulations. Storage relies on high-availability PostgreSQL for relational data and MinIO for S3-compatible, secure multimedia object storage.
- **Networking:** A Hub-and-Spoke VPC architecture isolates public and private subnets. Public edge load balancers route ingress traffic through distributed WAFs. Internal cluster traffic operates on a zero-trust model utilizing mutual TLS (mTLS).
- **Infrastructure Layout:** Three primary tiers comprise the topology: stateless high-throughput ingestion edge nodes, highly-available asynchronous message brokers (Redis), and specialized GPU inference worker pools equipped with RTX 5070 cards for AI workloads.
- **Scaling Architecture:** Asynchronous event-driven autoscaling via KEDA decouples compute from CPU, directly scaling AI worker pods based on queue depths to optimize GPU usage and strictly limit idle costs.

## Kubernetes Architecture

Kubernetes serves as the backbone orchestrator, providing robust self-healing and workload segmentation.

- **Cluster Topology:** Multi-AZ high-availability control plane. Distinct node pools are strictly tainted and labeled: general compute for APIs, high-memory for databases, and dedicated 12GB VRAM GPU instances for ML inference.
- **Deployment Strategy:** Workloads are defined parametrically via Helm charts and managed by GitOps controllers. Anti-affinity rules guarantee that replicas are spread across multiple availability zones to tolerate localized failures.
- **Autoscaling:** Horizontal Pod Autoscaler (HPA) manages stateless web/API traffic based on resource utilization. Cluster Autoscaler seamlessly provisions new GPU instances to schedule pending inference pods and aggressively scales them to zero when classroom capture queues are empty.
- **Ingress Architecture:** Ingress-Nginx controllers scale horizontally to terminate TLS 1.3 connections, enforce aggressive rate limiting, and mitigate DDoS attacks, ensuring smooth ingestion of massive concurrent audio/video chunk uploads.

## Observability Stack

A zero-blind-spot observability suite enables rapid MTTR and deep operational insights.

- **Metrics:** Highly available Prometheus clusters scrape critical telemetry from node-exporter, kube-state-metrics, and custom exporters tracking RTX 5070 VRAM utilization and asynchronous queue latency.
- **Logging:** Promtail efficiently ships structured logs to Loki. The logging pipeline incorporates strict, automated edge scrubbing to anonymize minor student PII before indexing, maintaining rigorous regulatory compliance.
- **Tracing:** End-to-end OpenTelemetry (OTel) instrumentation connects the entire user journey—from the Meta Ray-Ban DAT edge client, through the ingest buffers, down to the final multimodal pedagogy scoring—facilitating deterministic root cause analysis.
- **Alerting:** Alertmanager integrates with PagerDuty and Slack to route actionable, symptom-based alerts. Alert fatigue is mitigated by triggering strictly on defined SLO burn rates rather than localized infrastructure noise.

## Security Architecture

Security is intrinsic and absolute, centered around zero trust and data privacy.

- **IAM:** Strict Principle of Least Privilege (PoLP) applied universally. Workload Identity binds Kubernetes Service Accounts to heavily scoped cloud IAM roles, eliminating long-lived static credentials.
- **Secret Management:** HashiCorp Vault or External Secrets securely injects ephemeral configurations at runtime. No secrets are ever persisted in the source code or static configuration files.
- **Network Security:** Kubernetes NetworkPolicies enforce default-deny intra-cluster communication. Database and worker nodes reside on isolated private subnets with no public IPs, communicating exclusively over mTLS. All data is encrypted at rest (AES-256) and in transit (TLS 1.3).
- **Vulnerability Management:** Trivy automatically scans all container registries during CI. Infrastructure code is continuously audited by tfsec and checkov. Admission controllers block any deployments carrying critical CVEs.

## Reliability Strategy

The platform is designed to gracefully absorb and recover from inevitable failures.

- **Redundancy:** N+2 redundancy for all stateless nodes. Distributed databases (PostgreSQL, Redis) run active-passive clustered topologies with synchronous replication to prevent data loss.
- **Failover:** Automated leader elections ensure high availability. Edge proxy services actively route around degraded backend instances. Meta Ray-Ban edge clients securely buffer data locally if network connectivity degrades, preventing ingestion loss.
- **Disaster Recovery:** Automated continuous WAL backups and MinIO replication strictly stored in a geographically isolated cold-storage tier. Declarative Terraform pipelines guarantee full infrastructure reconstruction within minimal RTO limits.
- **Self Healing Mechanisms:** Comprehensive Kubernetes probes proactively terminate deadlocked inference pods. Circuit breakers prevent cascading failures during traffic spikes, ensuring that API ingestion remains functional even if ML workers degrade.

## Cost Optimization

Cost efficiency is paramount to sustain the ₹0 school hardware business model.

- **Infrastructure Savings:** Utilizing RTX 5070 consumer-grade GPUs bypasses the extreme pricing of enterprise datacenter hardware while delivering sufficient VRAM (12GB) via quantized OSS models.
- **Resource Optimization:** Strict memory and CPU limits are enforced via namespace quotas and Vertical Pod Autoscaler (VPA) profiling to tightly pack pods and minimize overall cluster footprint.
- **Scaling Efficiency:** KEDA drives aggressive scale-to-zero capabilities for GPU nodes during nights and weekends, cutting inference compute costs substantially while retaining constant availability on the API edge.

## Risks & Bottlenecks

Proactive threat modeling identifies current limitations to ensure safe operational scaling.

- **Operational Risks:** Managing complex, self-hosted CUDA environments, TensorRT optimizations, and underlying GPU node pools demands extreme operational maturity to avoid cluster degradation during updates.
- **Scaling Limitations:** Indian K-12 networks exhibit volatility; mass reconnection events can trigger "thundering herd" patterns that overwhelm initial ingest ingress controllers and Redis queues.
- **Security Risks:** Any failure in the PII redaction pipeline before durable storage constitutes a catastrophic DPDP compliance breach.
- **Deployment Risks:** Deploying massive OSS model weights natively inflates container startup times, which directly impacts KEDA scaling speed and can cause localized backpressure during ingestion bursts.

## Agile Sprint Plan

- **Phase 1: Foundation (Sprint 1-2)**
  - Establish multi-AZ VPC topology and Kubernetes control plane in an India-based region using Terraform.
  - Setup core ArgoCD GitOps pipelines for automated helm chart synchronization.
- **Phase 2: State & Storage (Sprint 3-4)**
  - Deploy Highly Available Postgres, Redis clusters, and MinIO.
  - Implement HashiCorp Vault for dynamic secrets management.
- **Phase 3: APIs & Inference (Sprint 5-6)**
  - Deploy Edge API ingestion gateways and implement KEDA monitoring on Redis queues.
  - Provision RTX 5070 node pools and validate AI worker autoscaling (including scale-to-zero).
- **Phase 4: Observability & Resilience (Sprint 7-8)**
  - Roll out complete Prometheus, Loki, and OpenTelemetry stack.
  - Perform chaos engineering simulations (node loss, DB failover) to validate runbooks and disaster recovery objectives.
