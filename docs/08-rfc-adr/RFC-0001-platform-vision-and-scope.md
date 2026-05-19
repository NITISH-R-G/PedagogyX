# RFC-0001: Platform Vision & Scope

| Field       | Value                          |
| ----------- | ------------------------------ |
| **Status**  | Draft                          |
| **Authors** | PedagogyX Architecture (Agent) |
| **Created** | 2026-05-19                     |

## Summary

Define PedagogyX as a **multimodal classroom intelligence platform** focused on **teacher professional growth**, with tiered analytics, event-sourced lesson processing, and human-approved AI coaching.

## Motivation

Global competitors prove demand (Edthena, Vosaic, IRIS, TeachFX, AI Sokrates, China smart classroom). None combine **Western privacy posture**, **deep multimodal fusion**, and **explainable coaching** at scale.

## Proposal

### In scope (phased)

| Phase  | Capabilities                                             |
| ------ | -------------------------------------------------------- |
| **P0** | Research, architecture, compliance, eval design          |
| **P1** | Audio ingest, ASR, talk ratio, coach review UI skeleton  |
| **P2** | Video + slides, evidence clips, rubric-mapped LLM drafts |
| **P3** | District analytics, LMS/VCS integrations                 |
| **P4** | Live coaching, advanced CV (opt-in)                      |

### Out of scope (initial)

- Student summative grading
- Covert surveillance deployments
- Unreviewed admin-facing AI narratives

## Design Tenets

Listed in [SYSTEM_ARCHITECTURE.md](../05-architecture/SYSTEM_ARCHITECTURE.md).

## Alternatives Considered

| Alternative                    | Rejected because                         |
| ------------------------------ | ---------------------------------------- |
| Video-only MVP                 | TeachFX wins audio; need differentiation |
| China-first feature parity     | Legal/ethical barrier in US/EU           |
| Pure LLM wrapper on transcript | Hallucination + weak pedagogy            |

## Risks

See [RISK_MATRIX.md](../10-risks/RISK_MATRIX.md).

## Open Questions

All Tier-1 items in [CRITICAL_DECISIONS_BLOCKERS.md](../01-phase0-founder-interrogation/CRITICAL_DECISIONS_BLOCKERS.md).

## Decision

Pending founder sign-off.
