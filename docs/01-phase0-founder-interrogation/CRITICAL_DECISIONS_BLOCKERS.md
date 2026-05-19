# Critical Decision Blockers — Implementation Gate G0/G1

**Status:** 🔴 **BLOCKING** — Cannot finalize architecture or cost models without these answers.

Answer directly in this file (append `**Founder answer:**` under each item) or in a linked decision log.

---

## Tier 1 — Must answer before any architecture freeze

| ID | Question | Default if silent | Impact |
|----|----------|-------------------|--------|
| **D-01** | Primary customer: K-12, higher ed, corporate L&D, or government? | K-12 US | GTM, compliance, UX |
| **D-02** | Primary geography year 1? | US only | Legal, language, cloud region |
| **D-03** | Is student **identifiable video** in scope for v1? | No — audio + de-identified video | 50% of CV pipeline |
| **D-04** | Is **real-time** coaching (in-ear / live dashboard) in scope for v1? | No — post-lesson only | Infra, WebRTC |
| **D-05** | Who is the **economic buyer**? | District curriculum/coaching office | Pricing, features |
| **D-06** | Can **admins** see individual teacher AI scores? | Coaches only, not HR | RBAC, unions |
| **D-07** | Is platform **surveillance-acceptable** in any market? | No | Brand, China features |
| **D-08** | Hardware: BYOD upload only, or bundled capture kits? | BYOD | Logistics, margin |
| **D-09** | Minimum viable modality: audio-only, single cam, or multi-cam? | Single cam + audio | Cost per hour |
| **D-10** | Budget ceiling per classroom per year for infra? | Unknown | Model selection |

---

## Tier 2 — Must answer before ML roadmap

| ID | Question | Default if silent |
|----|----------|-------------------|
| **D-11** | Target languages for ASR year 1? | English |
| **D-12** | Accept cloud LLM (OpenAI/Anthropic) or require private LLM? | Private/vPC for student-adjacent data |
| **D-13** | Will you **label data** in-house or vendor? | Vendor + teacher opt-in |
| **D-14** | Is **synthetic classroom data** acceptable for training? | Yes with disclosure |
| **D-15** | Required explainability: feature attributions, rubric mapping, or narrative only? | Rubric-mapped evidence clips |

---

## Tier 3 — Must answer before enterprise sales materials

| ID | Question |
|----|----------|
| **D-16** | SOC 2 Type II timeline expectation? |
| **D-17** | Data residency: US-only, EU region, India, Middle East? |
| **D-18** | SSO: SAML, OIDC, both? Clever/ClassLink? |
| **D-19** | LMS integrations priority list? |
| **D-20** | Union / collective bargaining markets — any hard exclusions? |

---

## Contradiction Alerts (Founder must pick a lane)

1. **"Privacy-first" + "engagement heatmaps from student faces"** — incompatible without strict consent and DPIA.
2. **"Rival China smart classroom" + "EU/US union-friendly"** — feature sets diverge sharply.
3. **"Autonomous classroom intelligence" + "human review mandatory"** — define autonomy boundary.
4. **"30-day research phase" + "ship in Q1"** — clarify calendar vs agent-effort metaphor.

---

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Founder | | | |
| Technical lead | | | |
| Legal counsel | | | |
