# Autonomous Senior Cloud Infrastructure Architecture Report v3

## Cloud Problem Analysis

PedagogyX requires an inherently resilient, highly available, and scalable cloud-edge infrastructure. However, the system must adhere to strict constraints: a 100% Free and Open Source Software (FOSS) mandate, offline execution capabilities for data residency compliance (especially crucial as production school data is blocked until G2 India legal sign-off), and the reality of deploying heavily onto consumer-grade RTX 5070 (12GB VRAM) hardware at edge locations. The primary v1 client is the Meta Ray-Ban via `clients/android-capture-dat` (DAT). Thus, the core cloud problem is managing a hybrid, multi-tiered infrastructure where "cloud" acts as a control plane, metadata registry, and synthetic training backbone, while the "edge" handles primary compute and offline operation, demanding seamless synchronization without vendor lock-in.

## Cloud Architecture

The architecture is fundamentally a Hybrid Cloud-to-Edge Control Plane Model.

- **Edge Layer (Primary Compute):** Forward-deployed RTX 5070 consumer nodes in localized environments. These handle real-time Meta Ray-Ban DAT ingestion and localized ASR/CV processing entirely offline using FOSS models.
- **Cloud Control Plane (Centralized Management):** Hosted on agnostic infrastructure (e.g., Kubernetes on bare metal or cloud providers strictly using FOSS layers like K3s/RKE2). The cloud layer manages node fleet state, telemetry aggregation, global routing, and synthetic training using non-PII data.
- **Data Residency Compliance:** Edge nodes are air-gapped during critical data processing, syncing anonymized telemetry or model weights to the cloud only under strict RBAC and G2 legal allowances.

## Infrastructure Automation

We enforce strict, declarative Infrastructure as Code (IaC) utilizing Terraform (or FOSS equivalents like OpenTofu) and Ansible.

- **Cloud Provisioning:** OpenTofu automates Kubernetes cluster bootstrapping and baseline networking.
- **Edge Provisioning:** Ansible playbooks orchestrate the configuration of RTX 5070 edge nodes, ensuring identical OS tuning, GPU driver installation (NVIDIA drivers), and Docker container deployments without manual intervention.
- **GitOps:** ArgoCD synchronizes configuration and application states from the central Git repository to both the cloud control plane and edge clusters, preventing configuration drift and ensuring reproducible environments.

## Networking Architecture

Networking is designed for secure, partitioned, and intermittent connectivity.

- **Cloud Networking:** Standard VPC layout with private subnets for control plane databases, ingress controllers managing API traffic from clients (when online), and strict network policies within Kubernetes.
- **Edge Networking:** Edge nodes operate on local networks, ingesting data directly from Meta Ray-Ban DAT clients via local Wi-Fi/Bluetooth proxies (`clients/android-capture-dat`).
- **Cloud-Edge Bridge:** When connectivity is available, edge nodes communicate with the cloud control plane via mutual TLS (mTLS) over secure VPN tunnels (e.g., WireGuard) to sync telemetry and pull configuration updates, gracefully handling network partitions.

## Reliability Strategy

Reliability focuses on offline survivability and eventual consistency.

- **Edge Autonomy:** Edge nodes are fully self-sufficient. If the cloud connection drops, local databases (e.g., SQLite or local Postgres) queue all telemetry and processing metadata.
- **Cloud Redundancy:** The cloud control plane utilizes multi-node Kubernetes clusters spanning multiple availability zones. State is backed by resilient, replicated databases (e.g., clustered PostgreSQL).
- **Disaster Recovery:** Automated volume snapshots of the cloud state are taken regularly. Edge nodes are treated as ephemeral cattle; if an RTX 5070 node fails, it can be entirely reprovisioned from bare metal using Ansible, pulling the latest state from the cloud upon boot.

## Security Architecture

A strict Zero Trust and FOSS-centric security posture is mandated.

- **Identity & Access (IAM):** Centralized OIDC/OAuth2 (via Keycloak) manages access to the cloud control plane. Edge nodes authenticate via short-lived, dynamically rotated X.509 certificates.
- **Data Protection:** All local storage on edge nodes uses full-disk encryption (LUKS). Traffic between the Meta Ray-Ban DAT client and the edge node is encrypted. No PII leaves the edge node until G2 compliance is met.
- **Vulnerability Management:** Continuous scanning of Docker images and IaC using FOSS tools (e.g., Trivy) integrated into the GitHub Actions CI pipeline.

## Observability

Observability must span both the centralized cloud and the distributed edge without relying on proprietary SaaS.

- **Metrics:** Prometheus instances on edge nodes scrape local GPU (DCGM) and system metrics, federating up to a central Thanos/Prometheus cluster in the cloud when connected.
- **Logging:** Promtail/Fluent Bit on edge nodes ships logs to a central FOSS Loki instance.
- **Tracing:** OpenTelemetry instruments the FastAPI backend and Rust/Python workers, forwarding traces to Jaeger/Tempo in the cloud for distributed latency analysis across the DAT client and worker pipelines.

## Performance & Cost Optimization

The architecture is inherently cost-optimized by leveraging consumer hardware.

- **Edge Efficiency:** Utilizing RTX 5070 (12GB VRAM) requires aggressive model quantization and memory management in the AI layer, maximizing the throughput per local node and eliminating per-inference cloud costs.
- **Cloud Efficiency:** The cloud control plane is lightweight, requiring minimal compute since heavy inference is pushed to the edge. We utilize cluster autoscaling during synthetic data generation runs and scale down to a minimal footprint during idle periods.

## Risks & Tradeoffs

- **Edge Hardware Reliability:** Consumer-grade RTX 5070 GPUs lack ECC memory and enterprise support, increasing the risk of hardware failures compared to datacenter GPUs. _Mitigation: Treat edge nodes as stateless cattle; implement robust local retries and automated reprovisioning._
- **Offline Sync Complexity:** Managing distributed state and eventual consistency across intermittently connected edge nodes is notoriously difficult. _Mitigation: Strict unidirectional sync patterns and append-only local queues._
- **FOSS Burden:** Mandating 100% FOSS requires self-hosting infrastructure (e.g., Keycloak, observability stack), increasing operational overhead compared to using managed SaaS platforms.

## Agile Sprint Plan

- **Sprint 1 (Foundation):** Finalize OpenTofu modules for the core cloud Kubernetes cluster. Deploy foundational observability (Prometheus/Loki) and GitOps (ArgoCD) tools.
- **Sprint 2 (Edge Provisioning):** Develop Ansible playbooks for automated setup of consumer RTX 5070 nodes. Implement local network bridging for the Meta Ray-Ban DAT client.
- **Sprint 3 (Secure Connectivity):** Establish WireGuard mTLS tunnels between edge nodes and the cloud control plane. Implement offline telemetry queuing and eventual sync.
- **Sprint 4 (Validation):** Conduct end-to-end load testing with synthetic DAT sessions. Execute "plug pull" drills to verify offline autonomy and recovery capabilities.
