# Counsel Outreach Package (S02-01)

**Purpose:** Everything needed to **send to Indian privacy counsel in one email** — copy/paste ready.  
**Status:** Prepared by engineering; **founder must click Send** (we cannot email on your behalf).  
**Not legal advice.**  
**Full gate checklist:** [G2_READINESS_CHECKLIST.md](G2_READINESS_CHECKLIST.md)

---

## Step 1 — Build attachment bundle

From repo root:

```bash
chmod +x scripts/build-counsel-packet.sh
./scripts/build-counsel-packet.sh
```

Output: `dist/pedagogyx-counsel-packet-YYYYMMDD.tar.gz`

---

## Step 2 — Copy email (edit [brackets])

**To:** [counsel@firm.in]  
**Subject:** PedagogyX — DPDP 2023 advisory request (EdTech classroom analytics pilot, India)

```text
Dear [Name],

We are preparing a free pilot of PedagogyX, an open-source classroom analytics platform
for Indian schools and universities. The product records screen, microphone, and camera
during lessons to generate teacher pedagogy scores for school administrators (supervision
mode). We need a written legal memo under the Digital Personal Data Protection Act, 2023.

Please find attached our counsel engagement brief and supporting architecture documents.

Key facts:
- Data fiduciary: pilot school/university; PedagogyX as processor
- Children's identifiable video may be processed (K-12); adult students at university
- Storage and inference in India; hybrid LAN edge + cloud GPU
- No public cloud LLM APIs; OSS models on our infrastructure
- Free pilot; no student commercialization in v1

Requested deliverables (see brief):
1. Lawfulness memo for v1 pilot
2. DPIA template (one K-12 + one university archetype)
3. Privacy notice drafts (English + Hindi)
4. Data Processing Agreement schedule
5. Explicit go/no-go for pilot start

We can share a mutual NDA immediately and schedule a 45-minute intake call this week.

Regards,
[Founder name]
[Title]
[Phone]
```

---

## Step 3 — Firms to contact (shortlist)

Research starting points — **verify current contacts and fees yourself**:

| Firm / resource   | Focus                            | Link                                                                                        |
| ----------------- | -------------------------------- | ------------------------------------------------------------------------------------------- |
| **Trilegal**      | DPDP sector guides (education)   | https://trilegal.com/dataprotection/dpdpforeducation/                                       |
| **Khaitan & Co**  | EdTech + DPDP analysis           | https://compass.khaitanco.com/how-indias-new-data-protection-law-impacts-ed-tech-businesses |
| **Anand & Anand** | Data protection practice         | https://www.anandandanand.com/industries/digital-personal-data-protection/                  |
| **KSandK**        | EdTech & schools DPDP compliance | https://ksandk.com/data-protection-and-data-privacy/dpdp-act-compliance-for-edtech-schools/ |

**Tip:** Ask each for (a) fixed-fee pilot memo quote, (b) timeline, (c) experience with **school video/audio** processing.

---

## Step 4 — After counsel responds

| Event             | Repo action                                                                                  |
| ----------------- | -------------------------------------------------------------------------------------------- |
| Engagement signed | Add date to [SPRINT_02_PLAN.md](../09-agile/SPRINT_02_PLAN.md) S02-01                        |
| Memo received     | Store PDF **off-repo** (confidential); add summary + G2 🟢 in [docs/README.md](../README.md) |
| Notice approved   | Add `PRIVACY_NOTICE_EN.md` / `PRIVACY_NOTICE_HI.md` from counsel text                        |

**We cannot mark G2 complete without a real counsel memo.**

---

## What engineering already did for you

- [INDIA_DPDP_COUNSEL_ENGAGEMENT_BRIEF.md](INDIA_DPDP_COUNSEL_ENGAGEMENT_BRIEF.md) — 14 counsel questions
- [INDIA_DPDP_ARCHITECTURE.md](INDIA_DPDP_ARCHITECTURE.md) — technical controls
- [THREAT_MODEL_STRIDE_v0.1.md](../10-risks/THREAT_MODEL_STRIDE_v0.1.md)
- `scripts/build-counsel-packet.sh` — one-command attachment bundle
