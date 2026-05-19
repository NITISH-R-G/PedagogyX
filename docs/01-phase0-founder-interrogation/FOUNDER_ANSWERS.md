# Founder Answers — Decision Log

**Recorded:** 2026-05-19  
**Source:** Founder reply to Tier-1 interrogation  
**Status:** G0 partially satisfied — **G1/G2 still blocked** (D-10–D-12, success metric, India legal sign-off)

---

## Tier 1 Answers

| ID | Question | **Founder answer** | Prior default | Architecture impact |
|----|----------|-------------------|---------------|---------------------|
| **D-01** | Primary customer | **K-12 district + university** (dual segment) | K-12 US only | Dual RBAC, rubrics, sales motions |
| **D-02** | Year-1 geography | **India** | US only | DPDP, data residency, Hindi/English ASR, ap-south-1 |
| **D-03** | Identifiable student video in v1 | **Yes** | No | Full CV, identity tracking, DPIA mandatory |
| **D-04** | Real-time coaching in v1 | **Yes** | No | WebRTC/live pipeline, edge GPU, <3s latency targets |
| **D-05** | Economic buyer | *Not answered* | District office | **BLOCKER** — school vs university vs state |
| **D-06** | Admins see individual AI pedagogy scores | **Yes** | Coaches only | Admin dashboards, audit, union/parent risk |
| **D-07** | China-style supervision acceptable | **Yes** (some markets) | No | Supervision mode, Flanders/S-T-style rollups |
| **D-08** | Capture model | **Screen recording + microphone** (not generic “phone video only”) | BYOD upload | Desktop agent / browser capture, A/V sync |
| **D-09** | MVP modality | **Multi-camera** | Single cam | Multi-stream sync, higher GPU cost |
| **D-10** | Budget per classroom/year | *Not answered* | Unknown | **BLOCKER** for unit economics |
| **D-11** | ASR languages | *Not answered* | English | **Assume** English + Hindi for India unless corrected |
| **D-12** | Cloud LLM on student-adjacent data | *Not answered* | Private/vPC | **BLOCKER** — default India: in-region private inference |
| **D-20** | Year-1 success metric | **Unknown (TBD)** | — | See [SUCCESS_METRIC_OPTIONS.md](SUCCESS_METRIC_OPTIONS.md) |

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

### Unresolved blockers (next founder reply)

1. **D-05** — Who signs: state/scheme, district, school principal, university registrar?
2. **D-10** — Max ₹/USD per classroom/month for GPU + storage?
3. **D-12** — Azure OpenAI India / self-hosted Llama / no LLM on raw student video?
4. **Success metric** — pick one primary from options doc?

---

## Sign-off

| Role | Status |
|------|--------|
| Founder Tier-1 | Partial (8/10 answered) |
| Legal (India DPDP) | Not started |
| Architecture freeze | **Denied** until D-10, D-12, legal memo |
