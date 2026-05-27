# Elite Agile Scrum Tracking

## Overview

This document outlines the Agile framework for PedagogyX, ensuring disciplined execution across research, engineering, and product design. It defines the structure for epics, stories, and the technical/research backlogs necessary to build a world-class educational AI platform.

---

## 1. Scrum Framework Definitions

All work must be categorized using the following hierarchy:

- **Initiative:** Massive, multi-quarter goals (e.g., "India Pilot Launch", "Phase 1b Smartboard Integration").
- **Epic:** Large bodies of work that span multiple sprints (e.g., "Multimodal Ingestion Pipeline", "Pedagogy Index v1").
- **Story (User/Technical):** A discrete unit of work delivering tangible value, completable within a single sprint.
- **Task/Sub-task:** Specific engineering or research actions required to complete a story.

### Story Required Metadata

Every story **must** contain:

- Title & Description
- Priority (P0 - Blocker, P1 - Critical, P2 - Normal, P3 - Low)
- Impact (High, Medium, Low)
- Difficulty/Effort (Story Points: 1, 2, 3, 5, 8)
- Dependencies (Linked ticket IDs)
- Acceptance Criteria (Clear, boolean statements)

---

## 2. Active Epics (Phase 1)

### Epic 1: Edge Capture Integration (Meta Ray-Ban)

- **Status:** In Progress
- **Owner:** Client Engineering
- **Goal:** Robustly capture, chunk, and upload POV video/audio from glasses to the cloud API via the Android host app.

### Epic 2: Core Data Infrastructure & API

- **Status:** In Progress
- **Owner:** Platform Engineering
- **Goal:** Establish the scalable, secure FastAPI ingestion endpoints, MinIO storage layer, and Postgres metadata schema.

### Epic 3: Foundational AI Workers

- **Status:** Backlog (Awaiting G2)
- **Owner:** ML Engineering
- **Goal:** Deploy the basic `worker-asr` (Whisper) and `worker-cv` pipelines pulling from the task queue.

---

## 3. Product & Technical Backlog

| ID     | Title                                    | Epic   | Priority | Impact | Difficulty | Dependencies | Acceptance Criteria                                                                                                                      | Effort |
| ------ | ---------------------------------------- | ------ | -------- | ------ | ---------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| PX-101 | Implement JWT Auth for Edge Client       | Epic 2 | P1       | High   | Medium     | None         | - API requires Bearer token.<br>- Android client successfully authenticates.<br>- Invalid tokens rejected (401).                         | 3      |
| PX-102 | Resumable Video Chunk Upload             | Epic 1 | P1       | High   | Hard       | PX-101       | - Client chunks 50MB file.<br>- Server accepts out-of-order chunks.<br>- File successfully reassembled in MinIO.                         | 5      |
| PX-103 | Whisper ASR Worker Stub                  | Epic 3 | P2       | Medium | Medium     | PX-102       | - Worker pulls job from Redis.<br>- Downloads audio from MinIO.<br>- Generates mock transcript JSON.<br>- Updates DB status to COMPLETE. | 3      |
| PX-104 | Database Migration Pipeline              | Epic 2 | P0       | High   | Easy       | None         | - Alembic configured.<br>- Initial schema (sessions, users) applied successfully via CLI.                                                | 2      |
| PX-105 | Admin Dashboard Wireframe Implementation | N/A    | P2       | Medium | Medium     | None         | - Next.js app running.<br>- Mock data populates 'Talk Ratio' chart.<br>- Responsive design implemented.                                  | 3      |

---

## 4. Research Backlog

| ID     | Title                                         | Topic   | Priority | Impact | Acceptance Criteria                                                                                                                  |
| ------ | --------------------------------------------- | ------- | -------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| RES-01 | Evaluate Whisper English-Hindi Code-Switching | NLP/ASR | P1       | High   | - Benchmark provided comparing Whisper large vs medium on custom mixed-language dataset.<br>- Error rates documented.                |
| RES-02 | Egocentric Pose Estimation Feasibility        | CV      | P2       | High   | - Report detailing open-source models capable of estimating student posture from teacher POV camera.<br>- FPS benchmark on RTX 5070. |
| RES-03 | DPDP Consent UX Patterns                      | Product | P0       | High   | - Figma mockups demonstrating legally compliant consent flows for parents/teachers in the Indian context.                            |

---

## 5. Sprint Planning Mechanics

- **Sprint Duration:** 2 weeks.
- **Sprint Planning:** Occurs on the first Monday. Team commits to stories based on historical velocity (initially assumed 20 points/developer).
- **Daily Standup:** Asynchronous via Slack/Teams. What was done, what is planned, blockers.
- **Sprint Review:** Friday of week 2. Demo of working software (vertical slices only).
- **Sprint Retrospective:** Following the review. Focus on process improvement, technical debt identification, and team health.

## 6. Technical Debt Tracking

Technical debt must be logged as tasks in the backlog with a specific `TechDebt` label. 20% of every sprint's capacity must be allocated to resolving technical debt or improving testing infrastructure.
