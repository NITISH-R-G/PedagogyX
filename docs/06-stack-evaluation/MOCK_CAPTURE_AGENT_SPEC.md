# Mock Capture Agent — Dev Spec (Pre-Implementation)

**Status:** Draft — implement **after G2** as `tools/mock-capture/` or script  
**Purpose:** Sprint 03 vertical slice testing without real smartboard hardware  
**Protocol:** [RFC-0002](../08-rfc-adr/RFC-0002-capture-agent-sync-protocol.md)

---

## Goals

- Upload **synthetic** 1-minute H.264 + AAC chunks to dev API/MinIO
- Simulate **edge delay** (WAN offline → burst forward)
- Produce session metadata matching production envelope

---

## Non-goals

- Real screen capture, MediaCodec, or WebRTC hot path
- Production signing / device attestation

---

## Inputs

| Asset      | Source                                                                                               |
| ---------- | ---------------------------------------------------------------------------------------------------- |
| Test video | `benchmarks/fixtures/lesson_45min_sample.mp4` (to add post-G2) or ffmpeg-generated color bars + tone |
| Test audio | Embedded in MP4 or separate WAV                                                                      |
| Config     | `mock-capture.yaml`: `school_id`, `room_id`, `teacher_id`, `edge_url`, `api_url`                     |

---

## Behavior

1. **Session start** — `POST /v1/sessions` → `session_id`, upload credentials
2. **Chunk loop** — for each 60 s segment:
   - Write local file with monotonic PTS (RFC-0002)
   - `PUT` resumable multipart to MinIO path `sessions/{id}/chunks/{n}.mp4`
   - Optional: sleep `edge_delay_ms` between chunks
3. **Session end** — `POST /v1/sessions/{id}/complete` → queue ASR job
4. **Failure injection** — flags: `--drop-chunk 3`, `--disk-full`, `--offline 10m`

---

## Acceptance (dev)

| Check                     | Expected                                        |
| ------------------------- | ----------------------------------------------- |
| 50 MB file lands in MinIO | S03-04                                          |
| worker-asr picks job      | transcript JSON in `benchmarks/results/` format |
| M-B smoke                 | preview talk ratio API &lt; 5 min on dev stack  |

---

## Implementation sketch (post-G2)

```text
tools/mock-capture/
  main.py          # CLI
  uploader.py      # S3 multipart
  fixtures/        # git-lfs or download script
```

Run against `docker compose -f infra/compose.dev.yaml up`.

---

## References

- [DOCKER_COMPOSE_PILOT_STACK.md](DOCKER_COMPOSE_PILOT_STACK.md) — dev profile
- [SPRINT_03_MVP_PREP.md](../09-agile/SPRINT_03_MVP_PREP.md)
