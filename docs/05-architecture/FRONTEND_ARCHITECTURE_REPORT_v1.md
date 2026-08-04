# PedagogyX Frontend Architecture Report

## User & Product Analysis

The primary user workflows revolve around school administrators and educational researchers reviewing teacher pedagogy via recorded classroom sessions.

- **Workflows:** Users access a dashboard summarizing key metrics ("M-A · Observation coverage" and "M-B · Time to insight"). They view recent sessions, monitoring processing status and teacher talk ratios.
- **Usability Considerations:** The interface must clearly present complex data (talk ratios, latency) in an easily scannable format. Status indicators (processing, completed, failed) need strong visual distinction.
- **Edge Cases:** Empty states (no recent sessions) need clear guidance, which is currently provided via the mock-capture instructions. API connectivity issues must be visible immediately (currently shown in the SchoolOverview component).
- **Accessibility Considerations:** The data-heavy table and metric cards require semantic structure, clear contrast, and keyboard navigability to support diverse user needs.

## Frontend Architecture

The current implementation in `services/web` utilizes a modern Next.js 15 app router architecture.

- **Component Structure:** The app is modularized into `app` (pages/layouts) and `components` (reusable UI pieces like `Header`, `MetricsCards`, `RecentSessionsTable`, `SchoolOverview`).
- **State Management:** Currently relies on server components and direct async data fetching (`fetchHealth`, `fetchOverview` in `page.tsx`). Client-side state is minimal, leveraging Next.js server-side rendering for performance.
- **Routing:** Handled by Next.js App Router. The current structure is a single-page dashboard at the root (`/`).
- **Design System Strategy:** Utilizes Tailwind CSS v4 for utility-first styling, ensuring consistency without a heavy component library overhead. The design system is nascent, embedded within component classes.

## UI/UX Strategy

- **Interaction Design:** Focuses on a clean, professional, administrative dashboard aesthetic. Status badges and metric visualizations (e.g., the coverage progress bar) provide quick cognitive mapping.
- **Responsiveness:** The layout uses Tailwind's flexbox (`flex-wrap`, `min-w-[220px]`) and auto-overflow (`overflow-x-auto`) to ensure tables and cards adapt from desktop to mobile screens.
- **Accessibility:** Uses semantic HTML (`<header>`, `<main>`, `<section>`, `<nav>`).
- **Visual Hierarchy:** Strong typography distinguishes primary metrics (3xl font) from secondary labels and contexts. The `Header` provides clear global navigation context.
- **Animation Systems:** Subtle transitions (`transition-shadow`, `transition-all duration-500 ease-out` on progress bars) enhance the premium feel without impacting performance.

## Performance Optimization

- **Rendering Optimization:** Next.js React Server Components (RSC) are used extensively, moving data fetching to the server and reducing the client JavaScript bundle size.
- **Lazy Loading:** Not currently explicitly implemented for components, but the Next.js router handles code splitting by default.
- **Bundle Optimization:** `next.config.ts` uses `output: "standalone"` which optimizes the build for Docker deployments, significantly reducing the final image size.
- **Caching Strategy:** Relies on Next.js default fetch caching.

## Accessibility Strategy

- **Semantic Structure:** The DOM is well-structured with appropriate landmarks (`main`, `header`, `nav`, `section`).
- **Keyboard Navigation:** Links and interactive elements (though currently mostly static presentation) are inherently focusable.
- **ARIA Strategy:** Currently minimal; relies heavily on native semantic HTML elements which is a good baseline, but could be enhanced for dynamic data regions.
- **Responsive Accessibility:** Ensure touch targets in tables and navigation are adequately sized on mobile devices.

## Testing Strategy

- **Component Testing:** Vitest and React Testing Library are configured (`vitest.config.ts`, `vitest.setup.ts`). Tests exist for `RecentSessionsTable.test.tsx` and `page.test.tsx`.
- **Interaction Testing:** To be expanded as more client-side interactivity is added.
- **Accessibility Testing:** Recommended to integrate `jest-axe` into the Vitest suite to automate WCAG compliance checks during component tests.
- **Regression Testing:** Core API integration logic (`api.test.ts`) is covered, ensuring the frontend gracefully handles backend contract changes.

## Frontend DevOps

- **CI Workflows:** Standard GitHub Actions (inferred via `dev-verify.sh`) validate linting, typing, and tests.
- **Deployment Optimization:** Dockerized via `services/web/Dockerfile` utilizing the standalone output for minimal, secure, and fast container deployments.
- **Frontend Observability:** Currently lacking explicit RUM (Real User Monitoring) or error boundary tracking (e.g., Sentry).
- **Monitoring:** API health is actively monitored and displayed in the UI via the `apiOk` flag in `SchoolOverview`.

## Refactoring Opportunities

- **Simplifications:** Consolidate Tailwind class strings using a utility like `clsx` or `tailwind-merge`, especially for dynamic classes (e.g., status badges in `RecentSessionsTable`).
- **Modularization:** Extract the status badge logic into a standalone `<StatusBadge />` component for reuse across future views.
- **Maintainability Improvements:** Centralize the design tokens (colors, typography) within a dedicated Tailwind configuration or CSS variables to formalize the design system.

## Risks & Tradeoffs

- **Browser Limitations:** Heavy reliance on modern CSS features (Tailwind v4) might require polyfills if older browser support is mandated, though unlikely for an admin dashboard.
- **Scalability Concerns:** As the dashboard grows, the single `page.tsx` fetching all data might become a bottleneck. Need to explore Next.js parallel routes or React Suspense for finer-grained loading states.
- **Performance Tradeoffs:** Server-side rendering (SSR) provides fast initial paint but shifts load to the Node server. If traffic spikes, caching strategies (ISR) will need tuning.

## Agile Sprint Plan

- **Milestone 1: Foundations & Robustness (Sprint 1)**
  - Implement error boundaries for resilient UI rendering.
  - Extract reusable UI primitives (`Badge`, `Card`, `ProgressBar`).
  - Integrate `jest-axe` for automated accessibility testing.
- **Milestone 2: Enhanced Interactivity (Sprint 2)**
  - Add client-side filtering and sorting to the `RecentSessionsTable`.
  - Implement pagination for session data.
- **Milestone 3: Observability & Polish (Sprint 3)**
  - Integrate Sentry for frontend error tracking.
  - Implement Web Vitals monitoring.
  - Refine mobile layouts for the data tables.
