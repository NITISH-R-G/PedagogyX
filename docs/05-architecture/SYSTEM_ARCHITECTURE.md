# System Architecture v0.2 (India Supervision)

**Status:** Draft — aligned to [FOUNDER_ANSWERS.md](../01-phase0-founder-interrogation/FOUNDER_ANSWERS.md)  
**Supersedes:** v0.1 assumptions (US coaching-only)  
**ADRs:** [ADR-0003](../08-rfc-adr/ADR-0003-india-supervision-v1-scope.md), [ADR-0004](../08-rfc-adr/ADR-0004-capture-screen-multicam.md)

---

## Architectural Principles (Revised)

1. **India data residency** default (ap-south-1)
2. **Dual analytics path:** real-time (hot) + batch (cold, authoritative scores)
3. **Multi-stream sync** — screen + mic + multi-cam
4. **Supervision mode** — admin dashboards with individual teacher metrics
5. **Segment templates** — K-12 vs university org policies
6. Human review **recommended** for AI narratives; **not blocking** admin quantitative scores

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

| Challenge | Mitigation |
|-----------|------------|
| A/V drift | Cross-correlate screen OCR events with speech |
| Multi-cam alignment | Hardware genlock or software timestamp + calibration |
| Packet loss | Local ring buffer on agent; resumable upload |

---

## Real-Time vs Batch Responsibilities

| Capability | Hot path (latency) | Cold path (quality) |
|------------|-------------------|---------------------|
| Talk ratio estimate | ~5s rolling | Final diarization |
| Activity detection | Lightweight YOLO | Full transformer fusion |
| Engagement proxy | Heuristic | Calibrated model |
| Pedagogy index | Preview score | **Authoritative** admin score |
| Coaching tips | Live nudges (optional) | Full LLM report |

**[ASSUMPTION]** Admin contractual SLAs reference **cold path** scores; hot path labeled "preliminary."

---

## Deployment (India Reference)

```mermaid
flowchart LR
    subgraph in [ap-south-1]
        EKS[EKS cluster]
        GPU[GPU pool - inference]
        SFU[Media SFU]
        S3[(S3)]
        RDS[(Postgres)]
        CH[(ClickHouse)]
    end
    SCH[Schools] --> AGENT
    AGENT --> SFU
    SFU --> GPU
    GPU --> CH
```

**Bandwidth:** Multi-cam + screen may require **5–15 Mbps uplink** per classroom **[HYPOTHESIS]** — needs pilot measurement.

---

## RBAC (Supervision Mode)

| Role | Live view | Individual scores | Raw student video |
|------|-----------|-------------------|-------------------|
| Teacher | Own class | Own (preview) | Own sessions |
| Coach | Assigned | Assigned | If permitted |
| School admin | School | **Yes** | **Yes** |
| District admin | District aggregate + drill-down | **Yes** | Policy-dependent |
| University dean | Department | **Yes** | Policy-dependent |

Audit: immutable log of every stream view and score export.

---

## Capture Agent (v1)

See ADR-0004. Minimum platforms:

- Windows 10+ (primary lab / smart classroom PC)
- **[HYPOTHESIS]** Android companion for USB camera relay

Not in v1: iOS screen capture (policy restrictions).

---

## Open Blockers

- D-10 budget → GPU sizing
- D-12 LLM → coaching narrative architecture
- Legal G2 → consent flows in agent installer
