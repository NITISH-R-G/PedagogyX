# Phase 0: Foundational Interrogation Report

**Date:** 2026-05-24
**Status:** In Progress / Awaiting Founder Final Sign-off
**Target:** PedagogyX MVP & Platform Architecture

## Executive Summary

This document synthesizes the foundational interrogation conducted for PedagogyX. It highlights the critical path decisions, acknowledged constraints, and open questions that must be resolved before finalizing the architecture and proceeding to Phase 1. The primary focus is on the pivot to Meta Ray-Ban smart glasses (DAT), the India-first launch strategy, and the strict adherence to DPDP compliance.

## Key Product Decisions (Confirmed)

1.  **Primary Client:** Meta Ray-Ban smart glasses tethered to an Android device (DAT companion app). Fixed-room cameras (smartboards) are deferred to Phase 1b.
2.  **Target Market:** India first (K-12 district + university).
3.  **End User / Buyer:** School and university administration (principal/dean/campus IT).
4.  **Core Value Proposition:** Monitor and assess teacher pedagogy, not student scoring.
5.  **Infrastructure Model:** Free pilot (₹0 budget per classroom/year for schools). Infrastructure costs subsidized by founder/dev budget.
6.  **AI/ML Strategy:** Open-source first (Ollama/vLLM on-prem). Maximum GPU: RTX 5070 12 GB.
7.  **Data Processing:** Hybrid (LAN edge buffer + India cloud GPU analytics).

## Critical Architectural Implications

1.  **Data Residency:** India DPDP compliance is mandatory. All data must reside within India (e.g., AWS `ap-south-1`).
2.  **Latency & Connectivity:** The system must handle unreliable classroom network conditions. The edge buffer (Android DAT) is crucial for preventing data loss during multi-hour outages.
3.  **Language Support:** The NLP pipeline must support English and Hindi simultaneously, handling code-switching seamlessly.
4.  **Hardware Constraints:** The RTX 5070 12GB limitation forces strict optimization. Large models must be quantized (e.g., Qwen2.5-7B-Q4), and batch processing will dominate over real-time inference for deep pedagogical analysis.

## Open Questions & Required Clarifications (Founder Action Required)

1.  **Language Priorities:** Are we strictly prioritizing Hindi and English ASR, or are regional dialects (e.g., Marathi, Tamil) required for the India launch?
2.  **Consent Mechanisms:** Given DPDP regulations, how is parental consent for capturing identifiable student video (D-03) being collected and managed in rural school districts?
3.  **Live vs. Batch Analytics:** While real-time coaching (D-04) is requested, the 12GB VRAM limit makes this challenging for complex multimodal models. What is the acceptable latency for "real-time" feedback (seconds vs. minutes)?
4.  **Admin Dashboard Fatigue:** How do we intend to present pedagogy scores for 50+ classrooms without overwhelming the principal?

## Next Steps

1.  Obtain founder answers to the open questions listed above.
2.  Initiate Phase 1: Competitive Analysis and Research phase, focusing heavily on India-specific ed-tech competitors and multimodal AI research constrained by edge hardware.
