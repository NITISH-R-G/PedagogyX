# Elite System Design & Architecture Report

**Status:** Draft v1.0
**Owner:** Autonomous Senior Systems Engineer & System Design Architect

This document details the world-class, globally distributed, massively scalable, and fault-tolerant architecture for PedagogyX. As a Senior Systems Architect, I have designed this system to operate reliably under extreme production load, process massive volumes of multimodal classroom data, and guarantee rigorous privacy compliance.

## System Overview

PedagogyX is a deep-tech, multimodal AI classroom intelligence platform focused on teacher optimization. The system ingests vast streams of real-time point-of-view (POV) video and audio captured via Meta Ray-Ban smart glasses (using the Wearables DAT SDK on Android host devices) and fixed low-end smartboards.

**Purpose:** Provide longitudinal pedagogical analytics, talk-ratio estimation, and automated coaching insights.
**Requirements:** Robust ingestion of multi-GB video/audio streams, low-latency "hot path" insights, deep authoritative "cold path" ML evaluation, zero-downtime scalability, and DPDP-compliant data residency.
**Scale Assumptions:** Millions of concurrent capturing sessions, heavy network volatility in rural school environments, PB-scale media ingestion per month, and massive transient spikes in traffic (e.g., end-of-class uploads).
**Constraints:** Hardware limitations on edge capture devices (low RAM/CPU constraints), intermittent connectivity, bounded compute budgets on central worker nodes (consumer-grade RTX 5070 clusters scaling to enterprise GPUs), and strict Indian data residency mandates.

## High Level Architecture

The architecture utilizes a deeply decoupled, modular **Hybrid Edge-Cloud (Tiered)** topology to isolate unpredictable edge environments from the core inference engines.

- **Edge Capture & Ingest Buffer:** Meta Ray-Ban smart glasses capture AV data via Bluetooth to an Android DAT host. The host app performs local chunking, SQLite state management, and implements an edge buffering strategy (D-PROC hybrid model) to handle transient network loss.
- **Ingestion Gateway (Hot Path):** A fleet of stateless API reverse proxies (FastAPI/Go) terminating TLS, performing JWT authentication, and immediately offloading binary payloads to object storage to prevent memory exhaustion.
- **Message Bus & Orchestration:** A distributed queueing tier (Kafka for high-throughput streaming, Redis for MVP) that decouples ingestion from heavy computation.
- **Asynchronous ML Processing (Cold Path):** Scalable GPU worker pools dedicated to specific tasks: `Worker-ASR` (Whisper), `Worker-CV` (YOLO/SCB-DETR), and `Worker-Pedagogy` (LLM fusion). These run decoupled and stateless, enabling heterogeneous scaling.
- **Control Plane:** Web administration shell (Next.js) fetching aggregated insights from a materialized read-store.

## Infrastructure Design

- **Deployment Topology:** Multi-zone, highly available Kubernetes clusters hosted in an India-based cloud region (e.g., ap-south-1).
- **Cloud Architecture:** Immutable infrastructure-as-code (Terraform) defining Virtual Private Clouds (VPCs), strict Network Security Groups, and multi-tier subnets (public ingress, private compute, isolated data).
- **Networking:** Anycast DNS routing into highly available API Gateways. Internal service-mesh (e.g., Istio) enforcing mTLS between microservices, traffic shaping, and circuit breaking.
- **Orchestration:** Kubernetes (EKS/GKE equivalent) managing auto-scaling node groups. Node taints and tolerations are utilized to isolate heavy GPU workloads from general-purpose API compute, minimizing blast radius and maximizing resource efficiency.

## Database Design

- **Schema Strategy:** Polyglot persistence model.
  - **Relational:** PostgreSQL (primary) structured into tightly bounded contexts (Tenant/RBAC, Session Metadata, Rubrics).
  - **Object Storage:** S3-compatible MinIO for chunked media streams, decoupled from DB compute.
  - **Vector:** Future Qdrant deployment for semantic RAG (Retrieval-Augmented Generation) on lesson transcripts.
- **Replication:** Multi-AZ synchronous streaming replication for PostgreSQL to guarantee RPO near zero. Object storage utilizes erasure coding and cross-region replication for disaster recovery.
- **Scaling:** Vertical scaling for the primary relational write node, paired with an array of horizontally scaled read replicas. Implementation of CQRS (Command Query Responsibility Segregation) patterns to offload complex analytical dashboard queries from the transaction path.
- **Consistency Model:** Strong consistency on tenant RBAC and session state; eventual consistency on ML processing metrics and aggregated dashboard views.

## Scalability Strategy

- **Horizontal Scaling:** Auto-scaling driven by custom metrics (HPA on Kubernetes via Prometheus). API gateways scale linearly based on RPS. Worker nodes scale dynamically based on queue depth and processing latency SLA.
- **Caching:** Distributed Redis clusters implementing read-through and write-behind caching for high-frequency dashboard queries, drastically reducing PostgreSQL load.
- **Partitioning:** Database sharding by Tenant ID (District/School) to ensure horizontal database growth and strict data isolation.
- **Load Balancing:** Layer 7 application load balancers managing external traffic, terminating TLS, and dynamically routing based on API version and tenant mapping.

## Reliability Strategy

- **Failover:** Automatic leader election in PostgreSQL clusters. Stateless workers implicitly tolerate termination and resume jobs from dead letter queues (DLQs) automatically.
- **Redundancy:** N+2 redundancy across all critical microservices. Availability zone awareness configured in Kubernetes schedulers to prevent single-rack failures from causing outages.
- **Recovery Mechanisms:** Continuous point-in-time recovery (PITR) backups for relational databases. Automated chaos engineering simulations to validate system self-healing capabilities.
- **Resilience Patterns:** Exponential backoff with jitter on edge clients. Circuit breakers, bulkheads, and timeouts implemented at every inter-service boundary.

## Security Architecture

- **Authentication:** OAuth2/OIDC integration for admin dashboards; secure, short-lived JWTs scoped to specific hardware device identities for capture agents via mTLS.
- **Authorization:** Strict, multi-tiered Role-Based Access Control (RBAC). Row-Level Security (RLS) embedded deeply within PostgreSQL schemas to enforce multi-tenant boundaries at the database kernel level.
- **Encryption:** TLS 1.3 mandated for all transit data. AES-256 GCM encryption at rest for object storage (via KMS) and database volumes.
- **Abuse Prevention:** Dynamic Layer 7 rate limiting via API gateways. Web Application Firewall (WAF) to filter malicious traffic. Continuous dependency vulnerability scanning and zero-trust container policies (non-root execution, dropped capabilities).

## Observability Stack

- **Logging:** Centralized, structured JSON logging via Fluent-bit aggregated into an ELK or Loki stack, enabling high-cardinality search and rapid incident forensics.
- **Tracing:** End-to-end distributed tracing via OpenTelemetry (OTel), propagating context headers from the Android capture device through the ingest proxy, queue, and across all microservice boundaries.
- **Monitoring:** Prometheus time-series database scraping high-resolution metrics (p50, p95, p99 latency, queue lag, GPU memory utilization).
- **Alerting:** Alertmanager routing actionable, symptom-based alerts to PagerDuty. Strict "low noise" alerting policies—paging only on SLA breaches (e.g., error rate spikes, elevated p99 latency).

## Performance Optimization

- **Bottlenecks:** Identified critical paths in I/O (video chunk writes) and GPU memory bandwidth (large ONNX model swaps).
- **Latency Optimization:** Implementing CDN edge-termination for static assets and API gateways physically closer to the users. Decoupling slow ML tasks from the "hot path" ingress to guarantee sub-100ms API response times.
- **Throughput Optimization:** Streaming large video payloads directly to MinIO via presigned URLs to bypass API application memory. Batching CV tasks to fully saturate RTX 5070 tensor cores using TensorRT optimizations. Using highly optimized serialization (e.g., Protobuf/gRPC) for internal microservice communication.

## Tradeoffs

- **Pros:** Massively decoupled, deeply resilient, easily scalable, allows independent evolution of ML models vs. ingestion APIs.
- **Cons:** Architectural complexity is high. Eventual consistency requires careful UX design to set user expectations (e.g., "Insights are generating...").
- **Limitations:** Phase 0 compute relies on consumer-grade RTX 5070s; scaling to tens of thousands of concurrent streams will necessitate a costly migration to A100/H100 data center GPUs.
- **Future Improvements:** Migrating from Redis to Apache Kafka for durable, replayable event streaming. Introducing WebRTC for true real-time, low-latency live class monitoring. Transitioning to a globally distributed database (e.g., CockroachDB) as international expansion occurs.

## Agile Sprint Plan

- **Phase 1 (Ingestion & Foundations):** Deploy IaC, setup Kubernetes clusters, implement the API Gateway, and establish the secure chunked upload pipeline to MinIO.
- **Phase 2 (Orchestration & State):** Roll out PostgreSQL (with RLS), Redis queues, and foundational RBAC. Implement the DLQ and retry mechanisms.
- **Phase 3 (Inference Engine):** Deploy decoupled worker node pools (Worker-ASR, Worker-CV, Worker-Pedagogy). Optimize GPU batching and implement ONNX/TensorRT acceleration.
- **Phase 4 (Analytics & Optimization):** Launch Next.js dashboards. Instrument full OTel observability stack. Conduct extensive load testing and chaos engineering to harden reliability.
- **Milestones:** M1: Secure video ingestion at scale. M2: Decoupled offline AI scoring. M3: Real-time dashboard insights.
- **Risk Assessment:** High risk on network instability from edge clients—mitigated by robust local SQLite buffering. Moderate risk on GPU utilization costs—mitigated by strict inference batching and asynchronous processing.
