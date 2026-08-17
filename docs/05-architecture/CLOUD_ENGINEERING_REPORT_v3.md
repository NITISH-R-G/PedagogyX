# Cloud Engineering Report

## Cloud Problem Analysis

- **Business Requirements:** PedagogyX requires an enterprise-grade, highly reliable, scalable, and open-source-first cloud platform capable of ingesting and processing multimodal classroom data. The system must support real-time "hot path" inference (e.g., talk ratio estimation, active speaker detection) and a "cold path" for heavy batch processing (e.g., full transformer fusion, deep pedagogical analysis) while strictly adhering to India data residency regulations (DPDP Act).
- **Scale Assumptions:** The primary endpoints will be edge capture devices like Meta Ray-Ban smart glasses (via Android capture DAT apps) and lightweight Windows smartboards. Hundreds of classrooms per district will continuously stream real-time audio and intermittent video/screen chunks. These streams will be aggregated at edge nodes, which will buffer uploads to the centralized India-based cloud over diverse WAN connections.
- **Operational Constraints:** Compute budgets are extremely constrained, necessitating the reliance on consumer-grade RTX 5070 GPUs for ML inference tasks to maintain unit economics. Infrastructure must transparently handle intermittent connectivity, requiring robust backpressure, guaranteed resumable uploads, and local buffering mechanisms without data loss.
- **Failure Scenarios:** Total or partial WAN disconnections at edge ingestion sites, spiky upload bursts causing API ingress saturation at end-of-class times, GPU worker node failures during long-running batch jobs, and multi-stream synchronization drift due to packet loss or clock skew at the edge.

## Cloud Architecture

- **Infrastructure Topology:** A Hybrid Edge-Cloud deployment. Edge nodes (district/school level) handle immediate WebRTC SFU and local buffering. The centralized Data Plane (India region) orchestrates scalable GPU compute workers, highly available data storage, and the control plane API.
- **Cloud Services:** Ingress traffic is handled by highly available Application Load Balancers and MediaMTX for media routing, backed by an auto-scaling API Gateway. Core data services include PostgreSQL for metadata and scoring, MinIO for durable, S3-compatible media chunk storage, and Redis for highly available event and job queueing.
- **Networking:** All Edge-to-Cloud communication utilizes TLS 1.3 encrypted HTTPS. Intra-cluster communication utilizes a container-native service mesh enforcing mTLS, ensuring strict isolation between the API gateway, job queues, and the GPU worker pools.
- **Deployment Layout:** Real-time hot-path API services and data tiers are segregated into isolated high-availability node pools, while cold-path ML workloads run on dedicated, dynamically scaling RTX 5070 GPU node pools isolated from core API ingress points.

## Infrastructure Automation

- **IaC Strategy:** The entire infrastructure lifecycle is managed via declarative Infrastructure as Code (Terraform), guaranteeing absolute immutability and reproducibility across development, staging, and production environments, eliminating configuration drift.
- **Provisioning Workflows:** CI/CD pipelines automatically provision and orchestrate Kubernetes clusters, auto-scaling groups (ASGs), MinIO buckets, and highly available PostgreSQL clusters. GPU node pools are dynamically provisioned on demand.
- **Deployment Automation:** Fully automated GitOps continuous deployment utilizing ArgoCD. Configuration changes merged into the mainline branch are automatically reconciled with the cluster state, enforcing declarative deployment logic.
- **Environment Management:** Strict isolation of environments utilizing distinct AWS/Cloud provider accounts and VPCs. All changes undergo rigorous CI validation, security scanning (Trivy, tfsec), and testing before automated progression to production.

## Networking Architecture

- **VPC Layout:** A multi-tier Hub-and-Spoke VPC model. Public subnets host WAF-protected load balancers and MediaMTX endpoints. Private subnets secure control planes, API services, and GPU workers. Isolated Data Subnets strict-lock PostgreSQL, Redis, and MinIO storage arrays behind aggressive Security Groups.
- **Ingress/Egress:** Layer 7 ALBs handle ingress and distribute traffic across stateless API gateways. Egress traffic is routed through strictly controlled NAT gateways, restricted by explicit firewall rules to only allow required updates or model downloads.
- **Load Balancing:** API request traffic and multi-part chunk uploads are load-balanced across stateless ingestion pods. Long-lived media streams utilize consistent hashing to ensure session persistence across ephemeral WebRTC routing nodes.
- **DNS Strategy:** High-availability cloud DNS routing handles service discovery. Since data residency strictly bounds the deployment to India (`ap-south-1` equivalent), geo-routing is omitted in favor of robust zonal failover records.

## Reliability Strategy

- **Failover Systems:** Stateless API tiers and worker pods deploy across multiple Availability Zones (AZs). Active-passive synchronous replication is enforced for PostgreSQL and Redis; failover is entirely automated to prevent split-brain degradation.
- **Redundancy:** N+2 redundancy enforced across stateless control-plane architectures. MinIO utilizes distributed erasure coding to guarantee media chunk survival against multiple concurrent disk or node failures.
- **Disaster Recovery:** Automated, cross-region backups of database WALs and MinIO states. Strict RTO (Recovery Time Objective) and RPO (Recovery Point Objective) metrics govern automated state restoration workflows via Terraform.
- **Self Healing Mechanisms:** Aggressive Kubernetes liveness and readiness probes instantly terminate deadlocked containers. Background workers utilize strict Dead Letter Queues (DLQs) with raw payload retention to ensure no telemetry or insights are dropped during transient failures.

## Security Architecture

- **IAM:** Strict Principle of Least Privilege. Kubernetes Service Accounts are explicitly bound to granular Cloud IAM roles via OIDC/Workload Identity, entirely eliminating hardcoded credential risks.
- **Encryption:** Encryption-in-transit via TLS 1.3 is universally enforced. Encryption-at-rest utilizes AES-256 for MinIO volumes and PostgreSQL storage, managed by a centralized Key Management Service (KMS).
- **Secrets Management:** Secrets are dynamically injected into running workloads via HashiCorp Vault or External Secrets Operator, ensuring credential rotation is seamless and invisible to application logic.
- **Network Security:** Zero Trust network architecture enforced via Kubernetes Network Policies. A strict default-deny paradigm allows only explicitly defined microservice-to-microservice communication.

## Observability

- **Monitoring:** High-availability Prometheus architectures continuously scrape granular metrics across the stack, tracking CPU, VRAM utilization, network throughput, and Redis queue depth.
- **Logging:** Centralized structured logging architecture utilizing Loki (LGTM stack) ingests telemetry from Edge clients, API gateways, and GPU inference workers, ensuring long-term auditability.
- **Tracing:** OpenTelemetry (OTel) traces request lifecycles from the initial client WebRTC upload, through API Gateway buffering, into the Redis queue, and finally out to the asynchronous asynchronous ML worker, pinpointing latency bottlenecks instantly.
- **Alerting:** Alertmanager dynamically routes symptom-based alerts to on-call engineers. Alerts are tied strictly to SLO breaches (e.g., API availability, queue saturation) rather than static CPU thresholds, minimizing alert fatigue.

## Performance & Cost Optimization

- **Autoscaling:** KEDA (Kubernetes Event-driven Autoscaling) directly targets custom Redis queue depth metrics to scale Horizontal Pod Autoscalers. GPU compute spins up exclusively when the inference backlog dictates, dropping to absolute zero when idle.
- **Resource Optimization:** ML pipelines are hyper-optimized via quantization (e.g., AWQ/GPTQ) to fit complex transformer fusion models inside the 12GB VRAM constraints of consumer-grade RTX 5070s.
- **Caching:** Aggressive Redis caching layers protect the primary PostgreSQL cluster from read-heavy administrative dashboard queries, allowing the database to scale efficiently under write-heavy classroom inference loads.
- **Infrastructure Efficiency:** Asynchronous cold-path inference queues aggressively leverage spot/preemptible instances, taking advantage of their transient nature via resumable processing state to drive down the total cost of compute.

## Risks & Tradeoffs

- **Operational Risks:** Operating custom Kubernetes clusters atop consumer-grade GPUs requires substantial operational maturity regarding drivers, CUDA versioning, and node provisioning compared to managed Datacenter A100/H100 APIs.
- **Scaling Concerns:** The primary scaling threat remains massive "thundering herds" of delayed payloads hitting the ingress Gateway simultaneously when school WAN connections restore. API limits and backpressure mechanisms must perfectly buffer these spikes.
- **Vendor Tradeoffs:** Total adherence to OSS-first and India data residency forces reliance on specific cloud vendors within the region, potentially sacrificing specialized hyperscaler proprietary tools for long-term portability and cost control.
- **Cost Implications:** While RTX 5070s drastically reduce unit economics, sustaining a highly available control plane and redundant database architecture introduces baseline fixed costs that must be amortized over a high volume of active classrooms.

## Agile Sprint Plan

- **Phase 1: Foundation & Resiliency:** Provision core declarative infrastructure modules (Terraform) establishing highly available VPCs, EKS/K8s clusters, and PostgreSQL/Redis primitives.
- **Phase 2: Ingestion & Storage:** Deploy MinIO distributed clusters and MediaMTX/API Gateway stateless tiers with robust auto-scaling and TLS ingress routing.
- **Phase 3: Asynchronous Scalability Engineering:** Implement KEDA autoscaling based on Redis queue depths, tuning the rapid provisioning and aggressive tear-down of the RTX 5070 GPU worker nodes.
- **Phase 4: Optimization & Observability:** Roll out full OpenTelemetry distributed tracing and Loki logging. Perform chaos engineering simulations to validate DLQ integrity and failover reliability during artificial load spikes.
