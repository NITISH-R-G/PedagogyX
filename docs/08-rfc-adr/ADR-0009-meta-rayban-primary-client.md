# ADR-0009: Meta Ray-Ban Smart Glasses as Primary Capture Client

| Field          | Value                                                                                                                   |
| -------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Status**     | **Accepted (plan change)**                                                                                              |
| **Date**       | 2026-05-23                                                                                                              |
| **Supersedes** | **Primary capture path** in [ADR-0007](ADR-0007-production-clients-low-end.md) (smartboards remain optional / Phase 1b) |

## Context

Founder direction (2026-05-23): **PedagogyX v1 will run on Meta Ray-Ban smart glasses** using the **Wearables Device Access Toolkit (DAT)** — not only on low-end Android/Windows classroom panels.

Prior docs (D-CLIENT, ADR-0007) targeted **smartboard thin clients** in India classrooms. That path stays valid for **fixed-room, screen-centric** capture but is **no longer the primary v1 wearable**.

## Decision

### Primary production client (v1 pilot)

| Layer         | Choice                                                                          |
| ------------- | ------------------------------------------------------------------------------- |
| **Hardware**  | Meta Ray-Ban Meta AI glasses (Ray-Ban Meta line)                                |
| **SDK**       | Meta Wearables **DAT** (`mwdat-core`, `mwdat-camera`)                           |
| **Companion** | **Android phone** running PedagogyX capture app (DAT host)                      |
| **Dev/test**  | **Mock Device Kit** — no physical glasses required in CI                        |
| **Upload**    | Phone forwards chunks / lifecycle to PedagogyX API (hybrid D-PROC per ADR-0008) |

### Capture semantics (revised)

| Stream             | Source                                          | Notes                                                                |
| ------------------ | ----------------------------------------------- | -------------------------------------------------------------------- |
| **POV video**      | Glasses camera via DAT `Stream` / `videoStream` | Replaces classroom multicam + screen capture as **primary** sensor   |
| **Audio**          | Glasses mic (DAT)                               | Master clock per [RFC-0002](RFC-0002-capture-agent-sync-protocol.md) |
| **Screen / board** | **Not in v1 primary path**                      | Optional phone MediaProjection in a later release                    |

**Implication:** D-08 (“screen + mic”) and D-09 (“multi-cam”) from Tier-1 are **partially superseded** for v1 — see [FOUNDER_ANSWERS.md](../01-phase0-founder-interrogation/FOUNDER_ANSWERS.md) plan-change table.

### Smartboards (ADR-0007)

- **Status:** Deferred / secondary — “classroom-fixed” profile for schools that cannot use wearables
- **No removal** of Android/Windows spec; do not invest new v1 features there until Ray-Ban path is pilot-validated

## Architecture impact

```mermaid
flowchart LR
    GL[Ray-Ban Meta glasses]
    PH[PedagogyX Android app DAT host]
    API[PedagogyX cloud API]
    W[GPU workers]

    GL <-->|Bluetooth DAT| PH
    PH -->|HTTPS chunks + lifecycle| API
    API --> W
```

- **Repo module:** [clients/android-capture-dat](../../clients/android-capture-dat/README.md)
- **Server bridge:** [RFC-0004](RFC-0004-dat-session-bridge.md), `POST /v1/dat-sessions/*`
- **Hot path:** DAT WebRTC / stream (MediaMTX) where enabled; **cold path:** chunked upload from phone buffer

## Compliance & product (unchanged, higher scrutiny)

- **G2** still required before real classroom/school data
- **Teacher-worn camera** increases notice/consent and union sensitivity — use [PRIVACY_NOTICE_CONSENT_WIREFRAMES.md](../02-product/PRIVACY_NOTICE_CONSENT_WIREFRAMES.md)
- **D-PEDAGOGY** unchanged: assess **teacher pedagogy**, not student league tables

## Consequences

| Area        | Action                                                                                |
| ----------- | ------------------------------------------------------------------------------------- |
| Engineering | Prioritize DAT session, stream lifecycle, Mock Device Kit tests                       |
| Docs        | Update [PRODUCTION_CLIENT_SPEC.md](../05-architecture/PRODUCTION_CLIENT_SPEC.md) v0.3 |
| Pilot       | Log glasses firmware + phone model; drop IFP checklist as primary                     |
| Benchmarks  | RTX 5070 still sizes **cloud** ASR/CV; glasses do not run 7B LLM                      |

## References

- [Meta Wearables DAT](https://wearables.developer.meta.com/docs/develop/)
- [MDK Android testing (Mock Device Kit)](https://wearables.developer.meta.com/docs/develop/dat/testing-mdk-android/)
- [ADR-0008](ADR-0008-d-proc-hybrid-central-ml.md)
