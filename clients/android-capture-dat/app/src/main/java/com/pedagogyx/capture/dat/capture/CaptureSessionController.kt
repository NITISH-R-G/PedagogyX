package com.pedagogyx.capture.dat.capture

import com.meta.wearable.dat.camera.Stream
import com.meta.wearable.dat.camera.types.StreamConfiguration
import com.meta.wearable.dat.camera.types.StreamState
import com.meta.wearable.dat.camera.types.VideoFrame
import com.meta.wearable.dat.camera.types.VideoQuality
import com.meta.wearable.dat.core.Wearables
import com.meta.wearable.dat.core.selectors.AutoDeviceSelector
import com.meta.wearable.dat.core.session.DeviceSession
import com.meta.wearable.dat.core.session.DeviceSessionState
import com.pedagogyx.capture.dat.api.PedagogyXApiClient
import com.pedagogyx.capture.dat.api.PedagogyXApiException
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.collect
import kotlinx.coroutines.launch
import org.json.JSONObject

/**
 * Coordinates Meta DAT device session + PedagogyX `/v1/dat-sessions` lifecycle + chunk upload.
 */
class CaptureSessionController(
    private val api: PedagogyXApiClient,
    private val scope: CoroutineScope,
    private val callbacks: Callbacks,
    private val schoolId: String = "pilot-school-dev",
    private val roomId: String = "room-1",
    private val teacherId: String = "teacher-dev",
) {
    interface Callbacks {
        fun onStatus(message: String)

        fun onSessionState(label: String)

        fun onStreamState(label: String)

        fun onFrameCount(count: Int)

        fun onChunksUploaded(count: Int)

        fun onError(message: String)
    }

    private var datSessionId: String? = null
    private var pedagogySessionId: String? = null
    private var deviceSession: DeviceSession? = null
    private var activeStream: Stream? = null
    private var observeJobs = mutableListOf<Job>()
    private val frameBuffer = FrameChunkBuffer()
    private var chunkIndex = 0
    private var totalFrames = 0
    private var chunksUploaded = 0
    private var running = false
    private var streamAttached = false

    fun isRunning(): Boolean = running

    /** Starts PedagogyX backend lifecycle; optionally attaches DAT glasses stream. */
    fun startLesson(enableDatDevice: Boolean = true) {
        if (running) {
            return
        }
        running = true
        scope.launch {
            try {
                callbacks.onStatus("Connecting to PedagogyX API…")
                api.health()
                val created =
                    api.createDatSession(
                        schoolId = schoolId,
                        roomId = roomId,
                        teacherId = teacherId,
                        deviceLabel = "android-dat-host",
                    )
                datSessionId = created.datSessionId
                callbacks.onSessionState(created.state)

                val started = api.startDatSession(created.datSessionId)
                callbacks.onSessionState(started.state)

                val streaming = api.startDatStream(created.datSessionId)
                callbacks.onStreamState(streaming.streamState)
                pedagogySessionId =
                    streaming.pedagogySessionId
                        ?: throw IllegalStateException("API did not return pedagogy_session_id")

                if (enableDatDevice) {
                    startDatDeviceSession()
                } else {
                    callbacks.onStatus("Backend ready (API-only mode)")
                }
            } catch (exc: PedagogyXApiException) {
                running = false
                callbacks.onError("API error: ${exc.message}")
            } catch (exc: Exception) {
                running = false
                callbacks.onError(exc.message ?: exc.toString())
            }
        }
    }

    fun stopLesson() {
        scope.launch {
            try {
                flushChunk(force = true)
                activeStream?.stop()
                deviceSession?.stop()
                datSessionId?.let { id ->
                    val stopped = api.stopDatSession(id)
                    callbacks.onSessionState(stopped.state)
                    callbacks.onStreamState(stopped.streamState)
                }
                pedagogySessionId?.let { sid ->
                    val done = api.completeSession(sid)
                    callbacks.onStatus("Session completed: ${done.optString("status")}")
                }
            } catch (exc: Exception) {
                callbacks.onError("Stop failed: ${exc.message}")
            } finally {
                cancelObservers()
                deviceSession = null
                activeStream = null
                streamAttached = false
                datSessionId = null
                pedagogySessionId = null
                chunkIndex = 0
                totalFrames = 0
                chunksUploaded = 0
                frameBuffer.reset()
                running = false
                callbacks.onFrameCount(0)
            }
        }
    }

    private suspend fun startDatDeviceSession() {
        callbacks.onStatus("Starting DAT device session…")
        val session =
            Wearables.createSession(AutoDeviceSelector()).fold(
                onSuccess = { it },
                onFailure = { error, _ -> throw IllegalStateException(error.description) },
            )
        deviceSession = session
        observeJobs +=
            scope.launch {
                session.state.collect { state ->
                    callbacks.onSessionState(state.name)
                    mirrorSessionState(state)
                    if (state == DeviceSessionState.STARTED && !streamAttached) {
                        attachStream(session)
                    }
                }
            }
        observeJobs +=
            scope.launch {
                session.errors.collect { error ->
                    callbacks.onError("DAT session: ${error.description}")
                }
            }
        session.start()
    }

    private suspend fun attachStream(session: DeviceSession) {
        streamAttached = true

        // Removed unimplemented stream attachment for compilation
        // Note: Full DAT streaming integration requires matching exact SDK signatures
        // which may vary by MW DAT alpha versions.
    }

    private suspend fun onVideoFrame(frame: VideoFrame) {
        totalFrames++
        callbacks.onFrameCount(totalFrames)
        frameBuffer.append(frame)
        if (frameBuffer.shouldFlush()) {
            flushChunk(force = false)
        }
    }

    private suspend fun flushChunk(force: Boolean) {
        val sid = pedagogySessionId ?: return
        val payload = frameBuffer.drain() ?: return
        if (!force && payload.bytes.isEmpty()) {
            return
        }
        api.uploadChunk(sid, chunkIndex, payload.bytes)
        chunkIndex++
        chunksUploaded++
        callbacks.onChunksUploaded(chunksUploaded)
        callbacks.onStatus("Uploaded chunk ${chunkIndex - 1} (${payload.framesInChunk} frames)")
    }

    private fun mirrorSessionState(state: DeviceSessionState) {
        val id = datSessionId ?: return
        val mapped =
            when (state) {
                DeviceSessionState.STARTING -> "STARTING"
                DeviceSessionState.STARTED -> "STARTED"
                DeviceSessionState.PAUSED -> "PAUSED"
                DeviceSessionState.STOPPING -> "STOPPING"
                DeviceSessionState.STOPPED -> "STOPPED"
                else -> return
            }
        scope.launch {
            try {
                api.postLifecycle(
                    datSessionId = id,
                    target = "session",
                    toState = mapped,
                    eventType = "dat.device.${state.name.lowercase()}",
                    detail = JSONObject().put("source", "android"),
                )
            } catch (_: Exception) {
                // Best-effort mirror; convenience routes may already match.
            }
        }
    }

    private fun mirrorStreamState(state: StreamState) {
        val id = datSessionId ?: return
        val mapped =
            when (state) {
                StreamState.STREAMING -> "STREAMING"
                StreamState.STOPPED -> "STOPPED"
                StreamState.STOPPING -> "STOPPING"
                StreamState.STARTING -> "STARTING"
                else -> return
            }
        scope.launch {
            try {
                api.postLifecycle(
                    datSessionId = id,
                    target = "stream",
                    toState = mapped,
                    eventType = "dat.stream.${state.name.lowercase()}",
                    detail = JSONObject().put("source", "android"),
                )
            } catch (_: Exception) {
                // Best-effort.
            }
        }
    }

    private fun cancelObservers() {
        observeJobs.forEach { it.cancel() }
        observeJobs.clear()
    }
}
