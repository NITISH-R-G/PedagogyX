# Founder Answers — Decision Log

**Recorded:** 2026-05-19  
**Source:** Founder reply to Tier-1 interrogation  
**Status:** **G0 complete** — **G2 legal still blocked** (implementation code)

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
| **D-20** | Year-1 success metric | **Primary M-A**; **Secondary M-B, M-C** | Unknown | Coverage + time-to-insight + admin action on flags |
| **D-DEV** | Device validation | **Any** panel meeting low-end profiles; OEM list is **examples only** | Named SKUs | [INDIA_PILOT_DEVICE_REFERENCE.md](INDIA_PILOT_DEVICE_REFERENCE.md) for pilot checklist |
| **D-CLIENT** | Production devices | **All low-end Android boards + all low-end Windows smartboards** (profile-based, no OEM whitelist) | Phone-only | ADR-0007; certify Android A/B + Windows SB profiles |
| **D-PEDAGOGY** | Primary product outcome | **Monitor & assess teacher teaching ability and pedagogy** | Mixed student/teacher analytics | Per-**teacher** scores and evidence; not per-student punitive ranking in v1 |
| **D-PROC** | Where ML runs in production | **C — Hybrid** (LAN edge buffer + India cloud GPU analytics) | Central TBD | ADR-0008 |

---

## Interpretation Notes (Architecture Team)

### Product focus (2026-05-19)

PedagogyX v1 exists to **monitor and assess how teachers teach** — instructional quality, discourse patterns, pacing, and composite **pedagogy** signals — for **school and university admins**, not to rank individual students.

| In scope (v1) | Out of scope / defer (v1) |
|---------------|---------------------------|
| Per-**teacher** lesson pedagogy index | Per-**student** report cards or punitive student scores |
| Admin/coach review of **teacher** sessions | Student identity as a primary dashboard unit |
| Capture from **any** certified low-end Android / Windows smartboard | iOS-only or high-end workstation-only deployments |
| Evidence clips tied to **teaching** moments | Social/emotional profiling of students as product goal |

Student video/audio may still be processed where legally permitted (D-03) to infer **classroom-level** discourse metrics (e.g. student talk ratio) that inform **teacher** pedagogy scores.

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

1. **D-DEV** — Log make/model at first pilot for compatibility matrix (any low-end board that passes profiles)

---

## Sign-off

| Role | Status |
|------|--------|
| Founder Tier-1 | **Complete** (D-DEV = confirm at pilot site) |
| Legal (India DPDP) | Not started |
| Architecture freeze | **Denied** until G2 legal memo |
| **D-20 (2026-05-19)** | **Primary M-A**, **Secondary M-B, M-C** — founder accepted architecture team suggestion |

**D-PROC (2026-05-19):** **C — Hybrid** — site LAN edge (buffer/ingest) + PedagogyX India cloud GPU analytics. See [ADR-0008](../08-rfc-adr/ADR-0008-d-proc-hybrid-central-ml.md).
