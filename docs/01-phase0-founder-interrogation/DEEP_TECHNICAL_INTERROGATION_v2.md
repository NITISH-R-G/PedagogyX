# Phase 0 — Deep Technical & Strategic Interrogation Questionnaire v2

**Version:** 2.0
**Author:** Principal Research Architect
**Status:** Requires Founder Action
**Context:** This document represents an exhaustive interrogation required before any production implementation begins. It grills the founder to clarify technical, strategic, ethical, and product requirements for PedagogyX. We require explicit answers to all questions to unblock Phase 1.

## Strategic & Business Model

1. Does the enterprise SaaS model require multi-tenant isolation at the database level, or is row-level security sufficient for Indian schools?
2. How does the B2B sales motion in district procurement affect our onboarding flow? Will IT departments mass-provision accounts via SCIM?
3. Should the UI emphasize teacher self-improvement workflows, or top-down surveillance for administrators? (This fundamentally changes the dashboard architecture).
4. For school administrator analytics dashboards, what is the maximum acceptable query latency when aggregating data across 500 classrooms?
5. How deeply must the instructional coach be integrated into the loop? Is their approval required before AI feedback is released to the teacher?
6. Do we need parental consent and transparency portals built into the v1 product, or will schools manage consent externally?
7. Given the pricing strategy for Indian markets (₹0 budget constraint), what is our internal maximum cloud compute cost per hour of processed video?
8. Is a freemium teacher tier viable if they bring their own device, or does that violate DPDP if data leaves the school network?
9. To achieve competitive displacement of Edthena, what specific multimodal feature must we launch with that they cannot easily replicate?
10. How do we ensure alignment with DPDP compliance constraints if a teacher requests immediate deletion of a session currently processing in the GPU queue?
11. Will the system need integration with state teaching standards natively, or will districts upload their own PDF rubrics for RAG?
12. If we support custom rubrics per district, how do we prevent prompt injection attacks against the Qwen2.5 scoring agent?
13. Are video clipping and highlight reels sharing allowed outside the school tenant (e.g., public portfolios)?
14. What specific metrics are required for longitudinal growth charts for pedagogical metrics (e.g., Talk Ratio over 6 months)?
15. What are the gamification and leaderboard risks if principals start using the pedagogy index for punitive measures?
16. Must the mobile-first capture applications support background recording while the teacher uses the phone for other tasks?
17. What is the handling protocol for substitute teachers who have not signed the AI evaluation consent form?
18. Does the offline mode functionality require storing unencrypted video on the Android device's local storage?
19. Are corporate training adjacencies explicitly out of scope for the next 24 months?
20. What are the university deployment differences regarding RBAC (e.g., Deans vs Department Heads vs TAs)?

## Technical Architecture & Latency

21. Is multi-region active-active deployment required, or is a single ap-south-1 region sufficient for Phase 1?
22. What are the hard RPO and RTO SLAs we are promising to early pilot schools?
23. How does the API Gateway handle peak concurrent video uploads at 3 PM when all classes end simultaneously?
24. Is there a GPU inference fallback to CPU if the RTX 5070 pool goes down, or do we just queue and wait?
25. Is a classroom edge appliance viability study required before finalizing the Android BYOD strategy?
26. Will we migrate to Kubernetes vs Docker Swarm for Phase 2, and should we write Helm charts now?
27. Why choose Redis over Kafka for the event bus architecture given Kafka's better persistence guarantees for large ML pipelines?
28. What is the S3 compatible MinIO scaling strategy when we exceed 100TB of raw video?
29. Does the review UI require adaptive bitrate streaming (HLS), or can we serve static MP4 files?
30. How will we handle search indexing across transcripts? Is Postgres full-text search enough, or do we need Elasticsearch?
31. At what scale do we transition from Postgres to ClickHouse for real-time OLAP dashboard queries?
32. Where is the model registry and versioning system hosted, and how do workers pull new weights?
33. Are we building a human-in-the-loop data labeling platform internally to refine the CV models?
34. What is the synthetic data generation policy for training models on simulated classroom environments?
35. Are homomorphic encryption requirements on the roadmap for highly sensitive special education classrooms?
36. What is the hard cost ceiling per processed hour, and how does it inform our GPU quantization strategy?
37. Are we hosting open source model weights on our own infrastructure, or pulling from HuggingFace at runtime?
38. Can the WebRTC signaling server load handle 50 concurrent live streams per school edge node?
39. How do we guarantee temporal alignment of asynchronous audio/video streams if the teacher's phone and the room PC clocks are out of sync?
40. What is the network bandwidth minimum per classroom required to stream 720p without saturating the school LAN?

## AI Models & Perception Layer

41. How does faster-whisper perform on heavily accented Indian English, and what is the acceptable Word Error Rate (WER)?
42. How accurate must the diarization be in overlapping speech scenarios (common in large classrooms)?
43. What is the strategy for hallucination-resistant LLM prompting when generating teacher feedback?
44. Do we need YOLO bounding box temporal smoothing (e.g., DeepSORT) to track students, or is static frame detection enough?
45. If the student face blurring pipeline efficiency drops below real-time, does it block the entire cold path?
46. What is the scientific validity of our affective computing and emotion recognition models in an educational context?
47. Which specific pedagogical discourse moves (e.g., Revoicing, Probing) must the system reliably classify?
48. Are whiteboard equation OCR challenges (glare, bad handwriting) going to block the Math teaching evaluation feature?
49. How do we achieve slide semantic alignment with speech if the teacher isn't explicitly clicking 'Next Slide' in our app?
50. What is the required automatic lesson summarization depth? High-level bullet points or a minute-by-minute narrative?
51. Does the AI coaching agent have conversation memory across multiple sessions with the same teacher?
52. How do we handle long-context video understanding constraints when an 80-minute class exceeds the LLM's token limit?
53. Will we perform subject-specific fine-tuning (e.g. evaluating a Math class differently than an Art class)?
54. How does RAG over district curriculum documents ensure the LLM evaluates the teacher against the correct standard?
55. How do the CV models algorithmically differentiate between engaged listening vs boredom in cultures where sitting still is mandated?
56. Does the quantization of 7B parameter models (Qwen2.5 to 4-bit) destroy its ability to reason about complex pedagogy?
57. How frequently will we conduct bias auditing against Indian demographics for both the ASR and CV pipelines?
58. What are the confidence score thresholds required before an AI insight is displayed on the admin UI?
59. Do we have active learning loops established for failed inferences (e.g., instances where Talk Ratio was entirely wrong)?
60. What are the automated model rollback procedures if a newly deployed LLM prompt starts generating toxic feedback?

## Legal, Privacy & Ethics

61. Does our DPDP architecture natively support FERPA compliance parity for future US market entry?
62. What structural changes are required for GDPR compliance for future EU expansion?
63. Is there a strict student biometric data prohibition, meaning we cannot build persistent facial recognition profiles of students?
64. Will we use default optical blurring on the edge device, or metadata stripping in the cloud?
65. What is the automated workflow for parental opt-out handling mid-semester if a parent revokes consent?
66. If a teacher utilizes the teacher consent withdrawal workflow, does the system immediately purge their historical analytics?
67. Have we consulted with any legal experts on union collective bargaining agreement constraints regarding video surveillance?
68. Who holds the liability in the Data Processing Agreement templates if a data breach occurs on the edge LAN node?
69. Will we maintain public subprocessor list transparency even though we are primarily OSS?
70. What are the hard student data deletion SLAs (e.g., 72 hours from request to purge)?
71. What are the retention period limits for raw video versus anonymized JSON metadata?
72. How do we satisfy the right to explanation for AI outputs if a teacher demands to know why they received a low score?
73. What is the bias auditing cadence and reporting structure to the board of directors?
74. How will we conduct disparate impact testing by demographic to ensure the AI doesn't penalize specific accents?
75. What is our PR strategy for surveillance framing mitigation in marketing materials?
76. Where are the ethical boundaries drawn regarding China-style supervision features?
77. Do we have documented law enforcement data request policies?
78. Have we verified encryption at rest standard (AES-256) implementation on the edge nodes?
79. Will enterprise clients require customer-managed keys (CMK) requirements for MinIO?
80. Is an air-gapped deployment for government entities a hard requirement for Year 2?

## Classroom Modalities & Hardware

81. Does the system mandate a single vs multi-camera topology, and how does the sync engine handle the latter?
82. Is USB document camera integration required for the Windows capture agent?
83. Is a beamforming microphone array necessity, or can we rely entirely on the teacher's lapel mic?
84. How does the system handle interactive whiteboard (SMART) screen recording when the teacher is drawing on it?
85. What is the fallback if the teacher lapel mic reliability fails mid-lecture?
86. Are we attempting any student device screen analytics (e.g., seeing if they are on YouTube during class)?
87. How does the ASR pipeline handle noisy environments (PE, Music) where background noise exceeds the speech signal?
88. What are the lighting and glare tolerance limits for the CV models reading the physical whiteboard?
89. Is LMS clickstream ingestion (Canvas) required to correlate online assignments with classroom instruction?
90. Are there plans for real-time sensor IoT integration (CO2, temperature) to correlate environment with engagement?

---

_End of deep interrogation. Founder response required._

## Founder Extension Questionnaire

91. If the school internet is completely down for 3 weeks, do we continue capturing on the edge buffer or halt the agent?
92. Is the "Instructional Practices Inventory" explicitly required by the Ministry of Education for our pilot phase?
93. Can administrators override AI-generated scores before they are visible to teachers?
94. If an administrator is evaluating a teacher, does the teacher receive an audit notification?
95. Is code-switching between Hindi and English natively supported without manually toggling languages?
96. If a classroom fight breaks out, does the AI anomaly detection immediately alert school security via webhook?
97. Does the system enforce minimum recording lengths (e.g. 15 minutes) before generating a pedagogical score?
98. What is the SLA for "near real-time" dashboard updates for instructional coaches watching from a different building?
99. Do we support asynchronous co-viewing where coaches and teachers can leave time-stamped video comments?
100.  If we rely strictly on Ollama and OSS models, do we have a strategy to continuously benchmark our LLM's pedagogical accuracy against GPT-4?
101.  Is there a strict prohibition on using customer data to fine-tune our models?
102.  Can a school district opt out of cross-district telemetry aggregation?
103.  If a teacher requests to export their portfolio upon leaving a district, in what format is it provided?
104.  Is watermarking on video exports required to prevent unauthorized distribution?
105.  Does the application natively support dark mode to reduce eye strain during long review sessions?
106.  Are we planning to integrate with HR systems like Workday for automated observation scheduling?
107.  What is the acceptable false-positive rate for identifying "off-task behavior" in students?
108.  Will we provide a liability cap to districts if the AI provides demonstrably harmful coaching advice?
109.  Does the "kill switch" for the AI features delete data, or just disable the UI presentation layer?
110.  Are we planning to release our classroom dataset publicly to spur academic research, or is it a proprietary moat?

---

_End of deep interrogation. Founder response required._
