# Competitor Analysis Report

**Status:** Draft v0.1
**Date:** 2026-05-20
**Owner:** Architecture Team

## Overview

This document evaluates all major global systems in the classroom analytics and educational video space to understand PedagogyX's competitive positioning, particularly within the India supervision market.

## 1. Edthena

**Strengths:**

- Market leader in the US for union-friendly instructional coaching.
- Strong video comment threading and reflection prompts.
- Established UI/UX for peer collaboration.
- AI Coach by Edthena handles basic self-reflection well.

**Weaknesses:**

- Expensive enterprise SaaS model.
- Highly dependent on human coaching loops.
- Limited multi-modal AI fusion (primarily ASR-based AI Coach).
- Lacks real-time analytics or "supervision" features.

**Architecture Assumptions:**

- Monolithic web app, heavily utilizing AWS (S3 for video storage, Transcribe for ASR).
- Asynchronous batch processing only.

**Differentiators vs PedagogyX:**

- PedagogyX will differentiate via multimodal fusion (CV + Audio), supervision-mode focus, and a much lower operating cost through OSS models and edge/hybrid infra.

## 2. Vosaic

**Strengths:**

- Extremely robust timeline marking and video clipping.
- Handles medical/simulation domains well (adjacencies).
- Fine-grained access control and sharing links.

**Weaknesses:**

- Minimal automated AI analytics (manual tagging focus).
- No real-time inference.
- Hardware agnostic but requires user-driven workflows.

**Architecture Assumptions:**

- Cloud-native video streaming (HLS/DASH) with heavily customized player overlays.

**Differentiators vs PedagogyX:**

- Vosaic is an annotation tool; PedagogyX is an _autonomous intelligence_ tool. We automate the tagging that Vosaic requires humans to do.

## 3. IRIS Connect

**Strengths:**

- Excellent proprietary hardware integration (Discovery Kit cameras, beamforming mics).
- "Go Live" in-ear coaching capability.
- Strong presence in UK and EU.

**Weaknesses:**

- High hardware capital expenditure (CapEx) for schools.
- Walled garden ecosystem.

**Architecture Assumptions:**

- Dedicated hardware appliances streaming RTMP/WebRTC to central cloud instances.
- Proprietary low-latency relay servers for the live coaching audio.

**Differentiators vs PedagogyX:**

- PedagogyX relies on _zero_ specialized hardware (low-end Android/Windows only), significantly lowering the barrier to entry for the Indian market.

## 4. AI Sokrates

**Strengths:**

- Pedagogical frameworks (TPACK indices) natively integrated.
- Educational data mining focus.

**Weaknesses:**

- Academic/research-heavy; less polished enterprise UI.
- Processing scale limitations.

**Architecture Assumptions:**

- Likely uses Python-heavy data science pipelines (Pandas, Scikit-learn, potentially older HuggingFace models) run in batch over uploaded videos.

**Differentiators vs PedagogyX:**

- PedagogyX will operationalize TPACK-style metrics into a reliable, enterprise-grade, auto-scaling inference pipeline using TensorRT and faster-whisper.

## 5. Chinese Smart Classroom Systems (e.g., Seewo, iFlytek)

**Strengths:**

- Incredible scale and multimodal integration.
- Hardware-software tight coupling (interactive flat panels with built-in arrays).
- Normalizes "supervision" (督导) and real-time principal dashboards.

**Weaknesses:**

- Severe privacy and ethical concerns outside China.
- Closed, proprietary ecosystems.

**Architecture Assumptions:**

- Edge AI integrated directly into the smartboards (NPU/Rockchip SOCs) running specialized CV/ASR models locally, streaming telemetry to central data centers.

**Differentiators vs PedagogyX:**

- PedagogyX targets a similar "supervision" outcome but uses a DPDP-compliant, OSS-first, hardware-agnostic hybrid architecture, avoiding vendor lock-in.

## 6. Corporate / Meeting Analytics (Zoom AI, Teams, Google Meet, Gong)

**Strengths:**

- World-class ASR, speaker diarization, and LLM summarization.
- Zero extra hardware required for online classes.

**Weaknesses:**

- Completely fail in physical, multi-cam, multi-speaker physical classrooms.
- General-purpose LLMs lack pedagogical domain knowledge (they summarize content, not teaching effectiveness).

**Architecture Assumptions:**

- Massive hyperscaler infrastructure with proprietary large-scale ASR (e.g., MS Teams' speech models).

**Differentiators vs PedagogyX:**

- Meeting tools measure "who spoke". PedagogyX measures _how_ they spoke, classifying discourse moves (probing, revoicing) and analyzing physical classroom interactions via CV.

## Strategic Opportunities for Disruption

1. **Hardware Agnosticism:** By supporting arbitrary low-end Android and Windows devices, PedagogyX sidesteps the hardware CapEx of IRIS Connect.
2. **Cost Structure:** Utilizing OSS models (faster-whisper, YOLO, Ollama) on a centralized hybrid-edge cluster (ADR-0008) allows a disruptive pricing model (starting with ₹0 founder-funded pilots).
3. **Supervision Focus in Emerging Markets:** Edthena and Vosaic deliberately avoid "supervision" for union reasons. PedagogyX embraces this for the Indian market, building admin-first dashboards for quality control.
4. **Multimodal Automation:** Replacing human annotation (Vosaic) with multimodal AI (Sokrates-like, but enterprise-grade).
