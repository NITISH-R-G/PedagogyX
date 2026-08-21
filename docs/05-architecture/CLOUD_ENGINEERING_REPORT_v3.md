# Cloud Engineering Report

## Cloud Problem Analysis

- **business requirements**: PedagogyX demands a self-hosted, scalable, open-source-centric platform for processing multimodal real-time classroom data (audio, video, whiteboard). Must adhere strictly to India data residency regulations (G2), demanding all central backend services and data reside on India-based cloud infrastructure with hybrid edge (school LAN) node ingestion.
- **scale assumptions**: The primary capture device is the Meta Ray-Ban smart glasses (ADR-0009), streaming heavily alongside lower-end Windows smartboards. A scale of hundreds of classrooms per district continuously uploading real-time audio and chunked media. Upload streams will traverse diverse WAN connections varying from robust fiber to fragile cellular networks.
- **operational constraints**: Heavy compute limitations strictly dictate the use of consumer-grade RTX 5070 GPUs for intensive ML tasks (e.g., full transformer fusion, pedagogy indexing) to maintain economic viability (Hybrid Edge/Cloud topology ADR-0008). Infrastructure must manage immense media payload backpressure, support resumable uploads, and buffer edge traffic efficiently without data loss.
- **failure scenarios**: Complete or partial WAN disconnections at the school edge node; massive traffic burst spikes saturating ingress gateways when classes end synchronously; unexpected node degradation or OOM errors on RTX 5070 GPUs during cold-path batch processing; time drift and synchronization failures among multiple classroom data streams.

## Cloud Architecture

- **infrastructure topology**: A Hybrid Edge/Cloud architecture (ADR-0008). The edge layer consists of school-local nodes handling WebRTC SFU, local buffering, and preliminary feature extraction. The centralized cloud in an India region hosts the control plane, database, deep learning clusters, and durable object storage.
- **cloud services**: Layer 7 API Gateways for request routing and backpressure handling; MediaMTX for robust real-time media ingestion; Kubernetes (managed or robust VM scale sets) orchestrating containerized edge-feature workers and cold-path AI batch workers; MinIO for high-performance S3-compatible durable object storage; PostgreSQL for metadata and scoring analytics.
- **networking**: Edge-to-cloud traffic utilizes secure TLS/HTTPS with robust chunking and resumption mechanisms. Intra-cloud traffic operates over a container-native service mesh ensuring isolated microservice communication (API gateways to message queues to GPU workers).
- **deployment layout**: Strong namespace and zone segregation dividing the real-time "hot path" components (ingestion, routing, fast inference) from the resource-heavy "cold path" (batch processing, data indexing). GPU worker nodes are fully isolated within dedicated auto-scaling pools.

## Infrastructure Automation

- **IaC strategy**: 100% declarative infrastructure utilizing Terraform. All state is managed remotely with strict versioning, ensuring identical, reproducible deployments across staging and production environments while preventing manual configuration drift.
- **provisioning workflows**: Automated CI/CD pipelines provision Kubernetes clusters, auto-scaling worker groups, managed databases, and MinIO storage arrays. RTX 5070 GPU node pools scale dynamically based on strict custom metrics from job queues.
- **deployment automation**: GitOps methodology driven by ArgoCD/Flux synchronizes state directly from repository definitions to the Kubernetes cluster, facilitating zero-downtime rollouts, automated health-check validations, and instant rollback capabilities.
- **environment management**: Complete isolation between development, staging, and production workloads using separate cloud accounts/VPCs. No direct human access to production environments; all changes pass through rigorous CI automated testing and peer review.

## Networking Architecture

- **VPC layout**: Multi-tier architecture. Public subnets host Load Balancers and ingress controllers (API Gateways, WebRTC endpoints). Private subnets secure the Kubernetes control plane, API microservices, and compute nodes. Isolated data subnets secure PostgreSQL clusters, Redis queues, and MinIO storage, restricting access solely to verified private subnets.
- **ingress/egress**: Highly Available Layer 7 Application Load Balancers manage ingress, executing TLS termination and routing to API gateways. Egress traffic is strictly controlled via NAT gateways with outbound firewall rules, permitting worker nodes to pull updates or models while blocking arbitrary external access.
- **load balancing**: Stateless API traffic and media chunk uploads distribute evenly across gateway instances. Long-lived media streams utilize stream-aware routing or consistent hashing to maintain persistent sessions without overwhelming specific nodes.
- **DNS strategy**: Managed highly-available Cloud DNS resolves services. Due to G2 India data residency requirements, initial deployment is single-region India, deferring complex Geo-DNS routing while maintaining readiness for multi-region active-active architectures if policy allows.

## Reliability Strategy

- **failover systems**: Stateless microservices deployed in multi-AZ auto-scaling groups ensure transparent traffic failover upon zone degradation. Core routing and API layers automatically shift traffic to healthy pods based on aggressive health checks.
- **redundancy**: PostgreSQL operates with synchronous (or near-synchronous) primary-replica architecture for rapid database failover. MinIO object storage is deployed with distributed erasure coding, safeguarding media archives against multiple concurrent drive or node failures.
- **disaster recovery**: Automated, continuous PostgreSQL snapshots and asynchronous replication of critical MinIO data to a secondary secure regional vault. Well-defined RPO and RTO procedures heavily tested via chaos engineering to validate state restoration capabilities.
- **self healing mechanisms**: Aggressive Kubernetes liveness and readiness probes automatically terminate and restart failing containers. Background job workers processing media chunks implement strict Dead Letter Queues (DLQ) in Redis, preventing transient ML processing errors from causing data loss, retaining raw payloads for manual intervention or automated retry.

## Security Architecture

- **IAM**: Stringent Least Privilege Access model. Granular machine identities and Service Accounts are utilized for all intra-service communication. Broad wildcard permissions are explicitly banned.
- **encryption**: In transit: TLS 1.3 enforced on all external and cross-region internal traffic. At rest: AES-256 encryption applied to all MinIO buckets, PostgreSQL volumes, and message queue storage via a centralized Key Management Service (KMS).
- **secrets management**: HashiCorp Vault (or cloud-native equivalent) securely injects dynamic credentials, database passwords, and API keys at runtime. Hardcoded secrets in code or environment variables are fundamentally prohibited.
- **network security**: Zero Trust architecture. Kubernetes Network Policies and VPC Security Groups enforce default-deny communication. Services may only communicate over explicitly allowed ports and protocols verified by mutual TLS (mTLS) where possible.

## Observability

- **monitoring**: Prometheus scrapes high-resolution metrics across infrastructure and application layers, tracking CPU, memory, GPU utilization, disk I/O, queue depths, and critical hot-path latencies.
- **logging**: Centralized, structured JSON logging pipelines route all logs from Meta Ray-Ban edge clients, API gateways, and cloud GPU workers into a highly available log aggregation cluster (e.g., Elasticsearch or Loki).
- **tracing**: OpenTelemetry provides distributed tracing, illuminating the complete lifecycle of a request from the edge device, through the ingestion tier, into the background Redis queues, and culminating at the asynchronous AI worker, rapidly identifying performance bottlenecks.
- **alerting**: Actionable, high-signal alerts configured in Alertmanager/Grafana thresholding critical events (e.g., Redis queue backlog breaches, GPU node unreachability, API error rate spikes). Designed explicitly to minimize alert fatigue.

## Performance & Cost Optimization

- **autoscaling**: Compute scales dynamically using custom metrics, specifically scaling GPU worker node pools based on Redis job queue depth and processing latency rather than rudimentary CPU load, maximizing the utilization of the constrained RTX 5070 budget.
- **resource optimization**: Heavy separation of hot vs. cold path workloads. Batch inference runs during off-peak hours to flatten compute demands, preventing linear cost scaling and avoiding peak-hour infrastructure bloat.
- **caching**: Redis caching layers accelerate read-heavy administrative dashboard queries, offloading historical pedagogy analytics queries from the primary PostgreSQL database to reduce compute load.
- **infrastructure efficiency**: Aggressive use of spot/preemptible instances for the cold-path batch processing tier, leveraging the asynchronous, resumable nature of the workloads to drastically cut compute costs without risking data loss.

## Risks & Tradeoffs

- **operational risks**: Maintaining a self-hosted FOSS AI stack demands extreme operational maturity to manage CUDA toolkits, driver updates, and GPU node stability compared to managed API services.
- **scaling concerns**: Burst traffic from synchronized school schedules (simultaneous class endings triggering massive uploads) risks saturating the ingress tier and WAN bandwidth, requiring aggressive, well-tested backpressure and edge-buffering mechanisms.
- **vendor tradeoffs**: G2 India data residency severely restricts cloud provider selection, limiting access to certain managed Kubernetes or advanced GPU services, placing more operational burden on the platform engineering team.
- **cost implications**: Running a sustained pool of RTX 5070 GPUs is inherently expensive. Balancing real-time inference demands against delayed batch processing is critical; failure to optimize this ratio will result in rapid cost overruns.

## Agile Sprint Plan

- **milestones**:
  - Sprint 1: Establish foundational secure cloud infrastructure (VPCs, IAM, EKS cluster, managed PostgreSQL) via Terraform.
  - Sprint 2: Deploy durable storage layer (MinIO) and robust ingress tier (MediaMTX, API Gateways) with resilient TLS.
  - Sprint 3: Implement background queuing architecture (Redis, DLQs) and provision the initial RTX 5070 GPU auto-scaling worker pools.
  - Sprint 4: Deploy the comprehensive observability suite (Prometheus, OpenTelemetry, Loki) and define critical alerting thresholds.
- **implementation phases**: Phase 1: Security & Networking Foundation. Phase 2: Data Persistence & Stateful Services. Phase 3: Compute Orchestration & Ingestion. Phase 4: Observability, Scaling, & Hardening.
- **priorities**:
  1. Guaranteed reliability and backpressure handling for edge-to-cloud media ingestion.
  2. Aggressive cost-efficient auto-scaling for the GPU batch processing tier.
  3. Strict, auditable adherence to G2 India data residency and security compliance.
- **expected infrastructure improvements**: Complete end-to-end automation of infrastructure via GitOps; a highly observable, resilient processing pipeline for multimodal data; elimination of manual deployment friction; drastically improved fault tolerance across the entire edge-to-cloud spectrum.
