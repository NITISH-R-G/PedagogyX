# India DPDP — Counsel Engagement Brief (S01-02)

**Status:** Draft for founder to send to qualified **Indian privacy counsel**  
**Owner:** Founder  
**Date:** 2026-05-20  
**Gate:** **G2** — legal sign-off required before implementation code  
**Not legal advice.**

---

## Purpose of engagement

PedagogyX is an **OSS classroom analytics platform** (Phase 0 complete) planning **free pilots** at **schools and universities in India**. We need a written legal memo covering DPDP 2023 compliance for **v1 supervision mode**:

- Screen + microphone + multi-camera capture
- **Identifiable student video** (founder confirmed D-03)
- **Per-teacher pedagogy scores** visible to admins (D-06)
- **Hybrid deployment:** LAN edge buffer + India cloud GPU (ADR-0008)
- **OSS-only LLM** on central GPU — no public cloud LLM APIs (D-12)

---

## Product summary for counsel (1 page)

| Item                           | Detail                                                                                      |
| ------------------------------ | ------------------------------------------------------------------------------------------- |
| **Data controller (expected)** | Pilot **school / university** (Data Fiduciary)                                              |
| **Data processor**             | PedagogyX (vendor)                                                                          |
| **Subjects**                   | Teachers and students in recorded lessons                                                   |
| **Purpose**                    | Monitor and assess **teacher pedagogy**; school supervision workflows                       |
| **Not in v1**                  | Per-student punitive report cards; advertising; model training on pilot data without opt-in |
| **Retention (proposed)**       | 90 days raw AV **[HYPOTHESIS]** — counsel to set                                            |
| **Geography**                  | Storage and inference in **India** (ap-south-1 class region)                                |
| **Customer budget**            | ₹0 pilot — founder-funded infra                                                             |

Full architecture: [INDIA_DPDP_ARCHITECTURE.md](INDIA_DPDP_ARCHITECTURE.md)

---

## Specific questions for counsel

### 1. Lawfulness and consent

1. For **K-12 minors**, what **verifiable parental consent** mechanism is sufficient (written, digital, school-as-proxy)?
2. For **university adults**, is institution-level consent + notice adequate?
3. Do **state-level** rules differ for classroom audio/video recording (two-party consent states)?

### 2. Children’s data (DPDP)

4. Are we processing **children’s personal data** under DPDP definitions for all K-12 pilots?
5. What **additional obligations** apply (purpose limitation, retention, grievance)?
6. Is **identifiable student video** justifiable for stated purpose, or must we offer **de-identified tier**?

### 3. Automated processing & employment

7. Do **teacher pedagogy scores** shown to admins constitute **automated decision-making** affecting employment?
8. What **transparency and appeal** rights must we offer teachers?

### 4. Processor agreement

9. Minimum **DPA** clauses for school ↔ PedagogyX (subprocessors, breach notification, deletion)?
10. Requirements if PedagogyX entity is **foreign-incorporated** (India representative, grievance officer)?

### 5. Cross-border and OSS stack

11. Is **India-only** MinIO/Postgres/GPU sufficient, or are there rules for **backup DR** outside India?
12. Any restriction on **open-source models** (Whisper, YOLO, Qwen) processing child data on rented GPU VPS?

### 6. Pilot-specific

13. Can a **free pilot** proceed with interim safeguards before full production DPIA?
14. Minimum **privacy notice + in-class recording indicator** language (English + Hindi)?

---

## Documents to attach for counsel

| Document                | Path                                                                                   |
| ----------------------- | -------------------------------------------------------------------------------------- |
| DPDP architecture draft | [INDIA_DPDP_ARCHITECTURE.md](INDIA_DPDP_ARCHITECTURE.md)                               |
| Ethical framework       | [ETHICAL_FRAMEWORK.md](ETHICAL_FRAMEWORK.md)                                           |
| Threat model            | [THREAT_MODEL_STRIDE_v0.1.md](../10-risks/THREAT_MODEL_STRIDE_v0.1.md)                 |
| Founder decisions       | [FOUNDER_ANSWERS.md](../01-phase0-founder-interrogation/FOUNDER_ANSWERS.md)            |
| Capture protocol        | [RFC-0002](../08-rfc-adr/RFC-0002-capture-agent-sync-protocol.md)                      |
| Admin UI wireframes     | [ADMIN_LIVE_DASHBOARD_WIREFRAMES.md](../02-product/ADMIN_LIVE_DASHBOARD_WIREFRAMES.md) |

---

## Deliverables expected from counsel

| #   | Deliverable                                                         | Due (suggested)        |
| --- | ------------------------------------------------------------------- | ---------------------- |
| 1   | **Legal memo** — lawfulness of v1 pilot under DPDP                  | 2–3 weeks              |
| 2   | **DPIA template** completed for one K-12 + one university archetype | With memo              |
| 3   | **Privacy notice** draft (EN + HI)                                  | With memo              |
| 4   | **DPA schedule** for school contracts                               | With memo              |
| 5   | **Go / no-go** for G2 gate                                          | Explicit sign-off line |

---

## Founder action checklist

- [ ] Shortlist 2–3 India education/privacy law firms
- [ ] Send this brief + attachments under NDA
- [ ] Name **pilot school** (even provisional) for DPIA fact pattern
- [ ] Budget for counsel fees (separate from D-10 ₹0 customer infra)
- [ ] File counsel memo in repo as `INDIA_LEGAL_MEMO_YYYY-MM.pdf` (confidential — may stay off GitHub)

---

## G2 exit

When counsel memo is **signed**, update [docs/README.md](../README.md) gate **G2** to 🟢 and authorize **MVP codebase** per [IMPLEMENTATION_ROADMAP.md](../09-agile/IMPLEMENTATION_ROADMAP.md).
