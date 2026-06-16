# Senior Cloud Infrastructure Architecture Report v3

## Cloud Problem Analysis

PedagogyX is an open-source educational platform currently operating in a Phase 0 MVP stage with strict constraints. The primary client is Meta Ray-Ban wearables (via Android DAT SDK). The project mandates a 100% Free and Open Source Software (FOSS) stack, local execution capabilities for data residency compliance (specifically offline execution and no reliance on third-party non-FOSS cloud APIs), and targets consumer-grade hardware (specifically the RTX 5070 with 12GB VRAM for GPU-bound tasks). Currently, production data is blocked pending G2 legal sign-off in India; the system relies exclusively on synthetic test sessions, dev boilerplate, and benchmarks.

The cloud engineering problem revolves around designing a cloud infrastructure and deployment strategy that accommodates these severe constraints while remaining extensible, highly scalable, and fundamentally sound as the platform transitions from local MVP (via Docker Compose) to distributed production scale (even if "cloud" in this context heavily implies bare-metal Kubernetes, edge computing, or private/hybrid cloud deployments to ensure data residency).

Failure scenarios involve restricted resource exhaustion (e.g., GPU memory leaks on constrained edge/cloud nodes), database single points of failure in the current local setup, missing external networking layers once the system leaves local dev, and the critical need to preserve strict data isolation when handling synthetic or future real PII data.

## Cloud Architecture

The overarching architecture must bridge the current `docker-compose` monolith into a scalable, distributed cloud-native footprint, heavily focused on a self-hosted Kubernetes (K8s) topology to honor the FOSS mandate.

- **Infrastructure Topology**: A Kubernetes-centric hybrid deployment. Edge nodes (potentially individual school servers or localized region clusters) will run local ASR/CV models on RTX 5070 constraints. Central orchestration will handle aggregated analytics (metrics).
- **Cloud Services**: No proprietary SaaS. We replace the local MVP components with highly available FOSS equivalents: PostgreSQL cluster (e.g., using Patroni) for relational data, Redis Cluster for distributed queues, and highly available MinIO clusters for S3-compatible object storage.
- **Networking**: Service Mesh (e.g., Istio or Linkerd) within K8s to manage microservice traffic between `api`, `worker-asr`, `worker-cv`, and `worker-metrics`.
- **Deployment Layout**: A hub-and-spoke model. The "hub" manages global configuration and anonymized metrics, while "spokes" (edge cloud deployments) handle heavy, localized ML processing to satisfy data residency requirements.

## Infrastructure Automation

Automation is critical for ensuring that the dev/MVP stack closely mirrors the production and edge deployments.

- **IaC Strategy**: Terraform (with local or self-hosted state backends) for provisioning base VMs or bare-metal instances. For Kubernetes configuration, we will use declarative manifests.
- **Provisioning Workflows**: Fully automated Ansible playbooks for OS-level bootstrapping and K8s node joins, specifically addressing the provisioning of NVIDIA drivers and container runtimes (e.g., NVIDIA Container Toolkit) for the RTX 5070 requirement.
- **Deployment Automation**: GitOps via ArgoCD or Flux. The `infra/` folder currently holding local `compose.yaml` will expand to include Helm charts or Kustomize manifests. All changes to deployments must be triggered by pull requests and merged to `main`.
- **Environment Management**: Strict separation of Dev, Staging, and Production (synthetic). Given the G2 block on production data, "Production" currently acts as a staging ground for synthetic volume testing.

## Networking Architecture

Networking must prioritize secure ingress from the Meta Ray-Ban client while strictly managing internal inter-service communication.

- **VPC Layout**: If deployed in a public cloud provider (AWS/GCP), strict private VPCs for all worker nodes and databases. Only the API Gateway is exposed.
- **Ingress/Egress**: A robust FOSS Ingress Controller (e.g., NGINX Ingress or Traefik) routing traffic to the `api` and `web` services. Egress is strictly controlled to prevent unauthorized exfiltration of sensitive audio/video data.
- **Load Balancing**: Layer 7 load balancing for HTTP/WebSocket connections from the DAT client to the API. Internal gRPC or Redis queue balancing for `worker-asr` and `worker-metrics`.
- **DNS Strategy**: Internal CoreDNS for service discovery (`api.local`, `redis.local`). External DNS routed through Cloudflare (with strict proxy rules) or a self-hosted DNS server for complete control.

## Reliability Strategy

The system must gracefully handle the limitations of consumer-grade GPUs and potential connectivity issues from edge deployments.

- **Failover Systems**: The database layer (Postgres) must transition from the single local container to a Multi-AZ / Multi-Node Patroni cluster with automated failover. Redis needs Redis Sentinel or Cluster mode.
- **Redundancy**: Microservices (`api`, `web`, `worker-asr`, `worker-metrics`) must run with minimum replica counts > 1.
- **Disaster Recovery**: Automated nightly Postgres dumps (pg_dump/WAL archiving via pgBackRest) backed up to an offsite MinIO bucket.
- **Self Healing Mechanisms**: K8s Liveness and Readiness probes must be rigorously defined. If `worker-asr` crashes due to GPU OOM (Out Of Memory) on the 12GB RTX 5070, K8s must instantly restart the pod and the Redis job queue must re-queue the failed task.

## Security Architecture

Data residency and PII protection are the foundational constraints of PedagogyX.

- **IAM**: Since we are using FOSS, we rely on K8s RBAC for internal authorization. We must implement strict least-privilege service accounts (e.g., `worker-asr` only has access to the ASR queue and MinIO read-only).
- **Encryption**: TLS 1.3 everywhere. Internal service mesh mTLS for all pod-to-pod traffic. Postgres encryption at rest. MinIO bucket encryption.
- **Secrets Management**: HashiCorp Vault (FOSS version) or Sealed Secrets to replace the currently hardcoded dev passwords (`pedagogyx_dev`) in the `compose.dev.yaml`.
- **Network Security**: Network Policies in K8s to default-deny all traffic. `worker-asr` cannot talk directly to `web`, only to `redis` and `minio`.

## Observability

Comprehensive observability is essential for debugging asynchronous ML pipelines across distributed infrastructure.

- **Monitoring**: Prometheus for scraping metrics from Postgres, Redis, MinIO, and custom metrics from the FastAPI and worker services.
- **Logging**: FluentBit daemonsets collecting logs from all containers, shipping them to a FOSS backend (e.g., Loki or Elasticsearch).
- **Tracing**: OpenTelemetry (OTel) instrumentation in the FastAPI (`api`) and worker services to trace a request from the Meta Ray-Ban DAT client upload all the way through ASR processing and metric generation.
- **Alerting**: Alertmanager configured to page when GPU utilization flatlines, queue depths exceed thresholds, or `worker-asr` pods crash continuously.

## Performance & Cost Optimization

The primary constraint is squeezing maximum performance out of low-cost hardware (RTX 5070).

- **Autoscaling**: KEDA (Kubernetes Event-driven Autoscaling) scaling `worker-asr` pods based on Redis queue length, limited by a `MaxReplicas` threshold tied to physical GPU availability.
- **Resource Optimization**: Strict K8s resource requests and limits. Ensure the CPU is heavily utilized for `worker-metrics` while the GPU is exclusively locked by `worker-asr`/`worker-cv`.
- **Caching**: Extensive use of Redis for caching frequently requested metadata to relieve pressure on Postgres. CDN caching for the Next.js `web` static assets.
- **Infrastructure Efficiency**: Exploring batch processing for ASR tasks to maximize GPU memory throughput rather than processing streams individually, ensuring the 12GB VRAM is fully saturated but not exceeded.

## Risks & Tradeoffs

- **Operational Complexity**: Moving from Docker Compose to a full FOSS K8s stack drastically increases operational overhead for the dev team.
- **FOSS Constraints**: Forgoing managed services (AWS RDS, S3, SQS) means taking on the burden of managing Patroni, MinIO, and Redis clustering.
- **Hardware Limitations**: The hard RTX 5070 12GB constraint means models may need severe quantization, risking accuracy tradeoffs for infrastructure cost savings.
- **Data Restrictions**: Developing against purely synthetic data limits the ability to test real-world edge cases in ML pipeline performance until G2 block is lifted.

## Agile Sprint Plan

- **Sprint 1**: Refactor MVP infrastructure into declarative Terraform modules for base node provisioning. Set up a local/remote K3s or Minikube equivalent for dev parity.
- **Sprint 2**: Migrate single-node Postgres and Redis in `compose.dev.yaml` to highly available FOSS K8s operators (e.g., CloudNativePG, Redis Operator). Implement Sealed Secrets.
- **Sprint 3**: Instrument FastAPI and Python workers with OpenTelemetry. Deploy Prometheus, Loki, and Grafana stack for baseline observability.
- **Sprint 4**: Implement KEDA for autoscaling the worker queues based on synthetic load testing. Conduct chaos testing on GPU worker failure recovery.
