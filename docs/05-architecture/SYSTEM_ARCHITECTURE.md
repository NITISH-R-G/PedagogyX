# System Architecture v0.1 (Reference)

**Status:** Draft — **blocked on G0/G1 founder decisions**  
**RFC:** [RFC-0001](../08-rfc-adr/RFC-0001-platform-vision-and-scope.md)

---

## Architectural Principles

1. **Privacy tiers by configuration** — same codebase, different feature flags per tenant
2. **Immutable ingest** — raw media append-only; analytics recomputable
3. **Event-driven** — lesson lifecycle as event stream
4. **Human-in-the-loop** for externally visible AI coaching
5. **Eval-first ML** — no model promotion without benchmark regression pass

---

## Logical Architecture

```mermaid
flowchart TB
    subgraph clients [Clients]
        WEB[Web App]
        MOB[Mobile Capture]
        EXT[LMS/VCS Integrations]
    end

    subgraph edge [Optional Edge]
        ENC[Classroom Encoder Appliance]
    end

    subgraph api [Control Plane]
        GW[API Gateway]
        AUTH[Auth / RBAC]
        META[Session Metadata Service]
    end

    subgraph ingest [Ingestion]
        UP[Upload Service]
        BUS[Event Bus]
        TR[Transcode Worker]
    end

    subgraph ml [ML Plane]
        ASR[ASR + Diarization]
        NLP[Discourse Analytics]
        CV[Video Understanding]
        FUS[Multimodal Fusion]
        LLM[Coaching Agent]
    end

    subgraph data [Data Plane]
        OBJ[(Object Storage)]
        OLTP[(PostgreSQL)]
        OLAP[(ClickHouse)]
        VEC[(Vector Store)]
        GRAPH[(Graph DB - optional)]
    end

    subgraph exp [Experience]
        REV[Review Player]
        COACH[Coach Workspace]
        DASH[District Analytics]
    end

    WEB --> GW
    MOB --> UP
    EXT --> UP
    ENC --> UP
    GW --> AUTH
    GW --> META
    UP --> OBJ
    UP --> BUS
    BUS --> TR
    TR --> OBJ
    BUS --> ASR
    ASR --> NLP
    TR --> CV
    NLP --> FUS
    CV --> FUS
    FUS --> OLAP
    FUS --> VEC
    FUS --> LLM
    META --> OLTP
  LLM --> COACH
    OBJ --> REV
    OLAP --> DASH
```

---

## Lesson Lifecycle (Event Model)

```mermaid
stateDiagram-v2
    [*] --> Draft: teacher_schedules
    Draft --> Uploading: capture_started
    Uploading --> Ingested: upload_complete
    Ingested --> Transcoding: transcode_queued
    Transcoding --> Transcribed: asr_complete
    Transcribed --> Analyzed: analytics_complete
    Analyzed --> InReview: coach_opens
    InReview --> Published: teacher_accepts_feedback
    Published --> Archived: retention_policy
    Archived --> [*]
```

**Core events (Avro/Protobuf TBD):** `lesson.uploaded`, `lesson.transcoded`, `lesson.transcript.ready`, `lesson.metrics.computed`, `lesson.coaching.draft`, `lesson.coaching.approved`

---

## Deployment Architecture (Cloud Reference)

```mermaid
flowchart LR
    subgraph region [Region e.g. us-east-1]
        subgraph k8s [Kubernetes]
            API[API pods]
            WRK[GPU worker pools]
            CPU[CPU workers]
        end
        S3[(S3)]
        RDS[(RDS Postgres)]
        CH[(ClickHouse Cloud)]
        KFK[Kafka/Redpanda]
    end
    CDN[CloudFront]
    CDN --> S3
    API --> RDS
    WRK --> S3
    WRK --> KFK
    CPU --> KFK
```

**[ASSUMPTION]** Single-region MVP; multi-region for EU data residency in Phase 2.

---

## Subsystem Boundaries

| Service | Responsibility | SLO draft |
|---------|----------------|-----------|
| Upload | Resumable multipart, virus scan, checksum | 99.9% |
| Transcode | H.264/H.265 normalization, thumbnails | p95 < 2× realtime |
| ASR | Transcript + diarization + confidence | p95 < 15 min / 50 min lesson |
| Discourse | Talk ratio, questions, dialogic proxies | batch |
| CV | Optional detectors | GPU quota |
| Coaching Agent | RAG + rubric-grounded narrative | human approval |
| Analytics API | Aggregates only for district roles | k-anonymity ≥ 5 |

---

## Sequence: Post-Lesson Analysis (Default Path)

```mermaid
sequenceDiagram
    participant T as Teacher
    participant U as Upload
    participant E as Event Bus
    participant X as Transcode
    participant A as ASR
    participant M as ML Fusion
    participant C as Coach UI
    participant H as Human Coach

    T->>U: Upload lesson artifact
    U->>E: lesson.uploaded
    E->>X: transcode job
    X->>E: lesson.transcoded
    E->>A: transcribe job
    A->>E: lesson.transcript.ready
    E->>M: analyze job
    M->>E: lesson.metrics.computed
    M->>C: AI coaching draft
    H->>C: Review/edit/approve
    C->>T: Published feedback
```

---

## Security Zones

| Zone | Data | Exposure |
|------|------|----------|
| Public | Marketing | Internet |
| App | De-identified analytics | Authenticated users |
| Sensitive | Raw video, transcripts with student voice | RBAC + audit |
| ML | Training exports | Isolated account, no prod keys |

---

## Open Architecture Questions

See [CRITICAL_DECISIONS_BLOCKERS.md](../01-phase0-founder-interrogation/CRITICAL_DECISIONS_BLOCKERS.md) and ADRs.
