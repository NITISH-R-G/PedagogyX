# Risk Matrix (Updated post-founder answers)

**Date:** 2026-05-19

| ID | Risk | L | I | Exp | Mitigation | Status |
|----|------|---|---|-----|------------|--------|
| R-01 | Scope ambiguity | 3 | 5 | 15 | Partial answers; D-05/10/12 open | Improved |
| R-02 | Union backlash (US) | 2 | 4 | 8 | India-first; defer US | Lower |
| R-03 | India DPDP / child data violation | **5** | **5** | **25** | Counsel, DPIA, consent | **Critical** |
| R-04 | LLM hallucination | 4 | 4 | 16 | Text-only prompts; labels | Open |
| R-05 | ASR in noisy Indian classrooms | **5** | 4 | **20** | HI+EN models; mic guidance | Open |
| R-06 | CV false engagement scores | 4 | 5 | **20** | Preliminary vs final; no student grade v1 | Open |
| R-07 | Unit economics (multi-cam GPU) | **5** | **5** | **25** | D-10 budget; edge caching | **Critical** |
| R-08 | Real-time pipeline failure at scale | 4 | 5 | 20 | Hot/cold split; degrade gracefully | New |
| R-09 | Teacher trust / public backlash | 4 | 4 | 16 | Contractual use limits | New |
| R-10 | Dual segment (K-12 + univ) dilution | 4 | 3 | 12 | Separate templates | New |
| R-11 | Screen capture PII leakage | 4 | 4 | 16 | Redact LMS chat; policies | New |
| R-12 | No success metric → wrong build | **5** | 4 | **20** | Founder pick M-A/B | Open |

---

## New Assumptions Requiring Validation

1. Indian schools will install **desktop agent** on teacher PC
2. **5–15 Mbps** uplink available per classroom
3. Admins will act on live dashboards (not ignore)
4. Universities share procurement path with K-12 (may be false)
