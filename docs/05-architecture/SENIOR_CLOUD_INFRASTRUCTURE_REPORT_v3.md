# Senior Cloud Infrastructure Architecture Report v3

## Cloud Problem Analysis

PedagogyX is entering a phase requiring significant cloud infrastructure enhancements to support robust real-time data pipelines and highly available application frontends. The core challenges involve maintaining high uptime while managing fluctuating loads, especially during peak school hours or when handling large volumes of computer vision (CV) and automatic speech recognition (ASR) data from the Ray-Ban Wearables integration. The infrastructure must handle regional failures gracefully, ensure minimal latency for end-users, and adhere strictly to data sovereignty requirements, particularly considering the impending G2 (India legal sign-off) which will introduce real pilot PII. Furthermore, the operational overhead must be minimized through extensive automation to allow the development team to focus on feature delivery rather than infrastructure firefighting.

## Cloud Architecture

The proposed architecture utilizes a multi-cloud strategy for resilience, primary workloads on AWS, with strategic disaster recovery components mirrored in a secondary cloud provider (GCP). The core application runs on a scalable Kubernetes cluster (EKS) managed via a GitOps workflow (ArgoCD). Microservices (`web`, `api`, `worker-cv`, `worker-metrics`, `worker-asr`) are deployed as independent deployments within the cluster, allowing isolated scaling based on individual service metrics. The workers consume tasks from highly available Redis clusters. Stateful data is managed through a managed PostgreSQL database (Aurora) configured for multi-AZ high availability with cross-region replicas. Object storage (S3) is used for storing raw audio, video, and extracted metadata, fronted by a global CDN (CloudFront) to reduce latency and egress costs.

## Infrastructure Automation

All infrastructure components are provisioned using declarative Terraform configurations, organized into modular, reusable components for networking, compute, storage, and databases. We enforce a strict Infrastructure as Code (IaC) pipeline using GitHub Actions, requiring automated plans, security scans (tfsec), and peer reviews before any apply operation. Environments (dev, staging, prod) are isolated at the account level. Configuration management and application deployment within Kubernetes are fully automated using ArgoCD, ensuring the cluster state always matches the Git repository, thus eliminating configuration drift and manual interventions in production.

## Networking Architecture

The network is structured around a central transit gateway hub connecting multiple VPCs for isolation (e.g., separating database VPCs from application VPCs). Ingress traffic is routed through AWS Global Accelerator to an Application Load Balancer (ALB) acting as the main entry point to the EKS cluster. Internal communication between microservices within EKS is managed by a service mesh (Istio), enforcing mTLS for all service-to-service traffic and providing granular traffic routing and observability. Egress traffic is strictly controlled through NAT gateways and predefined egress firewall rules to prevent data exfiltration. Dedicated VPN connections (Site-to-Site) or zero-trust network access (ZTNA) solutions provide secure administrative access to private subnets without exposing bastion hosts to the public internet.

## Reliability Strategy

Reliability is prioritized at every layer. Compute resources use Auto Scaling Groups spread across three Availability Zones to survive AZ failures. The database tier employs synchronous multi-AZ replication for instant failover without data loss. We implement comprehensive circuit breaking and retry logic within the service mesh to handle transient network issues or dependent service degradation gracefully. Disaster Recovery (DR) includes automated, continuous backups of all stateful data to cross-region storage buckets with strict lifecycle policies. Regular, automated "game days" are scheduled to simulate regional failovers and validate our Recovery Time Objective (RTO) and Recovery Point Objective (RPO) metrics.

## Security Architecture

A Zero Trust model is strictly enforced. IAM roles are granted using the principle of least privilege, with temporary, session-based credentials used whenever possible. All data is encrypted at rest using KMS-managed keys, and in transit using TLS 1.3 (external) and mTLS (internal). Secrets management is handled by HashiCorp Vault or AWS Secrets Manager, with dynamic secret generation for database credentials to eliminate long-lived passwords. Container images are scanned for vulnerabilities in the CI pipeline and at runtime. A Web Application Firewall (WAF) protects the API ingress against common OWASP top 10 attacks and rate-limits abusive traffic patterns automatically.

## Observability

Comprehensive observability is built-in, not bolted on. Metrics from the infrastructure, Kubernetes nodes, and application containers are scraped continuously using Prometheus. Distributed tracing (OpenTelemetry) is instrumented across all microservices, allowing us to visualize the critical path of every request from the client, through the API, and down into the asynchronous workers. Centralized structured logging is aggregated into an ELK stack or Datadog, providing powerful search capabilities during incident response. Actionable alerts are configured based on Service Level Objectives (SLOs), focusing on user-impacting symptoms (e.g., high error rates, latency spikes) rather than raw resource utilization, effectively minimizing alert fatigue for on-call engineers.

## Performance & Cost Optimization

Cost optimization is a continuous effort. We leverage Spot instances aggressively for stateless workloads (e.g., `worker-cv`, `worker-asr`), reducing compute costs significantly while handling interruptions through robust queueing and fast pod startup times. Horizontal Pod Autoscalers (HPA) scale workloads based on custom metrics (e.g., queue depth) rather than just CPU/Memory, ensuring resources align perfectly with demand. We implement aggressive caching strategies at the CDN edge and within the application layer (Redis) to offload database queries and improve response times. Regular cost allocation reviews utilize AWS Cost Explorer and Kubernetes cost monitoring tools (Kubecost) to identify idle resources and optimize instance sizing.

## Risks & Tradeoffs

Adopting a multi-cloud or cross-region DR strategy significantly increases operational complexity and data transfer costs. Utilizing managed services like Aurora or EKS reduces administrative overhead but introduces vendor lock-in; we mitigate this by relying on open standards (Kubernetes, PostgreSQL, Redis) where possible. The strict security and compliance controls (required for handling student data) can introduce friction into the developer experience; we aim to counteract this by building robust internal developer platforms and automating security checks directly into the CI/CD pipelines, making the secure path the easiest path.

## Agile Sprint Plan

- **Sprint 1: Infrastructure Foundations**
  - Develop foundational Terraform modules (VPC, IAM, EKS).
  - Set up CI/CD pipelines for IaC validation and deployment.
- **Sprint 2: Platform Deployment & Automation**
  - Deploy Kubernetes clusters across staging and production.
  - Install core platform tools (ArgoCD, Prometheus, Istio) via GitOps.
- **Sprint 3: Database & Worker Integration**
  - Provision managed Aurora databases and Redis clusters.
  - Integrate microservices into the new infrastructure and validate scaling metrics.
- **Sprint 4: Security Hardening & Observability**
  - Implement full mTLS, configure WAF, and finalize alerting rules based on initial load testing.
  - Conduct full disaster recovery tabletop exercise.
