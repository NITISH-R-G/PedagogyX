# ADR-0002: Privacy-Tiered Analytics Configuration

| Field      | Value                               |
| ---------- | ----------------------------------- |
| **Status** | Accepted — **default tier changed** |
| **Date**   | 2026-05-19 (amended)                |

## Context

Originally assumed Western default `audio_only`. Founder requires identifiable multi-cam video in India v1.

## Decision

Retain tiers for **future export markets**, but **India v1 default tenant config:**

| Tier                 | v0.1 default | India v1 default  |
| -------------------- | ------------ | ----------------- |
| `audio_only`         | Default      | Opt-in cost saver |
| `deidentified_video` | Optional     | Optional          |
| `full_video`         | Opt-in rare  | **Default**       |

Schools may downgrade tier only with legal approval + feature loss disclosure.

## Consequences

- Engineering implements full CV pipeline in Phase 1, not Phase 2
- Higher storage, GPU, and compliance cost
- `coaching` mode still available for teacher-private workflows

## Related

[ADR-0003](ADR-0003-india-supervision-v1-scope.md)
