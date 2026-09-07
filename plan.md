1. **Explore the codebase**:
   - Check the `README.md` and `AGENTS.md` at the root.
   - Explore backend directories to understand the architecture, database setup, caching mechanisms, API setup, worker models, metrics, queues, and testing frameworks.
   - Run tests if applicable to see the starting state.

2. **Generate the Backend Architecture Report**:
   - According to instructions, for every backend task as the Senior Backend Developer, I must output a report with 11 sections.
   - Let's check memory for the exact rules: "When generating architectural reports as the Autonomous Senior Backend Developer & Distributed Systems Architect, store them in the `docs/05-architecture/` directory using incrementally versioned filenames (e.g., `BACKEND_ARCHITECTURE_REPORT_v3.md`)."
   - Output must contain EXACTLY 11 sections.
   - Wait, the main prompt says 11 sections for System Design ("System Overview, High Level Architecture, Infrastructure Design, Database Design, Scalability Strategy, Reliability Strategy, Security Architecture, Observability Stack, Performance Optimization, Tradeoffs, and Agile Sprint Plan").
   - Wait, wait, let's look at the memory.
     - "For every backend engineering task output: System & Requirement Analysis, Backend Architecture, Database Design, API Strategy, Scalability Strategy, Reliability Strategy, Security Strategy, Observability, Performance Optimization, Risks & Tradeoffs, Agile Sprint Plan" -> This is 11 sections from the Master Prompt.
     - "When generating architectural reports as the Autonomous Senior Backend Developer & Distributed Systems Architect, store them in the `docs/05-architecture/` directory using incrementally versioned filenames (e.g., `BACKEND_ARCHITECTURE_REPORT_v3.md`)."
     - Let's look at `BACKEND_ARCHITECTURE_REPORT_v2.md` and use it as a base, expanding it with the deep exploration of the codebase.

3. **Verify the task outcome**:
   - Save the file at `docs/05-architecture/BACKEND_ARCHITECTURE_REPORT_v3.md`.
   - Run `ls -la docs/05-architecture/BACKEND_ARCHITECTURE_REPORT_v3.md` and `cat docs/05-architecture/BACKEND_ARCHITECTURE_REPORT_v3.md` to ensure correct formatting and content.

4. **Complete Pre-Commit Steps**:
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.

5. **Submit changes**:
   - Commit and submit.
