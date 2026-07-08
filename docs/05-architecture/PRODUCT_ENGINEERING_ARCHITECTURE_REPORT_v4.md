# Autonomous Senior Software Engineer & Product Engineering Architect Report v4

## Problem Analysis

PedagogyX is a multimodal AI classroom intelligence platform designed to analyze classroom sessions (voice, video, slides, student engagement) and measure pedagogical efficiency. Our primary challenges revolve around scaling our real-time Hot Path (YOLO, quick inference) and batch Cold Path (faster-whisper, Ollama) while maintaining exceptional product quality. We need to process high-throughput multimodal data streams from our primary v1 client (Meta Ray-Ban via `clients/android-capture-dat`) efficiently.

Key constraints and considerations:

- Real-time ingestion and processing of multimodal streams from mobile clients.
- Handling long-running asynchronous batch tasks for deep AI analysis.
- Storage and aggregation of classroom metrics for pedagogical insights.
- The system must adhere to G2 (India legal sign-off) compliance, blocking production school data until approval.
- High demands on system scalability, reliability, and maintainability across a diverse tech stack (FastAPI, React, Next.js).

## Architecture Design

The architecture is composed of distinct microservices facilitating separation of concerns, scalability, and independent deployment:

- **Frontend Application (`services/web`)**: Built with React and Next.js, serving as the primary interface for educators and administrators to view classroom intelligence metrics and insights.
- **API Gateway & Core Service (`services/api`)**: A FastAPI-based service orchestrating requests, routing data to respective workers, and managing business logic.
- **Computer Vision Worker (`services/worker-cv`)**: Handles real-time "Hot Path" inference (e.g., YOLO) for student engagement and classroom dynamics.
- **Audio/Speech Worker (`services/worker-asr`)**: Manages the "Cold Path" batch processing (e.g., faster-whisper) for transcribing and analyzing voice data.
- **Metrics Worker (`services/worker-metrics`)**: Aggregates processed outputs to compute final pedagogical efficiency metrics.
- **Central OSS Offline Inference Backend**: Powers both Hot and Cold paths securely and cost-effectively.

Data flows from the client to the API gateway, which places tasks into message queues for the respective worker microservices. Results are stored in the core database and served via the Next.js frontend.

## Implementation Strategy

1. **Phase 1: API Gateway & Core Routes**
   - Solidify the FastAPI endpoints in `services/api` for robust ingestion.
   - Implement asynchronous task delegation to workers using a reliable message broker (e.g., Redis/RabbitMQ).
2. **Phase 2: Worker Isolation & Optimization**
   - Ensure `worker-cv` is optimized for GPU utilization for real-time inference.
   - Refine `worker-asr` batch processing to efficiently handle large classroom audio files.
3. **Phase 3: Frontend Integration**
   - Consume aggregated APIs in the Next.js `services/web` app.
   - Implement real-time WebSocket connections for live session monitoring if necessary.
4. **Phase 4: Compliance & Data Flow**
   - Enforce data gating logic to block production school data routing until G2 sign-off.

## Code Quality Strategy

- **Linting & Formatting**: Enforce Python linting across microservices using `ruff check services/`. Use Prettier and Markdownlint for frontend and documentation.
- **Testing**:
  - API endpoints must be validated using `pytest` (e.g., `cd services/api && pytest tests/`).
  - Strict typed inputs and outputs for FastAPI using Pydantic models.
  - Implement CI-friendly testing for all services.
- **Quality Gates**: No hardcoded status codes; use `fastapi.status` constants (e.g., `status.HTTP_404_NOT_FOUND`) to comply with SonarCloud requirements.
- **CI Validation**: Ensure all documentation conforms to standards using `./scripts/dev-verify.sh --docs-only`.

## Performance Optimization

- **Hot Path Efficiency**: Optimize YOLO models in `worker-cv` for lower latency. Utilize TensorRT or ONNX Runtime for inference acceleration.
- **Cold Path Throughput**: Scale `worker-asr` horizontally to process multiple classroom sessions concurrently.
- **Database Indexing**: Ensure all metric queries in the core database have appropriate indexes to support rapid Next.js dashboard loading.
- **Caching**: Implement Redis caching at the API layer for frequently accessed, computationally expensive pedagogical insights.

## Security Considerations

- **Data Privacy**: Strictly enforce the block on production school data prior to G2 sign-off. Mask or drop PII during pre-production testing.
- **Authentication/Authorization**: Secure all APIs accessed by the Meta Ray-Ban client using robust token-based authentication (e.g., OAuth2/JWT).
- **Service Isolation**: Ensure workers operate in isolated network segments and can only communicate with the central message broker and designated databases.
- **Input Validation**: Use FastAPI's built-in validation via Pydantic to sanitize and validate all multimodal inputs.

## Observability

- **Centralized Logging**: Stream logs from all microservices (`api`, `worker-cv`, `worker-asr`, `worker-metrics`, `web`) to a centralized logging platform.
- **Distributed Tracing**: Implement OpenTelemetry to trace requests from the Meta Ray-Ban client through the API, into the message broker, and out from the workers.
- **Metrics Dashboard**: Expose Prometheus metrics from FastAPI and workers (e.g., inference latency, queue length, request rate) and visualize them in Grafana.
- **Alerting**: Set up alerts for critical thresholds, such as high Hot Path latency or failing Cold Path batch jobs.

## Refactoring Opportunities

- **Shared Core Libraries**: Extract common utility functions, database models, and Pydantic schemas shared across `api` and `worker-*` services into an internal shared package.
- **Asynchronous Task Management**: Review the current message queue implementation for robustness; refactor tightly coupled worker invocations into an event-driven architecture.
- **Frontend State Management**: Audit the Next.js application for overly complex state logic and refactor into clean, decoupled React hooks or lightweight state libraries.

## Risks & Tradeoffs

- **System Complexity vs. Microservice Autonomy**: The multi-worker architecture introduces operational complexity. Tradeoff: We gain scalability and fault isolation at the cost of deployment and tracing overhead.
- **Cost vs. Latency (Inference)**: Running dedicated GPUs for the Hot Path ensures low latency but incurs high costs. We must constantly monitor utilization.
- **Compliance Blocking**: Blocking production data for G2 sign-off may delay testing against real-world distributions. Tradeoff: Legal compliance is strictly prioritized over immediate data availability.

## Agile Sprint Plan

- **Sprint 1 (Architecture Refinement)**: Finalize API boundaries, set up shared schemas, and enforce `fastapi.status` code standards across the API.
- **Sprint 2 (Worker Optimization)**: Implement basic observability (logging, metrics) in `worker-cv` and `worker-asr`. Optimize basic Cold Path throughput.
- **Sprint 3 (Frontend Connectivity)**: Wire the Next.js `web` service to the aggregated metrics API. Implement UI for displaying pedagogical efficiency.
- **Sprint 4 (Security & Compliance Review)**: Audit the system for data masking, enforce the G2 data block, and perform an end-to-end load test using synthetic Ray-Ban client data.
