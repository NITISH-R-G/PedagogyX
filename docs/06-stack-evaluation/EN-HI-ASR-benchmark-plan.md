# EN+HI ASR Benchmark Plan (OSS Context)

**Goal:** Establish baseline Word Error Rate (WER) and Real-Time Factor (RTF) for code-switched English/Hindi speech in noisy Indian classroom environments, targeting an OSS-only pipeline.

## 1. Candidate Models

Since the founder mandated an OSS-first approach (ADR-0005) running on central GPU servers (RTX 5070 dev / similar prod specs), candidate models are:

1. **faster-whisper large-v3** (INT8 quantization via CTranslate2) - Baseline for accuracy.
2. **faster-whisper medium** (INT8) - Baseline for real-time edge processing.
3. **NVIDIA Nemo Conformer** (Indic languages specialized, if license permits).

_(Note: Cloud APIs like Deepgram or Google STT are excluded due to FOSS mandate, but may be used strictly for one-off golden label generation)._

## 2. Dataset Requirements

To simulate target conditions, we need a 10-hour golden dataset:

- **Demographics:** Indian K-12 teachers and students.
- **Acoustics:** High background noise (ceiling fans, traffic, echoey concrete rooms).
- **Linguistics:** Fluent code-switching between Hindi and English mid-sentence.
- **Hardware:** Captured via low-end laptop/Smartboard mics, not studio equipment.

## 3. Benchmark Metrics

1. **WER (Word Error Rate):** Overall error rate.
2. **Code-Switch WER:** Error rate specifically at the boundary where the speaker switches languages.
3. **RTF (Real-Time Factor):** Time taken to transcribe 1 hour of audio on the target GPU architecture. Target: RTF < 0.1 for batch.
4. **VRAM Peak:** Maximum memory footprint during inference to ensure it fits alongside other processes.

## 4. Execution Steps

- **Step A:** Acquire 10 hours of representative audio (consent required).
- **Step B:** Manually label to create the Ground Truth transcript.
- **Step C:** Script `bench_whisper.py` to run candidates against the dataset.
- **Step D:** Evaluate results and lock in the model size for the V1 release.
