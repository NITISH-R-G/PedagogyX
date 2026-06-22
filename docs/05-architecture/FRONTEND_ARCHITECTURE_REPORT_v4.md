# PedagogyX: Frontend Architecture & Strategy Report

**Status:** Draft v4.0
**Owner:** Senior Frontend Developer & UI Systems Architect
**Date:** 2026-05-27
**Scope:** PedagogyX Web Admin Dashboard & Frontend Ecosystem

As the Senior Frontend Developer & UI Systems Architect, this report establishes the updated frontend architecture, interaction strategy, and engineering standards for the PedagogyX ecosystem. This architecture focuses specifically on the Web Admin Dashboard utilized by school administrators and deans.

## User & Product Analysis

- **User Workflows:** Administrators monitor live classes (Hot Path), conduct post-lesson reviews for coaching preparation (Cold Path), and manage automated queuing for interventions.
- **Usability Considerations:** Principals and deans operate in high-cognitive-load, time-poor environments. The UI must rapidly surface actionable metrics and clearly distinguish between preliminary and authoritative data.
- **Edge Cases:** Dropped streams from Meta Ray-Ban glasses, temporary gaps in authoritative scores during inference processing delays, and graceful degradation during network connectivity issues.
- **Accessibility Considerations:** Dashboards must remain legible on legacy, low-brightness screens or projectors. High contrast modes, tabular data scaling, and seamless dual-language (Hindi/English) support are critical.

## Frontend Architecture

- **Component Structure:** The Next.js 15 App Router is the core structure. A strict separation is maintained between stateless presentational components (using Radix UI and Tailwind CSS 4) and stateful feature components encapsulating domain logic.
- **State Management:** Next.js React Server Components (RSC) manage server-side state and data fetching. Interactive client state is localized, utilizing lightweight context and Zustand only when absolutely necessary to prevent over-engineering.
- **Routing:** Deep-linking into specific lessons uses Next.js nested layouts, maintaining persistent navigation structures like sidebars and headers across the application without re-rendering.
- **Design System Strategy:** Tailwind CSS 4 is the single source of truth for design tokens. The styling architecture ensures strict adherence to color mappings for lesson and metric statuses to maintain consistency.

## UI/UX Strategy

- **Interaction Design:** Core interactions like the post-lesson Video Scrubber synchronize playback with the pedagogical timeline intuitively. Generous focus rings and clear hover states are utilized to support non-technical users.
- **Responsiveness:** A responsive bento-box grid automatically adapts to tablet and mobile views, supporting principals who use the dashboard while walking the school halls.
- **Accessibility:** Ensure visual and DOM reading orders are aligned. Use horizontal scroll areas for data tables instead of truncating text to support visually impaired users who rely on high zoom levels.
- **Visual Hierarchy:** Observation Coverage and critical alerts are visually prominent. Color supplements typography, iconography, and layout structure rather than functioning as the sole indicator of status.
- **Animation Systems:** Purposeful and minimal 200ms ease-in-out transitions are employed for expanding and collapsing sections to reduce cognitive load without impeding user velocity.

## Performance Optimization

- **Rendering Optimization:** Leverage React Server Components to deliver zero JavaScript for the initial dashboard shell. The `"use client"` directive is strictly isolated to interactive leaf components.
- **Lazy Loading:** Complex dependencies, such as heavy charting libraries and video player implementations, are dynamically imported to improve initial page load times.
- **Bundle Optimization:** Perform routine bundle analysis via `@next/bundle-analyzer`. Ensure strict tree-shaking and mindful inclusion of third-party dependencies.
- **Caching Strategy:** Edge-caching is applied to static assets. Real-time Hot Path data utilizes Server-Sent Events (SSE) or efficient polling to reduce network overhead compared to WebSockets.

## Accessibility Strategy

- **Semantic Structure:** The application adheres to strict HTML5 semantics, maintaining proper header hierarchies (e.g., `<h3>` inside `<h2>`), remaining usable even if CSS fails to load.
- **Keyboard Navigation:** All interactive elements must be accessible via keyboard. Custom components like the timeline scrubber natively support arrow key navigation for precise seeking.
- **ARIA Strategy:** Use `aria-live="polite"` for non-interruptive real-time updates and apply explicit `aria-labels` to all icon-only controls for screen reader compatibility.
- **Responsive Accessibility:** Ensure a minimum touch target size of 48x48dp on all mobile and tablet layouts to prevent accidental misclicks.

## Testing Strategy

- **Component Testing:** Vitest and React Testing Library are used for isolated unit testing of UI primitives, formatters, and logic hooks.
- **Interaction Testing:** Complex state transitions, such as drag-and-drop operations in the video timeline scrubber, are thoroughly verified.
- **Accessibility Testing:** `axe-core` is integrated into the CI pipeline, and `jest-axe` is used during unit testing to prevent contrast and ARIA regressions.
- **Regression Testing:** Automated frontend verification using Playwright protects core layouts, ensuring CSS changes do not break critical grid structures.

## Frontend DevOps

- **CI Workflows:** GitHub Actions enforces strict checks: `next lint`, formatting validation, and `vitest` unit tests must pass prior to merging any pull requests.
- **Deployment Optimization:** The application is packaged as a standalone Docker container (`output: 'standalone'`) to minimize image sizes and cold start times for self-hosted OSS deployments.
- **Frontend Observability:** Client-side error boundaries are implemented to catch exceptions gracefully, sending structured JSON logs directly to the centralized backend observability stack.
- **Monitoring:** Core Web Vitals (LCP, CLS, INP) are continuously tracked. Network throttling simulating slow 3G/4G connections relevant to Indian school environments is part of routine profiling.

## Refactoring Opportunities

- **Simplifications:** Complete the migration of any remaining raw inline styles to Tailwind CSS utility classes to unify the styling architecture.
- **Modularization:** Further abstract monolithic data fetching logic into structured utility boundaries within `lib/api/` for improved maintainability.
- **Maintainability Improvements:** Standardize TypeScript interfaces for API contracts and enforce ESLint rules to strictly forbid inline styling across the codebase.

## Risks & Tradeoffs

- **Browser Limitations:** Legacy tablets deployed in schools may lack support for modern CSS features like subgrid. Fallbacks utilizing Flexbox are maintained to balance modern layout techniques with required baseline support.
- **Scalability Concerns:** Rapid live metric updates risk overwhelming the React render cycle on low-end devices. Updates must be debounced and batched to maintain performance.
- **Performance Tradeoffs:** To ensure the default application language loads instantly, heavy internationalization (i18n) dictionaries for secondary languages are dynamically loaded on demand.

## Agile Sprint Plan

- **Sprint 06 (UI Foundation & Styling Cleanup):**
  - Priority: Modernize and solidify the design system foundation.
  - Tasks: Remove legacy inline styles, enforce Tailwind utility classes globally, and standardize component interfaces.
  - Expected UX Outcome: A consistent, polished visual hierarchy that renders quickly and predictably.
- **Sprint 07 (Real-time Metric Rendering):**
  - Priority: Optimize Hot Path update cycles for performance.
  - Tasks: Implement debounced SSE data ingestion and optimize React Server Component boundaries for live data streams.
  - Expected UX Outcome: Administrators view stable, smooth live metrics without browser stuttering or freezing.
- **Sprint 08 (Advanced Video Review Features):**
  - Priority: Refine and enhance the Cold Path timeline scrubber experience.
  - Tasks: Implement advanced keyboard navigation (arrow-key seeking) and synchronized transcript highlighting for video playback.
  - Expected UX Outcome: An accessible, highly responsive, and efficient post-lesson review workflow.
