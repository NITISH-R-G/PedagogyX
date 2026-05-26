# Phase 0 Deep Foundational Interrogation

**Status:** Research Phase 0 Active
**Date:** 2026-05-26
**Owner:** Principal Research Architect (Jules)

This document represents the absolute foundational layer of our product definition. Before any code is written, we must challenge the core premises of PedagogyX. We need precise clarity from the founder regarding constraints, risks, models, scale, and compliance before committing to a systems architecture.

## Part I: Product & Market Alignment

### Core Identity & User Intent

1.  **Surveillance vs. Coaching**: The architecture for punitive surveillance (China-style) versus supportive coaching (US-style) fundamentally dictates database design, RBAC, edge-cloud decisions, and ML failure handling. Is PedagogyX optimizing for teacher evaluation or autonomous improvement?
2.  **Consent Mechanics**: Given the primary pivot to Ray-Ban Meta glasses via Android DAT companion, how exactly will ambient consent work in K-12 classrooms in India where DPDP mandates strict verifiable consent mechanisms for minors?
3.  **Real-Time Pedagogy Feedback**: Is "real-time" defined as streaming sub-second inference via an earpiece, or post-class analytics loops (batch)? This fundamentally changes whether we are building an RTP streaming engine or a batch-oriented document pipeline.
4.  **Hardware Failures**: "₹0 customer hardware budget". The plan specifies using teacher's personal Android devices to interface with Ray-Bans. What are our thermal budgets? What is the expected battery degradation curve on consumer Android devices running active DAT Bluetooth streams + WebRTC uplinks for 6+ hours a day?
5.  **Multi-Modal Ground Truth**: How do we weigh conflicting signals? If the computer vision models classify a classroom as "engaged" (eyes forward) but audio detects a monotone, low-energy lecture without Socratic questioning, how does the AI adjudicate the overall pedagogical score?
6.  **Admin Oversight Limits**: What happens when a unionized environment pushes back on the "Supervision Mode"? Can we dynamically disable dashboards while keeping personal coaching active via RBAC?
7.  **SaaS Monetization**: In Phase 1 we are offering free trials. When and how does monetization activate? Will pricing be based on compute-minutes, seat-licenses, or successful outcomes?

## Part II: Deep Technical Unknowns

### Wearables Device Access Toolkit (DAT) Integration

8.  **Bluetooth Bandwidth Constraints**: Ray-Ban DAT transmits over Bluetooth/Wi-Fi Direct. What is the sustained bandwidth and MTU assumption for dual-streaming (video + audio)? What happens during Wi-Fi Direct disconnections in a dense school environment with heavy 2.4GHz/5GHz interference?
9.  **Battery & Thermal (Glasses)**: Meta Ray-Bans are not designed for 8-hour continuous streaming. What is the specific duty cycle we expect? (e.g., 10 minutes on, 50 minutes off?) If it's continuous, the glasses will overheat. How do we architect around discontinuous data capture?
10. **Android Companion Choke Points**: What is the strategy for out-of-memory (OOM) kills by the Android OS when the PedagogyX companion app is running as a foreground service handling heavily compressed datastreams?
11. **Client-Side Sync**: If the Android device drops its cellular/Wi-Fi connection mid-lecture, how large is our local buffer? Are we spooling chunks to disk, and what happens to disk I/O on low-end Indian Android phones?

### The "D-PROC" Hybrid Edge-Cloud Architecture

12. **Central Inference Scaling**: With an RTX 5070 compute budget, how many concurrent DAT streams can one node handle? Have we modeled the VRAM requirements for Whisper (audio) + YOLO (vision) + Ollama (LLM) concurrently?
13. **Bandwidth in India Schools**: Relying on central inference means the school's upstream bandwidth must support raw or compressed video streams. Has the 95th percentile upstream bandwidth of the target Indian schools been validated?
14. **Batch vs. Streaming (ADR-0001)**: Is the cold path (post-hoc batch) fundamentally separate infrastructure from the hot path, or are we leveraging the same Kafka/RabbitMQ backbone?
15. **Storage Costs**: Storing multimodal classroom sessions is exponentially more expensive than text. How aggressive is our data retention policy? Do we prune raw video after inference extraction, maintaining only the vector embeddings and metadata?

### Artificial Intelligence & Ethics

16. **LLM Hallucinations in Pedagogy**: A hallucinated coaching tip could damage a teacher's confidence or career. What deterministic guardrails (RAG, rule-based checks) surround the generative LLM outputs before a human sees them?
17. **Bias in ASR**: Indian English and Hindi code-switching (Hinglish) is notoriously difficult for standard Whisper models. How are we fine-tuning or zero-shot prompting to achieve acceptable Word Error Rates (WER)?
18. **Facial Recognition (CV)**: The decision states "Identifiable student video in v1 = Yes". This is a massive DPDP liability. How are we anonymizing this data at the edge, or ensuring strict temporal access controls in the cloud?
19. **Pedagogical Validity**: Who defines "good teaching"? Are we hardcoding models to the Danielson Framework, the Marzano model, or a proprietary Indian pedagogical standard?

## Part III: Infrastructure & Reliability

20. **Self-Hosted Complexity**: We committed to an OSS-first, self-hosted stack. Who handles the Kubernetes upgrades, Postgres vacuuming, and MinIO storage tiering for the pilot schools?
21. **Disaster Recovery**: If the `ap-south-1` cluster goes down, what is the exact RTO/RPO for the captured sessions? Do the Android clients fail gracefully or lock up?

_These questions represent the minimum baseline of unknowns that must be modeled, tested, or explicitly accepted as risks before production MVP code is finalized._
