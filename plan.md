1. **Explore the codebase and understand the requirements.**
   - Read the relevant documentation and system architecture reports.
   - Understand the system constraints: FOSS-first, offline inference, RTX 5070 compute constraints, Meta Ray-Ban target device, etc.
   - Read the existing `AI_SYSTEM_ARCHITECTURE_REPORT_v2.md` to see what needs to be improved or what an Elite Senior AI Engineer would produce.
2. **Generate the `AI_SYSTEM_ARCHITECTURE_REPORT_v3.md` file.**
   - It should contain exactly the 11 required sections: `AI Problem Analysis`, `AI System Architecture`, `Prompt & Reasoning Strategy`, `RAG & Retrieval Design`, `AI Infrastructure`, `Evaluation Strategy`, `Security & Safety`, `Observability`, `Performance Optimization`, `Risks & Tradeoffs`, and `Agile Sprint Plan`.
   - Adhere strictly to the requested behavior rules, optimizing for Reliability, Accuracy, Scalability, Maintainability, Inference Efficiency, User Value, Observability, Security, Extensibility, and Long Term Sustainability.
   - Address the system constraints thoroughly.
3. **Verify documentation formatting.**
   - Run `npx markdownlint-cli --fix` and `npx prettier --write` on the newly created file.
4. **Complete pre commit steps to ensure proper testing, verification, review, and reflection are done.**
5. **Submit the change.**
