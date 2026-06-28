# Product Design & Human Experience Architecture: PedagogyX MVP

**Version:** 3.0
**Context:** PedagogyX Phase 0 MVP (React/Next.js Web Dashboard + Meta Ray-Ban Android DAT Client).

## User & Experience Analysis

**Core Personas & Contexts:**

1. **The Teacher (Capture Persona):** Operating in a high-stress, dynamic classroom environment. They are managing 20-30 students, moving constantly, and have extremely limited cognitive bandwidth to manage technology. The primary interface is the Meta Ray-Ban smart glasses and the Android DAT client app in their pocket.
2. **The Coach/Administrator (Review Persona):** Operating in a quiet office environment. They need to rapidly synthesize data from multiple teachers, review specific classroom moments, and provide actionable feedback. The primary interface is the React/Next.js web dashboard.

**Workflows & Pain Points:**

- **Capture Workflow:** Teacher initiates session via Android app -> Glasses start streaming -> Session ends. **Pain Point:** Fumbling with the phone while students are entering the room. Uncertainty if the stream is actually working (anxiety).
- **Review Workflow:** Coach logs into web dashboard -> Selects teacher -> Reviews aggregated metrics -> Watches specific clip. **Pain Point:** Information overload on the dashboard. Difficulty finding the specific "teachable moment" in a 45-minute video.

**Emotional Considerations:**

- **Anxiety (Teachers):** Fear of being evaluated unfairly by the technology. The capture process must feel supportive, not surveillance-oriented.
- **Overwhelm (Coaches):** Too much data without insights.

**Accessibility Considerations:**

- **Mobile (Teachers):** High-contrast UI for use under varied classroom lighting. Large tap targets for quick, distracted interaction.
- **Web (Coaches):** Full WCAG 2.1 AA compliance for dashboard data visualization (color-blind friendly palettes for charts, robust keyboard navigation through complex data tables).

## UX Strategy

**1. "Zero-Friction" Capture (Mobile DAT Client):**

- **One-Tap Start:** The Android app must open directly to a massive, unmistakable "Start Session" button. No complex configuration prior to streaming.
- **Persistent Confirmation:** Once streaming begins, the UI must provide calm, continuous feedback (e.g., a slow pulsing green indicator) that streaming is active, reducing "is this working?" anxiety.
- **Post-Session Decompression:** When a session ends, provide immediate positive reinforcement ("Session securely uploaded"), not a data dump.

**2. "Insight-First" Review (Web Dashboard):**

- **Progressive Disclosure:** The web dashboard (`services/web/app/page.tsx`) must show high-level health and overview metrics first (implemented via `SchoolOverview` and `MetricsCards`). Deep-dive data (e.g., specific ASR transcripts or CV analytics) should be one click away, not cluttering the initial view.
- **Contextual Navigation:** Moving from `RecentSessionsTable` to a specific session view must maintain the context of the teacher's overall performance.
- **Error Recovery:** Clear, human-readable error states if a session fails to process, with actionable next steps (e.g., "Audio processing delayed. Check back in 5 minutes.") rather than technical error codes.

## UI Strategy

**Layout Systems:**

- **Mobile (Android):** Single-column, bottom-heavy layout for one-handed operation. Critical actions (Start/Stop) anchored to the bottom safe area.
- **Web (Next.js):** Max-width 7xl container (`max-w-7xl mx-auto`) to maintain readability on ultra-wide monitors. Card-based UI to modularize complex data (Metrics vs. Recent Sessions).

**Typography & Hierarchy:**

- Establish a strict typographic scale. Use highly legible sans-serif fonts (e.g., Inter or Roboto).
- **Web:** Large, expressive numbers for key metrics to allow instantaneous scanning by administrators.

**Visual Styling (Phase 0 Boilerplate):**

- **Colors:** Neutral gray backgrounds (`bg-gray-50`) to let data visualizations pop. Use semantic colors sparingly (Green for active/success, Red/Orange for alerts) to avoid visual noise.
- **Spacing:** Generous padding (e.g., `p-8` on main web container) to reduce cognitive density.
- **Responsiveness:** The Next.js dashboard must gracefully collapse from grid-based metric cards to a vertical stack on tablet/mobile review contexts.

## Interaction Design

**Microinteractions & Feedback:**

- **Mobile Stream Initiation:** Haptic feedback on pressing "Start Capture" followed by a smooth, un-interruptible loading animation indicating connection to the glasses.
- **Web Data Loading:** Use skeleton screens for `SchoolOverview` and `RecentSessionsTable` during API fetch (using Next.js `loading.tsx` boundaries) instead of jarring full-page spinners.

**Motion Systems:**

- Motion must be purely functional.
- **Web:** Subtle hover states on table rows to indicate interactivity. Smooth expand/collapse animations for accordion data elements. No decorative animations that distract from the data.

## Information Architecture

**Web Dashboard Navigation Structure:**

1.  **Global Header:** User profile, global search (future), school context switcher.
2.  **Dashboard Home (`/`):** High-level aggregate view (`fetchOverview`).
    - School Health & Status
    - Aggregate Metrics Cards (e.g., Total Sessions, Average Talk Time)
    - Recent Sessions Table (Actionable list)
3.  **Session Detail (`/sessions/[id]` - Future):** Deep dive into a specific recording, synchronized transcript, and extracted pedagogical metrics.
4.  **Teacher Roster (`/teachers` - Future):** List of all personnel and their individual longitudinal data.

**Discoverability:**

- Ensure that the transition from viewing an aggregate metric to viewing the underlying sessions that caused that metric is a direct, obvious path.

## Accessibility Strategy

**WCAG 2.1 AA Enforcement (Web):**

- **Color Contrast:** Ensure all text, especially secondary data labels in `MetricsCards`, meets the 4.5:1 contrast ratio against the `bg-gray-50` background.
- **Keyboard Navigation:** The `RecentSessionsTable` must be fully navigable via keyboard (Tab to focus rows, Enter to open session details). Provide visible focus states (`focus:ring`).
- **Screen Reader Support:** Use semantic HTML (`<main>`, `<header>`, `<table>`, `<th>`). Add `aria-labels` to complex data visualizations or iconography that lacks text equivalents.
- **Cognitive Accessibility:** Avoid jargon. Use clear, descriptive labels for all pedagogical metrics.

## Design System Strategy

**Component Architecture (React):**

- **Primitives:** Standardize buttons, inputs, and typography tokens.
- **Data Display:** Create reusable, accessible data visualization components (e.g., a standard `MetricCard` component that accepts title, value, trend, and status).
- **Consistency:** The current separation of `SchoolOverview`, `MetricsCards`, and `RecentSessionsTable` is a good start. These must rely on a shared set of Tailwind utility tokens to ensure visual consistency as the platform scales.

**Scalability:**

- The system must accommodate an increasing number of metrics (from `worker-cv`, `worker-asr`, `worker-metrics`) without breaking the dashboard layout. Grid systems must be fluid.

## UX Research Plan

**Phase 0/1 Validation Strategy:**

1.  **Teacher Usability Testing (Mobile):**
    - **Task:** Initiate a capture session while simulating classroom distractions (e.g., talking, walking).
    - **Metric:** Time to successful stream initiation; reported anxiety level.
2.  **Coach Workflow Validation (Web):**
    - **Task:** Identify the teacher who needs the most support based on the dashboard overview.
    - **Metric:** Task success rate; time to identification; qualitative feedback on data clarity.
3.  **Accessibility Audit:**
    - Conduct a full keyboard-only navigation test of the Next.js dashboard.
    - Run automated accessibility checks (e.g., axe-core integration in Next.js).

## Risks & Tradeoffs

- **Risk:** The physical disconnection between the Meta Ray-Ban glasses and the Android client creates interaction ambiguity (e.g., "Is the app listening, or the glasses?").
- _Tradeoff:_ We must heavily rely on the Android UI to reflect the hardware state, which may introduce slight latency, but is necessary for user confidence.
- **Risk:** Data overload on the Next.js dashboard as workers (CV, ASR) output more complex pedagogical metrics.
- _Tradeoff:_ We must ruthlessly prioritize which metrics are shown on the top-level `MetricsCards` versus burying them in detailed session views, potentially hiding valuable data from immediate view to preserve cognitive simplicity.
- **Risk:** Designing for full accessibility (WCAG AA) may constrain certain complex data visualization aesthetic choices.
- _Tradeoff:_ Accessibility is non-negotiable. We will prioritize clarity and inclusivity over trendy, low-contrast visual design.

## Agile Sprint Plan

### Sprint 1: Foundational Experience (Current Focus)

- **Design:** Standardize Tailwind color/typography tokens across the web dashboard.
- **UX:** Wireframe the "zero-friction" mobile capture flow.
- **Goal:** Establish visual consistency and basic usability for the MVP boilerplate.

### Sprint 2: Data Clarity & Accessibility

- **Design:** Redesign `MetricsCards` for higher contrast and better hierarchy.
- **UX:** Implement keyboard navigation for `RecentSessionsTable`.
- **Goal:** Ensure the dashboard is accessible and scannable.

### Sprint 3: Interaction & Feedback

- **Design:** Define loading states (skeletons) for web components.
- **UX:** Map out error states and recovery flows for API/Worker failures.
- **Goal:** Improve perceived performance and user trust.
