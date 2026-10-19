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

// Persistent DSA Storage
const DSA_FILE = path.join(DATA_DIR, "dsa_questions.json");
const DSA_PROGRESS_FILE = path.join(DATA_DIR, "dsa_progress.json");

function loadDsaQuestions() {
  try {
    if (fs.existsSync(DSA_FILE)) {
      return JSON.parse(fs.readFileSync(DSA_FILE, "utf-8"));
    }
  } catch (e) {
    console.error("Failed to load DSA questions:", e.message);
  }
  return [];
}

function loadDsaProgress() {
  try {
    if (fs.existsSync(DSA_PROGRESS_FILE)) {
      return JSON.parse(fs.readFileSync(DSA_PROGRESS_FILE, "utf-8"));
    }
  } catch (e) {}
  return { solvedQuestionIds: [], submissions: [] };
}

function saveDsaProgress(progress) {
  try {
    fs.writeFileSync(DSA_PROGRESS_FILE, JSON.stringify(progress, null, 2), "utf-8");
  } catch (e) {
    console.error("Failed to save DSA progress:", e.message);
  }
}

function executeDsaJudge(code, entryFunction, testCases) {
  return new Promise((resolve) => {
    const judgeScript = path.join(__dirname, "dsa_judge.py");
    const py = spawn(PYTHON_CMD, [judgeScript]);
    let stdout = "";
    let stderr = "";

    py.stdout.on("data", (chunk) => { stdout += chunk.toString(); });
    py.stderr.on("data", (chunk) => { stderr += chunk.toString(); });

    py.on("error", (err) => {
      resolve({ verdict: "INTERNAL_ERROR", error: err.message });
    });

    py.on("close", () => {
      try {
        const parsed = JSON.parse(stdout);
        resolve(parsed);
      } catch (err) {
        resolve({
          verdict: "INTERNAL_ERROR",
          error: "Failed to parse judge output: " + (stderr || stdout || err.message)
        });
      }
    });

    py.stdin.write(JSON.stringify({ code, entryFunction, testCases }));
    py.stdin.end();
  });
}

// 1. Get All DSA Questions (with filtering by difficulty, category, search)
app.get("/api/dsa/questions", (req, res) => {
  const { difficulty, category, search } = req.query;
  let questions = loadDsaQuestions();

  if (difficulty && difficulty !== "All") {
    questions = questions.filter((q) => q.difficulty.toLowerCase() === difficulty.toLowerCase());
  }
  if (category && category !== "All") {
    questions = questions.filter((q) => q.category.toLowerCase().includes(category.toLowerCase()));
  }
  if (search) {
    const qTerm = search.toLowerCase();
    questions = questions.filter(
      (q) =>
        q.title.toLowerCase().includes(qTerm) ||
        (q.companies && q.companies.some((c) => c.toLowerCase().includes(qTerm))) ||
        q.category.toLowerCase().includes(qTerm)
    );
  }

  // Summary mapping for fast catalog display
  const summary = questions.map((q) => ({
    id: q.id,
    title: q.title,
    difficulty: q.difficulty,
    category: q.category,
    companies: q.companies || [],
    descriptionPreview: q.description.slice(0, 140) + "...",
    examplesCount: (q.examples || []).length,
    testCasesCount: (q.testCases || []).length
  }));

  const progress = loadDsaProgress();
  const solvedSet = new Set(progress.solvedQuestionIds || []);

  const totalEasy = loadDsaQuestions().filter(q => q.difficulty === "Easy").length;
  const totalMed = loadDsaQuestions().filter(q => q.difficulty === "Medium").length;
  const totalHard = loadDsaQuestions().filter(q => q.difficulty === "Hard").length;

  res.json({
    total: questions.length,
    catalogTotal: loadDsaQuestions().length,
    stats: {
      easy: totalEasy,
      medium: totalMed,
      hard: totalHard,
      solvedCount: solvedSet.size,
      readinessScore: Math.min(100, Math.round((solvedSet.size / 100) * 100))
    },
    solvedIds: Array.from(solvedSet),
    questions: summary
  });
});

// 2. Get Single DSA Question by ID
app.get("/api/dsa/questions/:id", (req, res) => {
  const qId = parseInt(req.params.id, 10);
  const questions = loadDsaQuestions();
  const q = questions.find((item) => item.id === qId);

  if (!q) {
    return res.status(404).json({ error: `DSA Question #${qId} not found.` });
  }

  res.json(q);
});

// 3. Fast Run (Sample Test Cases)
app.post("/api/dsa/run", async (req, res) => {
  const { questionId, code } = req.body;
  if (!code || typeof code !== "string") {
    return res.status(400).json({ error: "Please provide valid Python code." });
  }

  const questions = loadDsaQuestions();
  const q = questions.find((item) => item.id === parseInt(questionId, 10));
  if (!q) {
    return res.status(404).json({ error: "Question not found." });
  }

  const sampleCases = (q.testCases || []).slice(0, 2);
  const judgeResult = await executeDsaJudge(code, q.entryFunction, sampleCases);
  return res.json(judgeResult);
});

// 4. Submit Solution (All Test Cases + Evaluation Record)
app.post("/api/dsa/submit", async (req, res) => {
  const { questionId, code, userEmail } = req.body;
  if (!code || typeof code !== "string") {
    return res.status(400).json({ error: "Please provide valid Python code." });
  }

  const questions = loadDsaQuestions();
  const q = questions.find((item) => item.id === parseInt(questionId, 10));
  if (!q) {
    return res.status(404).json({ error: "Question not found." });
  }

  const allCases = q.testCases || [];
  const judgeResult = await executeDsaJudge(code, q.entryFunction, allCases);

  // If Accepted, update user progress
  const progress = loadDsaProgress();
  const solvedSet = new Set(progress.solvedQuestionIds || []);

  if (judgeResult.verdict === "ACCEPTED") {
    solvedSet.add(q.id);
    progress.solvedQuestionIds = Array.from(solvedSet);
  }

  progress.submissions.unshift({
    timestamp: new Date().toISOString(),
    questionId: q.id,
    questionTitle: q.title,
    difficulty: q.difficulty,
    userEmail: userEmail || "anonymous",
    verdict: judgeResult.verdict,
    passedCount: judgeResult.passedCount,
    totalCount: judgeResult.totalCount,
    totalTimeMs: judgeResult.totalTimeMs,
    complexity: judgeResult.complexity
  });

  saveDsaProgress(progress);

  return res.json({
    ...judgeResult,
    solvedTotal: solvedSet.size,
    isFirstTimeSolved: judgeResult.verdict === "ACCEPTED" && solvedSet.size > (progress.solvedQuestionIds.length - 1)
  });
});

// 5. Get User DSA Placement Statistics
app.get("/api/dsa/stats", (req, res) => {
  const progress = loadDsaProgress();
  const allQ = loadDsaQuestions();
  const solvedSet = new Set(progress.solvedQuestionIds || []);

  const solvedEasy = allQ.filter(q => q.difficulty === "Easy" && solvedSet.has(q.id)).length;
  const solvedMed = allQ.filter(q => q.difficulty === "Medium" && solvedSet.has(q.id)).length;
  const solvedHard = allQ.filter(q => q.difficulty === "Hard" && solvedSet.has(q.id)).length;

  res.json({
    totalSolved: solvedSet.size,
    totalQuestions: allQ.length,
    readinessScore: Math.round((solvedSet.size / allQ.length) * 100),
    breakdown: {
      easy: { solved: solvedEasy, total: 50 },
      medium: { solved: solvedMed, total: 30 },
      hard: { solved: solvedHard, total: 20 }
    },
    solvedQuestionIds: Array.from(solvedSet),
    recentSubmissions: progress.submissions.slice(0, 15)
  });
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
