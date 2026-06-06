# Product Strategy Report v5

## Product Problem Analysis

Teachers face high administrative overhead and receive delayed, subjective feedback on their teaching methods. They often feel surveilled rather than supported, needing a non-intrusive way to capture classroom dynamics and receive actionable, objective insights. PedagogyX is pivoting its primary v1 capture client from fixed smartboards to Meta Ray-Ban smart glasses via the Wearables Device Access Toolkit (DAT). This shift aims to provide a natural, teacher-centric capture experience.

### User pain points

Teachers experience friction with traditional observation tools, feeling micromanaged. They need seamless, automated pedagogy analysis without complex setups.

### Business context

The shift to a wearables-first approach (ADR-0009) creates an opportunity to own the first-person perspective in classroom analytics. Strict privacy and compliance requirements, particularly around student data, require G2 clearance in India.

### Constraints

Strict privacy rules limit full deployment until G2 sign-off. Hardware constraints require the Meta Ray-Ban glasses to stream reliably to a companion Android device acting as a bridge to cloud or edge nodes.

### Opportunities

Establishing a first-mover advantage in wearables-based educational analytics. Delivering highly personalized, POV-based feedback to educators. Reducing infrastructure friction for districts by leveraging personal devices over fixed smartboards.

## User Workflow Analysis

The workflow focuses on simplicity and minimal intervention, ensuring teachers can naturally integrate the system into their daily routines.

### Onboarding flow

A teacher registers their Meta Ray-Ban glasses with the PedagogyX Android companion app. They complete a comprehensive privacy and consent walkthrough to comply with G2 requirements before their first session.

### User journeys

The teacher initiates a session via the Android app or the physical interface on the glasses. Video and audio stream from the glasses to the phone via Bluetooth DAT. The phone buffers and uploads data to the edge or cloud. Post-class, teachers access a web dashboard to review AI-generated coaching tips and pedagogy scores.

### Friction points

Bluetooth connection stability between glasses and the phone. Battery life management during extended teaching sessions. Latency in final authoritative score generation.

### Engagement loops

Teachers receive live nudges and comprehensive post-class reports, incentivizing them to continuously adapt and improve their teaching methodologies based on data-driven feedback.

## Product Strategy

Our strategy is to empower educators with multimodal, unobtrusive AI intelligence that fosters continuous professional development and improves student outcomes.

### Vision

To become the standard for privacy-first, AI-driven pedagogical coaching, leveraging wearable technology to capture the true essence of classroom interaction.

### Differentiation

A wearable form factor provides a unique, teacher-controlled perspective that fixed cameras cannot replicate. A strong commitment to an OSS-first inference stack and privacy-tiered analytics ensures trust.

### Positioning

An elite, privacy-conscious coaching tool for educators, fundamentally shifting the paradigm from surveillance to actionable support.

### Growth opportunities

Expansion from individual teacher coaching to systemic departmental and district-wide analytics. Integration with Learning Management Systems (LMS). Exploring support for other wearable devices.

## Competitive Analysis

The current market is saturated with traditional observation tools that are costly and intrusive.

### Market landscape

The landscape includes fixed swivel cameras and general-purpose audio transcription AI tools.

### Competitor strengths

Established relationships with large school districts and mature, comprehensive reporting dashboards.

### Competitor weaknesses

High hardware and installation costs for full-room capture. Intrusive presence in the classroom. Lack of true multimodal analysis, often relying solely on audio.

### Differentiation opportunities

The wearable approach lowers barriers to entry significantly and provides a highly personalized perspective that mitigates surveillance concerns.

## Feature Prioritization

Focus on features that validate the core wearables pivot and ensure privacy compliance.

### Impact analysis

The DAT streaming bridge and robust privacy consent flows are critical for the v1 value proposition and user trust.

### Effort analysis

The Android DAT host app and cloud chunk ingestion represent significant engineering effort due to novel technical challenges with continuous streaming.

### Strategic importance

Proving the wearable-first model is existential for the company's current pivot and long-term positioning.

### Expected outcomes

A functional, end-to-end pipeline from Meta Ray-Ban glasses to the AI backend, producing preliminary pedagogy scores securely.

## Success Metrics

We will measure success through system reliability, user adoption, and compliance progress.

### KPIs

Successful session capture rate. Average time to generate a pedagogy score. System uptime during the pilot phase.

### Retention metrics

Weekly Active Teachers (WAT) reviewing and acting upon their reports.

### Activation metrics

Time elapsed from unboxing the device to the first successfully captured session.

### Engagement metrics

Number of coaching tips interacted with per session.

### Business metrics

Number of pilot schools signed. Progression toward full G2 legal sign-off.

## Execution Plan

Our execution must be rapid, technically sound, and legally compliant.

### Milestones

1. Complete Mock Device Kit (MDK) testing for the Android application.
2. Implement the core API endpoints for DAT session lifecycle.
3. Validate full data flow on developer machines using RTX 5070 for local ML simulation.
4. Secure G2 clearance for synthetic and pilot data usage.

### Dependencies

Stability of the Meta Wearables DAT SDK. Finalization of G2 legal approvals.

### Implementation phases

Phase 0 focuses on current internal testing with the MDK. Alpha will involve limited internal pilots. Beta will include a limited rollout with real glasses, culminating in the v1 launch.

### Cross functional coordination

Requires tight alignment between Android developers, backend engineers, AI specialists, and the legal compliance team.

## Risks & Tradeoffs

Navigating hardware constraints and market perception is critical.

### Product risks

Teachers may find the glasses uncomfortable during long sessions. Battery life may degrade or fall short of required class lengths.

### Market risks

Schools might resist wearable technology due to privacy concerns or union pushback against recording devices.

### Scalability concerns

Handling massive, concurrent video streams requires robust hybrid edge-cloud infrastructure to manage bandwidth efficiently.

### Prioritization tradeoffs

Deprioritizing the Windows smartboard client limits our reach in schools with strict no-wearables policies, but focus is necessary to ensure a strong v1 wearables launch.

## Agile Sprint Plan

The upcoming sprints focus on foundational pipeline elements and user consent.

### Sprint goals

Establish the foundational DAT-to-cloud pipeline. Finalize privacy and consent wireframes.

### Backlog priorities

1. Implement Android DAT host chunking logic.
2. Create and deploy API endpoints for the DAT session lifecycle.
3. Finalize G2 consent flows in the Android UI.

### Deliverables

A working Android prototype utilizing the MDK that successfully uploads session chunks to the local development stack.

### Success criteria

A synthetic five-minute session can stream, upload, and process into a preliminary database record without errors.

## Post Launch Analysis

Continuous monitoring and rapid iteration will drive adoption.

### Monitoring strategy

Implement comprehensive observability on the Android app to track battery drain and connection drops, and on the API gateway to monitor chunk upload success rates.

### Experimentation plan

A/B test various reporting dashboard layouts to determine which maximizes teacher engagement and actionability of pedagogy scores.

### Feedback loops

Conduct weekly check-ins with pilot teachers to collect qualitative feedback regarding device comfort and dashboard utility.

### Iteration roadmap

Refine AI models based on pilot data to improve accuracy. Optimize the Android app to maximize battery life. Explore the Phase 1b smartboard integration once the wearables path is stabilized.
