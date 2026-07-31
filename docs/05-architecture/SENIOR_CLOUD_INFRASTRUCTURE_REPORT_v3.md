# Senior Cloud Infrastructure Report v3

## Cloud Problem Analysis

PedagogyX is rapidly evolving into a platform that must serve high-velocity, real-time audio and computer vision metrics across a distributed user base of educators. As the application transitions from an MVP to a pilot ready system, the infrastructure must scale dynamically to handle unpredictable spikes in usage during school hours. The current problem revolves around guaranteeing extremely low latency for capturing real-time streams (ASR/CV data), maintaining absolute data privacy (FERPA compliance for potential future sign-offs), and optimizing cloud spending for GPU/CPU workloads. Failure scenarios include regional cloud outages and worker saturation, requiring highly fault-tolerant architecture capable of seamless degradation.

## Cloud Architecture

The system will deploy across an AWS multi-region active-active topology to guarantee high availability and fault tolerance. At the edge, Cloudflare will be used for DNS, DDoS protection, and CDN delivery to minimize latency for static assets and API requests.

- **Compute:** EKS (Elastic Kubernetes Service) will orchestrate the microservices (api, web, worker-cv, worker-metrics, worker-asr). The control plane will be regional, with node groups distributed across multiple Availability Zones.
- **State and Data:** Amazon Aurora Serverless (PostgreSQL) will handle primary transactional data. Amazon ElastiCache (Redis) will be used for session management and distributed rate limiting. Data lake/object storage will be built on Amazon S3 with cross-region replication (replacing MinIO in production).
- **Asynchronous Workers:** Managed Kafka (MSK) or SQS/SNS will buffer high-throughput ingestion from ASR/CV clients, protecting the backend APIs from traffic spikes.

## Infrastructure Automation

The entire infrastructure stack will be managed strictly via Terraform (Infrastructure as Code) following GitOps principles using ArgoCD.

- **Provisioning:** Environments (dev, staging, prod) will be defined declaratively in Terraform with heavy reliance on modular design for VPCs, EKS clusters, and IAM roles.
- **GitOps:** ArgoCD will sync Kubernetes manifests from a dedicated infrastructure repository. Commits to the `main` branch will automatically trigger state reconciliation, preventing infrastructure drift.
- **Validation:** Tools like Checkov and Terraform Validate will run in CI pipelines to enforce security and compliance standards before infrastructure changes are applied.

## Networking Architecture

The networking topology strictly enforces network segmentation and zero-trust principles.

- **VPC Design:** A hub-and-spoke model using AWS Transit Gateway. The primary VPC will span 3 Availability Zones, partitioned into Public (ALB, NAT Gateways), Private (EKS Nodes, Workers), and Data (Aurora, Redis) subnets.
- **Ingress/Egress:** Traffic will ingress through Cloudflare to AWS WAF, terminating at an Application Load Balancer (ALB). Egress traffic will be routed through NAT Gateways, strictly filtered by security groups and VPC endpoints (e.g., S3 Gateway Endpoints) to ensure data never traverses the public internet unnecessarily.
- **Service Mesh:** Istio or Linkerd will be deployed within EKS for mTLS communication between microservices, offering deep network observability and fine-grained traffic policies.

## Reliability Strategy

Reliability is prioritized to ensure zero downtime for critical classroom metrics capturing.

- **Redundancy:** Multi-AZ deployment for all critical services. Stateless services will scale horizontally via Horizontal Pod Autoscaler (HPA) and Karpenter for rapid node provisioning.
- **Disaster Recovery:** RPO is set to 5 minutes, and RTO to 1 hour. Continuous automated backups for Aurora and S3 cross-region replication will support rapid failover to a secondary AWS region in case of complete region loss.
- **Self-Healing:** Kubernetes liveness/readiness probes, circuit breakers via Service Mesh (Istio), and dead-letter queues (DLQ) for asynchronous workers to ensure no data is lost during worker failures.

## Security Architecture

Security is built into every layer to prepare for strict educational compliance (FERPA/SOC2).

- **IAM:** AWS IAM Roles for Service Accounts (IRSA) will provide least-privilege access to EKS pods. Root access is disabled.
- **Encryption:** All data is encrypted at rest using AWS KMS (Customer Managed Keys). All data in transit is encrypted using TLS 1.3 and mTLS within the cluster.
- **Secrets Management:** External Secrets Operator integrated with AWS Secrets Manager will inject secrets directly into pods, completely avoiding hardcoded secrets or environment variables in manifest files.
- **Network Security:** Security Groups will restrict access tightly; only the API gateway can access worker APIs, and only authorized subnets can reach the database.

## Observability

Comprehensive observability ensures rapid MTTR (Mean Time to Resolution).

- **Telemetry:** OpenTelemetry will instrument all microservices (Python/FastAPI and Node/Next.js) for distributed tracing, metrics, and logs.
- **Backend:** Datadog or an LGTM stack (Loki, Grafana, Tempo, Mimir) hosted internally will aggregate all telemetry data.
- **Alerting:** PagerDuty integration with anomaly detection rules on error rates, latency spikes (p99 > 200ms), and worker queue saturation. Alerts are designed to minimize fatigue by requiring actionable conditions.

## Performance & Cost Optimization

Balancing high-performance compute requirements for CV/ASR with cost efficiency.

- **Compute Optimization:** Karpenter will dynamically provision Spot Instances for non-critical workers (e.g., asynchronous offline processing) while retaining On-Demand instances for real-time `api` and `worker-asr` services.
- **Scaling Policies:** KEDA (Kubernetes Event-driven Autoscaling) will scale workers based on SQS/Kafka queue depth rather than raw CPU, ensuring rapid scale-up before CPU saturation occurs.
- **Caching:** Aggressive caching via Cloudflare CDN for static assets and ElastiCache for frequent API queries (e.g., school dashboards), minimizing database load and compute cost.

## Risks & Tradeoffs

- **Complexity vs Agility:** A multi-region, service-mesh Kubernetes architecture is complex to maintain and requires significant platform engineering effort, potentially slowing feature velocity initially.
- **Cost vs Reliability:** Active-active multi-region deployment significantly increases baseline AWS spend. Tradeoff: We will begin with active-passive failover and scale to active-active only when SLA demands it.
- **GPU Scaling Risk:** `worker-cv` and high-tier ASR models may face GPU availability limits or cost overruns. Tradeoff: Implement strict tenant-based rate limiting and fallback to CPU-based lightweight models (e.g., Whisper Tiny) during peak load.

## Agile Sprint Plan

### Sprint 1: Foundational Infrastructure & IaC

- Establish baseline AWS VPC, IAM, and KMS structures using Terraform.
- Deploy basic EKS cluster and configure ArgoCD for GitOps.

### Sprint 2: Stateful Services & Networking

- Provision Aurora Serverless, ElastiCache, and MSK via Terraform.
- Configure Ingress, AWS WAF, and establish zero-trust network boundaries.

### Sprint 3: Observability & Security Hardening

- Deploy OpenTelemetry collectors and integrate Datadog/LGTM stack.
- Implement IRSA and Secrets Manager integrations.

### Sprint 4: Performance, DR, & CI/CD

- Implement Karpenter and KEDA autoscaling rules.
- Execute disaster recovery drills and finalize the multi-AZ automated failover procedures.
