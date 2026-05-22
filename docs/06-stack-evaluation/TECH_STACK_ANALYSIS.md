# Tech Stack Exhaustive Analysis

**Status:** Draft v0.1
**Date:** 2026-05-20
**Owner:** Architecture Team

## Overview

This document evaluates the options for PedagogyX's tech stack, aligning with the founder's constraints (ADR-0005: FOSS-first, D-10: ₹0 customer budget, RTX 5070 sizing).

---

## 1. Backend Languages

| Language    | Strengths                                                                   | Weaknesses                                                   | Decision                           |
| :---------- | :-------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------- |
| **Go**      | High concurrency, excellent for networking/streaming, low memory footprint. | Weak ML ecosystem, harder for data scientists to contribute. | **Primary API & Ingest.**          |
| **Python**  | Unmatched ML/AI ecosystem (PyTorch, Pandas).                                | GIL limits concurrency, higher latency.                      | **ML Worker Daemons.**             |
| **Rust**    | Memory safety, C-level performance.                                         | Steep learning curve, slower development velocity.           | Rejected for v1 (too slow to MVP). |
| **Node.js** | Easy full-stack sharing with frontend.                                      | Poor for heavy compute and multi-threading.                  | Rejected for backend.              |

**Strategy:** Polyglot. Go for the API gateway and WebRTC signaling; Python for the ML worker queues.

---

## 2. AI / ML Frameworks

| Framework    | Strengths                                              | Weaknesses                                              | Decision                     |
| :----------- | :----------------------------------------------------- | :------------------------------------------------------ | :--------------------------- |
| **PyTorch**  | Industry standard for research, native Python support. | Can be heavy for inference if unoptimized.              | Base model training/dev.     |
| **TensorRT** | Maximizes NVIDIA GPU throughput, lowest latency.       | Tied to NVIDIA hardware, export process can be complex. | **Chosen for CV Inference.** |
| **ONNX**     | Hardware agnostic.                                     | Sometimes lags behind PyTorch feature support.          | Fallback for CPU inference.  |

**Strategy:** Export YOLO to TensorRT for the RTX 5070 cloud workers to maximize the ₹0 budget capacity.

---

## 3. Video Pipelines

| Tool          | Strengths                                          | Weaknesses                                                | Decision                        |
| :------------ | :------------------------------------------------- | :-------------------------------------------------------- | :------------------------------ |
| **WebRTC**    | Sub-second latency, perfect for hot path.          | Complex state management, strict networking requirements. | **Hot Path / Live Preview.**    |
| **FFmpeg**    | Swiss army knife of video processing, ubiquitous.  | CLI based, can be slow for massive parallel real-time.    | **Cold Path chunk processing.** |
| **GStreamer** | High performance pipeline definition.              | Extremely steep learning curve.                           | Rejected (overkill).            |
| **MediaMTX**  | Zero-dependency WebRTC/RTSP server, written in Go. | Smaller community than Janus/Pion.                        | **Chosen as Ingest Hub.**       |

---

## 4. Databases

| DB             | Strengths                                         | Weaknesses                             | Decision                  |
| :------------- | :------------------------------------------------ | :------------------------------------- | :------------------------ |
| **PostgreSQL** | ACID compliant, pgvector handles RAG, ubiquitous. | Not a pure timeseries DB.              | **Primary Data Store.**   |
| **MinIO**      | S3 compatible, self-hostable, fast.               | Requires dedicated storage management. | **Video Blob Storage.**   |
| **ClickHouse** | Ultimate OLAP performance for analytics.          | Overkill for Phase 1 scale.            | Deferred to Phase 2.      |
| **Redis**      | In-memory speed, perfect for queues/pub-sub.      | Data volatility.                       | **Hot Path message bus.** |

---

## 5. Frontend

| Framework            | Strengths                                      | Weaknesses                                 | Decision                      |
| :------------------- | :--------------------------------------------- | :----------------------------------------- | :---------------------------- |
| **Next.js**          | React ecosystem, SSR, fast loading.            | Vercel lock-in if using advanced features. | **Admin Dashboard UI.**       |
| **Tauri**            | Tiny bundle sizes, Rust backend, web frontend. | Newer ecosystem for desktop apps.          | **Windows Smartboard Agent.** |
| **Kotlin (Compose)** | Native Android performance.                    | Requires Android devs.                     | **Android Agent.**            |

---

## 6. Infrastructure & Cloud

| Option                | Strengths                                          | Weaknesses                                              | Decision                       |
| :-------------------- | :------------------------------------------------- | :------------------------------------------------------ | :----------------------------- |
| **AWS (ap-south-1)**  | Unmatched reliability, complete ecosystem.         | High egress costs, expensive GPUs.                      | Rejected for GPU tier.         |
| **Self-Hosted / VPS** | Massive cost savings for 24/7 GPU workloads.       | You build your own VPC/security.                        | **Chosen for GPU Cloud Pool.** |
| **Kubernetes**        | Infinite scale, self-healing.                      | High operational complexity and base resource overhead. | Rejected for v1.               |
| **Docker Compose**    | Dead simple, perfect for single-node Edge and VPS. | Lacks multi-node orchestration.                         | **Chosen for v1 deploy.**      |

**Strategy:** Bare-metal VPS providers in India for cheap RTX 5070 equivalents managed via Ansible and Docker Compose.
