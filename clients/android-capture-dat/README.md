# PedagogyX Android — Primary client (Meta Ray-Ban DAT)

**Production capture** runs on **Meta Ray-Ban smart glasses** via the Wearables Device Access Toolkit. This module is the **v1 host app** on the teacher’s phone (not the classroom smartboard).

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

| Path                                                  | Description                                      |
| ----------------------------------------------------- | ------------------------------------------------ |
| `app/src/androidTest/.../MockDeviceKitTestCase.kt`    | Base rule: permissions + `mockDeviceKit.reset()` |
| `app/src/androidTest/.../MockDeviceKitTestHelpers.kt` | `prepareForStreaming`, `getAssetUri`             |
| `CameraStreamingInstrumentedTest`                     | `setCameraFeed(test_video.mp4)`                  |
| `PhotoCaptureInstrumentedTest`                        | `setCapturedImage(test_image.png)`               |

## Run tests

```bash
cd clients/android-capture-dat
./gradlew :app:connectedDebugAndroidTest
```

Add assets first (see `app/src/androidTest/assets/README.md`).

## Cursor — full DAT API reference (@Docs)

Add Meta’s indexed API docs once per machine (IDE setting, not in git):

1. **Settings → Features → Docs → Add new doc**
2. URL: `https://wearables.developer.meta.com/llms.txt?full=true`
3. Name: **Wearables DAT SDK**
4. In Chat: **@Docs** → select **Wearables DAT SDK**

Details: [CURSOR_WEARABLES_DAT_DOCS.md](../../docs/05-architecture/CURSOR_WEARABLES_DAT_DOCS.md)

## Cursor / Meta AI skills (optional)

Install Meta DAT agent **skills** (integration patterns; complements @Docs above):

```bash
curl -sL https://raw.githubusercontent.com/facebook/meta-wearables-dat-android/main/install-skills.sh | bash -s -- cursor
```

Or from repo root:

```bash
./scripts/install-dat-skills.sh cursor
```

## Capture flow (implemented)

`CaptureActivity` + `CaptureSessionController`:

1. PedagogyX API: `POST /v1/dat-sessions` → `start` → `stream/start` (links upload session)
2. DAT: `Wearables.createSession` → `session.start()` → `addStream` → `videoStream` → chunked upload
3. Stop: flush chunks → `POST …/stop` → `POST /v1/sessions/{id}/complete`

**API base URL:** default `http://10.0.2.2:8080` (emulator). Override in `local.properties`:

```properties
pedagogyx.api.base.url=http://192.168.1.10:8080
```

Run backend: `make dev-up` from repo root.

**API-only button** exercises the server lifecycle without pairing glasses (useful on emulator without Meta AI).

## Next steps

- End-to-end instrumented test with Mock Device Kit + API on host network
- Photo capture → chunk or sidecar upload
