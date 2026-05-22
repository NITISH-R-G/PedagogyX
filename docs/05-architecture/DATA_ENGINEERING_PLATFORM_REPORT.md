# Data Engineering Platform & Architecture Report

**Version:** 1.0
**Author:** Autonomous Senior Data Engineer
**Scope:** Petabyte-Scale Distributed Educational Data Platform

## 1. Data Problem Analysis

PedagogyX presents unique data engineering challenges:

- **Massive Unstructured Volume:** Millions of hours of 1080p/720p classroom video from distributed edge nodes.
- **Multimodal Spatiotemporal Alignment:** We must tightly join asynchronous streams (WebRTC video, discrete microphone audio, screen capture telemetry) against a unified timeline.
- **Evolving Schemas:** AI inference outputs (e.g., YOLO bounding boxes, LLM JSON evaluations) change shapes as models iterate.
- **Strict Compliance:** India DPDP requires strict data residency, localized encryption, and complex data deletion workflows (right to be forgotten).

## 2. Data Architecture

Our architecture is a **Hybrid Edge-to-Cloud Data Lakehouse**, designed for the ₹0 customer budget constraint by utilizing OSS and avoiding hyperscaler lock-in.

- **Edge Tier (School LAN):** Local buffering and chunking. Handles WAN dropouts.
- **Ingest Tier (India Cloud):** High-throughput message buses.
- **Cold Storage (Lake):** MinIO for raw/processed video and raw JSON inference outputs.
- **Serving Tier (Warehouse):** PostgreSQL (relational metadata + pgvector) transitioning to ClickHouse for analytics as scale dictates.

## 3. Pipeline Design

**The D-PROC Hybrid Pipeline:**

1. **Capture & Chunk:** Capture agents slice A/V into 10-second MP4/WebM chunks locally.
2. **Edge Spooling:** Chunks are pushed to a local edge relay (e.g., an Nginx RTMP/HTTP buffer).
3. **Cloud Ingest:** Edge node pushes chunks to the central MediaMTX / Go API.
4. **Event Bus:** API writes metadata to a Redis queue indicating "Chunk X Ready."
5. **Worker Fan-Out:**
   - ASR Workers pull audio, run `faster-whisper`, push VTT/JSON to MinIO.
   - CV Workers pull video, run YOLO, push bounding box JSON to MinIO.
6. **Fusion Job:** A separate worker joins ASR and CV outputs, feeds them to Ollama for pedagogical scoring, and writes the structured result to PostgreSQL.

## 4. Storage & Warehouse Design

- **Object Storage (MinIO):** Self-hosted S3-compatible storage. Organized by `tenant_id/school_id/session_id/`. Lifecycle policies will move raw video to cold tiers or delete after 30 days, retaining only metadata.
- **Operational DB (PostgreSQL):** Stores user data, RBAC, session metadata, and final pedagogical scores.
- **Vector DB (pgvector):** Used for semantic search over lesson transcripts.
- **Future Warehouse (ClickHouse):** Once we hit >10,000 sessions/day, we will pipe PostgreSQL CDC (via Debezium) into ClickHouse for real-time dashboard aggregations.

## 5. Data Quality & Governance

- **Schema Contracts:** All ML workers must validate outputs against Pydantic models before writing.
- **Data Lineage:** Every row in the final score table must contain a `model_version` array indicating exactly which ASR, CV, and LLM models generated it.
- **PII Masking:** Audio streams undergo real-time local bleeping (if required) or post-process redaction before hitting the cold-storage archive.

## 6. Observability

- **Pipeline Metrics:** Prometheus scraping custom metrics from the Go API and Python workers (e.g., `queue_depth`, `chunk_processing_latency`).
- **Data Freshness Monitors:** Alerts triggered if a session remains in "processing" state for > 2 hours.
- **Dashboards:** Grafana dashboards visualizing ingestion rates vs worker throughput.

## 7. Security & Compliance

- **Encryption:** AES-256 for MinIO data at rest. TLS 1.3 for all in-transit data.
- **Residency:** All infrastructure strictly hosted in `ap-south-1` equivalent datacenters in India.
- **Tenant Isolation:** Logical separation in Postgres via `tenant_id` on every table; dedicated MinIO buckets per large district.

## 8. Performance Optimization

- **Zero-Copy Streaming:** Optimizing the edge-to-cloud transfer to avoid unnecessary disk I/O on the API gateway.
- **Batching ML Inference:** Grouping video chunks into larger batches to saturate the RTX 5070 memory during cold-path processing.

## 9. Risks & Tradeoffs

- **Risk:** Postgres becomes a bottleneck for high-frequency ML inference writes.
  - **Tradeoff:** We write heavy JSON payloads to MinIO and only write summary statistics to Postgres.
- **Risk:** Unreliable school internet corrupts uploaded chunks.
  - **Mitigation:** Edge agent calculates checksums; cloud API verifies and requests re-transmission if failed.

## 10. Agile Sprint Plan (Data Track)

- **Sprint 03:** Stand up MinIO and Postgres via Docker Compose. Implement Go API upload endpoint.
- **Sprint 04:** Build Python worker harness connecting to Redis queue. Define Pydantic schemas for ASR outputs.
- **Sprint 05:** Implement the Data Fusion job that reads ASR/CV JSON from MinIO and writes final metrics to Postgres.
