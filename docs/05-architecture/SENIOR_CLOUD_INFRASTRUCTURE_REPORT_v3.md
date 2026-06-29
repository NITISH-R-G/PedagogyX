# Senior Cloud Infrastructure Architecture Report

## Cloud Problem Analysis

PedagogyX is transitioning from an MVP boilerplate—currently orchestrated via Docker Compose with local instances of PostgreSQL, Redis, and MinIO—into a scalable, production-ready cloud platform. The primary client is Meta Ray-Ban glasses capturing classroom data. The system must process high-throughput audio and visual data streams asynchronously (via `worker-asr`, `worker-cv`, and `worker-metrics`) while maintaining high availability, data sovereignty (especially given G2 compliance requirements for Indian schools), and low latency for the `api` and `web` frontend components. The architecture must anticipate regional failures, traffic spikes from concurrent classroom recordings, and potential cloud vendor outages, necessitating a highly available, distributed, and strictly isolated cloud infrastructure.

## Cloud Architecture

The target cloud architecture transforms the single-node containerized deployment into a distributed, horizontally scalable Kubernetes-based ecosystem (e.g., EKS or GKE).

- **Compute Layer**: The FastAPI (`api`) and Next.js (`web`) services will run as stateless deployments spanning multiple Availability Zones (AZs) behind managed Application Load Balancers. The worker services (`worker-asr`, `worker-cv`, `worker-metrics`) will be decoupled using an event-driven architecture with scalable node pools optimized for their specific computational profiles (e.g., GPU-enabled nodes for ASR and CV tasks once RTX 5070 constraints are removed).
- **Stateful Layer**: Local MinIO will be replaced with managed object storage (e.g., AWS S3) utilizing cross-region replication for durability. Local PostgreSQL and Redis will be migrated to highly available managed services (e.g., Amazon RDS Multi-AZ and Amazon ElastiCache) ensuring automated backups, failover, and scaling capabilities.

## Infrastructure Automation

We will implement declarative Infrastructure as Code (IaC) using Terraform to provision and manage the entire cloud footprint.

- **Provisioning Workflows**: Core infrastructure (VPCs, EKS clusters, RDS instances, IAM roles) will be managed via modularized Terraform configurations. State files will be secured remotely with state locking.
- **Environment Management**: Strict separation of Dev, Staging, and Production environments will be enforced at the AWS account or GCP project level to prevent accidental cross-contamination.
- **Deployment Automation**: We will adopt GitOps workflows (e.g., using ArgoCD) to synchronize Kubernetes manifests directly from repository commits. CI/CD pipelines via GitHub Actions will automatically test, build container images, and update manifest versions in a verifiable and reproducible manner.

## Networking Architecture

The networking topology will prioritize secure, segmented communication.

- **VPC Layout**: The infrastructure will be deployed within a dedicated VPC across at least 3 AZs. The VPC will be segmented into Public (for ALBs/NAT Gateways), Private (for EKS workloads), and Database subnets.
- **Ingress/Egress**: All external traffic will ingress through a WAF-protected global load balancer before reaching the internal Kubernetes ingress controllers. Egress from private subnets will traverse highly available NAT Gateways.
- **DNS & Routing**: Global DNS will be managed via Route53 or Cloudflare, employing latency-based routing and aggressive CDN caching for static `web` assets. Microservice communication will be strictly internal, potentially utilizing a service mesh (e.g., Istio) for mTLS authentication and advanced traffic shaping.

## Reliability Strategy

The architecture is designed to assume component failures and recover gracefully without user impact.

- **Failover Systems & Redundancy**: All stateless services will be replicated across AZs. The database layer will utilize Multi-AZ deployments with automatic failover capabilities.
- **Disaster Recovery**: We will define strict RPO and RTO targets. Automated snapshots for RDS and versioning/replication for S3 will ensure data integrity. Disaster recovery workflows will be regularly tested to ensure infrastructure can be restored into a secondary region within the defined RTO.
- **Self-Healing**: Kubernetes horizontal and vertical pod autoscalers will adapt dynamically to load changes, while liveness and readiness probes will automatically restart unresponsive containers and isolate failing instances from the load balancer rotation.

## Security Architecture

A Zero Trust model will be enforced across the platform.

- **IAM**: Principle of least privilege will dictate all IAM roles and Kubernetes Service Accounts using IAM Roles for Service Accounts (IRSA), ensuring microservices only access strictly required cloud resources (e.g., restricting `worker-cv` to its specific S3 buckets).
- **Encryption**: All data will be encrypted at rest utilizing managed KMS keys (for RDS, S3, and EBS volumes). All data in transit will be secured via TLS 1.3 internally (mTLS via service mesh) and externally.
- **Secrets Management**: Hardcoded secrets will be eliminated. We will integrate a centralized secrets management solution (e.g., AWS Secrets Manager or HashiCorp Vault) synced directly to Kubernetes workloads.
- **Network Security**: Security Groups and Kubernetes Network Policies will isolate microservices, ensuring that only the `api` can access the database, while `workers` only interact with Redis and object storage.

## Observability

We will transition from basic log tailing to a comprehensive observability platform.

- **Monitoring & Alerting**: Prometheus and Grafana will collect and visualize infrastructure metrics (CPU, memory, GPU utilization for workers) and custom application metrics (e.g., talk ratio calculation latency). Actionable alerts will trigger PagerDuty for anomalies, minimizing alert fatigue.
- **Logging**: All container standard output/error will be streamed to a centralized logging system (e.g., ELK stack or Datadog) for correlation and root cause analysis.
- **Tracing**: OpenTelemetry will be integrated into the FastAPI backend and Next.js frontend to provide distributed tracing across the `api` and decoupled worker queues, crucial for debugging the multi-stage asynchronous processing pipelines.

## Performance & Cost Optimization

Balancing performance with cost efficiency is paramount as the system scales.

- **Autoscaling & Resource Optimization**: Kubernetes Cluster Autoscaler will dynamically adjust underlying compute nodes. Spot instances will be aggressively leveraged for fault-tolerant, asynchronous worker queues (`worker-asr`, `worker-cv`) to dramatically reduce compute costs.
- **Infrastructure Efficiency**: We will right-size database instances and implement lifecycle policies on object storage to transition older audio/video chunks to cold storage tiers (e.g., S3 Glacier) automatically.
- **Caching**: The CDN will cache frontend static assets aggressively. Redis will be heavily utilized to cache frequent API queries and session states, reducing the database load and improving endpoint response times.

## Risks & Tradeoffs

- **Operational Complexity vs. Scalability**: Adopting Kubernetes and service meshes introduces a steep operational learning curve and maintenance overhead compared to simple Docker Compose setups, though it is necessary for global scaling.
- **Cost Implications**: Multi-AZ deployments, managed databases, and global load balancing incur higher baseline costs. These must be offset by leveraging Spot instances and strict auto-scaling policies.
- **Vendor Tradeoffs**: Utilizing deeply integrated managed services (e.g., AWS SQS or RDS) accelerates development and reliability but introduces vendor lock-in, which may complicate potential multi-cloud expansions required by strict data sovereignty laws.

## Agile Sprint Plan

- **Sprint 1: Foundational IaC & Networking**: Define the base Terraform modules. Provision the core VPC, subnets, NAT Gateways, and strict IAM roles. Setup centralized state management.
- **Sprint 2: Managed Stateful Services & Core Cluster**: Deploy Multi-AZ managed PostgreSQL and Redis. Provision the base Kubernetes cluster (EKS) and configure internal networking and security groups.
- **Sprint 3: CI/CD & Workload Migration**: Establish GitHub Actions CI pipelines. Containerize and deploy the `api` and `web` services to the cluster. Implement basic ingress and load balancing.
- **Sprint 4: Decoupled Workers & Observability**: Deploy the asynchronous workers (`worker-asr`, `worker-cv`, `worker-metrics`). Configure node pools (including Spot instances). Integrate the centralized logging and metrics stack (Prometheus/Grafana/ELK).
