# Product Engineering Architecture Report v4

## Problem Analysis

PedagogyX is developing an advanced, AI-driven multimodal classroom intelligence platform. The primary client interfaces are Meta Ray-Ban smart glasses operating through an Android-based companion app (`clients/android-capture-dat`) and low-end Windows smartboards.
The system must operate effectively in heavily constrained environments, such as Indian school districts characterized by low bandwidth and intermittent connectivity. We utilize a centralized open-source software (OSS) backend powered by cost-effective consumer-grade hardware (e.g., RTX 5070 GPUs).
A foundational requirement is strict adherence to India's DPDP (Digital Personal Data Protection) framework, demanding a zero-trust, privacy-first architecture. Production student data is entirely blocked from systemic ingestion until formal G2 clearance is obtained. The primary engineering challenge lies in delivering robust multi-stream media ingestion, ultra-low-latency processing loops, and fault-tolerant distributed system reliability—all engineered under strict zero-budget infrastructure constraints for the target customers (D-10 baseline).

## Architecture Design

- **Client & Edge Tier**
  - **DAT Host Agent:** An Android-based application acting as the primary interface bridge for Meta Ray-Ban glasses, alongside corresponding software for low-end Windows smartboards. These serve as robust edge capture agents.
  - **Resilient Buffering:** Edge node caching mechanisms designed to handle intermittent school LAN connectivity gracefully.
- **Ingestion & API Gateway Plane**
  - **FastAPI Core:** A stateless, high-throughput gateway managing session instantiation, dynamic HTTP chunk media ingestion, and routing.
  - **Tenant Isolation:** Enforced via strict RBAC at the gateway layer.
- **Asynchronous Inference & Processing**
  - **Worker Fleet:** Specialized background Python workers decoupled from the API gateway.
    - `worker-asr`: Handles audio transcription via faster-whisper.
    - `worker-cv`: Processes computer vision tasks via YOLO models.
    - `worker-metrics`: Computes pedagogical insights from the extracted telemetry.
  - **Message Broker:** Redis serves as the high-speed task queue binding the ecosystem.
- **Data & Object Storage Layer**
  - **Relational DB:** PostgreSQL securely stores normalized telemetry, pedagogical indices, and structured user mappings.
  - **Blob Storage:** MinIO provides S3-compatible, durable object storage for high-volume video/audio chunks and serialized ML artifacts.
- **Frontend Presentation Layer**
  - **Web Console:** A React and Next.js-based application functioning as an administrative shell.
  - **Bimodal Presentation:** Displays metrics via a dual-lane approach—a Hot Path for near-real-time heuristic feedback and a Cold Path for deep, batch-processed authoritative evaluations.

## Implementation Strategy

- **Phase 1: Resilient Edge-to-Cloud Ingestion**
  - Finalize the Docker Compose orchestrated microservice stack (`api`, `MinIO`, `PostgreSQL`, `Redis`).
  - Solidify robust, resumable multipart chunk upload protocols handling high-latency retries and cryptographic signature validation to combat intermittent connectivity.
- **Phase 2: Decoupled Worker Pipelines**
  - Operationalize isolated Celery/Python worker domains (`worker-asr`, `worker-cv`, `worker-metrics`) attached to Redis queues.
  - Instantiate a rigorous Dead Letter Queue (DLQ) topology to gracefully isolate processing exceptions and prevent queue poisoning.
- **Phase 3: Secure Presentation Layer**
  - Develop Next.js React Server Components (RSC) to render pedagogical dashboards securely.
  - Enforce server-side data fetching to minimize the client-side execution footprint and ensure strict data governance.
- **Phase 4: Hardware-Optimized Inference**
  - Transition from simulated CPU-bound inference mocks to high-efficiency GPU-bound operations tailored for RTX 5070 constraints, leveraging TensorRT execution environments and vLLM quantization techniques.

## Code Quality Strategy

- **Static Analysis & Enforcement**
  - Python: Enforce rigorous formatting, linting, and complexity checks via Ruff across the backend and worker fleet.
  - TypeScript/Frontend: Utilize ESLint and Prettier to maintain strict consistency within the React/Next.js environment.
  - Documentation: Ensure all markdown complies with formatting rules via `markdownlint`, verifiable through `./scripts/dev-verify.sh --docs-only`.
- **Testing & Continuous Integration**
  - Enforce high-coverage unit testing across backend services, rigorously mocking external dependencies (Postgres via `psycopg2.pool`, MinIO, Redis).
  - Implement Vitest for fast, reliable unit and integration verification in the frontend UI components.
- **Type Safety Guarantees**
  - Deep type enforcement using comprehensive Pydantic v2 schemas in Python and strict TypeScript interfaces across the Next.js boundary.

## Performance Optimization

- **Database Efficiency**
  - Eliminate N+1 query patterns by optimizing object-relational mapping patterns and sharing database connection pools effectively within FastAPI helper functions.
- **Worker Concurrency Model**
  - Strictly isolate heavy inference workloads (ASR, CV) into dedicated background workers, completely decoupled from the asynchronous FastAPI process pool to prevent HTTP starvation.
- **Frontend Rendering Velocity**
  - Maximize the use of Next.js React Server Components (RSC) to aggressively minimize the JavaScript bundle payloads delivered to end-user browsers.
- **Model Quantization**
  - Deploy Large Language Models optimized via INT4/AWQ quantization to operate securely and efficiently within the tight 12GB VRAM limitations of the target RTX 5070 deployment hardware.

## Security Considerations

- **Configuration Integrity**
  - Enforce explicit initialization of critical environment variables (`DATABASE_URL`, `REDIS_URL`, `API_KEY`) and entirely remove fallbacks or hardcoded default credentials from the codebase.
- **Authentication & Authorization Policy**
  - Implement uncompromising API key validation paired with a granular Role-Based Access Control (RBAC) matrix to guarantee tenant isolation and adhere to G2 clearance mandates.
- **Edge Boundary Validation**
  - Mandate strict Pydantic schema validation over all inbound API payloads to mitigate injection vectors or malformed object vulnerabilities.
- **Data Privacy & Anonymization**
  - Enforce systemic anonymization: Student identifiers and raw facial features are mathematically scrubbed from LLM context windows. Only synthesized, anonymized transcripts and metadata are persisted for analysis.

## Observability

- **Unified Telemetry Streams**
  - Aggregate standardized, context-rich JSON structured logs across the API gateway, worker fleet, and frontend server.
  - Ensure background worker exceptions (including deep tracebacks) are explicitly captured and routed to `sys.stderr` and the DLQ monitoring stack.
- **Proactive Health Probes**
  - Maintain rigorous, system-wide `/health` and `/readiness` endpoints in all microservices, inherently validated by CI via `./scripts/dev-verify.sh`.
- **Hardware & Queue Monitoring**
  - Implement granular tracking of GPU VRAM saturation metrics, Celery queue latency/depth, and heuristic model drift indicators across the platform.

## Refactoring Opportunities

- **DLQ & Error Handling Standardization**
  - Systematically refactor error capture mechanisms across all heterogeneous async worker instances (`worker-asr`, `worker-metrics`, `worker-cv`) to a unified, resilient DLQ design pattern.
- **Frontend CSS Modernization**
  - Deprecate isolated, inline styles within the Next.js admin portal, migrating entirely to utility-first Tailwind CSS classes for scalable, maintainable design.
- **API Monolith Decomposition**
  - Incrementally refactor monolithic API route controllers within FastAPI into modular, domain-driven service components, enhancing testability and architectural separation of concerns.

## Risks & Tradeoffs

- **Intermittent Edge Connectivity**
  - _Risk:_ Reliance on erratic school infrastructure amplifies upload failure rates.
  - _Tradeoff:_ We choose to absorb substantial engineering complexity into resilient chunk buffering and state reconciliation on the edge client rather than demanding unrealistic network reliability.
- **Strict VRAM Hardware Constraints**
  - _Risk:_ Consumer-grade GPUs (RTX 5070 with 12GB VRAM) structurally prevent the use of monolithic foundational models.
  - _Tradeoff:_ We pivot to a pipeline of specialized, unimodal extraction engines (Whisper + YOLO), orchestrating late-stage text-fusion for inference, trading architectural simplicity for hardware viability.
- **Data Privacy G2 Blockers**
  - _Risk:_ Absolute prohibition on processing real student data until regulatory G2 clearance is secured delays authentic accuracy benchmarking.
  - _Tradeoff:_ Total reliance on synthetic Mock Data Kits (MDK) for early-stage ML tuning limits real-world model precision initially, but is non-negotiable to mitigate severe legal liability.

## Agile Sprint Plan

- **Sprint 1: Core Gateway & Infrastructure Foundation**
  - Deploy PostgreSQL schemas, configure MinIO S3 buckets, and stabilize FastAPI endpoints handling multipart chunk ingestion securely.
- **Sprint 2: Decoupled Processing Pipeline**
  - Bring `worker-asr` and `worker-metrics` consumers online, implement structured DLQ topologies, and optimize Redis queue mechanics.
- **Sprint 3: Edge Client Integration (Meta Ray-Ban)**
  - Integrate the Android DAT app (`clients/android-capture-dat`) and hardware simulator securely with the centralized API gateway, verifying end-to-end data transmission telemetry.
- **Sprint 4: UI Dashboarding & Analytics**
  - Finalize Next.js UI integration using Server Components, style efficiently with Tailwind, and deploy the Hot Path real-time analytics dashboard.
- **Sprint 5: Production Scale & GPU Optimization**
  - Profile FastAPI DB access for N+1 queries, integrate TensorRT/vLLM for GPU performance tuning, and conduct full regression checks via `./scripts/dev-verify.sh`.
