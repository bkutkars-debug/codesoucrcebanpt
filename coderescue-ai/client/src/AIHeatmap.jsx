import React, { useState } from 'react';

export function AIHeatmap({ heatmap = [], functionBreakdown = [], overallProbability = 0, classification = "" }) {
  const [selectedLine, setSelectedLine] = useState(null);

  if (!heatmap || heatmap.length === 0) {
    return (
      <div className="heatmap-empty">
        <div className="heatmap-empty-icon">🔥</div>
        <h3>No Heatmap Data Available</h3>
        <p>Type or paste your Python code to compute line-by-line AI attribution.</p>
      </div>
    );
  }

  return (
    <div className="ai-heatmap-container">
      {/* Function Attribution Summary Bar */}
      {functionBreakdown && functionBreakdown.length > 0 && (
        <div className="function-breakdown-bar">
          <span className="fn-bar-title">Function Breakdown:</span>
          <div className="fn-pills">
            {functionBreakdown.map((fn, idx) => {
              const badgeClass =
                fn.aiProbability >= 70
                  ? "badge-ai"
                  : fn.aiProbability >= 40
                  ? "badge-assisted"
                  : "badge-human";
              return (
                <div
                  key={idx}
                  className={`fn-pill ${badgeClass}`}
                  title={`Lines ${fn.startLine}-${fn.endLine}: ${fn.reasons.join(', ')}`}
                >
                  <span className="fn-name"><code>def {fn.name}()</code></span>
                  <span className="fn-pct">{fn.aiProbability}% AI</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Heatmap Legend */}
      <div className="heatmap-legend">
        <span className="legend-item">
          <span className="legend-swatch swatch-ai"></span>
          <span>&gt;70% AI Boilerplate</span>
        </span>
        <span className="legend-item">
          <span className="legend-swatch swatch-assisted"></span>
          <span>40-70% Mixed / Assisted</span>
        </span>
        <span className="legend-item">
          <span className="legend-swatch swatch-human"></span>
          <span>&lt;40% Human-Authored</span>
        </span>
      </div>

      {/* Line-by-Line Heatmap Code Viewer */}
      <div className="heatmap-lines">
        {heatmap.map((lineData) => {
          const isSelected = selectedLine === lineData.line;
          const prob = lineData.probability;
          const cls = lineData.classification; // 'ai', 'assisted', 'human'

          return (
            <div
              key={lineData.line}
              className={`heatmap-line line-${cls} ${isSelected ? 'line-selected' : ''}`}
              onClick={() => setSelectedLine(isSelected ? null : lineData.line)}
            >
              <div className="heatmap-line-num">{lineData.line}</div>

              <div className="heatmap-code">
                <code>{lineData.code || " "}</code>
              </div>

              <div className="heatmap-meta">
                <span className={`prob-pill pill-${cls}`}>
                  {prob >= 70 ? `🤖 ${prob}% AI` : prob >= 40 ? `⚡ ${prob}%` : `👤 ${prob}% Human`}
                </span>
              </div>

              {/* Explainable AI Factor Tooltip on Click / Selection */}
              {isSelected && (
                <div className="line-factor-popup">
                  <div className="popup-header">
                    <strong>Line {lineData.line} Attribution: {prob}% Probability</strong>
                    <button className="popup-close" onClick={(e) => { e.stopPropagation(); setSelectedLine(null); }}>✕</button>
                  </div>
                  <div className="popup-factors">
                    {lineData.factors && lineData.factors.length > 0 ? (
                      lineData.factors.map((f, fIdx) => (
                        <div key={fIdx} className="factor-item">• {f}</div>
                      ))
                    ) : (
                      <div className="factor-item">• Standard procedural logic</div>
                    )}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
