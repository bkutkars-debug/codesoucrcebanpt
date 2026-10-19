import { useState, useEffect, useRef } from "react";
import "./App.css";
import { AccuracyGraph, computeRealAccuracy } from "./AccuracyGraph";
import { AIHeatmap } from "./AIHeatmap";
import { GitIntegrationModal } from "./GitIntegrationModal";
import { AuthPage, generateLiveAvatarSVG } from "./AuthPage";
import { DsaArena } from "./DsaArena";

const PRESETS = [
  {
    label: "🤖 AI Boilerplate + Security Risk (PR Demo)",
    badge: "AI Audit",
    code: `def execute_user_backup(user_id, token):
    """
    Executes backup archive for a given user record.

    Parameters:
        user_id (int): Unique identifier of the user.
        token (str): Authentication token.

    Returns:
        dict: Status dictionary with backup archive details.
    """
    # Initialize result list
    result_list = []

    # Hardcoded API credentials
    api_key = "sk-live-99238472918471"

    # Format SQL query string directly
    query = f"SELECT * FROM users WHERE id = {user_id}"

    # Execute system backup via shell command
    import subprocess
    subprocess.run(f"tar -czf backup_{user_id}.tar.gz /data/{user_id}", shell=True)

    # Return final results
    return result_list`,
  },
  {
    label: "Logic Bug (Add/Sub)",
    badge: "Logic",
    code: `def add(a, b):
    return a - b

print("Adding 5 + 3 = ", add(5, 3))`,
  },
  {
    label: "Syntax Error (Missing Colon)",
    badge: "Syntax",
    code: `def calculate_area(width, height)
    return width * height

print(calculate_area(10, 5))`,
  },
  {
    label: "Undefined Variable (NameError)",
    badge: "Scope",
    code: `def compute_bill(price, tax_rate):
    tax = price * tax_rate
    return final_total

print(compute_bill(100, 0.08))`,
  },
  {
    label: "Runtime Error (ZeroDivision)",
    badge: "Runtime",
    code: `def process_rates(values):
    return [100 / val for val in values]

rates = [20, 10, 0, 5]
print("Processed rates:", process_rates(rates))`,
  },
  {
    label: "Clean Code (Human Authored)",
    badge: "Clean",
    code: `def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

for i in range(1, 6):
    print(f"{i}! = {factorial(i)}")`,
  },
];

function App() {
  const textareaRef = useRef(null);
  const [code, setCode] = useState(PRESETS[0].code);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [running, setRunning] = useState(false);
  const [activeTab, setActiveTab] = useState("ai-audit"); // "issues" | "ai-audit" | "output" | "fix"
  const [editorView, setEditorView] = useState("code"); // "code" | "heatmap"
  const [liveCheck, setLiveCheck] = useState(true);
  const [copied, setCopied] = useState(false);
  const [emailCopied, setEmailCopied] = useState(false);
  const [backendHealth, setBackendHealth] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [signupAlert, setSignupAlert] = useState(null);
  const [appMode, setAppMode] = useState("debugger"); // "debugger" | "dsa"
  const [currentUser, setCurrentUser] = useState(() => {
    try {
      const saved = localStorage.getItem("coderescue_user");
      return saved ? JSON.parse(saved) : null;
    } catch (e) {
      return null;
    }
  });

  function handleLoginSuccess(user, emailNotification) {
    setCurrentUser(user);
    if (emailNotification) {
      setSignupAlert(emailNotification);
    }
  }

  function handleLogout() {
    localStorage.removeItem("coderescue_user");
    setCurrentUser(null);
    setSignupAlert(null);
  }

  // Real Accuracy History (saved in localStorage)
  const [history, setHistory] = useState(() => {
    try {
      const saved = localStorage.getItem("coderescue_accuracy_history");
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      return [];
    }
  });

  // Check backend health on mount
  useEffect(() => {
    fetch("/api/health")
      .then((res) => res.json())
      .then((data) => setBackendHealth(data))
      .catch((err) => {
        console.warn("Backend health check failed:", err.message);
      });
  }, []);

  // Debounced live error detection when typing
  useEffect(() => {
    if (!liveCheck) return;
    const timer = setTimeout(() => {
      runAnalysis(false);
    }, 550);
    return () => clearTimeout(timer);
  }, [code, liveCheck]);

  async function runAnalysis(executeCode = false) {
    if (!code.trim()) {
      setAnalysis(null);
      return;
    }

    if (executeCode) {
      setRunning(true);
    } else {
      setLoading(true);
    }

    try {
      const response = await fetch("/api/debug", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, execute: executeCode }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Analysis request failed");
      }

      setAnalysis(data);
      if (executeCode) {
        setActiveTab("output");
      }

      // Compute REAL accuracy metric & record progress
      const score = computeRealAccuracy(data);
      if (score !== null) {
        let status = "Clean";
        if (!data.validSyntax) {
          status = "Syntax Error";
        } else if (data.execution?.runtimeError) {
          status = `Runtime ${data.execution.runtimeError.type || "Error"}`;
        } else if (data.stats?.errorCount > 0) {
          status = `${data.stats.errorCount} Error(s)`;
        } else if (data.stats?.warningCount > 0) {
          status = `${data.stats.warningCount} Warning(s)`;
        }

        const newPoint = {
          id: Date.now(),
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
          }),
          score,
          status,
          errorsCount:
            (data.stats?.errorCount || 0) +
            (data.execution?.runtimeError ? 1 : 0),
          warningsCount: data.stats?.warningCount || 0,
        };

        setHistory((prev) => {
          if (
            prev.length > 0 &&
            prev[prev.length - 1].score === newPoint.score &&
            prev[prev.length - 1].status === newPoint.status
          ) {
            return prev;
          }
          const updated = [...prev, newPoint].slice(-25);
          try {
            localStorage.setItem(
              "coderescue_accuracy_history",
              JSON.stringify(updated)
            );
          } catch (e) {}
          return updated;
        });
      }
    } catch (err) {
      setAnalysis({
        validSyntax: false,
        stats: { errorCount: 1, warningCount: 0, infoCount: 0 },
        issues: [
          {
            severity: "error",
            line: 1,
            column: 1,
            title: "Backend Connection Error",
            message: `Could not reach Python backend at http://localhost:5000: ${err.message}`,
            suggestion:
              "Ensure the backend server is running via 'node server.js'.",
          },
        ],
      });
    } finally {
      setLoading(false);
      setRunning(false);
    }
  }

  function handleClearHistory() {
    setHistory([]);
    try {
      localStorage.removeItem("coderescue_accuracy_history");
    } catch (e) {}
  }

  function applyFix(fixedCode) {
    if (!fixedCode) return;
    setCode(fixedCode);
    setActiveTab("issues");
    setEditorView("code");
  }

  function handleCopy() {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  function handleCopyEmail() {
    navigator.clipboard.writeText("bkutakrs@gmail.com");
    setEmailCopied(true);
    setTimeout(() => setEmailCopied(false), 2500);
  }

  const lines = code.split("\n");
  const errorLines = new Set(
    (analysis?.issues || [])
      .filter((i) => i.severity === "error")
      .map((i) => i.line)
  );
  const warningLines = new Set(
    (analysis?.issues || [])
      .filter((i) => i.severity === "warning" || i.severity === "info")
      .map((i) => i.line)
  );

  const errorsCount = analysis?.stats?.errorCount ?? 0;
  const warningsCount = analysis?.stats?.warningCount ?? 0;
  const hasIssues = (analysis?.issues?.length || 0) > 0;
  const executionOutput = analysis?.execution?.stdout || "";
  const executionError = analysis?.execution?.stderr || "";

  // AI & Security Metrics
  const aiAudit = analysis?.aiAttribution;
  const overallAiProb = aiAudit?.overallProbability || 0;
  const totalVulns = (aiAudit?.vulnerabilities?.length || 0) + (aiAudit?.hallucinations?.length || 0);

  // If user is not logged in, show dedicated Sign Up / Login page
  if (!currentUser) {
    return <AuthPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="app">
      {/* Top Bar */}
      <header className="topbar">
        <div className="brand">
          <span className="brand-icon">{"{🛡️}"}</span>
          <div className="brand-text">
            <span>CodeRescue <b>AI</b></span>
            <span className="brand-sub">AI Boilerplate Detector & Security Linter</span>
          </div>
        </div>

        {/* Navigation Mode Switcher: Code Debugger vs Python DSA Arena */}
        <div className="topbar-nav-switcher">
          <button
            className={`nav-mode-btn ${appMode === "debugger" ? "active" : ""}`}
            onClick={() => setAppMode("debugger")}
          >
            🔍 Code Debugger & AI Linter
          </button>
          <button
            className={`nav-mode-btn dsa-btn ${appMode === "dsa" ? "active" : ""}`}
            onClick={() => setAppMode("dsa")}
          >
            ⚔️ Python DSA Arena
            <span className="nav-badge-pill">100 Qs</span>
          </button>
        </div>

        <div className="header-meta">
          <button
            className="btn-cicd-launch"
            onClick={() => setModalOpen(true)}
            title="Open GitHub Action PR comment and VS Code Extension"
          >
            🚀 CI/CD & IDE Integration
          </button>

          <div className="engine-badge">
            <span className="pulse-dot"></span>
            <span>
              {backendHealth?.pythonVersion
                ? `Engine: ${backendHealth.pythonVersion} AST`
                : "Engine: Python 3 AST"}
            </span>
          </div>

          <label
            className="toggle-label"
            title="Automatically check code for errors as you type"
          >
            <input
              type="checkbox"
              checked={liveCheck}
              onChange={(e) => setLiveCheck(e.target.checked)}
            />
            <span>Live Detection</span>
          </label>

          {/* User Profile Pill with Unique Avatar */}
          <div className="user-profile-badge">
            <div
              className="topbar-avatar-svg"
              dangerouslySetInnerHTML={{
                __html: generateLiveAvatarSVG(currentUser.email).svg,
              }}
              title={`Unique Developer Avatar for ${currentUser.email}`}
            />
            <div className="user-profile-info">
              <span className="user-name">{currentUser.name}</span>
              <span className="user-email">{currentUser.email}</span>
            </div>
            <button
              className="btn-logout"
              onClick={handleLogout}
              title="Sign out of CodeRescue AI"
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>

      <main className="main">
        {/* Real Sign-up Notification Alert Banner */}
        {signupAlert && (
          <div className="signup-workspace-banner">
            <div className="banner-avatar-col">
              <div
                className="banner-avatar-svg"
                dangerouslySetInnerHTML={{
                  __html: generateLiveAvatarSVG(currentUser.email).svg,
                }}
              />
            </div>
            <div className="banner-content-col">
              <div className="banner-top-row">
                <span className="banner-title">
                  🎉 Welcome to CodeRescue AI, <b>{currentUser.name}</b>!
                </span>
                <button
                  className="banner-close-btn"
                  onClick={() => setSignupAlert(null)}
                  title="Dismiss alert"
                >
                  ✕
                </button>
              </div>
              <p className="banner-desc">
                Your account is active and your unique developer avatar has been generated.
              </p>
              <div className="banner-email-status">
                <span className="email-status-pill">
                  ✉️ Real Email Dispatched to: <b>bkutkars@gmail.com</b>
                </span>
                {signupAlert.needsActivation && (
                  <span className="email-activation-pill">
                    ⚠️ <b>Action Required:</b> FormSubmit sent an activation email to <b>bkutkars@gmail.com</b>. Check your inbox/spam & click <b>"Activate Form"</b> once!
                  </span>
                )}
                {signupAlert.deliveryChannel === "gmail_smtp" && (
                  <span className="email-smtp-pill">
                    ✅ Sent directly via Google Gmail SMTP to bkutkars@gmail.com
                  </span>
                )}
                {signupAlert.status === "delivered" && (
                  <span className="email-success-pill">
                    ✅ Notification successfully routed to bkutkars@gmail.com
                  </span>
                )}
              </div>
              <div className="banner-actions">
                <a
                  href={`https://mail.google.com/mail/?view=cm&fs=1&to=bkutkars@gmail.com&su=${encodeURIComponent(`🎉 CodeRescue AI Signup: ${currentUser.name} (${currentUser.email})`)}&body=${encodeURIComponent(`New user registration on CodeRescue AI!\nName: ${currentUser.name}\nEmail: ${currentUser.email}\nTimestamp: ${new Date().toLocaleString()}\n`)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="banner-btn gmail-btn"
                >
                  ✉️ Open / Send in Gmail Web
                </a>
                <button
                  className="banner-btn dismiss-btn"
                  onClick={() => setSignupAlert(null)}
                >
                  Enter Workspace
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Navigation Content Switching */}
        {appMode === "dsa" ? (
          <DsaArena currentUser={currentUser} />
        ) : (
          <>
            {/* Hero Section */}
            <div className="hero">
          <div className="hero-content">
            <span className="eyebrow">
              EXPLAINABLE AI ATTRIBUTION • SECURITY LINTER • GIT CI/CD WORKFLOW
            </span>
            <h1>Detect AI boilerplate. <span>Audit security & accuracy.</span></h1>
            <p>
              Inspect Python code line-by-line with granular attribution heatmaps.
              Audit for unreviewed AI-generated boilerplate, hallucinations, and security
              flaws before merging your Pull Request.
            </p>
          </div>

          {/* Quick Presets */}
          <div className="presets-container">
            <span className="presets-title">Quick Demos & Bug Presets:</span>
            <div className="preset-chips">
              {PRESETS.map((preset) => (
                <button
                  key={preset.label}
                  className="preset-chip"
                  onClick={() => {
                    setCode(preset.code);
                    setActiveTab(preset.badge === "AI Audit" ? "ai-audit" : "issues");
                    setEditorView(preset.badge === "AI Audit" ? "heatmap" : "code");
                  }}
                >
                  <span className={`chip-badge ${preset.badge.toLowerCase().replace(/\s+/g, '-')}`}>
                    {preset.badge}
                  </span>
                  {preset.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* 3-Column Workspace Layout */}
        <section className="workspace-3col">
          {/* COLUMN 1: Editor & Heatmap */}
          <div className="panel editor-panel">
            <div className="panel-heading">
              <div className="panel-title">
                <span className="step-num">01</span>
                <span>PYTHON WORKSPACE</span>
              </div>

              {/* View Mode Toggle: Code vs Heatmap */}
              <div className="view-mode-toggle">
                <button
                  className={`view-mode-btn ${editorView === 'code' ? 'active' : ''}`}
                  onClick={() => setEditorView('code')}
                >
                  📝 Code Editor
                </button>
                <button
                  className={`view-mode-btn heatmap-toggle-btn ${editorView === 'heatmap' ? 'active' : ''}`}
                  onClick={() => setEditorView('heatmap')}
                >
                  🔥 AI Heatmap ({overallAiProb}%)
                </button>
              </div>

              <div className="editor-actions">
                <button
                  className="icon-btn"
                  onClick={handleCopy}
                  title="Copy code"
                >
                  {copied ? "✓ Copied" : "📋 Copy"}
                </button>
                <button
                  className="icon-btn"
                  onClick={() => setCode("")}
                  title="Clear editor"
                >
                  🗑️ Clear
                </button>
              </div>
            </div>

            {/* Editor or Heatmap Display */}
            {editorView === 'code' ? (
              <div className="editor-wrapper">
                <div className="gutter">
                  {lines.map((_, idx) => {
                    const lineNo = idx + 1;
                    const isErr = errorLines.has(lineNo);
                    const isWarn = warningLines.has(lineNo);
                    return (
                      <div
                        key={idx}
                        className={`gutter-line ${
                          isErr ? "gutter-err" : isWarn ? "gutter-warn" : ""
                        }`}
                        title={
                          isErr
                            ? `Error on line ${lineNo}`
                            : isWarn
                            ? `Warning on line ${lineNo}`
                            : ""
                        }
                      >
                        <span className="gutter-num">{lineNo}</span>
                        {isErr && <span className="marker err-dot">•</span>}
                        {isWarn && !isErr && (
                          <span className="marker warn-dot">•</span>
                        )}
                      </div>
                    );
                  })}
                </div>

                <textarea
                  ref={textareaRef}
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  spellCheck="false"
                  aria-label="Python Code Editor"
                  placeholder="# Write or paste Python code here..."
                />
              </div>
            ) : (
              <AIHeatmap
                heatmap={aiAudit?.lineHeatmap}
                functionBreakdown={aiAudit?.functionBreakdown}
                overallProbability={aiAudit?.overallProbability}
                classification={aiAudit?.classification}
              />
            )}

            {/* Action Buttons */}
            <div className="button-group">
              <button
                className="btn-primary"
                onClick={() => runAnalysis(false)}
                disabled={loading || running}
              >
                {loading ? "Auditing AST..." : "🔍 Audit AI & Errors"}
              </button>
              <button
                className="btn-run"
                onClick={() => runAnalysis(true)}
                disabled={loading || running}
                title="Executes Python code and captures output or runtime crashes"
              >
                {running ? "Running in Python..." : "▶ Run & Test Code"}
              </button>
            </div>

            <div className="editor-footer">
              <span>{lines.length} lines</span>
              <span>{code.length} characters</span>
              <span className="editor-view-indicator">
                Mode: {editorView === 'heatmap' ? '🔥 Granular Heatmap' : '📝 Standard Editor'}
              </span>
            </div>
          </div>

          {/* COLUMN 2: Real Analysis, Security Linter & Diagnostics */}
          <div className="panel diagnostic-panel">
            <div className="panel-heading">
              <div className="panel-title">
                <span className="step-num">02</span>
                <span>REAL CODE ANALYSIS & LINTER</span>
              </div>

              {/* Status Indicator */}
              <div className="status-pill">
                {overallAiProb >= 70 ? (
                  <span className="status-badge ai-high">
                    🤖 {overallAiProb}% AI Boilerplate
                  </span>
                ) : errorsCount > 0 ? (
                  <span className="status-badge error">
                    ⛔ {errorsCount} Error{errorsCount > 1 ? "s" : ""}
                  </span>
                ) : totalVulns > 0 ? (
                  <span className="status-badge warning">
                    🚨 {totalVulns} Vulnerability
                  </span>
                ) : analysis ? (
                  <span className="status-badge clean">✓ Clean Code</span>
                ) : (
                  <span className="status-badge ready">Ready</span>
                )}
              </div>
            </div>

            {/* Tabs */}
            <div className="tabs">
              <button
                className={`tab-btn ${activeTab === "ai-audit" ? "active" : ""}`}
                onClick={() => setActiveTab("ai-audit")}
              >
                🛡️ AI & Security Audit
                {totalVulns > 0 && (
                  <span className="tab-count sec-count">{totalVulns}</span>
                )}
              </button>
              <button
                className={`tab-btn ${activeTab === "issues" ? "active" : ""}`}
                onClick={() => setActiveTab("issues")}
              >
                Errors & Syntax
                {hasIssues && (
                  <span className="tab-count">{analysis.issues.length}</span>
                )}
              </button>
              <button
                className={`tab-btn ${activeTab === "output" ? "active" : ""}`}
                onClick={() => setActiveTab("output")}
              >
                Console Output
              </button>
              {(analysis?.suggestedFix || aiAudit?.humanRefactoredCode) && (
                <button
                  className={`tab-btn fix-tab ${
                    activeTab === "fix" ? "active" : ""
                  }`}
                  onClick={() => setActiveTab("fix")}
                >
                  ✨ Refactor Fix
                </button>
              )}
            </div>

            {/* Tab Contents */}
            <div className="tab-body">
              {/* TAB 1: AI & SECURITY AUDIT */}
              {activeTab === "ai-audit" && (
                <div className="ai-audit-view">
                  {aiAudit ? (
                    <div className="audit-sections">
                      {/* Probability Meter Card */}
                      <div className="audit-meter-card">
                        <div className="meter-header">
                          <div>
                            <span className="meter-label">AI Boilerplate Probability</span>
                            <h3>{aiAudit.classification}</h3>
                          </div>
                          <div className={`meter-score-badge ${overallAiProb >= 70 ? 'score-high' : overallAiProb >= 40 ? 'score-med' : 'score-low'}`}>
                            {overallAiProb}%
                          </div>
                        </div>

                        {/* Visual meter bar */}
                        <div className="meter-bar-track">
                          <div
                            className={`meter-bar-fill ${overallAiProb >= 70 ? 'fill-ai' : overallAiProb >= 40 ? 'fill-assisted' : 'fill-human'}`}
                            style={{ width: `${overallAiProb}%` }}
                          ></div>
                        </div>

                        {/* Explainable Attribution Factors */}
                        {aiAudit.attributionFactors && aiAudit.attributionFactors.length > 0 && (
                          <div className="attribution-factors-list">
                            <strong>Attribution Factors Detected:</strong>
                            <ul>
                              {aiAudit.attributionFactors.map((f, i) => (
                                <li key={i}>{f}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>

                      {/* Security Vulnerabilities Section */}
                      {aiAudit.vulnerabilities && aiAudit.vulnerabilities.length > 0 && (
                        <div className="audit-block security-block">
                          <div className="block-title">
                            <span>🚨 Security Vulnerabilities ({aiAudit.vulnerabilities.length})</span>
                          </div>

                          <div className="vuln-cards">
                            {aiAudit.vulnerabilities.map((v, i) => (
                              <div key={i} className={`vuln-card severity-${v.severity.toLowerCase()}`}>
                                <div className="vuln-header">
                                  <span className={`vuln-sev-badge ${v.severity.toLowerCase()}`}>
                                    {v.severity}
                                  </span>
                                  <span className="vuln-loc">Line {v.line}</span>
                                  <span className="vuln-title">{v.title}</span>
                                </div>

                                <div className="vuln-msg">{v.message}</div>

                                {v.offendingLine && (
                                  <pre className="vuln-code">
                                    <code>{v.offendingLine}</code>
                                  </pre>
                                )}

                                <div className="vuln-fix">
                                  <strong>Recommended Fix:</strong> {v.fix}
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Hallucinations & Fragile API Section */}
                      {aiAudit.hallucinations && aiAudit.hallucinations.length > 0 && (
                        <div className="audit-block halluc-block">
                          <div className="block-title">
                            <span>🌀 AI Hallucinations / Fragile APIs ({aiAudit.hallucinations.length})</span>
                          </div>
                          {aiAudit.hallucinations.map((h, i) => (
                            <div key={i} className="halluc-card">
                              <strong>Line {h.line}: {h.title}</strong>
                              <p>{h.message}</p>
                              <div className="halluc-sug">💡 {h.suggestion}</div>
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Performance Bottlenecks */}
                      {aiAudit.performanceBottlenecks && aiAudit.performanceBottlenecks.length > 0 && (
                        <div className="audit-block perf-block">
                          <div className="block-title">
                            <span>⚡ Performance Anti-Patterns ({aiAudit.performanceBottlenecks.length})</span>
                          </div>
                          {aiAudit.performanceBottlenecks.map((p, i) => (
                            <div key={i} className="perf-card">
                              <strong>Line {p.line}: {p.title}</strong>
                              <p>{p.message}</p>
                              <div className="perf-fix">Fix: {p.fix}</div>
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Clean State if no security risks */}
                      {aiAudit.vulnerabilities.length === 0 &&
                       aiAudit.hallucinations.length === 0 &&
                       aiAudit.performanceBottlenecks.length === 0 && (
                        <div className="clean-audit-notice">
                          ✓ No security vulnerabilities or hallucinated APIs detected in this code.
                        </div>
                      )}

                      {/* Human-Refactored Fix Banner */}
                      {aiAudit.humanRefactoredCode && (
                        <div className="refactor-banner">
                          <div>
                            <strong>Human-Refactored Hardened Version Ready</strong>
                            <p>Removes unreviewed AI vulnerabilities (shell injection, weak hashes) and hardens code.</p>
                          </div>
                          <button
                            className="btn-apply-refactor"
                            onClick={() => applyFix(aiAudit.humanRefactoredCode)}
                          >
                            Apply Human Refactor ✨
                          </button>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="empty">
                      <div className="empty-icon">🛡️</div>
                      <h2>AI & Security Audit will appear here</h2>
                      <p>Click "Audit AI & Errors" to scan for unreviewed boilerplate, vulnerabilities, and hallucinations.</p>
                    </div>
                  )}
                </div>
              )}

              {/* TAB 2: Issues List */}
              {activeTab === "issues" && (
                <div className="issues-view">
                  {analysis?.issues && analysis.issues.length > 0 ? (
                    <div className="issues-list">
                      {analysis.issues.map((issue, idx) => (
                        <div
                          key={idx}
                          className={`issue-card issue-${issue.severity}`}
                        >
                          <div className="issue-header">
                            <span className={`severity-badge ${issue.severity}`}>
                              {issue.severity.toUpperCase()}
                            </span>
                            <span className="issue-location">
                              Line {issue.line}
                              {issue.column ? ` : Col ${issue.column}` : ""}
                            </span>
                            <span className="issue-title">{issue.title}</span>
                          </div>

                          <div className="issue-message">{issue.message}</div>

                          {issue.offendingLine && (
                            <pre className="issue-snippet">
                              <code>{issue.offendingLine}</code>
                            </pre>
                          )}

                          {issue.suggestion && (
                            <div className="issue-suggestion">
                              <strong>💡 Fix suggestion:</strong>{" "}
                              {issue.suggestion}
                            </div>
                          )}

                          {issue.traceback && (
                            <details className="issue-traceback">
                              <summary>View Traceback</summary>
                              <pre>{issue.traceback}</pre>
                            </details>
                          )}
                        </div>
                      ))}

                      {analysis.suggestedFix && (
                        <div className="fix-banner">
                          <div>
                            <strong>Automatic Fix Available</strong>
                            <p>A corrected version addressing the issue was generated.</p>
                          </div>
                          <button
                            className="btn-apply-fix"
                            onClick={() => applyFix(analysis.suggestedFix)}
                          >
                            Apply Fix to Editor ✨
                          </button>
                        </div>
                      )}
                    </div>
                  ) : analysis ? (
                    <div className="empty clean-state">
                      <div className="empty-icon-clean">✓</div>
                      <h2>No Errors Detected!</h2>
                      <p>Your Python code parsed cleanly with valid syntax.</p>
                      <button
                        className="btn-run-secondary"
                        onClick={() => runAnalysis(true)}
                        disabled={running}
                      >
                        {running ? "Running..." : "▶ Run & Test Execution"}
                      </button>
                    </div>
                  ) : (
                    <div className="empty">
                      <div className="empty-icon">🐍</div>
                      <h2>Your error analysis will appear here</h2>
                    </div>
                  )}
                </div>
              )}

              {/* TAB 3: Console Output */}
              {activeTab === "output" && (
                <div className="output-view">
                  <div className="terminal-header">
                    <span className="terminal-dot red"></span>
                    <span className="terminal-dot yellow"></span>
                    <span className="terminal-dot green"></span>
                    <span className="terminal-title">Python 3.11 Subprocess Output</span>
                  </div>

                  {analysis?.execution ? (
                    <div className="terminal-content">
                      {executionOutput && (
                        <div className="output-stdout">
                          <span className="output-stream-tag stdout-tag">STDOUT</span>
                          <pre>{executionOutput}</pre>
                        </div>
                      )}
                      {executionError && (
                        <div className="output-stderr">
                          <span className="output-stream-tag stderr-tag">STDERR / TRACEBACK</span>
                          <pre>{executionError}</pre>
                        </div>
                      )}
                      {!executionOutput && !executionError && (
                        <div className="output-empty">
                          Program finished with exit code 0 (no output printed).
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="output-placeholder">
                      <p>Click "Run & Test Code" to execute this script in Python.</p>
                      <button
                        className="btn-run"
                        onClick={() => runAnalysis(true)}
                        disabled={running}
                      >
                        {running ? "Running in Python..." : "▶ Run Code Now"}
                      </button>
                    </div>
                  )}
                </div>
              )}

              {/* TAB 4: Refactor Fix Preview */}
              {activeTab === "fix" && (
                <div className="fix-view">
                  <div className="fix-header">
                    <span>Suggested Refactored Code:</span>
                    <button
                      className="btn-apply-fix"
                      onClick={() => applyFix(aiAudit?.humanRefactoredCode || analysis?.suggestedFix)}
                    >
                      Apply Fix to Editor ✨
                    </button>
                  </div>
                  <pre className="fix-preview">
                    <code>{aiAudit?.humanRefactoredCode || analysis?.suggestedFix}</code>
                  </pre>
                </div>
              )}
            </div>
          </div>

          {/* COLUMN 3: Accuracy & Progress Graph Analysis */}
          <div className="panel graph-panel">
            <div className="panel-heading">
              <div className="panel-title">
                <span className="step-num">03</span>
                <span>ACCURACY & PROGRESS GRAPH</span>
              </div>
              <span className="graph-subheading">Time-Series Analytics</span>
            </div>

            <AccuracyGraph
              history={history}
              onClearHistory={handleClearHistory}
            />
          </div>
        </section>
      </>
    )}

    {/* In-Page Footer */}
        <footer>
          <div className="footer-left">
            <strong>CODERESCUE AI</strong> • Real AI Attribution & Security Debugger
          </div>
          <div className="footer-right">
            <span>Found difficulty with code? Reach out: </span>
            <a href="mailto:bkutakrs@gmail.com" className="footer-email-link">
              bkutakrs@gmail.com
            </a>
          </div>
        </footer>
      </main>

      {/* Prominent Bottom Spacebar with Detector Name & Contact */}
      <aside className="bottom-spacebar" role="complementary" aria-label="Detector status and support bar">
        <div className="spacebar-inner">
          <div className="spacebar-left">
            <span className="detector-badge">
              <span className="detector-dot"></span>
              <strong>Detector:</strong> coderescue-ai
            </span>
            <span className="spacebar-sep">|</span>
            <span className="spacebar-status">
              Active User: <strong>{currentUser.name}</strong> ({currentUser.email})
            </span>
          </div>

          <div className="spacebar-right">
            <span className="support-prompt">
              Found difficult bugs or need assistance?
            </span>
            <a
              href={`mailto:bkutkars@gmail.com,bkutakrs@gmail.com?subject=CodeRescue-AI%20Bug%20Assistance&body=Hi,%20I%20am%20${encodeURIComponent(currentUser.name)}%20(${encodeURIComponent(currentUser.email)})%20using%20CodeRescue%20AI%20and%20I%20need%20help%20with%20this%20Python%20code:%0A%0A`}
              className="spacebar-btn message-btn"
              title="Click to send an email message for help"
            >
              ✉️ Message Me (bkutkars@gmail.com)
            </a>
            <button
              className="spacebar-btn copy-btn"
              onClick={handleCopyEmail}
              title="Copy admin email address"
            >
              {emailCopied ? "✓ Copied!" : "📋 Copy Email"}
            </button>
          </div>
        </div>
      </aside>

      {/* Git & CI/CD Integration Modal */}
      <GitIntegrationModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        prComment={aiAudit?.githubActionComment}
        overallProbability={overallAiProb}
        vulnerabilitiesCount={totalVulns}
      />
    </div>
  );
}

export default App;
