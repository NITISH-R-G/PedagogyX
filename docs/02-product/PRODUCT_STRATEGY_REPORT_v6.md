# Product Strategy Report v6

## Product Problem Analysis

Teachers face high administrative overhead and receive delayed, subjective feedback on their teaching methods. They often feel surveilled rather than supported, needing a non-intrusive way to capture classroom dynamics and receive actionable, objective insights. PedagogyX is pivoting its primary v1 capture client from fixed smartboards to Meta Ray-Ban smart glasses via the Wearables Device Access Toolkit (DAT). This shift aims to provide a natural, teacher-centric capture experience.

### User pain points

Teachers experience friction with traditional observation tools, feeling micromanaged. They need seamless, automated pedagogy analysis without complex setups. Fixed cameras fail to capture the teacher's true perspective and create a "big brother" feeling in the classroom.

### Business context

The shift to a wearables-first approach (ADR-0009) creates an opportunity to own the first-person perspective in classroom analytics. Strict privacy and compliance requirements, particularly around student data, require G2 clearance in India. The business needs to validate the market demand for a wearables-first education product.

### Constraints

Strict privacy rules limit full deployment until G2 sign-off. Hardware constraints require the Meta Ray-Ban glasses to stream reliably to a companion Android device acting as a bridge to cloud or edge nodes. The DAT requires a stable bluetooth connection.

### Opportunities

Establishing a first-mover advantage in wearables-based educational analytics. Delivering highly personalized, POV-based feedback to educators. Reducing infrastructure friction for districts by leveraging personal devices over fixed smartboards. Transforming teacher evaluation from punitive to developmental.

## User Workflow Analysis

The workflow focuses on simplicity and minimal intervention, ensuring teachers can naturally integrate the system into their daily routines.

### Onboarding flow

A teacher registers their Meta Ray-Ban glasses with the PedagogyX Android companion app. They complete a comprehensive privacy and consent walkthrough to comply with G2 requirements before their first session. The onboarding emphasizes trust, data ownership, and the developmental nature of the tool.

### User journeys

The teacher initiates a session via the Android app or the physical interface on the glasses. Video and audio stream from the glasses to the phone via Bluetooth DAT. The phone buffers and uploads data to the edge or cloud. Post-class, teachers access a web dashboard to review AI-generated coaching tips and pedagogy scores.

### Friction points

Bluetooth connection stability between glasses and the phone. Battery life management during extended teaching sessions. Latency in final authoritative score generation. Complexity of interpreting the AI-generated pedagogical insights.

### Engagement loops

Teachers receive live nudges (if audio feedback is enabled) and comprehensive post-class reports, incentivizing them to continuously adapt and improve their teaching methodologies based on data-driven feedback. Sharing exceptional moments with peers to foster a community of practice.

## Product Strategy

Our strategy is to empower educators with multimodal, unobtrusive AI intelligence that fosters continuous professional development and improves student outcomes.

### Vision

To become the standard for privacy-first, AI-driven pedagogical coaching, leveraging wearable technology to capture the true essence of classroom interaction and empower every teacher to be their best.

### Differentiation

A wearable form factor provides a unique, teacher-controlled perspective that fixed cameras cannot replicate. A strong commitment to an OSS-first inference stack and privacy-tiered analytics ensures trust. First-person video combined with advanced audio diarization and pedagogy models.

### Positioning

An elite, privacy-conscious coaching tool for educators, fundamentally shifting the paradigm from surveillance to actionable support. We are the "Strava for teaching", focusing on personal bests rather than top-down evaluation.

### Growth opportunities

Expansion from individual teacher coaching to systemic departmental and district-wide analytics. Integration with Learning Management Systems (LMS). Exploring support for other wearable devices (e.g., Apple Vision Pro, next-gen AR glasses).

## Competitive Analysis

The current market is saturated with traditional observation tools that are costly and intrusive.

### Market landscape

The landscape includes fixed swivel cameras (e.g., Swivl, Owl Labs) and general-purpose audio transcription AI tools (e.g., Otter.ai tailored for classrooms), as well as legacy in-person observation models.

### Competitor strengths

Established relationships with large school districts, mature and comprehensive reporting dashboards, and deep integrations with existing educational software ecosystems.

### Competitor weaknesses

High hardware and installation costs for full-room capture. Intrusive presence in the classroom leading to the Hawthorne effect. Lack of true multimodal analysis, often relying solely on audio or static wide-angle video.

### Differentiation opportunities

The wearable approach lowers barriers to entry significantly and provides a highly personalized perspective that mitigates surveillance concerns. It centers the teacher's agency and provides data that is intrinsically more relevant to the teacher's immediate interactions.

## Feature Prioritization

Focus on features that validate the core wearables pivot, ensure privacy compliance, and deliver immediate value to the early adopters.

### Impact analysis

The DAT streaming bridge and robust privacy consent flows are critical for the v1 value proposition and user trust. Accurate speaker diarization (separating teacher vs. student voices) has massive impact on the quality of insights.

### Effort analysis

The Android DAT host app and cloud chunk ingestion represent significant engineering effort due to novel technical challenges with continuous streaming. Training or fine-tuning models for classroom-specific audio on edge devices is high effort but high reward.

### Strategic importance

Proving the wearable-first model is existential for the company's current pivot and long-term positioning. Gaining legal clearance in target markets is a strict prerequisite for growth.

### Expected outcomes

A functional, end-to-end pipeline from Meta Ray-Ban glasses to the AI backend, producing preliminary pedagogy scores securely and reliably, demonstrating the core value loop to initial pilot users.

## Success Metrics

We will measure success through system reliability, user adoption, and compliance progress.

### KPIs

Successful session capture rate (percentage of attempted sessions that fully upload and process). Average time to generate a pedagogy score. System uptime during the pilot phase.

### Retention metrics

Weekly Active Teachers (WAT) reviewing and acting upon their reports. Day 1, Day 7, and Day 30 retention rates for the companion app.

### Activation metrics

Time elapsed from unboxing the device to the first successfully captured session. Completion rate of the onboarding and privacy consent flow.

### Engagement metrics

Number of coaching tips interacted with per session. Session length (are teachers keeping it on for the whole class?).

### Business metrics

Number of pilot schools signed. Progression toward full G2 legal sign-off. Customer Acquisition Cost (CAC) for individual teacher early adopters vs. district pilots.

## Execution Plan

Our execution must be rapid, technically sound, and legally compliant, operating in a tight loop with early testers.

### Milestones

1. Complete Mock Device Kit (MDK) testing for the Android application.
2. Implement the core API endpoints for DAT session lifecycle and chunk ingestion.
3. Validate full data flow on developer machines using RTX 5070 for local ML simulation.
4. Secure G2 clearance for synthetic and pilot data usage.
5. Launch closed Alpha with 5-10 trusted educators.

### Dependencies

Stability and updates of the Meta Wearables DAT SDK. Finalization of G2 legal approvals. Availability of test hardware (Meta Ray-Ban glasses).

### Implementation phases

Phase 0 focuses on current internal testing with the MDK. Alpha will involve limited internal pilots to test hardware limits. Beta will include a limited rollout with real glasses to measure real-world engagement, culminating in the v1 launch.

### Cross functional coordination

Requires tight alignment between Android developers (DAT integration), backend engineers (chunking/streaming), AI specialists (inference pipeline), and the legal compliance team (G2 clearance).

## Risks & Tradeoffs

Navigating hardware constraints and market perception is critical.

### Product risks

Teachers may find the glasses uncomfortable during long sessions. Battery life may degrade or fall short of required class lengths. The glasses might overheat during continuous streaming.

### Market risks

Schools might resist wearable technology due to privacy concerns or union pushback against recording devices. The association with "Meta" may cause friction with some privacy-conscious districts.

### Scalability concerns

Handling massive, concurrent video streams requires robust hybrid edge-cloud infrastructure to manage bandwidth efficiently. Cloud AI inference costs could spiral without aggressive optimization and edge-processing fallbacks.

### Prioritization tradeoffs

Deprioritizing the Windows smartboard client limits our reach in schools with strict no-wearables policies, but focus is necessary to ensure a strong v1 wearables launch. Delaying advanced analytics features to ensure core pipeline stability.

## Agile Sprint Plan

The upcoming sprints focus on foundational pipeline elements, user consent, and MDK validation.

### Sprint goals

Establish the foundational DAT-to-cloud pipeline. Finalize privacy and consent wireframes. Validate end-to-end chunk processing with synthetic data.

### Backlog priorities

1. Implement Android DAT host chunking logic and retry mechanisms.
2. Create and deploy API endpoints for the DAT session lifecycle (start, chunk, end).
3. Finalize G2 consent flows in the Android UI.
4. Set up the local testing environment with MDK and Docker compose.

### Deliverables

A working Android prototype utilizing the MDK that successfully uploads session chunks to the local development stack. Approved UI designs for the onboarding flow.

### Success criteria

A synthetic five-minute session can stream, upload, and process into a preliminary database record without errors. Zero dropped chunks during simulated network instability.

## Post Launch Analysis

Continuous monitoring and rapid iteration will drive adoption and refine the product market fit.

### Monitoring strategy

Implement comprehensive observability on the Android app to track battery drain, temperature, and connection drops. Instrument the API gateway to monitor chunk upload success rates, latency, and processing times.

### Experimentation plan

A/B test various reporting dashboard layouts to determine which maximizes teacher engagement and actionability of pedagogy scores. Test different framing of coaching nudges (e.g., authoritative vs. suggestive).

### Feedback loops

Conduct weekly check-ins with pilot teachers to collect qualitative feedback regarding device comfort, battery anxiety, and dashboard utility. Implement in-app micro-surveys after session review.

### Iteration roadmap

Refine AI models based on pilot data to improve accuracy (especially handling noisy classroom audio). Optimize the Android app to maximize battery life. Explore the Phase 1b smartboard integration once the wearables path is stabilized. Investigate real-time audio nudges directly through the glasses' speakers.
