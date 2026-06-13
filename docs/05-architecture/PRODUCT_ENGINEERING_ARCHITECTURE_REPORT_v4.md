# Product Engineering Architecture Report v4

## Problem Analysis

PedagogyX requires an elite, highly scalable, and privacy-preserving platform for multimodal AI classroom intelligence. The system must seamlessly ingest video and audio data from edge clients, primarily Meta Ray-Ban smart glasses via an Android host app, and process it centrally. A major challenge is maintaining high throughput and low-latency processing over intermittent network connections in Indian schools, adhering to strict data privacy requirements (DPDP compliance, G2 clearance blockers) and hardware constraints (zero customer infrastructure budget, reliance on centralized consumer-grade GPUs like the RTX 5070 with 12GB VRAM). The platform needs to bridge a complex offline-capable ingest pipeline with highly optimized asynchronous multimodal processing and a fast, accessible visualization layer.

## Architecture Design

The architecture follows a distributed, highly modular design to balance ingest load, async processing, and responsive frontends:

- **Client Tier**: Meta Ray-Ban glasses feed streams to an Android DAT host app, which buffers and uploads chunks reliably over volatile networks. Edge LAN nodes can act as local forwarders.
- **API & Ingestion Tier**: A stateless FastAPI cluster handles HTTP chunked multipart ingestion and provides secure REST endpoints. Scalable horizontally via Kubernetes HPA.
- **State & Storage Tier**:
  - PostgreSQL (via threaded connection pooling) manages structured relational metadata, pedagogical indices, and tenant state.
  - Redis serves as the message broker for Celery queues and ephemeral state.
  - MinIO provides durable S3-compatible blob storage for raw chunks and generated artifacts, decoupling binary data from the relational DB.
- **Inference Worker Tier**: Discrete Python worker pools (`worker-asr` using faster-whisper, `worker-cv` using YOLO, `worker-metrics`) pull tasks from Redis. They are physically segregated and optimized to maximize GPU utilization on 12GB VRAM constraints using quantization and model offloading.
- **Frontend Presentation Tier**: Next.js 15 App Router application rendering teacher dashboards. Leverages React Server Components (RSC) and Tailwind CSS v4 for optimized performance and minimal client bundles.

## Implementation Strategy

- **Phase 1: Robust Ingestion Platform**: Solidify the FastAPI ingestion API with resumable chunk uploads and cryptographic integrity checks to handle edge disconnects gracefully.
- **Phase 2: Asynchronous Intelligence Pipeline**: Refine the decoupled inference architecture. Deploy strict Dead Letter Queue (DLQ) implementations across all worker modules to trap unhandled exceptions and prevent main queue starvation.
- **Phase 3: Security & Tenancy**: Migrate from static `API_KEY` models to robust JWT and RBAC structures. Validate inputs heavily via Pydantic to enforce tenant isolation down to the PostgreSQL row level.
- **Phase 4: Client & Admin Interface**: Build out the Next.js teacher analytics dashboard. Use Server Actions for secured state mutations and implement real-time metric polling via optimized DB aggregations.
- **Phase 5: Edge Client Integration**: Complete end-to-end integration testing with the Android DAT companion app and Ray-Ban smart glasses hardware.

## Code Quality Strategy

- **Static Analysis & Formatting**: Enforce strict Python linting via Ruff, ensuring unused imports, complexity thresholds, and formatting standards are met. TypeScript and frontend components are validated with ESLint and Prettier. Markdown is checked via `markdownlint`.
- **Testing Requirements**: Comprehensive unit test coverage driven by Pytest for backend logic (mocking DB/MinIO dependencies). Vitest for the Next.js React components. Playwright for end-to-end visual and functional flow verification.
- **Type Safety**: Maintain end-to-end strict typing using Python Pydantic models for the API contracts and TypeScript interfaces for the Next.js frontend state.

## Performance Optimization

- **Database Concurrency**: Utilize `psycopg2.pool.ThreadedConnectionPool` efficiently across the FastAPI threadpool. Prevent N+1 query patterns by passing explicit `RealDictCursor` objects through helper domains.
- **Inference Constraints**: Quantize generative models (e.g., INT4/AWQ) to fit into the RTX 5070's 12GB VRAM limit alongside ASR and CV models. Batch requests dynamically at the worker boundary to maximize GPU throughput.
- **Frontend Delivery**: Heavily rely on Next.js 15 React Server Components (RSC) to render pedagogical metric views on the server, sending minimal HTML/JSON to the client to boost load speeds on low-end hardware.
- **Network Resiliency**: Implement intelligent exponential backoff in the Android client for chunk uploads, offloading pressure from the FastAPI ingress during thundering herd reconnection events.

## Security Considerations

- **Input Validation**: Zero trust applied at the API boundary; all inputs are strictly typed and sanitized via Pydantic schema validation.
- **Data Privacy & Compliance**: Minor student data must be anonymized before inference logic accesses it. PII is scrubbed, and raw data is isolated securely. Production workloads are blocked until explicit G2 clearance is achieved.
- **Secrets Management**: Enforcement of secure defaults. Base environment configurations default critical secrets (like API keys and DB URLs) to `None`, forcing explicit injection and avoiding accidental misconfigurations.
- **Authorization Boundary**: Strict RBAC limits data access ensuring teachers only view their own classrooms' aggregated insights and principals only view their designated school metrics.

## Observability

- **Centralized Telemetry**: All FastAPI nodes and Python worker instances emit structured JSON logs. Tracebacks from workers are captured via DLQs and directed to `sys.stderr` for log aggregation.
- **Health Probing**: Implementation of robust `/health` endpoints across FastAPI, PostgreSQL, MinIO, and Redis, validated during CI using `./scripts/compose-smoke.sh`.
- **System Metrics**: Monitoring API response times, DB connection pool saturation, Redis queue depths, and GPU VRAM utilization. Tracking these metrics ensures rapid scaling triggers via KEDA and quick remediation of bottleneck issues.

## Refactoring Opportunities

- **Database Connection Lifecycle**: Standardize context managers and connection pool fetching across legacy sync workers and API routes to ensure connections are efficiently released and not leaked.
- **DLQ Standardization**: Extract the Dead Letter Queue handling logic into a unified shared library for the `worker-asr`, `worker-cv`, and `worker-metrics` to avoid boilerplate and enforce consistent traceback capturing.
- **Frontend CSS Modernization**: Complete the migration of legacy inline styles in the Next.js platform to native Tailwind CSS v4 utility classes.

## Risks & Tradeoffs

- **Hardware vs Model Size**: Relying on RTX 5070 consumer GPUs (12GB VRAM) significantly restricts the use of large monolithic multimodal LLMs. **Tradeoff**: We adopt a modular approach using unimodal models (faster-whisper, YOLO) with late text fusion, improving throughput at the cost of architectural complexity.
- **Edge Connectivity**: Schools have volatile internet connectivity. **Tradeoff**: Increasing complexity in the Android capture client to manage local buffering and reliable chunking, rather than streaming directly over WebRTC, which would fail frequently.
- **Privacy Bottleneck**: The DPDP compliance framework forces a delay in utilizing real-world PII for ML tuning. **Tradeoff**: Dependence on heavily sanitized Mock Data Kits (MDK) in lower environments limits initial real-world accuracy until full clearance.

## Agile Sprint Plan

- **Sprint 1: Core Foundation & Ingestion**: Finalize the core architecture design. Deploy the FastAPI cluster with robust chunked multipart upload capabilities and durable MinIO storage.
- **Sprint 2: Queues & Resilient Workers**: Configure Redis queues, implement standard DLQ patterns, and deploy the base `worker-asr` and `worker-metrics` stubs. Ensure fault tolerance and graceful degradation.
- **Sprint 3: Database & Auth Scaling**: Implement threaded connection pooling. Transition the core platform from static API keys to RBAC-aware tenant isolation strategies.
- **Sprint 4: Next.js Presentation MVP**: Build the RSC-driven teacher analytics dashboard leveraging Tailwind v4. Integrate basic end-to-end testing with Playwright to verify visual stability.
- **Sprint 5: Client Integration & Load Optimization**: Conduct full-stack integration testing with the Meta Ray-Ban Android client. Profile GPU throughput and apply TensorRT/quantization optimizations to the inference workers.
