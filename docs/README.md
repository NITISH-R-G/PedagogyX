# PedagogyX — Research & Architecture Documentation Hub

**Status:** Phase 0 (Foundational Research) — **No production implementation authorized**

**Last updated:** 2026-05-19  
**Branch policy:** Research and architecture docs land on `cursor/*-db7b` branches until Phase 1 gate criteria are met.

---

## Mission

PedagogyX is a planned **multimodal AI classroom intelligence and teacher optimization platform**. This repository currently holds **research-grade documentation only**—not production services.

---

## Documentation Map

| Area | Path | Purpose |
|------|------|---------|
| Governance | [00-governance/](00-governance/) | Standards, epistemic labels (fact/assumption/hypothesis) |
| Phase 0 | [01-phase0-founder-interrogation/](01-phase0-founder-interrogation/) | Founder questionnaire, decision blockers |
| Product | [02-product/](02-product/) | PRD drafts, personas, jobs-to-be-done |
| Competitive intel | [03-competitive-intelligence/](03-competitive-intelligence/) | Global competitor analysis |
| Research library | [04-research-library/](04-research-library/) | Paper summaries, datasets |
| Architecture | [05-architecture/](05-architecture/) | System, AI, data, deployment diagrams |
| Stack evaluation | [06-stack-evaluation/](06-stack-evaluation/) | Language, ML, infra tradeoffs |
| Compliance & ethics | [07-compliance-ethics/](07-compliance-ethics/) | FERPA, GDPR, DPDP, ethical guardrails |
| RFCs & ADRs | [08-rfc-adr/](08-rfc-adr/) | Proposals and architectural decisions |
| Agile | [09-agile/](09-agile/) | Backlogs, sprint plans |
| Risks | [10-risks/](10-risks/) | Risk matrix, unknowns register |

---

## Phase Gates (Implementation Forbidden Until)

| Gate | Criteria | Status |
|------|----------|--------|
| **G0** | Founder answers Phase 0 questionnaire (critical path) | 🔴 Blocked |
| **G1** | Product scope locked (market, modality, privacy posture) | 🔴 Blocked |
| **G2** | Legal/compliance posture approved per target jurisdictions | 🔴 Blocked |
| **G3** | Reference architecture + ADRs for core subsystems | 🟡 In progress |
| **G4** | ML eval plan + dataset strategy documented | 🟡 In progress |
| **G5** | Infra cost model + SLO targets | 🔴 Blocked |
| **G6** | Security threat model + DPIA draft | 🟡 In progress |
| **G7** | First vertical slice spec (contracts, schemas, observability) | 🔴 Blocked |

---

## Immediate Actions Required from Founder

1. Complete **[FOUNDER_QUESTIONNAIRE.md](01-phase0-founder-interrogation/FOUNDER_QUESTIONNAIRE.md)** — at minimum **Section A (Strategic)** and **Section P (Privacy/Ethics)**.
2. Resolve items in **[CRITICAL_DECISIONS_BLOCKERS.md](01-phase0-founder-interrogation/CRITICAL_DECISIONS_BLOCKERS.md)**.
3. Confirm or reject default **hypotheses** in [DEFINITIONS.md](00-governance/DEFINITIONS.md).

---

## How to Read This Corpus

Every substantive claim is tagged:

- **[FACT]** — externally verifiable (paper, regulation, vendor doc)
- **[ASSUMPTION]** — working default until founder confirms
- **[HYPOTHESIS]** — requires experiment or pilot
- **[SPECULATION]** — directional idea, not planned work

---

## Related Artifacts

- [RFC-0001: Platform Vision & Scope](08-rfc-adr/RFC-0001-platform-vision-and-scope.md)
- [Competitor Matrix](03-competitive-intelligence/COMPETITOR_MATRIX.md)
- [System Architecture v0.1](05-architecture/SYSTEM_ARCHITECTURE.md)
