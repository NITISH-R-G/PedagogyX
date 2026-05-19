# ADR-0005: Free & Open-Source Software First

| Field      | Value                       |
| ---------- | --------------------------- |
| **Status** | Accepted (founder-directed) |
| **Date**   | 2026-05-19                  |

## Context

Founder requires **maximize free and open-source** components; avoid proprietary cloud AI and paid APIs where OSS alternatives exist.

## Decision

### License policy

| Tier                  | Policy                                                   |
| --------------------- | -------------------------------------------------------- |
| **Preferred**         | OSI-approved licenses (MIT, Apache-2.0, BSD, PostgreSQL) |
| **Acceptable**        | LGPL, MPL (with compliance review)                       |
| **Conditional**       | AGPL (MinIO, Grafana — network use review)               |
| **Avoid default**     | Proprietary SaaS APIs (OpenAI, Deepgram, AWS Transcribe) |
| **Forbidden default** | Vendor lock-in for core path (ASR, LLM, storage, DB)     |

### Mandatory OSS components (reference stack)

See [OSS_STACK_REFERENCE.md](../06-stack-evaluation/OSS_STACK_REFERENCE.md).

### Exceptions (require ADR)

- Schools already on **Google Workspace / Microsoft 365** — optional import only, not core runtime
- Patented codecs if unavoidable (H.264) — use system FFmpeg builds

## Consequences

- All inference **self-hosted** on customer or PedagogyX on-prem metal
- Engineering owns upgrades, security patches, model cards
- No per-minute cloud ASR bill; **capital cost = RTX 5070 nodes**

## Related

[ADR-0006](ADR-0006-rtx5070-compute-budget.md)
