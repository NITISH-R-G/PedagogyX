package com.pedagogyx.capture.dat

import androidx.test.ext.junit.runners.AndroidJUnit4
import com.pedagogyx.capture.dat.testing.MockDeviceKitTestHelpers
import com.pedagogyx.capture.dat.testing.PedagogyXCaptureTestCase
import org.junit.Assume.assumeTrue
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class PhotoCaptureInstrumentedTest : PedagogyXCaptureTestCase() {

    @Test
    fun testPhotoCapture() {
        assumeTrue(
            "Add androidTest/assets/test_image.png",
            MockDeviceKitTestHelpers.assetExists("test_image.png"),
        )

        val device = mockDeviceKit.pairRaybanMeta()
        MockDeviceKitTestHelpers.prepareForStreaming(mockDeviceKit, device)

        val mockCameraKit = MockDeviceKitTestHelpers.cameraKit(device)
        mockCameraKit.setCapturedImage(MockDeviceKitTestHelpers.getAssetUri("test_image.png"))

        scenarioRule.scenario.onActivity { activity ->
            activity.updateStreamState("CAPTURE_IMAGE_SET")
        }

        // Assert capture results when StreamSession.capturePhoto() is integrated.
    }
}
