import json
import os

def load_graph(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def generate_mermaid_architecture(graph):
    mermaid = "```mermaid\ngraph TD\n"

    # Add services
    mermaid += "    subgraph Services\n"
    for service in graph.get("services", []):
        name = service["name"]
        clean_name = name.replace("-", "_")
        path = service["path"]
        # Make nodes clickable in GitHub Markdown
        mermaid += f"        {clean_name}[\"{name}\"]\n"
        mermaid += f"        click {clean_name} href \"{path}\" \"Go to {name} source\"\n"
    mermaid += "    end\n\n"

    # Add frameworks
    mermaid += "    subgraph Frameworks\n"
    for fw in graph.get("frameworks", []):
        clean_fw = fw.replace(".", "_").replace(" ", "_")
        mermaid += f"        {clean_fw}({fw})\n"
    mermaid += "    end\n\n"

    mermaid += "```\n"
    return mermaid

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    graph_path = os.path.join(repo_root, "knowledge_graph.json")

    if not os.path.exists(graph_path):
        print("Knowledge graph not found. Run repo_analyzer.py first.")
        return

    graph = load_graph(graph_path)

    diagrams_content = "# Architecture Diagrams\n\n"
    diagrams_content += "## Services & Frameworks\n\n"
    diagrams_content += generate_mermaid_architecture(graph)

    docs_dir = os.path.join(repo_root, "docs")
    os.makedirs(docs_dir, exist_ok=True)

    output_path = os.path.join(docs_dir, "architecture-diagrams.md")
    with open(output_path, "w") as f:
        f.write(diagrams_content)

    print(f"Generated diagrams at {output_path}")

if __name__ == "__main__":
    main()
