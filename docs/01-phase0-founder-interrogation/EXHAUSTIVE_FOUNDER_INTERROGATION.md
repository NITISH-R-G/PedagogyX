# Exhaustive Founder Interrogation

**Status:** Draft v1.0
**Date:** 2026-05-20
**Owner:** Architecture Team

This document outlines a deep and rigorous interrogation of the founder's assumptions, constraints, and business intent, targeting the PedagogyX Phase 0 phase.

## I. Business Strategy & Target Market

1.  **Market Definition:** While India is the first market, what is the sequence of global expansion over the next 3 years? Are we targeting regions with GDPR-like regulations (EU), or markets with more permissive surveillance policies (parts of Southeast Asia, MENA)?
2.  **Economic Buyer:** If the current Phase is "free", when does monetization begin, and who writes the check? Is it individual school principals using discretionary funds, or regional educational boards?
3.  **Pricing Model:** Will pricing be flat-fee per school, per classroom, or based on compute usage (processed hours)? What happens when a school exceeds its allocated hours?
4.  **Sales Motion:** Is the sales motion top-down (superintendents) or bottom-up (teachers advocating to admins)? If top-down, how do we mitigate teacher resistance and union pushback, even in non-unionized segments of the Indian market?
5.  **Competitive Differentiation:** If Chinese Smart Classrooms offer heavily subsidized hardware and software, how does PedagogyX compete? Is our edge purely pedagogical validity, or open-source trust?
6.  **Exit Strategy / End Game:** Is the goal to build a standalone enterprise SaaS giant, or to be acquired by a major LMS (e.g., Canvas, Blackboard) or tech conglomerate (e.g., Microsoft, Google)?
7.  **SLA Guarantees:** What are the contractual obligations regarding system uptime, processing latency (hot vs. cold paths), and data retention? Are there financial penalties for breaching these SLAs?
8.  **Support Structure:** Given the zero hardware budget, how is field support handled? Who provisions, repairs, or replaces the low-end Android/Windows devices when they inevitably fail?

## II. Product & User Experience

9.  **Core Value Proposition for Teachers:** Beyond "monitoring," what actionable, immediate value does a teacher get that makes them _want_ to use the system rather than feeling spied upon?
10. **Supervision vs. Coaching:** The system is heavily skewed towards "Supervision" (admin dashboards). How do we prevent this from becoming a purely punitive tool, which historical data shows often degrades educational quality rather than improving it?
11. **Actionable Insights:** When the AI flags a "low engagement" lesson, what specific, evidence-based recommendations does it provide? Or does it merely flag the event for human review?
12. **Teacher Agency:** Can a teacher proactively record a session for private self-review without it ever hitting the admin dashboard? Is there a "sandbox" mode?
13. **Student Perspective:** Do students have any visibility into the system? Can a student request their data be anonymized or excluded from a specific recording?
14. **Dashboard Fatigue:** How are we preventing administrators from being overwhelmed by data? What is the hierarchy of alerts and notifications?
15. **Localization:** Beyond English and Hindi, what specific dialects or regional languages are supported in Phase 1? How does the system handle code-switching (e.g., "Hinglish") in real-time?
16. **Accessibility:** Does the admin dashboard and teacher portal comply with WCAG 2.2 AA standards? Are there considerations for users with visual or auditory impairments?

## III. AI, Pedagogy, and Modeling

17. **Pedagogical Frameworks:** What specific pedagogical theories (e.g., Bloom's Taxonomy, TPACK, Danielson Framework) underpin the "Pedagogy Index"? Are these frameworks culturally appropriate for the target market?
18. **Bias in ASR:** How are we evaluating and mitigating bias in our ASR models against different regional accents, dialects, and speech impediments?
19. **Engagement Metrics:** How exactly is "Student Attention Proxy" defined? Is it purely based on head pose estimation (gaze tracking), or does it incorporate multimodal signals (audio interactions, physical movement)?
20. **False Positives in Engagement:** If a student is staring out the window but actively listening and synthesizing information, how does the CV model avoid penalizing the teacher for "low engagement"?
21. **Hallucination in Coaching:** When the LLM (e.g., Qwen2.5) generates coaching narratives, what safeguards prevent it from hallucinating non-existent classroom events or misinterpreting standard pedagogical practices?
22. **Model Explainability:** If a teacher disputes a low Pedagogy Index score, can the system provide a transparent, step-by-step breakdown of how that score was calculated, linking directly to video evidence?
23. **Continuous Learning:** How does the system improve over time? Is there a human-in-the-loop (HITL) annotation pipeline where expert educators validate or correct the AI's assessments?
24. **Temporal Modeling:** How does the system capture long-context events, such as a concept introduced at minute 5 being revisited at minute 45? Does the architecture support long-term memory across sessions?
25. **Multimodal Fusion:** How exactly are audio, video, and screen capture streams fused? Does the system use early fusion (combining raw signals) or late fusion (combining individual predictions)?

## IV. Technical Architecture & Constraints

26. **Edge vs. Cloud (D-PROC):** The D-PROC model specifies a Hybrid Edge. What is the minimum acceptable hardware specification for the Edge Node (CPU, RAM, Storage)?
27. **Offline Capability:** If the Edge Node loses internet connectivity for 7 days, what happens? Does it implement LRU (Least Recently Used) caching, prioritizing high-value sessions over others?
28. **Stream Synchronization:** How do we handle clock drift between a Windows teacher PC and an Android wall panel over a congested school LAN? What is the acceptable sync delta (e.g., <100ms)?
29. **Video Encoding:** Given low-end client devices, what encoding standard is mandated (H.264, VP8)? Are we relying on hardware acceleration, and what is the fallback if hardware encoding fails?
30. **Storage Architecture:** How are video assets stored long-term? Are we utilizing tiered storage (e.g., MinIO hot, S3 Glacier cold)? What is the exact data lifecycle policy?
31. **Database Strategy:** Why Postgres for structured data? How are we handling the massive volume of time-series event data generated by the inference pipelines? Is a dedicated time-series DB (e.g., TimescaleDB, ClickHouse) required?
32. **Vector Retrieval:** For semantic lesson search and RAG, what Vector DB is selected (e.g., Qdrant, Milvus)? How are we managing index sizing and retrieval latency at scale?
33. **Queueing System:** How robust is the job queue handling the "Cold Path"? What happens if the GPU workers fail during processing? Does the queue support priority weighting, dead-letter queues, and automated retries?

## V. Security, Privacy, and Compliance

34. **DPDP Compliance (India):** Who is legally responsible for obtaining verifiable parental consent for processing minors' data? How is this consent tracked and revoked within our system?
35. **Data Residency:** All data must reside in India. Which cloud region (e.g., AWS ap-south-1) is designated? Are there physical data center audits required by the pilot schools?
36. **Anonymization Strategy:** Are student faces blurred at the Edge before upload, or in the Cloud? If in the Cloud, how do we mitigate the risk of interception or unauthorized access to raw footage?
37. **Data Retention:** What is the exact retention policy for raw video vs. derived analytics? Can a school set custom retention policies?
38. **Encryption:** Is mTLS enforced between the Edge Node and the Cloud? Are data volumes encrypted at rest using customer-managed keys (KMS)?
39. **RBAC Complexity:** The matrix mentions "Teacher", "Coach", "School Admin", "District Admin". How are overlapping permissions handled? Can a Teacher also be a Coach for specific sessions?
40. **Audit Logging:** Is every access to a raw video or an aggregated report logged immutably? Who has access to the audit logs?

## VI. Infrastructure & Operations

41. **Deployment Automation:** How are updates pushed to the Edge Nodes and thin clients? Do we rely on standard MDM (Mobile Device Management) solutions, or a custom OTA (Over-The-Air) update mechanism?
42. **Monitoring & Observability:** What is the observability stack? Are we using Prometheus/Grafana for infrastructure metrics, and Jaeger/OpenTelemetry for distributed tracing across the hot and cold paths?
43. **GPU Cost Management:** The founder expects to fund cloud GPUs during the pilot. What is the concrete strategy for multi-tenant GPU sharing (e.g., NVIDIA MIG, vGPU) to maximize utilization and control costs?
44. **Disaster Recovery:** What is the defined RTO (Recovery Time Objective) and RPO (Recovery Point Objective) for the central database and object storage?
45. **Load Testing:** Have we simulated the thundering herd problem (e.g., 500 classrooms uploading video simultaneously at the end of the school day)? How does the ingest gateway scale?
