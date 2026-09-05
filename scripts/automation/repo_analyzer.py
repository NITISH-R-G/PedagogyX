import os
import json
import re

def get_frameworks(repo_root):
    frameworks = []

    # Check for FastApi
    if os.path.exists(os.path.join(repo_root, "services/api/requirements.txt")):
        try:
            with open(os.path.join(repo_root, "services/api/requirements.txt"), "r") as f:
                content = f.read()
                if "fastapi" in content.lower():
                    frameworks.append("FastAPI")
        except Exception:
            pass

    # Check for React / Node
    if os.path.exists(os.path.join(repo_root, "services/web/package.json")):
        try:
            with open(os.path.join(repo_root, "services/web/package.json"), "r") as f:
                content = f.read()
                if "react" in content.lower():
                    frameworks.append("React")
                if "next" in content.lower():
                    frameworks.append("Next.js")
        except Exception:
            pass

    return frameworks

def get_services(repo_root):
    services_dir = os.path.join(repo_root, "services")
    services = []
    if os.path.exists(services_dir) and os.path.isdir(services_dir):
        for entry in os.listdir(services_dir):
            if os.path.isdir(os.path.join(services_dir, entry)):
                services.append({
                    "name": entry,
                    "path": f"services/{entry}"
                })
    return services

def extract_python_imports(filepath):
    imports = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("import ") or line.startswith("from "):
                    parts = line.split()
                    if len(parts) > 1:
                        imports.append(parts[1].split('.')[0])
    except Exception:
        pass
    return list(set(imports))

def build_knowledge_graph(repo_root):
    graph = {
        "frameworks": get_frameworks(repo_root),
        "services": get_services(repo_root),
        "modules": [],
        "dependencies": {},
        "env_vars": set(),
    }

    # Walk repo to find Python files and extract basic deps
    for root, _, files in os.walk(repo_root):
        if ".git" in root or ".venv" in root or "__pycache__" in root or "node_modules" in root:
            continue

        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, repo_root)
                imports = extract_python_imports(filepath)
                graph["modules"].append(rel_path)
                graph["dependencies"][rel_path] = imports

                # Check for env vars usage in Python (os.environ, os.getenv)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        env_matches = re.findall(r'os\.environ\[[\'"]([A-Z0-9_]+)[\'"]\]', content)
                        env_matches += re.findall(r'os\.getenv\([\'"]([A-Z0-9_]+)[\'"]\)', content)
                        for match in env_matches:
                            graph["env_vars"].add(match)
                except Exception:
                    pass

            elif file == "docker-compose.yml" or file.endswith(".yaml"):
                # Try to extract env vars from compose files
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        content = f.read()
                        env_matches = re.findall(r'- ([A-Z0-9_]+)=', content)
                        for match in env_matches:
                            graph["env_vars"].add(match)
                except Exception:
                    pass

    graph["env_vars"] = list(graph["env_vars"])

    return graph

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    graph = build_knowledge_graph(repo_root)

    output_path = os.path.join(repo_root, "knowledge_graph.json")
    with open(output_path, "w") as f:
        json.dump(graph, f, indent=2)
    print(f"Generated knowledge graph at {output_path}")

if __name__ == "__main__":
    main()
