# System Architecture v0.4 (Thin Clients + Central OSS Backend)

**Status:** Draft — aligned to [FOUNDER_ANSWERS.md](../01-phase0-founder-interrogation/FOUNDER_ANSWERS.md)  
**Supersedes:** v0.1 assumptions (US coaching-only)  
**ADRs:** [ADR-0003](../08-rfc-adr/ADR-0003-india-supervision-v1-scope.md), [ADR-0004](../08-rfc-adr/ADR-0004-capture-screen-multicam.md), [ADR-0005](../08-rfc-adr/ADR-0005-foss-first-stack.md), [ADR-0006](../08-rfc-adr/ADR-0006-rtx5070-compute-budget.md), [ADR-0007](../08-rfc-adr/ADR-0007-production-clients-low-end.md)  
**OSS stack:** [OSS_STACK_REFERENCE.md](../06-stack-evaluation/OSS_STACK_REFERENCE.md) | **GPU:** [GPU_BUDGET_RTX5070.md](GPU_BUDGET_RTX5070.md)

---

## Architectural Principles (Revised)

1. **OSS-first** — self-hosted; no proprietary ASR/LLM APIs ([ADR-0005](../08-rfc-adr/ADR-0005-foss-first-stack.md))
2. **Thin clients** — Android + low-end Windows smartboards capture/upload only ([ADR-0007](../08-rfc-adr/ADR-0007-production-clients-low-end.md)) ([ADR-0006](../08-rfc-adr/ADR-0006-rtx5070-compute-budget.md), [ADR-0007](../08-rfc-adr/ADR-0007-production-clients-low-end.md))
3. **India data residency** — school LAN / on-prem MinIO + Postgres
4. **Dual path:** **audio + 1 cam live** (hot) + **full multi-cam + screen** batch (cold, authoritative)
5. **Multi-stream sync** — screen + mic + multi-cam
6. **Supervision mode** — admin dashboards; **final** scores after cold queue
7. **Segment templates** — K-12 vs university

---

## Logical Architecture

```mermaid
flowchart TB
    subgraph capture [Capture Layer]
        AGENT[Desktop Capture Agent]
        SCR[Screen stream]
        MIC[Mic stream]
        CAM1[Cam 1]
        CAM2[Cam 2]
    end

    subgraph realtime [Hot Path - Real-Time]
        ING[Stream Ingest / WebRTC SFU]
        EDGE[Edge Feature Workers]
        LIVE[Live Analytics Bus]
        DASH_L[Live Admin Dashboard]
    end

    subgraph batch [Cold Path - Authoritative]
        ARCH[Object Store Archive]
        TR[Transcode + Index]
        ML[Batch ML Fusion]
        SCORE[Pedagogy Score Store]
    end

    subgraph plane [Control Plane]
        GW[API Gateway]
        AUTH[Auth RBAC]
        TEN[Tenant K-12 / Univ]
    end

    AGENT --> SCR & MIC & CAM1 & CAM2
    SCR & MIC & CAM1 & CAM2 --> ING
    ING --> EDGE --> LIVE --> DASH_L
    ING --> ARCH --> TR --> ML --> SCORE
    GW --> AUTH --> TEN
    SCORE --> DASH_A[Admin Analytics]
    SCORE --> T_PORT[Teacher Portal]
```

---

## Stream Synchronization

```mermaid
sequenceDiagram
    participant A as Capture Agent
    participant S as Sync Service
    participant H as Hot Path
    participant C as Cold Archive

    A->>S: Register session + stream descriptors
    par Streams
        A->>S: screen chunks
        A->>S: audio chunks
        A->>S: cam1/cam2 chunks
    end
    S->>H: Aligned micro-batches (e.g. 2s windows)
    S->>C: Chunked upload for durable storage
    Note over S: Master clock = audio sample clock
```

| Challenge           | Mitigation                                           |
| ------------------- | ---------------------------------------------------- |
| A/V drift           | Cross-correlate screen OCR events with speech        |
| Multi-cam alignment | Hardware genlock or software timestamp + calibration |
| Packet loss         | Local ring buffer on agent; resumable upload         |

---

## Real-Time vs Batch Responsibilities

| Capability          | Hot path (latency)     | Cold path (quality)           |
| ------------------- | ---------------------- | ----------------------------- |
| Talk ratio estimate | ~5s rolling            | Final diarization             |
| Activity detection  | Lightweight YOLO       | Full transformer fusion       |
| Engagement proxy    | Heuristic              | Calibrated model              |
| Pedagogy index      | Preview score          | **Authoritative** admin score |
| Coaching tips       | Live nudges (optional) | Full LLM report               |

**[ASSUMPTION]** Admin contractual SLAs reference **cold path** scores; hot path labeled "preliminary."

---

## Deployment (Production)

```mermaid
flowchart TB
    subgraph clients [Classroom - low spec]
        AND[Android app]
        WIN[Windows smartboard app]
    end
    subgraph edge [Site LAN edge - D-PROC hybrid]
        EDGE[Edge ingest + buffer]
    end
    subgraph cloud [PedagogyX India cloud OSS]
        MTX[MediaMTX / ingest]
        API[API]
        Q[Job queue]
        GPU[GPU workers]
        DB[(Postgres + MinIO)]
    end
    AND --> EDGE
    WIN --> EDGE
    EDGE -->|WAN upload| MTX
    MTX --> API --> Q --> GPU --> DB
```

| Layer               | Where it runs                                     |
| ------------------- | ------------------------------------------------- |
| Capture / encode    | **Android, Windows smartboard**                   |
| Buffer / LAN ingest | **District/school edge node** (hybrid — ADR-0008) |
| ASR, CV, LLM        | **India cloud** GPU workers (OSS stack)           |
| Model dev / bench   | **Developer RTX 5070** only                       |

See [PRODUCTION_CLIENT_SPEC.md](PRODUCTION_CLIENT_SPEC.md).

## RBAC (Supervision Mode)

| Role            | Live view                       | Individual scores | Raw student video |
| --------------- | ------------------------------- | ----------------- | ----------------- |
| Teacher         | Own class                       | Own (preview)     | Own sessions      |
| Coach           | Assigned                        | Assigned          | If permitted      |
| School admin    | School                          | **Yes**           | **Yes**           |
| District admin  | District aggregate + drill-down | **Yes**           | Policy-dependent  |
| University dean | Department                      | **Yes**           | Policy-dependent  |

Audit: immutable log of every stream view and score export.

---

## Capture Agent (v1)

See ADR-0004. Minimum platforms:

- Windows 10+ (primary lab / smart classroom PC)
- **[HYPOTHESIS]** Android companion for USB camera relay

Not in v1: iOS screen capture (policy restrictions).

---

## Open Blockers

- D-10 budget → GPU sizing (cloud pool + edge hardware)
- Legal G2 → consent flows in agent installer
- D-DEV → India OEM smartboard/Android models for minimum specs
