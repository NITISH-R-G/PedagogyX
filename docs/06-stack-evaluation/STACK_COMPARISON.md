# Stack Evaluation — Executive Summary

**Status:** Draft v0.1 | **Recommendation:** Hybrid (see bottom)

Scoring: 1 (poor) – 5 (excellent) for PedagogyX context

---

## Backend Languages

| Criterion | Go | Rust | Python | Node.js | Java |
|-----------|----|------|--------|---------|------|
| ML integration | 2 | 2 | **5** | 2 | 3 |
| Media/FFmpeg ops | 4 | **5** | 3 | 2 | 3 |
| API latency | **5** | **5** | 3 | 4 | 4 |
| Hiring pool | 4 | 3 | **5** | 5 | 4 |
| Concurrency | **5** | **5** | 3 | 4 | 4 |
| **PedagogyX fit** | Control plane | Transcode workers | ML + agents | Avoid core | Enterprise optional |

**Recommendation:** **Python** for ML plane; **Go** for API/ingest orchestration; **Rust** optional for transcode hot path at scale.

---

## ML Frameworks

| Framework | Training | Inference | Edge | Notes |
|-----------|----------|-----------|------|-------|
| **PyTorch** | **5** | 4 | 3 | Default research/training |
| TensorFlow | 3 | 4 | 4 | TFX production maturity |
| JAX | 4 | 3 | 2 | Research, TPU |
| ONNX | — | **5** | **5** | Exchange format |
| TensorRT | — | **5** | 4 | NVIDIA GPUs |

**Recommendation:** Train **PyTorch** → export **ONNX** → **TensorRT** on NVIDIA inference nodes.

---

## Video Pipelines

| Tech | Live stream | Batch transcode | Classroom fit |
|------|-------------|-----------------|---------------|
| **FFmpeg** | Via libav | **5** | Universal |
| GStreamer | **5** | 4 | Hardware integrators |
| WebRTC | **5** | 1 | Phase 3 live coaching |
| RTSP | 4 | 3 | Fixed cameras |
| DeepStream | 4 | 4 | Multi-cam edge |

**Recommendation:** **FFmpeg** batch MVP; **WebRTC** when IRIS-class live ships.

---

## Databases

| Store | Use case | Verdict |
|-------|----------|---------|
| **PostgreSQL** | Tenants, RBAC, lesson metadata | **Required** |
| **ClickHouse** | Time-series metrics, district rollups | **Recommended** |
| S3 | Raw media | **Required** |
| **Qdrant/Milvus** | Semantic search over lessons | Phase 2 |
| Neo4j | Interaction graphs | Phase 3 |
| MongoDB | Document blobs | Skip (Postgres JSONB) |
| Cassandra | Write-heavy events | Only if Kafka+CH insufficient |
| Weaviate | Managed vectors | Optional vs Qdrant |

---

## Frontend

| Option | Coach web | Mobile capture | Verdict |
|--------|-----------|----------------|---------|
| **Next.js (React)** | **5** | 3 (PWA) | Primary web |
| Flutter | 3 | **5** | Phase 2 native capture |
| Tauri | 4 | 2 | Desktop reviewer tool optional |
| Electron | 3 | 2 | Avoid |

---

## Infrastructure

| Option | PedagogyX MVP | Scale |
|--------|---------------|-------|
| **Kubernetes (EKS/GKE)** | Standard | GPU node pools |
| Nomad | Simpler ops | Less ML ecosystem examples |
| Serverless | Upload triggers | GPU limits |
| **Terraform** | IaC | Required |

---

## Cloud

| Provider | Pros | Cons |
|----------|------|------|
| **AWS** | Broad GPU, S3, Transcribe, Bedrock | Complex pricing |
| GCP | Video ML APIs | Smaller edu sales lore |
| Azure | Teams integration | Same |
| Self-hosted GPU | Cost at scale | Ops burden |

**Recommendation:** **AWS** primary **[ASSUMPTION]** for US K-12; EU region on AWS or GCP for GDPR.

---

## Reference Stack (MVP)

```
Next.js → Go API → Kafka → {Python GPU workers, FFmpeg CPU workers}
         ↓
    Postgres + S3 + ClickHouse
         ↓
    Private LLM or vLLM for coaching drafts
```

---

## Hiring Reality Check

**[FACT]** World-class classroom CV is **research-heavy**; team needs:

- 1–2 ML engineers (speech + optional CV)
- 1 backend (Go)
- 1 frontend
- 1 pedagogy/learning scientist
- 0.5 security/compliance
- Legal counsel on retainer

Before coding, confirm funding matches.
