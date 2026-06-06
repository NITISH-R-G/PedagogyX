import re

with open('.github/workflows/codeql.yml', 'r') as f:
    content = f.read()

# Replace the run block for manual build steps
run_block = """      run: |
        if [ "${{ matrix.language }}" = "java-kotlin" ]; then
          cd clients/android-capture-dat
          chmod +x gradlew
          ./gradlew build -x test
        fi"""

content = re.sub(r'      run: \|\n        echo \'If you are using a "manual" build mode for one or more of the\' \\\n          \'languages you are analyzing, replace this with the commands to build\' \\\n          \'your code, for example:\'\n        echo \'  make bootstrap\'\n        echo \'  make release\'\n        exit 1', run_block, content)

with open('.github/workflows/codeql.yml', 'w') as f:
    f.write(content)
