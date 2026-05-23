# AI Features Feasibility & Architecture Research

**Status:** Draft v1.0
**Date:** 2026-05-20
**Owner:** Senior AI Engineer

This document evaluates the technical feasibility, architectural requirements, and risk profile for the advanced AI capabilities requested for the PedagogyX platform.

## 1. Multimodal Event Timelines & Lesson Summarization

- **Concept:** Automatically generate a navigable timeline of the lesson with chapter markers and a synthesized text summary of the content taught.
- **Architecture:**
  1.  **ASR Pipeline:** `faster-whisper` generates timestamped transcripts.
  2.  **Diarization:** PyAnnote groups speech by speaker (Teacher vs. Student).
  3.  **Slide OCR/Scene Change:** Edge client or cloud worker extracts keyframes on high-delta pixel changes; runs fast OCR (e.g., Tesseract or lightweight Florence-2) to extract slide text.
  4.  **LLM Summarization:** The transcript, combined with OCR text and timestamp metadata, is chunked and fed into `Qwen2.5-7B` via vLLM. The prompt instructs the LLM to output JSON containing chapter titles, timestamps, and brief summaries.
- **Feasibility:** High. This relies on mature technologies (ASR + LLMs) and is highly resilient to low video quality.
- **Risks:** LLM hallucination. Mitigation: Strict prompt engineering forcing the LLM to cite specific line numbers from the transcript.

## 2. Classroom Engagement Heatmaps

- **Concept:** Generate a visual heatmap showing periods of high and low student "engagement" across the 50-minute lesson.
- **Architecture:**
  1.  **CV Inference:** Run a lightweight YOLO-pose model (TensorRT optimized) at 1-2 fps on the student-facing camera feed.
  2.  **Heuristics Engine:** Calculate a composite "Attention Proxy Score" based on face visibility, head yaw/pitch (looking at the teacher/board vs. down/away), and physical movement.
  3.  **Time-Series Aggregation:** Push scores to ClickHouse.
  4.  **Visualization:** Frontend renders an area chart over the video scrubber.
- **Feasibility:** Medium.
- **Risks:** High false-positive rate. Defining "engagement" strictly via CV is pedagogically flawed. A student looking down writing notes is engaged but will score low on face-visibility metrics. Requires significant calibration and contextual fusion (e.g., if the teacher says "write this down," expect heads to drop).

## 3. Teacher/Student Speaking Ratios & Interaction Graphs

- **Concept:** Measure how much the teacher talks vs. students, and map who is talking to whom.
- **Architecture:**
  1.  **Audio Processing:** Relies heavily on robust speaker diarization.
  2.  **Spatial Audio (Future):** If using microphone arrays, calculate angle-of-arrival to separate student voices spatially.
  3.  **Graph Generation:** Store "speaker X spoke after speaker Y" events in Postgres/ClickHouse.
- **Feasibility:** High (for ratio), Low (for precise interaction graphs in v1).
- **Risks:** Single-microphone setups in noisy classrooms make distinguishing individual student voices nearly impossible. We can reliably detect "Teacher vs. Non-Teacher" but separating "Student A" from "Student B" using only audio is a known unsolved problem in wild classroom environments.

## 4. Whiteboard OCR & Slide Semantic Analysis

- **Concept:** Extract equations, diagrams, and text written on the physical whiteboard and compare it against the curriculum standards.
- **Architecture:**
  1.  **Keyframe Extraction:** Identify frames where the teacher steps away from the board.
  2.  **Image Enhancement:** Contrast boosting and perspective correction (homography).
  3.  **VLM Inference:** Pass the cleaned frame to a Vision-Language Model (e.g., Qwen-VL or LLaVA-NeXT) to extract structured data (Markdown/LaTeX).
  4.  **Semantic Search:** Embed the extracted text using an embedding model (e.g., BGE-m3) and query the Qdrant vector database containing the district curriculum.
- **Feasibility:** Medium to Low (for physical whiteboards in low light), High (for digital smartboards).
- **Risks:** Glare, poor handwriting, and low camera resolution (480p from a cheap Android board) will cripple physical OCR. Digital screen capture is the reliable fallback.

## 5. Teacher Emotion Analysis & Speech Clarity Scoring

- **Concept:** Score the teacher's emotional tone and the clarity/pacing of their speech.
- **Architecture:**
  1.  **Acoustic Features:** Extract MFCCs, pitch (F0), and energy using `librosa`.
  2.  **SER Model:** Run a lightweight Speech Emotion Recognition classifier.
  3.  **Clarity Metrics:** Calculate Words Per Minute (WPM) and pause frequency from the Whisper transcript alignments.
- **Feasibility:** High (for pacing/clarity), Low/Risky (for emotion).
- **Risks:** SER models are notoriously biased across cultures and genders. Flagging a teacher as "angry" based on cultural tonal differences in Hindi/English code-switching is a massive liability. **Recommendation:** Do not expose raw emotion scores; use acoustic features only internally as context for the broader LLM analysis.

## 6. Pedagogical Pattern Detection (e.g., Wait Time, Open Questions)

- **Concept:** Detect if a teacher asks a question and waits 3+ seconds for an answer, or if they ask open vs. closed questions.
- **Architecture:**
  1.  **NLP Pipeline:** LLM classifies extracted questions from the transcript as "Open" or "Closed".
  2.  **Temporal Logic:** Combine transcript timings with voice activity detection (VAD). If `Question_End_Time` to `Next_Speech_Start_Time` > 3 seconds, flag as "Successful Wait Time".
- **Feasibility:** High.
- **Risks:** Requires highly accurate word-level timestamps from the ASR model.

## 7. AI Coaching Agents & Hallucination-Resistant Feedback

- **Concept:** An interactive chat agent that helps the teacher reflect on the lesson.
- **Architecture:**
  1.  **RAG System:** The agent retrieves specific timestamped events from the database based on the teacher's query.
  2.  **Constrained Generation:** The LLM prompt heavily penalizes making claims not present in the retrieved context.
- **Feasibility:** High.
- **Risks:** Hallucination. If the AI hallucinates a negative interaction, trust is destroyed instantly. Mitigation involves "Chain of Verification" prompting and requiring the UI to link every AI claim directly to a video timestamp clip.
