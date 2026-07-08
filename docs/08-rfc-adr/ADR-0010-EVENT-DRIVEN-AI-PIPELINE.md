# ADR-0010: Event-Driven Architecture for Multimodal AI Pipeline

## Context

PedagogyX requires deep analysis of classroom sessions. The analysis involves multiple steps: VAD, ASR (Whisper), Computer Vision (head pose, gaze), and finally LLM pedagogical scoring. Running these synchronously on a single API request is impossible due to the processing time (minutes to hours) and hardware constraints (RTX 5070 12GB).

## Decision

We will adopt a completely asynchronous, event-driven architecture for the "Cold Path" AI inference pipeline.

- **Message Broker:** Redis Streams (or Celery with Redis broker) will manage task queues.
- **Orchestration:** The main API will act only as an ingress for file uploads. Upon successful assembly of an uploaded lesson, the API will publish a `LessonUploaded` event.
- **Workers:** Dedicated GPU workers will subscribe to events. An orchestrator will manage the sequence (e.g., ASR worker runs first, publishes `TranscriptGenerated` event -> LLM worker consumes transcript).

## Rationale

- **Resilience:** If a GPU worker crashes or OOMs (Out of Memory), the task remains in the queue and can be retried.
- **Resource Management:** We can strictly control concurrency. Only one large model (e.g., Qwen2.5-7B) will be loaded onto the GPU at a time.
- **Extensibility:** New modalities (e.g., OCR on slides) can be added as isolated workers subscribing to the initial `LessonUploaded` event without touching existing pipeline code.

## Consequences

- Increased system complexity compared to a monolithic API.
- Requires robust monitoring of queue lengths and worker health.
- The frontend must rely on polling or WebSockets to receive the final pedagogical score, as the upload API will return immediately.
