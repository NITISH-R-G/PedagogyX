# World Class DevOps Platform Report

**Role:** Senior DevOps Engineer, Platform Infrastructure Architect
**Context:** PedagogyX - Multimodal AI classroom intelligence platform
**Constraints:** OSS-first, ₹0 hardware budget (D-10), DPDP compliance (India data residency), RTX 5070 GPU inference, Meta Ray-Ban primary capture client (DAT).

---

## Infrastructure Overview

- **Current Architecture:** Hybrid Edge-Cloud (D-PROC=C) architecture. Lightweight, zero-cost edge clients (Meta Ray-Ban glasses tethered to an Android companion app via DAT) capture multi-modal streams (video, audio). The cloud backend is a centralized, self-hosted OSS stack running entirely in an India-based region.
- **Environment Topology:**
  - _Local:_ Docker Compose (`infra/compose.dev.yaml`) ensuring strict developer parity.
  - _Ephemeral/Staging:_ Automated namespace provisioning via CI for integration testing.
  - _Production:_ High-availability Kubernetes clusters deployed across multi-AZ isolated VPCs inside India to comply strictly with the DPDP Act.
- **Deployment Model:** 100% Declarative GitOps via ArgoCD/Flux. Infrastructure as Code (IaC) strictly enforced using Terraform and Helm. Direct SSH or manual imperative changes are cryptographically prohibited.
- **Operational Goals:** 99.99% core API uptime. Fully automated, zero-touch disaster recovery. Scale-to-zero capability during off-school hours to maintain the strict ₹0 customer hardware budget.

## CI/CD Architecture

- **Pipeline Structure:** Trunk-based development enforced via GitHub Actions. Pipelines are strictly gated by static analysis (ruff, black, isort, eslint, prettier, markdownlint), automated unit testing (`pytest`, `vitest`), and container security scans (Trivy).
- **Automation Strategy:** Deterministic build pipelines. Immutable container images are built once, signed (e.g., Sigstore/Cosign), pushed to a private registry, and promoted chronologically across environments without rebuilding.
- **Deployment Flow:** GitOps continuous deployment. Commits to the main branch automatically reconcile cluster state via ArgoCD. All workloads are packaged and version-controlled via Helm charts.
- **Rollback Mechanisms:** Automated, telemetry-driven rollbacks using progressive delivery (Flagger or Argo Rollouts). Canary deployments are monitored via Prometheus SLIs (latency, 5xx rate); any threshold breach instantly reverts the deployment to the known-good state with zero manual intervention.

## Cloud Infrastructure

- **Cloud Services:** Cloud-agnostic deployment on bare-metal or cost-optimized cloud provider instances in India. Proprietary APIs (AWS Rekognition, OpenAI) are strictly forbidden. Storage relies on self-hosted, S3-compatible MinIO and PostgreSQL for relational data.
- **Networking:** Strict Hub-and-Spoke VPC topology. Public traffic terminates at high-availability edge load balancers, inspecting traffic via WAF. Private subnets isolate application, database, and inference nodes. Zero-trust mTLS implemented internally.
- **Infrastructure Layout:**
  - _Ingress/Edge Tier:_ Horizontally scaled, stateless FastAPI ingestion nodes.
  - _Message Bus:_ High-throughput asynchronous queues (Redis/Kafka).
  - _Inference Tier:_ Autoscaling GPU worker pools equipped with RTX 5070 GPUs.
- **Scaling Architecture:** Event-driven horizontal autoscaling decoupled from CPU metrics. Leveraging KEDA (Kubernetes Event-driven Autoscaling) to scale inference workers dynamically based purely on queue depth, ensuring optimal processing latency while preventing GPU idle bloat.

## Kubernetes Architecture

- **Cluster Topology:** Multi-AZ Kubernetes control plane for high availability. Highly segmented node pools defined by taints and tolerations: lightweight nodes for ingress and web services, high-memory nodes for databases, and dedicated 12GB VRAM GPU nodes for inference (faster-whisper, YOLO, Ollama).
- **Deployment Strategy:** Parameterized Helm-based deployments. Anti-affinity rules guarantee that mission-critical pods (e.g., API ingestion) are distributed across disparate availability zones to survive complete node or AZ outages.
- **Autoscaling:** Dual-layer scaling. Horizontal Pod Autoscaler (HPA) manages stateless API and web tiers. The Cluster Autoscaler dynamically provisions new RTX 5070 compute nodes when KEDA-driven inference pods enter a `Pending` state, scaling back down to zero when queues deplete.
- **Ingress Architecture:** NGINX or Traefik Ingress controllers handling aggressive TLS 1.3 termination, rate-limiting, and DDOS mitigation. Designed to handle sudden, large bursts of WebRTC stream uploads from Android edge clients.

## Observability Stack

- **Metrics:** High-availability Prometheus cluster scraping `node-exporter`, `kube-state-metrics`, `cAdvisor`, and custom application metrics (e.g., RTX 5070 VRAM utilization, queue wait times, active DAT sessions).
- **Logging:** Centralized log aggregation using Promtail shipping structured JSON logs to Loki, minimizing the heavy storage costs of traditional ELK stacks. All logs undergo strict, automated PII scrubbing at the edge before indexing.
- **Tracing:** Full OpenTelemetry (OTel) instrumentation. Distributed tracing tracks latency precisely from the initial Meta Ray-Ban Android capture, through the ingest queues, down to the final LLM pedagogy scoring, ensuring deterministic root cause analysis.
- **Alerting:** Alertmanager routing curated, symptom-based alerts to PagerDuty/Slack. Alerting strategy is strictly tuned against Service Level Objectives (SLOs) to prevent alert fatigue (e.g., alerting on `burn rate` rather than generic high CPU usage).

## Security Architecture

- **IAM:** Strict Principle of Least Privilege (PoLP). Kubernetes Service Accounts are tightly bound to scoped Cloud IAM roles via Workload Identity (OIDC), ensuring pods only access exactly the resources they require.
- **Secret Management:** HashiCorp Vault or External Secrets Operator dynamically syncing secrets into Kubernetes namespaces. Secrets are automatically rotated, ephemeral, and strictly barred from the Git repository.
- **Network Security:** Default-deny Kubernetes NetworkPolicies. Explicit allow-listing of intra-namespace communication. External databases and inference nodes have no public IP exposure. All data is AES-256 encrypted at rest and TLS 1.3 encrypted in transit.
- **Vulnerability Management:** Automated Trivy container vulnerability scanning in CI. Checkov and `tfsec` static analysis on all Terraform code. Strict admission controllers in Kubernetes blocking any image deployment with critical unpatched CVEs.

## Reliability Strategy

- **Redundancy:** N+2 redundancy for all stateless components. Distributed databases (Postgres, Redis) utilize synchronous active-passive replication to ensure zero data loss in split-brain scenarios.
- **Failover:** Automated leader elections across distributed clusters. Stateless proxy nodes dynamically route around failed backend workers instantaneously. Edge Android clients buffer capture data locally, ensuring resilience against flaky K-12 network drops.
- **Disaster Recovery:** Fully automated, continuous WAL archiving for Postgres and MinIO metadata mirroring to a secondary, geographically isolated cold-storage vault. The entire platform infrastructure can be deterministically rebuilt from Terraform state (RTO < 2 hours, RPO < 15 minutes).
- **Self Healing Mechanisms:** Rigorous Kubernetes liveness and readiness probes. Pods experiencing memory leaks or inference deadlocks are automatically killed and restarted. Graceful degradation mechanisms ensure that if the ML pipeline fails, stream ingestion still succeeds.

## Cost Optimization

- **Infrastructure Savings:** Exclusive reliance on open-source software (OSS) eliminates enterprise licensing. Strategic utilization of spot/preemptible instances for asynchronous, stateless ASR inference queues.
- **Resource Optimization:** Granular Vertical Pod Autoscaler (VPA) profiling to tightly pack workloads. AI models are quantized to strictly fit within the 12GB VRAM limits of the RTX 5070, avoiding the need for expensive datacenter-class GPUs like A100s.
- **Scaling Efficiency:** Aggressive scale-to-zero logic for GPU nodes during nights, weekends, and school holidays. The platform ensures we only pay for compute exactly when data is actively processing, achieving the ₹0 hardware budget constraint.

## Risks & Bottlenecks

- **Operational Risks:** Managing complex, self-hosted ML infrastructure (CUDA drivers, TensorRT engines) requires significant operational maturity and introduces risks of cluster instability during model updates.
- **Scaling Limitations:** Indian K-12 environments are prone to severe network volatility, causing sudden, massive "thundering herd" ingestion spikes when connectivity is restored, potentially overwhelming edge API gateways and Redis queues.
- **Security Risks:** Ensuring foolproof anonymization of minor student data before it enters the durable storage layer. Any failure in the PII scrubbing pipeline constitutes a severe DPDP compliance violation.
- **Deployment Risks:** Deploying multi-gigabyte ML model weights can cause massive container image bloat, leading to excruciatingly slow pod startup times, which directly degrades the responsiveness of autoscaling during traffic spikes.

## Agile Sprint Plan

- **Implementation Phases:**
  - _Sprint 1:_ Foundation. Establish core Terraform IaC repository. Provision base multi-AZ VPCs and Kubernetes clusters in the India region. Set up GitOps baseline via ArgoCD.
  - _Sprint 2:_ Data & State. Deploy highly available Postgres (Patroni), Redis, and MinIO clusters via Helm. Implement HashiCorp Vault for secrets management.
  - _Sprint 3:_ Ingestion & API. Deploy FastAPI stateless ingestion nodes and ingress controllers. Validate edge connectivity and secure mTLS configurations.
  - _Sprint 4:_ Inference Autoscale. Configure KEDA to monitor Redis queues. Provision the RTX 5070 GPU node pools and validate dynamic scale-from-zero capabilities.
  - _Sprint 5:_ Observability & Resilience. Deploy Prometheus, Loki, and OpenTelemetry. Execute chaos engineering scenarios (node termination, DB failover) to validate the disaster recovery runbooks.
- **Priorities:** Absolute priority on automated provisioning, security boundary enforcement (DPDP compliance), and observability. No ML workloads go to production without complete telemetry.
- **Milestones:** Zero-touch cluster deployment achieved; automated canary rollouts successfully reverting on synthetic failures; confirmed scale-to-zero GPU capability.
- **Expected Operational Improvements:** Transition from brittle, manual `docker-compose` setups to an elite, Google-grade resilient infrastructure. Eradication of configuration drift, massive reduction in MTTR, and profound cost efficiency strictly aligning with the ₹0 school hardware budget constraint.
