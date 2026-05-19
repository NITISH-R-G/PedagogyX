# Product Requirements Document v0.2 (India Supervision)

**Status:** 🟡 Revised per founder answers — legal G2 pending  
**Supersedes:** v0.1 US coaching assumptions

---

## 1. Target Market

| Attribute | Value |
|-----------|-------|
| Geography | **India** (year 1) |
| Segments | **K-12 schools/districts** + **universities** |
| Mode | **Supervision** — monitor & assess **teacher** teaching ability and **pedagogy** |
| Primary subject of analytics | **Teachers** (per-lesson pedagogy index), not per-student ranking |
| Client platforms | **All low-end Android boards + Windows smartboards** (profile-certified) |
| Comparable products | Smart classroom analytics (China/Taiwan/India), AI Sokrates |

---

## 2. Capture Requirements (v1)

- Desktop **screen recording** (slides, LMS, digital content)
- **Microphone** audio (classroom or teacher mic)
- **≥2 camera streams** (room + board or students)
- Synchronized timeline; local buffer on network loss
- Visible **recording indicator**

---

## 3. Analytics Requirements (v1)

**Purpose:** Measure **how well the teacher teaches** — discourse balance, engagement proxies, pacing, rubric-aligned pedagogy index — for admin review and improvement workflows.

### Real-time (hot path)

- Rolling **teacher** vs class talk ratio (preview) — informs **teaching** style, not student grades
- Activity / attention proxies at **room** level
- Live admin dashboard: **teacher** / lesson status per school

### Batch (cold path — authoritative)

- Final diarization and discourse metrics (feeds **teacher** pedagogy score)
- Multi-cam fusion
- **Composite pedagogy index per teacher per lesson** (admin-visible; primary product artifact)
- Lesson archive with searchable transcript for **coach/admin review of instruction**

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

| NFR | Target |
|-----|--------|
| Data residency | India region only |
| Hot path latency | p95 < 8s for preview metrics |
| Cold path SLA | < 45 min for 50-min lesson (TBD after GPU sizing) |
| Availability | 99.5% MVP |
| Languages | English + Hindi ASR |

---

## 6. Out of Scope v1 (Proposed)

- US FERPA-first deployment package
- Public teacher leaderboards
- **Per-student punitive scores** — **out of scope v1** (founder: focus is **teacher pedagogy**)
- iOS capture agent

---

## 7. Success Metric

**Founder selection (2026-05-19):**

| Role | Metric |
|------|--------|
| **Primary** | **M-A** — Observation coverage (% classrooms with ≥1 analyzed session/week) |
| **Secondary** | **M-B** — Time-to-insight (median minutes class end → admin dashboard ready) |
| **Secondary** | **M-C** — Admin action rate (% flagged lessons reviewed within 48h) |

See [SUCCESS_METRIC_OPTIONS.md](../01-phase0-founder-interrogation/SUCCESS_METRIC_OPTIONS.md).

---

## 8. Blockers

- India legal memo (G2)
- D-DEV: log pilot site make/model for compatibility matrix (any low-end profile-passing board)
