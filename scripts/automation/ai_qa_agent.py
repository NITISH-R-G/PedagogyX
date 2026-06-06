import os
import argparse
import json
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

def get_report_content(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return f.read().strip()
    return ""

def generate_qa_summary(reports, api_key=None):
    if OpenAI and api_key:
        client = OpenAI(api_key=api_key)
        prompt = f"Analyze the following code quality and security reports and provide a plain-English summary. Prioritize issues by severity, recommend fixes, and suggest refactoring:\n\n{json.dumps(reports)[:4000]}"
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a senior automated code reviewer and QA agent."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return generate_fallback_summary(reports) + f"\n\n*(Note: LLM API error: {e})*"
    else:
        return generate_fallback_summary(reports)

def generate_fallback_summary(reports):
    summary = "# AI-Powered QA & Security Insights (Fallback Generator)\n\n"
    summary += "## Overview\n"
    summary += "This report summarizes findings from the automated workflows.\n\n"

    summary += "## Findings\n"
    if reports.get("ruff"):
        summary += f"- **Code Quality:** Ruff detected potential issues.\n"
    else:
        summary += f"- **Code Quality:** No critical Ruff issues found.\n"

    if reports.get("vulture"):
         summary += f"- **Dead Code:** Vulture identified potential dead code.\n"

    if reports.get("gitleaks") and "leak" in reports["gitleaks"].lower():
        summary += "- **Security:** Critical secret leak detected! Immediate action required.\n"

    summary += "\n## Prioritized Recommendations\n"
    summary += "1. Review any 'D' or 'F' rated maintainability scores from the Radon report.\n"
    summary += "2. Eliminate dead code flagged by Vulture to reduce technical debt.\n"
    summary += "3. Consolidate logic flagged by duplicate code detection to enhance code reuse.\n"

    return summary

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ci-mode", action="store_true", help="Write report to docs directory")
    args = parser.parse_args()

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    reports = {
        "ruff": get_report_content(os.path.join(repo_root, "ruff_report.txt")),
        "vulture": get_report_content(os.path.join(repo_root, "vulture_report.txt")),
        "radon": get_report_content(os.path.join(repo_root, "radon_mi.txt")),
        "gitleaks": get_report_content(os.path.join(repo_root, "gitleaks_report.txt"))
    }

    api_key = os.environ.get("OPENAI_API_KEY")
    summary = generate_qa_summary(reports, api_key)

    if args.ci_mode:
        docs_dir = os.path.join(repo_root, "docs")
        os.makedirs(docs_dir, exist_ok=True)
        output_path = os.path.join(docs_dir, "QA_REPORT.md")
        with open(output_path, "w") as f:
            f.write(summary)
        print(f"Generated AI QA summary at {output_path}")
    else:
        print(summary)

if __name__ == "__main__":
    main()
