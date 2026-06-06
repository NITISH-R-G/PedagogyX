import json
import os
import argparse

# In a real environment, this would call the OpenAI API (e.g., openai.ChatCompletion.create)
# For this script, we'll simulate the AI summarization based on the knowledge graph.

def generate_summary(graph):
    frameworks = ", ".join(graph.get("frameworks", []))
    services = [s["name"] for s in graph.get("services", [])]

    summary = "## AI Generated Architecture Summary\n\n"
    summary += f"This repository is built using **{frameworks}**.\n\n"

    summary += "### Core Services\n"
    for svc in services:
        summary += f"- **{svc}**: Microservice part of the architecture.\n"

    return summary

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Print summary without writing")
    args = parser.parse_args()

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    graph_path = os.path.join(repo_root, "knowledge_graph.json")

    if not os.path.exists(graph_path):
        print("Knowledge graph not found. Run repo_analyzer.py first.")
        return

    with open(graph_path, 'r') as f:
        graph = json.load(f)

    summary = generate_summary(graph)

    if args.dry_run:
        print("--- DRY RUN: AI Documentation Summary ---")
        print(summary)
    else:
        docs_dir = os.path.join(repo_root, "docs")
        os.makedirs(docs_dir, exist_ok=True)
        output_path = os.path.join(docs_dir, "AI_SUMMARY.md")
        with open(output_path, "w") as f:
            f.write(summary)
        print(f"Generated AI documentation at {output_path}")

if __name__ == "__main__":
    main()
