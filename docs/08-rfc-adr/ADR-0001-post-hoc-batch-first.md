# ADR-0001: Post-Hoc Batch Processing Before Real-Time

| Field      | Value                                                                |
| ---------- | -------------------------------------------------------------------- |
| **Status** | **Superseded** by [ADR-0003](ADR-0003-india-supervision-v1-scope.md) |
| **Date**   | 2026-05-19 (superseded same day)                                     |

## Context

Original default assumed Western async coaching vendors.

## Original Decision

Post-hoc batch first; real-time Phase 4.

## Supersession

Founder requires **real-time coaching in v1**. Architecture must implement **dual path**:

- **Hot path:** stream ingest → low-latency feature extractors → live dashboard
- **Cold path:** full lesson archive → higher-quality batch re-analysis (source of truth for scores)

Do not delete this ADR — historical record.
