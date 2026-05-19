# ADR-0001: Post-Hoc Batch Processing Before Real-Time

| Field | Value |
|-------|-------|
| **Status** | Accepted (provisional — supersede if founder mandates live) |
| **Date** | 2026-05-19 |

## Context

Real-time classroom analytics (China platforms, IRIS Go Live) require WebRTC, edge compute, and low-latency ops. Western coaching vendors primarily use **async video review**.

## Decision

**Default architecture is post-hoc batch** after lesson upload. Real-time paths are **Phase 4** optional module.

## Consequences

**Positive:** Lower cost, simpler FERPA story, faster MVP, aligns with Edthena/Vosaic.  
**Negative:** Cannot compete on live in-ear coaching until later.

## Validation

Founder answers **D-04** in blockers document.
