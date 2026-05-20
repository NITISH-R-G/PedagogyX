# Founder Guide — Year-1 Success Metrics (D-20)

**You asked for detail on M-A through M-F.** This guide explains each option in plain language so you can pick **one primary** metric (and optionally two secondary).

**Quick reference:** [SUCCESS_METRIC_OPTIONS.md](SUCCESS_METRIC_OPTIONS.md)

**Your status:** **TBD** — architecture will default to **M-A + M-B** until you reply `Primary: M-?`.

---

## Why you must pick one

Without a primary metric, engineering optimizes for “everything” (accuracy, speed, cost, teacher happiness) and nothing wins. Sales and pilots also need a single sentence: _“Year 1 success means **\_\_**.”_

For **PedagogyX today** (India, supervision, multi-cam, admin scores, **free pilot**):

- Metrics about **paid renewal (M-D)** matter later, not as primary in a free test year.
- Metrics about **deployment and latency (M-A, M-B)** match proving the product **works in real schools**.
- Metrics about **admin behavior (M-C)** match supervision buyers.
- Metrics about **score movement (M-E, M-F)** matter after you have baseline data (often month 2+).

---

## M-A — Observation coverage

**What it measures:** Of all classrooms you _intended_ to monitor, what fraction had at least **one fully analyzed lesson per week**?

**Example:** 20 pilot classrooms; 17 had a valid upload + score last week → **85% coverage**.

**Good if you care about:** “Is the system actually running in class, or sitting unused?”

**Pros:**

- Simple to explain to school principals.
- Fits **supervision** (“are teachers being observed with data?”).
- Works in a **free pilot** (no payment required).

**Cons:**

- Does not prove teaching improved—only that capture + pipeline ran.
- Schools can game it with short dummy sessions unless you define “valid session” (e.g. ≥ 20 minutes).

**Engineering optimizes for:** Reliable capture agents, upload, edge buffer, ingest uptime.

---

## M-B — Time-to-insight

**What it measures:** After class ends, how long until the **admin dashboard** shows a usable result (preview or final score)?

**Example:** Median **12 minutes** from “Stop lesson” to “Admin can open report.”

**Good if you care about:** Real-time / near-real-time supervision (“same day” feedback).

**Pros:**

- Directly tests your **hot + cold path** architecture (hybrid D-PROC).
- Differentiates you from “upload video, get report next week” tools.

**Cons:**

- Harder on weak school internet unless edge buffer works.
- Must define what counts as “ready” (preview talk ratio vs full pedagogy index).

**Engineering optimizes for:** Streaming ASR, queue latency, GPU scheduling, honest UI labels (“preliminary” vs “final”).

---

## M-C — Admin action rate

**What it measures:** When the system **flags** a lesson (low score, anomaly, policy trigger), what % of flags get **opened/reviewed** by an admin or coach within **48 hours**?

**Example:** 50 flagged lessons; 30 opened within 48h → **60% action rate**.

**Good if you care about:** Proving supervision is **acted on**, not just recorded.

**Pros:**

- Strong story for principals who want accountability.
- Connects AI output to human workflow.

**Cons:**

- Needs clear **flagging rules** and enough admins with time.
- Low rate might mean bad AI _or_ bad process—not easy to diagnose.

**Engineering optimizes for:** Notifications, audit logs, dashboard UX, explainability clips.

---

## M-D — Pilot renewal

**What it measures:** After a pilot period, what % of schools **sign a paid contract** (or formal paid expansion)?

**Example:** 10 pilot schools; 4 paid → **40% renewal**.

**Good if you care about:** Commercial validation.

**Pros:**

- Ultimate business metric for investors.

**Cons:**

- **Poor primary metric for your stated free pilot** with **no monetary expectations**.
- Confounded by pricing, procurement, politics—not product quality alone.

**Recommendation for you:** Track as **secondary** or defer until paid phase.

---

## M-E — Pedagogy index delta

**What it measures:** Change in your **composite Pedagogy Index** over time (talk ratio, engagement proxies, pacing, etc.) for the same teacher or school.

**Example:** Teacher median index **62 → 71** over one term.

**Good if you care about:** “Is AI scoring showing improvement?”

**Pros:**

- Aligns with your product surface (admin sees individual scores).
- Good for longitudinal pilots (universities, terms).

**Cons:**

- Needs **weeks/months** of baseline; noisy in short pilots.
- Score must be **valid** (research + rubric) or critics dismiss it.

**Engineering optimizes for:** Stable scoring, term-over-term comparability, de-biasing across subjects.

---

## M-F — Student talk ratio increase

**What it measures:** District- or school-wide **median increase** in % of lesson time where **students** are speaking (vs teacher talk).

**Example:** Median student talk **18% → 24%** after coaching program.

**Good if you care about:** Student-centered instruction narrative (similar to TeachFX marketing).

**Pros:**

- Easy for educators to understand.
- Strong efficacy story if ASR diarization is accurate (EN + HI).

**Cons:**

- Requires reliable **teacher vs student** speech separation in noisy Indian classrooms.
- Not all subjects should have high student talk (e.g. lecture-heavy university).

**Engineering optimizes for:** Diarization quality, Hindi+English ASR, calibration per grade band.

---

## Comparison table

| ID      | One-line                                 | Free pilot fit                         | Needs long baseline? |
| ------- | ---------------------------------------- | -------------------------------------- | -------------------- |
| **M-A** | Are classrooms actually analyzed weekly? | **Excellent**                          | No                   |
| **M-B** | How fast after class is data ready?      | **Excellent**                          | No                   |
| **M-C** | Do admins open flagged lessons?          | Good                                   | Some flags needed    |
| **M-D** | Do pilots convert to paid?               | **Poor primary** (no payment expected) | Yes                  |
| **M-E** | Do pedagogy scores improve over time?    | Good secondary                         | **Yes**              |
| **M-F** | Does student talk ratio rise?            | Good secondary                         | **Yes**              |

---

## Suggested defaults for PedagogyX (if you remain unsure)

| Role          | Suggestion         | Why                                                   |
| ------------- | ------------------ | ----------------------------------------------------- |
| **Primary**   | **M-A**            | Proves deployment in free school/university pilots    |
| **Secondary** | **M-B**            | Proves hybrid architecture delivers timely dashboards |
| **Secondary** | **M-C** or **M-E** | Supervision workflow vs score improvement story       |

Reply when ready: `Primary: M-A , Secondary: M-B, M-C` (example).

---

## Founder action

Copy-paste reply:

```text
Primary: M-?
Secondary: M-?, M-?  (optional)
```
