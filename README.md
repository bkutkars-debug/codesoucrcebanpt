# 🛡️ CodeRescue AI — Python AST Analyzer & Security Auditor

> **Real Python AST Analysis • Line-by-Line AI Attribution Heatmap • Security & Hallucination Linter • Time-Series Accuracy Graph • GitHub PR & VS Code Workflows**

CodeRescue AI is an end-to-end Python debugging, code quality, and AI audit workspace built with **real static analysis, deterministic AST parsing, and sandbox subprocess execution** — zero fake mock responses or simulated heuristics.

---

## 🌟 Key Features

### 1. 🔍 Real Python AST & Runtime Execution
- **Syntax Diagnosis**: Detects exact line and column numbers for `SyntaxError`, `IndentationError`, and `TabError` with targeted fix suggestions.
- **Scope & NameError Detection**: Flags undefined variables and symbols before runtime.
- **Subprocess Execution Sandbox**: Executes code safely in a Python 3 sandbox to capture `stdout`, `stderr`, and runtime tracebacks (`ZeroDivisionError`, `TypeError`, `IndexError`, etc.).
- **One-Click Auto Fix**: Proposes and applies refactored corrections directly to the editor.

### 2. 🔥 Granular Attribution Heatmap (Explainable AI)
- **Line-by-Line & Function-by-Function**: Scores and visualizes which code blocks are human-crafted vs. unreviewed machine-generated boilerplate.
- **Explainable Attribution Factors**: Evaluates cyclomatic density, generic parameter naming, docstring-to-code ratios, comment density, and structural boilerplate signatures.

### 3. 🚨 AI Code Security & Hallucination Linter
- **Command Injection Scanner**: Flags risky subprocess calls (`subprocess.run(..., shell=True)`).
- **SQL Injection Detection**: Catches unescaped string formatting in SQL queries (`f"SELECT ... WHERE id = {user_id}"`).
- **Hardcoded Secret Detection**: Identifies hardcoded API tokens, keys, and private credentials.
- **AI Hallucination & Fragile API Warnings**: Flags deprecated, fragile, or commonly hallucinated methods with hardened, human-refactored alternatives.

### 4. 📈 Time-Series Accuracy & Progress Analytics
- **Mathematical Accuracy Scoring**: Evaluates code health on a 0–100% scale factoring in syntax errors, warnings, runtime crashes, and security vulnerabilities.
- **Persistent Progress History**: Renders a time-series SVG graph of user code accuracy improvements across test runs.

### 5. 🤖 GitHub Action PR Bot & VS Code Extension
- **GitHub Action Workflow** (`.github/workflows/coderescue-audit.yml`): Automatically inspects Pull Requests and comments line-by-line audits directly on GitHub.
- **VS Code Extension** (`vscode-extension/`): Adds in-editor commands (`CodeRescue: Audit Current Python File`) for local IDE integration.

### 6. 👤 User Authentication & Procedural Avatar Generator
- **Deterministic SVG Avatars**: Generates unique, procedural developer avatars deterministically from user emails.
- **Real Sign-Up Notifications**: Dispatches automated email alerts to admin (`bkutkars@gmail.com`) via FormSubmit API or native Google SMTP.

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** (v18+)
- **Python** (3.9+ installed and on system PATH)

### 1. Launch with One Click (Windows)
Double-click `start.bat` in the repository root.

### 2. Manual Startup

#### Backend Server
```powershell
cd coderescue-ai
npm install
node server.js
```
Runs at: **`http://localhost:5000`**

#### Frontend Development Server
```powershell
cd coderescue-ai/client
npm install
npm run dev
```
Runs at: **`http://localhost:5173`**

---

## ⚙️ Environment Configuration

Create a `.env` file in `coderescue-ai/.env` (reference `.env.example`):

```env
PORT=5000
ADMIN_EMAIL=bkutkars@gmail.com
ADMIN_SECONDARY_EMAIL=bkutakrs@gmail.com

# Optional: Direct Gmail SMTP Dispatch via App Password
# GMAIL_USER=bkutkars@gmail.com
# GMAIL_PASS=xxxx xxxx xxxx xxxx
```

---

## 📁 Repository Structure

```text
codesoucrcebanpt/
├── .github/
│   └── workflows/
│       └── coderescue-audit.yml     # GitHub Actions PR bot
├── coderescue-ai/
│   ├── client/                      # React 18 + Vite frontend
│   │   ├── src/
│   │   │   ├── AccuracyGraph.jsx    # Time-series accuracy graph
│   │   │   ├── AIHeatmap.jsx        # Line-by-line attribution heatmap
│   │   │   ├── AuthPage.jsx         # User auth & procedural avatar preview
│   │   │   ├── GitIntegrationModal.jsx # CI/CD & IDE modal
│   │   │   ├── App.jsx              # 3-column workspace
│   │   │   └── main.jsx             # React entry with ErrorBoundary
│   │   └── package.json
│   ├── data/                        # Persistent user accounts & audit logs
│   ├── vscode-extension/            # Lightweight VS Code Extension
│   ├── ai_security_linter.py        # Python security vulnerability scanner
│   ├── avatar_generator.js          # Procedural SVG avatar engine
│   ├── coderescue_cli.py            # CLI tool for CI/CD & terminal audits
│   ├── email_service.js             # Real email dispatch engine
│   ├── python_analyzer.py           # Real AST parser & execution sandbox
│   ├── server.js                    # Express REST API backend
│   ├── package.json
│   └── .env.example
├── .gitignore
├── README.md
└── start.bat                        # Windows 1-click launcher
```

---

## 📬 Contact & Support

- **Detector Name**: `coderescue-ai`
- **Lead / Admin Contact**: [bkutkars@gmail.com](mailto:bkutkars@gmail.com)
