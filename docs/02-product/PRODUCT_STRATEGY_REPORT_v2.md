# PedagogyX Product Strategy Report v2

**Version**: 2.0 (Post-Ray-Ban Pivot)
**Author**: Autonomous Senior Product Manager & Product Strategy Architect
**Focus**: Teacher Optimization & Classroom Intelligence via Meta Ray-Ban Wearables

---

## Product Problem Analysis

**User Pain Points:**

1. **School Administrators:** Lack visibility into actual pedagogical quality across dozens of classrooms. Existing classroom observation methods are manual, biased, slow, and unscalable.
2. **Teachers:** Suffer from high cognitive load, "Big Brother" surveillance anxiety from fixed cameras, and lack objective, private, and non-punitive feedback to improve their teaching methods.

**Business Context & Constraints:**

- **Market Segment:** K-12 private "smart" schools and state/government schools in India. High price sensitivity (₹0 customer hardware budget target).
- **Technical Context:** Shifting from low-end smartboards to Meta Ray-Ban Meta glasses (Wearables DAT SDK) as the primary v1 capture device (ADR-0009). Backed by an OSS-first central inference stack (faster-whisper, YOLO) due to cost and data residency constraints.
- **Legal Context:** G2 legal gate (DPDP compliance) must be cleared before capturing actual student/teacher data.

**Opportunities:**

- Provide a radical shift in form factor: from intrusive, fixed multi-cam setups to unobtrusive, teacher-controlled point-of-view (POV) wearables.
- Deliver automated "Pedagogy Indexes" (talk ratios, engagement metrics) without manual data entry.
- Build a sustainable, low-OpEx business model by avoiding proprietary cloud APIs in favor of a Hybrid D-PROC architecture (ADR-0008).

---

## User Workflow Analysis

**Onboarding Flow:**

1. **Hardware Provisioning:** School IT provisions Meta Ray-Ban glasses and Android companion devices (DAT hosts).
2. **Teacher Authentication:** Teacher logs into the PedagogyX Android app using school credentials, linking the glasses via Bluetooth.

**User Journeys (Capture to Insight):**

1. **Initiation (Teacher):** Teacher walks into the classroom, puts on the glasses, and initiates the lesson recording via a single tap on the Android host app. A clear recording indicator provides transparency.
2. **Live Monitoring (Admin Hot Path):** Admin logs into the Next.js Web Dashboard to view school-wide Observation Coverage (M-A) and preliminary live talk-ratio metrics.
3. **Processing (Cold Path):** Lesson concludes. Audio/Video chunks (buffered on the phone) upload securely to the central inference server. Open-source models (faster-whisper) generate final diarization and the definitive Pedagogy Index.
4. **Coaching & Review (Admin/Teacher):** Admin or Instructional Coach reviews the final Pedagogy Index on the dashboard, identifying specific moments for non-punitive, evidence-based feedback discussions with the teacher.

**Friction Points:**

- **Capture Initiation:** Teachers failing to connect the glasses or forgetting to start the recording.
- **Surveillance Anxiety:** Teachers modifying their behavior due to discomfort with being recorded.
- **Network Unreliability:** Indian classroom internet (< 10 Mbps) failing to support chunked video uploads, delaying Time-to-Insight (M-B).
- **Admin Overload:** Dashboard data density overwhelming principals if insights are not immediately actionable.

**Engagement Loops:**

- **Coaching Loop:** Flagged lesson -> Admin reviews specific timeline segment -> Direct, objective feedback session with teacher -> Teacher improves Pedagogy Index in subsequent lessons.
- **Deployment Loop:** Admin sees high Observation Coverage -> Trusts system reliability -> Mandates further usage.

---

## Product Strategy

**Vision:**
To become the invisible intelligence layer in Indian classrooms, empowering administrators with scalable, objective pedagogical data and supporting teachers with private, actionable coaching to systematically improve student outcomes.

**Differentiation:**

1. **Wearable Form Factor:** Utilizing Meta Ray-Ban glasses provides an unparalleled first-person perspective on classroom dynamics, replacing expensive, fixed multi-cam installations.
2. **Frictionless Deployment:** Bypassing complex school IT infrastructure with a simple wearable + mobile companion app approach.
3. **Cost Advantage:** Zero customer hardware CapEx and low OpEx via an OSS-first central inference pipeline, crucial for the Indian market.
4. **Privacy-First Architecture:** D-PROC hybrid design ensures DPDP compliance while maintaining performance.

**Positioning:**
PedagogyX is positioned as a "Classroom Optimization Engine," not a surveillance tool. For admins, it’s a scalable quality assurance platform. For teachers, it’s an AI assistant that provides objective self-reflection data without manual reporting.

**Growth Opportunities:**

1. Expand from Phase 0 "Supervision" (post-hoc analysis) to Phase 2 "AI Nudges" (real-time feedback via the glasses' earpiece).
2. Scale from private "Smart" school chains to massive state government programs (e.g., PM SHRI).
3. Re-introduce Smartboard integration (Phase 1b) for schools restricted from using wearables.

---

## Competitive Analysis

**Market Landscape:**
The Indian EdTech market features legacy Smartboard vendors and emerging AI classroom analytics startups, heavily focused on hardware integration.

**Competitor Strengths:**

- **Incumbents (China/Taiwan/India):** Established distribution channels and deep integration with existing CCTV/Smartboard infrastructure.
- **AI Sokrates:** Deep domain expertise and pre-existing relationships with Indian educational institutions.

**Competitor Weaknesses:**

- **High CapEx/OpEx:** Reliance on expensive camera installations, on-prem servers, or costly proprietary APIs (OpenAI).
- **Intrusive UX:** Fixed cameras miss the nuance of teacher-student interactions and heighten "Big Brother" anxieties.
- **Inflexible Capture:** Tied to specific physical rooms rather than following the teacher.

**Differentiation Opportunities:**

- **Point-of-View Analytics:** Capture the authentic classroom experience from the teacher's perspective, capturing nuance fixed cameras miss.
- **Teacher-Centric Control:** Providing the teacher with physical control over the capture device (glasses) can reduce surveillance anxiety compared to always-on room cameras.

---

## Feature Prioritization

1. **Meta Ray-Ban DAT Android Client (Highest Priority):**
   - **Impact:** Defines the entire v1 capture experience.
   - **Effort:** High (Wearables SDK integration, offline buffering).
   - **Expected Outcome:** Reliable, seamless start/stop of capture and chunk uploading.

2. **Core ASR & Talk Ratio Pipeline (Cold Path):**
   - **Impact:** Generates the core value proposition (Pedagogy Index).
   - **Effort:** Medium (faster-whisper optimization on RTX 5070).
   - **Expected Outcome:** Accurate teacher/student talk ratios available < 45 mins post-lesson.

3. **Admin Live Dashboard (Supervision MVP):**
   - **Impact:** Provides the primary interface for the buyer (Admin).
   - **Effort:** Medium (Next.js UI/UX).
   - **Expected Outcome:** Clear visualization of M-A (Coverage) and M-B (Time-to-Insight) metrics.

4. **Live Preview Metrics (Hot Path):**
   - **Impact:** Instant reassurance of system functionality.
   - **Effort:** High (Streaming architecture).
   - **Expected Outcome:** Rolling preliminary metrics visible during the lesson (secondary to cold path).

---

## Success Metrics

**North Star Metric:**

- **Pedagogical Improvement Rate:** Term-over-term increase in the average school-wide Pedagogy Index (composite score).

**Key Performance Indicators (KPIs):**

1. **M-A (Observation Coverage):** % of target classrooms with ≥1 analyzed session/week. Target: >85%. (Primary Deployment Metric)
2. **M-B (Time-to-Insight):** Median minutes from class end to authoritative dashboard readiness. Target: < 45 minutes. (Primary Performance Metric)
3. **M-C (Admin Action Rate):** % of flagged lessons where an admin/coach opens the review within 48 hours. Target: >80%. (Primary Engagement Metric)
4. **Capture Failure Rate:** % of initiated lessons that fail to upload or process. Target: < 5%. (Reliability)

---

## Execution Plan

**Milestones:**

1. **Milestone 1 (Legal/Compliance):** Clear G2 gate with signed counsel memo regarding DPDP compliance.
2. **Milestone 2 (Infrastructure Scaffold):** Complete end-to-end synthetic data flow: API -> worker-asr -> Admin Web Shell.
3. **Milestone 3 (DAT Client Integration):** Complete the Android host app using the Mock Device Kit, routing DAT `StreamSession` data to the edge buffer and API.
4. **Milestone 4 (Hardware Pilot):** End-to-end test with physical Meta Ray-Ban glasses.
5. **Milestone 5 (Alpha Deployment):** Deploy to 3-5 private "Smart" schools for real-world validation.

**Cross-Functional Coordination:**

- **Product/Design:** Finalize admin dashboard UX and non-punitive teacher feedback interfaces.
- **Engineering (Client):** Focus on robust DAT session lifecycle management and resilient chunk uploading in low-bandwidth environments.
- **Engineering (Backend/ML):** Optimize faster-whisper pipeline to meet the < 45 min SLA on constrained hardware (RTX 5070).

---

## Risks & Tradeoffs

**Product & Market Risks:**

- **Teacher Resistance:** Strong union or individual pushback against wearable cameras, leading to sabotage or refusal to use the system.
- **Hardware Dependency:** Tying the entire v1 strategy to Meta's hardware and the stability of the Android DAT connection.

**Scalability Concerns:**

- **Network Bottlenecks:** Indian school upload speeds failing to handle video chunks, severely delaying M-B (Time-to-Insight).
- **Compute Constraints:** End-of-school-day upload spikes overwhelming the central OSS inference servers.

**Prioritization Tradeoffs:**

- **Wearables vs. Smartboards:** Focusing entirely on Ray-Bans (ADR-0009) delays the original Smartboard path, potentially losing schools unwilling to adopt wearables.
- **Android Only:** Deferring an iOS client increases execution velocity but alienates iOS-using teachers in the short term.

---

## Agile Sprint Plan

### Sprint 03 (MVP Scaffolding - Active)

- **Goal:** First vertical slice using synthetic data.
- **Deliverables:** API + Postgres + MinIO infrastructure; worker-asr container processing audio; Admin Web Shell displaying static metrics.
- **Success Criteria:** Synthetic audio is processed into a preliminary talk ratio visible on the dashboard.

### Sprint 04 (Client Integration)

- **Goal:** Connect the Meta DAT Android app (via Mock Device Kit) to the cloud pipeline.
- **Deliverables:** Android app capturing and chunking video/audio; API `/v1/dat-sessions` endpoint handling lifecycle events.
- **Success Criteria:** A simulated DAT session successfully uploads and triggers the worker pipeline.

### Sprint 05 (Hardware & Pilot Polish)

- **Goal:** Physical hardware validation and UI refinement.
- **Deliverables:** End-to-end testing with physical Ray-Ban glasses; robust offline buffering; implemented RBAC and privacy notices in the UI.
- **Success Criteria:** A 15-minute physical recording appears accurately on the Admin Dashboard within 30 minutes of completion.

---

## Post Launch Analysis

**Monitoring Strategy:**

- Implement real-time dashboards (e.g., Datadog/Grafana) tracking API latency, upload success rates, and inference queue depth.
- Daily tracking of primary KPIs (M-A, M-B, M-C) across pilot schools.

**Experimentation Plan:**

- **Onboarding A/B Test:** Test variations of the Android app's "Start Capture" screen to minimize friction and maximize successful session initiations.
- **Dashboard UX Test:** Test presenting "Raw Metrics" vs. "Synthesized Coaching Nudges" to admins to determine which drives a higher M-C (Admin Action Rate).

**Feedback Loops:**

- **Admin Insight:** Bi-weekly qualitative interviews with Pilot Principals to assess the utility and accuracy of the Pedagogy Index.
- **Teacher Sentiment:** Anonymous end-of-week surveys for Pilot Teachers to measure "surveillance anxiety" and perceived value of the feedback.
- **Iterative Refinement:** Use feedback to adjust the weighting of the Pedagogy Index and refine the tone of the UI before broader market rollout.
