# Infrastructure & DevOps Architecture Report

**Version:** 1.0
**Author:** Senior DevOps Engineer
**Focus:** High-Reliability, Automated Cloud & Edge Deployment

## 1. Infrastructure Overview

The PedagogyX infrastructure spans two distinct zones:

- **The Edge (D-PROC Hybrid):** Untrusted, low-resource LAN environments in Indian schools.
- **The Cloud (Central OSS Pool):** Trusted, high-resource GPU instances hosted in an Indian datacenter (e.g., E2E Networks or similar local provider for DPDP compliance).

## 2. CI/CD Architecture

- **Code Repositories:** GitHub monorepo.
- **Continuous Integration (CI):** GitHub Actions runs on every PR:
  - Linting (Prettier, Markdownlint, Flake8, Black).
  - Unit and Integration tests.
  - Docker Image build and push to a private registry.
- **Continuous Deployment (CD):**
  - Phase 1: Ansible triggered via GitHub Actions SSHes into production VPS nodes and runs `docker compose up -d`.
  - Phase 2: GitOps via ArgoCD syncing manifests to Kubernetes.

## 3. Cloud Infrastructure

- **Compute:** Bare-metal instances equipped with RTX 5070 GPUs. Chosen over AWS/GCP to drastically reduce hourly compute costs for constant 24/7 inference workloads.
- **Storage:** NVMe SSDs for hot Postgres data and active MinIO buffers. HDD-backed MinIO nodes for cold video storage.
- **Networking:** Virtual Private Cloud (VPC) with strictly defined security groups. Only ports 80/443 (Gateway) and WebRTC UDP ports are exposed to the public internet.

## 4. Kubernetes Architecture (Phase 2 Target)

While Phase 1 uses Docker Compose for simplicity, the system is designed for Kubernetes:

- **Control Plane:** Managed K8s (if available in target Indian DC) or self-hosted K3s.
- **Node Pools:** Dedicated GPU node pool with strict taints/tolerations to ensure only ML workloads run on expensive hardware. General compute pool for API and web services.
- **Ingress:** Traefik Ingress Controller handling TLS termination and routing.

## 5. Observability Stack

- **Metrics:** Prometheus server scraping all containers.
- **Dashboards:** Grafana visualizing CPU/VRAM usage, API latency, and queue lengths.
- **Logs:** Promtail + Loki to centralize logs without the heavy JVM overhead of Elasticsearch.
- **Alerting:** Alertmanager configured to page the on-call engineer via Slack/PagerDuty for critical failures (e.g., "GPU Driver Failed", "Postgres Unreachable").

## 6. Security Architecture

- **Zero Trust Edge:** The edge buffer nodes are treated as compromised. They authenticate to the cloud via rotating, short-lived tokens.
- **Network Segmentation:** DB and MinIO are strictly firewalled from the public internet, accessible only by API and ML worker nodes.
- **Secrets Management:** Doppler or HashiCorp Vault injects secrets at runtime. No `.env` files with production secrets in the repo.

## 7. Reliability Strategy

- **Infrastructure as Code (IaC):** Entire cloud environment provisioned via Terraform. Entire node configuration managed via Ansible. Zero manual SSH changes allowed.
- **Disaster Recovery (DR):** Automated daily backups of Postgres to a separate physical datacenter.
- **Failover:** If a GPU node dies, Docker Swarm / Kubernetes automatically reschedules the worker containers to healthy nodes. Redis queues ensure no jobs are lost during the transition.

## 8. Cost Optimization

- **Spot/Preemptible Strategy:** If supported by the local cloud provider, use spot instances for the asynchronous batch workers.
- **Egress Minimization:** Host the edge relay and cloud ingestion nodes in the same region/ISP where possible to minimize bandwidth costs.

## 9. Risks & Bottlenecks

- **Risk:** GPU driver instability on bare-metal Linux.
  - **Mitigation:** Standardize on a specific, tested NVIDIA driver version and pin it via Ansible. Automate a reboot-and-recover script for node hangs.
- **Bottleneck:** High I/O wait times on MinIO when multiple workers read/write massive 1080p chunks simultaneously.
  - **Mitigation:** RAID 0 NVMe drives for the hot MinIO ingest tier.

## 10. Agile Sprint Plan (DevOps Track)

- **Sprint 03:** Finalize `docker-compose.yml` for local development. Implement GitHub Actions CI for linting and basic tests.
- **Sprint 04:** Provision the first cloud GPU instance using Terraform/Ansible. Setup Prometheus and Grafana.
- **Sprint 05:** Automate the CD pipeline to deploy the Go API and Web dashboard to a staging environment.
