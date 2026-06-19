import os
import glob

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    new_lines = []
    override_lines = []

    for line in lines:
        if line == "from app.auth import verify_api_key":
            pass # We will move it to the top
        elif line == "app.dependency_overrides[verify_api_key] = lambda: 'mock'":
            override_lines.append(line)
        else:
            new_lines.append(line)

    if override_lines:
        final_lines = []
        for line in new_lines:
            if line.startswith("from fastapi.testclient import TestClient"):
                final_lines.append(line)
                final_lines.append("from app.auth import verify_api_key")
            elif line.startswith("client = TestClient(app)"):
                final_lines.append(line)
                final_lines.append(override_lines[0])
            else:
                final_lines.append(line)
        with open(filepath, 'w') as f:
            f.write('\n'.join(final_lines))

for filepath in glob.glob("services/api/tests/**/*.py", recursive=True):
    fix_file(filepath)

# Fix syntax error in worker/asr_main.py
with open("services/worker-asr/worker/asr_main.py", 'r') as f:
    content = f.read()
content = content.replace("from worker.processor  # type: ignore import process_job", "from worker.processor import process_job  # type: ignore")
with open("services/worker-asr/worker/asr_main.py", 'w') as f:
    f.write(content)
