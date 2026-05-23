# Full Stack Architecture Report

**Status:** Draft v1.0
**Date:** 2026-05-20
**Role:** Autonomous Senior Full Stack Developer

## 1. Product & Problem Analysis

PedagogyX must seamlessly integrate hardware capture at the edge (Android/Windows), a high-throughput ML backend, and a real-time web frontend for administrators. The core problem for a Full Stack engineer is maintaining strict typing and smooth data flow across these highly disparate environments while adhering to strict privacy laws (DPDP) and low hardware budgets.

## 2. Full Stack Architecture

We utilize a decoupled, asynchronous architecture.

- **Edge Capture:** Tauri (Windows) / Kotlin (Android) -> MediaMTX -> MinIO.
- **Backend:** Python FastAPI handles the control plane; Celery coordinates ML workers on bare-metal GPUs.
- **Frontend:** Next.js serves the dashboards.
- **Data Backbone:** PostgreSQL for state, ClickHouse for analytics.

## 3. Frontend Strategy

- **Framework:** Next.js (React) for the web portal.
- **State Management:** React Query for server state; Zustand for complex local state (like the video scrubber timeline).
- **Styling:** Tailwind CSS + shadcn/ui for rapid, accessible component development.

## 4. Backend Strategy

- **Framework:** FastAPI (Python) chosen specifically to bridge the gap between traditional REST APIs and the PyTorch/ML ecosystem without requiring heavy RPC layers.
- **Async Processing:** Crucial. Video upload and ML inference are entirely non-blocking, managed via Celery and RabbitMQ/Redis.

## 5. Database Design

- **PostgreSQL:** Handles strongly-typed relational data (Users, Tenants, Roles).
- **ClickHouse:** Handles high-velocity telemetry (time-series analytics, engagement scores).
- **MinIO:** Object storage for the raw media and the final JSON inference artifacts.

## 6. Security Strategy

- **Auth:** JWT-based authentication via a standard OIDC provider.
- **CORS & CSRF:** Strict CORS policies on the FastAPI backend, restricting access to the deployed Next.js domain.
- **Data Segregation:** Tenant ID is injected into every JWT. The backend enforces Row-Level Security (RLS) in Postgres based on this Tenant ID.

## 7. DevOps & Deployment

- **Containerization:** Everything (FastAPI, Next.js, Celery workers) is containerized via Docker.
- **Local Dev:** `compose.dev.yaml` orchestrates the entire stack (minus heavy GPUs) for local development.
- **Production:** Deployed via Docker Swarm across AWS and the bare-metal GPU pool.

## 8. Testing Strategy

- **Unit Tests:** `pytest` for Python backend; `vitest` for React frontend.
- **Integration Tests:** API contract testing ensures the Next.js frontend and FastAPI backend agree on the Pydantic schemas.
- **E2E Tests:** Playwright simulates a teacher uploading a session and an admin reviewing the analytics.

## 9. Refactoring Opportunities

- _Current State:_ Being in Phase 0, we must establish strict API contracts (OpenAPI/Swagger) immediately before the frontend and backend teams diverge, preventing "integration hell" later.

## 10. Risks & Tradeoffs

- **Risk:** Maintaining types across Python (Pydantic) and TypeScript (React). **Tradeoff:** We will utilize OpenAPI generators to automatically build TypeScript types from the FastAPI backend, adding a build step but preventing massive runtime bugs.
- **Risk:** WebSocket scaling for the live admin dashboard. **Tradeoff:** We will rely on simple polling for the MVP, moving to WebSockets/Server-Sent Events (SSE) only when latency requirements demand it, to reduce infrastructure complexity.

## 11. Agile Sprint Plan

- **Sprint 1:** Scaffold Next.js frontend and FastAPI backend. Define the OpenAPI contract for the core `Session` object.
- **Sprint 2:** Implement the end-to-end file upload flow: React Dropzone -> FastAPI -> MinIO.
- **Sprint 3:** Build the Video Scrubber component in React and link it to a mock JSON ML artifact served by FastAPI.
