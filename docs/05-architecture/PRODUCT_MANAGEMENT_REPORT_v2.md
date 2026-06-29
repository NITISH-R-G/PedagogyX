# Product Management Report

## Product Problem Analysis

The core problem PedagogyX aims to solve is the lack of objective, real-time, and scalable visibility into classroom dynamics, teacher performance, and student engagement.

- **User Pain Points:**
  - School and district administrators lack granular insights into daily teaching efficacy without manual observation, which is costly, unscalable, and prone to subjective bias.
  - Teachers miss out on immediate, actionable, and objective feedback required for continuous professional development.
- **Business Context:** PedagogyX intends to serve K-12 schools/districts and universities in India during its first year. The platform has pivoted to prioritize Meta Ray-Ban smart glasses (via Wearables DAT and Android companion app) as the primary v1 capture client, offering an unobtrusive, wearable-first supervision model.
- **Constraints:** The platform must comply with the India legal sign-off (G2 pending), necessitating strict data residency and offline operational capabilities for the processing nodes. The system utilizes a hybrid D-PROC architecture, where edge capture is forwarded to centralized (but fully FOSS and localized) GPU workers running on RTX 5070 hardware.
- **Opportunities:** There is a significant opportunity to redefine educational supervision by offering an autonomous, wearable-first multi-modal classroom analytics tool. Using POV video and high-quality audio from smart glasses allows for unprecedented, naturalistic capture of the teaching experience, establishing a defensible, high-value asset for institutional stakeholders.

## User Workflow Analysis

The user journey centers around the new wearable-first paradigm, spanning setup, real-time engagement, and post-session review.

- **Onboarding Flow:**
  - Administrators provision the PedagogyX Android host application on teacher or school-provided smartphones.
  - Teachers pair their Meta Ray-Ban glasses to the host application via Bluetooth and the Wearables DAT.
  - Clear visual and audio indicators on the glasses and phone assure users of the recording state and compliance with privacy policies.
- **User Journeys:**
  - **Teachers:** Execute the lesson wearing the smart glasses. The Android app buffers and streams the POV video and audio transparently, handling network disruptions locally.
  - **Admins:** Access a live dashboard that aggregates rolling analytics per school. They drill down into specific lessons to review the composite pedagogy index and discourse metrics.
- **Friction Points:** The primary friction lies in ensuring seamless Bluetooth connectivity and battery management for the glasses over a full teaching day. Assuring teachers regarding privacy, particularly with a body-worn camera, requires careful UX signaling and strict adherence to the privacy notice wireframes.
- **Engagement Loops:** The core loop relies on delivering actionable insights quickly. Rapid access to the final diarization and searchable transcripts (cold path SLA < 45 min) ensures admins have timely intervention data.

## Product Strategy

Our strategy is rooted in creating a defensible, cost-effective edge-AI platform using consumer wearable technology for educational supervision.

- **Vision:** To become the standard operating system for classroom analytics and pedagogy improvement globally, starting with the Indian K-12 and university market via an innovative wearable-first approach.
- **Differentiation:** We differentiate through our primary client interface—Meta Ray-Ban smart glasses—which provides a more natural and less intrusive capture method than fixed smartboards. Combined with a strict 100% Free and Open Source Software (FOSS) mandate and RTX 5070 compute budget, we drastically reduce TCO.
- **Positioning:** We position PedagogyX as the secure, localized, wearable-enabled alternative to expensive and invasive cloud-based smart classroom solutions.
- **Growth Opportunities:** Upon successfully proving the MVP with wearable capture and achieving target classroom coverage (M-A), the platform can expand to support smartboards as secondary/fallback clients and explore advanced LLM coaching summaries and horizontal geographic expansion.

## Competitive Analysis

PedagogyX enters a space occupied by emerging ed-tech analytics and legacy observation tools.

- **Market Landscape:** The landscape features cloud-reliant smart classroom analytics (popular in China/Taiwan/India) and point solutions like AI Sokrates. Most competitors rely on fixed room installations.
- **Competitor Strengths:** Competitors often boast massive cloud-compute backing, enabling highly complex multi-modal models. They have established go-to-market channels and fixed-hardware deployment playbooks.
- **Competitor Weaknesses:** Fixed installations are expensive, inflexible, and highly visible, often changing teacher behavior. They suffer from high latency, privacy vulnerabilities associated with continuous cloud streaming, and a lack of open-source transparency.
- **Differentiation Opportunities:** By leveraging a wearable-first (Meta Ray-Ban) approach paired with a localized FOSS architecture, PedagogyX bypasses the high recurring costs and privacy risks of competitors while capturing a superior, first-person perspective of classroom dynamics.

## Feature Prioritization

Features are aggressively prioritized based on the new wearable capture path and core value delivery under strict hardware limits.

- **Impact Analysis:** Robust integration with the Wearables DAT (streaming POV video + audio to the Android host) and hot-path metrics (talk ratio, activity proxies) are non-negotiable for the v1 pilot.
- **Effort Analysis:** Cold-path batch processing (diarization, composite index) requires substantial optimization to meet the < 45 min SLA on an RTX 5070. Handling Bluetooth stream stability and Android battery optimization are high-effort mobile engineering tasks.
- **Strategic Importance:** The DAT session lifecycle management and the live admin dashboard are critical. A robust local buffer on the Android phone during network loss is essential for the target geography.
- **Expected Outcomes:** Successful deployment will result in a functional MVP running on Meta Ray-Ban glasses, capable of generating the required classroom coverage and time-to-insight metrics.

## Success Metrics

Success is measured through product adoption and the efficiency of insight delivery, tailored to the wearable experience.

- **KPIs:** Classroom coverage percentage (M-A) and Time-to-insight (M-B).
- **Retention Metrics:** Weekly Active Admins viewing the live dashboard; Percentage of recorded lessons reviewed post-session.
- **Activation Metrics:** Time from pairing the glasses to the Android app to the first successful lesson recording and analytics generation.
- **Engagement Metrics:** Session completion rate without dropped Bluetooth connections or battery exhaustion; Frequency of drill-downs to individual teacher composite indexes.
- **Business Metrics:** Total Cost of Ownership (TCO) per classroom deployed, demonstrating the cost-efficiency of the mobile+wearable approach.

## Execution Plan

Execution will be phased to manage technical risk, hardware integration, and ensure legal compliance.

- **Milestones:**
  1. Alpha: Core DAT integration (`StreamSession` in Android app), handling live frames, local buffering, and chunked upload to `/v1/dat-sessions`.
  2. Beta: End-to-end integration with Mock Device Kit and subsequent physical glasses testing; hot-path analytics.
  3. RC1: Cold-path processing (diarization, searchable transcript) optimized for RTX 5070 using wearable audio/video feeds.
  4. GA (India): Full deployment pending G2 legal clearance.
- **Dependencies:** G2 legal sign-off for data residency; Meta Wearables DAT SDK stability; optimization of local ML models to fit 12GB VRAM.
- **Implementation Phases:**
  - Phase 1: Android Client and DAT session bridge API.
  - Phase 2: Analytics Engine adaptation to POV feeds (Hot & Cold paths).
  - Phase 3: Dashboard and Access Control (RBAC).
- **Cross Functional Coordination:** Requires tight alignment between mobile engineers (DAT integration), AI optimization engineers, UI/UX for the admin dashboard and privacy notices, and legal for compliance verification.

## Risks & Tradeoffs

- **Product Risks:** Teacher resistance to wearing a camera is a significant risk. The UI and training must strongly emphasize constructive feedback and robust privacy controls.
- **Market Risks:** Delays in G2 legal sign-off could pause the India year 1 rollout.
- **Scalability Concerns:** Maintaining reliable connectivity and managing battery life on diverse Android host devices paired with the glasses presents a significant operational challenge compared to fixed hardware.
- **Prioritization Tradeoffs:** We have explicitly traded off the multi-cam room and screen capture features (now deferred to Phase 1b/secondary) to focus entirely on the Meta Ray-Ban primary client. Cloud-scale AI capabilities are traded for cost-efficiency and privacy via edge-to-local-GPU processing.

## Agile Sprint Plan

- **Sprint Goals:**
  - Sprint 1-2: Implement DAT `StreamSession` in `CaptureActivity` (Android) and the server bridge (`POST /v1/dat-sessions/*`). Test with Mock Device Kit.
  - Sprint 3-4: Deploy the hot-path rolling metrics (talk ratio) using the DAT streams and build the foundational admin dashboard. Validate with physical glasses.
  - Sprint 5-6: Optimize the cold-path diarization pipeline to operate within the 45-minute SLA on the target RTX 5070 hardware, tuned for the glasses' audio profile.
- **Backlog Priorities:** Fallback smartboard client (Android/Windows panel) integration, audit logging, post-lesson LLM summaries.
- **Deliverables:** A functional Android capture agent paired via DAT; a responsive admin dashboard; an optimized local inference pipeline.
- **Success Criteria:** The system successfully records a 50-minute session via the Mock Device Kit and physical glasses, buffers on the phone during a simulated network outage, and produces the composite index within 45 minutes.

## Post Launch Analysis

- **Monitoring Strategy:** Telemetry on Android app stability, Bluetooth connection drop rates, DAT stream latency, and hot-path metric latency (target p95 < 8s).
- **Experimentation Plan:** A/B test different onboarding flows for pairing the glasses and different visualizations of the composite pedagogy index to determine which format drives the most constructive admin-teacher dialogue.
- **Feedback Loops:** Establish a direct feedback channel for the first cohort of pilot school admins and teachers to iterate on the wearable comfort, app usability, and metric relevance.
- **Iteration Roadmap:** Post-launch focus will shift towards refining the AI coaching summaries, adding the fallback smartboard client for non-wearable classrooms, and preparing the FERPA-compliant package for US market expansion.
