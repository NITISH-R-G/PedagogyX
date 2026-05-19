# ADR-0003: India-First Supervision Scope for v1

| Field          | Value                                   |
| -------------- | --------------------------------------- |
| **Status**     | Accepted (founder-directed)             |
| **Date**       | 2026-05-19                              |
| **Supersedes** | Implicit defaults in ADR-0001, ADR-0002 |

## Context

Founder confirmed: **India**, **identifiable student video**, **real-time**, **admin individual scores**, **supervision acceptable**, **multi-cam**, **screen + mic capture**.

## Decision

v1 product defaults to **`supervision` mode**:

- Multi-stream capture: **screen + mic + ≥2 camera streams**
- **Real-time** analytics path (live admin/coach dashboard) plus post-lesson archive
- **Identifiable** student video processing permitted per tenant DPA
- **Admin-visible** per-teacher pedagogy scores and lesson-level indices
- Primary region: **India** data residency

Dual segment: **K-12** and **university** under separate org templates.

## Consequences

**Positive:**

- Aligns with high-budget Indian smart-classroom procurement
- Clear buyer story (admin visibility, district rollups)
- Differentiates from US coaching-only vendors

**Negative:**

- **ADR-0002 privacy tiers** remain but default tier is `full_video`, not `audio_only`
- **ADR-0001** superseded for v1: real-time is **in scope**, not Phase 4
- Legal cost and deployment friction increase materially
- Export to US/EU requires explicit `coaching` mode + feature flags

## Related

- [INDIA_DPDP_ARCHITECTURE.md](../07-compliance-ethics/INDIA_DPDP_ARCHITECTURE.md)
- [SYSTEM_ARCHITECTURE.md](../05-architecture/SYSTEM_ARCHITECTURE.md) (v0.2)

## Validation

- Legal sign-off (G2)
- Pilot LOI with Indian school chain or state program
