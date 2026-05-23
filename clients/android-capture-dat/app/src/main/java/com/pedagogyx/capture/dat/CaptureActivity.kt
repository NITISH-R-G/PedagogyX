package com.pedagogyx.capture.dat

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.pedagogyx.capture.dat.databinding.ActivityCaptureBinding

/**
 * Minimal host activity for Mock Device Kit instrumentation tests.
 * Production capture UI will observe [StreamSession] state here.
 */
class CaptureActivity : AppCompatActivity() {

    private lateinit var binding: ActivityCaptureBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCaptureBinding.inflate(layoutInflater)
        setContentView(binding.root)
    }

    fun updateStreamState(label: String) {
        binding.streamStateText.text = getString(R.string.stream_state_format, label)
    }

    fun updateSessionState(label: String) {
        binding.sessionStateText.text = "Session: $label"
    }

    fun updateFrameCount(count: Int) {
        binding.frameCountText.text = "Frames: $count"
    }
}
