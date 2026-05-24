package com.pedagogyx.capture.dat.testing

import android.net.Uri
import androidx.test.platform.app.InstrumentationRegistry
import com.meta.wearable.dat.mockdevice.api.MockDeviceKitInterface
import com.meta.wearable.dat.mockdevice.api.MockRaybanMeta
import com.meta.wearable.dat.mockdevice.api.camera.MockCameraKit
import java.io.File

/**
 * Helpers referenced by Meta's MDK testing guide (prepareForStreaming, getAssetUri).
 */
object MockDeviceKitTestHelpers {

    /**
     * Powers on mock glasses and unfolds — required before camera feed / capture tests.
     */
    fun prepareForStreaming(mockDeviceKit: MockDeviceKitInterface, device: MockRaybanMeta) {
        mockDeviceKit.enable()
        device.powerOn()
        device.unfold()
    }

    /**
     * Copies an androidTest asset to cache and returns a file [Uri] for Mock Camera Kit.
     */
    fun getAssetUri(assetName: String): Uri {
        val testContext = InstrumentationRegistry.getInstrumentation().context
        val outFile = File(testContext.cacheDir, assetName)
        testContext.assets.open(assetName).use { input ->
            outFile.outputStream().use { output -> input.copyTo(output) }
        }
        return Uri.fromFile(outFile)
    }

    fun assetExists(assetName: String): Boolean {
        return try {
            InstrumentationRegistry.getInstrumentation().context.assets.open(assetName).close()
            true
        } catch (_: Exception) {
            false
        }
    }

    /** MDK 0.7+: `device.services.camera`. Older guides use `device.getCameraKit()`. */
    fun cameraKit(device: MockRaybanMeta): MockCameraKit {
        return device.services.camera
    }
}
