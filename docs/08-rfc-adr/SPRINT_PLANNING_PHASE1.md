# Agile Sprint Planning: Phase 1 (Pre-Implementation)

**Date:** 2026-05-24
**Scope:** Establishing the foundational infrastructure and observability pipelines before core feature development begins.

## Epic 1: Local Infrastructure Setup (Sprint 1)

**Goal:** Establish a reproducible local development environment matching production topology.

- **Story 1.1:** Create `docker-compose.dev.yml` to orchestrate PostgreSQL, Redis, MinIO, and a mock Kafka instance.
- **Story 1.2:** Implement database migration scripts (Alembic) for core relational tables (Users, Schools, Sessions).
- **Story 1.3:** Configure FastAPI boilerplate with Pydantic schemas, typed APIs, and strict Mypy checking.
- **Story 1.4:** Setup basic API authentication (JWT) and role-based access control (RBAC) middleware for Admin vs. Teacher roles.

## Epic 2: Edge Upload Pipeline (Sprint 2)

**Goal:** Build a robust, fault-tolerant upload mechanism for the Android DAT host.

- **Story 2.1:** Design and implement a chunked upload API in FastAPI to handle large video files over unstable connections.
- **Story 2.2:** Integrate MinIO SDK in the backend to store raw chunks securely.
- **Story 2.3:** Create a Celery task to reassemble video chunks into complete lesson files once upload is complete.
- **Story 2.4:** Implement error handling and retry logic for incomplete uploads.

## Epic 3: AI Inference Scaffold (Sprint 3)

**Goal:** Create the pipeline architecture for "Cold Path" AI processing without committing to final models.

- **Story 3.1:** Set up a Celery worker dedicated to GPU tasks, isolating it from the main API service.
- **Story 3.2:** Implement a mock ASR (Speech-to-Text) function to simulate processing time and data flow.
- **Story 3.3:** Design the JSON schema for pedagogical output (e.g., Socratic ratio, speaking time).
- **Story 3.4:** Create a basic event publisher (Redis/Kafka) to notify the API service when an inference task completes.

## Epic 4: Observability & CI/CD (Continuous)

**Goal:** Ensure code quality and system transparency from day one.

- **Story 4.1:** Implement structured JSON logging (Loguru) across all backend services.
- **Story 4.2:** Set up GitHub Actions for automated linting (Black, Ruff, Mypy) on all pull requests.
- **Story 4.3:** Create a pre-commit hook configuration for local developer verification.
- **Story 4.4:** (Future) Integrate Prometheus metrics for API latency and Celery queue length.
