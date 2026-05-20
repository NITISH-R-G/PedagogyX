# G2 Readiness Checklist (Founder)

**Purpose:** Single page to unblock MVP code ([SPRINT_03_MVP_PREP.md](../09-agile/SPRINT_03_MVP_PREP.md)).  
**Track counsel send:** [GitHub Issue #11](https://github.com/NITISH-R-G/PedagogyX/issues/11)

---

## Before email to counsel

| #   | Action                                      | Doc / command                                                                    |
| --- | ------------------------------------------- | -------------------------------------------------------------------------------- |
| 1   | Read engagement brief                       | [INDIA_DPDP_COUNSEL_ENGAGEMENT_BRIEF.md](INDIA_DPDP_COUNSEL_ENGAGEMENT_BRIEF.md) |
| 2   | Build attachment tarball                    | `./scripts/build-counsel-packet.sh` → `dist/pedagogyx-counsel-packet-*.tar.gz`   |
| 3   | Copy email body                             | [COUNSEL_OUTREACH_PACKAGE.md](COUNSEL_OUTREACH_PACKAGE.md)                       |
| 4   | Attach brief + architecture PDFs (optional) | Same packet                                                                      |

---

## After counsel engagement

| #   | Deliverable                         | Unblocks                                                                          |
| --- | ----------------------------------- | --------------------------------------------------------------------------------- |
| 5   | Signed legal memo (PDF off-repo OK) | **G2** — implementation code                                                      |
| 6   | Approved privacy notice EN + HI     | S02-05 → replace [wireframes](../02-product/PRIVACY_NOTICE_CONSENT_WIREFRAMES.md) |
| 7   | Consent mechanism sign-off          | K-12 pilot capture                                                                |
| 8   | Update gate in hub                  | Edit [docs/README.md](../README.md) G2 row to 🟢                                  |

---

## Parallel (not G2, but Sprint 02 exit)

| #   | Action                    | Doc                                                                                 |
| --- | ------------------------- | ----------------------------------------------------------------------------------- |
| 9   | CPU dev verify (today)    | `./scripts/dev-verify.sh`                                                           |
| 10  | GPU benchmarks (RTX 5070) | `cd benchmarks && ./bench_full_pipeline.sh gpu`                                     |
| 11  | Pilot school intake       | [PILOT_SCHOOL_INTAKE.md](../01-phase0-founder-interrogation/PILOT_SCHOOL_INTAKE.md) |
| 12  | RFC-0002 acceptance       | [RFC-0002-ACCEPTANCE.md](../08-rfc-adr/RFC-0002-ACCEPTANCE.md)                      |

---

## When all green

1. Record G2 date in `FOUNDER_ANSWERS.md` (private memo reference only).
2. Open Sprint 03 implementation PR per [RFC-0003](../08-rfc-adr/RFC-0003-monorepo-scaffold-post-g2.md).
3. First commit may create `infra/compose.dev.yaml` + `services/` skeleton.

**Agents:** do not create `services/` until G2 is 🟢 in `docs/README.md`.
