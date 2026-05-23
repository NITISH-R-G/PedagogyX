package com.pedagogyx.capture.dat.capture

import com.meta.wearable.dat.camera.types.VideoFrame
import java.io.ByteArrayOutputStream
import java.nio.ByteBuffer

/**
 * Batches DAT [VideoFrame] payloads into upload-sized chunks for PedagogyX API.
 */
class FrameChunkBuffer(
    private val maxBytes: Int = 256 * 1024,
) {
    private val buffer = ByteArrayOutputStream()
    private var frameCount = 0

    fun append(frame: VideoFrame) {
        if (frame.isCodecConfig) {
            return
        }
        frameCount++
        val dup = frame.buffer.duplicate()
        dup.rewind()
        val bytes = ByteArray(dup.remaining())
        dup.get(bytes)
        buffer.write(bytes)
    }

    fun shouldFlush(): Boolean = buffer.size() >= maxBytes

    fun drain(): ChunkPayload? {
        if (buffer.size() == 0) {
            return null
        }
        val bytes = buffer.toByteArray()
        buffer.reset()
        val count = frameCount
        frameCount = 0
        return ChunkPayload(bytes, count)
    }

    fun reset() {
        buffer.reset()
        frameCount = 0
    }
}

data class ChunkPayload(val bytes: ByteArray, val framesInChunk: Int)
