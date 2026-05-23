# Exhaustive Tech Stack Analysis

**Status:** Draft v1.0
**Date:** 2026-05-20
**Owner:** Architecture Team

This document provides a comprehensive analysis of technology choices across all layers of the PedagogyX platform, resulting in our definitive stack recommendations.

## 1. Backend Languages & Frameworks

| Language / Framework   | Latency       | Concurrency                | ML Integration                                     | Infra Cost | Maintainability               | Verdict                                                                                   |
| :--------------------- | :------------ | :------------------------- | :------------------------------------------------- | :--------- | :---------------------------- | :---------------------------------------------------------------------------------------- |
| **Go**                 | Extremely Low | Excellent (Goroutines)     | Poor (Requires CGO/bindings)                       | Very Low   | High                          | **Rejected** (Lack of native ML ecosystem).                                               |
| **Rust**               | Lowest        | Excellent                  | Maturing (Candle, tch-rs)                          | Lowest     | Medium (Steep learning curve) | **Rejected** (Too slow to iterate for MVP, though ideal for future edge agent).           |
| **Python (FastAPI)**   | High (GIL)    | Moderate (Asyncio/Uvicorn) | **Best in Class** (Native to PyTorch/Transformers) | Medium     | High                          | **SELECTED** (Standard for ML APIs; required for interfacing with our inference workers). |
| **Node.js (NestJS)**   | Low           | High (Event Loop)          | Poor                                               | Low        | High                          | **Rejected** (Unnecessary bridging required to ML pipelines).                             |
| **Java (Spring Boot)** | Medium        | High                       | Poor                                               | High       | High                          | **Rejected** (Overkill, poor ML alignment).                                               |

## 2. AI/ML Inference Frameworks

| Framework            | GPU Efficiency | Portability       | Edge Deployment | Optimization Features | Verdict                                                                   |
| :------------------- | :------------- | :---------------- | :-------------- | :-------------------- | :------------------------------------------------------------------------ |
| **PyTorch (Native)** | Medium         | High              | Medium          | Medium                | **Rejected** (Too slow for production batch processing on RTX 5070).      |
| **TensorFlow**       | Medium         | Medium            | High (TFLite)   | Medium                | **Rejected** (Declining ecosystem momentum compared to PyTorch).          |
| **JAX**              | High           | Low               | Low             | High (XLA)            | **Rejected** (Overhead not justified for our specific model stack).       |
| **ONNX Runtime**     | High           | **Highest**       | High            | High                  | **SELECTED** (For Edge CV models and CPU fallbacks).                      |
| **TensorRT / vLLM**  | **Highest**    | Low (NVIDIA only) | Low             | **Highest**           | **SELECTED** (vLLM for Qwen2.5; TensorRT for YOLO/Whisper on cloud GPUs). |

## 3. Video Pipelines & Streaming

| Technology              | Real-time Latency   | Complexity | Browser Support | Use Case Fit           | Verdict                                                                                 |
| :---------------------- | :------------------ | :--------- | :-------------- | :--------------------- | :-------------------------------------------------------------------------------------- |
| **FFmpeg (CLI/Lib)**    | High                | Medium     | N/A             | Batch transcoding      | **SELECTED** (For Cold Path segmenting and transcoding).                                |
| **GStreamer**           | Low                 | Very High  | N/A             | Complex edge pipelines | **Rejected** (Overkill for our simple capture needs).                                   |
| **WebRTC**              | **Lowest (<500ms)** | High       | Universal       | Live streaming         | **SELECTED** (For Hot Path / Live Admin Dashboard).                                     |
| **MediaMTX (RTSP/HLS)** | Low (~2s)           | Low        | Broad (via HLS) | Ingest & Distribution  | **SELECTED** (Core streaming server for Edge-to-Cloud ingest).                          |
| **NVIDIA DeepStream**   | Lowest              | High       | N/A             | High-density CV        | **Rejected** (Locks us into NVIDIA at the edge; violates hardware-agnostic constraint). |

## 4. Databases & Storage

| Type                   | Technology     | Scalability | ML Integration      | Strengths              | Verdict                                                               |
| :--------------------- | :------------- | :---------- | :------------------ | :--------------------- | :-------------------------------------------------------------------- |
| **Relational / Core**  | **Postgres**   | High        | Vector via pgvector | ACID, ubiquitous       | **SELECTED** (Primary OLTP store).                                    |
| **OLAP / Time-Series** | **ClickHouse** | **Highest** | Medium              | Real-time analytics    | **SELECTED** (For aggregating millions of inferred telemetry events). |
| **NoSQL**              | **MongoDB**    | High        | Low                 | Flexible schema        | **Rejected** (We need strict schemas for ML pipelines).               |
| **Vector DB**          | **Qdrant**     | High        | Native              | Rust-based, fast       | **SELECTED** (For RAG and semantic lesson search).                    |
| **Vector DB**          | **Milvus**     | Very High   | Native              | Massive scale          | **Rejected** (Overly complex infrastructure requirements for MVP).    |
| **Graph DB**           | **Neo4j**      | Medium      | Medium              | Interaction graphs     | **Rejected** (Defer to Phase 2; Postgres CTEs suffice for now).       |
| **Object Storage**     | **MinIO**      | High        | High                | S3-compatible, on-prem | **SELECTED** (For hybrid-edge buffering and cloud video archive).     |

## 5. Frontend & Client

| Framework       | Paradigm         | Performance      | Ecosystem  | Verdict                                                           |
| :-------------- | :--------------- | :--------------- | :--------- | :---------------------------------------------------------------- |
| **React (SPA)** | Client-side      | Medium           | Massive    | **Rejected** (SEO/initial load issues, complex state management). |
| **Next.js**     | Full-stack (SSR) | High             | Massive    | **SELECTED** (For web portals, SEO, and robust API routes).       |
| **Flutter**     | Cross-platform   | High             | Medium     | **Rejected** (Non-native feel on web, though good for mobile).    |
| **Electron**    | Desktop App      | Low (Heavy)      | High       | **Rejected** (Violates low-end client constraint).                |
| **Tauri**       | Desktop App      | **High (Light)** | Rust-based | **SELECTED** (For Windows smartboard capture agent).              |

## 6. Infrastructure & Orchestration

| Platform         | Complexity  | Scalability | Cost Efficiency          | Verdict                                                                              |
| :--------------- | :---------- | :---------- | :----------------------- | :----------------------------------------------------------------------------------- |
| **Kubernetes**   | **Highest** | **Highest** | Low (High overhead)      | **Rejected** (Too complex for the initial 50-school pilot; high control-plane cost). |
| **Nomad**        | Medium      | High        | High                     | **Rejected** (Good, but smaller ecosystem than Docker Swarm/K8s).                    |
| **Docker Swarm** | Low         | Medium      | High                     | **SELECTED** (Simple multi-node orchestration, fits our bare-metal GPU strategy).    |
| **Serverless**   | Low         | High        | Low (Expensive at scale) | **Rejected** (Cannot handle long-running video workloads cost-effectively).          |

## 7. Cloud vs. Bare-Metal

| Provider                                               | Global Reach | GPU Availability           | Cost per Compute | Verdict                                                                     |
| :----------------------------------------------------- | :----------- | :------------------------- | :--------------- | :-------------------------------------------------------------------------- |
| **AWS (ap-south-1)**                                   | High         | Medium (Expensive)         | High             | **SELECTED** (For Control Plane, Postgres, Web frontend).                   |
| **GCP / Azure**                                        | High         | Medium                     | High             | **Rejected** (No specific advantage over AWS for our stack).                |
| **Bare-Metal GPU Rentals (e.g., RunPod, Lambda Labs)** | Low          | High (RTX 5070s available) | **Lowest**       | **SELECTED** (For heavy ML batch workers to meet the ₹0 budget constraint). |

## Summary of Chosen Stack

- **Backend:** Python (FastAPI) + Celery workers
- **Frontend:** Next.js (Web), Tauri (Windows Agent), Kotlin (Android App)
- **Databases:** Postgres (OLTP), ClickHouse (Analytics), Qdrant (Vector)
- **Storage:** MinIO (S3-compatible)
- **Video/Streaming:** MediaMTX + WebRTC + FFmpeg
- **AI/ML Pipeline:** TensorRT (CV), faster-whisper (Audio), vLLM (Ollama/Qwen2.5)
- **Infrastructure:** AWS (Control Plane) + Bare-Metal GPU pool, orchestrated via Docker Compose/Swarm.
