# Competitor Analysis: AI Sokrates (HABOOK / TEAM Model)

**Status:** Draft | **Category:** Smart classroom + automated pedagogical analytics (Taiwan/global)

## Executive Summary

AI Sokrates is the closest **operational analog** to PedagogyX vision: **automatic post-lesson analytics** integrated with teaching software (HiTeach), **TPACK-based indices**, and massive scale.

---

## Product Surface **[FACT]**

- **STAS** (Sokrates Teaching Analytics System): automatic behavior analysis from HiTeach-collected data (ICCE 2018 paper)
- **Five indexes:** Technology Interaction (T), Pedagogical Application (P), Content Implementation (C), School-based Comprehensive (D), Learning Engagement (E)
- **Digital lesson observation:** sync/async expert feedback via video, text, audio, image
- **Scale (2023):** ~350,000 lessons, ~10 million student instances (vendor claim)
- Outputs: Sokrates Videos, observation forms, AI transcripts, interaction records

---

## Inferred Architecture

| Layer            | Description                                                                      |
| ---------------- | -------------------------------------------------------------------------------- |
| Data capture     | HiTeach interactive whiteboard + classroom events (not generic phone video only) |
| Analytics engine | Rule + ML hybrid for TPACK indices                                               |
| Platform         | Cloud lesson repository + district dashboards                                    |
| PD loop          | Expert review + AI reports                                                       |

**Key insight:** Deep integration with **proprietary teaching OS** yields richer signals than passive video alone.

---

## Strengths

- **Pedagogical framework** baked into product (TPACK)
- **Proven scale** and government/school deployments
- **Multimodal data** from digital teaching interactions
- Research publications and academic legitimacy

## Weaknesses / Risks

- **Vendor lock-in** to HiTeach ecosystem
- **Surveillance perception** when deployed as oversight
- **Western privacy** alignment unclear (student-level analytics)
- Export / localization barriers

---

## Academic Anchor **[FACT]**

Ku et al., ICCE 2018 — "STAS: An Automatic Teaching Behavior Analysis System for Facilitating Teacher Professional Development"

---

## PedagogyX Lessons

1. **Framework-first analytics** beat raw CV scores
2. **Immediate post-class reports** drive adoption
3. **City/district aggregation** is sellable to governments—ethics must gate this
4. Consider **LMS/whiteboard integrations** as signal sources, not only MP4 files

---

## Sources

- https://www.habook.com/en/cloud.php?act=view&id=17
- https://library.apsce.net/index.php/ICCE/article/view/3731
