# DevOps & Platform Infrastructure Architecture Report

**Version:** 2.0
**Author:** Autonomous Senior DevOps Engineer & Platform Infrastructure Architect
**Focus:** Hyperscale, High-Reliability, Automated Multimodal AI Processing Infrastructure
**Project:** PedagogyX

## Infrastructure Overview

- **Current architecture:** Hybrid Edge-Cloud (D-PROC=C) architecture designed for resilience in low-connectivity K-12 environments. The system relies on lightweight, client-side capture on zero-cost hardware (Android/Windows smartboards) coupled with a massive, centralized inference engine.
- **Environment topology:** Local development utilizes `infra/compose.dev.yaml` for parity. Upstream environments progress through isolated CI, ephemeral staging namespaces, and a fully robust production footprint anchored in `ap-south-1` (Mumbai) to strictly enforce DPDP residency compliance.
- **Deployment model:** 100% Declarative Infrastructure as Code (IaC) via Terraform and Kubernetes manifests. Zero-touch, fully automated GitOps deployments (ArgoCD/Flux). No manual ssh access to production nodes is permitted.
- **Operational goals:** Achieve 99.99% availability for API components, ensure completely automated failure recovery, enforce immutable and reproducible infrastructure state, and scale down aggressively to zero during non-school hours to meet stringent ₹0 client hardware budget constraints.

## CI/CD Architecture

- **Pipeline structure:** Trunk-based development gating with GitHub Actions. Pipelines validate formatting, linting (e.g., `prettier`, `black`, `isort`, `flake8` enforced via `./scripts/dev-verify.sh`), test coverage, container immutability, and security scans prior to merge.
- **Automation strategy:** Continuous integration executes deterministic test environments. Artifacts are built once, signed, and promoted through environments. Local setups leverage `./scripts/compose-smoke.sh` for integration tests.
- **Deployment flow:** GitOps-driven continuous deployment via ArgoCD. Image updates automatically trigger rollouts via Helm charts across the cluster fleet, applying Blue/Green and Canary deployment models to minimize deployment blast radius.
- **Rollback mechanisms:** Automated, telemetry-driven rollbacks using progressive delivery mechanisms (Flagger). If an error rate or latency SLI breaches a threshold during a canary rollout, the system instantly reverts to the `n-1` known-good state without manual intervention.

## Cloud Infrastructure

- **Cloud services:** Self-hosted, cloud-agnostic OSS ecosystem ensuring complete independence from vendor lock-in. Compute relies on high-availability node pools spanning multi-AZ VPCs, strictly partitioned between general-purpose instances and specialized RTX 5070 GPU nodes for model inference (faster-whisper, YOLO, Ollama).
- **Networking:** Hub-and-spoke VPC topology with deep network isolation. Public ingress is routed exclusively through API Gateways/WAFs into public subnets, proxying to strictly private application and database subnets. Zero trust communication with mutual TLS (mTLS) enforced.
- **Infrastructure layout:** WebRTC/RTMP proxies terminate edge traffic, queuing AV streams into distributed message brokers (Kafka/Redis). Stateless Python-based FastAPI services handle orchestration while containerized ML workers process queue batches. Long-term object storage relies on S3-compatible endpoints (MinIO), and metadata resides in highly-available PostgreSQL.
- **Scaling architecture:** Event-driven horizontal autoscaling decoupled from CPU limits, instead relying on queue depths (KEDA) to proportionally spin up ML workers. Ensures optimal queue processing while limiting GPU idle time.

## Kubernetes Architecture

- **Cluster topology:** Highly Available Multi-AZ Kubernetes control plane. Segmented node groups: dedicated ingress/egress nodes, high-memory datastore nodes, and GPU-enabled inference nodes via device plugins.
- **Deployment strategy:** Helm-based parameterized deployments managed by GitOps controllers. Workloads deploy with Anti-Affinity rules to ensure Pod distribution across distinct availability zones to survive node or zone failures.
- **Autoscaling:** Cluster Autoscaler manages the underlying compute nodes, dynamically provisioning GPU instances when KEDA scales ML worker deployments past current cluster capacity, and tearing them down when queues are depleted.
- **Ingress architecture:** Ingress-Nginx or Traefik horizontally scaled ingress controllers handling strict TLS 1.3 termination, rate-limiting, and distributed WAF inspection before routing traffic inside the cluster.

## Observability Stack

- **Metrics:** Prometheus operating in a highly available clustered mode scraping node-exporter, kube-state-metrics, cAdvisor, and custom application metrics (e.g., VRAM utilization, inference queue latency, ingestion throughput).
- **Logging:** Centralized log aggregation via the LGTM stack (Loki, Grafana, Promtail) or Fluent-Bit to Elasticsearch. All logs enforce strict PII scrubbing before indexing. Retentions are aggressively lifecycle-managed to optimize storage costs.
- **Tracing:** End-to-end OpenTelemetry distributed tracing correlating edge capture timestamps, API ingestion, queue wait times, and inference processing times, enabling instant root-cause analysis for any latency degradation.
- **Alerting:** Alertmanager integrated with PagerDuty and Slack. Alerts are strictly curated to prevent fatigue—triggering only on actionable SLI/SLO breaches (e.g., 5xx error rate spikes, queue age exceeding SLA, node failure rates).

## Security Architecture

- **IAM:** Principle of Least Privilege (PoLP) strictly enforced across Cloud IAM and Kubernetes RBAC. Kubernetes Service Accounts are tied directly to scoped Cloud IAM roles via OIDC, preventing broad access tokens.
- **Secret management:** HashiCorp Vault or AWS Secrets Manager / External Secrets Operator natively syncing into Kubernetes namespaces as ephemeral secrets. Zero static credentials in repositories; all secrets are rotated automatically.
- **Network security:** Strict Kubernetes NetworkPolicies default to deny-all, explicitly allow-listing namespace/pod communications. Cloud environments utilize Security Groups/Firewalls restricting egress traffic. All intra-cluster traffic relies on mTLS (e.g., via Istio or Linkerd).
- **Vulnerability management:** Trivy or Clair integrated into CI pipelines scanning container registries. Automatic blocking of image promotions containing critical or high CVEs. Infrastructure compliance scanned via Checkov or tfsec.

## Reliability Strategy

- **Redundancy:** N+2 redundancy on all critical paths. Database clusters utilize active-passive synchronous replication (e.g., Patroni for PostgreSQL) to prevent split-brain and ensure zero data loss.
- **Failover:** Automated leader elections across distributed systems. Stateless proxy/ingest nodes dynamically load-balance away from unresponsive peers instantly.
- **Disaster recovery:** Automated cross-region backups for relational databases and object storage. Infrastructure codified in Terraform ensures complete, automated secondary-region restoration (RTO < 4 hours, RPO < 5 minutes) in a catastrophic failure event.
- **Self healing mechanisms:** Comprehensive Kubernetes liveness/readiness probes. Pods that deadlock or leak memory are automatically aggressively restarted. Edge clients feature offline buffering to mitigate transient network drops before uploading to the cloud.

## Cost Optimization

- **Infrastructure savings:** Full open-source stack (OSS) eliminates enterprise licensing costs. Utilizing spot instances / preemptible VMs for fault-tolerant, stateless worker queues, while maintaining on-demand nodes exclusively for critical databases.
- **Resource optimization:** Rigorous namespace resource quotas and pod requests/limits tuning via Vertical Pod Autoscaler (VPA) recommendations. Over-provisioning is aggressively minimized to reduce cloud spend.
- **Scaling efficiency:** Custom batching logic at the ML queue level ensures maximum GPU VRAM utilization on RTX 5070 constraints. Nodes scale down to zero on weekends and nights, dramatically lowering operational burn rates.

## Risks & Bottlenecks

- **Operational risks:** Network volatility across Indian K-12 environments causing large, unpredictable bursts of ingestion traffic. This is mitigated through resilient, distributed rate-limiting and asynchronous queueing.
- **Scaling limitations:** Database connection exhaustion and locking contention during high concurrency. Addressed through connection poolers (PgBouncer) and read-replicas.
- **Security risks:** Regulatory non-compliance (DPDP) and potential leakage of unanonymized minors' PII. Addressed by enforcing strict encryption at rest and in transit, and restricting physical infrastructure access strictly to the India region.
- **Deployment risks:** A misconfiguration in GitOps could propagate cluster-wide instantly. Mitigated by strict progressive delivery (canary rollouts), comprehensive smoke tests (`compose-smoke.sh`), and mandatory peer approvals.

## Agile Sprint Plan

- **Implementation phases:**
  - _Sprint 01:_ Establish foundational Terraform for base network (VPC) and cluster provisioning in ap-south-1.
  - _Sprint 02:_ Implement core GitOps continuous deployment loop (ArgoCD/Flux) with baseline OSS ingest/worker deployments.
  - _Sprint 03:_ Deploy fully configured observability suite (Prometheus, Loki, OpenTelemetry) and validate custom ML queuing metrics.
  - _Sprint 04:_ Configure robust KEDA-based autoscaling rules for GPU workloads and test dynamic scale-to-zero capabilities.
  - _Sprint 05:_ Conduct complete chaos engineering and disaster recovery simulation (simulated AZ loss, DB failover).
- **Priorities:** Immediate prioritization of fully automated infrastructure provisioning, airtight security boundaries, and deep observability.
- **Milestones:** Zero-touch cluster provisioning; fully automated canary deployments; validated autoscaling on synthetic classroom loads.
- **Expected operational improvements:** Complete elimination of configuration drift, profound reduction in deployment-related incidents, highly optimized cloud spend aligned with zero-cost models, and rapid MTTR for arbitrary infrastructure failures.
