# PRODUCT_STRATEGY_REPORT_v6

## Product Problem Analysis

Teachers face high administrative overhead and subjective, delayed feedback. The current observation tools feel intrusive, often acting more like surveillance than supportive coaching. With our pivot to Meta Ray-Ban smart glasses (ADR-0009), we have an opportunity to resolve these issues by providing a natural, first-person point of view (POV) capture mechanism via the Wearables Device Access Toolkit (DAT). This addresses the core problem of intrusive recording while gathering rich multimodal data (audio, video, engagement) to measure pedagogical efficiency accurately.

## User Workflow Analysis

The user workflow focuses on seamless integration into a teacher's daily routine.

- **Onboarding:** Teachers pair their Meta Ray-Ban glasses with the PedagogyX Android companion app and complete mandatory G2 privacy consent flows.
- **Session Initiation:** The teacher starts a capture session from the app or glasses before class.
- **Data Capture:** The glasses stream audio and video to the Android app via Bluetooth DAT, which acts as a bridge to upload chunks to the backend.
- **Post-Session:** The teacher reviews AI-generated insights, including pedagogy scores and personalized coaching nudges, on a secure web dashboard.
- **Friction Points:** The primary friction points are Bluetooth connection stability, device battery life, and the initial privacy consent hurdle.

## Product Strategy

Our strategy is to build a privacy-first, unobtrusive classroom intelligence platform that empowers educators.

- **Vision:** To become the default standard for continuous, AI-driven professional development in education, transforming classroom insights from surveillance to empowerment.
- **Differentiation:** Our wearables-first approach (Meta Ray-Ban) provides a unique, teacher-controlled perspective that fixed cameras lack, coupled with a robust open-source software (OSS) offline inference stack to ensure privacy.
- **Growth:** Begin with early-adopter pilot schools (post-G2 clearance), leveraging synthetic data for the MVP. Expand to district-wide deployments and potential integrations with major Learning Management Systems (LMS) once product-market fit and scalability are proven.

## Competitive Analysis

- **Landscape:** The market includes traditional, expensive fixed-camera systems (e.g., swivel cameras) and generic audio transcription tools.
- **Strengths of Competitors:** Competitors often have established district relationships and deep integrations with legacy school IT infrastructure.
- **Weaknesses of Competitors:** High costs, complex installations, intrusive presence, and a lack of holistic multimodal analysis (often relying on single modalities like audio only).
- **Our Edge:** Lower barrier to entry, teacher-centric wearable form factor, and deep multimodal pedagogical analysis. This fundamentally shifts the value proposition toward immediate, personalized support.

## Feature Prioritization

- **High Impact, High Urgency:** Robust Android DAT streaming bridge, secure chunk upload pipeline, and rigorous G2 privacy consent flows. These are existential for the v1 wearables pivot.
- **High Impact, Medium Urgency:** Multimodal AI pipeline (Hot Path YOLO and Cold Path faster-whisper/Ollama) optimization for accurate pedagogy scoring.
- **Medium Impact, Low Urgency:** Advanced historical trend analysis and cross-departmental dashboards.
- **Decision:** All immediate engineering efforts must focus on stabilizing the DAT-to-cloud pipeline and ensuring full compliance with G2 legal requirements before real pilot data can be processed.

## Success Metrics

- **Core KPIs:** Session capture success rate (%), average time to generate post-session reports (latency), and system uptime during synthetic and pilot testing.
- **Activation:** Time from unboxing/pairing the device to completing the first successful recorded session.
- **Engagement:** Weekly Active Teachers (WAT) reviewing their dashboards, and the interaction rate with AI coaching tips (e.g., clicks, feedback given).
- **Business Impact:** Securing G2 legal clearance for real school data and signing our first 10 pilot schools.

## Execution Plan

- **Phase 0 (Current):** Utilize the Mock Device Kit (MDK) and synthetic data on developer environments (RTX 5070) to validate the end-to-end pipeline.
- **Phase 1 (Alpha):** Internal testing with real Meta Ray-Ban hardware and the Android companion app to test Bluetooth stability and chunking logic.
- **Phase 2 (Beta):** Limited rollout with pilot schools once G2 clearance is achieved.
- **Milestones:** MDK pipeline validation, API endpoint deployment for DAT session lifecycle, Android G2 consent UI completion.

## Risks & Tradeoffs

- **Technical Risks:** Bluetooth DAT streaming may suffer from instability or excessive battery drain on the glasses or companion device.
- **Market Risks:** Pushback from teachers' unions regarding the introduction of recording devices in classrooms, despite privacy guarantees.
- **Tradeoffs:** By deprioritizing the Windows smartboard client to focus entirely on wearables, we risk alienating schools with strict "no-wearables" policies. However, this focus is critical to dominating the first-person perspective market.

## Agile Sprint Plan

- **Sprint Goals:** Finalize the foundational DAT-to-cloud pipeline and implement the necessary G2 privacy consent flows in the Android app.
- **Priorities:**
  1. Complete Android DAT host chunking and upload logic.
  2. Deploy core API endpoints to manage the DAT session lifecycle.
  3. Finalize and test the G2 privacy consent UI.
- **Deliverables:** A functional Android prototype that can stream a mock 5-minute session and successfully store the preliminary record in the database without errors.

## Post Launch Analysis

- **Monitoring Strategy:** Implement comprehensive telemetry in the Android app (battery usage, drop rates) and the API gateway (chunk upload success, latency).
- **Experimentation:** A/B test variations of the post-session dashboard to identify which layout drives the highest engagement with coaching tips.
- **Feedback Loops:** Schedule regular qualitative check-ins with pilot educators to assess device comfort, perceived intrusiveness, and dashboard value.
- **Iteration:** Refine the AI inference models based on early pilot feedback to reduce false positives in pedagogical scoring, and continuously optimize the Android client for battery efficiency.
