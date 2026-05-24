package com.pedagogyx.capture.dat

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch
import com.meta.wearable.dat.core.Wearables
import com.meta.wearable.dat.core.types.Permission
import com.meta.wearable.dat.core.types.PermissionStatus
import com.pedagogyx.capture.dat.api.PedagogyXApiClient
import com.pedagogyx.capture.dat.capture.CaptureSessionController
import com.pedagogyx.capture.dat.databinding.ActivityCaptureBinding
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlin.coroutines.resume
import kotlin.coroutines.suspendCoroutine

/**
 * Host activity: Meta DAT stream + PedagogyX API lifecycle and chunk upload.
 */
class CaptureActivity : AppCompatActivity(), CaptureSessionController.Callbacks {

    private lateinit var binding: ActivityCaptureBinding
    private lateinit var controller: CaptureSessionController
    private val permissionMutex = Mutex()
    private var permissionContinuation: ((PermissionStatus) -> Unit)? = null

    private val permissionLauncher =
        registerForActivityResult(Wearables.RequestPermissionContract()) { result ->
            permissionContinuation?.invoke(result)
            permissionContinuation = null
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCaptureBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val apiBase = BuildConfig.PEDAGOGYX_API_BASE_URL
        controller =
            CaptureSessionController(
                api = PedagogyXApiClient(apiBase),
                scope = lifecycleScope,
                callbacks = this,
                schoolId = BuildConfig.PEDAGOGYX_SCHOOL_ID,
                roomId = BuildConfig.PEDAGOGYX_ROOM_ID,
                teacherId = BuildConfig.PEDAGOGYX_TEACHER_ID,
            )

        binding.startButton.setOnClickListener {
            lifecycleScope.launch {
                binding.startButton.isEnabled = false
                if (!ensureCameraPermission()) {
                    onError("Camera permission required for DAT streaming")
                    binding.startButton.isEnabled = true
                    return@launch
                }
                controller.startLesson(enableDatDevice = true)
                binding.stopButton.isEnabled = true
            }
        }

        binding.stopButton.setOnClickListener {
            binding.stopButton.isEnabled = false
            controller.stopLesson()
            binding.startButton.isEnabled = true
        }

        binding.apiOnlyButton.setOnClickListener {
            lifecycleScope.launch {
                binding.apiOnlyButton.isEnabled = false
                controller.startLesson(enableDatDevice = false)
                binding.stopButton.isEnabled = true
            }
        }

        updateUiIdle()
    }

    override fun onDestroy() {
        if (controller.isRunning()) {
            controller.stopLesson()
        }
        super.onDestroy()
    }

    private suspend fun ensureCameraPermission(): Boolean {
        var status = Wearables.checkPermissionStatus(Permission.CAMERA)
        if (status == PermissionStatus.Granted) {
            return true
        }
        status = requestWearablesPermission(Permission.CAMERA)
        return status == PermissionStatus.Granted
    }

    private suspend fun requestWearablesPermission(permission: Permission): PermissionStatus =
        permissionMutex.withLock {
            suspendCoroutine { cont ->
                permissionContinuation = { cont.resume(it) }
                permissionLauncher.launch(permission)
            }
        }

    private fun updateUiIdle() {
        binding.stopButton.isEnabled = false
        binding.startButton.isEnabled = true
        binding.apiOnlyButton.isEnabled = true
    }

    override fun onStatus(message: String) {
        runOnUiThread { binding.statusText.text = message }
    }

    override fun onSessionState(label: String) {
        runOnUiThread { binding.sessionStateText.text = getString(R.string.session_state_format, label) }
    }

    override fun onStreamState(label: String) {
        runOnUiThread { binding.streamStateText.text = getString(R.string.stream_state_format, label) }
    }

    override fun onFrameCount(count: Int) {
        runOnUiThread { binding.frameCountText.text = getString(R.string.frame_count_format, count) }
    }

    override fun onChunksUploaded(count: Int) {
        runOnUiThread { binding.chunksText.text = getString(R.string.chunks_uploaded_format, count) }
    }

    override fun onError(message: String) {
        runOnUiThread {
            binding.statusText.text = message
            binding.startButton.isEnabled = true
            binding.apiOnlyButton.isEnabled = true
            binding.stopButton.isEnabled = false
        }
    }

    // Used by instrumentation tests to drive UI state without full DAT registration.
    fun updateStreamState(label: String) = onStreamState(label)

    fun updateSessionState(label: String) = onSessionState(label)

    fun updateFrameCount(count: Int) = onFrameCount(count)
}
