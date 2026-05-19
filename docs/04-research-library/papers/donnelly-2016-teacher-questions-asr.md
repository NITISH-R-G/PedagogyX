# P-002: Identifying Teacher Questions Using ASR in Classrooms

| Field       | Value            |
| ----------- | ---------------- |
| **Authors** | Donnelly et al.  |
| **Year**    | 2016             |
| **Venue**   | ACL Workshop BEA |
| **Tags**    | CDA              |
| **Label**   | **[FACT]**       |

## Problem

Teacher questions correlate with discourse quality; manual coding does not scale.

## Method

ASR transcripts + classifier for question detection vs human coding.

## Results **[FACT]**

- F1 ≈ 0.59 for question detection (~51% over chance)
- Correlation r ≈ 0.85 between auto and human **question rates** at lesson level

## Limitations

- Not all questions are instructionally equivalent (rhetorical, managerial)
- Classroom noise degrades ASR
- English-centric; modern diarization may improve but needs re-benchmark

## PedagogyX Takeaway

**Lesson-level aggregates** can be reliable even when **utterance-level** classification is imperfect—design UX around distributions, not single-utterance accusations.

## Link

https://aclanthology.org/W16-3623.pdf
