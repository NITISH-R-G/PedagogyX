# Plan Change — Meta Ray-Ban as Primary Client

**Recorded:** 2026-05-23  
**Decision:** PedagogyX **v1 runs on Meta Ray-Ban smart glasses** (via DAT + Android companion app), not smartboards as the primary capture surface.

## What changed

| Before (2026-05-19)                                | After (2026-05-23)                                                                          |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Primary: low-end **Android / Windows smartboards** | Primary: **Meta Ray-Ban Meta** + **phone host app**                                         |
| Capture: screen + mic + multi-cam in room          | Capture: **glasses POV video + mic** (DAT)                                                  |
| Client spike: future                               | Client: [clients/android-capture-dat](../../clients/android-capture-dat/) + Mock Device Kit |

## What did **not** change

- **India-first**, school/university buyer, free pilot (D-02, D-05, D-10)
- **Hybrid D-PROC** (ADR-0008), OSS stack, RTX 5070 dev GPU
- **Teacher pedagogy** focus (D-PEDAGOGY), metrics M-A / M-B / M-C (D-20)
- **G2 legal** before production student/teacher data

## Founder answers to refresh (suggested)

| ID           | Old                 | New (plan change)                                              |
| ------------ | ------------------- | -------------------------------------------------------------- |
| **D-08**     | Screen + mic        | **Glasses camera + mic** (phone may add screen later)          |
| **D-09**     | Multi-cam classroom | **Single POV stream** (glasses); room cams deferred            |
| **D-CLIENT** | All low-end boards  | **Meta Ray-Ban + Android DAT host** (boards optional Phase 1b) |
| **D-DEV**    | IFP checklist       | **Glasses + phone** make/model, DAT firmware                   |

Canonical ADR: [ADR-0009](../08-rfc-adr/ADR-0009-meta-rayban-primary-client.md).

## Engineering priority (next)

1. Finish DAT `StreamSession` in `CaptureActivity` (live frames → buffer → upload)
2. Wire lifecycle to `/v1/dat-sessions` on PedagogyX API
3. Pilot with Mock Device Kit → real glasses
4. Revisit smartboard clients only if a school cannot use wearables
