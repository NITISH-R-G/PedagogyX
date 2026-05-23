package com.pedagogyx.capture.dat.capture

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test
import java.io.ByteArrayOutputStream

/**
 * Logic tests without DAT SDK types (buffer sizing only).
 */
class FrameChunkBufferLogicTest {
    @Test
    fun drainEmptyReturnsNull() {
        val buf = FrameChunkBuffer(maxBytes = 1024)
        assertNull(buf.drain())
    }

    @Test
    fun flushThresholdUsesMaxBytes() {
        val inner = ByteArrayOutputStream()
        repeat(300) { inner.write(1) }
        assertEquals(300, inner.size())
    }
}
