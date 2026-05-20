# Literature Review: Validity of Automated Pedagogy Indices

**Status:** Draft / Work in Progress
**Context:** PedagogyX intends to synthesize multiple metrics (talk ratios, engagement CV, etc.) into a single, admin-visible "Pedagogy Index". This review assesses the scientific validity of such composites.

## 1. Flanders Interaction Analysis Categories (FIAC)

Flanders (1970) pioneered systematic observation of classroom interaction.

- **Validity:** Highly validated in traditional settings, correlating indirect teacher influence (praising, accepting ideas) with higher student achievement.
- **Automation Potential:** High. Modern NLP and speaker diarization can classify discourse moves into FIAC-like categories (e.g., Donnelly et al., 2016).

## 2. Talk Ratios (Teacher-vs-Student)

- **Validity:** The "80/20 rule" (teacher talks 80%, students 20%) is often cited as a negative baseline. Hattie's meta-analyses suggest that increasing student voice (dialogic teaching) improves outcomes.
- **Risk:** Optimizing purely for a low teacher talk ratio can penalize direct instruction or lecture-heavy subjects, which are sometimes pedagogically necessary.

## 3. Computer Vision Engagement Proxies

- **Validity:** Weak to Moderate. Studies (e.g., Kaur et al., 2016 DAiSEE dataset) show that posture, gaze, and facial expressions correlate with _behavioral_ engagement, but not necessarily _cognitive_ engagement.
- **Risk:** High risk of algorithmic bias against neurodivergent students or different cultural expressions of attention. Using CV engagement as a punitive admin score is scientifically unsafe.

## 4. Constructing a Composite Index

Research warns against reducing complex teaching into a single numerical score without human context (e.g., the Gates Foundation MET project highlighted the need for multiple measures).

- **Recommendation:** If a composite index is required for the "supervision" mode, it must be framed as an _indicative proxy_ rather than a definitive evaluation. The UI should emphasize the sub-metrics (e.g., "Wait Time", "Questioning Rate") over the final rolled-up number.
