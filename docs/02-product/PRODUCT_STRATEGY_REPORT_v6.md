# Product Strategy Report v6

## Product Problem Analysis

Teachers currently face significant administrative burdens and often receive subjective, delayed feedback on their teaching methodologies. Existing classroom observation tools are frequently perceived as intrusive and punitive surveillance rather than supportive coaching mechanisms. PedagogyX is addressing these concerns by shifting its primary v1 capture client from fixed, expensive smartboards to Meta Ray-Ban smart glasses via the Wearables Device Access Toolkit (DAT).

- **User Pain Points:** Teachers experience friction and anxiety with traditional surveillance tools. They need seamless, automated analysis without complex setup, enabling them to focus on teaching.
- **Business Context:** The wearables-first pivot (ADR-0009) creates an opportunity to own the first-person perspective in classroom analytics, reducing installation costs and scaling faster. Strict privacy and compliance requirements, particularly concerning student data, mandate G2 clearance in India.
- **Constraints:** Full deployment is blocked until G2 sign-off. Hardware constraints require reliable Bluetooth streaming from Meta Ray-Ban glasses to an Android companion device, acting as a bridge to edge/cloud ingestion nodes.
- **Opportunities:** We have a significant first-mover advantage in wearables-based educational analytics. This approach delivers highly personalized, point-of-view-based feedback while leveraging personal devices over fixed, high-cost infrastructure.

## User Workflow Analysis

Our primary workflow design objective is zero-friction capture to encourage daily habit formation.

- **Onboarding Flow:** Teachers register their Meta Ray-Ban glasses with the PedagogyX Android companion app. They complete a comprehensive, legally vetted privacy and consent walkthrough (G2 requirement) before any recording can occur.
- **User Journeys:** The teacher initiates a session with a simple tap on the Android app or glasses before class. Video and audio stream seamlessly via Bluetooth DAT to the phone, which buffers and uploads the chunks. Post-class, teachers access a web dashboard to review automated AI coaching tips and their composite pedagogy score.
- **Friction Points:** Maintaining stable Bluetooth connectivity between glasses and the host phone. Managing device battery life during long or consecutive teaching sessions. Minimizing latency in the "cold path" generation of the final authoritative pedagogy score.
- **Engagement Loops:** Delivering actionable live nudges and comprehensive post-class reports incentivizes teachers to continuously adapt and improve their instruction based on objective, data-driven feedback.

## Product Strategy

Our goal is to redefine classroom observation by transforming it from a top-down surveillance mechanism into a bottom-up, teacher-empowering coaching tool.

- **Vision:** To become the default standard for privacy-first, AI-driven pedagogical coaching, utilizing wearable technology to capture the authentic, uninterrupted essence of classroom interaction.
- **Differentiation:** The wearable form factor provides a unique, teacher-controlled perspective that fixed multi-camera setups cannot replicate. Our FOSS-first inference stack and strict privacy-tiered analytics build trust.
- **Positioning:** An elite, privacy-conscious coaching tool designed explicitly to support educators, effectively shifting the paradigm from punitive evaluation to actionable, continuous professional development.
- **Growth Opportunities:** Expanding from individual teacher coaching to departmental and district-wide analytics. Integrating with existing Learning Management Systems (LMS) and exploring support for additional wearable device ecosystems in the future.

## Competitive Analysis

The EdTech market is crowded with legacy hardware vendors and emerging AI tools that often miss the mark on user experience and cost.

- **Market Landscape:** Current solutions range from high-cost fixed swivel cameras (e.g., traditional smart classroom analytics) to general-purpose audio transcription tools that lack pedagogical context.
- **Competitor Strengths:** Established competitors have deep relationships with large school districts and offer mature, comprehensive administrative reporting dashboards.
- **Competitor Weaknesses:** High capital expenditure (CapEx) for full-room capture hardware. Intrusive physical presence in the classroom that heightens teacher anxiety. Many rely solely on audio, missing critical visual cues of student engagement.
- **Differentiation Opportunities:** The wearable approach drastically lowers the barrier to entry (₹0 customer hardware budget) and provides a highly personalized, less intrusive perspective that directly mitigates surveillance concerns.

## Feature Prioritization

We must aggressively prioritize features that validate the core wearables pivot and ensure strict privacy compliance.

- **Impact Analysis:** The DAT streaming bridge and robust privacy consent flows are existential for the v1 value proposition and for establishing user trust in the Indian market.
- **Effort Analysis:** Developing the Android DAT host app and resilient cloud chunk ingestion pipeline represents significant engineering effort due to the novel technical challenges of continuous Bluetooth video streaming.
- **Strategic Importance:** Successfully proving the wearable-first model is critical for the company's current strategic pivot and long-term positioning against legacy hardware vendors.
- **Expected Outcomes:** Delivering a functional, end-to-end pipeline from Meta Ray-Ban glasses through the Android host to the central AI backend, reliably producing preliminary pedagogy scores.

## Success Metrics

Our success metrics evaluate system reliability, user adoption, and regulatory progress.

- **KPIs:** M-A (Classroom Coverage): Percentage of scheduled lessons successfully recorded. M-B (Time-to-Insight): Median minutes from class-end to dashboard readiness. System uptime during the pilot phase.
- **Retention Metrics:** Weekly Active Teachers (WAT) who consistently review and engage with their post-lesson reports.
- **Activation Metrics:** Time elapsed from unboxing and pairing the device to the successful completion of the first captured session.
- **Engagement Metrics:** The number of coaching tips clicked or interacted with per session (M-C: Admin Action Rate).
- **Business Metrics:** Number of pilot schools signed and successfully onboarded. Concrete progression toward and achievement of full G2 legal sign-off.

## Execution Plan

Our execution strategy emphasizes rapid technical validation and strict legal compliance.

- **Milestones:**
  1. Complete Mock Device Kit (MDK) testing for the Android DAT host application.
  2. Implement and stabilize core API endpoints for DAT session lifecycle management.
  3. Validate the full end-to-end data flow using local RTX 5070 dev environments for ML simulation.
  4. Secure formal G2 clearance for synthetic and pilot data usage.
- **Dependencies:** The stability and reliability of the Meta Wearables DAT SDK. Finalization of G2 legal approvals for data processing.
- **Implementation Phases:**
  - Phase 0: Internal testing with synthetic data and the MDK.
  - Phase Alpha: Limited internal pilots to test end-to-end connectivity.
  - Phase Beta: Limited rollout in pilot schools with real glasses.
  - v1 Launch: General availability for the target Indian market.
- **Cross Functional Coordination:** Demands tight alignment between Android developers (client), backend engineers (ingestion), AI specialists (inference), and the legal team (compliance).

## Risks & Tradeoffs

We must proactively manage hardware limitations and address potential market resistance.

- **Product Risks:** Teachers may find the glasses uncomfortable during extended teaching blocks. Device battery life may degrade quickly or fail to last through consecutive classes. Bluetooth connection drops could result in lost data.
- **Market Risks:** Schools or teacher unions might resist wearable technology due to entrenched privacy concerns or the perception of continuous recording devices in the classroom.
- **Scalability Concerns:** Handling massive, concurrent video stream uploads at the end of the school day requires a highly robust hybrid edge-cloud infrastructure to manage network bandwidth efficiently.
- **Prioritization Tradeoffs:** Deprioritizing the Windows/Android smartboard client (Phase 1b) limits our immediate reach in schools with strict no-wearables policies, but this focus is essential to ensure a successful, high-quality v1 wearables launch.

## Agile Sprint Plan

Immediate sprints are focused on unblocking the foundational DAT-to-cloud pipeline and securing user consent.

- **Sprint Goals:** Establish the foundational DAT-to-cloud streaming and chunking pipeline. Finalize and implement privacy and consent wireframes.
- **Backlog Priorities:**
  1. Finalize the Android DAT host chunking and offline buffering logic.
  2. Create, deploy, and harden API endpoints for the DAT session lifecycle.
  3. Implement G2-approved consent flows within the Android UI.
- **Deliverables:** A working Android prototype utilizing the MDK that securely and successfully uploads session chunks to the local development stack.
- **Success Criteria:** A synthetic five-minute session can stream from the client, upload to the backend, and process into a preliminary database record without data loss or errors.

## Post Launch Analysis

We will continuously monitor performance and gather user feedback to drive rapid iteration and adoption.

- **Monitoring Strategy:** Implement comprehensive observability (e.g., Datadog) on the Android app to track battery drain and connection drops, and on the API gateway to monitor chunk upload success rates and latency.
- **Experimentation Plan:** Conduct A/B tests on various reporting dashboard layouts to determine which visualizations maximize teacher engagement and the actionability of the AI coaching tips.
- **Feedback Loops:** Schedule weekly qualitative check-ins with pilot teachers to collect direct feedback regarding device comfort, app usability, and the perceived value of the pedagogy scores.
- **Iteration Roadmap:** Continuously refine AI models based on incoming pilot data to improve transcription and diarization accuracy. Optimize the Android app to minimize battery consumption. Explore the Phase 1b smartboard integration once the primary wearables path is fully stabilized and adopted.
