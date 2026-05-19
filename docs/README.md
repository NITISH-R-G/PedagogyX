# PedagogyX — Research & Architecture Documentation Hub

**Status:** Phase 0 — **Founder Tier-1 answers received (partial)**  
**Last updated:** 2026-05-19  
**Product direction:** [India-first supervision, multi-cam real-time](../docs/01-phase0-founder-interrogation/FOUNDER_ANSWERS.md)

---

## Phase Gates

| Gate   | Criteria                    | Status                                 |
| ------ | --------------------------- | -------------------------------------- |
| **G0** | Founder Tier-1 blockers     | 🟡 **Partial** (D-05, D-10, D-12 open) |
| **G1** | Product scope locked        | 🟡 India supervision scope locked      |
| **G2** | India DPDP legal sign-off   | 🔴 **Blocked** — counsel required      |
| **G3** | Reference architecture v0.2 | 🟢 Draft complete                      |
| **G4** | ML eval plan                | 🟡 Revised for EN+HI, multi-cam        |
| **G5** | Infra cost model            | 🔴 Needs D-10 budget                   |
| **G6** | DPIA + threat model         | 🟡 India DPIA draft                    |
| **G7** | First vertical slice spec   | 🔴 Blocked on G2 + capture agent PRD   |

---

## Founder Decision Record

**[FOUNDER_ANSWERS.md](01-phase0-founder-interrogation/FOUNDER_ANSWERS.md)** — canonical log  
**[PRODUCT_DECISION_IMPLICATIONS.md](01-phase0-founder-interrogation/PRODUCT_DECISION_IMPLICATIONS.md)** — engineering impact  
**[SUCCESS_METRIC_OPTIONS.md](01-phase0-founder-interrogation/SUCCESS_METRIC_OPTIONS.md)** — pick primary metric

---

## Key Architecture (v0.2)

- [SYSTEM_ARCHITECTURE.md](05-architecture/SYSTEM_ARCHITECTURE.md) — hot/cold paths, multi-stream
- [AI_ARCHITECTURE.md](05-architecture/AI_ARCHITECTURE.md) — pedagogy index, real-time GPU
- [INDIA_DPDP_ARCHITECTURE.md](07-compliance-ethics/INDIA_DPDP_ARCHITECTURE.md)
- [ADR-0003](08-rfc-adr/ADR-0003-india-supervision-v1-scope.md) — v1 scope

---

## Still Required from Founder

1. **D-05** — Who is the economic buyer?
2. **D-10** — Budget per classroom per year (₹ or USD)
3. **D-12** — Cloud LLM yes/no; which provider?
4. **Success metric** — choose M-A through M-F
5. **Per-student admin scores** — yes or no for v1?

## Hardware & OSS (2026-05-19)

- [ADR-0005 FOSS-first](../08-rfc-adr/ADR-0005-foss-first-stack.md)
- [ADR-0006 RTX 5070](../08-rfc-adr/ADR-0006-rtx5070-compute-budget.md)
- [OSS_STACK_REFERENCE](../06-stack-evaluation/OSS_STACK_REFERENCE.md)
- [GPU_BUDGET_RTX5070](../05-architecture/GPU_BUDGET_RTX5070.md)
- [PRODUCTION_CLIENT_SPEC](../05-architecture/PRODUCTION_CLIENT_SPEC.md)
- [ADR-0007 production clients](../08-rfc-adr/ADR-0007-production-clients-low-end.md)
