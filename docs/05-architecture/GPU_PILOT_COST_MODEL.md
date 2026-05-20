# GPU Pilot Cost Model (S01-03)

**Status:** Draft v0.1  
**Owner:** Architecture  
**Date:** 2026-05-19  
**Inputs:** D-10 = **₹0 customer budget**; D-PROC = **Hybrid**; D-20 = M-A / M-B / M-C

---

## Purpose

Estimate **founder-funded** monthly burn for free pilots — not school OPEX. Use this to cap classroom count before paid phase.

**Benchmark source:** RTX 5070 dev workstation ([GPU_BUDGET_RTX5070.md](GPU_BUDGET_RTX5070.md)) → size **1× cloud GPU** ≈ same VRAM class (12 GB).

---

## Assumptions

| Assumption                     | Value                                                  |
| ------------------------------ | ------------------------------------------------------ |
| Pilot geography                | India (`ap-south-1` or equivalent VPS)                 |
| Lessons per classroom per week | 5 × 45 min (M-A coverage target)                       |
| Hot path                       | Audio + 1 cam preview per active lesson                |
| Cold path                      | Full ASR + CV + LLM batch same night                   |
| Edge node                      | 1 per school (4–8 classrooms share)                    |
| Storage retention              | 90 days raw video **[HYPOTHESIS]** — legal may shorten |

---

## Unit economics (per classroom, founder cost)

| Line item                           | 1-school pilot (4 rooms) | 10-school pilot (40 rooms) | Notes                        |
| ----------------------------------- | ------------------------ | -------------------------- | ---------------------------- |
| **Cloud GPU** (12 GB, ~720h/mo)     | ₹18,000–₹35,000          | ₹45,000–₹90,000            | Shared pool; batch overnight |
| **Cloud CPU/RAM** (API, queue, DB)  | ₹3,000–₹6,000            | ₹8,000–₹15,000             | VPS 8 vCPU / 32 GB           |
| **Object storage** (MinIO/S3)       | ₹500–₹2,000              | ₹3,000–₹10,000             | ~2 GB/hour/room compressed   |
| **Egress / WAN**                    | ₹1,000–₹3,000            | ₹5,000–₹15,000             | Edge → cloud upload          |
| **Edge hardware** (amortized 36 mo) | ₹800/room                | ₹800/room                  | ₹25k NUC ÷ 4 rooms ÷ 36 mo   |
| **Total founder burn**              | **~₹23k–₹46k/mo**        | **~₹62k–₹130k/mo**         | Order-of-magnitude           |

**USD rough (₹83):** ~$280–$550/mo (1 school) · ~$750–$1,570/mo (10 schools).

---

## Capacity model (from RTX 5070 benchmarks — to validate)

| Workload                                  | Target on 12 GB GPU      | Pilot cap                           |
| ----------------------------------------- | ------------------------ | ----------------------------------- |
| Live preview (ASR partial + 1×480p CV)    | **2 concurrent lessons** | Hot path for 2 rooms simultaneously |
| Cold batch (50 min lesson, full pipeline) | **16 lessons / night**   | All rooms if staggered upload       |
| LLM report (Qwen2.5-7B Q4)                | **~1 report / 2–4 min**  | Queue after ASR completes           |

**[ACTION S01-09]:** Replace placeholders with measured RTF from `bench_*.py` on 5070.

---

## Scenarios

### Scenario A — Minimal free pilot (recommended start)

- **1 school**, 4 classrooms, 1 edge node, 1 cloud GPU
- **Founder burn:** ~₹25k–₹40k/month
- **M-A risk:** Low if teachers run ≥1 session/week
- **M-B target:** Preview &lt; 5 min; cold &lt; 45 min (aligns PRD)

### Scenario B — District demo

- **3 schools**, 12 classrooms, 3 edge nodes, 2 cloud GPUs
- **Founder burn:** ~₹55k–₹85k/month

### Scenario C — CPU-only fallback (zero GPU month)

- Batch ASR on CPU only; defer CV/LLM
- **Founder burn:** ~₹8k–₹15k/month
- **Trade-off:** M-B fails for real-time; M-A still achievable

---

## Decision triggers

| Signal                         | Action                                       |
| ------------------------------ | -------------------------------------------- |
| Queue backlog &gt; 2 h nightly | Add GPU or reduce CV resolution              |
| Storage &gt; ₹10k/mo           | Shorten retention; transcode to 720p archive |
| M-A coverage &lt; 70%          | Fix client reliability before adding GPU     |
| Founder burn &gt; comfort cap  | Pause new school onboarding                  |

---

## Spreadsheet export (manual)

Copy to Google Sheets / Excel:

```csv
Classrooms,Cloud GPU INR,Cloud CPU INR,Storage INR,Egress INR,Edge INR/mo,Total INR/mo
4,25000,4500,1000,2000,3200,35700
12,55000,8000,4000,6000,9600,82600
40,70000,12000,8000,12000,32000,132000
```

---

## References

- [ADR-0008](../08-rfc-adr/ADR-0008-d-proc-hybrid-central-ml.md)
- [CENTRAL_OSS_BACKEND_SPEC.md](CENTRAL_OSS_BACKEND_SPEC.md)
- [DOCKER_COMPOSE_PILOT_STACK.md](../06-stack-evaluation/DOCKER_COMPOSE_PILOT_STACK.md)
