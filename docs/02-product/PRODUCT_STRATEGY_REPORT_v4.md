# Product Strategy Report v4: Wearables-First PedagogyX

## Product Problem Analysis

- **User Pain Points:** Teachers face high administrative overhead, receive subjective or delayed feedback on their pedagogy, and often feel surveilled rather than supported. They need a non-intrusive way to capture classroom dynamics and receive actionable, objective insights.
- **Business Context:** PedagogyX is pivoting its primary v1 capture client from fixed smartboards to Meta Ray-Ban smart glasses using the Wearables Device Access Toolkit (DAT). This shift aims to provide a more natural, teacher-centric capture experience.
- **Constraints:**
  - Strict privacy and compliance requirements, especially around student data (requires G2 clearance).
  - Hardware limitations: The AI glasses need to stream data reliably to a companion Android phone, which then bridges to the cloud/edge.
  - The need for a hybrid edge-cloud architecture to manage bandwidth and latency.
- **Opportunities:**
  - Establish a "first-mover" advantage in wearables-based classroom analytics.
  - Deliver highly personalized, POV-based pedagogical feedback.
  - Reduce infrastructure friction for schools (no need for complex smartboard setups if teachers have glasses).

## User Workflow Analysis

- **Onboarding Flow:** Teacher registers the Meta Ray-Ban glasses with the PedagogyX Android companion app. They complete a privacy and consent walkthrough (critical for G2 compliance) before their first session.
- **User Journeys:**
  - **Capture:** Teacher starts a session via the Android app or glasses' physical interface. The glasses stream POV video and audio to the phone via Bluetooth/DAT.
  - **Ingest:** The phone buffers the chunks and uploads them over WAN to the PedagogyX cloud or an edge node.
  - **Review:** After the session, the teacher logs into the web dashboard to review preliminary pedagogy scores and AI-generated coaching tips.
- **Friction Points:** Pairing and maintaining the Bluetooth connection between glasses and phone; ensuring sufficient battery life for full sessions; potential latency in generating the final "authoritative" score.
- **Engagement Loops:** Teachers receive immediate "live nudges" (optional) and comprehensive post-class reports, incentivizing them to review and adapt their teaching methods continuously.

## Product Strategy

- **Vision:** To empower educators with multimodal, unobtrusive AI intelligence that fosters continuous professional development and improves student outcomes.
- **Differentiation:** Leveraging wearable technology (Meta Ray-Bans) for a teacher's POV, providing a unique dataset that fixed cameras cannot capture. A strong focus on OSS-first inference and privacy-tiered analytics.
- **Positioning:** An elite, privacy-conscious coaching tool for educators, moving away from the "surveillance" paradigm of traditional classroom cameras.
- **Growth Opportunities:**
  - Expansion from individual teacher coaching to departmental and district-wide analytics.
  - Integration with existing Learning Management Systems (LMS).
  - Potential expansion to other wearable devices in the future.

## Competitive Analysis

- **Market Landscape:** The market is crowded with traditional classroom observation tools (e.g., swivel cameras) and general-purpose transcription AI.
- **Competitor Strengths:** Established relationships with districts; mature reporting dashboards.
- **Competitor Weaknesses:** High hardware costs for full-room capture; intrusive presence; lack of true multimodal pedagogical analysis (often just audio).
- **Differentiation Opportunities:** The wearable form factor is our biggest wedge. It lowers the barrier to entry (cost and setup) and provides a highly personalized, teacher-controlled perspective.

## Feature Prioritization

- **Impact Analysis:** The core DAT streaming bridge and the privacy/consent flows are the highest impact, as they enable the entire v1 value proposition.
- **Effort Analysis:** The Android DAT host app and the cloud chunk ingest are high effort due to novel technical challenges.
- **Strategic Importance:** Proving the wearable-first model is existential for this pivot.
- **Expected Outcomes:** A functional, end-to-end pipeline from Ray-Bans to the AI backend, producing a preliminary pedagogy score.

## Success Metrics

- **KPIs:** Successful session capture rate; average time to generate a pedagogy score; system uptime during pilot.
- **Retention Metrics:** Weekly Active Teachers (WAT) reviewing their reports.
- **Activation Metrics:** Time from unboxing to first successful capture.
- **Engagement Metrics:** Number of coaching tips interacted with per session.
- **Business Metrics:** Number of pilot schools signed; progression toward G2 legal sign-off.

## Execution Plan

- **Milestones:**
  1. Complete Mock Device Kit (MDK) testing for the Android app.
  2. Implement the `POST /v1/dat-sessions/*` bridge in the API.
  3. Validate full data flow on developer machines (using RTX 5070 for local ML simulation).
  4. Secure G2 clearance for synthetic/pilot data.
- **Dependencies:** Meta Wearables DAT SDK stability; G2 legal approval.
- **Implementation Phases:** Phase 0 (current) -> Alpha (internal testing with MDK) -> Beta (limited pilot with real glasses) -> v1 Launch.
- **Cross Functional Coordination:** Close alignment between Android dev, backend engineers, and legal/compliance teams.

## Risks & Tradeoffs

- **Product Risks:** Teachers may find the glasses uncomfortable or distracting; battery life issues during long classes.
- **Market Risks:** Schools may be hesitant to adopt wearable tech due to privacy concerns or union pushback.
- **Scalability Concerns:** Handling massive video data streams from hundreds of simultaneous sessions requires robust hybrid edge-cloud infrastructure.
- **Prioritization Tradeoffs:** De-prioritizing the smartboard/Windows client limits our reach in schools with strict "no wearables" policies, but focusing on the Ray-Bans is necessary for a strong v1 launch.

## Agile Sprint Plan

- **Sprint Goals:** Establish the foundational DAT-to-cloud pipeline and finalize privacy wireframes.
- **Backlog Priorities:**
  1. Implement Android DAT host chunking logic.
  2. Create API endpoints for DAT session lifecycle.
  3. Finalize G2 consent flows in the UI.
- **Deliverables:** A working Android prototype (using MDK) that successfully uploads session chunks to the local dev stack.
- **Success Criteria:** A 5-minute synthetic session can be streamed, uploaded, and processed into a preliminary database record without errors.

## Post Launch Analysis

- **Monitoring Strategy:** Implement rigorous observability on the Android app (battery drain, connection drops) and the API gateway (chunk upload success rates).
- **Experimentation Plan:** A/B testing different reporting dashboard layouts to maximize teacher engagement with the pedagogy scores.
- **Feedback Loops:** Weekly check-ins with pilot teachers to gather qualitative feedback on the glasses' comfort and the dashboard's utility.
- **Iteration Roadmap:** Based on pilot feedback, refine the AI models for better accuracy, optimize the Android app for battery life, and begin exploring the Phase 1b smartboard integration.
