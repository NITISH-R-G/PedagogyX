# ADR-0008: D-PROC — Hybrid Central ML (LAN Edge + India Cloud)

| Field              | Value                       |
| ------------------ | --------------------------- |
| **Status**         | Accepted (founder-directed) |
| **Date**           | 2026-05-19                  |
| **Decision ID**    | **D-PROC**                  |
| **Founder choice** | **C — Hybrid**              |

## Context

Production clients (Android + low-end Windows smartboards) capture and encode only. Heavy OSS ML (faster-whisper, TensorRT/YOLO, Ollama) runs on **central** infrastructure, not in the classroom.

Founder was asked to choose where that central stack runs:

| Option | Summary                                                  |
| ------ | -------------------------------------------------------- |
| **A**  | PedagogyX-managed cloud (India VPS + GPU)                |
| **B**  | District/school on-prem server (Compose / k3s)           |
| **C**  | **Hybrid** — LAN buffer/ingest at site + cloud analytics |

## Decision

**Adopt Option C (Hybrid)** for v1 production architecture.

### v1 split of responsibility

| Layer                 | Location                                                   | Role                                                                                                                        |
| --------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Classroom capture** | Android + Windows smartboard                               | Screen + mic (+ optional cam); H.264 encode; consent UI                                                                     |
| **Site edge (LAN)**   | District or school **edge node** (mini-server / NUC class) | MediaMTX or equivalent ingest; **offline buffer**; resumable upload; optional RTSP fan-in; **no** full GPU ML on edge in v1 |
| **Central analytics** | PedagogyX **India-region** OSS backend (VPS + GPU)         | Hot-path previews (talk ratio, activity proxies); cold-path ASR, CV, LLM, authoritative pedagogy index                      |
| **Model dev**         | Founder **RTX 5070** workstation                           | Benchmark and export only — see ADR-0006                                                                                    |

**[ASSUMPTION]** Edge and cloud communicate over HTTPS/TLS; when WAN is down, edge retains encrypted buffers until backfill succeeds.

### Rationale (founder trade-off)

- **LAN edge** reduces classroom dependency on continuous internet; supports weak uplinks common in Indian schools.
- **Cloud central** keeps multi-school updates, GPU pooling, and operational control with PedagogyX.
- **Cost/complexity** accepted: two deployment surfaces (edge Compose profile + cloud Compose/K8s profile) vs pure A or B.

## Consequences

### Positive

- Aligns with [PRODUCTION_CLIENT_SPEC.md](../05-architecture/PRODUCTION_CLIENT_SPEC.md) offline buffer + resumable upload.
- Sprint 01 can spec **central OSS backend** and **capture agent RFCs** without choosing pure cloud-only or pure on-prem-only.
- District IT can host a **known hardware profile** for edge while PedagogyX operates GPU analytics.

### Negative / mitigations

| Risk                            | Mitigation                                                                   |
| ------------------------------- | ---------------------------------------------------------------------------- |
| Two ops surfaces (edge + cloud) | Single OSS Compose reference for edge; same container images where possible  |
| Edge hardware variance          | Reference edge spec in S01; pilot on 1–2 district archetypes                 |
| Data residency / DPDP           | India cloud region; edge stores encrypted at rest; retention policy in DPIA  |
| Sync conflicts                  | Edge is **buffer + forward**; authoritative scores only from cloud cold path |

## Still open (not D-PROC)

| ID             | Item                                                                    |
| -------------- | ----------------------------------------------------------------------- |
| **D-10**       | Budget per classroom/year (₹ or USD) — sizes cloud GPU pool             |
| **D-DEV**      | Exact Android + smartboard **OEM models** for India pilot minimum specs |
| **D-05, D-12** | Economic buyer; LLM already closed OSS on-prem at central GPU           |

## References

- [FOUNDER_ANSWERS.md](../01-phase0-founder-interrogation/FOUNDER_ANSWERS.md)
- [SYSTEM_ARCHITECTURE.md](../05-architecture/SYSTEM_ARCHITECTURE.md)
- [OSS_STACK_REFERENCE.md](../06-stack-evaluation/OSS_STACK_REFERENCE.md)
- Supersedes open **D-PROC** questions in ADR-0006, ADR-0007

## Validation

- [ ] RFC-0002 Capture Agent & Sync Protocol references hybrid upload path
- [ ] S01-10 Docker Compose defines **edge** and **cloud** profiles
- [ ] D-10 spreadsheet includes edge hardware + cloud GPU line items
