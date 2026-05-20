# Follow-Up Questionnaire: India-First Supervision & Multi-Cam Sync

**Status:** Draft — Generated after Tier-1 answers review.
**Purpose:** To drill down into the technical, legal, and operational implications of the India-first supervision mode with identifiable student video and real-time multi-cam capabilities.

## 1. India-First Supervision & Deployments

1. **Economic Buyer (D-05 Deep Dive):** Are the deals structured as state-level tenders (e.g., PM SHRI schools), district-level procurement, or private school chains? (Dictates compliance & scale).
2. **Classroom Hardware (D-10 Deep Dive):** Who provides the Android/Windows Smartboards? Are they pre-existing, or part of our BOM?
3. **Network Constraints:** You requested real-time multi-cam. What is the guaranteed upload bandwidth (Mbps) per classroom in rural vs. urban Indian schools?
4. **D-PROC Location:** Will the central OSS inference servers sit in a district/school on-prem rack or a centralized cloud (e.g., AWS ap-south-1)?
5. **Power Reliability:** What is the assumption around power cuts? Do clients need aggressive local caching and store-and-forward mechanisms?

## 2. Real-Time Multi-Cam & Sync

6. **Hardware Sync:** Are the multiple USB cameras genlocked, or must the software purely rely on NTP/audio timestamp correlation?
7. **Camera Placements:** What are the exact physical placements for the 2+ cameras? (e.g., 1 front-facing the class, 1 tracking the teacher).
8. **Real-Time SLAs:** What happens if the network drops during "real-time supervision"? Do we degrade to audio-only, or stop the dashboard feed entirely and queue for batch?
9. **Screen Capture:** Will the screen capture include high-motion video (e.g., teacher playing a YouTube video), or mostly static slides? (Impacts FPS/bitrate requirements).

## 3. Privacy, Ethics & India DPDP (G2 Blocker)

10. **Identifiable Video:** If the product identifies students in v1, how are we capturing verifiable parental consent in Indian government schools?
11. **Admin Punitive Actions:** If admins see individual AI pedagogy scores, and teachers unionize/protest, what is our liability/response plan?
12. **Retention Policy:** What is the maximum acceptable retention period for raw identifiable child video? (Default: 90 days - confirm?).

## 4. AI & Inference

13. **Language Code-Switching (D-11):** Indian classrooms frequently code-switch between English and Hindi mid-sentence. Do we require a specialized code-switching model, or is a generic Whisper-large-v3 sufficient?
14. **LLM Coaching (D-12):** If restricted to a 7B-14B on-prem model, we cannot do complex Video-LLM analysis. Are you comfortable with the LLM _only_ generating feedback from text transcripts and metrics?
15. **Golden Dataset:** Who is responsible for labeling the initial 100 hours of Indian classroom footage to establish our baseline Pedagogy Index?

## 5. Extrapolated Phase 0 Questions

16. **Is this enterprise SaaS?**
17. **Is this B2B?**
18. **Is this for schools or universities?**
19. **Is this for governments?**
20. **Is this for teacher self-improvement?**
21. **Is this for surveillance?**
22. **Is this for instructional coaching?**
23. **Is this for online classes?**
24. **Is this for physical classrooms?**
25. **Is this for hybrid classrooms?**
26. **Is this real-time or post-processing?**
27. **Is this cloud-native?**
28. **Is this edge AI?**
29. **Is privacy-first architecture required?**
30. **Is offline mode required?**
31. **What countries are target markets?**
32. **Is China-style surveillance acceptable?**
33. **Is student facial analysis allowed?**
34. **Is biometric analysis allowed?**
35. **What legal jurisdictions matter?**
36. **Is FERPA compliance required?**
37. **Is GDPR compliance required?**
38. **Is India DPDP compliance required?**
39. **Is explainable AI mandatory?**
40. **Is human review mandatory?**
41. **Is teacher scoring public or private?**
42. **Are unions involved?**
43. **Can administrators see teacher analytics?**
44. **Should the AI score pedagogy?**
45. **Should the AI detect emotional tone?**
46. **Should the AI evaluate student engagement?**
47. **Is multilingual support required?**
48. **Is low-bandwidth mode required?**
49. **Is mobile-first required?**

## 6. Technical Questions

50. scalability requirements?
51. latency acceptable?
52. inference pipelines design?
53. GPU requirements and availability?
54. edge deployment strategy?
55. classroom hardware constraints?
56. audio quality and recording setup?
57. microphone arrays required?
58. classroom camera topology?
59. synchronization pipelines?
60. multimodal fusion strategies?
61. storage architecture and retention?
62. distributed systems design?
63. vector databases utility?
64. observability setup?
65. security standards?
66. role-based access design?
67. ML ops lifecycle?
68. data labeling operations?
69. annotation workflows?
70. synthetic data generation?
71. model retraining policy?
72. privacy-preserving ML techniques?
73. federated learning applicability?
74. classroom network reliability?
75. live transcription constraints?
76. temporal event modeling?
77. multimodal embeddings?
78. long-context memory handling?
79. streaming pipelines robustness?

## Next Steps

Please review these questions along with the Tier-1 blockers (D-05, D-10, D-12) to unblock the next phase of architecture.
