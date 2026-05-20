# RFC-0002 — Acceptance Record (S02-07)

**RFC:** [RFC-0002-capture-agent-sync-protocol.md](RFC-0002-capture-agent-sync-protocol.md)  
**Status:** Pending sign-off  
**Implementation:** Blocked until G2 + this record is **Accepted**

---

## Review summary

| Topic        | Decision (draft)                        |
| ------------ | --------------------------------------- |
| Master clock | Microphone audio                        |
| Hot path     | WebRTC/RTSP via MediaMTX (480p + 1 cam) |
| Cold path    | 1-minute MP4 segments, resumable upload |
| Local buffer | 2 GB rolling (RFC-0002)                 |
| Drift        | PTS cross-correlation at ingest         |

---

## Open questions (must resolve before Accept)

| #   | Question                                            | Owner  | Resolution                  |
| --- | --------------------------------------------------- | ------ | --------------------------- |
| 1   | Max drift tolerance (ms) for talk-ratio alignment?  | ML     |                             |
| 2   | MediaCodec PTS reliability on Android B profile?    | Client | Pilot matrix                |
| 3   | Edge vs direct-to-cloud when school has stable WAN? | Arch   | Hybrid default per ADR-0008 |

---

## Sign-off

| Role                  | Name | Date | Status  |
| --------------------- | ---- | ---- | ------- |
| Founder               |      |      | Pending |
| Technical lead / arch |      |      | Pending |

**When Accepted:**

1. Change RFC-0002 header `Status` to **Accepted**.
2. Update this file statuses to **Accepted** with dates.
3. Mark S02-07 🟢 in [SPRINT_02_PLAN.md](../09-agile/SPRINT_02_PLAN.md).

---

## References

- [MOCK_CAPTURE_AGENT_SPEC.md](../06-stack-evaluation/MOCK_CAPTURE_AGENT_SPEC.md)
- [PRODUCTION_CLIENT_SPEC.md](../05-architecture/PRODUCTION_CLIENT_SPEC.md)
