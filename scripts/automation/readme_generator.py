import json
import os

def load_graph(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def load_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return f.read()
    return ""

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    graph_path = os.path.join(repo_root, "knowledge_graph.json")

    if not os.path.exists(graph_path):
        print("Knowledge graph not found. Run repo_analyzer.py first.")
        return

    graph = load_graph(graph_path)

    # Load dynamically generated parts
    diagrams_path = os.path.join(repo_root, "docs/architecture-diagrams.md")
    diagrams_content = load_file(diagrams_path)
    # Demote headings for inclusion in README
    diagrams_content = diagrams_content.replace("# Architecture Diagrams\n", "## Architecture Diagrams\n\n").replace("## Architecture\n", "### Architecture\n\n").replace("## Services\n", "### Services\n\n")

    ai_summary_path = os.path.join(repo_root, "docs/AI_SUMMARY.md")
    ai_summary_content = load_file(ai_summary_path)
    # Demote headings for inclusion in README
    ai_summary_content = ai_summary_content.replace("# AI Generated Architecture Summary (Fallback)\n", "## AI Generated Architecture Summary (Fallback)\n\n").replace("## Core Services\n", "### Core Services\n\n")

    readme_content = "# PedagogyX - Autonomous Repository\n\n"

    readme_content += "![CI Status](https://img.shields.io/github/actions/workflow/status/owner/repo/test.yml?branch=main&label=CI)\n"
    readme_content += "![Auto-Docs](https://img.shields.io/badge/Docs-Auto--Generated-blue)\n\n"

    readme_content += "## Project Overview\n\n"
    readme_content += "This repository is continuously analyzed, documented, and visualized automatically.\n\n"

    readme_content += "## Technology Stack\n\n"
    for fw in graph.get("frameworks", []):
        readme_content += f"- {fw}\n"
    readme_content += "\n"

    if ai_summary_content:
        # Avoid multiple blank lines
        ai_summary_content = ai_summary_content.replace("\n\n\n", "\n\n")
        readme_content += ai_summary_content.strip() + "\n\n"

    readme_content += "## Repository Structure\n\n"
    for svc in graph.get("services", []):
        readme_content += f"- **[{svc['name']}]({svc['path']})**\n"
    readme_content += "\n"

    if diagrams_content:
        diagrams_content = diagrams_content.replace("\n\n\n", "\n\n")
        readme_content += diagrams_content.strip() + "\n\n"

    readme_content += "## Setup Instructions\n\n"
    readme_content += "1. Install dependencies via `pip install -r services/api/requirements.txt` or Node/NPM.\n"
    readme_content += "2. Run locally via Docker: `docker compose -f infra/compose.dev.yaml up --build`\n\n"

    readme_content += "## Environment Variables\n\n"
    readme_content += "The following environment variables are detected in the codebase:\n\n"
    if graph.get("env_vars"):
        for env in graph.get("env_vars"):
            readme_content += f"- `{env}`\n"
        readme_content += "\n"
    else:
        readme_content += "None detected.\n\n"

    readme_content += "## Contribution Guide\n\n"
    readme_content += "Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.\n"

    output_path = os.path.join(repo_root, "README.md")
    with open(output_path, "w") as f:
        f.write(readme_content)

    print(f"Generated dynamic README.md at {output_path}")

if __name__ == "__main__":
    main()
