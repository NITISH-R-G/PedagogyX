# Compliance & Privacy Architecture

**Status:** Draft — **not legal advice**

---

## Jurisdiction Matrix

| Regulation     | Applies when                             | PedagogyX default posture                                           |
| -------------- | ---------------------------------------- | ------------------------------------------------------------------- |
| **FERPA**      | US K-12/higher ed, identifiable students | Treat classroom video with students as education records **[FACT]** |
| **COPPA**      | Under 13                                 | Parental consent flows; minimize data                               |
| **GDPR**       | EU                                       | DPIA, lawful basis, special category biometrics restricted          |
| **India DPDP** | India processing                         | Data localization evaluation                                        |
| State laws     | CA SOPIPA, etc.                          | Prohibit commercial use of student data                             |

---

## FERPA Implications **[FACT]**

- Recordings with identifiable students = **education records** when maintained by institution
- Sharing outside class requires consent, de-identification, or exception
- **Third-party AI** processing requires institutional agreement; many GenAI tools prohibited for student data without BAA/DPA review
- Recordings with **teacher only** may fall outside student record rules (institution-dependent)

**Product requirements:**

- District-owned data processing agreement
- Subprocessor transparency
- No training public LLMs on customer content (contractual + technical)

---

## GDPR / Biometrics **[FACT]**

- Facial recognition in schools triggered **enforcement** (e.g., Sweden €20k fine for attendance FRT)
- Consent alone often **insufficient** due to power imbalance
- Requires DPIA, necessity, proportionality, less intrusive alternatives

**PedagogyX default:** no facial recognition for identification; optional de-identified CV aggregates only with DPIA.

---

## Privacy-by-Design Controls

| Control                 | Implementation                                         |
| ----------------------- | ------------------------------------------------------ |
| Tiered analytics        | Tenant flag `privacy_tier` ∈ {audio, deid_video, full} |
| De-identification       | Face blur, voice alteration for exports                |
| Retention TTL           | Raw video 90d default **[ASSUMPTION]**                 |
| RBAC                    | Coach cannot see unless shared                         |
| Audit log               | All views/downloads                                    |
| CMK                     | Enterprise option                                      |
| Student voice redaction | NLP + beep on export                                   |

---

## AI-Specific Compliance

| Risk                    | Mitigation                             |
| ----------------------- | -------------------------------------- |
| Hallucinated feedback   | Human approval, citation-required      |
| Bias in engagement CV   | Disaggregated eval, no high-stakes use |
| Surveillance perception | Teacher-initiated recording default    |
| Cross-lesson search     | Admin policy + audit                   |

---

## Data Processing Agreement Checklist

- [ ] Roles: school = controller, PedagogyX = processor
- [ ] Subprocessors listed (cloud, ASR, LLM)
- [ ] Deletion on contract end
- [ ] Breach notification SLA
- [ ] SOC 2 roadmap
- [ ] Standard Contractual Clauses for EU

---

## Open Legal Questions (Counsel)

1. Is AI-generated coaching text an **education record**?
2. Aggregated district analytics — when re-identifiable?
3. Union bargaining — mandatory consultation states?
4. Recording consent — one-party vs all-party audio states?
