# PedagogyX Cloud Infrastructure Strategy

## Cloud Problem Analysis

- **Business Requirements:** PedagogyX requires an OSS-first, highly scalable, and cost-efficient multimodal AI classroom intelligence platform. The primary capture method involves Meta Ray-Ban (DAT) Android clients and Windows smartboards pushing data to edge nodes for buffering, followed by asynchronous WAN uploads to a central India-based cloud for ASR, CV, and ML processing. Strict India data residency requirements are mandated (G2 compliance).
- **Scale Assumptions:** Tens of thousands of classrooms concurrent during school hours, generating continuous audio, screen, and multi-cam video streams. Edge nodes buffer and chunk data to handle erratic school WAN uplinks. Millions of requests and massive object storage demands for batch ML processing.
- **Operational Constraints:** Must use open-source software (OSS-first stack) to avoid proprietary API costs. Cost-effective GPU utilization is critical (RTX 5070 budget context). The platform must balance real-time hot path analytics with deep authoritative batch processing without bottlenecking.
- **Failure Scenarios:** Edge hardware failure, school LAN/WAN outages, cloud ingest bottlenecks, GPU worker starvation, Postgres database connection exhaustion, MinIO storage degradation.

## Cloud Architecture

- **Infrastructure Topology:** Hybrid Edge-Cloud Architecture. Edge nodes (hybrid D-PROC) sit on school LANs to ingest and buffer streams. A centralized India-based OSS-first cloud processes asynchronous uploads.
- **Cloud Services:** Bare-metal or IaaS cloud instances in India (e.g., AWS AP-South, GCP Mumbai, or local data centers) running Kubernetes. Compute split into stateless API gateways and stateful/GPU worker node pools.
- **Networking:** Asynchronous REST/WebRTC for edge-to-cloud sync. MediaMTX used for stream ingest. VPCs segmenting public ingress from internal batch ML and database layers.
- **Deployment Layout:** Multi-AZ Kubernetes clusters in the India region. Stateful workloads (Postgres + MinIO) run on dedicated optimized storage instances. GPU workers managed via separate scalable node pools.

## Infrastructure Automation

- **IaC Strategy:** Terraform for all cloud resources (VPCs, node pools, storage buckets, IAM). Pulumi or Crossplane considered for Kubernetes-native infrastructure provisioning.
- **Provisioning Workflows:** GitOps via ArgoCD or Flux to enforce declarative cluster states. Changes to infrastructure and application manifests are merged to `main` and automatically reconciled.
- **Deployment Automation:** Helm charts for packaged deployments of internal services. Automated canary rollouts for the API and worker components to validate changes safely.
- **Environment Management:** Ephemeral dev environments and strict separation of staging and production VPCs/clusters. Immutable infrastructure patterns enforced across all worker nodes.

## Networking Architecture

- **VPC Layout:** Hub-and-spoke VPC topology. Public subnets for API gateways and Ingress controllers; private subnets for GPU workers, job queues (Redis), and data stores (Postgres/MinIO).
- **Ingress/Egress:** Edge node traffic ingests via highly available L4/L7 load balancers to API/MediaMTX endpoints. Egress via NAT gateways restricted to necessary updates and webhook integrations.
- **Load Balancing:** Layer 7 load balancing for API traffic; gRPC/WebRTC load balancing for MediaMTX ingest streams. Service mesh (e.g., Istio or Linkerd) for internal microservice routing and circuit breaking.
- **DNS Strategy:** Geo-routed DNS pointing to the optimal India-based ingest points. Internal Kubernetes DNS (CoreDNS) for service discovery.

## Reliability Strategy

- **Failover Systems:** Stateless API tier and ingest tier scale horizontally. Edge nodes cache data locally during WAN partitions and resume uploads.
- **Redundancy:** Multi-AZ deployments for API, Redis, Postgres, and MinIO. At least N+1 redundancy in GPU worker pools to absorb instance failures.
- **Disaster Recovery:** Automated volume snapshots for Postgres. Cross-region or cross-bucket replication for critical MinIO data. Infrastructure defined entirely in IaC for complete RTO minimization.
- **Self Healing Mechanisms:** Kubernetes liveness and readiness probes automatically restart failed containers. Job queues automatically retry failed ASR/ML processing tasks.

## Security Architecture

- **IAM:** Least privilege RBAC for all internal microservices. IAM roles linked to Kubernetes ServiceAccounts (e.g., IRSA). Strict segmentation between tenant data.
- **Encryption:** TLS 1.3 for all edge-to-cloud and internal service-to-service transit. AES-256 for Postgres databases and MinIO object stores at rest.
- **Secrets Management:** External Secrets Operator integrating with HashiCorp Vault or Cloud KMS to inject secrets into pods at runtime. No hardcoded secrets.
- **Network Security:** Zero trust network policies within Kubernetes blocking lateral movement. WAF filtering at the edge to mitigate malicious payloads and DDoS attacks.

## Observability

- **Monitoring:** Prometheus and VictoriaMetrics for scalable metric scraping (infrastructure health, GPU utilization, worker queue depths).
- **Logging:** Promtail/Fluent Bit shipping logs to Grafana Loki or Elasticsearch for centralized analysis of worker errors and API anomalies.
- **Tracing:** OpenTelemetry instrumented across API, MediaMTX, and Python workers, tracking request latency from edge ingest to final DB score.
- **Alerting:** Alertmanager routing actionable alerts to PagerDuty/Slack based on SLA thresholds (e.g., edge buffer upload failures, high GPU queue latency).

## Performance & Cost Optimization

- **Autoscaling:** KEDA (Kubernetes Event-driven Autoscaling) triggering GPU worker scaling based on Redis queue depths. Horizontal Pod Autoscaler for API traffic. Cluster Autoscaler for node provisioning.
- **Resource Optimization:** Strict CPU/Memory requests and limits on all containers. Dedicated node affinities for GPU workloads to maximize utilization.
- **Caching:** Redis for caching frequent API responses, tenant configurations, and hot-path analytics states.
- **Infrastructure Efficiency:** Spot instances for batch processing GPU workers (since jobs are queued and retriable). Reserved instances for baseline API and database nodes.

## Risks & Tradeoffs

- **Operational Risks:** Hybrid Edge-Cloud introduces complexity with edge node fleet management and debugging WAN failures in remote Indian schools.
- **Scaling Concerns:** Spiky traffic patterns aligned with school schedules could lead to massive queue backups or high cost if auto-scaling is too slow or over-provisioned.
- **Vendor Tradeoffs:** OSS-first self-hosting trades higher operational/SRE overhead for reduced per-request API costs (e.g., self-hosting ASR vs. Whisper API).
- **Cost Implications:** Maintaining large GPU node pools is expensive; aggressive spot-instance usage and scale-to-zero capabilities for batch workers are required to stay within budget.

## Agile Sprint Plan

- **Milestones:**
  - Milestone 1: Baseline IaC (Terraform) and Kubernetes cluster setup in the India region.
  - Milestone 2: CI/CD GitOps pipelines and Observability stack (Prometheus, Loki, OpenTelemetry) deployment.
  - Milestone 3: Ingest API, Redis, Postgres, and MinIO stateful services deployment.
  - Milestone 4: GPU worker autoscaling configuration (KEDA) and Edge-to-Cloud sync validation.
- **Implementation Phases:** Phase 1 focuses on core infrastructure and stateless API. Phase 2 tackles stateful storage and streaming ingest. Phase 3 focuses on GPU worker elasticity and scaling.
- **Priorities:** High priority on declarative infrastructure, automated deployments, and reliable stateful storage before onboarding heavy GPU workloads.
- **Expected Infrastructure Improvements:** Transition from the MVP docker-compose setup to a scalable, multi-AZ Kubernetes environment capable of handling simulated multi-classroom load with automated failover and autoscaling.
