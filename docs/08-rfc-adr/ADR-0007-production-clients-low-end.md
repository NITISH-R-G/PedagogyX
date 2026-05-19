# ADR-0007: Production on Android & Low-End Windows Smartboards

| Field | Value |
|-------|-------|
| **Status** | Accepted (founder-directed) |
| **Date** | 2026-05-19 |

## Context

Production does **not** run on developer GPU hardware. Classrooms use:

- **Android** (tablets / smart panels / boxes)
- **Windows smartboards** — **low-end** CPU/RAM (typical embedded PC: Celeron, 4–8 GB RAM, Intel UHD)

All heavy ML runs **off-device** on central OSS infrastructure (spec TBD).

## Decision

### Client responsibilities (thin client)

| Task | Android | Windows smartboard |
|------|---------|-------------------|
| Screen capture | MediaProjection API | DXGI / GDI capture |
| Microphone | AudioRecord | WASAPI |
| Camera(s) | Camera2 (0–1 USB/built-in) | DirectShow / Media Foundation |
| Encode | **MediaCodec** H.264 (HW if available) | Media Foundation / FFmpeg DLL |
| Buffer on network loss | Local SQLite + file chunks | Same |
| Upload | HTTPS resumable to central API | Same |
| On-device ML | **Optional:** Silero VAD only (CPU, &lt;50 MB) | Same |
| On-device ASR/CV/LLM | **Forbidden** in v1 | **Forbidden** |

### What low-end hardware cannot do

- Multi-stream 1080p real-time CV
- Whisper medium/large
- Any 7B LLM
- TensorRT / CUDA (most boards have no discrete GPU)

### Multi-cam strategy (revised)

| Stream | Source on low-end client |
|--------|--------------------------|
| Screen | Yes (primary) |
| Mic | Yes |
| Cam 1 | Yes if USB/built-in and CPU can encode 480p@15fps |
| Cam 2+ | **[ASSUMPTION]** IP cameras → **ingest direct to central server** (RTSP), not through smartboard |

### Real-time analytics

- **Live metrics** computed on **central server** from **uploaded stream chunks** (WebRTC/SRT) or **short-interval chunk upload** (every 10–30s)
- Smartboard shows **WebView dashboard** or minimal native UI polling server
- If uplink poor: **store-and-forward**; live dashboard degrades to “uploading…”

### Client technology (OSS-first)

| Platform | Recommended stack |
|----------|-------------------|
| **Android** | **Kotlin** + Jetpack + MediaCodec + WorkManager upload |
| **Windows** | **Tauri 2** (Rust + WebView2) *or* **.NET 8** WinUI — pick one in RFC-0002 |
| **Shared logic** | Rust `capture-core` crate (FFI to Kotlin + Tauri) **[HYPOTHESIS]** |

**Flutter** alternative: single codebase for Android + Windows desktop — evaluate in RFC-0002.

### Central processing (production)

| Tier | Hardware | When |
|------|----------|------|
| **P0 pilot** | India VPS **CPU-only** (slow batch) | Zero GPU budget |
| **P1 recommended** | 1× datacenter GPU per ~8–16 concurrent analyses | Matches dev benchmarks from RTX 5070 |
| **P2** | Autoscale GPU pool (still OSS: vLLM, faster-whisper) | Scale |

**Not** RTX 5070 in classroom.

## Consequences

- Internet dependency per session (or LAN to school mini-server **[optional future]**)
- Minimum smartboard spec doc required ([PRODUCTION_CLIENT_SPEC.md](../05-architecture/PRODUCTION_CLIENT_SPEC.md))
- Dev team uses **5070** to validate server-side model configs only

## Open question (founder)

**D-PROC:** Where does central processing run?

- A) PedagogyX managed cloud (India region, rented GPU)
- B) District-owned server room
- C) Hybrid

## Validation

- Test on reference low-end device list (2 Android SoCs + 1 Celeron smartboard PC)
