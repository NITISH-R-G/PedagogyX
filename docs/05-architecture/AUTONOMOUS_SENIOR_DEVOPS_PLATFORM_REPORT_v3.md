# Autonomous Senior DevOps & Platform Infrastructure Report

## Infrastructure Overview

The PedagogyX infrastructure relies on a distributed microservices ecosystem designed for scale, reliability, and developer productivity. The current architecture runs locally with `docker compose` (`infra/compose.dev.yaml`), representing the deployment target configuration. It comprises:

- A FastAPI backend service (`api`)
- A React and Next.js frontend application (`web`)
- Asynchronous worker services handling heavy processing: `worker-cv`, `worker-metrics`, and `worker-asr`
- Foundational state storage utilizing PostgreSQL (relational data), Redis (caching and job queueing), and MinIO (S3-compatible object storage).

This infrastructure is fully containerized, setting a strong baseline for deployment into production-ready Kubernetes environments.

## CI/CD Architecture

The CI/CD pipeline, executed via GitHub Actions (`.github/workflows/`), enforces rigorous validation and deployment safety:

- **Pipeline Structure**: Multiple workflows ensure continuous integration. `test.yml` runs full backend Python testing via Pytest and frontend Node.js testing. `dev-verify.yml` automatically lints and formats documentation, and audits dependencies using `safety` and `pip-audit`. `codeql.yml` scans the repository for security vulnerabilities.
- **Automation Strategy**: Shell scripts like `dev-verify.sh` guarantee standardization of markdown validation (`markdownlint` and `prettier`).
- **Deployment Flow**: The current local flow relies on Docker Compose, establishing the immutable containers needed for deployment scaling into a staging/production cluster.
- **Rollback Mechanisms**: No explicit CD rollbacks are currently automated in the repository, presenting an opportunity for GitOps integrations using ArgoCD or Flux.

## Cloud Infrastructure

The repository is primed for multi-cloud readiness based on containerized components:

- **Cloud Services**: Designed to utilize managed relational databases (RDS/Cloud SQL for Postgres), managed caching (ElastiCache/MemoryStore for Redis), and scalable object storage (S3/GCS replacing MinIO in production).
- **Networking**: In production, services should be segregated within a VPC, keeping databases and worker pools in private subnets, while an API Gateway or Ingress controller manages external traffic to `api` and `web`.
- **Infrastructure Layout**: Microservices are decoupled for independent scaling and failure isolation. Workers process workloads off the `api` via Redis task queues.
- **Scaling Architecture**: Current container boundaries provide the foundation for horizontal scaling depending on computational load (e.g., scaling `worker-asr` node instances dynamically based on queue depth).

## Kubernetes Architecture

While the repository uses Docker Compose for local environments, the architecture directly maps to Kubernetes concepts:

- **Cluster Topology**: Translates to namespaces containing specific Deployments, ConfigMaps, and Services.
- **Deployment Strategy**: Containerization ensures parity. Production deployments will use declarative Helm charts or Kustomize manifests.
- **Autoscaling**: Requires configuration of Horizontal Pod Autoscaler (HPA), specifically scaling `worker-asr` and `worker-cv` based on custom Redis metrics.
- **Ingress Architecture**: An NGINX or external Load Balancer ingress would expose `api` port 8080 and `web` port 3000 externally, providing TLS termination.

## Observability Stack

Visibility relies heavily on standard service logging.

- **Metrics**: Current baseline metrics involve dependency checks and basic testing statuses in CI. Real-time metrics will require Prometheus/Grafana integrations.
- **Logging**: Container stdout/stderr forms the foundation, visible via `docker compose logs`. In production, this data should be routed via Fluent Bit to a centralized log aggregator.
- **Tracing**: Implementing OpenTelemetry across the API and worker boundaries is an identified necessity to track latency for compute-heavy CV/ASR tasks.
- **Alerting**: Alerting is primarily handled by CI failure notifications via GitHub Actions.

## Security Architecture

Security automation is integrated into the SDLC.

- **IAM**: Implicit via environmental variables passed in `compose.dev.yaml` (e.g. `MINIO_ROOT_USER`, `POSTGRES_USER`).
- **Secret Management**: Handled via environment variables. In production, tools like AWS Secrets Manager or HashiCorp Vault should inject these.
- **Network Security**: Services within the local `docker-compose` network are isolated by default. In a cluster setup, Kubernetes Network Policies should enforce zero-trust isolation.
- **Vulnerability Management**: Implemented automatically in CI via `safety` and `pip-audit` checks for Python dependencies. CodeQL workflows detect code-level security issues.

## Reliability Strategy

The system handles background workload distribution to prevent synchronous API blocking:

- **Redundancy**: The decoupled state enables redundancy across all stateless microservices (`api`, `web`, `workers`).
- **Failover**: State layers (Postgres, Redis, MinIO) rely on local volumes for development. In production, these must utilize managed service failovers.
- **Disaster Recovery**: Relies on stateless app recovery combined with database backups (e.g., point-in-time recovery for Postgres).
- **Self Healing Mechanisms**: Managed via Docker Compose's implicit restarts and `healthcheck` declarations in `compose.dev.yaml` ensuring containers wait for dependencies (e.g., `redis: service_healthy`).

## Cost Optimization

- **Infrastructure Savings**: Offloading long-running tasks to async workers (`worker-cv`, `worker-asr`) allows the system to utilize cheaper spot instances/preemptible VMs for the bulk of compute.
- **Resource Optimization**: The use of lightweight Alpine Linux container images (e.g., `postgres:16-alpine`, `redis:7-alpine`) minimizes resource footprint.
- **Scaling Efficiency**: Separating workloads by queues (`jobs:asr`, `jobs:talk_ratio`) ensures compute capacity is only provisioned precisely where required.

## Risks & Bottlenecks

- **Operational Risks**: Lack of formal IaC (Terraform/Pulumi) definitions in the repository for production deployment environments limits deployment reproducibility outside local setups.
- **Scaling Limitations**: The current lack of connection pooling (e.g., PgBouncer) may bottleneck the Postgres database under heavy concurrent API and worker load.
- **Security Risks**: Relying strictly on environment variable injection for secrets without a secret manager introduces potential exposure in production.
- **Deployment Risks**: Zero-downtime deployment pipelines for worker nodes need to gracefully drain inflight Redis jobs during rollouts.

## Agile Sprint Plan

- **Sprint 1: IaC Foundation**
  - Implement basic Terraform configurations for VPC, managed Postgres, and Redis infrastructure to formalize the production footprint.
- **Sprint 2: Kubernetes Migration**
  - Create Helm charts or Kustomize manifests mapping the `compose.dev.yaml` definitions into Kubernetes deployments and services.
- **Sprint 3: Advanced Observability**
  - Integrate Prometheus scraping and OpenTelemetry tracing across the FastAPI backend and worker services to track CV/ASR processing latency.
- **Sprint 4: Secret Management & Connection Pooling**
  - Introduce HashiCorp Vault or AWS Secrets Manager integrations for secure credential injection. Deploy PgBouncer to manage database connection scale.
