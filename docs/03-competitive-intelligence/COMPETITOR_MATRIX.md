# Competitive Intelligence Matrix

**Status:** Draft v0.1 | **Date:** 2026-05-19

Legend: **M** = mature, **P** = partial, **N** = none/unknown, **?** = inferred

| Capability             | Edthena      | Vosaic   | IRIS Connect    | TeachFX        | AI Sokrates       | China smart class | PedagogyX target       |
| ---------------------- | ------------ | -------- | --------------- | -------------- | ----------------- | ----------------- | ---------------------- |
| Video upload/coaching  | **M**        | **M**    | **M**           | N (audio)      | **M**             | **M**             | TBD                    |
| Timestamped feedback   | **M**        | **M**    | **M**           | P              | **M**             | P                 | **M**                  |
| ASR / transcript       | **M**        | **M**    | **M**           | **M**          | **M**             | **M**             | **M**                  |
| Talk ratio analytics   | P            | **M**    | P               | **M**          | **M**             | **M**             | **M**                  |
| AI coaching agent      | **M** (2025) | **M**    | **M**           | P              | **M**             | **M**             | **HYPOTHESIS**         |
| Live remote coaching   | N            | N        | **M** (Go Live) | N              | P                 | **M**             | Phase 2+               |
| Student face/gaze CV   | N            | P (blur) | P               | N              | P                 | **M**             | **ASSUMPTION: opt-in** |
| Whiteboard OCR         | N            | N        | N               | N              | P                 | **M**             | Phase 2+               |
| TPACK / rubric indices | P            | P        | P               | N              | **M**             | **M**             | Phase 2+               |
| Hardware ecosystem     | N            | N        | **M** (kits)    | N              | **M** (HiTeach)   | **M**             | BYOD first             |
| LMS integration        | P            | **M**    | P               | P              | P                 | P                 | Phase 2+               |
| Scale (lessons)        | ?            | ?        | 100k+ educators | District scale | **350k+ lessons** | National          | —                      |
| US FERPA posture       | **M**        | **M**    | **M**           | **M**          | ?                 | ?                 | **M**                  |
| Surveillance framing   | Low          | Low      | Low             | Low            | Medium            | **High**          | **Reject**             |

---

## Strategic White Space (Hypotheses)

1. **Explainable multimodal coaching** — evidence clips + rubric mapping better than black-box scores (gap in China systems).
2. **Privacy-tiered analytics** — same platform, config from audio-only → full CV (gap in one-size-fits-all vendors).
3. **Long-context lesson understanding** — 50–90 min unified timeline (research advancing faster than product).
4. **Human-AI hybrid coaching workflows** — coach + agent co-edit feedback (Edthena moving here).
5. **Open eval benchmarks** for classroom AI (no vendor owns this).

---

## Detailed Reports

| Vendor                     | Document                                                                     |
| -------------------------- | ---------------------------------------------------------------------------- |
| Edthena                    | [competitors/edthena.md](competitors/edthena.md)                             |
| Vosaic                     | [competitors/vosaic.md](competitors/vosaic.md)                               |
| IRIS Connect               | [competitors/iris-connect.md](competitors/iris-connect.md)                   |
| TeachFX                    | [competitors/teachfx.md](competitors/teachfx.md)                             |
| AI Sokrates / HABOOK       | [competitors/ai-sokrates.md](competitors/ai-sokrates.md)                     |
| China smart classroom      | [competitors/china-smart-classroom.md](competitors/china-smart-classroom.md) |
| Big Tech (Zoom/Teams/Meet) | [competitors/big-tech-meeting-ai.md](competitors/big-tech-meeting-ai.md)     |

---

## Business Model Summary

| Vendor        | Model                    | **[FACT]** Strength          | Weakness                          |
| ------------- | ------------------------ | ---------------------------- | --------------------------------- |
| Edthena       | B2B district SaaS        | VC3 workflow + new AI Coach  | Less multimodal CV                |
| Vosaic        | B2B SaaS (FACTS/Nelnet)  | Tagging + talk-time + LMS    | AI depth unclear vs hype          |
| IRIS Connect  | B2B + hardware kits      | Live coaching, global PD     | Hardware lock-in                  |
| TeachFX       | B2B district             | Audio simplicity, talk ratio | No video whiteboard               |
| AI Sokrates   | Platform + HiTeach SW    | Massive lesson corpus, TPACK | Taiwan-centric, surveillance risk |
| China vendors | Gov / school procurement | Full stack CV+audio          | Ethics, export limits             |

---

## Inferred Architecture Patterns (Industry)

```text
[Capture] → [Upload/API] → [Transcode] → [Object Store]
                ↓
         [Transcription ASR]
                ↓
    [NLP Analytics] + [Optional CV Pipeline]
                ↓
         [Insights DB] → [Coach UI / Dashboards]
```text

**[ASSUMPTION]** Most Western vendors are **post-hoc batch**; China vendors add **real-time edge CV**.

---

## Cost Pressure Points

| Cost driver                   | Who suffers most                      |
| ----------------------------- | ------------------------------------- |
| GPU video understanding       | Full CV platforms                     |
| Storage (raw 1080p retention) | Video-heavy vendors                   |
| ASR per minute                | TeachFX-scale audio                   |
| Human coaching labor          | Everyone (AI reduces margin pressure) |

**PedagogyX implication:** Tier processing (audio tier → single cam → multi-cam) mandatory for unit economics.
