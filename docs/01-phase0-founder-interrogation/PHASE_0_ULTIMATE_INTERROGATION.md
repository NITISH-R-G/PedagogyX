# Phase 0: Ultimate Founder Interrogation

**Status:** Draft v1.0
**Date:** 2026-05-24
**Owner:** Principal Research Architect

This document contains a comprehensive and unyielding interrogation of the founder's assumptions. Before any code is written, we must challenge every ambiguous requirement, clarify every technical constraint, and force precise product decisions.

## Part I: Product & Business Strategy Clarification

### 1. Market Positioning & Scope

1. Is this exclusively an enterprise B2B SaaS platform, or will there be a B2C component for individual teacher self-improvement?
2. If this is B2B for schools and universities, what is the exact persona of the buyer (e.g., Superintendent, Principal, IT Director, Dean)?
3. The target market is India. Are we building specifically for CBSE/ICSE boards, State boards, or higher education institutions like IITs/NITs?
4. Is government deployment in scope? If so, what are the specific public sector procurement and compliance requirements?
5. How does this system avoid being perceived purely as "surveillance"? What is the exact narrative given to teachers and unions?
6. Is this system primarily for post-processing instructional coaching, or is real-time intervention a mandatory feature?
7. Will the platform support online classes (Zoom/Teams), physical classrooms, or is it strictly hybrid?
8. The current constraint specifies ₹0 customer hardware budget. How do we monetize long-term if we bear the initial infrastructure costs?
9. Is China-style surveillance (facial recognition, continuous tracking) explicitly acceptable in our target markets, or strictly forbidden?
10. Is student facial analysis allowed for engagement tracking? If so, what is the legal justification under DPDP?

### 2. Legal & Compliance

11. Does the India DPDP compliance strictly mandate that all data processing must occur within India's borders (data residency)?
12. Is explicit, written consent required from parents for biometric analysis of minors, or does the school act in loco parentis?
13. If deployed internationally later, is FERPA (US) or GDPR (EU) compliance architecturally considered from day one, or retrofitted later?
14. Is human review mandatory for AI-generated teacher scores before they are finalized and visible to administrators?
15. If a teacher is penalized based on an AI assessment, is "Explainable AI" a legal requirement in our target jurisdictions?
16. Who owns the classroom recordings—the school, the teacher, or PedagogyX? What happens if a teacher requests deletion of their data?

### 3. User Experience & Interactions

17. Can administrators see individual teacher analytics, or only aggregated departmental trends?
18. If the AI detects a negative emotional tone, does it flag this immediately, or include it in a weekly summary?
19. Is the system required to evaluate student engagement on a per-student basis, or as a classroom-level aggregate (e.g., "70% of the class is engaged")?
20. Does the teacher receive real-time pedagogical nudges (e.g., via the Meta Ray-Ban glasses or a companion app), or only post-lesson reports?
21. What happens when a teacher strongly disagrees with the AI's assessment? Is there an appeals or correction workflow?
22. Is a "low-bandwidth mode" explicitly required for rural Indian schools? What is the minimum acceptable uplink speed?
23. Given the shift to Meta Ray-Ban glasses, how does a teacher interact with the system if they already wear prescription glasses?

## Part II: Deep Technical Interrogation

### 4. Hardware & Edge Capture

24. The primary client is now Meta Ray-Ban (DAT) + Android phone host. What happens when the phone's battery dies mid-lecture?
25. Meta Ray-Ban glasses have a limited continuous recording time due to battery and thermal constraints. How does the system handle multi-hour lectures?
26. Does the Android DAT host app process video locally (edge AI), or does it merely stream raw/compressed chunks to the cloud?
27. If the classroom network drops, how much video data can the Android host app buffer locally before it runs out of storage?
28. Are we entirely abandoning the "multi-cam classroom" and "microphone array" approach in Phase 1 in favor of the glasses' POV and mic?
29. How do we achieve audio synchronization if we eventually incorporate secondary room cameras or smartboards (Phase 1b)?

### 5. AI Pipelines & Multimodal Models

30. We are using `faster-whisper` for ASR. How accurately does it handle Indian English accents ("Hinglish") and code-switching between Hindi and English?
31. The benchmark is for RTX 5070 GPUs. If we scale to 1,000 concurrent classrooms, how many 5070s are required, and what is the exact cost model?
32. What is the target latency for real-time coaching insights? Is it <1 second, <3 seconds, or is 30-second batch processing acceptable?
33. How does the multimodal fusion model align the timestamps of the video feed (from the glasses) with the transcribed audio text?
34. Are we fine-tuning LLMs (like Llama 3 or Qwen) for pedagogical analysis, or relying on prompt engineering and RAG against a foundational model?
35. What is the fallback mechanism if the AI pipeline hallucinates a severe critique of a teacher's lesson?

### 6. Infrastructure & Scalability

36. Is the infrastructure entirely cloud-native (AWS/GCP), or are we planning a self-hosted bare-metal GPU cluster for cost efficiency?
37. How are we managing the massive storage requirements for recording thousands of hours of high-definition classroom video per day?
38. What is the database architecture for storing high-dimensional vector embeddings of classroom sessions? Are we using pgvector, Milvus, or Qdrant?
39. How do we guarantee the isolation of tenant data (School A cannot see School B's recordings) in a shared database environment?
40. What observability stack (e.g., Prometheus, Grafana, Datadog) is required to monitor the health of the GPU inference queues?

## Part III: Validated Facts vs. Assumptions

**Validated Facts:**

- Target Market: India (D-02)
- Primary Capture Device: Meta Ray-Ban smart glasses via DAT + Android app (ADR-0009)
- Budget Constraint: ₹0 customer hardware budget for pilot (D-10)
- Core Infrastructure: Hybrid Edge-Cloud (D-PROC=C)
- Dev GPU Target: RTX 5070 12GB (ADR-0006)

**Dangerous Assumptions (Require Clarification):**

- _Assumption:_ Teachers will willingly wear Meta Ray-Ban glasses during lectures without union or personal pushback.
- _Assumption:_ The Meta Ray-Ban battery and thermal limits are sufficient for typical Indian classroom session lengths (45-90 minutes).
- _Assumption:_ India DPDP compliance allows us to stream identifiable student faces to our centralized cloud for processing.
- _Assumption:_ Our open-source LLM stack (Ollama/faster-whisper) can deliver insights quickly enough to be perceived as "real-time" by the user.

---

_End of Interrogation Document. Awaiting explicit founder sign-off on all assumptions before proceeding to Phase 1 implementation._
