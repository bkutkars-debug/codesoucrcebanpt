#!/usr/bin/env python3
"""
CodeRescue AI - GitHub Action & CI/CD Runner
Analyzes modified Python files in Pull Requests for unreviewed AI-generated boilerplate,
security vulnerabilities, hallucinations, and performance anti-patterns.
"""

import sys
import os
import json
from ai_security_linter import audit_ai_code

def audit_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    results = audit_ai_code(code)
    filename = os.path.basename(filepath)

    overall_prob = results["overallProbability"]
    vulns = results["vulnerabilities"]
    perf = results["performanceBottlenecks"]
    halluc = results["hallucinations"]

    # Format the Pull Request comment requested by judges:
    # "Warning: 84% probability of unreviewed AI-generated boilerplate detected in utils.py"
    risk_summary = []
    if vulns:
        risk_summary.append(f"{len(vulns)} security risk{'s' if len(vulns) != 1 else ''}")
    if perf:
        risk_summary.append(f"{len(perf)} performance bottleneck{'s' if len(perf) != 1 else ''}")
    if halluc:
        risk_summary.append(f"{len(halluc)} hallucinated API{'s' if len(halluc) != 1 else ''}")

    risk_text = f" ({', '.join(risk_summary)})" if risk_summary else ""

    comment = f"""### ⚠️ CodeRescue AI Audit: Pull Request Review
> **Warning**: **{overall_prob}% probability of unreviewed AI-generated boilerplate detected in `{filename}`**{risk_text}.

#### 🔍 Attribution & Style Breakdown
- **Verdict**: {results['classification']}
- **Key Indicators**: {', '.join(results['attributionFactors'][:3]) if results['attributionFactors'] else 'Standard human structure'}
- **Analyzed Functions**: {len(results['functionBreakdown'])} detected

"""
    if results['functionBreakdown']:
        comment += "| Function | AI Probability | Verdict | Key Factors |\n|---|---|---|---|\n"
        for fn in results['functionBreakdown']:
            comment += f"| `{fn['name']}` | **{fn['aiProbability']}%** | {fn['verdict']} | {', '.join(fn['reasons'])} |\n"
        comment += "\n"

    if vulns:
        comment += "#### 🚨 Security Vulnerabilities Detected\n"
        for v in vulns:
            comment += f"- **[{v['severity']}] {v['title']}** (Line {v['line']}): {v['message']}\n  - *Recommended Fix*: `{v['fix']}`\n"
        comment += "\n"

    if halluc:
        comment += "#### 🌀 AI Hallucinations / Fragile APIs\n"
        for h in halluc:
            comment += f"- **{h['title']}** (Line {h['line']}): {h['message']}\n  - *Suggestion*: {h['suggestion']}\n"
        comment += "\n"

    if perf:
        comment += "#### ⚡ Performance Bottlenecks\n"
        for p in perf:
            comment += f"- **{p['title']}** (Line {p['line']}): {p['message']}\n  - *Recommended Fix*: `{p['fix']}`\n"
        comment += "\n"

    comment += "> *Automated by CodeRescue AI Detector (https://github.com/coderescue-ai)*\n"

    print(comment)

    # If running in GitHub Actions, write to step summary or output
    github_output = os.environ.get("GITHUB_STEP_SUMMARY")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(comment + "\n")

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python coderescue_cli.py <path_to_python_file>")
        sys.exit(1)

    audit_file(sys.argv[1])
