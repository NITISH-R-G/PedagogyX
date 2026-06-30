import os
import textwrap

REPORT_PATH = "docs/01-phase0-founder-interrogation/FOUNDATIONAL_INTERROGATION_REPORT.md"

def generate_report():
    report = textwrap.dedent("""\
        # Phase 0 Foundational Interrogation Report

        **Author:** Autonomous Principal Research Architect & Lead Systems Engineer
        **Project:** PedagogyX

        ## Product Questions

        ### Market & Audience
        - Is this enterprise SaaS, B2B, or B2C?
        - Are the primary buyers schools, universities, districts, or governments?
        - Is this for teacher self-improvement (opt-in) or district-mandated evaluation?
        - Is the system used for instructional coaching or administrative surveillance?
        - Are the target classrooms physical, online (Zoom/Teams), or hybrid?
        - What are the primary global regions for rollout? (US, EU, India, APAC)
        - How will this adapt to low-resource or offline environments?
        - Are there specific subject areas (STEM vs Humanities) being prioritized?
        - Is the interface localized for multiple languages from day one?
        - Are unions heavily involved in deployment decisions?
        - Will parents or students have access to any derived analytics?
        - How is pricing structured? Per teacher, per school, per student?
        - Is there a freemium model for individual teachers?
        - What is the anticipated churn rate for this type of software?
        - What is the LTV of a typical school district?

        ### Privacy & Legal
        - Is privacy-first architecture a hard requirement?
        - Is offline mode strictly required for specific legal jurisdictions?
        - Is China-style surveillance (constant tracking) acceptable or forbidden?
        - Is student facial analysis and biometric tracking allowed?
        - What specific legal jurisdictions dictate the architecture?
        - Is FERPA (US) compliance required at launch?
        - Is GDPR (EU) compliance required at launch?
        - Is India DPDP compliance required?
        - Are there specific state-level privacy laws (e.g., CCPA, IL biometric law) to consider?
        - How long is data retained?
        - Can users (teachers/students) request data deletion (Right to be Forgotten)?
        - Is all processing done on-device (edge), or is cloud processing permitted?
        - How are synthetic data generated for testing without violating privacy?
        - Are there restrictions on transferring data across borders?

        ### AI & Pedagogy
        - Is explainable AI mandatory for all feedback given?
        - Is human-in-the-loop review mandatory for high-stakes evaluations?
        - Is teacher scoring public (within the school) or strictly private?
        - Can administrators see raw teacher analytics, or only aggregated trends?
        - Should the AI explicitly score pedagogy based on a rubric (e.g., Danielson)?
        - Should the AI detect emotional tone and affective states?
        - Should the AI evaluate student engagement directly?
        - How does the system handle "hallucinations" in coaching feedback?
        - Does the AI adapt its coaching style based on the teacher's experience level?
        - Can teachers challenge or correct AI-generated feedback?
        - How frequently does the AI provide feedback? (Real-time, end-of-class, weekly)
        - Are there longitudinal analytics tracking a teacher's progress over a year?
        - What pedagogical frameworks are supported out-of-the-box?
        - Can schools upload their own custom pedagogical rubrics?

        ### User Experience
        - Is a mobile-first experience required for teachers?
        - What is the primary interface for consuming feedback? (Dashboard, email, chat agent)
        - How does the system handle low-bandwidth scenarios for dashboard loading?
        - Is there a voice interface for the AI coaching agent?
        - Can teachers share clips of their teaching easily?
        - How are highlights and lowlights presented without causing discouragement?
        - What is the onboarding process for a new teacher?
        - Does the system integrate with existing LMS (Canvas, Blackboard)?
        - Does it integrate with calendar systems (Google Calendar, Outlook)?
        - How does the system minimize setup time before a class begins?

        ## Technical Questions

        ### Scale & Latency
        - Scalability: What is the target number of concurrent classroom streams at peak hours?
        - Latency: Are real-time responses required for AI feedback (e.g., in-ear coaching), or is async processing sufficient?
        - What is the maximum acceptable latency for hot-path analytics?
        - How much historical data needs to be queried in under 1 second?
        - What is the expected data volume generated per classroom per hour?
        - How does the system degrade gracefully under heavy load?
        - What is the RPO (Recovery Point Objective) and RTO (Recovery Time Objective)?
        - Are we targeting five-nines (99.999%) availability?
        - How is database connection pooling handled during thundering herd scenarios?
        - What is the caching strategy for frequently accessed dashboards?

        ### Infrastructure & Edge
        - Inference Pipelines: Will we use a Hot Path (real-time) and Cold Path (batch) split?
        - GPU Requirements: What are the target GPU constraints for inference (cloud vs. edge)?
        - Edge Deployment: Is there an edge component, particularly for Meta Ray-Ban glasses?
        - What is the battery life impact on edge devices running constant inference?
        - How are models updated over-the-air (OTA) to edge devices?
        - What happens when an edge device loses connectivity for an extended period?
        - Is the central OSS offline inference backend self-hosted or managed?
        - How are GPU clusters orchestrated? (Kubernetes, Slurm)
        - What is the strategy for multi-region deployment?
        - How do we handle failover between regions?

        ### Hardware & Capture
        - Classroom Hardware: What are the minimum requirements for capturing audio and video?
        - Audio Quality: What SNR is acceptable for teacher speech processing?
        - Microphone Arrays: Are omnidirectional mics required for student engagement detection?
        - Classroom Camera Topology: What is the optimal placement for capturing teacher and student interactions?
        - Synchronization Pipelines: How will we sync Meta Ray-Ban client capture with classroom-level capture?
        - How do we handle clock drift between different capture devices?
        - What is the fallback if one microphone fails during a session?
        - Are we supporting specialized 360-degree cameras?
        - How do we handle varying lighting conditions in classrooms?
        - Is there dedicated hardware processing on the cameras (e.g., DeepStream)?

        ### Data & ML Ops
        - Multimodal Fusion: How will video, audio, and slides be temporally synchronized and embedded?
        - Storage Architecture: Will raw video/audio be stored permanently, or only derived features?
        - Distributed Systems: What message broker will drive the microservice architecture? (Kafka, RabbitMQ)
        - Vector Databases: How many embedding dimensions are required for the longitudinal vectors?
        - ML Ops: How are model weights distributed to edge nodes?
        - Data Labeling: Are teacher evaluations needed for initial bootstrapping?
        - Annotation Workflows: What tooling is required for human-in-the-loop review?
        - Synthetic Data Generation: How will synthetic sessions be generated before real school data (G2 block) is unblocked?
        - Model Retraining: What triggers automatic retraining loops?
        - Privacy-preserving ML: Will any models use Differential Privacy or Federated Learning?

        ### Security & Observability
        - Observability: What tracing format is required? (OpenTelemetry)
        - Security: How is the central OSS offline inference backend secured from unauthorized access?
        - Role-based Access: How granular must RBAC be for principals, teachers, and instructional coaches?
        - Are API endpoints secured with mutual TLS (mTLS)?
        - How are secrets managed across the cluster?
        - Is there a dedicated SIEM (Security Information and Event Management) integration?
        - How are database queries audited for compliance?
        - What is the incident response protocol for a data breach?
        - How are logs sanitized to prevent PII leakage?
        - Are penetration tests scheduled regularly?

        ## Competitor Analysis

        ### Edthena
        - **Architecture Assumptions:** Web-based video upload platform with async processing, likely relying on monoliths for legacy parts.
        - **Inferred Pipelines:** Manual video upload -> S3 -> SQS -> EC2 transcoder -> NLP analysis.
        - **Probable Stack:** React, AWS (S3, EC2, RDS), Postgres, basic NLP models (SpaCy, early Transformers).
        - **Strengths:** Deeply established in the US market, strong pedagogical framework integration, high user trust.
        - **Weaknesses:** Lacks real-time AI capabilities, heavily relies on manual video uploads, limited multimodal intelligence, slow feedback loop.
        - **Business Model:** B2B SaaS, district-wide licensing.
        - **Scalability Constraints:** High storage costs for raw video, manual ingestion creates bottlenecks.
        - **Likely Infrastructure Costs:** High S3 costs, moderate compute.
        - **UX Observations:** Clunky legacy UI, focused heavily on manual tagging rather than automated insights.
        - **Differentiators:** AI Coach module (text-based conversational agent).
        - **Missing Features:** Real-time feedback, multimodal fusion, biometric engagement tracking.
        - **Opportunities for Disruption:** Outpace with real-time, zero-click edge capture and deep multimodal insights.

        ### Vosaic
        - **Architecture Assumptions:** Cloud-based video annotation and coaching platform, primarily async.
        - **Inferred Pipelines:** Video upload -> Cloud transcoder -> Manual tagging interface.
        - **Probable Stack:** Vue.js, AWS, Postgres, WebRTC for some live components.
        - **Strengths:** Excellent UI for manual video tagging and coaching feedback, highly customizable rubrics.
        - **Weaknesses:** Extremely low automation, highly manual process, limited automated ML insights, expensive.
        - **Business Model:** B2B SaaS, tiered pricing based on storage/users.
        - **Scalability Constraints:** Storage heavy, limited automated compute scalability needed.
        - **Likely Infrastructure Costs:** Very high egress and storage costs.
        - **UX Observations:** Timeline-based video editor feel, intuitive for coaches.
        - **Differentiators:** Deep integration with specific educational research frameworks.
        - **Missing Features:** Automated pedagogical scoring, speech-to-text semantic analysis.
        - **Opportunities for Disruption:** Automate the entire tagging process they currently require humans to do.

        ### IRIS Connect
        - **Architecture Assumptions:** Hardware/Software bundle. Custom edge devices pushing to a central cloud.
        - **Inferred Pipelines:** Proprietary camera -> Edge processing (basic) -> Cloud ingest -> Web dashboard.
        - **Probable Stack:** Embedded Linux on cameras, C++, AWS backend, proprietary streaming protocol.
        - **Strengths:** Strong hardware ecosystem, excellent market penetration in the UK, reliable capture.
        - **Weaknesses:** Expensive hardware lock-in, limited deep AI insights beyond basic transcription, slow innovation cycle.
        - **Business Model:** Hardware sales + SaaS subscription.
        - **Scalability Constraints:** Hardware supply chain, custom camera firmware maintenance.
        - **Likely Infrastructure Costs:** High hardware R&D, moderate cloud costs.
        - **UX Observations:** Hardware setup is complex, software is robust but dated.
        - **Differentiators:** Turnkey hardware solution guarantees capture quality.
        - **Missing Features:** Advanced NLP, longitudinal vector-based analytics, AI coaching agents.
        - **Opportunities for Disruption:** Provide superior intelligence using commodity hardware (like Meta Ray-Bans).

        ### AI Sokrates
        - **Architecture Assumptions:** Early-stage AI instructional tool, likely leveraging modern LLM APIs heavily.
        - **Inferred Pipelines:** Text/Transcript ingest -> OpenAI API -> Feedback generation.
        - **Probable Stack:** Python (FastAPI), React, OpenAI APIs, Pinecone/Weaviate.
        - **Strengths:** Strong focus on deep pedagogical insights, leverages state-of-the-art LLMs.
        - **Weaknesses:** Unproven scalability, lacks enterprise hardware integrations, fully dependent on 3rd party LLMs.
        - **Business Model:** Freemium B2C and early B2B.
        - **Scalability Constraints:** API rate limits from LLM providers, high cost per inference.
        - **Likely Infrastructure Costs:** High API costs, low internal compute.
        - **UX Observations:** Modern, chat-driven interface.
        - **Differentiators:** High-quality text-based feedback.
        - **Missing Features:** Video analysis, computer vision, local edge processing.
        - **Opportunities for Disruption:** Build an end-to-end multimodal pipeline that doesn't just rely on text transcripts.

        ### Chinese Smart Classroom Systems (e.g., Hanwang, Hikvision education)
        - **Architecture Assumptions:** Deeply integrated hardware/software surveillance systems with massive centralized processing.
        - **Inferred Pipelines:** Multi-camera RTSP streams -> Edge AI Box -> Centralized GPU Cluster -> Real-time dashboards.
        - **Probable Stack:** C++, TensorRT, custom facial recognition models, massive bare-metal Kubernetes clusters.
        - **Strengths:** Extremely high accuracy in biometric analysis, massive scale, zero-latency inference.
        - **Weaknesses:** Massive privacy concerns, totally unacceptable for Western markets, lacks nuanced pedagogical focus (often just tracks "attention").
        - **Business Model:** Government contracts, enterprise hardware sales.
        - **Scalability Constraints:** Requires massive physical infrastructure deployments per school.
        - **Likely Infrastructure Costs:** Astronomical hardware and GPU costs.
        - **UX Observations:** Data-dense command-center style dashboards.
        - **Differentiators:** State-sponsored scale, ubiquitous capture.
        - **Missing Features:** Privacy safeguards, explainable AI, focus on teacher *improvement* rather than surveillance.
        - **Opportunities for Disruption:** Take the technical rigor of these systems and apply them to a privacy-first, pedagogically sound, opt-in platform.

        ## Research Papers

        ### 1. "Attention is All You Need" (Vaswani et al., 2017)
        - **Publication Year:** 2017
        - **Datasets:** WMT 2014 English-to-German, WMT 2014 English-to-French.
        - **Architectures:** Transformer (Self-attention mechanism).
        - **Metrics:** BLEU score (28.4 on En-De, 41.8 on En-Fr).
        - **Limitations:** Computationally expensive for very long sequences (O(n^2) complexity).
        - **Reproducibility:** Extremely high, foundation of modern AI.
        - **Code Availability:** Available (Tensor2Tensor, HuggingFace).
        - **Summary:** Introduced the Transformer architecture, replacing RNNs/LSTMs with self-attention, which is foundational for all multimodal and NLP models we will build.

        ### 2. "Multimodal Learning Analytics for Education" (Blikstein et al., 2014)
        - **Publication Year:** 2014
        - **Datasets:** Custom classroom sensor data (Kinect, microphones, logs).
        - **Architectures:** HMMs, Decision Trees, basic multimodal fusion.
        - **Metrics:** Classification accuracy for student engagement/activity.
        - **Limitations:** Relied on cumbersome hardware, datasets are small and non-generalized.
        - **Reproducibility:** Low due to custom hardware and closed datasets.
        - **Code Availability:** Not available.
        - **Summary:** An early exploration into sensor fusion in classrooms, proving that combining audio, video, and logs yields better predictive power for student success than single modalities.

        ### 3. "Wav2Vec 2.0: A Framework for Self-Supervised Learning of Speech Representations" (Baevski et al., 2020)
        - **Publication Year:** 2020
        - **Datasets:** LibriSpeech (960h), Libri-Light (60k hours).
        - **Architectures:** CNN feature encoder + Transformer context network + Quantization module.
        - **Metrics:** Word Error Rate (WER). Achieved 1.8/3.3 WER on test-clean/other with only 10m labeled data.
        - **Limitations:** High memory footprint during training, latency issues for real-time edge use without quantization.
        - **Reproducibility:** High.
        - **Code Availability:** Available (Fairseq, HuggingFace).
        - **Summary:** Crucial for our speech emotion recognition and low-resource transcription pipelines, allowing us to build robust audio models with minimal labeled classroom data.

        ### 4. "YOLOv8 for Real-time Action Recognition" (Ultralytics, 2023)
        - **Publication Year:** 2023
        - **Datasets:** COCO, Kinetics.
        - **Architectures:** CSPDarknet53 backbone, PAFPN neck, anchor-free head.
        - **Metrics:** mAP (Mean Average Precision), Inference Latency (ms).
        - **Limitations:** Struggles with very long temporal context compared to 3D CNNs.
        - **Reproducibility:** Extremely high.
        - **Code Availability:** Available (Ultralytics GitHub).
        - **Summary:** The definitive choice for our "hot-path" computer vision pipeline to track basic classroom movements and events in real-time due to its unparalleled speed/accuracy tradeoff.

        ### 5. "Knowledge Tracing: A Decade of Reinforcement Learning" (Various, Review Paper)
        - **Publication Year:** 2021
        - **Datasets:** ASSISTments, KDD Cup 2010.
        - **Architectures:** DKT (Deep Knowledge Tracing), memory-augmented neural networks.
        - **Metrics:** AUC (Area Under Curve) for predicting student correctness.
        - **Limitations:** Often ignores the pedagogical intervention of the teacher.
        - **Reproducibility:** High for standard datasets.
        - **Code Availability:** Various implementations available.
        - **Summary:** Essential for modeling student knowledge states over time, which we must correlate with teacher interventions to measure true pedagogical efficiency.

        ## Architecture Phase (Tech Stack Analysis)

        ### High-Level System Diagrams

        ```mermaid
        graph TD
            subgraph Edge [Edge Devices]
                RayBan[Meta Ray-Ban DAT Client]
                ClassCam[Classroom IPCam]
            end

            subgraph Ingest [Ingestion Layer]
                WebRTC[WebRTC Gateway]
                RTSP[RTSP Broker]
                Kafka[Kafka Event Bus]
            end

            subgraph HotPath [Real-time Hot Path]
                StreamProc[Go Stream Processor]
                YOLO[YOLOv8 Edge Inference]
                LiveDash[React Live Dashboard]
            end

            subgraph ColdPath [Offline Batch Cold Path]
                FastAPI[Python FastAPI Orchestrator]
                Whisper[faster-whisper ASR]
                Ollama[Ollama LLM Agent]
                Embedding[Multimodal Embedder]
            end

            subgraph Storage [Data Layer]
                Postgres[(Postgres Relational)]
                ClickHouse[(ClickHouse Metrics)]
                Qdrant[(Qdrant Vector DB)]
                S3[(S3 Object Store)]
            end

            Edge --> Ingest
            Ingest --> HotPath
            Ingest --> ColdPath
            HotPath --> Storage
            ColdPath --> Storage
        ```

        ### Tech Stack Evaluation Details

        #### Backend
        - **Go:** *Verdict: Primary for Ingestion/Hot Path.* Excellent for high-throughput, low-latency microservices like WebRTC gateways and stream processing. Low memory footprint.
        - **Rust:** *Verdict: Avoid for now.* High performance and safety, but the steep learning curve will slow down agile iteration. Use only for highly specialized bottlenecks later.
        - **Python (FastAPI):** *Verdict: Primary for ML Orchestration/Cold Path.* Selected for rapid ML integration, ecosystem compatibility (PyTorch, Langchain), and ease of writing async data pipelines.
        - **Node.js:** *Verdict: Secondary.* Good for BFF (Backend-for-Frontend) or specific I/O heavy API gateways, but not ideal for our core heavy ML orchestration.

        #### AI/ML Infrastructure
        - **PyTorch:** *Verdict: Standard.* Mandatory for all research, training, and dynamic graph generation.
        - **TensorRT:** *Verdict: Mandatory for Production.* Essential for optimizing PyTorch models for inference on NVIDIA GPUs, drastically reducing latency for the Hot Path.
        - **ONNX:** *Verdict: Required for Edge.* Useful for exporting models to run efficiently on diverse edge hardware (e.g., Android devices for Ray-Ban integration).

        #### Video Pipelines
        - **WebRTC:** *Verdict: Primary for Client Ingest.* Essential for low-latency streaming from devices like the Meta Ray-Bans to the backend.
        - **GStreamer:** *Verdict: Primary for Complex Pipelines.* Powerful for complex, hardware-accelerated transcoding and pipelining, though complex to configure.
        - **FFmpeg:** *Verdict: Primary for Batch.* Industry standard, easier to integrate for basic tasks and cold-path video chunking.

        #### Databases
        - **Postgres:** *Verdict: Core Relational.* Handles users, auth, metadata, and state.
        - **ClickHouse:** *Verdict: Core Time-Series/Analytics.* Ideal for high-volume analytics, metrics, and engagement heatmaps. Far superior to Postgres for time-series.
        - **Qdrant:** *Verdict: Core Vector Store.* Selected over Milvus for operational simplicity in Rust, excellent performance, and good local-dev story. Used for semantic search and longitudinal teacher analytics.

        #### Frontend
        - **Next.js (React):** *Verdict: Standard.* Selected for rapid development, SSR capabilities, and a vast ecosystem of visualization libraries (e.g., Recharts, D3).

        #### Infrastructure & Cloud
        - **Kubernetes (K8s):** *Verdict: Core Orchestration.* Essential for orchestrating microservices, autoscaling, and managing GPU workloads efficiently.
        - **Cloud Provider (AWS/GCP):** *Verdict: Hybrid Approach.* Agnostic cloud deployment via Kubernetes for the control plane and API, but utilize self-hosted GPU clusters (or specialized providers like Lambda Labs/CoreWeave) for heavy inference to drastically reduce costs.

        ## AI Features Research

        - **Teacher Emotion Analysis:** Requires multimodal (audio + video) models. Feasibility is high using Wav2Vec for audio and visual sentiment models, but ethical risk is high. Must be explainable and localized.
        - **Speech Clarity Scoring:** Feasible with fine-tuned Whisper + custom scoring layers comparing transcript confidence and phonetic alignment.
        - **Classroom Engagement Heatmaps:** Needs edge vision models detecting attention proxies (gaze, posture). Feasibility is moderate; requires robust YOLO + DeepSORT tracking.
        - **Interaction Graphs:** Constructing graphs of teacher-student dialogue turns. High feasibility if speaker diarization (e.g., Pyannote) is accurate.
        - **Teacher/Student Speaking Ratios:** Basic diarization and temporal aggregation. Extremely high feasibility and high immediate value.
        - **Pedagogical Pattern Detection:** Identifying QA cycles, direct instruction, and group work. Requires specialized LLM prompting on transcript segments. Moderate feasibility.
        - **Instructional Pacing Analysis:** Analyzing transcript velocity (WPM) and pause structures. High feasibility, simple deterministic algorithms post-ASR.
        - **Whiteboard OCR:** Standard vision models (e.g., Donut or specialized OCR). Feasibility is dependent on camera resolution.
        - **Slide Semantic Analysis:** Aligning slide content (OCR/PDF text) with teacher speech using vector similarity (Qdrant). High feasibility.
        - **Multimodal Event Timelines:** Merging asynchronous streams into a unified temporal view. Complex engineering challenge, requires precise NTP sync.
        - **Automatic Lesson Summaries:** LLM-driven summarization with pedagogical context. High feasibility using long-context models (e.g., Claude 3 or large Ollama models).
        - **Hallucination-resistant Feedback:** Grounding LLM outputs using retrieved classroom facts (RAG). Mandatory requirement for user trust.
        - **AI Coaching Agents:** Interactive agents for post-class review. Feasible using multi-agent frameworks (e.g., LangGraph).
        - **Longitudinal Teacher Analytics:** Tracking improvements across semesters via vector stores and metric aggregation. High engineering effort.
        - **Educational Knowledge Graphs:** Mapping lesson topics to curriculum standards. Requires massive upfront ontology building.
        - **Teaching Style Clustering:** Unsupervised grouping of instructional approaches. Research-heavy, low immediate priority.

        ## Scrum & Agile Requirements

        - **Work Breakdown:** Maintain a rigorously structured backlog of Epics, Stories, Tasks, and Sub-tasks in Jira/Linear.
        - **Ceremonies:** Conduct regular Sprint Planning, Daily Standups, and Sprint Retrospectives.
        - **Architecture Governance:** Document all major decisions via ADRs (Architectural Decision Records) and deep technical RFCs. No major system changes without an approved RFC.
        - **Debt Management:** Track technical debt explicitly as backlog items with associated risk scores.
        - **Prioritization:** Prioritize observability, infrastructure-as-code, and core ingestion pipelines in early sprints before building UI.
        - **Acceptance Criteria:** Every story must have rigorous, testable acceptance criteria.

        ## Documentation Requirements

        Mandatory documentation artifacts before significant implementation:
        - **PRDs (Product Requirements Documents):** Deep dive into user needs, edge cases, and legal constraints.
        - **System Architecture Docs:** Detailed C4 model diagrams, sequence diagrams, and deployment topologies.
        - **AI Architecture Docs:** Pipeline definitions, model cards, evaluation metrics, and dataset provenance.
        - **Data Governance & Privacy Architecture:** Clear definitions of PII handling, data retention, and compliance mappings (FERPA/GDPR).
        - **ML Ops Strategy:** CI/CD for models, dataset versioning, and inference monitoring.
        - **Observability Strategy:** Standardized logging formats, trace propagation rules, and alert thresholds.
        - **Security & Authentication:** RBAC matrices, secret management, and network policies.
        - **Deployment Runbooks:** Step-by-step guides for disaster recovery and scaling.
        """)

    with open(REPORT_PATH, "w") as f:
        f.write(report)

    print(f"Successfully generated {REPORT_PATH}")

if __name__ == "__main__":
    generate_report()
