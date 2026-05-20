# Epistemic & Domain Definitions

## Labeling Convention

| Label             | Meaning                              | Example                                                       |
| ----------------- | ------------------------------------ | ------------------------------------------------------------- |
| **[FACT]**        | Verifiable from primary sources      | FERPA treats identifiable student video as education records  |
| **[ASSUMPTION]**  | Default for planning until confirmed | Primary market is US K-12 districts                           |
| **[HYPOTHESIS]**  | Testable prediction                  | Talk-ratio coaching improves student discourse within 8 weeks |
| **[SPECULATION]** | Exploratory, not on roadmap          | Federated learning across districts without central video     |

---

## Working Product Definition (Draft)

**PedagogyX** — A privacy-configurable, multimodal analytics platform that ingests classroom session artifacts (audio, video, slides, whiteboard, LMS signals), produces **pedagogically grounded, explainable insights** for teacher growth, and supports **longitudinal instructional quality analytics** without defaulting to surveillance framing.

**[ASSUMPTION]** PedagogyX is **B2B SaaS** sold to institutions (districts, universities, governments), not direct-to-consumer teacher apps—unless founder overrides.

---

## Core Contradictions to Resolve (Phase 0)

| Tension                      | Pole A                    | Pole B                         | Why it matters            |
| ---------------------------- | ------------------------- | ------------------------------ | ------------------------- |
| Coaching vs surveillance     | Teacher-owned growth      | Admin quality dashboards       | UX, unions, retention     |
| Rich multimodal vs privacy   | Student face/gaze CV      | Audio-only / de-identified     | Legal, adoption, accuracy |
| Real-time vs post-hoc        | Live coaching earpiece    | Async reflection               | Latency, hardware, cost   |
| Global vs regional           | One platform              | China-style analytics          | Architecture, ethics, GTM |
| AI scoring vs human judgment | Automated pedagogy scores | Human coach in the loop        | Validity, liability       |
| Research-grade vs MVP        | Full multimodal fusion    | Talk-ratio only (TeachFX-like) | Timeline, team size       |

---

## Default Architectural Hypotheses (Revise via ADR)

| ID        | Hypothesis                                                                      | Rationale                                   |
| --------- | ------------------------------------------------------------------------------- | ------------------------------------------- |
| H-ARCH-01 | **Post-hoc batch pipeline first**, real-time second                             | Lower risk, aligns with Edthena/Vosaic/IRIS |
| H-ARCH-02 | **Event-sourced session model** with immutable raw ingest                       | Audit, replay, model reprocessing           |
| H-ARCH-03 | **Python for ML**, **Go or Rust for media/control plane**                       | Hiring + performance split                  |
| H-ARCH-04 | **No student biometric inference in v1** without explicit jurisdiction approval | GDPR fines, union backlash                  |
| H-ARCH-05 | **Human review gate** on all AI coaching narratives shown to admins             | Hallucination + labor relations             |

---

## Pedagogical Constructs (Reference)

| Construct                       | Description                       | Automation feasibility                                 |
| ------------------------------- | --------------------------------- | ------------------------------------------------------ |
| Talk ratio (T/S)                | Teacher vs student speech time    | **[FACT]** Mature (TeachFX, Vosaic, ASR)               |
| Flanders/IPI/S-T                | Interaction coding schemes        | **[HYPOTHESIS]** Partial via discourse + CV            |
| TPACK indices                   | Tech/pedagogy/content integration | **[FACT]** AI Sokrates operationalizes at scale        |
| Dialogic vs monologic discourse | Balance of interactive talk       | **[HYPOTHESIS]** ASR+NLP, moderate accuracy            |
| Engagement (affective)          | Boredom, confusion, etc.          | **[HYPOTHESIS]** DAiSEE/EngageNet ≠ physical classroom |
| Question quality                | Open vs closed, Bloom level       | **[HYPOTHESIS]** NLP classifiers, needs eval           |
| Wait time / pacing              | Temporal instructional events     | **[HYPOTHESIS]** Audio pause + slide transition fusion |

---

## Non-Goals (Until Founder Overrides)

- **[ASSUMPTION]** No automated **summative teacher evaluation** tied to compensation in v1
- **[ASSUMPTION]** No **public leaderboards** of teacher scores
- **[ASSUMPTION]** No sale to **pure surveillance** buyers without ethics review
- **[SPECULATION]** Real-time emotion classification of students
