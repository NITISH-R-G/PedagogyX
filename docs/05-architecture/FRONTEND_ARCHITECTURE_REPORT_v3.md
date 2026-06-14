# Frontend Architecture Report v3

## User & Product Analysis

PedagogyX is an autonomous multimodal AI classroom intelligence and teacher optimization platform. The frontend web application is the primary interface through which educators, administrators, and product operators consume critical, high-latency multimodal insights (e.g., computer vision data, speech intelligence, educational analytics).

**User Workflows:**

- Users authenticate and land on the main overview dashboard.
- Users view high-level metrics for schools, such as observed rooms, target rooms, and coverage percentages.
- Users consume latency-sensitive metrics, analyzing teacher talk ratios, insight latencies, and real-time processing statuses.

**Usability Considerations:**

- Cognitive load must be minimized. Present complex AI metrics using intuitive and visually separated components.
- The interface must seamlessly handle varied processing states (e.g., `completed`, `processing`, `failed`) and clearly indicate when sessions require user attention or retry workflows.

**Edge Cases:**

- Handling API unavailability or unreachable states cleanly with fallback UI components.
- Visualizing zero-state and empty states gracefully, explicitly directing users to recovery or seeding actions (e.g., `make mock-capture`).
- Parsing incomplete metrics from the API (e.g., missing teacher talk ratios or null insight latency) without breaking the rendering loop.

**Accessibility Considerations:**

- Essential that metric cards, tables, and statuses are accessible via screen readers, employing proper semantic HTML and high-contrast color statuses.

## Frontend Architecture

The current web client (`services/web`) is built with a modern Next.js 15.x App Router stack, leveraging React 19 Server Components for high-performance server-side rendering and streamlined data fetching.

**Component Structure:**

- The architecture favors functional, stateless components (e.g., `Header`, `SchoolOverview`, `MetricsCards`, `RecentSessionsTable`) isolated in the `components/` directory.
- Root layouts handle page skeleton and metadata, while deeply nested subcomponents are highly modularized and strongly typed using TypeScript.

**State Management:**

- Application state is primarily server-driven. Data is fetched on the server during request time via async layout/page functions, minimizing client-side JS bundles.
- Minimal client state is necessary, shifting complexity from the browser to the Edge/Server using Next.js native fetching patterns (`fetch` with configurable caching schemas like `no-store`).

**Routing:**

- Next.js App Router defines routing natively via directory structures. Current routes leverage top-level root routing (`app/page.tsx`), acting as the primary entry point for dashboard insights.

**Design System Strategy:**

- Styling is powered by Tailwind CSS v4 via PostCSS, promoting highly maintainable, utility-first CSS logic directly coupled with components.
- Standardized UI tokens (colors, spacing, typography) are strictly driven by Tailwind’s utility classes, ensuring visual consistency across the platform.

## UI/UX Strategy

**Interaction Design:**

- Interactions are constrained to essential workflows. The system provides instantaneous visual feedback via hover states and transition classes (e.g., `hover:bg-gray-50/80 transition-colors` on table rows).

**Responsiveness:**

- The layout employs CSS Flexbox and Grid, with Tailwind breakpoints optimizing container widths (`max-w-7xl mx-auto`).
- Data-heavy components like tables are wrapped in responsive overflow containers (`overflow-x-auto`) to guarantee functionality on mobile and tablet contexts.

**Accessibility:**

- Core components enforce basic semantic structures (`<main>`, `<section>`, `<h2>`, `<table>`).
- Status indicators combine color-coding (emerald, amber, rose) with distinct text representations to avoid reliance on color alone.

**Visual Hierarchy:**

- The dashboard utilizes a muted, low-distraction background (`bg-gray-50`) to emphasize content cards, tables, and metrics.
- Typographic scale differentiates primary metrics from supplementary labels effectively.

**Animation Systems:**

- Animations are intentionally minimal, focused on micro-interactions (hover states, focus rings) leveraging fast CSS transitions (`transition-colors`) rather than heavy JS-driven animations.

## Performance Optimization

**Rendering Optimization:**

- Next.js Server Components eliminate unnecessary client-side React hydration for read-only metric displays, achieving ultra-fast Time to First Byte (TTFB) and minimal JavaScript payloads.

**Lazy Loading:**

- The application natively defers off-screen image loading and relies on route-based code splitting inherently provided by Next.js.

**Bundle Optimization:**

- Relying on server-side rendering prevents large API response payloads and processing logic from bleeding into the client bundle.
- Tailwind CSS v4 compilation aggressively purges unused CSS, producing minimal stylesheet artifacts.

**Caching Strategy:**

- Critical data fetching circumvents aggressive caching (`cache: "no-store"`) to guarantee real-time data representation for AI session processing. Future scaling will require investigating revalidation periods (`Next.js ISR`).

## Accessibility Strategy

**Semantic Structure:**

- Strict adherence to native HTML landmarks ensures clear parsing by assistive technologies.
- Tables are defined with accurate `<thead>`, `<tbody>`, `<tr>`, `<th>`, and `<td>` relationships.

**Keyboard Navigation:**

- Native focus management is preserved, allowing efficient tab traversal through interactive dashboard elements.

**ARIA Strategy:**

- Given the current server-rendered nature, ARIA attributes are used sparingly but correctly, relying first on semantic elements before overriding with roles.

**Responsive Accessibility:**

- Responsive tables gracefully downgrade on smaller viewports without breaking DOM flow or obscuring critical data cells.

## Testing Strategy

**Component Testing:**

- Vitest provides an ultra-fast, Vite-powered test runner executing component-level validation using React Testing Library (`@testing-library/react`).
- Key components like `RecentSessionsTable.tsx` are tested for empty state visualization and accurate data formatting.

**Interaction Testing:**

- UI edge cases (such as API failures and empty data sets) are rigorously verified through isolated component tests (`RecentSessionsTable.test.tsx`).

**Accessibility Testing:**

- Automated accessibility validations can be layered directly into Vitest suites via `jest-axe`.

**Regression Testing:**

- A comprehensive end-to-end testing suite (e.g., Playwright or Cypress) should be implemented to validate full-stack orchestration between the UI and local mock APIs.

## Frontend DevOps

**CI Workflows:**

- Code quality is strictly governed. The pipeline enforces TypeScript compilation (`next build`), Vitest suite completion (`vitest run`), and standard Next.js linting (`next lint`).

**Deployment Optimization:**

- Dockerized deployment strategy (`Dockerfile`) guarantees an immutable, production-ready frontend artifact capable of scaling across orchestration platforms.

**Frontend Observability:**

- To support "Production Readiness," the current setup must be expanded with a robust observability suite (e.g., Sentry, Datadog RUM) to track client-side rendering failures and real-world Core Web Vitals.

**Monitoring:**

- Continuous checks on the `/health` endpoint guarantee basic runtime validation and API integration stability.

## Refactoring Opportunities

**Simplifications:**

- Data extraction logic within UI components (e.g., formatting percentages) could be consolidated into standalone utility functions or custom hooks to reduce component responsibility.

**Modularization:**

- Status badges within the `RecentSessionsTable` could be extracted into a dedicated reusable `<StatusBadge />` component to standardize rendering logic.

**Maintainability Improvements:**

- Establishing a robust Storybook environment to visualize UI primitives in isolation and standardize the emerging design system.

## Risks & Tradeoffs

**Browser Limitations:**

- Heavy reliance on native overflow for responsive tables can sometimes result in sub-optimal mobile touch experiences if scroll-snapping is absent.

**Scalability Concerns:**

- Circumventing caching (`no-store`) on the dashboard ensures real-time accuracy but significantly increases load on the backend database if concurrent users spike.

**Performance Tradeoffs:**

- Fetching latency-sensitive metrics directly during Server-Side Rendering (SSR) blocks the UI render. Moving non-critical insight data to parallel fetching streams or suspense boundaries would enhance perceived performance.

## Agile Sprint Plan

**Milestones & Priorities:**

- **Sprint 1 (Current):** Establish the baseline Next.js 15 SSR architecture, implement core Vitest unit testing, and achieve zero-error local docker composition.
- **Sprint 2:** Refactor complex inline styling (e.g., Status Badges) into discrete, reusable UI components. Implement Next.js Suspense boundaries for non-critical metric fetching.
- **Sprint 3:** Introduce frontend observability (RUM) and a visual regression testing suite (Playwright/Storybook). Optimize caching via ISR for metrics that tolerate minor latency.
- **Sprint 4:** Conduct a comprehensive Web Content Accessibility Guidelines (WCAG) audit and implement advanced ARIA live regions for session processing state changes.

**Expected UX Outcomes:**

- A resilient, sub-second dashboard rendering experience, impervious to localized AI processing delays, while guaranteeing universal accessibility compliance.
