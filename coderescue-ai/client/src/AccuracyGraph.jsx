import React, { useState } from "react";

export function computeRealAccuracy(analysis) {
  if (!analysis) return null;

  // If code has invalid syntax (cannot compile in Python):
  if (!analysis.validSyntax) {
    const errorCount = analysis.stats?.errorCount || 1;
    return Math.max(5, 25 - errorCount * 5);
  }

  let score = 100;
  const errors = analysis.stats?.errorCount || 0;
  const warnings = analysis.stats?.warningCount || 0;
  const infos = analysis.stats?.infoCount || 0;
  const runtimeError = analysis.execution?.runtimeError;

  score -= errors * 25;
  if (runtimeError) {
    score -= 30;
  }
  score -= warnings * 10;
  score -= infos * 3;

  return Math.max(0, Math.min(100, Math.round(score)));
}

export function AccuracyGraph({ history = [], onClearHistory }) {
  const [hoveredIdx, setHoveredIdx] = useState(null);

  const totalRuns = history.length;
  const latestRun = totalRuns > 0 ? history[totalRuns - 1] : null;
  const prevRun = totalRuns > 1 ? history[totalRuns - 2] : null;

  // Calculate average accuracy
  const avgScore =
    totalRuns > 0
      ? Math.round(
          history.reduce((acc, curr) => acc + curr.score, 0) / totalRuns
        )
      : 0;

  // Calculate improvement trend
  let trendLabel = "Baseline";
  let trendDelta = 0;
  let trendDirection = "neutral"; // "up", "down", "neutral"

  if (totalRuns >= 2 && latestRun && prevRun) {
    trendDelta = latestRun.score - prevRun.score;
    if (trendDelta > 0) {
      trendLabel = `+${trendDelta}% Improved`;
      trendDirection = "up";
    } else if (trendDelta < 0) {
      trendLabel = `${trendDelta}% Decreased`;
      trendDirection = "down";
    } else {
      trendLabel = "Steady (0%)";
      trendDirection = "neutral";
    }
  } else if (totalRuns === 1) {
    trendLabel = "Initial Run";
  }

  // Compare earliest vs latest for overall trajectory
  let overallImprovement = 0;
  if (totalRuns >= 2) {
    overallImprovement = latestRun.score - history[0].score;
  }

  // SVG Chart Geometry
  const width = 440;
  const height = 180;
  const padLeft = 42;
  const padRight = 20;
  const padTop = 24;
  const padBottom = 30;
  const plotWidth = width - padLeft - padRight;
  const plotHeight = height - padTop - padBottom;

  const points = history.map((item, idx) => {
    const x =
      totalRuns <= 1
        ? padLeft + plotWidth / 2
        : padLeft + (idx / (totalRuns - 1)) * plotWidth;
    const y = padTop + (1 - item.score / 100) * plotHeight;
    return { x, y, ...item, idx };
  });

  const linePath =
    points.length === 0
      ? ""
      : points.length === 1
      ? `M ${padLeft} ${points[0].y} L ${width - padRight} ${points[0].y}`
      : points.map((p, idx) => `${idx === 0 ? "M" : "L"} ${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join(" ");

  const areaPath =
    points.length > 1
      ? `${linePath} L ${points[points.length - 1].x.toFixed(1)} ${(padTop + plotHeight).toFixed(1)} L ${points[0].x.toFixed(1)} ${(padTop + plotHeight).toFixed(1)} Z`
      : "";

  const hoveredItem = hoveredIdx !== null ? points[hoveredIdx] : null;

  return (
    <div className="accuracy-graph-container">
      {/* Header Metric Cards */}
      <div className="accuracy-metrics">
        <div className="metric-box">
          <span className="metric-label">Current Accuracy</span>
          <span className="metric-val primary">
            {latestRun ? `${latestRun.score}%` : "--"}
          </span>
          <span
            className={`metric-sub ${
              latestRun?.score >= 85
                ? "good"
                : latestRun?.score >= 60
                ? "fair"
                : "bad"
            }`}
          >
            {latestRun
              ? latestRun.score >= 85
                ? "✓ High Quality"
                : latestRun.score >= 60
                ? "⚠️ Needs Refinement"
                : "⛔ Critical Bugs"
              : "No data yet"}
          </span>
        </div>

        <div className="metric-box">
          <span className="metric-label">Time Improvement</span>
          <span className={`metric-val trend-${trendDirection}`}>
            {trendLabel}
          </span>
          <span className="metric-sub">
            {totalRuns >= 2
              ? overallImprovement >= 0
                ? `Overall: +${overallImprovement}% from start`
                : `Overall: ${overallImprovement}% from start`
              : "Run code to plot progress"}
          </span>
        </div>

        <div className="metric-box">
          <span className="metric-label">Average Score</span>
          <span className="metric-val">{totalRuns > 0 ? `${avgScore}%` : "--"}</span>
          <span className="metric-sub">{totalRuns} test runs recorded</span>
        </div>
      </div>

      {/* Visual SVG Chart */}
      <div className="chart-wrapper">
        <div className="chart-header">
          <span className="chart-title">Accuracy Progress Over Time (0 - 100%)</span>
          {totalRuns > 0 && (
            <button
              className="chart-reset-btn"
              onClick={onClearHistory}
              title="Reset history points"
            >
              Reset History
            </button>
          )}
        </div>

        <div className="svg-canvas-box">
          <svg
            viewBox={`0 0 ${width} ${height}`}
            className="accuracy-svg"
            preserveAspectRatio="none"
          >
            <defs>
              <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.4" />
                <stop offset="100%" stopColor="#38bdf8" stopOpacity="0.0" />
              </linearGradient>
            </defs>

            {/* Gridlines */}
            {[0, 25, 50, 75, 100].map((pct) => {
              const yVal = padTop + (1 - pct / 100) * plotHeight;
              return (
                <g key={pct}>
                  <line
                    x1={padLeft}
                    y1={yVal}
                    x2={width - padRight}
                    y2={yVal}
                    stroke="#1e293b"
                    strokeDasharray={pct === 0 || pct === 100 ? "0" : "3,3"}
                  />
                  <text
                    x={padLeft - 6}
                    y={yVal + 3}
                    textAnchor="end"
                    fill="#64748b"
                    fontSize="9"
                    fontFamily="monospace"
                  >
                    {pct}%
                  </text>
                </g>
              );
            })}

            {/* Area Fill */}
            {areaPath && (
              <path d={areaPath} fill="url(#areaGradient)" />
            )}

            {/* Trend Line */}
            {linePath && (
              <path
                d={linePath}
                fill="none"
                stroke="#38bdf8"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            )}

            {/* Points */}
            {points.map((p, idx) => {
              const isHovered = hoveredIdx === idx;
              const isLatest = idx === points.length - 1;
              const pointColor =
                p.score >= 85
                  ? "#10b981"
                  : p.score >= 55
                  ? "#f59e0b"
                  : "#ef4444";

              return (
                <g key={idx}>
                  <circle
                    cx={p.x}
                    cy={p.y}
                    r={isHovered ? 6 : isLatest ? 5 : 3.5}
                    fill={pointColor}
                    stroke="#070b14"
                    strokeWidth="2"
                    style={{ cursor: "pointer", transition: "all 0.15s ease" }}
                    onMouseEnter={() => setHoveredIdx(idx)}
                    onMouseLeave={() => setHoveredIdx(null)}
                  />
                  {/* Point number indicator */}
                  {(points.length <= 10 || isLatest || isHovered) && (
                    <text
                      x={p.x}
                      y={p.y - 8}
                      textAnchor="middle"
                      fill={isHovered ? "#fff" : "#94a3b8"}
                      fontSize="9"
                      fontWeight="bold"
                    >
                      {p.score}%
                    </text>
                  )}
                </g>
              );
            })}
          </svg>

          {/* Hover Tooltip Overlay */}
          {hoveredItem && (
            <div
              className="chart-tooltip"
              style={{
                left: `${(hoveredItem.x / width) * 100}%`,
                top: `${(hoveredItem.y / height) * 100}%`,
              }}
            >
              <div className="tooltip-title">
                Run #{hoveredItem.idx + 1} • {hoveredItem.timestamp}
              </div>
              <div className="tooltip-body">
                <strong>Accuracy: {hoveredItem.score}%</strong>
                <div>Status: {hoveredItem.status}</div>
                <div>Errors: {hoveredItem.errorsCount} | Warnings: {hoveredItem.warningsCount}</div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* History Log Timeline */}
      <div className="history-log-box">
        <div className="history-title">
          <span>Recent Accuracy History</span>
          <span className="history-count">
            {totalRuns === 0
              ? "No runs yet"
              : `Showing last ${Math.min(5, totalRuns)} runs`}
          </span>
        </div>

        {totalRuns === 0 ? (
          <div className="history-empty">
            Type your Python code and click <strong>"Inspect"</strong> or <strong>"Run & Test"</strong>.
            Your accuracy score will be calculated and tracked on this graph automatically.
          </div>
        ) : (
          <div className="history-items">
            {[...history]
              .reverse()
              .slice(0, 5)
              .map((item, i) => {
                const actualIndex = totalRuns - i;
                const statusColor =
                  item.score >= 85
                    ? "status-clean"
                    : item.score >= 55
                    ? "status-warn"
                    : "status-err";

                return (
                  <div key={item.id || i} className="history-item">
                    <div className="item-meta">
                      <span className="run-tag">Run #{actualIndex}</span>
                      <span className="time-tag">{item.timestamp}</span>
                    </div>

                    <div className="item-details">
                      <span className={`status-pill-small ${statusColor}`}>
                        {item.status}
                      </span>
                      <span className="score-pill">
                        <strong>{item.score}%</strong> Accuracy
                      </span>
                    </div>
                  </div>
                );
              })}
          </div>
        )}
      </div>
    </div>
  );
}
