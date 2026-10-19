# CodeRescue AI - VS Code Extension

Lightweight VS Code extension providing **line-by-line attribution heatmaps** and **security linting** for AI-generated Python code.

## 🌟 Features

- **Granular Attribution Heatmap**: Highlights lines with high probability of unreviewed AI-generated boilerplate in purple/amber.
- **AI Security & Hallucination Linter**: Identifies Command Injections (`shell=True`), SQL Injections, hardcoded secrets, and hallucinated APIs directly in the editor.
- **Zero Cloud Leakage**: Uses your local CodeRescue AI backend (`http://localhost:5000`) for 100% private AST analysis.

## 🚀 How to Install & Test

1. Open this folder `codesource-1/coderescue-ai/vscode-extension` in VS Code.
2. Press `F5` to open an Extension Development Host window.
3. Open any Python file (e.g. `test.py`).
4. CodeRescue AI automatically underlines security flaws and highlights AI boilerplate in real-time!
