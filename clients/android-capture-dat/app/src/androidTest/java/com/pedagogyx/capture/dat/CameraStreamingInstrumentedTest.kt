package com.pedagogyx.capture.dat

import androidx.test.ext.junit.runners.AndroidJUnit4
import com.pedagogyx.capture.dat.testing.MockDeviceKitTestHelpers
import com.pedagogyx.capture.dat.testing.PedagogyXCaptureTestCase
import org.junit.Assume.assumeTrue
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Mock camera streaming without physical Meta glasses.
 *
 * Add `androidTest/assets/test_video.mp4` — Meta recommends H.265/HEVC for Android mock feed.
 * Transcode example:
 * `ffmpeg -i input.mp4 -c:v libx265 -tag:v hvc1 -vf scale=540:960 test_video.mp4`
 */
@RunWith(AndroidJUnit4::class)
class CameraStreamingInstrumentedTest : PedagogyXCaptureTestCase() {

    @Test
    fun testCameraStreaming() {
        assumeTrue(
            "Add androidTest/assets/test_video.mp4 (H.265) — see README",
            MockDeviceKitTestHelpers.assetExists("test_video.mp4"),
        )

        val device = mockDeviceKit.pairRaybanMeta()
        MockDeviceKitTestHelpers.prepareForStreaming(mockDeviceKit, device)

        val mockCameraKit = MockDeviceKitTestHelpers.cameraKit(device)
        mockCameraKit.setCameraFeed(MockDeviceKitTestHelpers.getAssetUri("test_video.mp4"))

        scenarioRule.scenario.onActivity { activity ->
            activity.updateStreamState("MOCK_FEED_SET")
            activity.updateSessionState("STREAMING")
        }

        // Hook StreamSession / videoStream assertions here when Wearables session is wired.
    }
}
