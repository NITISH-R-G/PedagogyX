# Advanced Cloud Architecture Report

**Version:** 1.0
**Role:** Senior Cloud Engineer & Cloud Infrastructure Architect
**Context:** PedagogyX - Multimodal AI classroom intelligence platform

## Cloud Problem Analysis

- **Business Requirements:** The platform must provide scalable, real-time AI classroom intelligence (supervision mode via Admin dashboards) targeting the Indian K-12 and University market. A paramount constraint is strict compliance with the Digital Personal Data Protection Act (DPDP), mandating robust data sovereignty and privacy.
- **Scale Assumptions:** The system expects to handle district-wide traffic patterns concurrently, equating to thousands of continuous audio/video WebRTC streams and batch payload uploads from distributed edge devices during school hours.
- **Operational Constraints:** A strict ₹0 customer hardware budget (D-10) necessitates a Hybrid Edge-Cloud architecture (D-PROC=C). Low-end production clients (Android/Windows smartboards) will only handle capture and encoding, offloading heavy ML processing (faster-whisper, YOLO+TensorRT, Ollama) to a central cloud inference pool. We must rely exclusively on OSS, self-hosted solutions, avoiding proprietary cloud APIs.
- **Failure Scenarios:** Must anticipate flaky edge networking (dropped uploads, incomplete streams), single-node GPU hardware failures, traffic spikes during lesson transitions, and regional data center outages.

## Cloud Architecture

- **Infrastructure Topology:** A Hybrid Hub-and-Spoke model where low-end edge clients (spokes) securely transmit encrypted media to a highly available, centralized Indian datacenter (hub).
- **Cloud Services:** Bare-metal or cost-optimized cloud instances acting as Kubernetes worker nodes. Dedicated GPU node pools equipped with 12GB VRAM class GPUs (e.g., RTX 5070) for ML inference. General compute pools for API services, data ingestion, and administration dashboards.
- **Networking:** Strict logical separation using Kubernetes namespaces and VPC subnets. Ingestion traffic hits edge load balancers, is quickly buffered into MinIO (S3-compatible), and queues are populated in Redis/Kafka for asynchronous worker consumption.
- **Deployment Layout:** Stateless web and API tiers deployed across multiple availability zones (AZs) where supported by the provider. Stateful components (Postgres, MinIO, Redis) deployed with high-availability configurations (e.g., Patroni for Postgres).

## Infrastructure Automation

- **IaC Strategy:** 100% declarative infrastructure using Terraform to provision VMs, networking, and base clusters. No manual configuration via UI consoles.
- **Provisioning Workflows:** Ansible used to bootstrap bare-metal/VM instances with required NVIDIA drivers and Kubernetes (K3s/RKE2) runtimes securely.
- **Deployment Automation:** ArgoCD driving a pure GitOps workflow. Application deployments, ConfigMaps, and infrastructure manifests are continuously synced from the GitHub monorepo.
- **Environment Management:** Completely reproducible environments (`dev`, `staging`, `prod`) driven by parameterized Kustomize or Helm charts, enabling ephemeral test environments on demand.

## Networking Architecture

- **VPC Layout:** Private VPCs with no direct public IP assignments for worker or database nodes. All external traffic routes through highly available NAT gateways and Ingress controllers.
- **Ingress/Egress:** Traefik or NGINX Ingress controllers acting as the API gateway, terminating TLS, and enforcing WAF rules and rate limiting.
- **Load Balancing:** Layer 4/Layer 7 load balancing distributing traffic across API ingestion pods.
- **DNS Strategy:** Geo-fenced DNS routing ensuring all Indian traffic remains within local infrastructure to guarantee DPDP compliance.

## Reliability Strategy

- **Failover Systems:** Stateless components scale horizontally and auto-recover via Kubernetes ReplicaSets. Stateful clusters (Postgres, MinIO) configured with automatic leader election and failover.
- **Redundancy:** Multi-node storage arrays and message queues. N+1 redundancy in the GPU worker pool to absorb node failures transparently.
- **Disaster Recovery:** Automated, encrypted continuous backups of Postgres WALs and MinIO critical buckets to cold offsite object storage. RPO < 15 mins, RTO < 4 hours.
- **Self Healing Mechanisms:** Aggressive Kubernetes Liveness and Readiness probes. Pod disruption budgets to guarantee minimum availability during cluster upgrades.

## Security Architecture

- **IAM:** Strict Role-Based Access Control (RBAC) in Kubernetes. Principle of least privilege enforced across all service accounts.
- **Encryption:** AES-256 for all data at rest (MinIO, Postgres). Enforced TLS 1.3 for all data in transit. Mutual TLS (mTLS) for internal microservice communication via a service mesh if complexity warrants it.
- **Secrets Management:** Integration with HashiCorp Vault or SOPS for encrypted secret management in GitOps. Zero hardcoded credentials in the repository.
- **Network Security:** Kubernetes Network Policies explicitly whitelisting traffic between namespaces (e.g., Web tier cannot directly query Postgres, only the API tier can).

## Observability

- **Monitoring:** Centralized Prometheus scraping node exporters, cAdvisor, and custom app metrics. Dashboards in Grafana visualizing GPU VRAM utilization, queue depths, and API latency.
- **Logging:** Promtail collecting structured JSON logs from all containers, shipping to Loki for centralized, high-performance querying without the heavy overhead of Elasticsearch.
- **Tracing:** OpenTelemetry (OTel) instrumentation across the stack to trace requests from Edge upload through API ingestion to asynchronous GPU inference.
- **Alerting:** Alertmanager routing critical incidents to PagerDuty/Slack based on actionable thresholds (e.g., `Queue Length > 1000`, `Node Offline`, `GPU OOM`).

## Performance & Cost Optimization

- **Autoscaling:** KEDA (Kubernetes Event-driven Autoscaling) configured to scale the GPU worker deployments dynamically based on queue depth (Redis/Kafka), ensuring we don't idle expensive GPU resources while meeting SLA targets.
- **Resource Optimization:** Granular Kubernetes requests and limits defined for all workloads. ML workloads packed tightly to maximize RTX 5070 12GB VRAM utilization.
- **Caching:** Aggressive edge and API caching via Redis to offload repetitive Admin UI queries and static data, protecting the database.
- **Infrastructure Efficiency:** Strict object lifecycle management in MinIO to automatically delete raw media files post-processing and DPDP retention periods, slashing storage costs.

## Risks & Tradeoffs

- **Operational Risks:** Relying on low-end, generic cloud providers in India for DPDP compliance may reduce availability compared to AWS/GCP. Mitigation: Robust app-layer retries and high internal redundancy.
- **Scaling Concerns:** Synchronous real-time feedback is constrained by GPU cold-start times. Mitigation: Asynchronous batch processing is prioritized for MVP; real-time features require dedicated, pre-warmed models.
- **Vendor Tradeoffs:** Complete OSS and self-hosted stack prevents vendor lock-in and controls costs, but significantly increases the operational burden and maintenance responsibilities of the platform engineering team.
- **Cost Implications:** Batching workloads allows high utilization of a smaller GPU pool, keeping costs low to support the ₹0 customer budget, but at the expense of near-real-time feedback latency.

## Agile Sprint Plan

- **Milestones:**
  - Milestone 1: Automated provisioning of the core Kubernetes cluster and network foundations.
  - Milestone 2: Deployment of stateful backing services (Postgres, Redis, MinIO) with persistence.
  - Milestone 3: CI/CD GitOps pipeline integration and observability stack deployment.
  - Milestone 4: Scaling logic and GPU node pool configuration for worker-asr workloads.
- **Implementation Phases:**
  - **Sprint 1 (Current):** Refine Terraform modules for VPC and Base VM provisioning. Setup K3s/RKE2 via Ansible.
  - **Sprint 2:** ArgoCD installation. Declarative deployment of Prometheus, Loki, and Traefik.
  - **Sprint 3:** Deploy API, Web, and Stateful data tiers via GitOps. Implement automated secrets management.
  - **Sprint 4:** Configure KEDA autoscaling based on queue metrics. Perform load testing against the GPU inference cluster.
- **Priorities:** Stability and Observability first. Ensure we can monitor the stack completely before deploying expensive machine learning workloads.
- **Expected Infrastructure Improvements:** Transitioning from local `docker-compose` to a fully automated, resilient, and observable Kubernetes cluster capable of handling production edge traffic.
