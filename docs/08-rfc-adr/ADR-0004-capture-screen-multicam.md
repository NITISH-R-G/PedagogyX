# ADR-0004: Screen + Microphone + Multi-Camera Capture

| Field      | Value      |
| ---------- | ---------- |
| **Status** | Accepted   |
| **Date**   | 2026-05-19 |

## Context

Founder specified **screen recording + mic** and **multi-cam** for MVP—not phone-only upload.

## Decision

Standard session ingest comprises **synchronized streams**:

| Stream ID        | Source                           | Required v1 |
| ---------------- | -------------------------------- | ----------- |
| `screen`         | Teacher device display capture   | Yes         |
| `audio_mic`      | Classroom / teacher microphone   | Yes         |
| `cam_room_1`     | Room wide shot                   | Yes         |
| `cam_room_2`     | Second angle (board or students) | Yes         |
| `cam_optional_n` | Additional RTSP/USB              | Optional    |

**Clock:** Single session timeline; NTP-aligned timestamps; drift correction in fusion service.

## Client delivery options (evaluate in RFC-0002)

1. **Electron/Tauri desktop agent** (recommended for reliable screen + multi-USB cam)
2. **Browser** screen share + separate IP cam apps (fragile for schools)
3. **Edge appliance** (future) for fixed classrooms

**[ASSUMPTION]** v1 ships **desktop capture agent** for Windows + Android tablet for mobile cam proxy.

## Consequences

- IT deployment guide required (firewall, USB bandwidth)
- Sync service is **critical path** engineering
- Storage multiplies by stream count (~3–5× vs single video)
