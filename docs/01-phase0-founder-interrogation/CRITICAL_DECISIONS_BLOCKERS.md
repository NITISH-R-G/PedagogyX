# Critical Decision Blockers — Implementation Gate G0/G1

**Status:** 🟢 **G0 COMPLETE** (founder Tier-1 answers 2026-05-19)  
**Canonical answers:** [FOUNDER_ANSWERS.md](FOUNDER_ANSWERS.md)

---

## Tier 1 — Founder answers recorded

| ID             | Question                                  | **Founder answer**                                                              | Gate                   |
| -------------- | ----------------------------------------- | ------------------------------------------------------------------------------- | ---------------------- |
| **D-01**       | Primary customer                          | **K-12 district + university**                                                  | ✅                     |
| **D-02**       | Year-1 geography                          | **India**                                                                       | ✅                     |
| **D-03**       | Identifiable student video in v1?         | **Yes**                                                                         | ✅ (triggers G2 legal) |
| **D-04**       | Real-time coaching in v1?                 | **Yes**                                                                         | ✅                     |
| **D-05**       | Economic buyer?                           | **School + university**; **free pilot**, no payment expected                    | ✅                     |
| **D-06**       | Admins see individual AI pedagogy scores? | **Yes**                                                                         | ✅                     |
| **D-07**       | China-style supervision acceptable?       | **Yes** (some markets)                                                          | ✅                     |
| **D-08**       | Capture model?                            | **Screen recording + microphone**                                               | ✅                     |
| **D-09**       | MVP modality?                             | **Multi-cam**                                                                   | ✅                     |
| **D-10**       | Budget ceiling per classroom/year?        | **₹0 / $0 customer** (founder-funded pilot infra)                               | ✅                     |
| **D-11**       | ASR languages (inferred)?                 | **TBD** (assume EN + HI)                                                        | 🟡                     |
| **D-12**       | Cloud LLM?                                | **OSS on-prem only**                                                            | ✅                     |
| **D-GPU**      | Dev GPU?                                  | **RTX 5070 — dev only**                                                         | ✅                     |
| **D-OSS**      | OSS-first?                                | **Yes**                                                                         | ✅                     |
| **D-CLIENT**   | Production devices?                       | **All low-end Android + Windows smartboards** (profile-based, no OEM whitelist) | ✅                     |
| **D-PROC**     | Where ML runs?                            | **C — Hybrid** (LAN edge + India cloud)                                         | ✅                     |
| **D-DEV**      | Device validation?                        | **Any** panel meeting low-end profiles; OEM list is examples only               | 🟡                     |
| **D-20**       | Year-1 success metric?                    | **Primary M-A**; **Secondary M-B, M-C**                                         | ✅                     |
| **D-PEDAGOGY** | Product focus?                            | **Monitor & assess teacher pedagogy** (not per-student punitive scores in v1)   | ✅                     |

---

## Tier 2 — Still open

| ID       | Question                       | Default until answered  |
| -------- | ------------------------------ | ----------------------- |
| **D-13** | Label data in-house or vendor? | Vendor                  |
| **D-14** | Synthetic data OK?             | Yes with disclosure     |
| **D-15** | Explainability level?          | Rubric + evidence clips |

---

## Tier 3 — Still open

D-16 through D-19 — see [FOUNDER_QUESTIONNAIRE.md](FOUNDER_QUESTIONNAIRE.md)

---

## Contradiction Alerts — **ACTIVE**

| Tension                                      | Founder choice  | Risk                                        |
| -------------------------------------------- | --------------- | ------------------------------------------- |
| India DPDP + child data + identifiable video | Yes to ID video | Consent, purpose limitation, retention caps |
| Real-time + multi-cam + screen capture       | All in v1       | Cost, bandwidth, school IT burden           |
| Supervision + admin individual scores        | Yes             | Teacher trust, press, parent complaints     |
| Dual customer (K-12 + university)            | Both            | Two compliance paths, two UX                |

**Legal review required before G2** — see [INDIA_DPDP_ARCHITECTURE.md](../07-compliance-ethics/INDIA_DPDP_ARCHITECTURE.md)

---

## Sign-off

| Role                  | Name | Date       | Status                            |
| --------------------- | ---- | ---------- | --------------------------------- |
| Founder               |      | 2026-05-19 | Tier-1 complete                   |
| Legal counsel (India) |      |            | Not started                       |
| Technical lead        |      |            | Architecture revision in progress |
