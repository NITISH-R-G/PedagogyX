# Autonomous Senior DevOps Platform Architecture Report

**Status:** Active
**Owner:** Autonomous Senior DevOps Engineer & Platform Infrastructure Architect
**Context:** PedagogyX - Multimodal AI classroom intelligence platform

## Infrastructure Overview

PedagogyX is designed as a highly scalable, Hybrid Edge-Cloud platform built to handle multimodal audio and video stream ingestion from thin clients across Indian educational environments. The current architecture centers on edge capture via Android-based Meta Ray-Ban (DAT) applications or lightweight Windows smartboards, bridging to a centralized, OSS-first cloud processing tier.

- **Current Architecture:** WebRTC/HTTPS chunked ingestion from edge devices. Gateway nodes route payloads to MinIO object storage, while metadata events queue in Redis for processing by autonomous Python-based inference workers (ASR, CV, Metrics).
- **Environment Topology:**
  - `Edge`: Untrusted, unmanaged school LANs/WANs subject to heavy latency and disconnections.
  - `Cloud`: Centralized India-region VPCs (`ap-south-1` equivalent) designed for extreme data sovereignty compliance under the DPDP Act.
- **Deployment Model:** Fully automated, declarative infrastructure. No manual SSH access permitted. Transitioning to GitOps-driven deployment utilizing immutable Helm charts.
- **Operational Goals:** Provide 99.99% availability for API ingestion endpoints, ensuring zero data loss during network disruptions. Scale compute precisely in response to queue depth, tearing down aggressively during non-school hours to meet the stringent ₹0 hardware budget.

## CI/CD Architecture

- **Pipeline Structure:** Trunk-based development anchored by comprehensive GitHub Actions. Every pull request is strictly gated by linting (Ruff, Black, Prettier, Markdownlint), unit testing (Pytest, Vitest), and security/vulnerability scanning.
- **Automation Strategy:** Container images are built once per commit, immutably tagged, signed, and pushed to a central registry. Promotion across staging and production namespaces occurs linearly without rebuilds.
- **Deployment Flow:** GitOps continuous deployment utilizing ArgoCD/Flux. Configuration changes automatically reconcile cluster state.
- **Rollback Mechanisms:** Integrated progressive delivery (e.g., Flagger) orchestrating canary rollouts. Deployment health is bound to Prometheus telemetry; SLI breaches trigger instantaneous, automated rollback to the previous known-good state.

## Cloud Infrastructure

- **Cloud Services:** Adherence to a strict OSS-first doctrine. Infrastructure relies on agnostic compute primitives within India data centers to preclude vendor lock-in.
- **Networking:** Hub-and-Spoke VPC models isolating public ingestion from private inference compute. All ingress is proxied through rate-limited WAFs.
- **Infrastructure Layout:**
  - _Ingress/Gateway:_ Stateless API pods scaling dynamically.
  - _Queue & Storage:_ Highly available Redis and MinIO (S3-compatible) arrays.
  - _Compute:_ Horizontally scalable worker node pools.
- **Scaling Architecture:** KEDA (Kubernetes Event-driven Autoscaling) translates Redis queue depths into Horizontal Pod Autoscaler targets, ensuring GPU and CPU compute provisions exactly match the backlog, detached from simplistic CPU-utilization metrics.

## Kubernetes Architecture

- **Cluster Topology:** High-Availability Control Plane managing tightly bound node pools via strict node affinities.
  - _Web/API Nodes:_ High CPU/Memory optimized for rapid scaling.
  - _Inference Nodes:_ Dedicated RTX 5070 GPU nodes restricted solely to ML worker execution via device plugins.
- **Deployment Strategy:** Anti-affinity rules guarantee that API ingestion pods are distributed across multiple Availability Zones (AZs) to survive complete node or zone isolation events.
- **Autoscaling:** Cluster Autoscaler monitors un-schedulable pods triggered by KEDA queue thresholds, dynamically provisioning new RTX 5070 nodes and rapidly aggressively draining and terminating them when idle.
- **Ingress Architecture:** NGINX or Traefik serving as clustered ingress controllers, responsible for aggressive TLS 1.3 termination, DDOS mitigation, and traffic routing into private cluster networks.

## Observability Stack

- **Metrics:** Highly Available Prometheus deployments scraping all core services. Custom ML metrics (VRAM utilization, worker batch latency, dead letter queue length) are surfaced as critical operational signals.
- **Logging:** Centralized log aggregation via the LGTM stack (Loki, Grafana, Promtail) ensuring long-term retention of operational telemetry. All inference output strictly implements full traceback logging into standard streams for ingestion.
- **Tracing:** OpenTelemetry (OTel) correlating request lifecycles from the initial client edge chunk upload through Gateway API storage and asynchronous processing worker completion.
- **Alerting:** Alertmanager configured to route actionable incidents to appropriate on-call tiers, drastically reducing alert fatigue by alerting on symptom-based SLO breaches rather than raw threshold alarms.

## Security Architecture

- **IAM:** Principle of Least Privilege rigorously enforced. Kubernetes Service Accounts are explicitly mapped to tightly scoped cloud IAM roles via OIDC/Workload Identity.
- **Secret Management:** Secrets are strictly ephemeral and injected dynamically via HashiCorp Vault or External Secrets Operator. Hardcoded credentials are fundamentally disallowed.
- **Network Security:** Kubernetes Network Policies operate in a default-deny paradigm, explicitly allowing only required intra-namespace communication. Internal communications are hardened using mTLS via a service mesh layer.
- **Vulnerability Management:** Continuous scanning of container images via Trivy natively within CI. Infrastructure as code undergoes static security analysis via Checkov/tfsec prior to apply.

## Reliability Strategy

- **Redundancy:** N+2 redundancy enforced across all stateless tiers. PostgreSQL and Redis deployments configured with active-passive synchronous replication to avert split-brain states and data loss.
- **Failover:** Automated leader election within distributed data planes. Stateless application architectures seamlessly route around terminated worker nodes.
- **Disaster Recovery:** Automated cross-region/AZ backups of database WAL files and MinIO buckets. Entire application and networking state is deterministically recoverable via Terraform and GitOps manifestations with an aggressive RTO/RPO target.
- **Self Healing Mechanisms:** Rigorous implementation of Kubernetes liveness, readiness, and startup probes. Services encountering unrecoverable state (e.g., deadlocked GPU kernels) are forcefully terminated and gracefully rescheduled. Background queues strictly leverage Dead Letter Queues (DLQs) to capture and isolate poison pill payloads.

## Cost Optimization

- **Infrastructure Savings:** Exclusive use of OSS databases (Postgres) and storage (MinIO) eliminates proprietary managed-service premiums. Spot instance or preemptible VM usage aggressively pursued for asynchronous asynchronous inference queues.
- **Resource Optimization:** AI models rigorously quantized to operate efficiently within the 12GB VRAM constraints of consumer-grade RTX 5070s, precluding the necessity for expensive datacenter silicon (A100/H100).
- **Scaling Efficiency:** By binding scaling actions directly to queue depth, the platform ensures expensive GPU resources are only online while active processing is required, successfully scaling compute to absolute zero during idle night/weekend periods.

## Risks & Bottlenecks

- **Operational Risks:** Inconsistent network availability at K-12 edge locations poses the risk of massive, synchronized "thundering herds" of delayed payload uploads once connectivity is restored, potentially overwhelming ingestion API limits.
- **Scaling Limitations:** Concurrent asynchronous operations risk database connection exhaustion. N+1 query structures and unbounded DB sessions within worker threads are actively targeted for connection pooling (PgBouncer) and cursor-sharing refactors.
- **Security Risks:** Any leakage or insufficient obfuscation of minors' PII due to logic faults directly infringes upon DPDP legislation.
- **Deployment Risks:** Releasing unoptimized multi-gigabyte ML weights extends container pull and startup times exponentially, significantly degrading the responsiveness of queue-based autoscaling logic during traffic surges.

## Agile Sprint Plan

- **Phase 1: Foundation & Resiliency**
  - Finalize core declarative infrastructure modules (Terraform/Helm) targeting full cluster high-availability within the ap-south-1 compliant region.
- **Phase 2: Automated Deployment & Observability**
  - Implement full GitOps CD pipelines via ArgoCD.
  - Deploy and validate the centralized Prometheus, Loki, and OpenTelemetry stack, establishing baseline SLO alerts.
- **Phase 3: Deep Scalability Engineering**
  - Configure and test KEDA based autoscaling targeting custom Redis queue metrics.
  - Execute chaos engineering tests confirming RTX 5070 nodes accurately spin up under simulated batch load and cleanly tear down to zero when idle.
- **Phase 4: Optimization & Refinement**
  - Implement aggressive database connection pooling schemas.
  - Finalize and audit DLQ routing across all background processing worker nodes to ensure zero dropped insights.
- **Expected Operational Improvements:** Absolute elimination of configuration drift, comprehensive operational visibility across the Hybrid Edge-Cloud divide, and radical reduction in operational spend through hyper-efficient, queue-driven scale-to-zero capabilities.
