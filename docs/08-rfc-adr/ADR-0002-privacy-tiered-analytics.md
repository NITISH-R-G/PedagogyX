# ADR-0002: Privacy-Tiered Analytics Configuration

| Field | Value |
|-------|-------|
| **Status** | Accepted (provisional) |
| **Date** | 2026-05-19 |

## Context

Student biometric CV creates GDPR/FERPA/union risk. Audio-only products (TeachFX) succeed with narrower data.

## Decision

Every tenant configures `privacy_tier`:

| Tier | Modalities | Student identifiability |
|------|------------|-------------------------|
| `audio_only` | Mic audio | No video |
| `deidentified_video` | Video with face blur default | No student ID |
| `full_video` | Raw video | Requires explicit legal approval + DPIA |

ML pipelines are **modular** per tier; billing and SLAs differ.

## Consequences

Engineering must enforce tier at ingest (reject upstream CV jobs). Sales must not oversell tiers.

## Validation

Founder answers **D-03**, **D-11–D-15**.
