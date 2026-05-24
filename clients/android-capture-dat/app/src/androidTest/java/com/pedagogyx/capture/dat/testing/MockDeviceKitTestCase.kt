package com.pedagogyx.capture.dat.testing

import android.content.Context
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.platform.app.InstrumentationRegistry
import com.meta.wearable.dat.mockdevice.MockDeviceKit
import com.meta.wearable.dat.mockdevice.api.MockDeviceKitInterface
import com.pedagogyx.capture.dat.CaptureActivity
import org.junit.After
import org.junit.Before
import org.junit.Rule

/**
 * Base instrumentation test per Meta Wearables MDK guide:
 * https://wearables.developer.meta.com/docs/develop/dat/testing-mdk-android/
 */
open class MockDeviceKitTestCase<T : Any>(
    private val activityClass: Class<T>,
) {

    @get:Rule
    val scenarioRule = ActivityScenarioRule(activityClass)

    protected lateinit var mockDeviceKit: MockDeviceKitInterface
    protected lateinit var targetContext: Context

    @Before
    open fun setUp() {
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        targetContext = instrumentation.targetContext
        mockDeviceKit = MockDeviceKit.getInstance(targetContext)
        grantRuntimePermissions()
    }

    @After
    open fun tearDown() {
        mockDeviceKit.reset()
    }

    private fun grantRuntimePermissions() {
        val packageName = targetContext.packageName
        val shell = InstrumentationRegistry.getInstrumentation().uiAutomation
        shell.executeShellCommand("pm grant $packageName android.permission.BLUETOOTH_CONNECT")
        shell.executeShellCommand("pm grant $packageName android.permission.CAMERA")
    }
}

/** Convenience base for this module's default activity. */
open class PedagogyXCaptureTestCase : MockDeviceKitTestCase<CaptureActivity>(CaptureActivity::class.java)
