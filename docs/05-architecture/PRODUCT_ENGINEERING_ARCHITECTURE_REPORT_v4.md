# Product Engineering Architecture Report v4

## Problem Analysis

PedagogyX is scaling its multimodal AI classroom intelligence platform to analyze complex classroom sessions involving voice, video, slides, and student engagement data to measure pedagogical efficiency. As the platform transitions to production readiness, critical product engineering challenges must be addressed. Our primary v1 client relies on Meta Ray-Ban glasses capturing real-time classroom telemetry via `clients/android-capture-dat`. Since production school data is blocked pending G2 (India legal sign-off), the system must be highly robust, simulator-tested, and secure by default to ensure a smooth transition once data unblocks. The core engineering problem is orchestrating a hybrid AI processing pipeline—balancing a real-time Hot Path for immediate feedback (e.g., YOLO) with a batch Cold Path for intensive offline processing (e.g., faster-whisper, Ollama) on a central OSS inference backend, without sacrificing maintainability, reliability, or developer experience.

## Architecture Design

PedagogyX embraces a distributed, event-driven microservices architecture optimized for scalability, product quality, and long-term sustainability. The core microservices (`api`, `web`, `worker-asr`, `worker-cv`, `worker-metrics`) interact asynchronously to decoupled AI inference paths.

- **Web Tier (`web`)**: Next.js and React frontend offering educators and administrators actionable insights via interactive dashboards and pedagogical efficiency metrics.
- **API Gateway (`api`)**: FastAPI backend serving as the central orchestration layer, enforcing type safety and business rules.
- **AI Inference Backend**:
  - **Hot Path**: Real-time synchronous endpoints (powered by YOLO and lightweight models) designed for sub-second latency to capture immediate engagement vectors.
  - **Cold Path**: Asynchronous batch workers (`worker-asr`, `worker-cv`, `worker-metrics`) running on an OSS offline inference infrastructure leveraging faster-whisper and Ollama.
- **Data Flow**: The Android capture client streams multi-modal payloads to the FastAPI ingestion endpoints, which triage data into hot/cold queues via a scalable message broker, ensuring fault-tolerant delivery to the respective worker pools.

## Implementation Strategy

The execution of the architecture will follow an iterative, product-focused strategy prioritizing simplicity and extensibility.

1. **Phase 1: API and Client Integration Hardening**: Standardize ingestion payloads from `clients/android-capture-dat`. Establish strict validation models in FastAPI to ensure incoming streams meet pedagogical data schemas.
2. **Phase 2: Hybrid Pipeline Orchestration**: Decouple the real-time Hot Path from the batch Cold Path. Implement a scalable message queueing system (e.g., Redis/RabbitMQ) to buffer heavy video and audio streams for offline processing by `worker-cv` and `worker-asr`.
3. **Phase 3: Worker Node Autoscaling**: Develop infrastructure-as-code patterns to spin up batch Cold Path workers dynamically based on queue depth, ensuring performance is maintained during peak classroom hours.
4. **Phase 4: Dashboard Aggregation**: Surface pedagogical metrics in the Next.js `web` client, providing a seamless user experience that clearly differentiates real-time insights from deep, offline analytical metrics.

## Code Quality Strategy

To maintain the highest levels of developer experience and maintainability, strict automated quality gates are enforced across the monorepo.

- **Backend (Python/FastAPI)**: Enforce strict type checking using `mypy`. Linting and formatting are mandated via `ruff` and `black` to ensure consistent, readable code.
- **Frontend (TypeScript/React/Next.js)**: Enforce strict TypeScript compilation. Utilize Prettier and ESLint for styling and code consistency.
- **Testing**: Comprehensive coverage utilizing `pytest` for unit and integration testing of the API and workers. Frontend state logic and UI components will be validated using Jest and Playwright. Continuous integration hooks will reject any PR not meeting the defined coverage thresholds.

## Performance Optimization

To deliver an exceptional user experience and optimize computational resources, performance tuning will focus on both the application tier and the AI inference boundaries.

- **Hot Path Tuning**: The real-time AI endpoints must leverage optimized tensor inference (e.g., TensorRT, ONNX) to ensure the YOLO models execute within strict millisecond latency budgets.
- **Cold Path Throughput**: The OSS backend processing faster-whisper and Ollama will implement smart batching and hardware-accelerated processing queues, reducing idle GPU time and maximizing throughput.
- **API and Frontend**: FastAPI will utilize asynchronous non-blocking I/O extensively. The Next.js frontend will leverage static generation and incremental static regeneration (ISR) where appropriate to minimize Time to First Byte (TTFB) and improve client-side rendering speed.

## Security Considerations

Security is paramount, especially given the sensitive nature of classroom recordings and the pending G2 legal sign-off.

- **Data Privacy**: Ensure that all incoming payload data from the Meta Ray-Ban client is strictly pseudo-anonymized before storage or processing.
- **Authentication & Authorization**: The API must enforce zero-trust access control. Implement strict OAuth2/JWT flows with granular scope controls for different user roles (teachers, admins, researchers).
- **Network Boundaries**: Service-to-service communication between the API, web, and workers must be authenticated. The central OSS offline inference backend will be isolated within a secure VPC with restricted ingress/egress.

## Observability

Comprehensive observability ensures operational resilience and aids rapid debugging.

- **Distributed Tracing**: Implement OpenTelemetry across the `api`, `web`, and all `worker-*` services to trace requests as they traverse from the Android client through the hot and cold inference paths.
- **Metrics**: Expose Prometheus endpoints across all services to monitor GPU utilization, queue latencies, inference times, and worker saturation.
- **Logging**: Centralized, structured JSON logging will aggregate application events, capturing vital context without logging sensitive PII, facilitating proactive alerting.

## Refactoring Opportunities

As the system evolves from an initial MVP towards a robust enterprise architecture, several areas require refactoring for long-term sustainability:

- **Unified Messaging Interface**: Current inter-service communication patterns show signs of tight coupling. We will refactor workers to subscribe to a unified event bus, abstracting away the specific queue implementation.
- **API Route Modularization**: As pedagogical features expand, the core FastAPI routing structure will be decomposed into bounded domains (e.g., `/api/v1/ingest`, `/api/v1/metrics`, `/api/v1/insights`) to preserve simplicity.
- **Frontend Component Reusability**: Extract common visualization patterns (e.g., metric cards, engagement timeline graphs) in the React frontend into a strictly defined, reusable design system library.

## Risks & Tradeoffs

- **Real-time vs Accuracy Tradeoff**: The YOLO-based Hot Path prioritizes speed over comprehensive analysis. There is a risk of contradicting metrics between real-time feedback and the deeper insights generated by the Cold Path. This must be managed via UI UX messaging.
- **OSS Infrastructure Complexity**: Managing self-hosted models like Ollama and faster-whisper in the Cold Path introduces significant DevOps and scaling complexity compared to managed SaaS APIs, trading developer time for data privacy and cost-control.
- **Regulatory Blocking**: The G2 legal hold prevents testing with real-world production data. We risk overfitting our models and architectural choices to synthetic or internal testing data.

## Agile Sprint Plan

- **Sprint 1: Pipeline Decoupling & Ingestion**: Solidify the `api` ingestion points for the `android-capture-dat` client. Implement the initial RabbitMQ/Redis event bus separating the hot and cold paths.
- **Sprint 2: Worker Isolation**: Refactor `worker-cv`, `worker-asr`, and `worker-metrics` to consume from the new event bus. Implement foundational telemetry and logging across these nodes.
- **Sprint 3: AI Backend Integration**: Connect the centralized OSS inference backend (Ollama, faster-whisper) securely to the cold path workers. Implement basic queue autoscaling policies.
- **Sprint 4: Product Dashboard & Metrics**: Finalize the Next.js `web` dashboard to display real-time Hot Path data alongside historical Cold Path metrics. Conduct end-to-end simulator testing to validate data flow.
