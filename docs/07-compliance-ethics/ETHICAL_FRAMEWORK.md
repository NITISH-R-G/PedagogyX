# Ethical Framework — Revised for Supervision Mode

**Status:** Draft — **founder chose supervision posture**; ethics board review still required

---

## Declared Product Stance (2026-05-19)

PedagogyX v1 targets **India K-12 and university** buyers who want:

- **Administrative visibility** into teaching quality
- **Real-time and historical** analytics
- **Identifiable** classroom video where legally consented
- Feature parity with **smart classroom / 督导-class** systems in some markets

This is **not** the same ethical posture as US teacher-coaching-first vendors.

---

## Guardrails We Still Enforce

1. **Contractual purpose limitation** — education quality only
2. **No advertising / no sale of student profiles**
3. **Audit logs** on all admin access
4. **Consent artifacts** stored per session
5. **Deletion** on fiduciary request within SLA
6. **No public teacher shaming** — scores not published to students/parents by default **[ASSUMPTION]**
7. **Preliminary vs final** labels on real-time scores

---

## Elevated Risks (Founder-Accepted Tradeoffs)

| Risk | Mitigation |
|------|------------|
| Chilling effect on student participation | Schools disclose recording; classroom signage |
| Teacher morale / union issues | Less acute in India context but monitor; coaching use case messaging |
| Algorithmic bias across regions/languages | Disaggregated eval; human spot audits |
| Children’s psychological harm from being scored | **No individual student grades in v1 admin UI** **[PROPOSAL — confirm]** |
| Scope creep to punitive HR | Contract clause: scores not sole employment input |

---

## Modes (Technical)

| Mode | When |
|------|------|
| `supervision` | India v1 default |
| `coaching` | Teacher-private reflection; de-id options |
| `research` | Anonymized exports only |

Export to US/EU requires mode downgrade + legal review.

---

## Open Founder Decision

**Should v1 show per-student engagement scores to admins?**

- Founder said identifiable video **yes** and admin pedagogy scores **yes**
- **Per-student** scoring not explicitly confirmed — **default OFF** until answered
