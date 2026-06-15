# PedagogyX: Autonomous Senior Product Management Report

## Product Problem Analysis

- **User Pain Points:** Teachers lack real-time, objective feedback on their instructional practices. They struggle to measure student engagement, talk time distribution, and pedagogical effectiveness without disruptive, manual classroom observations.
- **Business Context:** The education sector faces high teacher burnout and a need for data-driven professional development. There is a market gap for privacy-first, locally-executed educational analytics platforms. PedagogyX aims to be the leading multimodal AI classroom intelligence platform.
- **Constraints:**
  - 100% Free and Open Source Software (FOSS) mandate.
  - Strict offline execution requirement for complete data residency and student privacy compliance.
  - Hardware limitations: Must run on consumer-grade RTX 5070 (12GB VRAM) systems.
- **Opportunities:** Leverage local, efficient AI models (whisper, small vision models) to provide immediate, actionable feedback on classroom dynamics, ultimately empowering teachers and improving student outcomes.

## User Workflow Analysis

- **Onboarding Flow:**
  - School IT admin deploys PedagogyX via Docker/Compose locally.
  - Teacher is provided a minimal setup capture device or app (e.g., wearable dat client).
  - Teacher completes a 2-minute calibration and test capture.
- **User Journeys:**
  - **Capture:** Teacher starts recording at the beginning of a lesson. Data is processed locally by `worker-asr` (speech) and `worker-cv` (vision) without internet dependency.
  - **Review:** Post-lesson, the teacher logs into the admin web UI.
  - **Insight:** Teacher reviews metrics such as Teacher Talk vs. Student Talk ratio, questioning patterns, and student engagement heatmaps.
- **Friction Points:**
  - Hardware setup and ensuring the RTX 5070 constraints are managed gracefully.
  - Accuracy of local ASR (Whisper) in noisy classroom environments.
- **Engagement Loops:** Teachers reviewing insights, setting goals for the next lesson (e.g., "increase student talk time by 10%"), and checking progress in subsequent recordings.

## Product Strategy

- **Vision:** To become the default, privacy-preserving standard for autonomous classroom intelligence and teacher optimization.
- **Differentiation:** Zero-cloud dependency. Complete local control. We prioritize data residency and free open-source access over central data aggregation.
- **Positioning:** PedagogyX is not an evaluation tool; it is a supportive, private co-pilot for teacher self-reflection and professional growth.
- **Growth Opportunities:**
  - Expand offline model capabilities (e.g., emotion recognition, advanced pedagogy classification).
  - Integrations with local School Information Systems (SIS).
  - Community-driven plug-in ecosystem for custom metrics.

## Competitive Analysis

- **Market Landscape:** Dominated by expensive, cloud-based observation platforms or hardware-heavy proprietary solutions (e.g., Swivl, TeachFX).
- **Competitor Strengths:** High-accuracy cloud AI models, polished enterprise dashboards, established sales channels.
- **Competitor Weaknesses:** High recurring costs, massive privacy concerns (sending audio/video of children to the cloud), complex setups, vendor lock-in.
- **Differentiation Opportunities:**
  - Capitalize on the offline, privacy-first mandate.
  - Position the 12GB VRAM hardware constraint as an advantage in accessibility and cost-effectiveness for underfunded school districts.

## Feature Prioritization

- **Impact Analysis vs Effort Analysis:**
  1. **Core ASR & Talk Ratio (High Impact, Medium Effort):** Vital MVP feature.
  2. **Local Admin Dashboard (High Impact, Low Effort):** Essential for reviewing metrics.
  3. **Computer Vision Engagement Metrics (High Impact, High Effort):** Phase 2 capability, requires optimizing CV models for 12GB VRAM.
  4. **Custom Metric Plugins (Medium Impact, High Effort):** De-prioritized for initial release.
- **Strategic Importance:** Proving the viability of the offline ASR pipeline (`worker-asr`) and basic metric aggregation (`worker-metrics`) is paramount for the MVP.
- **Expected Outcomes:** A functional, end-to-end local pipeline delivering accurate talk-time ratios immediately post-lesson.

## Success Metrics

- **KPIs:**
  - Pipeline completion rate: % of sessions successfully processed locally.
  - Processing speed: Ratio of processing time to recording time.
- **Retention Metrics:** Weekly Active Teachers (WAT) reviewing their dashboards.
- **Activation Metrics:** Time to first successfully processed session post-installation.
- **Engagement Metrics:** Number of recorded sessions per week per teacher.
- **Business Metrics:** Number of active local deployments, GitHub repository stars, community contributions.

## Execution Plan

- **Milestones:**
  - **M1:** MVP Pipeline (Capture -> ASR Stub -> Metrics -> UI).
  - **M2:** Real Whisper Integration (Optimization for RTX 5070).
  - **M3:** Beta Vision Capabilities (`worker-cv` activation).
  - **M4:** Polished Next.js/React Admin Dashboard.
- **Dependencies:**
  - Hardware availability for testing.
  - Optimization of `worker-asr` and `worker-cv` to co-exist within 12GB VRAM constraints.
- **Implementation Phases:**
  - **Phase 1:** Core infrastructure (FastAPI, Postgres, Docker Compose).
  - **Phase 2:** AI Worker integration and optimization.
  - **Phase 3:** Frontend UI refinement and metric visualization.
- **Cross Functional Coordination:** Close alignment between AI Engineers (model optimization), Data Engineers (pipeline stability), and Frontend/UX (dashboard simplicity).

## Risks & Tradeoffs

- **Product Risks:** Teachers may find the data overwhelming or feel evaluated rather than supported.
- **Market Risks:** Schools may prefer established cloud vendors despite privacy concerns due to perceived ease of use.
- **Scalability Concerns:** Managing updates for completely air-gapped, offline deployments.
- **Prioritization Tradeoffs:** Choosing lower-tier Whisper models (`tiny` or `base`) to fit VRAM constraints at the cost of slight ASR accuracy degradation.

## Agile Sprint Plan

- **Sprint Goals:**
  - Sprint 1: Stabilize the dev stack (`make dev-up`) and mock capture pipeline.
  - Sprint 2: Integrate functional Whisper ASR within hardware limits.
  - Sprint 3: Finalize talk-ratio metrics calculation and UI presentation.
- **Backlog Priorities:**
  - Fix Dockerfile entrypoints for workers.
  - Refine React/Next.js dashboard components.
  - Develop hardware utilization monitoring tools.
- **Deliverables:** A deployable `compose.dev.yaml` stack that fully processes an audio file into a talk-ratio metric.
- **Success Criteria:** End-to-end processing of a 10-minute audio clip within 5 minutes on target hardware, displaying accurate metrics in the UI.

## Post Launch Analysis

- **Monitoring Strategy:** Implement local telemetry (opt-in only) to track processing failures and hardware bottlenecks.
- **Experimentation Plan:** A/B test different visualizations of talk-time (e.g., pie chart vs. timeline) to see which drives higher teacher comprehension.
- **Feedback Loops:** In-app (local) feedback forms for teachers to report inaccurate transcriptions or metric anomalies.
- **Iteration Roadmap:** Use feedback to adjust AI model thresholds and UI layouts for subsequent minor releases.
