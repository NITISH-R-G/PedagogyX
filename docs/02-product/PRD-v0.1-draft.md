# Product Requirements Document v0.2 (India Supervision)

**Status:** 🟡 Revised per founder answers — legal G2 pending  
**Supersedes:** v0.1 US coaching assumptions

---

## 1. Target Market

| Attribute           | Value                                                         |
| ------------------- | ------------------------------------------------------------- |
| Geography           | **India** (year 1)                                            |
| Segments            | **K-12 schools/districts** + **universities**                 |
| Mode                | **Supervision** (admin visibility, individual teacher scores) |
| Comparable products | Smart classroom analytics (China/Taiwan/India), AI Sokrates   |

---

## 2. Capture Requirements (v1)

- Desktop **screen recording** (slides, LMS, digital content)
- **Microphone** audio (classroom or teacher mic)
- **≥2 camera streams** (room + board or students)
- Synchronized timeline; local buffer on network loss
- Visible **recording indicator**

---

## 3. Analytics Requirements (v1)

### Real-time (hot path)

- Rolling teacher/student talk ratio (preview)
- Activity / attention proxies
- Live admin dashboard per school

### Batch (cold path — authoritative)

- Final diarization and discourse metrics
- Multi-cam fusion
- **Composite pedagogy index** per lesson (admin-visible)
- Lesson archive with searchable transcript

### AI coaching

- Post-lesson LLM summary **[pending D-12]**
- Optional live nudges **[HYPOTHESIS]** secondary priority

---

## 4. Admin & RBAC

- School/district admins: **individual teacher scores**, drill-down to lessons
- Audit log of all video/score access
- University dean role with department scope

---

## 5. Non-Functional (Draft)

| NFR              | Target                                            |
| ---------------- | ------------------------------------------------- |
| Data residency   | India region only                                 |
| Hot path latency | p95 < 8s for preview metrics                      |
| Cold path SLA    | < 45 min for 50-min lesson (TBD after GPU sizing) |
| Availability     | 99.5% MVP                                         |
| Languages        | English + Hindi ASR                               |

---

## 6. Out of Scope v1 (Proposed)

- US FERPA-first deployment package
- Public teacher leaderboards
- **Per-student punitive scores** (pending founder confirm)
- iOS capture agent

---

## 7. Success Metric

**TBD** — see [SUCCESS_METRIC_OPTIONS.md](../01-phase0-founder-interrogation/SUCCESS_METRIC_OPTIONS.md)

**Recommended primary:** M-A (classroom coverage) + M-B (time-to-insight)

---

## 8. Blockers

- D-05, D-10, D-12
- India legal memo (G2)
