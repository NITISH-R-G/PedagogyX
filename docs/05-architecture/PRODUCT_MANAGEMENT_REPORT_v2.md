# Product Management Report v2

## Product Problem Analysis

The core problem PedagogyX aims to solve is the lack of objective, real-time, and scalable visibility into classroom dynamics, teacher performance, and student engagement.

- **User Pain Points:**
  - School and district administrators lack granular insights into daily teaching efficacy without manual observation, which is costly, unscalable, and prone to subjective bias.
  - Teachers miss out on immediate, actionable, and objective feedback required for continuous professional development.
- **Business Context:** PedagogyX intends to serve K-12 schools/districts and universities in India during its first year, providing a supervision model that captures classroom and digital activity using consumer-grade hardware constraints (offline execution, max RTX 5070 specs, 100% FOSS).
- **Constraints:** The platform must comply with the India legal sign-off (G2 pending), necessitating strict data residency and offline operational capabilities. The system must operate reliably on affordable hardware, mandating extreme efficiency in the AI models and architecture.
- **Opportunities:** There is a significant opportunity to redefine educational supervision by offering an autonomous, edge-capable, multi-modal classroom analytics tool. Creating a seamless integration of teacher-student talk ratios, attention proxies, and a composite pedagogy index establishes a defensible, high-value asset for institutional stakeholders.

## User Workflow Analysis

The user journey spans setup, real-time engagement, and post-session review.

- **Onboarding Flow:**
  - Administrators provision the offline-capable capture software on classroom desktop hardware.
  - Instructors connect physical components (≥2 camera streams, teacher/room microphones) with a clear visual recording indicator assuring users of system state.
- **User Journeys:**
  - **Teachers:** Execute the lesson. The system runs transparently with minimal intervention, buffering data locally if the network is disrupted.
  - **Admins:** Access a live dashboard that aggregates rolling analytics per school. They drill down into specific lessons to review the composite pedagogy index and discourse metrics.
- **Friction Points:** The primary friction lies in hardware reliability and the calibration of multiple streams in diverse physical classroom environments. Assuring teachers regarding privacy while delivering admin visibility will require careful UX signaling (like the visible recording indicator).
- **Engagement Loops:** The core loop relies on delivering actionable insights quickly (e.g., p95 < 8s for preview metrics). Rapid access to the final diarization and searchable transcripts (cold path SLA < 45 min) ensures admins have timely intervention data.

## Product Strategy

Our strategy is rooted in creating a defensible, cost-effective edge-AI platform for educational supervision.

- **Vision:** To become the standard operating system for classroom analytics and pedagogy improvement globally, starting with the Indian K-12 and university market.
- **Differentiation:** We differentiate through a strict 100% Free and Open Source Software (FOSS) mandate, offline data residency compliance, and the ability to run on consumer-grade RTX 5070 GPUs. This massively reduces the Total Cost of Ownership (TCO) compared to cloud-dependent alternatives.
- **Positioning:** We position PedagogyX as the secure, localized, high-performance alternative to expensive and invasive cloud-based smart classroom solutions.
- **Growth Opportunities:** Upon successfully proving the MVP and achieving the target classroom coverage (M-A), the platform can expand via module up-sells (e.g., predictive failure analysis, advanced LLM coaching summaries) and horizontal growth into new geographic regions (e.g., US FERPA-compliant deployments).

## Competitive Analysis

PedagogyX enters a space occupied by emerging ed-tech analytics and legacy observation tools.

- **Market Landscape:** The landscape features cloud-reliant smart classroom analytics (popular in China/Taiwan/India) and point solutions like AI Sokrates.
- **Competitor Strengths:** Competitors often boast massive cloud-compute backing, enabling highly complex multi-modal models without end-user hardware constraints. They have established go-to-market channels in specific regions.
- **Competitor Weaknesses:** High latency, prohibitive costs for resource-constrained schools, privacy vulnerabilities associated with continuous cloud streaming, and a lack of open-source transparency.
- **Differentiation Opportunities:** By leveraging a local-first, FOSS architecture running on accessible hardware, PedagogyX completely bypasses the high recurring costs and privacy risks of its competitors. We offer a uniquely compelling proposition to institutions prioritizing data sovereignty and cost control.

## Feature Prioritization

Features are aggressively prioritized based on core value delivery under strict hardware limits.

- **Impact Analysis:** Real-time capture (screen, audio, ≥2 cameras) and hot-path metrics (talk ratio, activity proxies) are non-negotiable for delivering the immediate visibility admins demand.
- **Effort Analysis:** Cold-path batch processing (diarization, composite index) requires substantial optimization to meet the < 45 min SLA on an RTX 5070, making it a high-effort but high-reward technical hurdle.
- **Strategic Importance:** The live admin dashboard per school is the primary interface for our target buyer (the admin). A robust local buffer on network loss is critical for the target geography.
- **Expected Outcomes:** Successful deployment of these priority features will result in the foundational MVP capable of generating the required classroom coverage and time-to-insight metrics.

## Success Metrics

Success is measured through product adoption and the efficiency of insight delivery.

- **KPIs:** Classroom coverage percentage (M-A) and Time-to-insight (M-B).
- **Retention Metrics:** Weekly Active Admins viewing the live dashboard; Percentage of recorded lessons reviewed post-session.
- **Activation Metrics:** Time from physical hardware setup to the first successful lesson recording and analytics generation.
- **Engagement Metrics:** Frequency of drill-downs from the school dashboard to individual teacher composite indexes.
- **Business Metrics:** Total Cost of Ownership (TCO) per classroom deployed, ensuring it remains viable within the Indian market context.

## Execution Plan

Execution will be phased to manage technical risk and ensure legal compliance.

- **Milestones:**
  1. Alpha: Core capture pipeline (A/V sync, local buffering) on target hardware.
  2. Beta: Hot-path analytics and live dashboard integration.
  3. RC1: Cold-path processing (diarization, searchable transcript) optimized for RTX 5070.
  4. GA (India): Full deployment pending G2 legal clearance.
- **Dependencies:** G2 legal sign-off for data residency; finalization of the optimal composite pedagogy index formula; optimization of local ML models to fit 12GB VRAM.
- **Implementation Phases:**
  - Phase 1: Infrastructure and Capture Agent.
  - Phase 2: Analytics Engine (Hot & Cold paths).
  - Phase 3: Dashboard and Access Control (RBAC).
- **Cross Functional Coordination:** Requires tight alignment between hardware procurement, AI optimization engineers, UI/UX for the admin dashboard, and legal for compliance verification.

## Risks & Tradeoffs

- **Product Risks:** The composite pedagogy index may be initially perceived as punitive if not framed correctly, leading to teacher resistance. The UI must emphasize constructive feedback.
- **Market Risks:** Delays in G2 legal sign-off could pause the India year 1 rollout.
- **Scalability Concerns:** While the offline model scales well by distributing compute to the edge, maintaining and updating software across thousands of offline nodes presents a logistical challenge.
- **Prioritization Tradeoffs:** We are explicitly trading off cloud-scale AI capabilities (e.g., massive parameter LLMs) for cost-efficiency, privacy, and low-latency edge processing. We have deprioritized iOS capture and public leaderboards for v1.

## Agile Sprint Plan

- **Sprint Goals:**
  - Sprint 1-2: Establish baseline capture reliability (screen, mic, 2x cam) with local buffering.
  - Sprint 3-4: Deploy the hot-path rolling metrics (talk ratio) and the foundational admin dashboard.
  - Sprint 5-6: Optimize the cold-path diarization pipeline to operate within the 45-minute SLA on the target RTX 5070 hardware.
- **Backlog Priorities:** Audit logging, university dean RBAC roles, post-lesson LLM summaries (pending D-12 evaluation).
- **Deliverables:** A functional, offline-capable capture agent; a responsive admin dashboard; an optimized local inference pipeline.
- **Success Criteria:** The system successfully records a 50-minute multi-modal session, buffers it during a simulated network outage, and produces the composite index within 45 minutes of session end.

## Post Launch Analysis

- **Monitoring Strategy:** Telemetry (where permitted and aggregated) on system resource utilization (GPU VRAM, thermal throttling) and hot-path metric latency (target p95 < 8s).
- **Experimentation Plan:** A/B test different visualizations of the composite pedagogy index to determine which format drives the most constructive admin-teacher dialogue.
- **Feedback Loops:** Establish a direct feedback channel for the first cohort of pilot school admins to iterate on dashboard usability and metric relevance.
- **Iteration Roadmap:** Post-launch focus will shift towards refining the AI coaching summaries, exploring live nudges (currently a secondary hypothesis), and preparing the FERPA-compliant package for the US market expansion.
