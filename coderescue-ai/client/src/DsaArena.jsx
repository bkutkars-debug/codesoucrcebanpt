import React, { useState, useEffect, useRef } from "react";

export function DsaArena({ currentUser }) {
  const [questions, setQuestions] = useState([]);
  const [loadingList, setLoadingList] = useState(true);
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [loadingQuestion, setLoadingQuestion] = useState(false);
  
  // Filters
  const [difficultyFilter, setDifficultyFilter] = useState("All"); // "All" | "Easy" | "Medium" | "Hard"
  const [categoryFilter, setCategoryFilter] = useState("All");
  const [searchTerm, setSearchTerm] = useState("");
  
  // Editor & Evaluation
  const [code, setCode] = useState("");
  const [evaluating, setEvaluating] = useState(false);
  const [evalType, setEvalType] = useState(""); // "run" | "submit"
  const [evalResult, setEvalResult] = useState(null);
  const [activeTestCaseTab, setActiveTestCaseTab] = useState(0);

  // Statistics
  const [stats, setStats] = useState({
    easy: 50,
    medium: 30,
    hard: 20,
    solvedCount: 0,
    readinessScore: 0
  });
  const [solvedIds, setSolvedIds] = useState(new Set());
  const [leftTab, setLeftTab] = useState("description"); // "description" | "problemList"

  // Load questions on mount & when filters change
  useEffect(() => {
    fetchQuestions();
  }, [difficultyFilter, categoryFilter, searchTerm]);

  async function fetchQuestions() {
    setLoadingList(true);
    try {
      const params = new URLSearchParams();
      if (difficultyFilter !== "All") params.append("difficulty", difficultyFilter);
      if (categoryFilter !== "All") params.append("category", categoryFilter);
      if (searchTerm.trim()) params.append("search", searchTerm.trim());

      const res = await fetch(`/api/dsa/questions?${params.toString()}`);
      const data = await res.json();
      if (res.ok) {
        setQuestions(data.questions || []);
        if (data.stats) setStats(data.stats);
        if (data.solvedIds) setSolvedIds(new Set(data.solvedIds));

        // Select first question if none selected
        if (!selectedQuestion && data.questions && data.questions.length > 0) {
          loadQuestionDetails(data.questions[0].id);
        }
      }
    } catch (err) {
      console.error("Failed to load questions:", err.message);
    } finally {
      setLoadingList(false);
    }
  }

  async function loadQuestionDetails(id) {
    setLoadingQuestion(true);
    setEvalResult(null);
    try {
      const res = await fetch(`/api/dsa/questions/${id}`);
      const data = await res.json();
      if (res.ok) {
        setSelectedQuestion(data);
        setCode(data.starterCode || "");
        setLeftTab("description");
      }
    } catch (err) {
      console.error("Failed to load question details:", err.message);
    } finally {
      setLoadingQuestion(false);
    }
  }

  async function handleRunCode() {
    if (!selectedQuestion || !code.trim()) return;
    setEvaluating(true);
    setEvalType("run");
    setEvalResult(null);
    try {
      const res = await fetch("/api/dsa/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          questionId: selectedQuestion.id,
          code
        })
      });
      const data = await res.json();
      setEvalResult(data);
      setActiveTestCaseTab(0);
    } catch (err) {
      setEvalResult({ verdict: "INTERNAL_ERROR", error: err.message });
    } finally {
      setEvaluating(false);
    }
  }

  async function handleSubmitSolution() {
    if (!selectedQuestion || !code.trim()) return;
    setEvaluating(true);
    setEvalType("submit");
    setEvalResult(null);
    try {
      const res = await fetch("/api/dsa/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          questionId: selectedQuestion.id,
          code,
          userEmail: currentUser?.email || "anonymous"
        })
      });
      const data = await res.json();
      setEvalResult(data);
      setActiveTestCaseTab(0);

      if (data.verdict === "ACCEPTED") {
        setSolvedIds(prev => new Set([...prev, selectedQuestion.id]));
        setStats(prev => ({
          ...prev,
          solvedCount: (data.solvedTotal !== undefined ? data.solvedTotal : prev.solvedCount + 1),
          readinessScore: Math.min(100, Math.round(((data.solvedTotal || prev.solvedCount + 1) / 100) * 100))
        }));
      }
    } catch (err) {
      setEvalResult({ verdict: "INTERNAL_ERROR", error: err.message });
    } finally {
      setEvaluating(false);
    }
  }

  function handleResetCode() {
    if (selectedQuestion) {
      setCode(selectedQuestion.starterCode || "");
      setEvalResult(null);
    }
  }

  const lines = code.split("\n");

  return (
    <div className="dsa-arena">
      {/* Top Placement Preparation Status Bar */}
      <div className="dsa-prep-header">
        <div className="dsa-prep-left">
          <div className="dsa-title-badge">
            <span className="dsa-trophy">🏆</span>
            <div>
              <h3>Python DSA Placement & Internship Arena</h3>
              <p>100 LeetCode & Codeforces Standard Challenges (50 Easy • 30 Medium • 20 Hard)</p>
            </div>
          </div>
        </div>

        {/* Readiness Metric */}
        <div className="dsa-readiness-card">
          <div className="readiness-header">
            <span>Interview Readiness Score</span>
            <strong>{stats.readinessScore}%</strong>
          </div>
          <div className="readiness-progress-track">
            <div
              className="readiness-progress-fill"
              style={{ width: `${stats.readinessScore}%` }}
            ></div>
          </div>
          <div className="readiness-breakdown">
            <span>Solved: <b>{solvedIds.size} / 100</b></span>
            <span>Easy: <b>50</b></span>
            <span>Med: <b>30</b></span>
            <span>Hard: <b>20</b></span>
          </div>
        </div>
      </div>

      {/* Filter and Search Toolbar */}
      <div className="dsa-toolbar">
        {/* Difficulty Selector */}
        <div className="dsa-diff-buttons">
          <button
            className={`diff-btn ${difficultyFilter === 'All' ? 'active' : ''}`}
            onClick={() => setDifficultyFilter('All')}
          >
            All Questions (100)
          </button>
          <button
            className={`diff-btn diff-easy ${difficultyFilter === 'Easy' ? 'active' : ''}`}
            onClick={() => setDifficultyFilter('Easy')}
          >
            🟢 Easy (50)
          </button>
          <button
            className={`diff-btn diff-med ${difficultyFilter === 'Medium' ? 'active' : ''}`}
            onClick={() => setDifficultyFilter('Medium')}
          >
            🟡 Medium (30)
          </button>
          <button
            className={`diff-btn diff-hard ${difficultyFilter === 'Hard' ? 'active' : ''}`}
            onClick={() => setDifficultyFilter('Hard')}
          >
            🔴 Hard (20)
          </button>
        </div>

        {/* Search Input */}
        <div className="dsa-search-wrap">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Search questions or company (Google, Amazon, Meta)..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          {searchTerm && (
            <button className="clear-search" onClick={() => setSearchTerm("")}>✕</button>
          )}
        </div>

        {/* Left Panel View Mode Toggle */}
        <div className="dsa-view-toggle">
          <button
            className={`toggle-tab ${leftTab === 'description' ? 'active' : ''}`}
            onClick={() => setLeftTab('description')}
          >
            📖 Problem Statement
          </button>
          <button
            className={`toggle-tab ${leftTab === 'problemList' ? 'active' : ''}`}
            onClick={() => setLeftTab('problemList')}
          >
            📋 Problem Catalog ({questions.length})
          </button>
        </div>
      </div>

      {/* Main Split Layout: Left Problem/Catalog Panel & Right Code/Test Panel */}
      <div className="dsa-workspace-grid">
        {/* LEFT COLUMN: Problem Details or Catalog */}
        <div className="dsa-left-panel">
          {leftTab === "problemList" ? (
            /* Catalog List View */
            <div className="dsa-catalog-view">
              <div className="catalog-header">
                <h4>All Placement Problems ({questions.length})</h4>
                <span className="catalog-hint">Click any question to start coding</span>
              </div>
              <div className="catalog-list">
                {questions.map((q) => {
                  const isSolved = solvedIds.has(q.id);
                  const isSelected = selectedQuestion?.id === q.id;
                  return (
                    <div
                      key={q.id}
                      className={`catalog-item ${isSelected ? 'selected' : ''} ${isSolved ? 'solved' : ''}`}
                      onClick={() => loadQuestionDetails(q.id)}
                    >
                      <div className="item-status">
                        {isSolved ? (
                          <span className="solved-badge">✓</span>
                        ) : (
                          <span className="unsolved-dot">•</span>
                        )}
                      </div>
                      <div className="item-info">
                        <div className="item-title-row">
                          <span className="q-number">#{q.id}</span>
                          <strong>{q.title}</strong>
                        </div>
                        <div className="item-tags">
                          <span className={`diff-pill ${q.difficulty.toLowerCase()}`}>
                            {q.difficulty}
                          </span>
                          <span className="category-pill">{q.category}</span>
                          {q.companies && q.companies.slice(0, 2).map((c, i) => (
                            <span key={i} className="company-pill">{c}</span>
                          ))}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ) : (
            /* Problem Description View */
            <div className="dsa-description-view">
              {loadingQuestion ? (
                <div className="dsa-loading">Loading problem statement...</div>
              ) : selectedQuestion ? (
                <div className="problem-details">
                  <div className="problem-header-row">
                    <h2>
                      #{selectedQuestion.id}. {selectedQuestion.title}
                    </h2>
                    <span className={`diff-tag ${selectedQuestion.difficulty.toLowerCase()}`}>
                      {selectedQuestion.difficulty}
                    </span>
                  </div>

                  {/* Company & Topic Tags */}
                  <div className="problem-meta-tags">
                    <span className="topic-badge">🏷️ {selectedQuestion.category}</span>
                    {selectedQuestion.companies && selectedQuestion.companies.map((comp, idx) => (
                      <span key={idx} className="comp-badge">🏢 {comp}</span>
                    ))}
                    {solvedIds.has(selectedQuestion.id) && (
                      <span className="solved-tag">✓ Solved</span>
                    )}
                  </div>

                  {/* Problem Description */}
                  <div className="problem-text">
                    <p style={{ whiteSpace: "pre-line" }}>{selectedQuestion.description}</p>
                  </div>

                  {/* Examples */}
                  {selectedQuestion.examples && selectedQuestion.examples.length > 0 && (
                    <div className="problem-examples">
                      <h4>Examples:</h4>
                      {selectedQuestion.examples.map((ex, i) => (
                        <div key={i} className="example-box">
                          <strong>Example {i + 1}:</strong>
                          <div className="ex-line"><code>Input: {ex.input}</code></div>
                          <div className="ex-line"><code>Output: {ex.output}</code></div>
                          {ex.explanation && (
                            <div className="ex-explain">Explanation: {ex.explanation}</div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Constraints */}
                  {selectedQuestion.constraints && selectedQuestion.constraints.length > 0 && (
                    <div className="problem-constraints">
                      <h4>Constraints & Complexity Goals:</h4>
                      <ul>
                        {selectedQuestion.constraints.map((c, i) => (
                          <li key={i}><code>{c}</code></li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <div className="dsa-empty">Select a question from the catalog</div>
              )}
            </div>
          )}
        </div>

        {/* RIGHT COLUMN: Code Editor & Test Evaluation Runner */}
        <div className="dsa-right-panel">
          {/* Editor Header */}
          <div className="editor-top-bar">
            <div className="editor-lang-badge">
              <span className="py-icon">🐍</span>
              <span>Python 3.11 Sandboxed AST Engine</span>
            </div>

            <div className="editor-ctrl-buttons">
              <button
                className="btn-editor-action reset-btn"
                onClick={handleResetCode}
                title="Restore starter code"
              >
                ↺ Reset
              </button>
              <button
                className="btn-editor-action run-btn"
                onClick={handleRunCode}
                disabled={evaluating}
                title="Run sample test cases"
              >
                {evaluating && evalType === "run" ? "Testing..." : "▶ Run Sample Tests"}
              </button>
              <button
                className="btn-editor-action submit-btn"
                onClick={handleSubmitSolution}
                disabled={evaluating}
                title="Submit solution for full evaluation"
              >
                {evaluating && evalType === "submit" ? "Evaluating..." : "🚀 Submit Solution"}
              </button>
            </div>
          </div>

          {/* Python Code Editor */}
          <div className="dsa-code-editor-wrap">
            <div className="gutter">
              {lines.map((_, idx) => (
                <div key={idx} className="gutter-line">
                  <span className="gutter-num">{idx + 1}</span>
                </div>
              ))}
            </div>
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              spellCheck="false"
              aria-label="Python DSA Code Editor"
              placeholder="# Write your Python solution here..."
            />
          </div>

          {/* Test Case & Submission Results Panel */}
          <div className="dsa-results-panel">
            <div className="results-panel-header">
              <span className="panel-tab-title">
                {evalType === "submit" ? "Submission Results" : "Test Evaluation"}
              </span>

              {evalResult && (
                <span className={`verdict-pill verdict-${evalResult.verdict.toLowerCase().replace(/_/g, '-')}`}>
                  {evalResult.verdict === "ACCEPTED" ? "✓ ACCEPTED" :
                   evalResult.verdict === "WRONG_ANSWER" ? "✗ WRONG ANSWER" :
                   evalResult.verdict === "SYNTAX_ERROR" ? "⛔ SYNTAX ERROR" :
                   evalResult.verdict === "RUNTIME_ERROR" ? "⚠️ RUNTIME ERROR" :
                   evalResult.verdict}
                </span>
              )}
            </div>

            <div className="results-panel-body">
              {evaluating ? (
                <div className="eval-loading">
                  <span className="spinner">⏳</span>
                  <span>Executing test cases against Python AST sandbox...</span>
                </div>
              ) : evalResult ? (
                <div className="eval-output">
                  {/* Verdict Details Header */}
                  <div className={`verdict-banner banner-${evalResult.verdict.toLowerCase().replace(/_/g, '-')}`}>
                    <div className="banner-left">
                      <h3>
                        {evalResult.verdict === "ACCEPTED"
                          ? "🎉 All Test Cases Passed! Solution Accepted."
                          : evalResult.verdict === "WRONG_ANSWER"
                          ? `Wrong Answer on Test Case ${evalResult.firstFailure?.caseIndex || 1}`
                          : evalResult.verdict === "SYNTAX_ERROR"
                          ? "Python Syntax Error Detected"
                          : evalResult.verdict === "RUNTIME_ERROR"
                          ? "Runtime Exception Occurred"
                          : evalResult.verdict}
                      </h3>
                      <div className="banner-sub">
                        <span>Passed: <b>{evalResult.passedCount} / {evalResult.totalCount}</b> test cases</span>
                        {evalResult.totalTimeMs !== undefined && (
                          <span> • Execution Time: <b>{evalResult.totalTimeMs} ms</b></span>
                        )}
                        {evalResult.percentile > 0 && (
                          <span> • Beats <b>{evalResult.percentile}%</b> of submissions</span>
                        )}
                      </div>
                    </div>

                    {/* Complexity Card */}
                    {evalResult.complexity && (
                      <div className="complexity-badge-card">
                        <div>Estimated Time: <b>{evalResult.complexity.timeComplexity}</b></div>
                        <div>Space: <b>{evalResult.complexity.spaceComplexity}</b></div>
                      </div>
                    )}
                  </div>

                  {/* Syntax Error Box */}
                  {evalResult.verdict === "SYNTAX_ERROR" && evalResult.error && (
                    <div className="syntax-error-box">
                      <strong>Line {evalResult.error.line}: {evalResult.error.message}</strong>
                      {evalResult.error.text && <pre><code>{evalResult.error.text}</code></pre>}
                    </div>
                  )}

                  {/* Test Case Details Tabs */}
                  {evalResult.testResults && evalResult.testResults.length > 0 && (
                    <div className="test-cases-inspection">
                      <div className="case-tabs">
                        {evalResult.testResults.map((tc, idx) => (
                          <button
                            key={idx}
                            className={`case-tab-btn ${activeTestCaseTab === idx ? 'active' : ''} ${tc.passed ? 'passed' : 'failed'}`}
                            onClick={() => setActiveTestCaseTab(idx)}
                          >
                            Case {tc.caseIndex} {tc.passed ? "✓" : "✗"}
                          </button>
                        ))}
                      </div>

                      {/* Active Case Details */}
                      {evalResult.testResults[activeTestCaseTab] && (
                        <div className="active-case-details">
                          <div className="case-field">
                            <span className="field-label">Input:</span>
                            <pre><code>{JSON.stringify(evalResult.testResults[activeTestCaseTab].input, null, 2)}</code></pre>
                          </div>

                          <div className="case-field">
                            <span className="field-label">Expected Output:</span>
                            <pre className="expected-pre"><code>{JSON.stringify(evalResult.testResults[activeTestCaseTab].expected)}</code></pre>
                          </div>

                          <div className="case-field">
                            <span className="field-label">Your Output:</span>
                            <pre className={evalResult.testResults[activeTestCaseTab].passed ? "actual-pass" : "actual-fail"}>
                              <code>{evalResult.testResults[activeTestCaseTab].error || JSON.stringify(evalResult.testResults[activeTestCaseTab].actual)}</code>
                            </pre>
                          </div>

                          {evalResult.testResults[activeTestCaseTab].traceback && (
                            <div className="case-field">
                              <span className="field-label">Traceback:</span>
                              <pre className="traceback-pre"><code>{evalResult.testResults[activeTestCaseTab].traceback}</code></pre>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ) : (
                <div className="eval-placeholder">
                  <p>Click <b>"Run Sample Tests"</b> to check your code, or <b>"Submit Solution"</b> for full placement verification.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
