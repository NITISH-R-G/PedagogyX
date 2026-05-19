# Research Library Index

**Status:** Seed corpus v0.1 — expand weekly during Phase 0–2

## Taxonomy

| Tag   | Domain                           |
| ----- | -------------------------------- |
| `MM`  | Multimodal ML                    |
| `CDA` | Classroom discourse analysis     |
| `CV`  | Classroom computer vision        |
| `EDM` | Educational data mining          |
| `AFF` | Affective computing / engagement |
| `TE`  | Teacher effectiveness            |
| `LKV` | Long-context video               |
| `ETH` | Ethics / privacy                 |
| `SYS` | Systems / MLOps                  |

---

## Tier 1 — Anchor Papers (Summarized)

| ID    | Citation                                                  | Tags    | Summary doc                                                                                              |
| ----- | --------------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------- |
| P-001 | Ku et al., ICCE 2018 — STAS                               | TE, SYS | [papers/ku-2018-stas.md](papers/ku-2018-stas.md)                                                         |
| P-002 | Donnelly et al., ACL 2016 — ASR teacher questions         | CDA     | [papers/donnelly-2016-teacher-questions-asr.md](papers/donnelly-2016-teacher-questions-asr.md)           |
| P-003 | Karumbaiah et al., EDM 2024 — student diarization         | CDA     | [papers/karumbaiah-2024-student-diarization.md](papers/karumbaiah-2024-student-diarization.md)           |
| P-004 | arXiv 2410.07834 — SCB-DETR smart classroom               | CV      | [papers/scb-detr-2024-smart-classroom.md](papers/scb-detr-2024-scb-detr.md)                              |
| P-005 | NSF — multimodal teacher noticing (human-AI class)        | MM, TE  | [papers/nsf-teacher-noticing-multimodal.md](papers/nsf-teacher-noticing-multimodal.md)                   |
| P-006 | DAiSEE (Kaur et al., 2016)                                | AFF     | [papers/kaur-2016-daisee.md](papers/kaur-2016-daisee.md)                                                 |
| P-007 | Nature Sci Data 2025 — classroom group engagement dataset | AFF, CV | [papers/nature-2025-classroom-engagement-dataset.md](papers/nature-2025-classroom-engagement-dataset.md) |
| P-008 | Instructional activity recognition transformer (NSF PAR)  | CV, MM  | [papers/instructional-activity-transformer.md](papers/instructional-activity-transformer.md)             |

---

## Tier 2 — Queued for Summary

- Flanders interaction analysis automation
- TalkMoves / Accountable Talk classifiers
- Lesson transcript LLM summarization hallucination studies
- Video-LLM (GPT-4o, Gemini) classroom eval benchmarks
- Federated learning in education surveys
- TPACK measurement validity literature

---

## Public Datasets

| Dataset                      | Use case             | Classroom physical? | Access           |
| ---------------------------- | -------------------- | ------------------- | ---------------- |
| DAiSEE                       | Affective engagement | No (e-learning)     | Request          |
| EngageNet                    | Engagement levels    | No (tutor avatar)   | Request          |
| Nature 2025 group engagement | Group engagement CV  | Yes                 | Paper supplement |
| HiTeach/Sokrates             | TPACK analytics      | Yes (platform)      | Proprietary      |

**[ASSUMPTION]** PedagogyX will need **consented district data** + synthetic augmentation; public sets insufficient alone.

---

## Reproducibility Checklist (per paper)

- [ ] Code public?
- [ ] Weights public?
- [ ] Dataset public?
- [ ] Report classroom transfer?
- [ ] Report inter-rater agreement vs human coaches?
