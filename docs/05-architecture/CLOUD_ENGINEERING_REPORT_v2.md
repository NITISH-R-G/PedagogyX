# Cloud Engineering Report

## Cloud Problem Analysis

### Business Requirements

PedagogyX requires a robust, self-hosted, open-source-first cloud platform capable of processing multi-modal classroom data. The system must support real-time "hot path" inference (talk ratio estimation, activity detection) and a "cold path" for heavy batch processing (full transformer fusion, pedagogy indexing). Strict India data residency requirements mandate deploying the centralized backend in an India-based cloud with school LAN or edge node ingestion.

### Scale Assumptions

The primary capture devices in v1 are Meta Ray-Ban smart glasses via an Android capture app, alongside low-end Windows smartboards. Hundreds of classrooms per district will continuously stream real-time audio and intermittent video/screen chunks. The edge nodes will aggregate these streams and buffer uploads to the centralized cloud over varying WAN connections.

### Operational Constraints

The compute budget is highly constrained, specifically relying on consumer-grade RTX 5070 GPUs for ML workloads to maintain cost-efficiency. Cloud infrastructure must accommodate varying network conditions at the edge, requiring robust backpressure, resumable uploads, and local buffering.

### Failure Scenarios

- Partial or total WAN disconnection at the school edge node.
- Spiky upload bursts saturating ingress API gateways.
- GPU worker node failure during heavy cold-path batch processing.
- Multi-stream synchronization drift due to packet loss or clock skew.

## Cloud Architecture

### Infrastructure Topology

PedagogyX will operate a hybrid edge-to-cloud topology.

- **Edge Layer:** District or school-local hybrid ingest nodes handling WebRTC SFU and buffering.
- **Central Cloud:** An India-based region running the control plane and data plane.
- **Data Plane:** Centralized processing cluster managing GPU workers, PostgreSQL for metadata/scoring, and MinIO for durable object storage.

### Cloud Services

- **Ingress & Routing:** MediaMTX for media stream ingest, coupled with an API Gateway (Go-based) for high-throughput buffering and request routing.
- **Compute:** Managed Kubernetes cluster (or robust VM scale sets) orchestrating containerized edge-feature workers and cold-path batch ML fusion workers.
- **Storage:** MinIO object store for media chunk archiving, and highly available PostgreSQL for tenant and pedagogy score data.
- **Messaging:** Redis for job queue management and Dead Letter Queue (DLQ) implementation.

### Networking

- **Edge-to-Cloud WAN:** Encrypted transport over TLS/HTTPS with resumable chunked upload capabilities.
- **Intra-Cloud:** Container-native service mesh for internal component communication (API gateway to job queues to GPU workers).

### Deployment Layout

Infrastructure is segregated into namespaces/zones separating the real-time hot path components from the resource-intensive batch processing cold path. GPU nodes are isolated in dedicated auto-scaling node pools.

## Infrastructure Automation

### IaC Strategy

The entire cloud infrastructure will be defined using declarative Infrastructure as Code (Terraform or Pulumi) to ensure reproducibility, version control, and immutability across staging and production environments.

### Provisioning Workflows

Automated pipelines will provision Kubernetes clusters, configure auto-scaling groups, deploy MinIO buckets, and set up PostgreSQL replication. Node pools for RTX 5070-equivalent GPUs will be dynamically scaled.

### Deployment Automation

GitOps workflows (e.g., using ArgoCD or Flux) will automatically sync container image updates from the container registry to the Kubernetes cluster, enabling automated rollouts and rollbacks without manual intervention.

### Environment Management

Clear separation between development, staging, and production environments using distinct cloud accounts or strict VPC isolation. All infrastructure changes must pass CI validation before being applied to production.

## Networking Architecture

### VPC Layout

The cloud environment will feature a multi-tier VPC architecture:

- **Public Subnets:** Load balancers, API Gateways, and WebRTC SFU/MediaMTX endpoints.
- **Private Subnets:** Control plane, API servers, GPU worker pools.
- **Isolated Data Subnets:** PostgreSQL clusters, Redis queues, and MinIO storage (accessible only from approved private subnet security groups).

### Ingress and Egress

- **Ingress:** Handled via highly available layer 7 Application Load Balancers, routing traffic to API gateways and MediaMTX.
- **Egress:** NAT gateways configured in public subnets to allow private worker nodes to pull updates or external FOSS models, heavily restricted by egress firewall rules.

### Load Balancing

API traffic and media uploads will be distributed across multiple stateless gateway instances. Long-lived streaming connections (WebRTC) will use consistent hashing or dedicated stream routing to maintain session state.

### DNS Strategy

Geo-DNS routing will not be initially required since data residency restricts the central cloud to India. Standard highly available cloud DNS will manage service discovery and public endpoint resolution.

## Reliability Strategy

### Failover Systems

Stateless API and worker nodes will utilize auto-scaling groups spanning multiple availability zones. If a zone degrades, traffic will automatically shift to healthy instances.

### Redundancy

PostgreSQL will operate in a primary-replica configuration with automated synchronous (or near-synchronous) failover. MinIO will be deployed in a distributed mode with erasure coding to protect against disk and node failures.

### Disaster Recovery

Daily automated snapshots of the PostgreSQL database and asynchronous replication of MinIO object storage to a secondary regional backup vault. Clear RTO and RPO targets will be defined for state restoration.

### Self Healing Mechanisms

Kubernetes liveness and readiness probes will automatically restart failed or deadlocked containers. Background workers pulling from Redis will implement strict Dead Letter Queues (DLQ) with raw payload retention to ensure no captured media is lost due to transient ML processing errors.

## Security Architecture

### IAM

Strict Least Privilege Access will be enforced across all cloud services. Machine identities (service accounts) will be used for inter-service communication rather than hardcoded credentials.

### Encryption

- **In Transit:** All external and cross-region internal traffic will be encrypted using TLS 1.3.
- **At Rest:** MinIO buckets and PostgreSQL volumes will utilize AES-256 encryption using a centralized Key Management Service (KMS).

### Secrets Management

Secrets, database credentials, and API keys will be managed using a secure vault solution (e.g., HashiCorp Vault or cloud-native secrets manager) and injected into workloads at runtime.

### Network Security

Zero Trust principles will guide network security. Strict Security Groups and Network Policies will enforce default-deny rules, allowing only explicitly required communication paths between microservices.

## Observability

### Monitoring

System-level metrics (CPU, memory, GPU utilization, disk I/O) and application-level metrics (queue depth, hot-path latency) will be continuously gathered using Prometheus.

### Logging

Centralized structured logging will aggregate logs from all edge clients, API gateways, and GPU workers into a unified log aggregation system (e.g., ELK stack or Grafana Loki).

### Tracing

Distributed tracing (e.g., OpenTelemetry) will track requests from edge ingestion through the API gateway to the final asynchronous background worker, providing critical visibility into media processing bottlenecks.

### Alerting

Actionable alerts will be configured in Grafana/Alertmanager for critical thresholds (e.g., Redis queue backlog exceeding limits, GPU node unreachability, API error rate spikes).

## Performance and Cost Optimization

### Autoscaling

Compute resources will scale dynamically based on custom metrics, specifically scaling GPU worker node pools based on Redis job queue depth rather than simple CPU utilization.

### Resource Optimization

GPU workloads will be heavily optimized to maximize the RTX 5070 compute budget. Batch processing will run during off-peak hours (cold path) to flatten the compute utilization curve and reduce peak infrastructure sizing requirements.

### Caching

A caching layer will be implemented for read-heavy administrative dashboard queries, reducing the load on the primary PostgreSQL database for historical pedagogy scores.

### Infrastructure Efficiency

Spot or preemptible instances will be utilized for the cold-path batch processing pool where asynchronous execution and resumable state allow for node interruption without data loss.

## Risks and Tradeoffs

### Operational Risks

Operating a self-hosted FOSS AI stack introduces significant maintenance overhead compared to managed AI APIs. Keeping GPU drivers, CUDA toolkits, and inference engines updated across the cluster requires a high degree of operational maturity.

### Scaling Concerns

Spiky WAN ingestion patterns from synchronized class schedules (e.g., all classrooms ending and uploading chunks simultaneously) may overwhelm API gateways or network ingress bandwidth if backpressure is not aggressively managed.

### Vendor Tradeoffs

The India data residency requirement limits cloud vendor selection. We must ensure the chosen provider offers robust managed Kubernetes and GPU instance availability.

### Cost Implications

Sustaining a dedicated pool of RTX 5070-equivalent GPUs for processing is highly cost-sensitive. Careful tuning of the hot-path vs. cold-path processing ratio is required to prevent compute costs from scaling linearly with classroom adoption.

## Agile Sprint Plan

### Milestones

- **Sprint 1:** Provision foundation cloud infrastructure (VPC, EKS/K8s cluster, managed PostgreSQL) using Terraform.
- **Sprint 2:** Deploy MinIO distributed cluster and MediaMTX/API Gateway ingress layer with robust TLS.
- **Sprint 3:** Implement background worker architecture (Redis queues, DLQ patterns) and deploy initial GPU worker node pool.
- **Sprint 4:** Roll out comprehensive observability stack (Prometheus, Loki, OpenTelemetry) and configure alerting for failure scenarios.

### Implementation Phases

1. **Foundation & Security:** Establish secure network boundaries and IAM roles.
2. **Data Services:** Stand up and validate durable storage (DB and object store).
3. **Compute & Ingest:** Deploy the API gateway and auto-scaling compute pools.
4. **Operations & Observability:** Integrate logging, tracing, and metrics dashboards.

### Priorities

1. Reliability of the edge-to-cloud media ingestion and buffering pipeline.
2. Cost-efficient autoscaling of the GPU batch processing pool.
3. Strict adherence to security and data residency compliance.

### Expected Infrastructure Improvements

- Resilient, fully automated infrastructure deployment from scratch.
- Highly observable processing pipeline enabling rapid bottleneck identification.
- Drastic reduction in manual operational overhead through GitOps and IaC.
