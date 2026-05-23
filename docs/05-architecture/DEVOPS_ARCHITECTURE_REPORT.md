# DevOps Architecture Report

**Status:** Draft v1.0
**Date:** 2026-05-20
**Role:** Senior DevOps Engineer

## 1. Infrastructure Overview

The PedagogyX infrastructure spans three distinct zones: the unmanaged School Edge, the AWS Control Plane (`ap-south-1`), and the Bare-Metal GPU Inference Pool. Our goal is to achieve near-zero touch deployment and self-healing capabilities across this highly fragmented footprint.

## 2. CI/CD Architecture

- **Version Control:** GitHub.
- **CI:** GitHub Actions runs automated tests, linting, and security scans (Dependabot/Snyk) on every pull request.
- **Artifacts:** Docker images are built, tagged (SemVer), and pushed to a private container registry (e.g., AWS ECR) upon merge to `main`.
- **CD (Control Plane):** ArgoCD (if K8s) or custom GitHub Actions (if ECS/Swarm) deploy changes to the staging environment automatically, requiring manual approval for production rollout.
- **CD (Edge):** An Over-The-Air (OTA) update mechanism triggers edge nodes to pull new container images during off-peak hours (e.g., 2 AM IST).

## 3. Cloud Infrastructure

(Summarized from Cloud Report) AWS handles all stateful data (RDS Postgres), API routing (ALB), and object storage (S3/MinIO), provisioned strictly via Terraform.

## 4. Kubernetes Architecture

- _Decision:_ Kubernetes (EKS) will **not** be used for Phase 0 / MVP to reduce operational complexity and control plane costs.
- _Alternative:_ We utilize AWS ECS for the Control Plane and Docker Swarm for the bare-metal GPU pool. This drastically lowers the learning curve and maintenance burden while meeting MVP scaling needs.

## 5. Observability Stack

- **Metrics:** Prometheus instances run in the AWS VPC and on the GPU Swarm manager.
- **Logs:** Promtail ships logs from all containers to a centralized Grafana Loki instance.
- **Dashboards:** Grafana visualizes the health of the entire hybrid system.
- **Tracing:** OpenTelemetry provides distributed tracing, critical for debugging latency between the edge, control plane, and GPU workers.

## 6. Security Architecture

- **Container Security:** Trivy scans all Docker images in the CI pipeline to block deployments containing critical CVEs.
- **Network Security:** Security Groups in AWS and `ufw` on bare-metal nodes enforce strict allowlists.
- **Zero Trust:** Edge nodes authenticate via short-lived JWTs; GPU nodes authenticate via WireGuard/Tailscale identity.

## 7. Reliability Strategy

- **Immutable Infrastructure:** We never patch a running container. We rebuild and redeploy.
- **Health Checks:** Rigorous HTTP and TCP health checks determine if a node should be killed and recreated.
- **Graceful Degradation:** If the GPU pool is fully saturated or down, the API must continue to accept uploads (queuing them) and serve cached dashboards.

## 8. Cost Optimization

- **Ephemeral Environments:** CI pipelines tear down staging databases and compute immediately after tests complete.
- **Log Retention:** Loki is configured with aggressive log rotation; debug logs are dropped after 7 days, warning/error logs kept for 30.

## 9. Risks & Bottlenecks

- **Risk:** Edge Node drift. Without K8s at the edge, ensuring 50 distinct school nodes are running the exact same configuration is difficult. **Mitigation:** Strict Ansible playbooks and an immutable OS approach (e.g., Flatcar or similar) for the edge nodes, if we control the hardware.
- **Bottleneck:** The single Tailscale/VPN gateway connecting the bare-metal pool to AWS could become a network bottleneck for heavy video artifacts.

## 10. Agile Sprint Plan

- **Sprint 1:** Standardize Dockerfiles across the monorepo. Implement GitHub Actions CI pipeline (lint, test, build, push).
- **Sprint 2:** Setup the central observability stack (Prometheus, Loki, Grafana) and ensure dummy logs are flowing.
- **Sprint 3:** Implement the CD pipeline for the Control Plane. Implement the OTA update mechanism for the mock capture agents.
