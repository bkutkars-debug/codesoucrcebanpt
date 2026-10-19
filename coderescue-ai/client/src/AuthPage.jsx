import React, { useState, useEffect } from "react";

function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = (hash << 5) - hash + str.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash);
}

const COLOR_PALETTES = [
  { name: "Indigo Cyber", bg1: "#0f172a", bg2: "#1e1b4b", body: "#6366f1", accent: "#a855f7", eyes: "#38bdf8" },
  { name: "Emerald Matrix", bg1: "#022c22", bg2: "#064e3b", body: "#10b981", accent: "#34d399", eyes: "#fef08a" },
  { name: "Amber Tech", bg1: "#1c1917", bg2: "#451a03", body: "#f59e0b", accent: "#fbbf24", eyes: "#38bdf8" },
  { name: "Cobalt Pulse", bg1: "#172554", bg2: "#1e3a8a", body: "#0284c7", accent: "#38bdf8", eyes: "#4ade80" },
  { name: "Neon Violet", bg1: "#3b0764", bg2: "#581c87", body: "#c084fc", accent: "#e879f9", eyes: "#fef08a" },
  { name: "Crimson Spark", bg1: "#450a0a", bg2: "#7f1d1d", body: "#f43f5e", accent: "#fb7185", eyes: "#67e8f9" },
  { name: "Teal Guardian", bg1: "#18181b", bg2: "#27272a", body: "#06b6d4", accent: "#14b8a6", eyes: "#f43f5e" },
  { name: "Royal Nebula", bg1: "#0c0a09", bg2: "#292524", body: "#8b5cf6", accent: "#a78bfa", eyes: "#22c55e" },
];

export function generateLiveAvatarSVG(email) {
  const cleanEmail = (email || "developer@gmail.com").trim().toLowerCase();
  const hash = hashString(cleanEmail);

  const palette = COLOR_PALETTES[hash % COLOR_PALETTES.length];
  const headVariant = (hash >> 3) % 4;
  const eyeVariant = (hash >> 5) % 5;
  const mouthVariant = (hash >> 8) % 4;
  const accessoryVariant = (hash >> 11) % 4;

  let eyesSvg = "";
  if (eyeVariant === 0) {
    eyesSvg = `
      <circle cx="36" cy="48" r="6" fill="${palette.eyes}" />
      <circle cx="64" cy="48" r="6" fill="${palette.eyes}" />
      <circle cx="38" cy="46" r="2" fill="#ffffff" />
      <circle cx="66" cy="46" r="2" fill="#ffffff" />
    `;
  } else if (eyeVariant === 1) {
    eyesSvg = `
      <rect x="26" y="44" width="48" height="10" rx="5" fill="${palette.eyes}" />
      <line x1="30" y1="49" x2="70" y2="49" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,3" />
    `;
  } else if (eyeVariant === 2) {
    eyesSvg = `
      <rect x="28" y="42" width="18" height="14" rx="3" fill="none" stroke="${palette.eyes}" stroke-width="3" />
      <rect x="54" y="42" width="18" height="14" rx="3" fill="none" stroke="${palette.eyes}" stroke-width="3" />
      <line x1="46" y1="48" x2="54" y2="48" stroke="${palette.eyes}" stroke-width="3" />
      <circle cx="37" cy="49" r="3" fill="#ffffff" />
      <circle cx="63" cy="49" r="3" fill="#ffffff" />
    `;
  } else if (eyeVariant === 3) {
    eyesSvg = `
      <rect x="30" y="46" width="14" height="4" rx="2" fill="${palette.eyes}" />
      <rect x="56" y="46" width="14" height="4" rx="2" fill="${palette.eyes}" />
    `;
  } else {
    eyesSvg = `
      <circle cx="36" cy="48" r="7" fill="${palette.eyes}" />
      <circle cx="64" cy="48" r="7" fill="${palette.eyes}" />
      <polygon points="36,43 38,47 42,48 38,49 36,53 34,49 30,48 34,47" fill="#ffffff" />
      <polygon points="64,43 66,47 70,48 66,49 64,53 62,49 58,48 62,47" fill="#ffffff" />
    `;
  }

  let mouthSvg = "";
  if (mouthVariant === 0) {
    mouthSvg = `<path d="M 40 68 Q 50 78 60 68" stroke="${palette.accent}" stroke-width="3" stroke-linecap="round" fill="none" />`;
  } else if (mouthVariant === 1) {
    mouthSvg = `
      <line x1="38" y1="70" x2="62" y2="70" stroke="${palette.accent}" stroke-width="3" stroke-linecap="round" />
      <circle cx="50" cy="70" r="2" fill="#ffffff" />
    `;
  } else if (mouthVariant === 2) {
    mouthSvg = `<path d="M 38 66 Q 50 78 62 66 Z" fill="${palette.accent}" />`;
  } else {
    mouthSvg = `<path d="M 42 68 Q 54 74 62 66" stroke="${palette.accent}" stroke-width="3" stroke-linecap="round" fill="none" />`;
  }

  let headShapeSvg = "";
  if (headVariant === 0) {
    headShapeSvg = `<rect x="20" y="24" width="60" height="60" rx="16" fill="${palette.body}" />`;
  } else if (headVariant === 1) {
    headShapeSvg = `<circle cx="50" cy="54" r="32" fill="${palette.body}" />`;
  } else if (headVariant === 2) {
    headShapeSvg = `<polygon points="30,24 70,24 84,54 70,84 30,84 16,54" fill="${palette.body}" />`;
  } else {
    headShapeSvg = `<path d="M 22 36 Q 50 20 78 36 L 76 68 Q 50 86 24 68 Z" fill="${palette.body}" />`;
  }

  let accessorySvg = "";
  if (accessoryVariant === 0) {
    accessorySvg = `
      <line x1="50" y1="24" x2="50" y2="12" stroke="${palette.accent}" stroke-width="3" />
      <circle cx="50" cy="10" r="4" fill="${palette.eyes}" />
    `;
  } else if (accessoryVariant === 1) {
    accessorySvg = `
      <rect x="12" y="42" width="6" height="20" rx="3" fill="${palette.accent}" />
      <rect x="82" y="42" width="6" height="20" rx="3" fill="${palette.accent}" />
      <path d="M 16 44 Q 50 14 84 44" stroke="${palette.accent}" stroke-width="3" fill="none" />
    `;
  } else if (accessoryVariant === 2) {
    accessorySvg = `
      <rect x="36" y="8" width="28" height="14" rx="4" fill="#0b1120" stroke="${palette.accent}" stroke-width="1.5" />
      <text x="50" y="19" font-family="monospace" font-size="9" font-weight="bold" fill="${palette.eyes}" text-anchor="middle">&lt;/&gt;</text>
    `;
  } else {
    accessorySvg = `
      <polygon points="40,24 45,14 50,22 55,14 60,24" fill="${palette.accent}" />
      <circle cx="50" cy="12" r="2.5" fill="${palette.eyes}" />
    `;
  }

  return {
    paletteName: palette.name,
    svg: `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGradLive_${hash}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="${palette.bg1}" />
      <stop offset="100%" stop-color="${palette.bg2}" />
    </linearGradient>
  </defs>
  <rect width="100" height="100" rx="24" fill="url(#bgGradLive_${hash})" />
  ${accessorySvg}
  ${headShapeSvg}
  ${eyesSvg}
  ${mouthSvg}
</svg>
`.trim(),
  };
}

export function AuthPage({ onLoginSuccess }) {
  const [mode, setMode] = useState("signup"); // "signup" | "login"
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [successInfo, setSuccessInfo] = useState(null);

  const previewAvatar = generateLiveAvatarSVG(email || "developer@gmail.com");

  async function handleSubmit(e) {
    e.preventDefault();
    setErrorMsg("");

    if (!email || !email.includes("@")) {
      setErrorMsg("Please enter a valid Gmail / Email address.");
      return;
    }

    setLoading(true);

    try {
      const endpoint = mode === "signup" ? "/api/auth/signup" : "/api/auth/login";
      const payload = mode === "signup" ? { name, email, password } : { email, password };

      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Authentication failed.");
      }

      // Persist in localStorage
      localStorage.setItem("coderescue_user", JSON.stringify(data.user));

      // Direct transition to workspace with notification payload
      onLoginSuccess(data.user, data.emailNotification);
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleContinueAfterSignup() {
    if (successInfo?.user) {
      onLoginSuccess(successInfo.user, successInfo.emailNotification);
    }
  }

  return (
    <div className="auth-container">
      {/* Background Glow */}
      <div className="auth-glow-top"></div>
      <div className="auth-glow-bottom"></div>

      <div className="auth-card-wrapper">
        {/* Left Side: Brand & Feature Highlights */}
        <div className="auth-info-panel">
          <div className="auth-brand">
            <span className="brand-icon">{"{🛡️}"}</span>
            <div>
              <h2>CodeRescue <b>AI</b></h2>
              <span className="auth-badge">Python AST & Security Auditor</span>
            </div>
          </div>

          <div className="auth-hero-text">
            <h3>Start debugging with real AST analysis & AI detection</h3>
            <p>
              Join developer teams using CodeRescue AI to catch syntax errors,
              detect unreviewed AI boilerplate, and audit security vulnerabilities.
            </p>
          </div>

          <div className="auth-features">
            <div className="auth-feat-item">
              <span className="feat-icon">🔥</span>
              <div>
                <strong>Line-by-Line AI Attribution Heatmap</strong>
                <p>Pinpoint machine-generated boilerplate vs human-crafted logic.</p>
              </div>
            </div>
            <div className="auth-feat-item">
              <span className="feat-icon">🚨</span>
              <div>
                <strong>Real Security & Hallucination Linter</strong>
                <p>Detect Command Injection (shell=True), SQL bugs, and hardcoded keys.</p>
              </div>
            </div>
            <div className="auth-feat-item">
              <span className="feat-icon">📈</span>
              <div>
                <strong>Time-Series Accuracy Tracking</strong>
                <p>Mathematical scoring to track code improvement across test runs.</p>
              </div>
            </div>
          </div>

          <div className="auth-footer-note">
            <span>🛡️ Admin Notification: Signups are sent to <b>bkutkars@gmail.com</b></span>
          </div>
        </div>

        {/* Right Side: Sign Up / Sign In Form Card */}
        <div className="auth-form-panel">
          {successInfo ? (
            /* Celebration State on Completed Sign-Up */
            <div className="signup-success-state">
              <div className="celebrate-avatar-wrap">
                <div
                  className="celebrate-avatar-svg"
                  dangerouslySetInnerHTML={{
                    __html: generateLiveAvatarSVG(successInfo.user.email).svg,
                  }}
                />
              </div>

              <h2>Welcome to CodeRescue AI, {successInfo.user.name}!</h2>
              <p className="success-subtitle">
                Your unique developer avatar has been generated and your account is active.
              </p>

              <div className="email-dispatch-notice">
                <div className="notice-header">
                  <span className="notice-icon">✉️</span>
                  <strong>Signup Notification Dispatched!</strong>
                </div>
                <p>
                  A real signup notification message with your profile details was sent to:
                </p>
                <div className="notice-recipient">
                  bkutkars@gmail.com
                </div>
                {successInfo.emailNotification?.previewUrl && (
                  <div className="notice-preview">
                    <a
                      href={successInfo.emailNotification.previewUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="preview-link"
                    >
                      🔗 View Live Delivered Email on Ethereal →
                    </a>
                  </div>
                )}
              </div>

              <button
                className="btn-enter-workspace"
                onClick={handleContinueAfterSignup}
              >
                Enter Developer Workspace →
              </button>
            </div>
          ) : (
            /* Normal Sign-Up / Sign-In Form */
            <div>
              <div className="auth-tabs">
                <button
                  type="button"
                  className={`auth-tab ${mode === "signup" ? "active" : ""}`}
                  onClick={() => {
                    setMode("signup");
                    setErrorMsg("");
                  }}
                >
                  Create Account (Sign Up)
                </button>
                <button
                  type="button"
                  className={`auth-tab ${mode === "login" ? "active" : ""}`}
                  onClick={() => {
                    setMode("login");
                    setErrorMsg("");
                  }}
                >
                  Sign In
                </button>
              </div>

              {/* Dynamic Live Avatar Generator Preview */}
              <div className="live-avatar-preview-box">
                <div
                  className="live-avatar-svg"
                  dangerouslySetInnerHTML={{ __html: previewAvatar.svg }}
                />
                <div className="live-avatar-text">
                  <span className="live-avatar-title">Your Unique Developer Avatar</span>
                  <span className="live-avatar-desc">
                    {email.trim()
                      ? `Generated for: ${email}`
                      : "Type your Gmail/email below to watch your unique avatar generate!"}
                  </span>
                  <span className="live-avatar-theme">
                    Theme: <strong>{previewAvatar.paletteName}</strong>
                  </span>
                </div>
              </div>

              <form onSubmit={handleSubmit} className="auth-form">
                {errorMsg && (
                  <div className="auth-error-banner">
                    ⚠️ {errorMsg}
                  </div>
                )}

                {mode === "signup" && (
                  <div className="form-group">
                    <label>Full Name / Developer Alias</label>
                    <input
                      type="text"
                      required
                      placeholder="e.g. Alex Rivers"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                    />
                  </div>
                )}

                <div className="form-group">
                  <label>Gmail / Email Address</label>
                  <input
                    type="email"
                    required
                    placeholder="e.g. alex.dev@gmail.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                  <span className="input-hint">
                    Unique avatar and signup notification will be linked to this email.
                  </span>
                </div>

                <div className="form-group">
                  <label>Password</label>
                  <input
                    type="password"
                    required
                    placeholder="Enter secure password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </div>

                {mode === "signup" && (
                  <div className="admin-alert-note">
                    ℹ️ When you complete signup, an automatic registration alert is sent directly to <strong>bkutkars@gmail.com</strong>.
                  </div>
                )}

                <button
                  type="submit"
                  className="btn-auth-submit"
                  disabled={loading}
                >
                  {loading
                    ? mode === "signup"
                      ? "Generating Unique Avatar & Notifying Admin..."
                      : "Verifying credentials..."
                    : mode === "signup"
                    ? "Complete Sign Up & Enter Workspace →"
                    : "Sign In to Workspace →"}
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
