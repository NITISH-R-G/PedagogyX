# STRIDE Threat Model v0.1: India Supervision Deployment

**Scope:** Capture Agent (Android/Windows) -> Central OSS Backend
**Methodology:** STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)
**Created:** 2026-05-19

## 1. System Assets

- Identifiable student video (High sensitivity)
- Teacher audio & pedagogy scores (High sensitivity)
- API Gateway & Dashboards

## 2. Threat Analysis

### Spoofing (Identity)

- **Threat:** A student or unauthorized teacher installs the Capture Agent and spoofs a valid teacher's session token to upload fake video.
- **Mitigation:** Mutual TLS (mTLS) for agent-backend communication. Strict JWT expiration and hardware binding for Windows Smartboards.

### Tampering (Data Integrity)

- **Threat:** Man-in-the-middle (MitM) alters video chunks or pedagogy metrics JSON en route to the backend.
- **Mitigation:** TLS 1.3 enforced for all uploads and WebRTC streams. Chunks are hashed (SHA-256) locally, and the hash is verified by the ingestion service.

### Repudiation (Auditability)

- **Threat:** A principal views a teacher's pedagogy score and later denies doing so; or a teacher denies recording a controversial session.
- **Mitigation:** Immutable audit logs in PostgreSQL tracking every view, export, and start/stop event.

### Information Disclosure (Privacy)

- **Threat:** S3/MinIO bucket is misconfigured, exposing raw identifiable child video to the public internet.
- **Mitigation:** MinIO isolated within a private VPC. Pre-signed, time-limited URLs used strictly for playback. Default AES-256 encryption at rest.

### Denial of Service (Availability)

- **Threat:** Malicious actor or bug causes thousands of agents to simultaneous upload huge 4K streams, saturating the ap-south-1 ingest bandwidth and crashing the MediaMTX service.
- **Mitigation:** Rate limiting on the API gateway. Auto-scaling groups for the ingest tier. Client-side exponential backoff on upload failures.

### Elevation of Privilege (Authorization)

- **Threat:** A teacher manipulates API requests to view the pedagogy scores of other teachers or access the district admin dashboard.
- **Mitigation:** Strict Role-Based Access Control (RBAC) via Keycloak. Every API endpoint must validate tenant ID and role scope explicitly.
