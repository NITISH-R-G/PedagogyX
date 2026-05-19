# Competitor Analysis: Big Tech Meeting & Lecture AI

**Status:** Draft | **Category:** Adjacent / platform risk

## Scope

Not direct classroom coaching vendors, but **platform gravity** for capture, transcription, and emerging "meeting intelligence."

| Platform              | Classroom-relevant capabilities                                |
| --------------------- | -------------------------------------------------------------- |
| **Zoom**              | AI Companion, summaries, clips; education SKUs                 |
| **Microsoft Teams**   | Speaker analytics, meeting recap, Education Insights ecosystem |
| **Google Meet**       | Transcripts, Gemini integration in Workspace for Education     |
| **Panopto / Echo360** | Lecture capture + search; analytics partnerships               |

---

## Threat Model

1. **Bundling** — districts already own Teams/Zoom; "good enough" coaching analytics added free
2. **Data gravity** — recordings stay in M365/Google vault
3. **Partner ecosystem** — ISVs build on Graph/APIs faster than greenfield

---

## PedagogyX Defensive Strategy **[HYPOTHESIS]**

- **Pedagogy-specific constructs** (not generic meeting summaries)
- **Integrate** via APIs (import Teams/Zoom recordings) vs competing on capture
- **Coach workflow + rubrics + longitudinal teacher growth** as moat
- **Neutrality** across LMS/VCS providers

---

## Integration Priority **[ASSUMPTION]**

| Priority | Integration                               |
| -------- | ----------------------------------------- |
| P0       | File upload (MP4/audio)                   |
| P1       | Zoom cloud recording webhook              |
| P1       | Teams recording via Graph (admin consent) |
| P2       | Google Drive / Meet exports               |
| P2       | Panopto API                               |

---

## Sources

- Vendor education blogs (verify per release); treat feature lists as **[FACT]** only when version-dated.
