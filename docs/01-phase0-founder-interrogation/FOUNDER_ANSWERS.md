# Founder Answers — Decision Log

**Recorded:** 2026-05-19  
**Source:** Founder reply to Tier-1 interrogation  
**Status:** G0 nearly complete — **G2 legal still blocked**; **D-20** success metric TBD (default M-A+M-B until chosen)

---

## Tier 1 Answers

| ID | Question | **Founder answer** | Prior default | Architecture impact |
|----|----------|-------------------|---------------|---------------------|
| **D-01** | Primary customer | **K-12 district + university** (dual segment) | K-12 US only | Dual RBAC, rubrics, sales motions |
| **D-02** | Year-1 geography | **India** | US only | DPDP, data residency, Hindi/English ASR, ap-south-1 |
| **D-03** | Identifiable student video in v1 | **Yes** | No | Full CV, identity tracking, DPIA mandatory |
| **D-04** | Real-time coaching in v1 | **Yes** | No | WebRTC/live pipeline, edge GPU, <3s latency targets |
| **D-05** | Economic buyer | **School + university** (principal / dean / campus IT) | District office | Pilot signed at **institution** level; not state procurement for v1 |
| **D-06** | Admins see individual AI pedagogy scores | **Yes** | Coaches only | Admin dashboards, audit, union/parent risk |
| **D-07** | China-style supervision acceptable | **Yes** (some markets) | No | Supervision mode, Flanders/S-T-style rollups |
| **D-08** | Capture model | **Screen recording + microphone** (not generic “phone video only”) | BYOD upload | Desktop agent / browser capture, A/V sync |
| **D-09** | MVP modality | **Multi-camera** | Single cam | Multi-stream sync, higher GPU cost |
| **D-10** | Budget per classroom/year | **₹0 / $0 (customer)** — free pilot; **no monetary expectations** in test year | Unknown | Size infra to **founder/dev cost**, not school OPEX; see note below |
| **D-11** | ASR languages | *Not answered* | English | **Assume** English + Hindi for India unless corrected |
| **D-12** | Cloud LLM on student-adjacent data | **OSS only — Ollama/vLLM on-prem** | Private/vPC | **Closed** — Qwen2.5-7B-Q4 on RTX 5070 |
| **D-GPU** | Max GPU hardware | **RTX 5070 12 GB** | Cloud GPU | **Closed** — ADR-0006 |
| **D-OSS** | Stack preference | **Free & open source first** | Mixed | **Closed** — ADR-0005 |
| **D-20** | Year-1 success metric | **TBD** (founder requested detailed guide) | — | [FOUNDER_SUCCESS_METRICS_GUIDE.md](FOUNDER_SUCCESS_METRICS_GUIDE.md); **default M-A + M-B** if silent |
| **D-DEV** | India OEM devices | **Research list** (founder IDK) | — | [INDIA_PILOT_DEVICE_REFERENCE.md](INDIA_PILOT_DEVICE_REFERENCE.md); confirm at pilot site |
| **D-CLIENT** | Production devices | **Android + low-end Windows smartboards** | Phone-only | ADR-0007 |
| **D-PROC** | Where ML runs in production | **C — Hybrid** (LAN edge buffer + India cloud GPU analytics) | Central TBD | ADR-0008 |

---

## Interpretation Notes (Architecture Team)

### Capture stack clarification needed

“Screen recording + mic” implies:

- Teacher laptop/tablet **display capture** (slides, LMS, videos)
- **Microphone** for classroom audio
- **Multi-cam** for room video (student/teacher/board)

**[ASSUMPTION]** Three synchronized streams minimum per active session.

### Product positioning shift

Founder choices align with **supervision + analytics** platforms (China smart classroom, Indian “smart class” vendors) more than **US union-friendly coaching** (Edthena/TeachFX). PedagogyX must implement **mode flags**:

| Mode | Admin scores | Student ID video | Real-time | Use case |
|------|--------------|------------------|-------------|----------|
| `supervision` | Yes | Yes | Yes | Founder v1 default |
| `coaching` | Restricted | De-identified optional | Optional | Future US export |

### Pilot commercial model (2026-05-19)

- **Buyer entity:** individual **schools** and **universities** (not state/district as economic buyer for v1).
- **Payment:** **none expected** in test phase — free evaluation only.
- **D-10 = ₹0 customer budget** does **not** mean zero cloud cost; PedagogyX bears infra during pilot (minimize via hybrid edge + single GPU pool).

### Unresolved blockers (next founder reply)

1. **D-20** — Pick primary success metric: `Primary: M-?` — see [FOUNDER_SUCCESS_METRICS_GUIDE.md](FOUNDER_SUCCESS_METRICS_GUIDE.md)
2. **D-DEV** — Confirm **exact** panel/tablet model at first pilot site (use checklist in device reference)

---

## Sign-off

| Role | Status |
|------|--------|
| Founder Tier-1 | **Complete except D-20** (D-DEV = research until site visit) |
| Legal (India DPDP) | Not started |
| Architecture freeze | **Denied** until G2 legal memo |
| Success metric default | **M-A + M-B** if D-20 still open at Sprint 01 end |

**D-PROC (2026-05-19):** **C — Hybrid** — site LAN edge (buffer/ingest) + PedagogyX India cloud GPU analytics. See [ADR-0008](../08-rfc-adr/ADR-0008-d-proc-hybrid-central-ml.md).
