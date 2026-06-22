with open('.github/workflows/codeql.yml', 'r') as f:
    lines = f.readlines()

new_lines = []
skip_next = False
for i, line in enumerate(lines):
    if skip_next:
        skip_next = False
        continue
    if "language: actions" in line or "language: java-kotlin" in line or "language: javascript-typescript" in line:
        skip_next = True
        continue
    new_lines.append(line)

with open('.github/workflows/codeql.yml', 'w') as f:
    f.writelines(new_lines)
