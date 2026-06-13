# Frontend Architecture Report v3: PedagogyX Platform

## User & Product Analysis

PedagogyX is an AI classroom intelligence platform, which means the user base primarily consists of teachers, educators, administrators, and potentially researchers. These users operate in high-cognitive-load environments (classrooms) and need intuitive, fast, and accessible interfaces that do not interrupt their workflow.

- **User Workflows:** Real-time classroom monitoring, post-session analytic reviews, student engagement tracking via multimodal inputs (CV and ASR), and generating actionable pedagogical insights.
- **Usability Considerations:** Interfaces must handle dense data visualization without overwhelming the user. Key actions must be clear and readily accessible. Real-time data streams must be presented predictably.
- **Edge Cases:** Network instability in school environments; users on legacy hardware (older tablets/laptops) or lower-end mobile devices; noisy environments requiring clear visual cues over audio.
- **Accessibility Considerations:** A high priority on cognitive simplicity. Interfaces must accommodate users with varying degrees of tech-savviness, visual impairments, or motor difficulties. Screen reader compatibility and high contrast modes are essential for inclusive design.

## Frontend Architecture

PedagogyX employs a modern React/Next.js architecture (as evidenced by `services/web`).

- **Component Structure:** We utilize a modular, feature-based component hierarchy. Components are decoupled, separating UI presentation from business logic to enable high reusability across dashboards, real-time monitors, and analytics views.
- **State Management:** A tiered state management strategy. Local state (React `useState`/`useReducer`) for isolated UI elements, context API for global themes/auth, and server-state management (e.g., React Query or SWR) for caching and synchronizing analytics and AI insights from the FastAPI backend.
- **Routing:** Next.js App Router is used for file-system based routing, enabling server-side rendering (SSR) and static site generation (SSG) where appropriate, optimizing both initial load and SEO (if public-facing pages exist).
- **Design System Strategy:** Implementation of a strict, typed design system using scalable CSS architectures (e.g., Tailwind CSS). We maintain reusable primitives (Buttons, Cards, Modals, Charts) to ensure visual consistency and reduce duplicated styling logic.

## UI/UX Strategy

The PedagogyX interface is designed for elegance, polish, and clarity in complex data environments.

- **Interaction Design:** Fast, responsive interactions with immediate feedback loops. Real-time insights from `worker-cv` and `worker-asr` are animated smoothly into the view without causing layout shifts.
- **Responsiveness:** Fluid grid systems ensure the dashboard is usable on large projector screens down to mobile devices for teachers walking around the classroom.
- **Accessibility:** Built from the ground up with inclusivity. High contrast ratios, clear typography, and reduced motion capabilities.
- **Visual Hierarchy:** Critical real-time alerts (e.g., student disengagement flags) take precedence, while long-term analytics are structured hierarchically, allowing deep dives only when requested.
- **Animation Systems:** Purposeful micro-interactions. Animations are used to guide the eye to state changes (e.g., new AI insights arriving) rather than for pure decoration, ensuring they remain performant and meaningful.

## Performance Optimization

To maintain a fast, app-like feel for data-heavy educational analytics:

- **Rendering Optimization:** Heavy utilization of React concurrent features. Expensive data visualizations are offloaded to web workers or virtualized lists to maintain 60fps scrolling and interaction.
- **Lazy Loading:** Code-splitting at the route level via Next.js. Heavy third-party libraries (e.g., D3.js or Chart.js for data visualization) are loaded dynamically only when the specific analytics view is accessed.
- **Bundle Optimization:** Strict bundle-size budgets enforced in CI. Unused code is tree-shaken, and modern module formats are preferred.
- **Caching Strategy:** Aggressive edge caching for static assets. SWR/React Query handles stale-while-revalidate patterns for dynamic classroom metrics, reducing unnecessary network requests to the FastAPI backend.

## Accessibility Strategy

Accessibility is not an afterthought; it is integrated into the core component primitives.

- **Semantic Structure:** Strict adherence to semantic HTML5 (nav, main, article, section) to provide meaningful structure to assistive technologies.
- **Keyboard Navigation:** Fully navigable via keyboard. Predictable focus rings and logical tab orders are enforced across all complex data tables and interactive charts.
- **ARIA Strategy:** Minimal and deliberate use of ARIA attributes. We prefer semantic HTML first, falling back to ARIA only for complex custom widgets (like custom date pickers or multi-select dropdowns for student filtering).
- **Responsive Accessibility:** Ensuring touch targets are large enough (minimum 44x44px) on mobile and tablet devices for teachers "on the go."

## Testing Strategy

A robust testing pipeline guarantees production readiness for PedagogyX.

- **Component Testing:** Vitest and React Testing Library are used to test individual component logic and rendering in isolation, ensuring pure functions and UI components behave predictably.
- **Interaction Testing:** Simulating user events (clicks, typing, focus) on complex forms and real-time dashboards to prevent regression in critical workflows.
- **Accessibility Testing:** Automated Axe-core integration within Vitest suites to catch semantic and contrast issues early.
- **Regression Testing:** Playwright or Cypress for End-to-End (E2E) testing of critical user journeys (e.g., logging in, starting a classroom session, viewing an insight report) to ensure backend-to-frontend integration stability.

## Frontend DevOps

Seamless developer experience and reliable deployments are key.

- **CI Workflows:** GitHub Actions configured to run linting, type-checking (TypeScript), unit tests (Vitest), and bundle analysis on every pull request.
- **Deployment Optimization:** Automated Vercel or containerized Next.js deployments. Preview environments for every PR to allow visual inspection by design and product stakeholders before merging.
- **Frontend Observability:** Integration with tools like Sentry for real-time error tracking and Datadog/Vercel Analytics for monitoring Core Web Vitals (LCP, INP, CLS) in production.
- **Monitoring:** Tracking rendering failures and interaction latency, specifically around the real-time AI insight delivery pipeline, ensuring the UI does not lock up during heavy data processing.

## Refactoring Opportunities

Continuous improvement is embedded in our engineering culture.

- **Simplifications:** Auditing legacy context providers that may be causing unnecessary re-renders and migrating them to more atomic state management solutions or server-state cache.
- **Modularization:** Extracting shared chart logic and real-time WebSocket connection handling into reusable custom hooks, decoupling them from specific page components.
- **Maintainability Improvements:** Standardizing the design system tokens (colors, spacing, typography) and ensuring all components map strictly to these tokens, removing hard-coded or inline styles.

## Risks & Tradeoffs

- **Browser Limitations:** Heavy client-side processing of CV/ASR visualizations may degrade battery life or performance on older teacher devices. Tradeoff: We must degrade gracefully, showing simplified insights on low-end hardware.
- **Scalability Concerns:** Managing WebSocket connections for real-time streams across thousands of concurrent classroom sessions requires careful frontend connection handling and reconnection logic to prevent overwhelming the `api` service.
- **Performance Tradeoffs:** Rich animations and complex data visualizations improve UX but can impact Initial Load Time and Total Blocking Time. We trade some initial load weight for a richer client-side experience, mitigated through aggressive lazy-loading.

## Agile Sprint Plan

- **Sprint 1: Architecture & Design System Foundation**
  - Establish strict TypeScript configurations and ESLint rules.
  - Build and document core UI primitives (Buttons, Inputs, Cards) mapped to accessibility guidelines.
  - Set up Vitest and Vitest setup configuration.
- **Sprint 2: Core Routing & Authentication**
  - Implement Next.js App Router structure.
  - Build accessible login and onboarding flows.
  - Integrate with backend authentication.
- **Sprint 3: Real-time Dashboard MVP**
  - Develop the main classroom monitoring view.
  - Integrate server-state fetching (React Query/SWR) for AI insights.
  - Implement basic data visualizations.
- **Sprint 4: Performance & Observability**
  - Conduct bundle analysis and implement lazy-loading for charts.
  - Setup Sentry and Core Web Vitals tracking.
  - Perform E2E accessibility audits.
