# System Design Architecture Report

**Status:** Phase 0 Architecture Planning
**Date:** 2026-05-30
**Owner:** Architecture Team

As the Autonomous Senior Systems Engineer & System Design Architect, the following structured report details the comprehensive design for the PedagogyX system, scaling from initial India-based MVP to global enterprise deployment.

## 1. System Overview

PedagogyX is a deep-tech educational AI platform designed to ingest, process, and analyze multimodal classroom data (audio, video, text). The system provides longitudinal pedagogical analytics and AI coaching insights. The current Phase 0 targets low-end Android/Windows devices and Meta Ray-Ban glasses for edge capture, pushing data to an India-based central cloud (ap-south-1) for rigorous privacy-first processing.

## 2. High Level Architecture

The architecture follows a Hybrid Edge-Cloud model, optimized for intermittent network connectivity and heavy batch processing:

- **Edge Capture Agents:** Deployed on Meta Ray-Bans (via DAT) and Android/Windows smartboards. Responsible for local buffering, chunking, and secure HTTPS transport.
- **Ingest Gateway:** Highly available API layer to receive resumable chunked uploads.
- **Message Broker (Redis/Kafka):** Decouples the ingest pipeline from the heavy inference workloads.
- **Multimodal Inference Workers:** GPU-accelerated microservices handling ASR (faster-whisper), CV, and NLP tasks asynchronously.
- **Central API & Analytics Engine:** Serves aggregated data to the Next.js web application for administrators and teachers.

## 3. Infrastructure Design

- **Compute:** Kubernetes (or Docker Compose for MVP) orchestrating stateless API services and stateful worker queues.
- **Storage:** MinIO (S3-compatible) for highly scalable, durable object storage of raw and processed media chunks.
- **Database:** PostgreSQL for structured relational data (sessions, user accounts, rubrics) and time-series metrics.
- **Network:** API Gateway for routing, rate limiting, and SSL termination.

## 4. Database Design

- **Relational Storage (PostgreSQL):** Utilizes structured schemas for RBAC, session metadata, and institutional hierarchy. Heavily relies on Row-Level Security (RLS) for multi-tenant data isolation.
- **Vector/Embedding Storage:** Future phases will incorporate a vector database (e.g., Milvus or Qdrant) for semantic search across lesson transcripts and multimodal embeddings.
- **Caching:** Redis for rapid retrieval of live dashboard metrics and session state.

## 5. Scalability Strategy

- **Asynchronous Processing:** By decoupling upload from inference, the system can queue jobs during peak school hours and process them overnight or during off-peak times.
- **Horizontal Scaling:** API nodes and ML worker nodes scale independently based on CPU/GPU utilization and queue depth.
- **Edge Resiliency:** Capture agents implement robust local SQLite databases and persistent file storage to handle prolonged network outages without data loss.

## 6. Reliability Strategy

- **Idempotent Operations:** All API endpoints and background jobs are designed to be idempotent to handle retries seamlessly.
- **Graceful Degradation:** If the GPU cluster is overwhelmed, the system falls back to prioritizing audio processing (ASR) over heavier video CV tasks.
- **Data Integrity:** Multi-part uploads with checksum validation ensure chunks are not corrupted over poor WAN links.

## 7. Security Architecture

- **Authentication:** API keys (MVP) and eventually OAuth2/OIDC for institution-level SSO.
- **Encryption:** TLS 1.3 for data in transit; AES-256 for data at rest (MinIO and Postgres).
- **Compliance:** Designed with India DPDP compliance in mind. Future-proofed for FERPA and GDPR via strict data lifecycle policies and automated redaction pipelines.
- **Zero Trust:** Worker nodes operate in isolated networks with no inbound access, pulling jobs from the central queue.

## 8. Observability Stack

- **Metrics:** Prometheus for scraping system and application metrics (e.g., queue lengths, inference latency).
- **Logging:** Fluent-bit/Loki for centralized structured logging.
- **Tracing:** OpenTelemetry (OTel) distributed tracing across the ingest, queue, and worker boundaries to pinpoint bottlenecks.
- **Dashboards:** Grafana for real-time visualization of system health.

## 9. Performance Optimization

- **GPU Utilization:** Batching inference requests to maximize throughput on consumer-grade (RTX 5070) or enterprise GPUs.
- **Model Quantization:** Utilizing INT8/FP16 precision for ASR and CV models to reduce memory footprint and increase inference speed.
- **Efficient Codecs:** Enforcing modern audio/video codecs at the edge to minimize upload bandwidth requirements.

## 10. Tradeoffs

- **Latency vs. Cost:** Opting for asynchronous batch processing reduces cloud infrastructure costs significantly but prevents immediate real-time coaching feedback.
- **Edge Compute vs. Cloud Compute:** Keeping the edge devices "dumb" (upload only) simplifies deployment on low-end hardware but increases cloud ingestion costs and bandwidth dependency.
- **MVP Simplicity vs. Enterprise Readiness:** The current architecture uses Redis for queuing and basic API keys to expedite Phase 0, knowing these must be refactored to Kafka and OIDC before massive scale.

## 11. Agile Sprint Plan

- **Sprint 1:** Finalize Phase 0 documentation and legal sign-offs (G2). Complete mock capture agent.
- **Sprint 2:** Implement robust chunked upload API and MinIO integration.
- **Sprint 3:** Deploy asynchronous worker architecture (Redis + Python workers).
- **Sprint 4:** Integrate faster-whisper for initial ASR pipeline and deploy Next.js analytics dashboard.
- **Sprint 5:** End-to-end performance benchmarking and threat modeling workshop.
