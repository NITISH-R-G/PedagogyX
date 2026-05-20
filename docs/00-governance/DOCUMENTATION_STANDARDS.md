# Documentation Standards

## File Naming

- RFCs: `RFC-NNNN-short-title.md` (four-digit, zero-padded)
- ADRs: `ADR-NNNN-short-title.md`
- Competitors: `competitors/<vendor-slug>.md`
- Papers: `papers/<first-author-year-short-title>.md`

## Required Sections (Technical Docs)

1. **Status** — Draft | Review | Accepted | Superseded
2. **Authors / reviewers**
3. **Summary** (≤ 200 words)
4. **Context & problem**
5. **Goals / non-goals**
6. **Design** (with diagrams)
7. **Tradeoffs**
8. **Risks & mitigations**
9. **Open questions**
10. **References** (links, not bare URLs in prose without context)

## RFC Lifecycle

````text
Draft → Review (founder + tech lead) → Accepted → Implementation
                ↘ Rejected / Superseded
```text

## ADR Lifecycle

One ADR per significant irreversible decision. Supersede, do not silently edit accepted ADRs.

## Sprint Artifacts

Located under `docs/09-agile/`:

- `SPRINT_NN_PLAN.md`
- `SPRINT_NN_RETRO.md`
- Backlogs: YAML or Markdown tables with MoSCoW + risk score (1–5)

## Diagrams

Prefer **Mermaid** in Markdown for version control. Complex diagrams may later move to Excalidraw/Figma with exported PNG in `docs/assets/` (not created in Phase 0).
````
