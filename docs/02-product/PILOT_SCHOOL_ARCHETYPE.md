# Pilot School Archetype (India Market)

**Status:** Draft - Pending Founder Approval

## Objective

Identify the ideal profile for the first 3-5 pilot deployments in India to validate the PedagogyX MVP (Supervision Mode, Multi-Cam, Central OSS Inference).

## Ideal Archetype: Private "Smart" School Chain (Tier 1/2 Cities)

### Why Private Chains?

1. **Budget:** They have the budget for Smartboards and central servers (answering D-10 implicitly for the pilot).
2. **Infrastructure:** Reliable power and >20 Mbps internet uplink per classroom.
3. **Agility:** Faster procurement cycles compared to State Government tenders.
4. **Consent:** Private school admission agreements often already include clauses for CCTV and classroom monitoring, easing the DPDP verifiable parental consent burden.

### Minimum Technical Requirements for Pilot

- **Hardware:** Classrooms must already be equipped with a Windows-based Smartboard or a dedicated teacher PC (Intel i3/equivalent minimum, 4GB RAM).
- **Network:** Minimum 10 Mbps sustained uplink per classroom to test real-time WebRTC streams.
- **Server Room:** Space and cooling for one standard rack to host the local inference server (RTX 5070 equivalent or better) if D-PROC dictates on-prem.

## Secondary Archetype: Progressive State Government Program (e.g., PM SHRI)

### Pros

- Massive scale potential.
- Strong alignment with the "supervision" mode and administrative dashboards.

### Cons

- High friction regarding DPDP and children's data privacy.
- Unreliable network/power infrastructure requiring heavy offline batch processing and store-and-forward mechanisms.
- Low budget ceilings.

## Validation Goals for the Pilot

1. Measure the exact network bandwidth consumed by the multi-cam Capture Agent.
2. Validate the accuracy of English/Hindi code-switched ASR in a real acoustic environment.
3. Test the teacher and admin reaction to the preliminary Pedagogy Index.
