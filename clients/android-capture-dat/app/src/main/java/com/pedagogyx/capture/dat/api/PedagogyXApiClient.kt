package com.pedagogyx.capture.dat.api

import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.util.concurrent.TimeUnit

/**
 * HTTP client for PedagogyX DAT bridge + chunk upload.
 * Mirrors [tools/dat-session-sim/dat_session_cli.py].
 */
class PedagogyXApiClient(
    private val baseUrl: String,
    client: OkHttpClient? = null,
) {
    private val http =
        client
            ?: OkHttpClient.Builder()
                .connectTimeout(15, TimeUnit.SECONDS)
                .readTimeout(120, TimeUnit.SECONDS)
                .writeTimeout(120, TimeUnit.SECONDS)
                .build()

    private val root = baseUrl.trimEnd('/')

    fun health(): JSONObject = getJson("$root/health")

    fun createDatSession(
        schoolId: String,
        roomId: String?,
        teacherId: String?,
        deviceLabel: String?,
    ): DatSessionResponse {
        val body =
            JSONObject()
                .put("school_id", schoolId)
                .put("room_id", roomId)
                .put("teacher_id", teacherId)
                .put("device_label", deviceLabel)
        return DatSessionResponse.from(postJson("$root/v1/dat-sessions", body))
    }

    fun startDatSession(datSessionId: String): DatSessionResponse =
        DatSessionResponse.from(postJson("$root/v1/dat-sessions/$datSessionId/start", JSONObject()))

    fun startDatStream(datSessionId: String): DatSessionResponse =
        DatSessionResponse.from(postJson("$root/v1/dat-sessions/$datSessionId/stream/start", JSONObject()))

    fun stopDatSession(datSessionId: String): DatSessionResponse =
        DatSessionResponse.from(postJson("$root/v1/dat-sessions/$datSessionId/stop", JSONObject()))

    fun postLifecycle(
        datSessionId: String,
        target: String,
        toState: String,
        eventType: String,
        detail: JSONObject = JSONObject(),
    ): DatSessionResponse {
        val body =
            JSONObject()
                .put("target", target)
                .put("to_state", toState)
                .put("event_type", eventType)
                .put("detail", detail)
        return DatSessionResponse.from(
            postJson("$root/v1/dat-sessions/$datSessionId/lifecycle", body),
        )
    }

    fun uploadChunk(
        pedagogySessionId: String,
        chunkIndex: Int,
        bytes: ByteArray,
        contentType: String = "application/octet-stream",
        filename: String = "chunk.bin",
    ): JSONObject {
        val fileBody = bytes.toRequestBody(contentType.toMediaType())
        val multipart =
            MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("file", filename, fileBody)
                .build()
        val request =
            Request.Builder()
                .url("$root/v1/sessions/$pedagogySessionId/chunks/$chunkIndex")
                .post(multipart)
                .build()
        return executeJson(request)
    }

    fun completeSession(pedagogySessionId: String): JSONObject =
        postJson("$root/v1/sessions/$pedagogySessionId/complete", JSONObject())

    private fun getJson(url: String): JSONObject {
        val request = Request.Builder().url(url).get().build()
        return executeJson(request)
    }

    private fun postJson(url: String, body: JSONObject): JSONObject {
        val media = "application/json; charset=utf-8".toMediaType()
        val request =
            Request.Builder()
                .url(url)
                .post(body.toString().toRequestBody(media))
                .build()
        return executeJson(request)
    }

    private fun executeJson(request: Request): JSONObject {
        http.newCall(request).execute().use { response ->
            val text = response.body?.string().orEmpty()
            if (!response.isSuccessful) {
                throw PedagogyXApiException(response.code, text)
            }
            return if (text.isBlank()) JSONObject() else JSONObject(text)
        }
    }
}

data class DatSessionResponse(
    val datSessionId: String,
    val state: String,
    val streamState: String,
    val pedagogySessionId: String?,
) {
    companion object {
        fun from(json: JSONObject): DatSessionResponse =
            DatSessionResponse(
                datSessionId = json.getString("dat_session_id"),
                state = json.getString("state"),
                streamState = json.getString("stream_state"),
                pedagogySessionId = json.optString("pedagogy_session_id").ifBlank { null },
            )
    }
}

class PedagogyXApiException(val code: Int, val body: String) : Exception("HTTP $code: $body")
