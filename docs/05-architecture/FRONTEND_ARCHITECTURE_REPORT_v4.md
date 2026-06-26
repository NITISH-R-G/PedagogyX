# PedagogyX: Frontend Architecture & Strategy Report

**Status:** Draft v4.0
**Owner:** Senior Frontend Developer & UI Systems Architect
**Date:** 2026-06-26
**Scope:** PedagogyX Web Admin Dashboard & Frontend Ecosystem

As the Senior Frontend Developer & UI Systems Architect, this report establishes the updated frontend architecture, interaction strategy, and engineering standards for the PedagogyX ecosystem. This architecture focuses specifically on the Web Admin Dashboard utilized by school administrators and deans.

## User & Product Analysis

- **User Workflows:** Administrators need real-time monitoring of live classes (Hot Path), post-lesson review and coaching preparation (Cold Path), and automated queuing for interventions.
- **Usability Considerations:** Principals operate in high-cognitive-load, time-poor environments. The UI must aggressively prioritize actionable metrics above the fold. Preliminary vs. Authoritative data must be visually distinct.
- **Edge Cases:** Disconnected streams from mobile clients, missing authoritative scores due to inference queuing, and graceful degradation during network failures.
- **Accessibility Considerations:** Dashboards must remain legible on low-brightness screens and projectors. High contrast, tabular data scaling, and dual-language (Hindi/English) support are required.

## Frontend Architecture

- **Component Structure:** The Next.js app router application uses a strict component hierarchy. UI components are stateless and presentational (using Radix UI and Tailwind CSS 4), while feature components encapsulate domain logic and state.
- **State Management:** Server-side state and initial data fetching are handled by Next.js 15 React Server Components with aggressive caching. Client-side interactive state is managed via lightweight context or Zustand.
- **Routing:** Next.js 15 App Router is used with nested layouts for persistent navigation (Sidebars, Global Headers) while deep-linking into specific lesson routes.
- **Design System Strategy:** Tailwind CSS 4 is used with CSS-based configuration to define a single source of truth for design tokens. The system enforces strict visual mapping for statuses.

## UI/UX Strategy

- **Interaction Design:** The critical Video Scrubber must synchronize playback seamlessly with the pedagogical timeline. Focus rings and hover states are over-indexed for non-technical user discoverability.
- **Responsiveness:** The dashboard utilizes a responsive bento-box grid that collapses into a single column for tablet/mobile views, anticipating usage by principals walking the halls.
- **Accessibility:** Ensure visual reading order matches the DOM order. Semantic HTML5 maps to ARIA roles. Data tables use horizontal scroll boundaries instead of text truncation to support zoom requirements.
- **Visual Hierarchy:** Observation Coverage is prioritized. Color is used sparingly, supplementing typography weight and icons to indicate status rather than relying on color alone.
- **Animation Systems:** Purposeful, minimal 200ms ease-in-out transitions are used for expanding lists to prevent cognitive jarring without slowing down the user.

## Performance Optimization

- **Rendering Optimization:** Maximize React Server Components to ship zero JavaScript for the initial dashboard shell, isolating `"use client"` directives to interactive leaf components.
- **Lazy Loading:** Heavy dependencies such as complex charting libraries and the video player are dynamically imported.
- **Bundle Optimization:** Routine bundle audits via `@next/bundle-analyzer` and strict tree-shaking for third-party libraries.
- **Caching Strategy:** Static assets are edge-cached. Hot Path live data polls or uses SSE to minimize network overhead compared to heavy WebSockets.

## Accessibility Strategy

- **Semantic Structure:** The application is completely usable with CSS disabled, strictly adhering to header hierarchies (`<h3>` inside `<h2>`).
- **Keyboard Navigation:** Full keyboard navigation support. All interactive elements are reachable via `Tab`, and custom components like the timeline scrubber support precise seeking via arrow keys.
- **ARIA Strategy:** Use `aria-live="polite"` for non-interruptive real-time updates and apply explicit `aria-labels` to icon-only controls.
- **Responsive Accessibility:** Ensure a minimum 48x48dp touch target size on mobile and tablet layouts.

## Testing Strategy

- **Component Testing:** Vitest and React Testing Library for isolated unit testing of UI primitives and formatters.
- **Interaction Testing:** Verifying state transitions for complex components, such as drag-and-drop interactions in the video scrubber.
- **Accessibility Testing:** Integrating `axe-core` in CI and using `jest-axe` to catch contrast and ARIA violations during unit testing.
- **Regression Testing:** Automated frontend verification (e.g., Playwright) of core layouts to catch CSS regressions that break grid structures.

## Frontend DevOps

- **CI Workflows:** GitHub Actions pipeline enforces `next lint`, `vitest` unit tests, and formatting checks before merge.
- **Deployment Optimization:** Packaged as a standalone Docker container (`output: 'standalone'`) to minimize image size and cold starts for self-hosted OSS deployments.
- **Frontend Observability:** Client-side error boundaries catch exceptions and post structured JSON directly to the backend observability stack.
- **Monitoring:** Core Web Vitals (LCP, CLS, INP) are tracked, specifically simulating slow 3G/4G networks relevant to Indian schools.

## Refactoring Opportunities

- **Simplifications:** Migrate any remaining raw inline styles to Tailwind CSS utility classes.
- **Modularization:** Extract monolithic fetch logic into a structured `lib/api/` boundary.
- **Maintainability Improvements:** Enforce strict TypeScript interfaces for API responses and use ESLint rules to forbid inline styling.

## Risks & Tradeoffs

- **Browser Limitations:** Older tablets may not support CSS subgrid. Fallbacks to Flexbox are used, maintaining a balance between modern layout and baseline support.
- **Scalability Concerns:** Rapid live metric updates can overwhelm the React render cycle on low-end devices. Updates are debounced to maximize performance.
- **Performance Tradeoffs:** Heavy i18n dictionaries are dynamically loaded to ensure the default language loads instantly.

## Agile Sprint Plan

- **Sprint 06 (UI Foundation & Styling Cleanup):**
  - Priority: Modernize the design system foundation.
  - Tasks: Remove inline styles, enforce Tailwind utility classes across all components.
  - Expected UX Outcome: Consistent, polished visual hierarchy that renders quickly.
- **Sprint 07 (Real-time Metric Rendering):**
  - Priority: Optimize Hot Path update cycles.
  - Tasks: Implement debounced SSE data ingestion, optimize React Server Component boundaries for live updates.
  - Expected UX Outcome: Principals see stable, smooth live metrics without browser freezing.
- **Sprint 08 (Advanced Video Review Features):**
  - Priority: Refine the Cold Path timeline scrubber.
  - Tasks: Implement arrow-key seek navigation and synchronized transcript highlighting.
  - Expected UX Outcome: An accessible, highly responsive post-lesson review workflow.
