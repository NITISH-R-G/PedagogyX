# PedagogyX Distributed System Design Report

## System Overview

- **Purpose**: PedagogyX is a multimodal AI classroom intelligence and teacher optimization platform designed to provide both real-time insights (hot path) and authoritative batch analytics (cold path) for educational environments.
- **Requirements**:
  - Open Source Software (OSS) first, fully self-hosted, no proprietary APIs (e.g., no OpenAI, AWS Transcribe).
  - Data residency in India (DPDP privacy compliance).
  - Hybrid Edge-Cloud architecture (D-PROC=C).
  - Strict ₹0 customer hardware budget for classroom deployments.
  - Thin clients via Meta Ray-Ban smart glasses (Android DAT companion app) and low-end Windows smartboards.
  - Dual pipeline: a low-latency WebRTC live stream (audio + 1 cam) and a durable batch multi-cam upload.
  - Supervision mode with hierarchical RBAC for Admin dashboards.
- **Scale Assumptions**:
  - Millions of students across thousands of schools in India.
  - Massive concurrent morning login/startup spikes.
  - High video/audio data ingestion throughput per classroom.
  - Constrained edge bandwidth in rural/semi-urban schools.
- **Constraints**:
  - Heavy cost constraints on GPU usage (RTX 5070 dev budget, D-10 cloud budget).
  - Poor WAN connections at edge sites.
  - Zero tolerance for PII/data leaks.

## High Level Architecture

- **Major Components**:
  - **Capture Layer**: Android host app for Meta Ray-Ban DAT and Windows Desktop Agent.
  - **Edge Node (LAN)**: District/school local ingest and buffer to mitigate WAN unreliability.
  - **Hot Path (Real-Time)**: WebRTC SFU (MediaMTX) for live analytics, routing to lightweight YOLO and rolling talk-ratio estimation.
  - **Cold Path (Batch)**: Chunked, resumable uploader writing to MinIO for authoritative, deep transformer-based diarization and pedagogy scoring.
  - **Control Plane**: FastAPI Backend API, Tenant/RBAC Manager, PostgreSQL DB.
  - **Asynchronous Workers**: Redis-backed job queues feeding GPU workers for faster-whisper (ASR), computer vision (CV), and LLM pipelines.
- **Interactions**:
  - Clients authenticate and retrieve session descriptors.
  - Clients stream real-time components via WebRTC and background-upload high-res recordings via chunked HTTPS.
  - FastAPI enqueues processing jobs. GPU workers pull jobs, fetch media from MinIO, process, and write results to PostgreSQL.
- **Data Flow**:
  - Camera/Mic -> Edge Ingest -> MediaMTX -> Real-time Bus -> Live Admin UI.
  - Camera/Mic -> Edge Buffer -> MinIO Archive -> Transcode -> ML Fusion -> Final Pedagogy Score -> Admin Analytics UI.
- **Service Boundaries**:
  - Separated concerns between Capture, Storage, Sync, Auth, Hot-Path Analytics, and Batch ML Fusion.

## Infrastructure Design

- **Deployment Topology**:
  - Hybrid Edge-Cloud.
  - Lightweight Edge nodes (Docker/k3s) on local school networks acting as local reverse proxies and stream buffers.
  - Central Cloud infrastructure in an India-based FOSS-friendly cloud or bare-metal provider.
- **Cloud Architecture**:
  - Self-hosted Kubernetes (or Nomad) cluster managing stateless API nodes and stateful ML worker nodes.
  - Distinct node pools for CPU (API, DB, Ingest) and GPU (ML Workers).
- **Networking**:
  - Tailscale or Wireguard for secure Edge-to-Cloud communication.
  - API Gateway and Ingress controllers handling rate-limiting and JWT validation.
- **Orchestration**:
  - Infrastructure as Code using Terraform/Ansible.
  - Workloads managed via Helm and ArgoCD for GitOps deployment.

## Database Design

- **Schema Strategy**:
  - Multi-tenant architecture using PostgreSQL row-level security (RLS) or tenant ID partitioning.
  - Clear separation between raw metadata, preliminary hot-path scores, and authoritative cold-path analytics.
- **Replication**:
  - PostgreSQL primary-replica setup for high availability and read-scaling.
  - MinIO distributed mode with erasure coding for high durability of large media blobs.
- **Scaling**:
  - Connection pooling using PgBouncer to prevent connection exhaustion from stateless workers and API nodes.
  - Sharding by district or region if single-cluster limits are reached.
- **Consistency Model**:
  - Read-Committed for metadata.
  - Eventual consistency for analytics and scores (acceptable since cold path processing takes time).

## Scalability Strategy

- **Horizontal Scaling**:
  - Stateless FastAPI layer and GPU workers scale horizontally based on queue depth and CPU/GPU utilization.
- **Caching**:
  - Redis for caching session data, tenant configurations, and RBAC policies.
  - CDN (if applicable for static assets, though internal dashboard usage limits this necessity).
- **Partitioning**:
  - PostgreSQL table partitioning by time (e.g., monthly) for session metrics.
- **Load Balancing**:
  - Layer 4/7 load balancing at the cloud edge (HAProxy/Nginx).

## Reliability Strategy

- **Failover**:
  - Automatic pod eviction and rescheduling in Kubernetes.
  - Database automatic failover using Patroni.
- **Redundancy**:
  - Multi-AZ cloud deployment.
  - Local edge buffer handles WAN disconnects seamlessly via resumable chunked uploads.
- **Recovery Mechanisms**:
  - Dead letter queues for failed ML processing jobs.
  - Automated backups to cold storage (e.g., S3 Glacier equivalent or local tape) for disaster recovery.
- **Resilience Patterns**:
  - Circuit breakers on API gateway to prevent cascading failures.
  - Backpressure handling in WebRTC ingest to drop frames rather than crash under load.

## Security Architecture

- **Authentication**:
  - Bearer token (JWT) API key validation for edge devices.
  - Strict OAuth2/OIDC for dashboard users.
- **Authorization**:
  - Deep Hierarchical RBAC (Teacher, Coach, School Admin, District Admin).
  - RLS in PostgreSQL to prevent cross-tenant data leakage.
- **Encryption**:
  - TLS 1.3 everywhere (in-transit).
  - AES-256 for MinIO data at rest and PostgreSQL TDE.
- **Abuse Prevention**:
  - Rate limiting via Redis on the API Gateway.
  - Strict payload size limits and chunk validation.

## Observability Stack

- **Logging**:
  - Structured JSON logs aggregated via Promtail/Loki.
- **Tracing**:
  - OpenTelemetry auto-instrumentation for FastAPI and Python ML workers, visualized in Jaeger/Tempo.
- **Monitoring**:
  - Prometheus scraping metrics from nodes, Postgres (postgres_exporter), Redis, and custom API/Worker metrics.
- **Alerting**:
  - Grafana and Alertmanager configured for critical thresholds (e.g., GPU memory exhaustion, queue buildup, elevated 5xx rates).

## Performance Optimization

- **Bottlenecks**:
  - Inference time on RTX 5070 constraints.
  - Network throughput from rural schools.
- **Latency Optimization**:
  - Hot path skips deep ML, using lightweight heuristics and 5s rolling windows.
- **Throughput Optimization**:
  - Batching multiple inputs to `model.predict(stream=True)` for Ultralytics YOLO to maximize parallel efficiency and memory overhead.
  - Asynchronous chunked uploads minimize active TCP connection time.

## Tradeoffs

- **Pros**:
  - Complete control over data and privacy (crucial for DPDP).
  - Low OPEX at scale due to OSS/bare-metal choices.
  - High resilience to network drops due to edge buffering.
- **Cons**:
  - Higher initial operational complexity (managing own MinIO, GPU clusters, K8s).
  - Inference hardware procurement and maintenance falls on the organization.
- **Limitations**:
  - Real-time features are heavily simplified compared to batch path.
- **Future Improvements**:
  - Implementation of dedicated NPUs or edge TPUs to move inference to the classroom.
  - Federated learning to improve models without moving raw video to the cloud.

## Agile Sprint Plan

- **Phase 1 (MVP Foundation)**:
  - Deliver barebones API, MinIO chunk upload, and basic PostgreSQL migrations.
  - Stub out worker queues and build Next.js admin shell.
- **Phase 2 (Hot Path & Edge)**:
  - Implement WebRTC ingest and 5s rolling talk-ratio logic.
  - Finalize Android DAT client connectivity.
- **Phase 3 (Cold Path & Deep ML)**:
  - Integrate faster-whisper diarization and YOLO multi-cam batch processing.
  - Connect scoring engine to authoritative Admin dashboard.
- **Phase 4 (Scale & Hardening)**:
  - Load testing, auto-scaling configuration, and comprehensive security audits.
  - Establish complete OpenTelemetry distributed tracing.
