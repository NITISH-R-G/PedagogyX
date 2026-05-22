# PedagogyX: Product Design Architecture & Human Experience Strategy

**Status:** Draft v0.1
**Owner:** Elite Product Design Architect
**Date:** 2026-05-19
**Scope:** India K-12 and University Market (Phase 0 / Supervision Mode)

This document establishes the foundational design systems, human-computer interaction paradigms, and product experience architecture for PedagogyX. It is designed to scale across the India market ecosystem, serving distracted teachers, highly engaged principals, and K-12/university stakeholders under strict zero-friction, zero-budget hardware constraints.

---

## User & Experience Analysis

### User Personas

1. **The Overburdened Teacher (Primary End-User, Capture Path):**
   - **Environment:** Noisy, dynamic K-12 or university classroom in India.
   - **Constraints:** Extremely low tech literacy, high cognitive load during class, fearful of punitive surveillance.
   - **Needs:** Invisible or ultra-low friction capture initiation. Absolute clarity on what is being recorded and why. Reassurance of privacy.
2. **The School Principal / Dean (Primary Admin, Insight Path):**
   - **Environment:** Office setting, frequently interrupted, managing large staff.
   - **Constraints:** Time-poor, needs high-level insight in seconds.
   - **Needs:** Instant visibility into school coverage (M-A), quick access to authoritative pedagogical metrics, clear queue of flagged lessons needing intervention.
3. **The Instructional Coach (Secondary Reviewer):**
   - **Environment:** 1:1 teacher meetings, deep review sessions.
   - **Needs:** Direct evidence (clips), objective discourse metrics (talk ratios), structured AI narratives to base coaching upon.

### Workflows & Pain Points

- **Capture Initiation (Teacher):** Friction here kills the product. Pain point: Forgotten to start, complicated setup, anxiety over indicator presence.
- **Admin Review (Principal):** Pain point: Wading through raw video. Workflow must summarize everything into immediate actionable metrics (Coverage vs. Flags).
- **Consent (Parents/Adults):** Pain point: Legal jargon. Workflow must be bite-sized, culturally adapted (English/Hindi), and non-threatening.

### Accessibility & Emotional Considerations

- **Emotional Threat:** The system is inherently surveillant (Supervision Mode). Design must strictly differentiate between "punitive tracking" and "professional development." Use empowering, neutral language.
- **Accessibility:** Users operate on varying low-end Windows/Android devices. Contrast must be high for low-brightness screens or smartboards in glare-heavy rooms.

---

## UX Strategy

### Navigation & Workflow

- **Flat Architecture:** Maximize breadth over depth. Admins should reach any flagged lesson within 2 clicks from the dashboard.
- **Progressive Disclosure:** Present high-level metrics (Coverage, Median Insight Time) first. Drill down into specific video segments only when requested.
- **Asynchronous Clarity:** Clearly demarcate "PRELIMINARY" (Hot Path) vs "AUTHORITATIVE" (Cold Path) scores to prevent knee-jerk administrative action based on incomplete data.

### Interaction Flow & Onboarding

- **Zero-Onboarding Capture:** Teachers should only need to click one massive, unmistakable button to start a lesson. The indicator must provide continuous but non-intrusive reassurance.
- **Admin Onboarding:** First login must explain the "Pedagogy Index" components (Talk balance, Engagement, etc.) so metrics are trusted, not mysterious AI black boxes.

---

## UI Strategy

### Layout Systems

- **Dashboard Grid (Admin):** Responsive bento-box grid for the principal dashboard, emphasizing widgets for Coverage (M-A) and Insight (M-B).
- **Sticky Sidebars/Headers:** Keep context (Room #, Teacher Name) perpetually visible during lesson review.

### Typography & Hierarchy

- **Typeface:** Inter or a similarly highly legible, neutral sans-serif that supports excellent Devanagari (Hindi) rendering alongside Latin text.
- **Hierarchy:** Data-heavy tables must use tabular numbers. Primary metrics (Index Score: 74/100) must command the highest visual weight on a detail page.

### Spacing & Responsiveness

- **Touch Targets:** Minimum 48x48 dp for all interactive elements (smartboard constraints for teachers, tablet usage for principals).
- **Density:** Provide a "comfortable" density for the live dashboard to allow scanning across a room, but a "compact" mode for the flagged lessons queue.

---

## Interaction Design

### Microinteractions & Feedback

- **Capture Start:** A distinct, tactile haptic/visual expansion when a lesson begins recording, fading smoothly into the persistent recording indicator.
- **Processing States:** Smooth, non-anxiety-inducing skeleton loaders and progress bars (`Uploading: 82%`) rather than harsh spinners. Explain what the system is doing ("Cloud: Processing").
- **Hover/Focus:** Clear visual elevation (drop shadow, background color shift) on lesson rows and actionable buttons to support keyboard navigation and mouse usage.

### Motion Systems

- **Purposeful Motion:** Use slide-in transitions for deep-diving into a lesson from the dashboard to maintain spatial awareness. Avoid gratuitous bouncy animations; maintain a professional, calm tone.

---

## Information Architecture

### Navigation Structure

- **Global Level (Admin):** School Overview (Home) | Live Sessions | Teachers List | Flagged Queue | Settings.
- **Local Level (Lesson Detail):** Video Player + Timeline | Pedagogy Index Breakdown | Evidence Clips | Coaching Narrative.

### Discoverability

- **Timeline Scrubbing:** The video timeline is the primary discovery tool for pedagogical insight. Highlight "low engagement" or "high teacher talk" segments directly on the scrubber track using color coding.
- **Flags:** Surface overdue/flagged items persistently in the global header or right rail.

---

## Accessibility Strategy

### WCAG Compliance

- **Color Contrast:** Strictly adhere to WCAG 2.1 AA (minimum 4.5:1 for text, 3:1 for UI components). Avoid red/green sole indicators for status (use icons + text like "↑" or "OVERDUE").
- **Keyboard Navigation:** Fully navigable via `Tab` key with highly visible, high-contrast focus rings (`:focus-visible`). Focus order must follow the visual reading order.
- **Screen Reader Support:** Semantic HTML throughout. `aria-live="polite"` for dynamic metric updates on the dashboard. Clear `aria-labels` for play/pause and timeline interactions.
- **Cognitive Accessibility:** Keep sentences short. Use clear, bilingual (Hindi/English) labels. Avoid hiding critical actions behind obscure icons (always use Icon + Text where space permits).

---

## Design System Strategy

### Scalable Primitives

- **Color Tokens:**
  - `status-success` / `status-warning` / `status-error` (mapped to accessible, non-pure hues).
  - `brand-primary` (used sparingly to guide action).
  - `surface-base` / `surface-raised` for layered architecture.
- **Component Library Requirements:**
  - **Data Tables:** Sortable, paginated, responsive.
  - **Video Player:** Custom overlay with timeline markers for pedagogical events.
  - **Status Badges:** For "LIVE", "PROCESSING", "PRELIMINARY".
  - **Indicator Applet:** The 48x48 persistent recording indicator (OS-level component design).

### Consistency & Maintainability

- Maintain a single source of truth in Figma (or equivalent), synced to CSS variables/Tailwind config in the upcoming frontend monorepo.

---

## UX Research Plan

### Validation Strategy

1. **Teacher Usability Testing (Smartboard Simulator):**
   - **Goal:** Verify the capture initiation takes < 5 seconds and the recording indicator does not cause undue anxiety.
2. **Principal Dashboard Heuristic Evaluation:**
   - **Goal:** Validate time-to-insight (M-B). Can a principal identify a flagged teacher and understand the pedagogical issue within 30 seconds of looking at the prototype?
3. **Bilingual Comprehension (Consent Flow):**
   - **Goal:** Test the Hindi/English privacy notices with non-technical parents/guardians to ensure informed consent is genuinely understood, not blindly clicked.

---

## Risks & Tradeoffs

- **Risk:** High cognitive load on the admin dashboard if too many classrooms are active simultaneously.
  - **Tradeoff:** Aggressive pagination or grouping by department may hide information but preserves usability.
- **Risk:** Teacher anxiety regarding the persistent recording indicator.
  - **Tradeoff:** It must be large enough to be legally compliant (minimum 48x48dp) but small enough not to obscure teaching material.
- **Risk:** Misinterpretation of "Preliminary" scores.
  - **Tradeoff:** We must visually degrade the importance of live scores (greyed out, italicized) compared to cold-path authoritative scores to prevent premature admin action.

---

## Agile Sprint Plan

### Sprint Priorities for Design

**Sprint 02 (Current - Pre-G2 Legal Gate):**

- Finalize Wireframes: Refine `ADMIN_LIVE_DASHBOARD_WIREFRAMES.md` and `PRIVACY_NOTICE_CONSENT_WIREFRAMES.md` against this architecture.
- Accessibility Audit: Review wireframes for contrast and semantic hierarchy.

**Sprint 03 (Post-G2 - MVP Scaffolding):**

- Design System Translation: Convert tokens into Tailwind configuration in the monorepo.
- Component Prototyping: Build the Video Player + Timeline Scrubber core component.
- Usability Testing: Conduct remote tests on the capture initiation flow with the mock agent.

**Sprint 04 (Pilot Deployment Prep):**

- Dashboard Refinement: Implement real data fetching and test cognitive load with dense data sets.
- Bilingual Implementation: Verify Hindi text rendering and layout shifts across all UI components.
