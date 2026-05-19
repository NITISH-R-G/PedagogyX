# Product Requirements Document v0.1 (Draft)

**Status:** 🔴 Blocked on Phase 0 answers  
**Product:** PedagogyX Classroom Intelligence Platform

---

## 1. Problem Statement

Teachers lack **timely, objective, actionable feedback** on classroom practice. Coaches cannot scale observation. Districts spend heavily on PD with weak measurement.

**[FACT]** Teachers talk 70–80% in many classrooms (TeachFX mission); dialogic instruction correlates with better outcomes.

---

## 2. Vision

**Multimodal evidence + pedagogical frameworks → explainable coaching → longitudinal teacher growth.**

Not: automated surveillance scoring.

---

## 3. Goals (Year 1 hypothesis)

| Goal | Metric (TBD with founder) |
|------|---------------------------|
| Adoption | X% pilot teachers upload ≥4 lessons/month |
| Utility | Coach NPS ≥ 40 |
| Efficacy | +Y% student talk time (pilot RCT optional) |
| Trust | <Z% teachers report "surveillance" in survey |

---

## 4. Personas (Draft)

| Persona | Need |
|---------|------|
| **Teacher** | Private reflection, evidence clips, growth tracking |
| **Instructional coach** | Efficient review, rubric alignment, PLC sharing |
| **Principal** | Aggregate PD insights (not individual punishment) |
| **District admin** | ROI, standards alignment, compliance |
| **Researcher** | Anonymized exports |

---

## 5. Functional Requirements (Epic-level)

### EPIC-01 Capture & Ingest
- Resumable upload (web/mobile)
- Consent + recording indicator
- Privacy tier enforcement

### EPIC-02 Media Processing
- Transcode to house format
- Thumbnail + waveform
- Optional face blur pipeline

### EPIC-03 Speech Intelligence
- Transcript with timestamps
- Teacher/student talk ratio (confidence band)
- Silence, overlap detection

### EPIC-04 Discourse Analytics (Phase 2)
- Question type proxies
- Dialogic vs monologic indicators

### EPIC-05 Coaching Experience
- Timeline player with transcript sync
- Commenting + tags
- AI draft narrative with citations
- Human approve workflow

### EPIC-06 Administration
- SSO, RBAC, audit logs
- District aggregates (k-anonymized)

---

## 6. Non-Functional Requirements

| NFR | Target (draft) |
|-----|----------------|
| Availability | 99.9% |
| Analysis SLA | < 30 min for 50-min lesson (T0) |
| Security | SOC 2 Type II in 18 months **[ASSUMPTION]** |
| Accessibility | WCAG 2.2 AA |

---

## 7. Out of Scope v1

- Live in-ear coaching
- Student face emotion scoring
- Automated tenure recommendations

---

## 8. Dependencies

Founder questionnaire, legal review, pilot district LOI.
