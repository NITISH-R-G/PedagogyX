# Product Decision Implications Analysis

**Based on:** Founder answers 2026-05-19  
**Labeling:** Mix of **[FACT]** (founder stated), **[INFERENCE]**, **[RISK]**

---

## Executive Summary

Your choices define a **India-first, supervision-heavy, multimodal real-time platform**—closer to **AI Sokrates / 智慧课堂** than to **Edthena/TeachFX**. Engineering complexity and compliance burden **exceed** the original Phase 1 audio-MVP by an estimated **4–6×** on infra and **2–3×** on team size for same timeline.

---

## What Changed vs Original Plan

| Dimension    | Was (ADR-0001/002)        | Now                                |
| ------------ | ------------------------- | ---------------------------------- |
| Geography    | US                        | **India (DPDP)**                   |
| Video        | De-identified optional    | **Identifiable required**          |
| Latency      | Batch post-lesson         | **Real-time + batch**              |
| Admin        | Coaches only              | **Individual AI scores visible**   |
| Ethics       | Anti-surveillance default | **Supervision explicitly OK**      |
| Capture      | Upload MP4                | **Screen + mic + multi-cam agent** |
| MVP modality | Audio → video phased      | **Multi-cam day one**              |
| Segments     | K-12                      | **K-12 + university**              |

---

## Architecture Impacts **[INFERENCE]**

### Must build immediately (Phase 1 scope inflation)

1. **Desktop capture agent** (screen + multi USB/RTSP cam)
2. **Media SFU / stream ingest** (WebRTC or SRT)
3. **Sync + drift correction** service
4. **GPU hot-path** + **GPU cold-path** (costly)
5. **Live WebSocket dashboards** for admins
6. **Hindi/English** ASR pipeline
7. **India region** full stack (no US-only services)

### Can defer (but document)

- US FERPA-first features
- Union-friendly "teacher-only sharing" as default
- Audio-only tier (still offer as **school opt-in** for cost)

---

## Compliance Impacts **[RISK]**

| Item                            | Severity                                  |
| ------------------------------- | ----------------------------------------- |
| Children's identifiable video   | **Critical** — DPDP + school consent      |
| Admin scores linked to teachers | Employment law review                     |
| Real-time processing            | Continuous monitoring disclosure          |
| Screen capture                  | May capture student names/chat from LMS   |
| University segment              | Adults — simpler consent, different buyer |

**G2 gate cannot clear without Indian counsel.**

---

## Commercial Impacts

**Buyers (guess until D-05 answered):**

- State smart-education programs
- Private school chains
- University quality cells / NAAC-style accreditation support

**Pricing driver:** per-classroom GPU-hours + storage, not per-seat only.

---

## Contradictions Still Open

1. **Cloud LLM** — you did not answer; we default **in-region private, no child images in prompts**
2. **Success metric** — pick from [SUCCESS_METRIC_OPTIONS.md](SUCCESS_METRIC_OPTIONS.md)
3. **Economic buyer** — state vs school vs university
4. **Per-student admin scores** — not specified (recommend **no** for v1)

---

## Recommended Immediate Founder Actions

1. Pick **D-20** primary metric (guide published); **D-05, D-10, D-12** closed
2. Pick **primary success metric** (suggest **M-A + M-B**: coverage + time-to-insight)
3. Confirm: **per-student** scores on admin UI — yes/no?
4. Engage **India privacy counsel** this week
5. Name **one pilot partner** (state, chain, or university)

---

## Sprint 01 Re-Scope

| Original Sprint 01  | Revised Sprint 01                     |
| ------------------- | ------------------------------------- |
| OpenAPI upload      | **Capture agent PRD + sync protocol** |
| ASR benchmark       | **EN+HI ASR benchmark**               |
| Coach UI wireframes | **Admin live dashboard wireframes**   |
| US FERPA memo       | **India DPDP memo (counsel)**         |
| Cost model          | **Multi-stream GPU cost model**       |

**Implementation code still blocked** until G2. Pilot infra sized to **founder cost** (D-10 = ₹0 customer budget).

---

## Update: Free pilot + zero customer budget (2026-05-19)

| Impact    | Detail                                                                            |
| --------- | --------------------------------------------------------------------------------- |
| **D-05**  | Signatories: **school principal / university dean or IT** — not state procurement |
| **D-10**  | **₹0 / $0** per classroom from customer; no revenue expectation in test year      |
| **Infra** | Minimize cloud GPU hours; one edge node + one cloud GPU pool; dev on RTX 5070     |
| **G5**    | Track **internal** burn, not school OPEX                                          |
| **M-D**   | Do **not** use paid renewal as primary success metric in year 1                   |

---

## Update: D-PROC Hybrid (2026-05-19)

| Impact            | Detail                                                                         |
| ----------------- | ------------------------------------------------------------------------------ |
| **Deployment**    | Two reference stacks: **edge** (LAN buffer/ingest) + **cloud** (GPU analytics) |
| **Sprint 01**     | RFC-0002 capture/sync; S01-10 Compose profiles; Android + Windows capture RFCs |
| **Ops**           | PedagogyX operates cloud GPU; districts host edge node (Compose/k3s)           |
| **Still blocked** | Implementation until G2; **D-10** for sizing                                   |

See [ADR-0008](../08-rfc-adr/ADR-0008-d-proc-hybrid-central-ml.md).

---

## Update: OSS + RTX 5070 (2026-05-19)

| Impact              | Detail                                                                     |
| ------------------- | -------------------------------------------------------------------------- |
| **Cost model**      | Cap-ex per edge server (~GPU + 64GB RAM) vs cloud GPU-hours                |
| **Real-time scope** | **Reduced** — audio + 1 cam live; multi-cam batch on same 5070             |
| **Stack**           | faster-whisper, YOLO TensorRT, Ollama, MinIO, Postgres, MediaMTX           |
| **Timeline**        | GPU scheduler + Compose pilot before K8s                                   |
| **Risk R-07**       | Mitigated at small scale; returns if school expects 20 live rooms on 1 GPU |

See [HARDWARE_CONSTRAINTS.md](HARDWARE_CONSTRAINTS.md).
