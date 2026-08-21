# Tech Stack Evaluation Report

## Overview

This document evaluates the chosen technology stack for PedagogyX, justifying the selections based on project constraints (e.g., hybrid edge/cloud, OSS first, 12GB VRAM limits) and current repository implementations.

## Document History

- **Version:** v1.0
- **Author:** Autonomous Principal Research Architect
- **Date:** 2026-05-24

## 1. Backend API & Workers

### 1.1 Selection: Python & FastAPI

- **Evidence:** `services/api/requirements.txt` includes `fastapi`, `uvicorn`, `pydantic`.
- **Justification:** Python is the undisputed lingua franca of AI/ML. Using FastAPI for the API gateway ensures seamless integration with PyTorch/ONNX models in the worker services without complex IPC (Inter-Process Communication) overhead across different languages. FastAPI's async capabilities handle concurrent IO bound tasks (like receiving streams) efficiently.
- **Tradeoffs:** Python's Global Interpreter Lock (GIL) limits true multicore CPU concurrency. We mitigate this by utilizing an asynchronous event-driven architecture and scaling workers horizontally.

## 2. Frontend Dashboard

### 2.1 Selection: Next.js & React

- **Evidence:** `services/web/package.json` includes `next`, `react`, `tailwindcss`.
- **Justification:** Next.js provides robust server-side rendering (SSR) and API routes, ideal for building secure admin dashboards that consume the PedagogyX backend. TailwindCSS allows for rapid, consistent UI development.
- **Tradeoffs:** Adds a Node.js ecosystem dependency alongside Python. However, for complex UIs, the React ecosystem is significantly more mature than Python-based alternatives (like Streamlit) for enterprise SaaS.

## 3. Database & Message Broker

### 3.1 Selection: PostgreSQL & Redis

- **Evidence:** `services/api/requirements.txt` includes `psycopg2-binary` and `redis`.
- **Justification:**
  - **PostgreSQL:** A rock-solid relational database essential for managing RBAC, teacher profiles, and longitudinal pedagogical scores.
  - **Redis:** Serves dual purpose as a fast cache and a message broker (via Redis Streams) for coordinating tasks between the API and `worker-*` services.
- **Tradeoffs:** Managing relational migrations and state requires discipline. Redis adds an in-memory component that must be monitored for OOM (Out of Memory) issues under heavy load.

## 4. AI & Machine Learning Infrastructure

### 4.1 Selection: OSS Models (e.g., Qwen2.5-7B-Q4) & ONNX/TensorRT

- **Evidence:** Founder requirement (D-OSS) and hardware limit (D-GPU: RTX 5070 12GB).
- **Justification:** To comply with the strict 12GB VRAM limit on the edge, massive foundational models are excluded. Heavily quantized OSS models (like Qwen2.5-7B in Q4) offer the best tradeoff between pedagogical reasoning capabilities and memory footprint.
- **Tradeoffs:** Quantization can slightly degrade reasoning quality compared to unquantized FP16/FP32 models. Continuous evaluation pipelines (evals) must be built to ensure pedagogical scoring remains accurate and unbiased.

## 5. Conclusion

The current stack (FastAPI, Next.js, Postgres, Redis, Quantized OSS AI) is highly pragmatic for the constraints of PedagogyX. It prioritizes ML integration and rapid iteration while acknowledging the strict hardware and budgetary limits of the Year 1 India pilot.

EOF
