# RFC-0004 — DAT Session Bridge (Dev + Production)

| Field      | Value      |
| ---------- | ---------- |
| **Status** | Draft      |
| **Date**   | 2026-05-23 |

## Summary

PedagogyX exposes HTTP endpoints that mirror **Meta Wearables Device Access Toolkit (DAT)** session/stream lifecycle so:

1. **Dev:** `tools/dat-session-sim` can drive webcam → upload → ASR without smartboard hardware.
2. **Prod:** Future Android capture agent can forward DAT callbacks to the same API.

## States

**Device session:** `IDLE` → `STARTING` → `STARTED` ↔ `PAUSED` → `STOPPING` → `STOPPED`  
**Camera stream:** `STOPPED` → `STARTING` → `STREAMING` → `STOPPING` → `STOPPED`

On `STREAMING`, server creates/links `sessions.id` for cold-path chunk upload (RFC-0002).

## Endpoints

See [tools/dat-session-sim/README.md](../../tools/dat-session-sim/README.md).

## Android Mock Device Kit (no glasses)

Module: [clients/android-capture-dat](../../clients/android-capture-dat/README.md)

- `MockDeviceKitTestCase` — permissions + reset
- `prepareForStreaming` / `getAssetUri` helpers
- Instrumentation: `testCameraStreaming`, `testPhotoCapture`

## References

- Meta DAT: DeviceSession, Stream — [wearables.developer.meta.com](https://wearables.developer.meta.com/)
- [MDK Android testing guide](https://wearables.developer.meta.com/docs/develop/dat/testing-mdk-android/)
- [RFC-0002](RFC-0002-capture-agent-sync-protocol.md)
