# Cursor — Wearables DAT SDK documentation source

PedagogyX’s primary v1 client uses Meta’s **Wearables Device Access Toolkit (DAT)**. Cursor can index the official API reference as a persistent doc source so Chat and agents can cite it via **@Docs**.

This is a **per-developer Cursor IDE setting** (not stored in git). Each contributor should add it once on machines where they work on `clients/android-capture-dat/`.

---

## Add the doc source (one-time)

1. Open **Settings → Features → Docs**.
2. Click **Add new doc**.
3. **URL:** `https://wearables.developer.meta.com/llms.txt?full=true`
4. **Name:** `Wearables DAT SDK`
5. Save and wait for indexing to finish.

The `?full=true` query parameter pulls the **full API reference** (not only the short index).

---

## Use in Chat

1. In Cursor Chat, type **@Docs**.
2. Select **Wearables DAT SDK**.
3. Ask your question (e.g. `StreamSession`, `videoStream`, Mock Device Kit).

Combine with repo context: `@Docs Wearables DAT SDK` plus files under `clients/android-capture-dat/`.

---

## Complements (repo-local)

| Resource                                                                             | Purpose                                        |
| ------------------------------------------------------------------------------------ | ---------------------------------------------- |
| `./scripts/install-dat-skills.sh cursor`                                             | Meta agent **skills** (patterns, not full API) |
| [clients/android-capture-dat/README.md](../../clients/android-capture-dat/README.md) | PedagogyX Android module + tests               |
| [ADR-0009](../08-rfc-adr/ADR-0009-meta-rayban-primary-client.md)                     | Ray-Ban primary client decision                |
| [RFC-0004](../08-rfc-adr/RFC-0004-dat-session-bridge.md)                             | PedagogyX `/v1/dat-sessions` bridge            |

Human-readable guides (not in `llms.txt`): [MDK Android testing](https://wearables.developer.meta.com/docs/develop/dat/testing-mdk-android/).

---

## Cloud Agents

Background agents **cannot** configure your Cursor **Settings → Docs**. If you rely on DAT API details in Cloud, paste relevant excerpts into the task or ensure this file and `clients/android-capture-dat/` are in context.
