# PedagogyX: Frontend Architecture & Strategy Report

**Status:** Draft v3.0
**Owner:** Senior Frontend Developer & UI Systems Architect
**Date:** 2026-06-08
**Scope:** PedagogyX Web Admin Dashboard & Frontend Ecosystem

As the Senior Frontend Developer & UI Systems Architect, this report establishes the updated frontend architecture, interaction strategy, and engineering standards for the PedagogyX ecosystem. This architecture focuses specifically on the Web Admin Dashboard utilized by school administrators and deans.

---

## User & Product Analysis

- **User Workflows:** Administrators require real-time monitoring of live classes (Hot Path), post-lesson review and coaching preparation (Cold Path), and automated queuing for interventions.
- **Usability Considerations:** Principals operate in high-cognitive-load, time-poor environments. The UI aggressively prioritizes actionable metrics above the fold. Preliminary vs. Authoritative data are visually distinct to guide quick decision-making.
- **Edge Cases:** Handling disconnected streams from mobile clients, missing authoritative scores due to inference queuing, and providing graceful degradation during intermittent network failures in school environments.
- **Accessibility Considerations:** Dashboards are designed to remain legible on low-brightness screens and older projectors. High contrast modes, scalable tabular data without truncation, and dual-language (Hindi/English) support are foundational requirements.

## Frontend Architecture

- **Component Structure:** The Next.js 15 App Router application implements a strict component hierarchy. UI components are stateless and presentational (using Radix UI and Tailwind CSS v4), while feature components encapsulate domain logic and state.
- **State Management:** Server-side state and initial data fetching are handled by Next.js React Server Components with aggressive caching. Client-side interactive state is cleanly managed via lightweight React Context or Zustand, depending on global access needs.
- **Routing:** Leveraging Next.js 15 nested layouts, the architecture provides persistent navigation shells (Sidebars, Global Headers) while allowing deep-linking into specific lesson review routes.
- **Design System Strategy:** Tailwind CSS v4 is used with CSS-based configuration (`@import "tailwindcss";`) to define a single source of truth for design tokens. The system enforces strict visual mapping for application state and data statuses.

## UI/UX Strategy

- **Interaction Design:** The critical Video Scrubber synchronizes playback seamlessly with the pedagogical timeline. Focus rings and interactive hover states are over-indexed to ensure non-technical user discoverability.
- **Responsiveness:** The dashboard utilizes a responsive bento-box grid that automatically collapses into a single-column layout for tablet and mobile views, explicitly supporting principals walking the school halls.
- **Accessibility:** Ensure visual reading order strictly matches the DOM structure. Semantic HTML5 maps properly to ARIA roles. Data tables use horizontal scroll boundaries instead of text truncation to fully support zoom and localization requirements.
- **Visual Hierarchy:** Observation Coverage and key operational metrics are prioritized. Color is used sparingly, primarily supplementing typography weight and icon shapes to indicate status, avoiding reliance on color alone.
- **Animation Systems:** Purposeful, minimal 200ms ease-in-out transitions are used for expanding lists or data state changes to prevent cognitive jarring without slowing down the user experience.

## Performance Optimization

- **Rendering Optimization:** Maximize the use of React Server Components to ship zero JavaScript for the initial dashboard shell, strictly isolating `"use client"` directives to interactive leaf components.
- **Lazy Loading:** Heavy dependencies, such as complex charting libraries and the video playback engine, are dynamically imported to prioritize Time to Interactive (TTI) for core metrics.
- **Bundle Optimization:** Routine bundle audits via `@next/bundle-analyzer` are enforced in CI, along with strict tree-shaking for all third-party libraries.
- **Caching Strategy:** Static assets are edge-cached. Hot Path live data polls or uses Server-Sent Events (SSE) to minimize network overhead and maintain high responsiveness compared to heavy WebSockets.

## Accessibility Strategy

- **Semantic Structure:** The application is completely usable with CSS disabled, strictly adhering to header hierarchies (e.g., `<h3>` must reside inside `<h2>`).
- **Keyboard Navigation:** Comprehensive keyboard navigation support is built-in. All interactive elements are reachable via `Tab`, and custom components like the timeline scrubber support precise seeking via arrow keys.
- **ARIA Strategy:** Use `aria-live="polite"` for non-interruptive real-time dashboard updates and apply explicit `aria-labels` to icon-only controls.
- **Responsive Accessibility:** Ensure a minimum 48x48dp touch target size on all mobile and tablet layouts, complying with WCAG usability standards for touch devices.

## Testing Strategy

- **Component Testing:** Vitest and React Testing Library are used for highly isolated, fast unit testing of UI primitives, metric formatters, and logic hooks.
- **Interaction Testing:** Complex state transitions, such as drag-and-drop interactions in the video scrubber, are tested robustly using simulated user events.
- **Accessibility Testing:** `axe-core` is integrated into CI, and `jest-axe` is used to strictly catch contrast and ARIA violations automatically during unit test execution.
- **Regression Testing:** Automated frontend verification using Playwright of core layouts and responsive breakpoints to automatically catch CSS regressions that might break grid structures.

## Frontend DevOps

- **CI Workflows:** GitHub Actions pipeline automatically enforces `next lint`, `vitest` unit tests, and formatting checks (`prettier`, `markdownlint`) before any pull request can be merged.
- **Deployment Optimization:** The Next.js application is packaged as a standalone Docker container (`output: 'standalone'`) to drastically minimize image size and cold start times for self-hosted OSS deployment models.
- **Frontend Observability:** Client-side error boundaries consistently catch exceptions and post structured JSON directly to the backend observability stack.
- **Monitoring:** Core Web Vitals (LCP, CLS, INP) are tracked, specifically simulating slow 3G/4G networks relevant to deployment environments in Indian schools.

## Refactoring Opportunities

- **Simplifications:** Migrate any remaining raw inline styles (e.g., dynamic progress bar percentages) to Tailwind CSS utility classes where possible, or document exceptions explicitly for dynamic values.
- **Modularization:** Extract remaining monolithic fetch logic in components into the structured `lib/api/` boundary for better reusability and testing isolation.
- **Maintainability Improvements:** Enforce strict TypeScript interfaces for all API responses across the dashboard and use ESLint rules to enforce architectural boundaries and forbid anti-patterns.

## Risks & Tradeoffs

- **Browser Limitations:** Older tablets in specific school districts may not fully support CSS subgrid. Fallbacks to Flexbox are implemented, maintaining a careful balance between modern layout architecture and necessary baseline support.
- **Scalability Concerns:** Rapid live metric updates can overwhelm the React render cycle on low-end devices. Updates are strategically debounced to maximize performance and battery life.
- **Performance Tradeoffs:** Heavy i18n dictionaries are dynamically loaded to ensure the default dashboard language loads instantly, slightly delaying language-switch actions.

## Agile Sprint Plan

- **Sprint 08 (Architecture Refinement & Debt Reduction):**
  - Priority: Finalize dynamic styling cleanup and strengthen typing.
  - Tasks: Complete the extraction of API calls to `lib/api/`, enforce TypeScript coverage, and run `dev-verify.sh --docs-only` locally.
  - Expected UX Outcome: A cleaner, more stable codebase that results in fewer regression bugs affecting end users.
- **Sprint 09 (Real-time Video Review Enhancements):**
  - Priority: Finalize advanced interaction paths in the Cold Path review.
  - Tasks: Implement keyboard-accessible timeline markers and synchronize transcript highlights seamlessly with playback.
  - Expected UX Outcome: Deans experience a polished, professional video review workflow mimicking industry-leading tools.
- **Sprint 10 (Frontend Observability Rollout):**
  - Priority: Improve visibility into frontend rendering issues.
  - Tasks: Integrate advanced Core Web Vitals logging specifically mapping user interactions (INP) directly to dashboard UI freezes.
  - Expected UX Outcome: Proactive identification and resolution of slow interactions before administrators report them.
