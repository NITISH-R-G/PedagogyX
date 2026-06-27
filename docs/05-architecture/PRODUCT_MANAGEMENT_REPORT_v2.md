# Product Management Report: PedagogyX MVP Strategy

## Product Problem Analysis

PedagogyX aims to solve the problem of real-time capture and analysis of educational environments and interactions without intrusive equipment, leveraging Meta Ray-Ban smart glasses for seamless capture. Current solutions require obtrusive cameras, complex manual tagging, or significant latency. The constraints include G2 legal sign-off for using production school data, requiring initial development and validation on synthetic data and a boilerplate MVP stack. Opportunities lie in providing immediate, actionable insights to educators through edge-cloud processing, combining a fast local LAN edge buffer (Go) with a scalable OSS-first AI backend in India for hot/cold path processing.

## User Workflow Analysis

- **Onboarding Flow:** Educators put on the Meta Ray-Ban glasses and authenticate via the paired Android app. The app connects to the local Go-based LAN edge buffer.
- **User Journeys:** A teacher begins a class. The glasses capture audio/video, stream it to the Android app, which buffers it to the local edge node. The edge node performs lightweight pre-processing and forwards it to the cloud API for ASR and CV analysis. The teacher later accesses a web dashboard (React/Next.js) to review metrics and insights.
- **Friction Points:** Initial device pairing, reliable LAN connectivity in school environments, and ensuring glasses battery life over a full teaching day.
- **Engagement Loops:** Teachers receive automated summaries of student engagement and instructional pacing, encouraging them to review daily feedback and adjust strategies, establishing a habit of continuous self-improvement.

## Product Strategy

- **Vision:** To seamlessly capture, analyze, and elevate the educational experience through unobtrusive AI, empowering educators with invisible yet powerful insights.
- **Differentiation:** Hybrid edge-cloud architecture enabling low-latency processing without compromising privacy or requiring heavy local compute. Reliance on consumer-grade smart glasses rather than custom, expensive hardware.
- **Positioning:** PedagogyX is the first unobtrusive, AI-powered pedagogical assistant for modern classrooms, designed for minimal setup and maximum insight.
- **Growth Opportunities:** Expanding from individual teacher feedback to institutional analytics, integrating with LMS platforms, and offering real-time coaching via audio feedback through the glasses.

## Competitive Analysis

- **Market Landscape:** The EdTech market is crowded with LMS and video-based coaching tools (e.g., Swivl, TeachFX). However, few leverage wearable smart glasses.
- **Competitor Strengths:** Existing video coaching tools have deep LMS integrations and established trust with school districts. TeachFX has strong audio-based engagement metrics.
- **Competitor Weaknesses:** Swivl requires specialized, bulky hardware. Many solutions have high latency or lack multimodal (CV + ASR) real-time processing capabilities.
- **Differentiation Opportunities:** Utilizing Meta Ray-Ban glasses offers a vastly superior, unobtrusive user experience. The Go-based edge buffer provides a unique advantage in handling poor school network infrastructure efficiently.

## Feature Prioritization

- **Impact Analysis:** Real-time ASR for speech ratio (teacher vs. student talking time) provides immediate, high-value pedagogical insight.
- **Effort Analysis:** Integrating ASR with the existing worker architecture (Redis/MinIO) is well-understood, while real-time CV poses higher latency challenges.
- **Strategic Importance:** Proving the core pipeline (Glasses -> Android -> Edge -> Cloud) is critical for MVP validation.
- **Expected Outcomes:** A functional MVP demonstrating reliable data ingestion, basic ASR/Metrics processing, and dashboard visualization on synthetic data.

## Success Metrics

- **KPIs:** System uptime, end-to-end latency (capture to dashboard availability), AI processing accuracy (ASR word error rate).
- **Retention Metrics:** Weekly Active Teachers (WAT) accessing the dashboard post-class.
- **Activation Metrics:** Time to first successful session capture.
- **Engagement Metrics:** Number of sessions captured per week per teacher, average time spent viewing the dashboard.
- **Business Metrics:** Cost per hour of processed audio/video (optimizing the OSS-first backend in India).

## Execution Plan

- **Milestones:**
  1. Complete MVP boilerplate stack (API, Web, Workers).
  2. Implement Go-based LAN edge buffer integration.
  3. Validate ASR and CV pipelines with synthetic test sessions.
- **Dependencies:** Android client readiness for Ray-Ban integration, completion of G2 legal sign-off for non-synthetic data.
- **Implementation Phases:** Phase 1: Local development with `docker compose`. Phase 2: Edge buffer integration. Phase 3: Cloud deployment and synthetic load testing.
- **Cross-Functional Coordination:** Engineering to finalize Redis/MinIO worker queues; Design to refine the Next.js dashboard UX; Legal to unblock production data.

## Risks & Tradeoffs

- **Product Risks:** Teachers may find wearing glasses distracting or uncomfortable for long periods.
- **Market Risks:** Privacy concerns from parents and school boards regarding continuous recording.
- **Scalability Concerns:** Handling concurrent video streams from multiple classrooms to the LAN edge buffer without overwhelming local network bandwidth.
- **Prioritization Tradeoffs:** De-prioritizing real-time CV analysis in favor of robust ASR and audio metrics for the MVP to ensure low latency and high reliability.

## Agile Sprint Plan

- **Sprint Goals:** Finalize the worker queues (`worker-asr`, `worker-metrics`) and ensure seamless communication with the FastAPI backend.
- **Backlog Priorities:** 1. Redis queue integration for `worker-asr`. 2. MinIO storage pipeline for raw capture data. 3. Next.js dashboard UI for metrics visualization.
- **Deliverables:** Working local MVP stack verifiable via `./scripts/dev-verify.sh`.
- **Success Criteria:** `dat-session-smoke` CI test passes reliably using the `dat_session_cli.py` simulator.

## Post Launch Analysis

- **Monitoring Strategy:** Deploy Prometheus/Grafana to monitor worker queue lengths, processing times, and API error rates.
- **Experimentation Plan:** A/B test different dashboard layouts to see which data visualizations (e.g., charts vs. text summaries) drive higher teacher engagement.
- **Feedback Loops:** Implement in-app feedback mechanisms in the Next.js dashboard and conduct weekly user interviews with pilot teachers.
- **Iteration Roadmap:** Based on MVP feedback, optimize the Go edge buffer for lower latency, introduce advanced CV features (e.g., student posture analysis), and begin scaling the India-based backend.
