import os
import glob

def add_dependency_override(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    if "dependency_overrides" in content:
        return

    if "from app.main import app" not in content:
        return

    lines = content.split('\n')
    new_lines = []
    override_added = False

    for line in lines:
        new_lines.append(line)
        if line.startswith("client = TestClient(app)") and not override_added:
            new_lines.append("from app.auth import verify_api_key")
            new_lines.append("app.dependency_overrides[verify_api_key] = lambda: 'mock'")
            override_added = True

    with open(filepath, 'w') as f:
        f.write('\n'.join(new_lines))

for filepath in glob.glob("services/api/tests/**/*.py", recursive=True):
    add_dependency_override(filepath)
