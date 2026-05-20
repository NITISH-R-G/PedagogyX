# PedagogyX — Research & Architecture Documentation Hub

**Status:** Phase 0 — **Founder Tier-1 complete** (G2 legal blocks implementation)  
**Last updated:** 2026-05-19  
**Product direction:** [India-first supervision, multi-cam real-time](../docs/01-phase0-founder-interrogation/FOUNDER_ANSWERS.md)

---

## Phase Gates

| Gate   | Criteria                    | Status                                                    |
| ------ | --------------------------- | --------------------------------------------------------- |
| **G0** | Founder Tier-1 blockers     | 🟢 **Complete**                                           |
| **G1** | Product scope locked        | 🟡 India supervision scope locked                         |
| **G2** | India DPDP legal sign-off   | 🔴 **Blocked** — counsel required                         |
| **G3** | Reference architecture v0.2 | 🟢 Draft complete                                         |
| **G4** | ML eval plan                | 🟡 Revised for EN+HI, multi-cam                           |
| **G5** | Infra cost model            | 🟡 **Internal** founder-funded pilot (D-10 = ₹0 customer) |
| **G6** | DPIA + threat model         | 🟡 India DPIA draft                                       |
| **G7** | First vertical slice spec   | 🔴 Blocked on G2 + capture agent PRD                      |

---

## Founder Decision Record

**[FOUNDER_ANSWERS.md](01-phase0-founder-interrogation/FOUNDER_ANSWERS.md)** — canonical log  
**[PRODUCT_DECISION_IMPLICATIONS.md](01-phase0-founder-interrogation/PRODUCT_DECISION_IMPLICATIONS.md)** — engineering impact  
**[SUCCESS_METRIC_OPTIONS.md](01-phase0-founder-interrogation/SUCCESS_METRIC_OPTIONS.md)** — pick primary metric  
**[FOUNDER_SUCCESS_METRICS_GUIDE.md](01-phase0-founder-interrogation/FOUNDER_SUCCESS_METRICS_GUIDE.md)** — detailed M-A…M-F guide  
**[INDIA_PILOT_DEVICE_REFERENCE.md](01-phase0-founder-interrogation/INDIA_PILOT_DEVICE_REFERENCE.md)** — smartboard/tablet OEM research (D-DEV)

---

## Key Architecture (v0.2)

- [SYSTEM_ARCHITECTURE.md](05-architecture/SYSTEM_ARCHITECTURE.md) — hot/cold paths, multi-stream
- [AI_ARCHITECTURE.md](05-architecture/AI_ARCHITECTURE.md) — pedagogy index, real-time GPU
- [INDIA_DPDP_ARCHITECTURE.md](07-compliance-ethics/INDIA_DPDP_ARCHITECTURE.md)
- [ADR-0003](08-rfc-adr/ADR-0003-india-supervision-v1-scope.md) — v1 scope

---

## Still Required from Founder

1. **D-DEV** — Log device make/model at first pilot (compatibility matrix; **any** low-end Android/Windows board in scope)

**Recorded (2026-05-19):**

- **D-PROC = C (Hybrid)** — [ADR-0008](08-rfc-adr/ADR-0008-d-proc-hybrid-central-ml.md)
- **D-05** — School / university buyer; **free pilot**, no payment expected
- **D-10** — **₹0 customer budget** per classroom (founder bears infra during test)
- **D-20** — **Primary M-A**; **Secondary M-B, M-C**
- **D-CLIENT / D-PEDAGOGY** — All low-end Android + Windows smartboards; **teacher pedagogy** monitoring/assessment

---

## Hardware & OSS (2026-05-19)

- [ADR-0005 FOSS-first](../08-rfc-adr/ADR-0005-foss-first-stack.md)
- [ADR-0006 RTX 5070](../08-rfc-adr/ADR-0006-rtx5070-compute-budget.md)
- [OSS_STACK_REFERENCE](../06-stack-evaluation/OSS_STACK_REFERENCE.md)
- [GPU_BUDGET_RTX5070](../05-architecture/GPU_BUDGET_RTX5070.md)
- [PRODUCTION_CLIENT_SPEC](../05-architecture/PRODUCTION_CLIENT_SPEC.md)
- [ADR-0007 production clients](../08-rfc-adr/ADR-0007-production-clients-low-end.md)
