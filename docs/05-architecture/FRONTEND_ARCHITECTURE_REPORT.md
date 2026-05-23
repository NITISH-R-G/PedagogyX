# Frontend Architecture Report

**Status:** Draft v1.0
**Date:** 2026-05-20
**Role:** Autonomous Senior Frontend Developer & UI Systems Architect

## 1. User & Product Analysis

The primary users are school administrators (principals, deans) and teachers. Admins require high-density, real-time dashboards to monitor multiple classrooms simultaneously (Supervision Mode). Teachers need detailed, navigable timelines of their specific lessons with integrated AI feedback. The system must be accessible on potentially low-bandwidth connections and older hardware.

## 2. Frontend Architecture

We adopt a monorepo approach utilizing Next.js (React) for the web application to leverage Server-Side Rendering (SSR) for fast initial loads and SEO (if public profiles are enabled).

- **Capture Agents:** A lightweight Tauri (Rust + React) app handles desktop capture on Windows smartboards, ensuring minimal CPU footprint while hooking natively into OS media devices. Android capture utilizes a native Kotlin application.

## 3. UI/UX Strategy

- **Admin Dashboard:** Emphasizes macro-level metrics. Uses grid layouts with visual indicators (red/green) for immediate state recognition of ongoing classes.
- **Teacher Portal:** Focuses on the "Timeline Scrubber". The video player is central, augmented by overlay tracks indicating speaking time, detected activities, and AI-flagged moments.
- **Cognitive Load:** Strict minimalism. The AI generates massive amounts of data; the UI must progressively disclose this. Default views show aggregated scores, with drill-downs for raw metrics.

## 4. Performance Optimization

- **Video Playback:** Implement Adaptive Bitrate Streaming (HLS) to accommodate fluctuating school networks. Use custom WebGL/Canvas overlays for timeline metrics to avoid DOM bloat during playback.
- **State Management:** Use Zustand for lightweight global state and React Query for aggressive caching and optimistic UI updates of API requests.
- **Bundle Size:** Strict code-splitting and dynamic imports for heavy charting libraries (e.g., Recharts or Apache ECharts).

## 5. Accessibility Strategy

- **Compliance:** Target WCAG 2.2 AA.
- **Keyboard Navigation:** Critical for the video scrubber and timeline navigation.
- **Screen Readers:** Ensure ARIA labels clearly describe complex data visualizations.
- **Color Contrast:** Implement strict contrast ratios, especially for the heatmap and timeline indicators. Provide a high-contrast dark mode.

## 6. Testing Strategy

- **Unit Tests:** Vitest + React Testing Library for core component logic and utility functions.
- **E2E Tests:** Playwright to simulate complex user flows, such as uploading a video, navigating the timeline, and verifying RBAC boundaries across admin/teacher views.
- **Visual Regression:** Percy or Chromatic to prevent CSS drift in charting components.

## 7. Frontend DevOps

- **CI/CD:** GitHub Actions to run linters (ESLint, Prettier), type-checks (TypeScript strict mode), and test suites on every PR.
- **Deployment:** Vercel or custom Node.js Docker containers depending on final infrastructure decisions (aligned with OSS/self-hosted mandates, we will likely build Next.js as a standalone container deployed to AWS ECS/Swarm).

## 8. Refactoring Opportunities

- _Phase 0 status:_ We are building from scratch, but we must establish a robust Design System (Storybook) immediately to prevent component fragmentation as the team scales.

## 9. Risks & Tradeoffs

- **Risk:** Tauri capture agent stability on legacy Windows smartboards. **Tradeoff:** We sacrifice cross-platform uniformity (Electron) for extreme performance and lower memory usage, which is non-negotiable for D-10 constrained hardware.
- **Risk:** Syncing complex canvas overlays with HLS video streams. **Tradeoff:** Will require custom synchronization logic, adding engineering complexity upfront to ensure a smooth teacher review experience.

## 10. Agile Sprint Plan

- **Sprint 1:** Setup Next.js monorepo, integrate Tailwind CSS and shadcn/ui components. Build the fundamental layout shells and Auth wrapper.
- **Sprint 2:** Develop the core Video Player component with custom timeline controls. Mock API integration for timeline events.
- **Sprint 3:** Build the Admin Dashboard grid view and integrate real-time WebSockets. Build the Teacher Portfolio view.
