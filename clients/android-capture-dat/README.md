# PedagogyX Android — Meta Wearables DAT + Mock Device Kit

Instrumentation tests for **camera streaming** and **photo capture** without physical Meta glasses, following:

https://wearables.developer.meta.com/docs/develop/dat/testing-mdk-android/

Server-side DAT lifecycle (PedagogyX API): [RFC-0004](../../docs/08-rfc-adr/RFC-0004-dat-session-bridge.md) · `tools/dat-session-sim/`

## Prerequisites

1. **GitHub Packages token** for `com.meta.wearable` artifacts ([SDK setup](https://wearables.developer.meta.com/docs/getting-started-toolkit/#sdk-for-android-setup)):
   - `export GITHUB_TOKEN=ghp_...` (classic token, `read:packages`)
   - or `github_token=...` in `clients/android-capture-dat/local.properties`

2. Android Studio / SDK 35, JDK 17

3. Emulator or device API 29+

## Project layout

| Path | Description |
| ---- | ----------- |
| `app/src/androidTest/.../MockDeviceKitTestCase.kt` | Base rule: permissions + `mockDeviceKit.reset()` |
| `app/src/androidTest/.../MockDeviceKitTestHelpers.kt` | `prepareForStreaming`, `getAssetUri` |
| `CameraStreamingInstrumentedTest` | `setCameraFeed(test_video.mp4)` |
| `PhotoCaptureInstrumentedTest` | `setCapturedImage(test_image.png)` |

## Run tests

```bash
cd clients/android-capture-dat
./gradlew :app:connectedDebugAndroidTest
```

Add assets first (see `app/src/androidTest/assets/README.md`).

## Cursor / Meta AI skills (optional)

Install Meta DAT agent skills into Cursor from the upstream repo:

```bash
curl -sL https://raw.githubusercontent.com/facebook/meta-wearables-dat-android/main/install-skills.sh | bash -s -- cursor
```

Or from repo root:

```bash
./scripts/install-dat-skills.sh cursor
```

## Next steps

- Wire `Wearables.startStreamSession` + `videoStream` in `CaptureActivity`
- Forward lifecycle to PedagogyX `POST /v1/dat-sessions/*` (see backend running via `make dev-up`)
