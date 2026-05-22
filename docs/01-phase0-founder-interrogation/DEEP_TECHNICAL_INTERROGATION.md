# Deep Technical Interrogation (India Supervision Mode & Hybrid Edge)

**Status:** Draft v0.1
**Date:** 2026-05-20
**Owner:** Architecture Team

This questionnaire is an extension to the initial `FOUNDER_QUESTIONNAIRE.md`, digging aggressively into the newly established constraints from `FOUNDER_ANSWERS.md`:

- India DPDP compliance.
- Hybrid Edge-Cloud (D-PROC = C).
- Supervision mode (Admin dashboards).
- ₹0 customer hardware budget (D-10).

---

## 1. Hybrid Edge-Cloud Resiliency (D-PROC)

1. If the school's WAN link goes down entirely for 3 days, does the Edge Node stop capturing, or does it fill its 2GB buffer and permanently lose data?
2. Can we require schools to provide a local NAS for extended offline buffering?
3. Who replaces the physical Edge Node if it has a hardware failure? Will PedagogyX dispatch IT support to rural Indian schools?
4. Is mTLS mandatory for the LAN communication between the Android smartboard and the Edge Node, or is HTTP acceptable to save CPU cycles on low-end boards?

## 2. Multi-Cam & Synchronization

5. When capturing `cam_1` (480p) from a 3-year-old Android smartboard, what happens if thermal throttling drops the frame rate to 2fps? Do we still calculate "Interaction Density"?
6. How do we guarantee clock synchronization across a Windows teacher PC (screen) and an Android wall panel (cam_1) without an external NTP server accessible on a restricted school LAN?
7. Do we accept audio from multiple sources and attempt algorithmic de-duplication, or do we force the user to pick exactly _one_ master microphone source?

## 3. Pedagogy Index & Supervision Mode

8. If a teacher scores in the bottom 5% of the Pedagogy Index due to heavy local accents failing our ASR, what is the automated dispute/human-review SLA?
9. Is "Student Attention Proxy" (measured via CV pose estimation) weighted heavily enough to fail a teacher's evaluation?
10. Are principals allowed to export raw video clips of "unengaged" students to show to parents, or does DPDP legally restrict this?

## 4. Financial Constraints & GPU Sizing

11. With a ₹0 customer budget, PedagogyX pays for the cloud GPUs. If a school leaves their cameras running 24/7 by accident, do we have a hard cut-off to prevent infinite cloud billing?
12. A single RTX 5070 node can process ~16 lessons per night (cold path). What is our plan when the pilot scales to 50 schools? Will the founder fund $2,000/mo in bare-metal GPU rentals?
13. If Ollama (Qwen2.5-7B) fails to generate a coaching summary within 5 minutes due to queue length, do we serve the dashboard _without_ the summary, or block the entire report?

## 5. India DPDP Compliance Specifics

14. Under DPDP 2023, verifiable parental consent is required for processing data of children (<18). Who collects this? The school, or the PedagogyX app?
15. If a parent revokes consent mid-year, does our vector DB support cascading deletes for a specific child's embeddings without retraining the whole model?
16. Are we acting purely as a "Data Processor" while the school is the "Data Fiduciary"? If yes, do we have a standard Data Processing Agreement (DPA) ready?

## Next Steps

These questions must be resolved before finalizing the MVP specifications for the capture agent and the central API.
