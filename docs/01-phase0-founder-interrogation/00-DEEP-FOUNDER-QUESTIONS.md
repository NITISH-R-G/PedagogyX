# Deep Technical Interrogation & Founder Questions

This document serves as an exhaustive, aggressive, and highly detailed interrogation of the core product assumptions, constraints, legal boundaries, and technical architecture for the PedagogyX platform (Phase 0 — Foundational Interrogation). The goal is to flush out ambiguity, highlight contradictory requirements, force precise decision-making, and expose hidden risks before any production implementation begins.

---

## Part I: Product & Market Realities

### Market Scope & Go-To-Market

1. If the product is initially targeted at India, what specific regional/linguistic variations in teaching style and pedagogy are we optimizing for first (e.g., UP vs. Kerala)?
2. If this is B2B, who exactly holds the budget? District superintendents, school principals, or government bodies?
3. The "₹0 customer budget" implies the founder is subsidizing infrastructure. At what scale does this model break, and how is the transition to paid tiers handled?
4. Is the product for public (government) schools or private (international/tier-1) schools? The bandwidth and hardware assumptions differ wildly between the two.
5. If the system is used for "supervision," how are we mitigating the risk of teacher unions outright banning the tool?
6. Are there any plans to pivot to direct-to-consumer (e.g., individual teachers paying for an AI coach)?
7. Will the AI index score ever be used to determine teacher salaries, bonuses, or firings? If so, the legal liability of algorithmic bias is immense. Are you prepared for this?

### End-User Experience (Teachers & Students)

8. Does the teacher have a "kill switch" to stop recording if sensitive situations arise (e.g., medical emergency, disciplinary action)?
9. If a teacher disputes a low "Pedagogy Score," what is the exact workflow for human review and score override?
10. Is student facial analysis completely prohibited, or allowed with consent? What constitutes "consent" in a rural Indian school?
11. How do we prevent dashboard fatigue for principals who oversee 50+ classrooms simultaneously?
12. Will the mobile interface support low-end offline viewing of reports, or is it purely cloud-dependent?
13. If the system detects a highly successful teaching pattern, how does it share this insight globally while preserving the original teacher's privacy?

## Part II: Deep Technical Architecture & Scalability

### Edge Deployment & Capture (D-PROC Hybrid)

14. How are we ensuring clock synchronization (< 50ms drift) between Meta Ray-Ban smart glasses (Bluetooth to phone) and secondary fixed classroom cameras?
15. If the edge device (e.g., Android phone acting as DAT host) overheats and thermal throttles during a 60-minute class, what is the fallback strategy for video buffering?
16. How much local storage is mandated on the edge device to cache video during multi-day internet outages?
17. Are we running ANY on-device inference (e.g., VAD - Voice Activity Detection) to cull silence before cloud upload, or uploading raw feeds?
18. If a teacher walks out of the classroom (and out of Bluetooth/Wi-Fi range), how does the system gracefully handle connection drops and subsequent reconciliation?
19. What specific video encoding (H.264, H.265, AV1) is being used, and is hardware encoding guaranteed on all supported edge devices?

### Central Cloud Architecture & Distributed Systems

20. The pipeline handles "hot" (live dashboard) and "cold" (deep analytics) paths. What happens when the message broker (e.g., Redis/Kafka) drops messages during a massive 3:00 PM school-day-end upload spike?
21. What is the SLA for cold-path processing? 2 hours? 24 hours? This dictates our GPU queuing architecture.
22. How are we handling multi-tenancy at the database level? Row-level security (RLS) in Postgres, or separate schemas per school district?
23. If the centralized OSS-first backend in an India-based cloud goes down, is the edge capable of entirely autonomous operation, or does the system fail?
24. How are we scaling WebSocket connections for the live "hot path" across thousands of concurrent classrooms?
25. For vector embeddings (used in RAG for coaching), how often are indexes rebuilt to incorporate the latest pedagogical frameworks?

### AI Pipeline & Multimodal Inference

26. How exactly are we fusing audio transcription (ASR) with visual cues (CV head-pose estimation)? Is this early fusion at the embedding level or late fusion in a final decision tree?
27. When using LLMs (e.g., Qwen2.5) for coaching summaries, how are we anchoring the prompt to strict timestamps to prevent hallucination?
28. How does the system handle "Hinglish" or rapid code-switching within a single sentence? Standard whisper models struggle with this without specific fine-tuning.
29. Whiteboard OCR: Are we attempting to OCR from a moving POV camera (smart glasses), and how are we combating motion blur and poor lighting?
30. If the primary capture is Ray-Ban glasses, the POV is highly erratic. Have we validated that engagement CV models (trained on fixed security cameras) will even work on POV footage?
31. How are we measuring the "Pedagogy Index"? Is this a deterministic rule engine based on NLP markers, or an end-to-end black box neural network?
32. What is the synthetic data strategy to bootstrap the engagement models before we have thousands of real classroom recordings?

## Part III: Data Privacy, Security & Legal Bounds

33. DPDP Compliance (India): Does the platform function as a Data Fiduciary or a Data Processor?
34. If a parent revokes consent under DPDP, what is the SLA and technical mechanism to scrub their child's face/voice from a 45-minute multi-person video?
35. Are video files encrypted at rest using customer-managed keys (CMK), or system-managed keys?
36. Are we relying on hardware-backed keystores (e.g., Android Keystore, TPM) on the edge devices to secure mTLS certificates?
37. If a teacher demands the right to be forgotten, do we delete the video but keep the anonymized semantic transcript, or purge all derivative data?
38. Is China-style granular biometric tracking (e.g., micro-expressions) explicitly banned in the product requirements, or just deprioritized?
39. How do we audit access to raw video feeds by internal PedagogyX engineers for ML debugging?

## Part IV: Operational Strategy & MLOps

40. How do we orchestrate OTA (Over-The-Air) updates to the Android companion apps if a critical vulnerability is found?
41. What is the strategy for continuous retraining of the ASR model on specific regional dialects? How is ground-truth data labeled without violating privacy?
42. How are we monitoring GPU utilization, memory fragmentation, and OOM (Out of Memory) errors on the central inference cluster?
43. If a new version of the "Pedagogy Model" is deployed, do we backfill and re-score historical videos? If yes, how do we explain changing scores to confused principals?
44. What is the exact observability stack? Distributed tracing (OpenTelemetry) across the edge app, ingestion gateway, worker queues, and database?

---

_Note: This list is an initial barrage. The founder must provide written clarification on these points before system architecture is fully locked._
