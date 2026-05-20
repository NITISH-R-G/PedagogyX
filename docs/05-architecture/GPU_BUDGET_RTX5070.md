# GPU Budget — RTX 5070 (12 GB) — **Development & Benchmarking Only**

> **Production** runs on **central servers**, not RTX 5070 in classrooms. Clients are low-end Android / Windows smartboards.

**ADR:** [ADR-0006](../08-rfc-adr/ADR-0006-rtx5070-compute-budget.md)

---

## Hardware facts

| Spec            | Value                                  |
| --------------- | -------------------------------------- |
| GPU             | GeForce RTX 5070                       |
| VRAM            | **12 GB** GDDR7                        |
| TDP             | ~250 W                                 |
| Inference stack | CUDA 12.x, TensorRT 10.x, ONNX Runtime |

---

## VRAM budget table (single job, exclusive GPU)

| Job        | Model                       | Quant           | Peak VRAM | Wall time (50 min lesson, est.) |
| ---------- | --------------------------- | --------------- | --------- | ------------------------------- |
| ASR        | faster-whisper **medium**   | INT8            | ~3 GB     | ~8–15 min                       |
| ASR        | faster-whisper **large-v3** | INT8            | ~5 GB     | ~15–25 min                      |
| CV batch   | YOLO11n TensorRT            | FP16            | ~2 GB     | ~5–10 min (1 cam 720p)          |
| CV batch   | 2 cams sequential           | FP16            | ~2 GB     | ~10–20 min                      |
| LLM report | Qwen2.5-7B                  | Q4_K_M (Ollama) | ~5–6 GB   | ~2–5 min                        |
| LLM report | Llama-3.2-3B                | Q4              | ~3 GB     | ~1–3 min                        |

**Total cold pipeline (medium ASR + 2 cam CV + 7B LLM):** ~35–50 min **sequential** per lesson on one GPU.

---

## Hot path (live) — feasible subset

```mermaid
flowchart TB
    subgraph gpu [RTX 5070 12GB]
        W[faster-whisper SMALL int8 ~1.5GB]
        Y[YOLO11n 480p cam1 ~1GB]
    end
    subgraph cpu [CPU]
        SCR[Screen frame diff]
        VAD[Silero VAD]
    end
    IN[Ingest] --> VAD --> W
    IN --> Y
    IN --> SCR
    W --> DASH[Live dashboard previews]
    Y --> DASH
```text

**Not on GPU live:** 2nd camera, large ASR, LLM, 1080p, screen OCR.

---

## Scheduling algorithm (edge worker)

```text
priority_queue:
  1. LIVE_AUDIO_METRICS     (preempt none; 2s cadence)
  2. LIVE_CAM1_DETECTION    (5 fps max)
  3. COLD_ASR               (when lesson ends)
  4. COLD_CV_CAMS           (sequential per stream)
  5. COLD_LLM               (last; needs full VRAM)
```text

If VRAM OOM: drop LIVE_CAM1 → audio-only live.

---

## Scaling without more GPUs

| Strategy                     | Tradeoff                             |
| ---------------------------- | ------------------------------------ |
| Audio-only live, video batch | Best fit for 12 GB                   |
| Night batch all video        | Admin sees final scores next morning |
| Lower resolution (480p)      | Accuracy loss                        |
| Nano models only             | Weaker engagement proxy              |
| More RTX 5070 nodes          | Linear scale; still OSS              |

---

## Founder alignment note

You asked for **real-time multi-cam**. On **one RTX 5070**, we implement:

- **Real-time:** audio talk ratio + optional **one** 480p cam
- **Multi-cam + screen:** **post-lesson batch** on same GPU
- **Admin authoritative score:** after cold queue completes

To get full real-time multi-cam, you need **more GPUs** or **cloud GPUs** (contradicts current constraint).

---

## Benchmark tasks (Sprint 01)

- [ ] `bench_whisper.py` — medium vs large-v3 INT8, RTF
- [ ] `bench_yolo_trt.py` — 480p vs 720p, 1 vs 2 streams
- [ ] `bench_ollama.py` — Qwen2.5-7B Q4 tokens/sec
- [ ] `bench_full_pipeline.sh` — end-to-end VRAM peak via `nvidia-smi`

---

## Production inference sizing

Use benchmark results from this GPU to **size central server GPUs** (e.g. if one 5070 handles 2 live + 16 batch lessons/day, rent equivalent GPU in India cloud for N schools).

**D-PROC closed (Hybrid):** size **India cloud** GPUs from 5070 benchmarks; edge nodes are buffer/ingest only (no classroom GPU). See [ADR-0008](../08-rfc-adr/ADR-0008-d-proc-hybrid-central-ml.md).
