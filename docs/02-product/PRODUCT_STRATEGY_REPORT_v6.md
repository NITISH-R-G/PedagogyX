# Product Strategy Report v6

## Product Problem Analysis

The core problem in educational assessment remains that teachers experience high administrative burden and receive delayed, often highly subjective feedback from occasional peer or administrative observations. These sporadic evaluations create an environment of surveillance rather than continuous, supportive professional development.

PedagogyX is addressing this by leveraging Meta Ray-Ban smart glasses (via the Wearables Device Access Toolkit, DAT) combined with an Android companion application. This wearable-first pivot (ADR-0009) shifts the capture paradigm from intrusive, fixed smartboard cameras to an unobtrusive, teacher-centric, first-person perspective. The overarching opportunity is to provide automated, objective, and private multimodal pedagogy analysis to empower educators.

### User pain points

- **Intrusive Evaluations**: Teachers feel micromanaged by traditional in-classroom observations and full-room camera setups.
- **Delayed Feedback**: Feedback on pedagogy is often disconnected from the actual moment of teaching.
- **High Friction**: Existing capture systems require complex setups, manual starting/stopping, and maintenance that interrupts the teaching flow.

### Business context

- **Wearable-First Advantage**: Owning the first-person perspective in classroom analytics differentiates PedagogyX from incumbent players relying on fixed cameras.
- **Compliance Constraints**: Strict privacy rules (particularly concerning student data and requiring G2 clearance in India) dictate the pace of deployment and feature availability. The system must operate within a privacy-first, tiered analytics framework.

### Constraints

- **Hardware Limitations**: Meta Ray-Ban glasses have finite battery life and require robust Bluetooth streaming to an Android device.
- **Privacy Clearances**: Full production deployment is blocked until G2 legal sign-off; operations are restricted to synthetic test sessions and MVP stacks currently.

### Opportunities

- Establish a dominant first-mover advantage in wearables-based educational analytics.
- Deliver highly personalized, actionable coaching tips and pedagogy scores directly to educators.
- Reduce infrastructure friction and costs for school districts by utilizing personal, non-fixed devices.

## User Workflow Analysis

The PedagogyX workflow is designed around minimal intervention, allowing teachers to integrate the tool naturally into their daily routines without cognitive overload.

### Onboarding flow

A teacher pairs their Meta Ray-Ban smart glasses with the PedagogyX Android companion app. Before capturing any data, the teacher completes a rigorous privacy and consent walkthrough to comply with G2 requirements, ensuring complete transparency and control over their data.

### User journeys

1. **Initiation**: The teacher starts a session either via the Android app or a physical tap on the glasses.
2. **Capture & Streaming**: Multimodal data (video and audio) streams from the glasses to the phone via the DAT SDK.
3. **Processing**: The phone chunks the data and securely uploads it to edge/cloud nodes for AI inference.
4. **Review**: Post-session, the teacher accesses a secure web dashboard to review AI-generated coaching tips, their pedagogy score, and insights into classroom engagement.

### Friction points

- Bluetooth connection stability between the glasses and the Android device.
- Battery drain on both the glasses and the Android phone during extended classes.
- Latency between the end of a class and the availability of the final authoritative report.

### Engagement loops

Teachers receive low-latency "nudges" (where appropriate) and comprehensive post-class reports. By consistently reviewing these actionable insights, teachers are incentivized to iterate on their teaching methodologies, creating a continuous loop of improvement and engagement with the platform.

## Product Strategy

Our mission is to empower educators with multimodal, privacy-centric AI intelligence that fosters continuous professional development and fundamentally improves student outcomes.

### Vision

To become the global standard for unobtrusive, AI-driven pedagogical coaching by leveraging wearable technology to capture the true essence of classroom interactions from the teacher's perspective.

### Differentiation

- **First-Person Perspective**: The wearable form factor provides a unique, teacher-controlled viewpoint that traditional room cameras simply cannot capture.
- **Privacy-First Architecture**: A strong commitment to an OSS-first inference stack and rigorous privacy compliance (G2 clearance readiness) builds trust with educators and unions.
- **Multimodal AI**: Moving beyond audio transcription to include visual context for a holistic analysis of pedagogy.

### Positioning

PedagogyX is positioned as an elite, supportive coaching tool for educators—shifting the narrative from administrative surveillance to actionable, personalized professional support.

### Growth opportunities

- Scaling from individual teacher coaching to aggregated, anonymized departmental and district-wide analytics.
- Integration with major Learning Management Systems (LMS).
- Expanding the Wearables Device Access Toolkit implementation to support other compatible wearable devices in the future.

## Competitive Analysis

The current EdTech observation market relies heavily on costly, intrusive hardware or simplistic audio-only software solutions.

### Market landscape

Incumbents utilize fixed swivel cameras (e.g., Swivl) or general-purpose audio transcription AI tools that lack pedagogical context.

### Competitor strengths

- Deeply established relationships with large school districts.
- Mature, enterprise-grade reporting dashboards and administrative tools.

### Competitor weaknesses

- High hardware and installation costs for full-room capture solutions.
- Intrusive presence in the classroom that alters natural teaching dynamics.
- Lack of true multimodal analysis, resulting in incomplete pedagogical insights.

### Differentiation opportunities

The wearable approach significantly lowers the barrier to entry, eliminates installation friction, and provides a highly personalized perspective that directly mitigates surveillance concerns.

## Feature Prioritization

Our prioritization focuses relentlessly on validating the core wearables pivot, ensuring technical viability, and maintaining strict privacy compliance.

### Impact analysis

- **DAT Streaming Bridge**: Critical for the v1 value proposition; without reliable capture, there is no product.
- **Privacy Consent Flows**: Essential for user trust and G2 compliance.
- **AI Feedback Engine**: The core value driver that turns raw data into actionable coaching.

### Effort analysis

- The Android DAT host app and cloud chunk ingestion represent the highest engineering effort due to the novel technical challenges of continuous, high-bandwidth streaming from constrained wearables.

### Strategic importance

Successfully proving the wearable-first model is existential for PedagogyX's current pivot and long-term positioning.

### Expected outcomes

A robust, end-to-end pipeline from the Meta Ray-Ban glasses, through the Android bridge, to the AI backend, producing accurate and secure preliminary pedagogy scores.

## Success Metrics

Success is defined by system reliability, user adoption, and demonstrable progress toward legal compliance.

### KPIs

- Successful session capture rate (>95%).
- Average time to generate a complete pedagogy score post-session.
- End-to-end system uptime during the pilot phase (>99.9%).

### Retention metrics

- Weekly Active Teachers (WAT): Percentage of activated teachers reviewing and acting upon their coaching reports weekly.

### Activation metrics

- Time to First Session (TTFS): Time elapsed from device unboxing/setup to the first successfully captured and processed teaching session.

### Engagement metrics

- Number of coaching tips and specific insights interacted with per session review.

### Business metrics

- Number of pilot schools actively engaged.
- Milestone progression toward full G2 legal sign-off and removal of data restrictions.

## Execution Plan

Execution requires rapid iteration on technical foundations while adhering strictly to legal and compliance boundaries.

### Milestones

1. **MDK Validation**: Complete Mock Device Kit (MDK) testing for the Android application.
2. **API Foundation**: Implement and solidify core API endpoints for the complete DAT session lifecycle.
3. **Local Simulation**: Validate full data flow on developer machines using local ML simulation (e.g., RTX 5070 setup).
4. **Compliance Clearance**: Secure G2 clearance for synthetic and subsequent pilot data usage.

### Dependencies

- Stability and capabilities of the Meta Wearables DAT SDK.
- Timely finalization of G2 legal approvals.
- Android Bluetooth stack reliability.

### Implementation phases

- **Phase 0**: Current focus on internal testing with the MDK and synthetic data.
- **Alpha**: Limited internal pilots using physical devices to validate ergonomics and initial data quality.
- **Beta**: Controlled rollout with real teachers in pilot schools to validate the value proposition and refine AI models.

### Cross functional coordination

Requires daily alignment between Android engineers, backend developers, AI specialists, product design, and the legal/compliance team.

## Risks & Tradeoffs

Navigating the intersection of novel hardware, complex AI, and strict privacy regulations presents significant risks.

### Product risks

- Ergonomics: Teachers may find the glasses uncomfortable during extended teaching blocks.
- Hardware Constraints: Battery life may degrade or fail to cover required class lengths, necessitating fallback strategies.

### Market risks

- Institutional Resistance: Schools, unions, or parents might resist wearable technology due to privacy concerns or existing anti-recording policies.

### Scalability concerns

- Infrastructure Costs: Handling massive, concurrent video streams requires a highly optimized hybrid edge-cloud infrastructure to manage bandwidth and compute costs effectively.

### Prioritization tradeoffs

- Deprioritizing the Windows smartboard client limits our immediate reach in schools with strict no-wearables policies. However, this focus is absolutely necessary to ensure a successful, high-quality v1 wearables launch.

## Agile Sprint Plan

Upcoming sprints are dedicated to establishing the foundational data pipeline and cementing user trust through consent UI.

### Sprint goals

- Harden the foundational DAT-to-cloud data pipeline.
- Finalize and implement privacy and consent wireframes in the Android application.

### Backlog priorities

1. Implement and optimize Android DAT host chunking and upload logic.
2. Deploy robust API endpoints for the complete DAT session lifecycle.
3. Implement G2 consent flows in the Android UI.
4. Establish basic session state management across the app and backend.

### Deliverables

- A functional Android prototype utilizing the MDK that successfully, reliably uploads session chunks to the local development stack.

### Success criteria

- A synthetic five-minute session can stream, upload, and process into a preliminary database record without data loss or pipeline errors.

## Post Launch Analysis

Continuous monitoring and rapid iteration are critical to driving adoption and improving the core AI value proposition.

### Monitoring strategy

- Implement comprehensive observability within the Android app to track battery drain, thermal throttling, and Bluetooth connection drops.
- Monitor API gateway metrics to track chunk upload success rates and latency.

### Experimentation plan

- A/B test various iterations of the reporting dashboard to determine which visualizations and feedback formats maximize teacher comprehension and engagement.

### Feedback loops

- Establish weekly qualitative check-ins with pilot teachers to collect feedback on device comfort, workflow friction, and the perceived utility of the coaching tips.

### Iteration roadmap

- Refine AI models based on actual pilot data to improve the accuracy of pedagogy scores.
- Relentlessly optimize the Android app and DAT integration to maximize battery life and streaming reliability.
- Re-evaluate the Phase 1b smartboard integration only once the primary wearables path is stabilized and proven.
