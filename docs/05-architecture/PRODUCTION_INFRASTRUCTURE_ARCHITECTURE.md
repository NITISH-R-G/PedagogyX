# Production Infrastructure Architecture

## Infrastructure Overview

PedagogyX operates a **Hybrid Edge-Cloud Architecture (D-PROC=C)** designed to serve the India market with strict DPDP (Digital Personal Data Protection) compliance. The infrastructure must support low-end client devices—specifically Android companion apps (DAT) paired with Meta Ray-Ban smart glasses—which handle only capture and encoding.

The core processing relies on a central OSS-first, self-hosted inference stack, entirely devoid of proprietary cloud APIs. The compute topology is optimized around 12GB VRAM consumer-grade GPUs (e.g., RTX 5070) for executing faster-whisper (ASR), YOLO with TensorRT (Computer Vision), and Ollama (LLMs). This architecture guarantees ₹0 customer hardware budgets by shifting heavy multimodal compute to centralized, self-hosted Kubernetes clusters.

Operational goals include maximizing automation, ensuring zero-trust security per strict privacy regulations, preventing infrastructure drift, and maintaining production-grade reliability across environments with potentially flaky client connectivity.

## CI/CD Architecture

The continuous integration and continuous deployment pipeline is engineered for zero-downtime rollouts, automated rollback capabilities, and strict environment reproducibility.

- **Pipeline Structure:** GitHub Actions serves as the primary CI engine, enforcing formatting (prettier, markdownlint), code quality (ruff for Python, eslint for Next.js), and automated benchmark validation (CPU/GPU pipeline testing).
- **Automation Strategy:** All infrastructure is managed declaratively via Terraform and Helm charts. Infrastructure-as-Code (IaC) pipelines mandate automated plan generation and security scanning (tfsec, checkov) before any merge.
- **Deployment Flow:** We utilize a GitOps model with ArgoCD. Commits to the main branch trigger container builds which are pushed to a private, scanned registry. ArgoCD continuously reconciles the cluster state against the deployment repository.
- **Rollback Mechanisms:** Deployments utilize progressive delivery (canary and blue-green deployments) via Argo Rollouts. Automated synthetic tests run post-deployment; if error rates or API latency exceed threshold SLAs, Argo Rollouts automatically triggers a seamless rollback without human intervention.

## Cloud Infrastructure

Because PedagogyX strictly prohibits proprietary cloud APIs (e.g., OpenAI, AWS Rekognition) for its core AI workloads, the cloud infrastructure is tailored to host scalable OSS components effectively.

- **Cloud Services:** Bare-metal instances or optimized GPU VMs on cloud providers (e.g., AWS EC2, GCP Compute Engine, or regional Indian providers for DPDP compliance) dedicated to high-density GPU processing. Managed PostgreSQL for relational state, and a robust S3-compatible object storage layer (MinIO) for secure multimedia ingestion.
- **Networking:** A hub-and-spoke VPC topology isolates public-facing API gateways from private inference clusters. The edge layer uses highly available Load Balancers terminating TLS 1.3, forwarding traffic to the ingress tier via private subnets.
- **Infrastructure Layout:** Three primary tiers:
  1. **Edge/Ingestion:** High-throughput, low-latency API nodes built to handle chunky HTTP uploads from Android clients over intermittent WAN.
  2. **Control Plane:** Web servers (Next.js), asynchronous job queues (Redis), and orchestration nodes.
  3. **Inference Plane:** Auto-scaling groups of GPU-equipped worker nodes strictly dedicated to YOLO, faster-whisper, and Ollama inference.
- **Scaling Architecture:** Compute scales dynamically based on Redis queue depth for ASR/CV tasks, rather than mere CPU usage, ensuring timely processing of classroom audio/video streams.

## Kubernetes Architecture

Kubernetes is the orchestrator of choice, ensuring resilient, declarative management of the entire backend platform.

- **Cluster Topology:** Multi-zone clusters for high availability. Nodes are tainted and labeled: `gpu-inference` nodes for AI workloads, and `general-compute` for APIs, web admin shells, and background workers.
- **Deployment Strategy:** All applications are deployed as Helm charts. AI workloads utilize StatefulSets or Deployments with strict resource requests/limits aligned to the 12GB VRAM constraints to prevent OOM errors.
- **Autoscaling:** Horizontal Pod Autoscaler (HPA) manages API and web pods based on CPU/Memory. Cluster Autoscaler (CA) provisions new GPU nodes when pending pods cannot be scheduled, allowing scale-to-zero during off-school hours to optimize costs.
- **Ingress Architecture:** NGINX Ingress Controller or Traefik handles Layer 7 routing. Rate limiting and WAF rules are applied at the ingress level to protect the API gateway from abuse. Service Mesh (Istio or Linkerd) is employed for mTLS between internal microservices.

## Observability Stack

A comprehensive, zero-blind-spot observability stack ensures rapid MTTR (Mean Time To Recovery) and low alert fatigue.

- **Metrics:** Prometheus scrapes system and application metrics. Custom Exporters monitor GPU utilization, VRAM usage, and TensorRT engine latency. Grafana provides dashboards for node health, application throughput, and infrastructure costs.
- **Logging:** Promtail/Fluent Bit ships structured logs to Loki or Elasticsearch. All logs are anonymized at the edge to maintain DPDP compliance before persistence.
- **Tracing:** OpenTelemetry (OTel) instruments the FastAPI backend, Next.js frontend, and worker queues. Jaeger or Tempo correlates traces across the distributed system, identifying bottlenecks in the multimedia upload and inference pipeline.
- **Alerting:** Alertmanager handles critical routing via PagerDuty/Slack. Alerts are symptom-based (e.g., "High Talk Ratio Job Queue Latency" or "GPU Node OOM") rather than cause-based, minimizing noise.

## Security Architecture

Given the processing of highly sensitive classroom audio and visual data, security is absolute and non-negotiable.

- **IAM:** Strict least-privilege IAM roles are enforced for all cloud resources. Workload Identity binds Kubernetes service accounts to cloud roles, eliminating long-lived credentials.
- **Secret Management:** HashiCorp Vault or Kubernetes External Secrets securely injects sensitive configurations (database passwords, API keys) at runtime. Secrets are never stored in the repository.
- **Network Security:** Default-deny Kubernetes NetworkPolicies restrict pod-to-pod communication. The database and inference nodes have no public IP addresses. Strict DPDP compliance is maintained by ensuring all data at rest and in transit is AES-256 / TLS 1.3 encrypted, geographically pinned to Indian data centers.
- **Vulnerability Management:** Trivy scans all container images during the CI process. Dependabot monitors package dependencies. Any critical CVE immediately halts the pipeline.

## Reliability Strategy

The system is designed for failure, ensuring localized faults do not cascade across the platform.

- **Redundancy:** All stateless components (APIs, Next.js) run with a minimum of 3 replicas across multiple availability zones. Redis and PostgreSQL use highly available clustered setups.
- **Failover:** In case of zone degradation, traffic is automatically routed to healthy zones. Client applications (DAT) implement edge buffering to temporarily store captured data if the API goes offline.
- **Disaster Recovery:** Automated daily snapshots of the PostgreSQL database and MinIO metadata are taken and replicated to a cold-storage vault. Infrastructure-as-Code ensures a complete environment can be restored from scratch in under 30 minutes.
- **Self Healing Mechanisms:** Kubernetes liveness and readiness probes automatically restart deadlocked workers. Circuit breakers in the API prevent overwhelming the inference workers during traffic spikes.

## Cost Optimization

With a strict ₹0 customer hardware budget constraint, infrastructure must be aggressively optimized for cost-efficiency.

- **Infrastructure Savings:** The architecture explicitly leverages commodity consumer-class GPUs (e.g., RTX 5070) instead of enterprise datacenter GPUs (A100s) for inference, significantly reducing hourly compute costs while maintaining acceptable RTF (Real-Time Factor).
- **Resource Optimization:** Granular VRAM management is enforced. Models are quantized (e.g., INT8/FP16) where feasible to fit multiple models into a single 12GB VRAM node.
- **Scaling Efficiency:** The cluster employs aggressive scale-to-zero policies for GPU nodes during non-school hours, cutting compute costs by up to 60%. Spot instances or preemptible VMs are utilized for asynchronous queue workers (ASR processing) where job retries are trivial.

## Risks & Bottlenecks

Proactive identification of structural limits ensures the platform can scale gracefully.

- **Operational Risks:** The reliance on self-hosted inference for complex models (faster-whisper, YOLO) introduces operational burden in model serving, CUDA driver versioning, and TensorRT optimization.
- **Scaling Limitations:** Scaling consumer-grade GPUs in a cloud environment can be challenging due to availability constraints and VRAM limits. Sudden bursts of synchronous processing requests could overwhelm the Redis queues.
- **Security Risks:** Managing DPDP-compliant PII ingestion from edge devices (Meta Ray-Ban) necessitates flawless execution of redaction and anonymization before long-term storage.
- **Deployment Risks:** Multi-container Helm deployments involving large AI model weights can result in slow container startup times, affecting autoscaling responsiveness.

## Agile Sprint Plan

The rollout of this infrastructure will follow an iterative Agile approach.

- **Phase 1 (Sprint 1-2): Foundation & IaC.** Establish the Terraform scaffolding, VPC configuration, and deploy the foundational Kubernetes cluster. Implement basic CI/CD formatting and linting pipelines.
- **Phase 2 (Sprint 3-4): Storage & State.** Deploy highly available PostgreSQL and MinIO on the cluster. Establish external secrets and GitOps workflows via ArgoCD.
- **Phase 3 (Sprint 5-6): Application & AI Tier.** Deploy the API gateways, Next.js admin shell, and worker queues. Introduce the GPU node pools and validate the 12GB VRAM inference containers with synthetic data.
- **Phase 4 (Sprint 7-8): Observability & Hardening.** Integrate Prometheus, Grafana, and OpenTelemetry. Implement NetworkPolicies, run vulnerability scans, and conduct disaster recovery drills.
- **Expected Operational Improvements:** By Sprint 8, the platform will support end-to-end synthetic audio/video capture from the Android DAT client through the self-hosted inference pipeline, demonstrating a fully automated, scalable, and DPDP-compliant infrastructure with complete observability.
