# Pilot School Intake (S02-06)

**Status:** Template — founder fills before first on-site capture  
**Links:** [INDIA_PILOT_DEVICE_REFERENCE.md](INDIA_PILOT_DEVICE_REFERENCE.md) · [Issue #11](https://github.com/NITISH-R-G/PedagogyX/issues/11) (G2)

Copy this section into a private tracker or commit a redacted `pilot-sites/abc-school.md` **after** G2 (no PII in public repo until counsel approves storage).

---

## 1. Site identity

| Field                          | Value                            |
| ------------------------------ | -------------------------------- |
| Legal school / university name |                                  |
| Display name (admin UI)        |                                  |
| City, state, PIN               |                                  |
| Segment                        | K-12 / University / Both         |
| Primary contact (role)         | Principal / IT / Department head |
| Contact email / phone          | _(store off-repo if needed)_     |

---

## 2. Commercial & scope (D-05, D-10)

| Field                              | Value                            |
| ---------------------------------- | -------------------------------- |
| Paid pilot?                        | **No** (founder-funded per D-10) |
| Classrooms in scope (count)        |                                  |
| Target start date                  |                                  |
| Languages taught (EN / HI / other) |                                  |

---

## 3. Network & IT

| Field                                        | Value          |
| -------------------------------------------- | -------------- |
| Upload Mbps sustained (speed test)           |                |
| WAN outages per week (estimate)              |                |
| Edge host available? (NUC / mini-PC)         | Yes / No / TBD |
| Firewall allows HTTPS outbound to India VPS? |                |

---

## 4. Devices (per room) — repeat per classroom

Use [INDIA_PILOT_DEVICE_REFERENCE.md](INDIA_PILOT_DEVICE_REFERENCE.md) profiles (**A** / **B**), not brand allow-lists.

| Room ID | Panel brand/model | Panel Android ver. | OPS PC model | OPS RAM | Windows ver. | Profile (A/B) | Notes |
| ------- | ----------------- | ------------------ | ------------ | ------- | ------------ | ------------- | ----- |
|         |                   |                    |              |         |              |               |       |
|         |                   |                    |              |         |              |               |       |

**Teacher tablet/phone (if any):**  
**Student devices (if any):**

---

## 5. Compliance gates (do not capture until green)

| Gate                              | Status        |
| --------------------------------- | ------------- |
| G2 counsel memo received          | 🔴 / 🟢       |
| DPIA signed for this site         | 🔴 / 🟢       |
| Privacy notices EN+HI approved    | 🔴 / 🟢       |
| Parental consent artifacts (K-12) | 🔴 / 🟢 / N/A |

---

## 6. Success metrics (D-20)

| Metric                   | Target at this site               |
| ------------------------ | --------------------------------- |
| **M-A** coverage         | e.g. 15/18 rooms/week             |
| **M-B** time-to-insight  | &lt; 30 min for 45 min lesson     |
| **M-C** admin review SLA | e.g. 80% flags reviewed &lt; 48 h |

---

## Sign-off

| Role             | Name | Date |
| ---------------- | ---- | ---- |
| Founder          |      |      |
| School principal |      |      |

When complete, update `docs/README.md` pilot line and Sprint 02 S02-06 to 🟢.
