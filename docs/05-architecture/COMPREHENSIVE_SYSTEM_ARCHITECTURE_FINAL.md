# Comprehensive System Architecture: PedagogyX

**Document Objective**: To define the world-class, highly scalable, and privacy-preserving hybrid edge-cloud architecture for the PedagogyX classroom intelligence platform.

---

## 1. High-Level Architecture Overview

PedagogyX utilizes a **Hybrid Edge-Cloud Architecture**.

1. **Edge (Classroom)**: Handles low-latency capture, buffering, and secure transmission.
2. **Cloud (Central OSS Backend)**: Handles compute-heavy multimodal AI inference, data storage, and the web application interface.

```text
[ Classroom Environment ]                                   [ India Cloud Region ]

+---------------------+     Bluetooth/Wi-Fi    +-----------+      +-------------------+
| Meta Ray-Ban (DAT)  | =====================> | Edge Node | ===> | API Gateway / WAF |
| (Audio/Video/Photo) |                        | (Buffer)  |      +-------------------+
+---------------------+                        +-----------+               |
                                                                           v
                                                                  +-------------------+
                                                                  | Core FastAPI App  |
                                                                  +-------------------+
                                                                     |             |
                                                                +-------+      +-------+
                                                                | Redis |      | PSQL  |
                                                                +-------+      +-------+
                                                                     |
                                                +-----------------------------------------------+
                                                |                   GPU Workers                 |
                                                | +----------+  +----------+  +---------------+ |
                                                | | ASR Node |  | VAD Node |  | Vision / LLM  | |
                                                | +----------+  +----------+  +---------------+ |
                                                +-----------------------------------------------+
```

---

## 2. The Edge Tier (Capture & Buffer)

**Primary Client**: Meta Ray-Ban Smart Glasses (via DAT SDK).
**Edge Node**: An Android companion device or a local LAN PC.

### Core Responsibilities

1. **Continuous Capture**: Interfaces with the DAT SDK to pull streaming audio and periodic high-res photo/video frames.
2. **Local Buffering**: Writes raw media to local disk. This is critical because classroom Wi-Fi is notoriously unreliable. If the uplink drops, no data is lost.
3. **Secure Uplink**: Uses chunked, resumable uploads via presigned S3/MinIO URLs to push data to the cloud.
4. **Anonymization (Future Phase)**: Run lightweight face-blurring models (e.g., MediaPipe) before data leaves the LAN to satisfy strict DPDP/GDPR requirements.

---

## 3. The Cloud Tier (Ingestion & Storage)

**Tech Stack**: FastAPI, PostgreSQL, MinIO (Object Storage).

### Core Responsibilities

1. **Session Management**: API handles session creation, state management (Recording, Uploading, Processing, Complete).
2. **Presigned Uploads**: API issues secure, time-limited presigned URLs to the Edge Node for direct-to-object-storage uploads, bypassing the API server to save bandwidth and compute.
3. **Queue Orchestration**: Once an upload chunk is verified, the API pushes an event to Redis (e.g., `process_audio_chunk`).

---

## 4. The Intelligence Tier (GPU Pipeline)

This is the core intellectual property of PedagogyX. It is a distributed, event-driven pipeline.

### Pipeline Stages

1. **VAD (Voice Activity Detection)**:
   - _Input_: Raw Audio.
   - _Model_: Silero VAD.
   - _Output_: Timestamps of speech vs. silence. Filters out non-speech noise.
2. **Diarization & ASR (Automatic Speech Recognition)**:
   - _Input_: Speech segments.
   - _Model_: Pyannote (Diarization) + Faster-Whisper (ASR).
   - _Output_: Speaker-labeled transcript (e.g., `SPEAKER_00 (Teacher): "What is photosynthesis?"`).
3. **Visual Extraction (Slide/Board OCR)**:
   - _Input_: Video frames/Photos.
   - _Model_: Tesseract or a multimodal LLM (e.g., Llava).
   - _Output_: Extracted text and semantic descriptions of visual aids.
4. **Multimodal Fusion & Embedding**:
   - _Process_: Aligns the audio transcript with the visual context using timestamps.
   - _Output_: Dense vector embeddings representing 5-minute semantic chunks, stored in Qdrant.
5. **LLM Evaluation & Coaching Generation**:
   - _Input_: Fused multimodal text and embeddings.
   - _Model_: Local Llama 3 (via vLLM) or Cloud LLM API.
   - _Process_: Prompts the LLM with pedagogical frameworks (e.g., "Analyze this 5-minute chunk for Wait Time and Question Quality").
   - _Output_: Actionable JSON metrics and coaching text.

---

## 5. Security & Privacy Architecture

Given the sensitive nature of classroom recordings:

1. **Data Locality**: All processing occurs in a specific geographic cloud region (e.g., AWS ap-south-1 for India) to satisfy data sovereignty laws.
2. **RBAC**: Strict Role-Based Access Control. A teacher can see their own data. An administrator can see aggregate data, but _not_ individual teacher recordings without explicit consent workflows.
3. **Ephemeral Processing**: Intermediate files (raw audio chunks, unblurred video frames) are aggressively deleted from GPU worker nodes immediately after inference.
4. **Encryption**: TLS 1.3 in transit. AES-256 at rest for all databases and object storage.

---

## 6. Scalability Strategy

- **Stateless Workers**: The GPU workers are entirely stateless. They pull from Redis, process, write to Postgres/MinIO, and ack the message. This allows for massive horizontal scaling of inference nodes.
- **Queue Prioritization**: Premium users or real-time live-coaching requests get pushed to a high-priority Redis queue. Asynchronous post-class uploads go to a bulk-processing queue.
- **Cost Control**: Use auto-scaling groups for GPU instances. Scale to zero at night. Use spot instances for bulk asynchronous processing.

---

## 7. Risks & Mitigation

- **Risk**: ASR fails in noisy environments.
  - _Mitigation_: Fall back to visual cues and overall acoustic energy (volume/tone) to provide feedback, rather than relying solely on semantic transcripts.
- **Risk**: Database bottlenecks during massive ingestion.
  - _Mitigation_: Direct-to-S3 uploads protect the API. Postgres only handles metadata.
- **Risk**: Edge node failure.
  - _Mitigation_: Implement robust local SQLite caching on the edge node to resume uploads seamlessly after power/network loss.
