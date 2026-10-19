const express = require("express");
const cors = require("cors");
const path = require("path");
const { spawn, execSync } = require("child_process");
const fs = require("fs");
const crypto = require("crypto");
require("dotenv").config();

const { generateUniqueAvatarSVG } = require("./avatar_generator");
const { sendSignupNotification, getNotificationLogs, ADMIN_PRIMARY_EMAIL } = require("./email_service");

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json({ limit: "5mb" }));

// Persistent Storage Directory
const DATA_DIR = path.join(__dirname, "data");
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}
const USERS_FILE = path.join(DATA_DIR, "users.json");

function loadUsers() {
  try {
    if (fs.existsSync(USERS_FILE)) {
      return JSON.parse(fs.readFileSync(USERS_FILE, "utf-8"));
    }
  } catch (e) {
    console.error("Error reading users file:", e.message);
  }
  return [];
}

function saveUsers(users) {
  try {
    fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2), "utf-8");
  } catch (e) {
    console.error("Error saving users file:", e.message);
  }
}

// Detect available python command
function getPythonCommand() {
  if (process.env.PYTHON_PATH) return process.env.PYTHON_PATH;
  try {
    execSync("python --version", { stdio: "ignore" });
    return "python";
  } catch (e1) {
    try {
      execSync("py --version", { stdio: "ignore" });
      return "py";
    } catch (e2) {
      return "python";
    }
  }
}

const PYTHON_CMD = getPythonCommand();

// Health check endpoint
app.get("/api/health", (req, res) => {
  let pyVersion = "Unknown";
  try {
    pyVersion = execSync(`${PYTHON_CMD} --version`, { encoding: "utf-8" }).trim();
  } catch (e) {}

  res.json({
    status: "ok",
    app: "CodeRescue AI (Real Analysis Engine)",
    engine: "Python AST & Subprocess Sandbox",
    pythonVersion: pyVersion,
    pythonCommand: PYTHON_CMD,
    aiConnected: Boolean(process.env.GEMINI_API_KEY),
    adminEmail: ADMIN_PRIMARY_EMAIL
  });
});

// Dynamic Unique Avatar Endpoint
app.get("/api/avatar/:email", (req, res) => {
  const email = req.params.email || "user@coderescue.dev";
  const svg = generateUniqueAvatarSVG(email);
  res.setHeader("Content-Type", "image/svg+xml");
  res.setHeader("Cache-Control", "public, max-age=86400");
  res.send(svg);
});

// User Sign Up Endpoint
app.post("/api/auth/signup", async (req, res) => {
  const { name, email, password } = req.body;

  if (!email || !email.includes("@")) {
    return res.status(400).json({ error: "Please enter a valid Gmail / Email address." });
  }

  const cleanName = (name && name.trim()) || email.split("@")[0];
  const cleanEmail = email.trim().toLowerCase();

  const users = loadUsers();
  const existingUser = users.find((u) => u.email.toLowerCase() === cleanEmail);

  if (existingUser) {
    return res.status(409).json({
      error: "An account with this email already exists. Please sign in instead.",
      existingUser: {
        id: existingUser.id,
        name: existingUser.name,
        email: existingUser.email,
        avatarSeed: existingUser.avatarSeed
      }
    });
  }

  // Create unique avatar for this user
  const avatarSeed = `avatar_${crypto.createHash("md5").update(cleanEmail).digest("hex").slice(0, 8)}`;
  const avatarSvg = generateUniqueAvatarSVG(cleanEmail);

  const newUser = {
    id: `usr_${Date.now()}_${Math.floor(Math.random() * 1000)}`,
    name: cleanName,
    email: cleanEmail,
    passwordHash: password ? crypto.createHash("sha256").update(password).digest("hex") : null,
    avatarSeed: avatarSeed,
    avatarUrl: `/api/avatar/${encodeURIComponent(cleanEmail)}`,
    createdAt: new Date().toISOString()
  };

  users.push(newUser);
  saveUsers(users);

  // Send real sign-up notification to bkutkars@gmail.com
  let emailResult = null;
  try {
    emailResult = await sendSignupNotification({ user: newUser, avatarSvg });
  } catch (err) {
    console.error("Failed to send signup email:", err.message);
    emailResult = { success: false, error: err.message };
  }

  return res.status(201).json({
    success: true,
    message: "Sign up completed successfully!",
    user: {
      id: newUser.id,
      name: newUser.name,
      email: newUser.email,
      avatarSeed: newUser.avatarSeed,
      avatarUrl: newUser.avatarUrl,
      createdAt: newUser.createdAt
    },
    emailNotification: emailResult
  });
});

// User Login Endpoint
app.post("/api/auth/login", (req, res) => {
  const { email, password } = req.body;
  if (!email) {
    return res.status(400).json({ error: "Email is required." });
  }

  const cleanEmail = email.trim().toLowerCase();
  const users = loadUsers();
  const user = users.find((u) => u.email.toLowerCase() === cleanEmail);

  if (!user) {
    return res.status(404).json({ error: "Account not found with this email. Please sign up first." });
  }

  if (user.passwordHash && password) {
    const hash = crypto.createHash("sha256").update(password).digest("hex");
    if (hash !== user.passwordHash) {
      return res.status(401).json({ error: "Incorrect password. Please try again." });
    }
  }

  return res.json({
    success: true,
    message: "Logged in successfully!",
    user: {
      id: user.id,
      name: user.name,
      email: user.email,
      avatarSeed: user.avatarSeed,
      avatarUrl: user.avatarUrl || `/api/avatar/${encodeURIComponent(user.email)}`,
      createdAt: user.createdAt
    }
  });
});

// View Signup Notifications (for Admin Verification)
app.get("/api/auth/notifications", (req, res) => {
  res.json({
    adminRecipient: ADMIN_PRIMARY_EMAIL,
    notifications: getNotificationLogs()
  });
});

// Test Email Dispatch Endpoint
app.post("/api/auth/test-email", async (req, res) => {
  try {
    const testUser = {
      id: `usr_test_${Date.now()}`,
      name: req.body.name || "Test User",
      email: req.body.email || "test.developer@gmail.com",
      avatarSeed: "avatar_test_preview"
    };
    const result = await sendSignupNotification({ user: testUser });
    return res.json({ success: true, result });
  } catch (err) {
    return res.status(500).json({ success: false, error: err.message });
  }
});

// Real code analysis endpoint
app.post(["/api/debug", "/api/analyze"], (req, res) => {
  const { code, execute = true } = req.body;

  if (typeof code !== "string" || !code.trim()) {
    return res.status(400).json({
      error: "Please provide valid Python code to analyze."
    });
  }

  const scriptPath = path.join(__dirname, "python_analyzer.py");
  const args = [scriptPath, "--stdin"];
  if (!execute) {
    args.push("--no-exec");
  }

  const pyProcess = spawn(PYTHON_CMD, args);
  let stdoutData = "";
  let stderrData = "";

  pyProcess.stdin.write(code);
  pyProcess.stdin.end();

  pyProcess.stdout.on("data", (chunk) => {
    stdoutData += chunk.toString();
  });

  pyProcess.stderr.on("data", (chunk) => {
    stderrData += chunk.toString();
  });

  pyProcess.on("error", (err) => {
    return res.status(500).json({
      error: "Failed to launch Python engine.",
      details: err.message,
      suggestion: "Make sure Python is installed and added to PATH."
    });
  });

  pyProcess.on("close", (exitCode) => {
    if (exitCode !== 0 && !stdoutData.trim()) {
      return res.status(500).json({
        error: "Python analyzer failed with non-zero exit code.",
        details: stderrData || `Exit code: ${exitCode}`
      });
    }

    try {
      const parsed = JSON.parse(stdoutData);
      return res.json({
        mode: "real_analysis",
        engine: "Python 3 AST & Runtime Sandbox",
        ...parsed
      });
    } catch (parseError) {
      return res.status(500).json({
        error: "Failed to parse analyzer response.",
        rawOutput: stdoutData,
        details: stderrData || parseError.message
      });
    }
  });
});

// Serve frontend build if dist folder exists
const distPath = path.join(__dirname, "client", "dist");
if (fs.existsSync(distPath)) {
  app.use(express.static(distPath));
  app.use((req, res, next) => {
    if (req.method === "GET" && !req.path.startsWith("/api")) {
      return res.sendFile(path.join(distPath, "index.html"));
    }
    next();
  });
}

app.listen(PORT, () => {
  console.log(`===============================================`);
  console.log(` CodeRescue AI Real Python Analyzer Backend `);
  console.log(` Server URL    : http://localhost:${PORT}`);
  console.log(` Python CMD    : ${PYTHON_CMD}`);
  console.log(` Admin Alerts  : ${ADMIN_PRIMARY_EMAIL}`);
  console.log(` Authentication: Active (/api/auth/signup, login)`);
  console.log(` Mode          : Real Code Analysis (AST + Runtime)`);
  console.log(`===============================================`);
});
