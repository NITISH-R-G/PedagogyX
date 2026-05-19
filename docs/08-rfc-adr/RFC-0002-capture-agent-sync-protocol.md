# RFC-0002: Capture Agent & Sync Protocol

| Field | Value |
|-------|-------|
| **Status** | Draft |
| **Authors** | PedagogyX Architecture (Agent) |
| **Created** | 2026-05-19 |

## Summary
Defines the synchronization protocol and architecture for the PedagogyX Capture Agent across Android and Windows thin clients. This protocol guarantees that screen, microphone, and multiple camera streams are time-aligned for both real-time streaming and offline batch uploads.

## Motivation
Founder decision (D-04, D-08, D-09) mandates real-time processing of multi-camera and screen capture data. Since clients are low-end devices (ADR-0007), we must perform lightweight capture and rely on a robust synchronization protocol before transmitting to central OSS inference servers.

## Proposal

### Time Alignment & Master Clock
1. **Master Clock:** The local microphone audio stream will serve as the master clock.
2. **Timestamps:** Every frame (video or screen) and audio chunk will be tagged with a precise relative timestamp from the start of the recording session.
3. **Session Genesis:** An initial NTP sync establishes absolute wall-clock time for the session start.

### Streaming Protocol
1. **Real-time (Hot Path):** Media MTX (WebRTC/RTSP) will be used for live ingest. The capture agent pushes low-latency 480p streams (audio + 1 cam) prioritizing liveness over quality.
2. **Batch (Cold Path):** High-quality chunks (720p/1080p, H.264/H.265 encoded) are buffered to disk locally.
3. **Chunking Strategy:** Video/Audio files are saved locally in 1-minute segmented MP4 chunks and uploaded concurrently via resumable HTTP/S3 multipart upload to the central MinIO store.

### Drift Compensation
To handle clock drift or dropped frames on low-end hardware:
- The agent will embed presentation timestamps (PTS) into the encoded streams.
- The central ingestion service cross-correlates audio timestamps with video PTS to align micro-batches.

## Failure Modes & Mitigation
- **Network Loss:** If WebRTC connection drops, the agent stops the hot path immediately but continues writing chunks to the local disk buffer.
- **Disk Full:** A rolling buffer strategy (max 2GB) is used. Once full, the agent pauses recording, alerts the user, or automatically discards the oldest chunks (configurable by policy).

## Open Questions
- Can Android's MediaCodec reliably embed PTS across varied OEM devices?
- What is the acceptable maximum drift tolerance (in ms) for accurate engagement detection?

## Decision
Pending architecture review.
