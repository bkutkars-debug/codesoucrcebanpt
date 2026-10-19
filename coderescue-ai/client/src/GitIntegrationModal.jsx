import React, { useState } from 'react';

export function GitIntegrationModal({ isOpen, onClose, prComment, overallProbability = 84, vulnerabilitiesCount = 0 }) {
  const [activeTab, setActiveTab] = useState('pr-comment'); // 'pr-comment' | 'github-yaml' | 'vscode'
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const yamlContent = `name: CodeRescue AI - PR Code Audit

on:
  pull_request:
    paths:
      - '**/*.py'

jobs:
  audit-ai-boilerplate-and-security:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Run CodeRescue AI Audit
        run: python coderescue_cli.py "\${{ github.event.pull_request.head.ref }}"
      - name: Comment on PR
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const comment = fs.readFileSync('audit_output.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });`;

  function handleCopy(text) {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <span className="modal-icon">🚀</span>
            <div>
              <h3>IDE & Git CI/CD Integrations (The Workflow Play)</h3>
              <p>Automate AI boilerplate detection & security auditing across Pull Requests and VS Code</p>
            </div>
          </div>
          <button className="modal-close-btn" onClick={onClose}>✕</button>
        </div>

        {/* Modal Navigation Tabs */}
        <div className="modal-tabs">
          <button
            className={`modal-tab ${activeTab === 'pr-comment' ? 'active' : ''}`}
            onClick={() => setActiveTab('pr-comment')}
          >
            🐙 Simulated GitHub PR Comment
          </button>
          <button
            className={`modal-tab ${activeTab === 'github-yaml' ? 'active' : ''}`}
            onClick={() => setActiveTab('github-yaml')}
          >
            ⚙️ GitHub Action Workflow (.yml)
          </button>
          <button
            className={`modal-tab ${activeTab === 'vscode' ? 'active' : ''}`}
            onClick={() => setActiveTab('vscode')}
          >
            💻 VS Code Extension
          </button>
        </div>

        {/* Tab 1: Simulated GitHub Action PR Comment */}
        {activeTab === 'pr-comment' && (
          <div className="modal-body">
            <div className="github-pr-preview">
              <div className="github-pr-header">
                <div className="bot-avatar">🤖</div>
                <div className="bot-meta">
                  <strong>github-actions <span className="bot-tag">bot</span></strong> commented on Pull Request #42
                  <span className="bot-time">just now</span>
                </div>
              </div>

              <div className="github-comment-body">
                <div className="pr-callout-warning">
                  <div className="callout-icon">⚠️</div>
                  <div className="callout-text">
                    <strong>CodeRescue AI Audit</strong>: Warning: <strong>{overallProbability}% probability of unreviewed AI-generated boilerplate detected in <code>utils.py</code></strong>
                    {vulnerabilitiesCount > 0 && ` (${vulnerabilitiesCount} security risk${vulnerabilitiesCount !== 1 ? 's' : ''} detected)`}.
                  </div>
                </div>

                <div className="comment-pre">
                  <pre>{prComment || "No comment generated yet. Click 'Inspect' or 'Run' on your code first."}</pre>
                </div>
              </div>
            </div>

            <div className="modal-actions">
              <button
                className="btn-primary"
                onClick={() => handleCopy(prComment)}
              >
                {copied ? "✓ Copied PR Comment" : "📋 Copy PR Comment Markdown"}
              </button>
            </div>
          </div>
        )}

        {/* Tab 2: GitHub Action YAML */}
        {activeTab === 'github-yaml' && (
          <div className="modal-body">
            <div className="yaml-guide">
              <p>Add this file to <code>.github/workflows/coderescue-audit.yml</code> in your repository. It will automatically run on every Pull Request and post diagnostic warnings with line-by-line attribution.</p>
            </div>
            <pre className="yaml-code">
              <code>{yamlContent}</code>
            </pre>
            <div className="modal-actions">
              <button
                className="btn-primary"
                onClick={() => handleCopy(yamlContent)}
              >
                {copied ? "✓ Copied YAML Workflow" : "📋 Copy .github/workflows/coderescue-audit.yml"}
              </button>
            </div>
          </div>
        )}

        {/* Tab 3: VS Code Extension */}
        {activeTab === 'vscode' && (
          <div className="modal-body">
            <div className="vscode-guide">
              <h4>Lightweight VS Code Extension Ready in Codebase</h4>
              <p>The VS Code extension package is located inside <code>vscode-extension/</code> in this project directory.</p>
              
              <div className="feature-grid">
                <div className="feature-card">
                  <strong>🔥 Inline Line Heatmaps</strong>
                  <span>Highlights AI-generated boilerplate in purple/amber directly inside the VS Code editor buffer.</span>
                </div>
                <div className="feature-card">
                  <strong>🚨 Real-Time Security Flags</strong>
                  <span>Flags Command Injection (shell=True), hardcoded secrets, and SQL bugs in the VS Code Problems tab.</span>
                </div>
                <div className="feature-card">
                  <strong>🔒 100% Local & Private</strong>
                  <span>Communicates directly with your local CodeRescue engine at <code>http://localhost:5000</code>. No code sent to external servers.</span>
                </div>
              </div>

              <div className="step-list">
                <div className="step-item">
                  <span className="step-circle">1</span>
                  <span>Open <code>coderescue-ai/vscode-extension</code> in VS Code.</span>
                </div>
                <div className="step-item">
                  <span className="step-circle">2</span>
                  <span>Press <code>F5</code> to launch the Extension Development Host window.</span>
                </div>
                <div className="step-item">
                  <span className="step-circle">3</span>
                  <span>Open any Python file to see real-time line heatmaps and security alerts!</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
