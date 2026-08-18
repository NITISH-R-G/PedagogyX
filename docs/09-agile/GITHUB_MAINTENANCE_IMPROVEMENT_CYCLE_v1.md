# GitHub Maintenance & Improvement Cycle v1

**Date:** 2026-05-25
**Author:** Autonomous GitHub Repository Maintenance & Improvement System
**Cycle:** Sprint 04 (Foundational MVP Setup)
**Status:** DRAFT

## 1. Repository Health Report

Currently, the repository contains Phase 0 documentation and a basic MVP boilerplate (`services/`, `infra/`, `tools/`). Real implementation is blocked by G2 (India legal sign-off). The current focus is restricted to docs, benchmarks, the boilerplate dev stack, and synthetic test sessions.

**Key Issues Identified:**

- Significant documentation generation requires rigorous linting and formatting validation before CI merges.
- The pivot to Meta Ray-Ban (ADR-0009) requires establishing the initial contracts and schemas for the DAT application to communicate with the cloud backend.

## 2. Competitor Analysis

Competitors (Edthena, Vosaic, IRIS Connect) largely rely on high-bandwidth, post-hoc upload architectures or expensive, proprietary hardware. PedagogyX's advantage relies entirely on building a robust, low-latency streaming pipeline from the DAT edge device to the constrained (RTX 5070) cloud. This sprint focuses on the foundations of that pipeline.

## 3. Priority Improvements

Following the "Implementation Rules" (Observability first, infra first, contracts first, schemas first):

1.  **Define Core API Contracts:** Establish OpenAPI schemas for the initial DAT-to-Cloud ingestion endpoints (ignoring full implementation until G2 clearance).
2.  **Establish MVP Observability:** Integrate basic logging and metrics capture into the FastAPI boilerplate.
3.  **Harden CI Pipelines:** Ensure formatting and linting (markdownlint, prettier, ruff) are strictly enforced in the GitHub Actions workflows.

## 4. Sprint Plan (Sprint 04 - Foundations)

### Epic 1: Cloud Ingestion Contracts

- **Story 1.1:** Define OpenAPI schema for DAT authentication (`/auth/device`).
- **Story 1.2:** Define payload schema for synchronous AV buffer chunk ingestion (`/ingest/stream`).

### Epic 2: MVP Observability Setup

- **Story 2.1:** Configure structured JSON logging in the `services/api` FastAPI application.
- **Story 2.2:** Add a basic health-check endpoint (`/health`) returning dependency status (Postgres, Redis/Kafka).

### Epic 3: CI/CD Hardening

- **Story 3.1:** Verify and harden `.github/workflows/dev-verify.yml` to enforce `npx markdownlint-cli` and `npx prettier` on all `docs/**/*.md` PRs.
- **Story 3.2:** Ensure `ruff check` and `black` run successfully on all `services/` code.

## 5. Technical Improvements

- **Schema First Development:** By defining the OpenAPI contracts now, the mobile team (DAT app) can begin synthetic mocking while the backend team waits for legal clearance on real data.
- **Standardized Logging:** Structured JSON logging will immediately improve debuggability once synthetic streams are pushed through the system.

## 6. Metrics Improved

- **Developer Experience (DX):** Clear API contracts reduce friction between edge and cloud development.
- **Reliability:** Enforced CI checks prevent malformed documentation and unlinted code from breaking the `main` branch.
