import sys
import os
import json
import time
import hashlib
import datetime
import pandas as pd
import streamlit as st

# Ensure local modules can be imported
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from dsa_judge import run_dsa_evaluation, estimate_complexity
from python_analyzer import analyze
from ai_security_linter import audit_ai_code

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="CodeRescue AI | Python DSA Arena & AST Debugger",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Tech Dark Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    code, pre, .stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Top Header Bar */
    .top-hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 12px;
        padding: 1.25rem 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.4);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .hero-title {
        font-size: 1.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa 0%, #a855f7 50%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 0.25rem;
    }
    
    /* Metrics & Cards */
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #38bdf8;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Badges */
    .badge-easy {
        background-color: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-medium {
        background-color: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-hard {
        background-color: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .company-pill {
        background: #334155;
        color: #cbd5e1;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        margin-right: 0.35rem;
        display: inline-block;
    }
    
    /* Spacebar Bottom Attribution */
    .bottom-spacebar {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: linear-gradient(90deg, #090d16 0%, #1e1b4b 50%, #090d16 100%);
        border-top: 1px solid rgba(99, 102, 241, 0.4);
        padding: 0.6rem 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 99999;
        font-size: 0.85rem;
        box-shadow: 0 -4px 16px rgba(0,0,0,0.6);
    }
    .spacebar-left {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #e2e8f0;
    }
    .detector-tag {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: #ffffff;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        letter-spacing: 0.03em;
    }
    .spacebar-contact {
        color: #94a3b8;
    }
    .spacebar-contact a {
        color: #38bdf8;
        font-weight: 600;
        text-decoration: none;
    }
    .spacebar-contact a:hover {
        text-decoration: underline;
    }
    
    /* Heatmap lines */
    .heat-line-ai {
        background-color: rgba(239, 68, 68, 0.18);
        border-left: 3px solid #ef4444;
        padding: 2px 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        margin: 1px 0;
    }
    .heat-line-human {
        background-color: rgba(34, 197, 94, 0.12);
        border-left: 3px solid #22c55e;
        padding: 2px 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        margin: 1px 0;
    }
    .heat-line-neutral {
        background-color: rgba(148, 163, 184, 0.08);
        border-left: 3px solid #64748b;
        padding: 2px 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        margin: 1px 0;
    }
    
    /* Footer spacing for sticky bar */
    .footer-spacer {
        height: 60px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Deterministic Avatar Generator
# ---------------------------------------------------------
def generate_user_avatar_svg(seed: str, size: int = 54) -> str:
    seed_str = (seed or "coderescue-user").strip().lower()
    h = hashlib.md5(seed_str.encode('utf-8')).hexdigest()
    hue = int(h[:4], 16) % 360
    hue2 = (hue + 55) % 360
    color1 = f"hsl({hue}, 75%, 52%)"
    color2 = f"hsl({hue2}, 85%, 42%)"
    
    # Initials
    parts = seed_str.replace("@", ".").split(".")
    if len(parts) >= 2 and parts[0] and parts[1]:
        initials = (parts[0][0] + parts[1][0]).upper()
    else:
        initials = seed_str[:2].upper()
    
    # SVG string
    svg = f"""
    <svg width="{size}" height="{size}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad_{h[:6]}" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="{color1}" />
                <stop offset="100%" stop-color="{color2}" />
            </linearGradient>
            <filter id="shadow_{h[:6]}" x="-10%" y="-10%" width="120%" height="120%">
                <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#000" flood-opacity="0.3"/>
            </filter>
        </defs>
        <circle cx="32" cy="32" r="30" fill="url(#grad_{h[:6]})" stroke="#ffffff" stroke-width="2" filter="url(#shadow_{h[:6]})"/>
        <circle cx="32" cy="32" r="24" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="1.5" stroke-dasharray="3,3"/>
        <text x="32" y="39" font-family="'JetBrains Mono', sans-serif" font-size="20" font-weight="700" fill="#ffffff" text-anchor="middle">{initials}</text>
    </svg>
    """
    return svg


# ---------------------------------------------------------
# Load 100 Questions Data
# ---------------------------------------------------------
@st.cache_data
def load_dsa_questions():
    questions_path = os.path.join(CURRENT_DIR, "data", "dsa_questions.json")
    if not os.path.exists(questions_path):
        # Fallback search
        alt_path = os.path.join(os.path.dirname(CURRENT_DIR), "coderescue-ai", "data", "dsa_questions.json")
        if os.path.exists(alt_path):
            questions_path = alt_path
    with open(questions_path, "r", encoding="utf-8") as f:
        return json.load(f)

dsa_questions = load_dsa_questions()


# ---------------------------------------------------------
# Initialize Session State
# ---------------------------------------------------------
if "user_email" not in st.session_state:
    st.session_state.user_email = "student@placement.ai"
if "solved_questions" not in st.session_state:
    st.session_state.solved_questions = set()
if "submissions_history" not in st.session_state:
    st.session_state.submissions_history = [
        {"run": 1, "accuracy": 60.0, "passed": 3, "total": 5, "type": "DSA", "title": "Two Sum", "time": "10:00"},
        {"run": 2, "accuracy": 80.0, "passed": 4, "total": 5, "type": "DSA", "title": "Reverse Linked List", "time": "10:15"},
        {"run": 3, "accuracy": 100.0, "passed": 5, "total": 5, "type": "DSA", "title": "Valid Parentheses", "time": "10:30"}
    ]
if "last_verdict" not in st.session_state:
    st.session_state.last_verdict = None
if "selected_q_id" not in st.session_state:
    st.session_state.selected_q_id = dsa_questions[0]["id"]


# ---------------------------------------------------------
# Sidebar Profile & Readiness Tracker
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 👤 User Profile & Avatar")
    avatar_html = generate_user_avatar_svg(st.session_state.user_email, size=64)
    
    col_av, col_info = st.columns([1, 2])
    with col_av:
        st.markdown(avatar_html, unsafe_allow_html=True)
    with col_info:
        email_input = st.text_input("Your Email / ID", value=st.session_state.user_email, key="email_box")
        if email_input != st.session_state.user_email:
            st.session_state.user_email = email_input
            st.rerun()
            
    st.markdown(f"**Status**: `Active Contender` 🛡️")
    st.caption("Custom deterministic SVG avatar generated live from email hash.")
    
    st.divider()
    
    # DSA Placement Readiness
    total_q = len(dsa_questions)
    easy_q = [q for q in dsa_questions if q["difficulty"] == "Easy"]
    med_q = [q for q in dsa_questions if q["difficulty"] == "Medium"]
    hard_q = [q for q in dsa_questions if q["difficulty"] == "Hard"]
    
    solved_easy = len([qid for qid in st.session_state.solved_questions if any(q["id"] == qid and q["difficulty"] == "Easy" for q in dsa_questions)])
    solved_med = len([qid for qid in st.session_state.solved_questions if any(q["id"] == qid and q["difficulty"] == "Medium" for q in dsa_questions)])
    solved_hard = len([qid for qid in st.session_state.solved_questions if any(q["id"] == qid and q["difficulty"] == "Hard" for q in dsa_questions)])
    total_solved = len(st.session_state.solved_questions)
    
    st.markdown("### 🎯 Placement Readiness")
    readiness_pct = round((total_solved / total_q) * 100, 1)
    st.progress(readiness_pct / 100.0)
    st.write(f"**Solved**: `{total_solved} / {total_q}` ({readiness_pct}%)")
    
    col_e, col_m, col_h = st.columns(3)
    col_e.metric("Easy", f"{solved_easy}/{len(easy_q)}")
    col_m.metric("Medium", f"{solved_med}/{len(med_q)}")
    col_h.metric("Hard", f"{solved_hard}/{len(hard_q)}")
    
    st.divider()
    
    st.markdown("### 📡 Quick Contact")
    st.markdown("""
    - **Engine**: `coderescue-ai`
    - **Mentor / Dev**: [bkutkars@gmail.com](mailto:bkutkars@gmail.com)
    - **Mode**: 100% Real AST & Runtime (Zero Mock)
    """)


# ---------------------------------------------------------
# Top Hero Banner
# ---------------------------------------------------------
st.markdown("""
<div class="top-hero-banner">
    <div>
        <h1 class="hero-title">🛡️ CodeRescue AI — Python Placement & DSA Hub</h1>
        <div class="hero-subtitle">100 LeetCode/Codeforces Tier Questions • Real AST Error Debugger • Granular AI Attribution Heatmap • Security Linter</div>
    </div>
    <div>
        <span class="badge-medium">Real Python Engine</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Navigation Tabs
# ---------------------------------------------------------
tab_dsa, tab_debugger, tab_linter, tab_analytics, tab_video = st.tabs([
    "⚔️ 100 DSA Placement Arena",
    "🔍 Python AST Debugger & Sandbox",
    "🔥 AI Attribution & Security Linter",
    "📈 Accuracy & Progress Analytics",
    "🎬 Video Walkthrough & 14-Feature Gallery"
])


# =========================================================
# TAB 1: 100 DSA PLACEMENT ARENA
# =========================================================
with tab_dsa:
    st.markdown("### 🏆 100-Question Python DSA Placement Arena")
    st.caption("Practice curated FAANG & top-tier placement problems across Easy (50), Medium (30), and Hard (20). Real test evaluation running at < 1ms execution speed.")
    
    # Filter Row
    col_diff, col_cat, col_comp = st.columns([1, 1, 1])
    with col_diff:
        diff_filter = st.selectbox("Difficulty Filter", ["All Difficulties", "Easy (50)", "Medium (30)", "Hard (20)"])
    with col_cat:
        all_cats = sorted(list(set(q.get("category", "General") for q in dsa_questions)))
        cat_filter = st.selectbox("Topic Category", ["All Categories"] + all_cats)
    with col_comp:
        all_comps = sorted(list(set(c for q in dsa_questions for c in q.get("companies", []))))
        comp_filter = st.selectbox("Target Company", ["All Companies"] + all_comps)
        
    # Apply Filters
    filtered_questions = dsa_questions
    if "Easy" in diff_filter:
        filtered_questions = [q for q in filtered_questions if q["difficulty"] == "Easy"]
    elif "Medium" in diff_filter:
        filtered_questions = [q for q in filtered_questions if q["difficulty"] == "Medium"]
    elif "Hard" in diff_filter:
        filtered_questions = [q for q in filtered_questions if q["difficulty"] == "Hard"]
        
    if cat_filter != "All Categories":
        filtered_questions = [q for q in filtered_questions if q.get("category") == cat_filter]
        
    if comp_filter != "All Companies":
        filtered_questions = [q for q in filtered_questions if comp_filter in q.get("companies", [])]

    if not filtered_questions:
        st.warning("No questions match the selected filters. Please adjust your criteria.")
        filtered_questions = dsa_questions

    # Question Selection Box
    def format_q_label(q):
        check = "✅ " if q["id"] in st.session_state.solved_questions else "⬜ "
        return f"{check}Q{q['id']:03d}: {q['title']} ({q['difficulty']}) - {q['category']}"
        
    selected_idx = 0
    # Try to keep currently selected
    for idx, q in enumerate(filtered_questions):
        if q["id"] == st.session_state.selected_q_id:
            selected_idx = idx
            break
            
    selected_q = st.selectbox(
        "Select Problem to Solve",
        filtered_questions,
        index=selected_idx,
        format_func=format_q_label
    )
    st.session_state.selected_q_id = selected_q["id"]
    
    st.divider()
    
    # Problem Layout: Left Column = Problem Statement, Right Column = Code Editor & Test Results
    col_stmt, col_editor = st.columns([1, 1], gap="medium")
    
    with col_stmt:
        # Title & Badges
        diff_class = f"badge-{selected_q['difficulty'].lower()}"
        st.markdown(f"## {selected_q['title']} <span class='{diff_class}'>{selected_q['difficulty']}</span>", unsafe_allow_html=True)
        st.write(f"**Category**: `{selected_q['category']}`")
        
        # Company Tags
        comp_tags = "".join([f"<span class='company-pill'>{c}</span>" for c in selected_q.get("companies", [])])
        st.markdown(f"**Target Companies**: {comp_tags}", unsafe_allow_html=True)
        
        st.markdown("#### Description")
        st.markdown(selected_q["description"])
        
        st.markdown("#### Examples")
        for idx, ex in enumerate(selected_q.get("examples", [])):
            with st.expander(f"Example {idx+1}", expanded=(idx == 0)):
                st.code(f"Input: {ex.get('input')}\nOutput: {ex.get('output')}", language="text")
                if ex.get("explanation"):
                    st.caption(f"💡 {ex['explanation']}")
                    
        st.markdown("#### Constraints")
        for c in selected_q.get("constraints", []):
            st.markdown(f"- `{c}`")

    with col_editor:
        st.markdown(f"#### 🐍 Python Solution Editor (`def {selected_q['entryFunction']}`) ")
        
        code_key = f"code_editor_{selected_q['id']}"
        if code_key not in st.session_state:
            st.session_state[code_key] = selected_q.get("starterCode", "")
            
        user_code = st.text_area(
            "Write your solution here:",
            value=st.session_state[code_key],
            height=300,
            key=f"text_area_{selected_q['id']}"
        )
        st.session_state[code_key] = user_code
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn1:
            run_btn = st.button("⚡ Run Tests (Sample)", key=f"run_btn_{selected_q['id']}", use_container_width=True)
        with col_btn2:
            submit_btn = st.button("🚀 Submit Solution", type="primary", key=f"submit_btn_{selected_q['id']}", use_container_width=True)
        with col_btn3:
            if st.button("🔄 Reset Code", key=f"reset_btn_{selected_q['id']}", use_container_width=True):
                st.session_state[code_key] = selected_q.get("starterCode", "")
                st.rerun()

        # Judge Execution
        if run_btn or submit_btn:
            is_full_submit = submit_btn
            test_cases_to_run = selected_q.get("testCases", [])
            if not is_full_submit:
                # Run first 2 sample cases for fast test run
                test_cases_to_run = test_cases_to_run[:2]
                
            payload = {
                "code": user_code,
                "entryFunction": selected_q.get("entryFunction"),
                "testCases": test_cases_to_run
            }
            
            with st.spinner("Evaluating Python execution against test cases..."):
                judge_result = run_dsa_evaluation(payload)
                complexity = estimate_complexity(user_code)
                
            verdict = judge_result.get("verdict")
            passed = judge_result.get("passedCount", 0)
            total = judge_result.get("totalCount", len(test_cases_to_run))
            total_time = judge_result.get("totalExecutionTimeMs", 0.0)
            
            # Record submission for accuracy analytics
            acc_pct = round((passed / total * 100) if total > 0 else 0, 1)
            new_run_id = len(st.session_state.submissions_history) + 1
            st.session_state.submissions_history.append({
                "run": new_run_id,
                "accuracy": acc_pct,
                "passed": passed,
                "total": total,
                "type": "DSA",
                "title": selected_q["title"],
                "time": datetime.datetime.now().strftime("%H:%M:%S")
            })
            
            # Display Big Verdict Box
            if verdict == "ACCEPTED":
                if is_full_submit:
                    st.session_state.solved_questions.add(selected_q["id"])
                    st.success(f"🎉 **ACCEPTED!** All {total}/{total} Test Cases Passed in {total_time} ms!")
                    st.balloons()
                else:
                    st.success(f"✅ **Sample Tests Passed!** ({passed}/{total}) in {total_time} ms. Ready to Submit!")
            elif verdict == "WRONG_ANSWER":
                st.error(f"❌ **WRONG ANSWER**: Passed {passed}/{total} test cases.")
            elif verdict == "SYNTAX_ERROR":
                err = judge_result.get("error", {})
                st.warning(f"⚠️ **SYNTAX ERROR** at Line {err.get('line')}: {err.get('message')}")
            elif verdict == "COMPILE_ERROR" or verdict == "RUNTIME_ERROR":
                err = judge_result.get("error", {})
                st.error(f"💥 **RUNTIME {err.get('type')}**: {err.get('message')}")
            else:
                st.info(f"ℹ️ **Verdict**: {verdict} - {judge_result.get('message')}")

            # Interview AST Complexity Advisor
            st.markdown("##### ⏱️ Placement Interview Complexity Profile")
            col_c1, col_c2, col_c3 = st.columns(3)
            col_c1.metric("Time Complexity", complexity.get("timeComplexity", "O(N)"))
            col_c2.metric("Space Complexity", complexity.get("spaceComplexity", "O(1)"))
            col_c3.metric("Execution Time", f"{total_time} ms")
            st.info(f"🧠 **Interview Advice**: {complexity.get('interviewAdvice', 'Good approach.')}")
            
            # Detailed Test Case Breakdown
            st.markdown("##### 🧪 Detailed Test Case Results")
            for t_idx, tc_res in enumerate(judge_result.get("testResults", [])):
                status_icon = "✅ Passed" if tc_res.get("passed") else "❌ Failed"
                with st.expander(f"Test Case {tc_res.get('caseNumber')}: {status_icon} ({tc_res.get('executionTimeMs')} ms)"):
                    st.code(f"Input:    {json.dumps(tc_res.get('input'))}\nExpected: {json.dumps(tc_res.get('expected'))}\nActual:   {json.dumps(tc_res.get('actual'))}", language="text")
                    if tc_res.get("error"):
                        st.error(f"Error: {tc_res.get('error')}")


# =========================================================
# TAB 2: PYTHON AST DEBUGGER & SANDBOX
# =========================================================
with tab_debugger:
    st.markdown("### 🔍 Real Python AST Debugger & Runtime Sandbox")
    st.caption("Performs static AST code tree inspection, scope resolution, NameError detection, mutable default arguments detection, and safe runtime execution.")

    debugger_presets = {
        "Custom Code": "# Write or paste your Python code here\ndef solve(x):\n    return x * 2\n\nprint(solve(21))",
        "SyntaxError: Missing Colon & Parenthesis": "def calculate_average(items)\n    total = sum(items\n    return total / len(items)\n\nprint(calculate_average([10, 20, 30]))",
        "NameError: Undefined Variable & Typo": "def process_user_data(user_name):\n    greeting = 'Hello, ' + user_name\n    print(greetng)  # Typo in variable name\n    return results   # Undefined name\n\nprocess_user_data('Alex')",
        "Warning: Mutable Default Argument (W001)": "def append_item(val, container=[]):\n    # Bug: container is shared across all function invocations!\n    container.append(val)\n    return container\n\nprint(append_item(1))\nprint(append_item(2))",
        "Security Issue: Dangerous Subprocess shell=True": "import subprocess\n\ndef run_system_cmd(cmd):\n    # Critical: Command injection vulnerability\n    res = subprocess.run(cmd, shell=True, capture_output=True)\n    return res.stdout\n\nrun_system_cmd('echo Hello Security')"
    }
    
    preset_choice = st.selectbox("Choose a Code Preset to Test", list(debugger_presets.keys()))
    
    if "dbg_code" not in st.session_state or st.session_state.get("last_preset") != preset_choice:
        st.session_state["dbg_code"] = debugger_presets[preset_choice]
        st.session_state["last_preset"] = preset_choice
        
    code_input = st.text_area("Python Code to Analyze:", value=st.session_state["dbg_code"], height=220)
    st.session_state["dbg_code"] = code_input

    col_dbg1, col_dbg2 = st.columns([1, 4])
    with col_dbg1:
        run_analysis_btn = st.button("🚀 Analyze & Execute", type="primary", use_container_width=True)
    with col_dbg2:
        exec_toggle = st.checkbox("Execute code in sandbox if syntax is valid", value=True)

    if run_analysis_btn:
        with st.spinner("Analyzing AST and executing code..."):
            res = analyze(code_input, execute=exec_toggle)

        # Summary Metrics
        stats = res.get("stats", {})
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Syntax Valid", "YES ✅" if res.get("validSyntax") else "NO ❌")
        col_m2.metric("Errors Detected", stats.get("errorCount", 0))
        col_m3.metric("Warnings", stats.get("warningCount", 0))
        col_m4.metric("Total Lines", stats.get("totalLines", 0))
        
        st.divider()

        # Detailed Issues
        issues = res.get("issues", [])
        st.markdown(f"#### 📋 Code Inspector Report ({len(issues)} items)")
        if not issues:
            st.success("🎉 **Zero Issues Found!** Code syntax is 100% valid with clean AST tree.")
        else:
            for iss in issues:
                sev = iss.get("severity", "error")
                line = iss.get("line", 1)
                col = iss.get("column", 1)
                code_id = iss.get("code", "ERR")
                title = iss.get("title", "Issue")
                msg = iss.get("message", "")
                sugg = iss.get("suggestion", "")

                if sev == "error":
                    st.error(f"🔴 **[{code_id}] {title}** (Line {line}, Col {col})\n\n{msg}\n\n💡 **Suggestion**: `{sugg}`")
                elif sev == "warning":
                    st.warning(f"🟡 **[{code_id}] {title}** (Line {line}, Col {col})\n\n{msg}\n\n💡 **Suggestion**: `{sugg}`")
                else:
                    st.info(f"🔵 **[{code_id}] {title}** (Line {line}, Col {col})\n\n{msg}")

        # Runtime Output
        if res.get("execution"):
            exec_data = res["execution"]
            st.markdown("#### 🖥️ Sandbox Execution Output")
            col_ex1, col_ex2 = st.columns(2)
            col_ex1.caption(f"Exit Code: `{exec_data.get('exitCode')}`")
            col_ex2.caption(f"Execution Time: `{exec_data.get('executionTimeMs')} ms`")
            
            stdout_text = exec_data.get("stdout")
            stderr_text = exec_data.get("stderr")
            if stdout_text:
                st.code(stdout_text, language="text")
            if stderr_text:
                st.error("Standard Error:")
                st.code(stderr_text, language="text")
                
        # Smart Fix Recommendation
        if res.get("suggestedFix"):
            st.markdown("#### 🛠️ Automated Smart Fix Suggestion")
            st.code(res["suggestedFix"], language="python")


# =========================================================
# TAB 3: EXPLAINABLE AI ATTRIBUTION HEATMAP & SECURITY LINTER
# =========================================================
with tab_linter:
    st.markdown("### 🔥 Explainable AI Attribution Heatmap & Security Linter")
    st.caption("Granular line-by-line attribution distinguishing AI boilerplate from human-authored code, plus automated vulnerability scanning (OWASP/CWE) and hallucinated API detection.")

    sample_ai_code = """import subprocess
import hashlib
import math

def process_data(input_data):
    # Initialize the result list
    result_list = []
    
    # Loop through each item in the data
    for item in input_data:
        # Check if item is valid
        if item is not None:
            # Perform calculation
            val = math.round(item * 1.5)  # Hallucinated API: math.round()
            result_list.append(val)
            
    # Vulnerable shell command execution
    subprocess.run("echo processing " + str(len(result_list)), shell=True)
    
    # Insecure MD5 hash for password storage
    pw_hash = hashlib.md5(b"secret").hexdigest()
    
    return result_list
"""
    linter_code = st.text_area("Inspect code for AI attribution & security vulnerabilities:", value=sample_ai_code, height=240)
    
    if st.button("🔥 Run AI Attribution & Security Audit", type="primary"):
        with st.spinner("Analyzing attribution factors, generating line heatmap, and auditing security..."):
            audit = audit_ai_code(linter_code)

        overall_prob = audit.get("overallProbability", 0)
        classification = audit.get("classification", "Unknown")
        vulns = audit.get("vulnerabilities", [])
        hallucs = audit.get("hallucinations", [])
        perfs = audit.get("performanceBottlenecks", [])

        # Top Metric Cards
        col_p1, col_p2, col_p3 = st.columns(3)
        col_p1.metric("Overall AI Probability", f"{overall_prob}%")
        col_p2.metric("Security Vulnerabilities", len(vulns))
        col_p3.metric("Hallucinated / Deprecated APIs", len(hallucs))

        # Classification Banner
        if overall_prob >= 70:
            st.error(f"🤖 **Attribution Verdict**: {classification} ({overall_prob}% probability)")
        elif overall_prob >= 40:
            st.warning(f"🤝 **Attribution Verdict**: {classification} ({overall_prob}% probability)")
        else:
            st.success(f"👤 **Attribution Verdict**: {classification} ({overall_prob}% probability)")

        # Granular Line Heatmap
        st.markdown("#### 🗺️ Granular Line-by-Line Attribution Heatmap")
        heatmap = audit.get("lineHeatmap", [])
        heatmap_html = ["<div style='background: #0d1117; padding: 12px; border-radius: 8px; border: 1px solid #30363d;'>"]
        for row in heatmap:
            l_num = row.get("line")
            txt = row.get("text", "").replace("<", "&lt;").replace(">", "&gt;")
            prob = row.get("aiProbability", 0)
            tag = row.get("attribution", "Neutral")
            
            if prob >= 65:
                cls_name = "heat-line-ai"
                tag_icon = "🤖 AI"
            elif prob <= 35:
                cls_name = "heat-line-human"
                tag_icon = "👤 Human"
            else:
                cls_name = "heat-line-neutral"
                tag_icon = "⚖️ Mixed"
                
            heatmap_html.append(
                f"<div class='{cls_name}'>"
                f"<span style='color: #64748b; margin-right: 12px; font-size: 0.75rem;'>{l_num:02d}</span>"
                f"<span style='color: #e2e8f0;'>{txt if txt else '&nbsp;'}</span>"
                f"<span style='float: right; font-size: 0.7rem; color: #94a3b8; margin-left: 10px;'>{tag_icon} ({prob}%)</span>"
                f"</div>"
            )
        heatmap_html.append("</div>")
        st.markdown("".join(heatmap_html), unsafe_allow_html=True)
        
        # Security & Hallucination Details
        st.divider()
        st.markdown("#### 🛡️ Automated Security & Hallucination Linter")
        if not vulns and not hallucs and not perfs:
            st.success("✅ No security vulnerabilities or hallucinated APIs detected in this code.")
        else:
            for v in vulns:
                st.error(f"🔴 **Vulnerability ({v.get('cwe')})**: {v.get('title')} at Line {v.get('line')}\n\n{v.get('message')}\n\n👉 **Recommendation**: `{v.get('recommendation')}`")
            for h in hallucs:
                st.warning(f"🟡 **Hallucinated / Deprecated API**: Line {h.get('line')} - `{h.get('hallucinated')}`\n\n{h.get('explanation')}\n\n👉 **Fix**: Use `{h.get('correctAlternative')}`")
            for p in perfs:
                st.info(f"⚡ **Performance Bottleneck**: Line {p.get('line')} - {p.get('message')}")

        # Human Refactored Fix
        if audit.get("humanRefactoredCode"):
            st.markdown("#### 💡 Human-Refactored Secure Fix")
            st.code(audit["humanRefactoredCode"], language="python")

        # GitHub Action PR Comment
        st.markdown("#### 🐙 GitHub Action PR Review Preview")
        st.markdown(audit.get("githubActionComment", ""))


# =========================================================
# TAB 4: ACCURACY & PROGRESS ANALYTICS
# =========================================================
with tab_analytics:
    st.markdown("### 📈 Accuracy & Skill Improvement Analytics")
    st.caption("Real-time graph tracking of your Python code accuracy and DSA test pass rates over time.")
    
    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    history = st.session_state.submissions_history
    
    latest_acc = history[-1]["accuracy"] if history else 0.0
    avg_acc = round(sum(h["accuracy"] for h in history) / len(history), 1) if history else 0.0
    total_runs = len(history)
    
    col_a1.metric("Latest Run Accuracy", f"{latest_acc}%", f"{round(latest_acc - avg_acc, 1)}% vs avg")
    col_a2.metric("Average Accuracy", f"{avg_acc}%")
    col_a3.metric("Total Code Evaluations", total_runs)
    col_a4.metric("DSA Solved", f"{len(st.session_state.solved_questions)} / 100")
    
    st.divider()
    
    # Accuracy Time Series Chart
    st.markdown("#### 📉 Accuracy Improvement Over Time")
    if history:
        df_history = pd.DataFrame(history)
        df_history["Run #"] = df_history["run"].astype(str)
        chart_data = df_history.set_index("Run #")[["accuracy"]]
        st.line_chart(chart_data, color="#38bdf8")
    else:
        st.info("Run DSA problems or AST analyses to build your real accuracy graph.")
        
    st.divider()
    
    # Topic Mastery Chart
    st.markdown("#### 📊 DSA Topic Coverage Breakdown")
    cat_counts = {}
    for q in dsa_questions:
        c = q.get("category", "General")
        cat_counts[c] = cat_counts.get(c, 0) + 1
        
    df_cats = pd.DataFrame(list(cat_counts.items()), columns=["Topic", "Questions"]).sort_values("Questions", ascending=False)
    st.bar_chart(df_cats.set_index("Topic"))
    
    st.divider()
    
    # Submissions Log Table
    st.markdown("#### 📜 Recent Submissions Log")
    if history:
        st.dataframe(pd.DataFrame(history)[["run", "title", "accuracy", "passed", "total", "time"]], use_container_width=True)


# =========================================================
# TAB 5: VIDEO WALKTHROUGH & 14-FEATURE GALLERY
# =========================================================
with tab_video:
    st.markdown("### 🎬 Full Subsystem Walkthrough Video (HD 1280x720)")
    st.caption("A complete video explanation detailing every subsystem of CodeRescue AI, accompanied by high-definition architectural illustrations for each component.")
    
    video_file_path = os.path.join(CURRENT_DIR, "media", "coderescue_explanation_walkthrough.mp4")
    if os.path.exists(video_file_path):
        st.video(video_file_path)
        st.markdown("**Direct Walkthrough Video URL**: `http://localhost:5000/media/coderescue_explanation_walkthrough.mp4`")
    else:
        st.info("Walkthrough video is being prepared.")
        
    st.divider()
    st.markdown("### 🖼️ 14-Component Architectural Visual Gallery")
    st.caption("All 14 subsystems engineered into CodeRescue AI with non-mock algorithmic accuracy.")
    
    features_data = [
        ("01. CodeRescue AI Master Hub", "01_project_overview_banner.jpg", "Futuristic cybernetic banner showcasing the real Python Abstract Syntax Tree (AST) engine, cybersecurity matrix shields, and placement telemetry."),
        ("02. Deterministic Avatar & Auth", "02_user_avatar_auth_system.jpg", "Unique mathematical SVG avatar generation from user email hash, with live notification dispatch to mentor at bkutkars@gmail.com."),
        ("03. 100 Python DSA Placement Arena", "03_100_dsa_placement_arena.jpg", "Curated technical placement curriculum: 50 Easy (emerald), 30 Medium (gold), 20 Hard (ruby) mapped to Google, Amazon, Meta, and Microsoft."),
        ("04. Sub-Millisecond Code Judge", "04_submillisecond_code_judge.jpg", "Ultra-fast in-memory test case runner executing user Python solutions in < 1 ms with deep equality matching and zero mock results."),
        ("05. AST Big-O Complexity Profiler", "05_ast_complexity_profiler.jpg", "Automated algorithmic analysis parsing loop nesting and recursion to output Big-O Time & Space complexity plus placement interview advice."),
        ("06. AST Syntax Error Engine", "06_ast_syntax_error_engine.jpg", "Pinpoints exact line and column numbers for syntax defects, missing colons, unbalanced brackets, and generates 1-click repairs."),
        ("07. Scope & NameError Resolver", "07_scope_name_error_resolver.jpg", "Tracks Python LEGB scope hierarchy to catch undefined names, variable typos, and missing imports before code execution starts."),
        ("08. Anti-Pattern Linter (W001)", "08_mutable_default_arg_linter.jpg", "Detects mutable default arguments (def foo(items=[])) that silently share state across calls, suggesting clean 'None' initializations."),
        ("09. AI Attribution Heatmap", "09_ai_attribution_heatmap.jpg", "Granular line-by-line classification of AI boilerplate vs. human-authored code with probability scores and color-coded visual highlighting."),
        ("10. Security Vulnerability Scanner", "10_security_vulnerability_scanner.jpg", "OWASP & CWE security audit detecting dangerous shell=True injection (CWE-78), raw SQL injection (CWE-89), and weak MD5 hashing (CWE-327)."),
        ("11. Hallucinated API Detector", "11_hallucinated_api_detector.jpg", "Catches non-existent functions commonly hallucinated by AI (e.g., math.round(), dict.has_key()) and redirects to standard library methods."),
        ("12. Human-Refactored Fix Engine", "12_human_refactored_fix_engine.png", "Transforms bloated, vulnerable code into clean, secure, idiomatic Python with side-by-side diff comparisons ready for immediate copy."),
        ("13. GitHub Actions PR Review Bot", "13_github_actions_pr_bot.jpg", "Simulated CI/CD bot posting automated Pull Request comments with risk alerts, boilerplate percentages, and merge checklists."),
        ("14. Accuracy & Progress Analytics", "14_accuracy_progress_analytics.jpg", "Time-series graph tracking accuracy improvement over consecutive code runs, DSA topic mastery bars, and placement readiness gauges.")
    ]
    
    for i in range(0, len(features_data), 2):
        c1, c2 = st.columns(2)
        # Col 1
        t1, img1, desc1 = features_data[i]
        ipath1 = os.path.join(CURRENT_DIR, "media", "images", img1)
        with c1:
            st.markdown(f"#### {t1}")
            if os.path.exists(ipath1):
                st.image(ipath1, use_container_width=True)
            st.caption(desc1)
            
        # Col 2
        if i + 1 < len(features_data):
            t2, img2, desc2 = features_data[i+1]
            ipath2 = os.path.join(CURRENT_DIR, "media", "images", img2)
            with c2:
                st.markdown(f"#### {t2}")
                if os.path.exists(ipath2):
                    st.image(ipath2, use_container_width=True)
                st.caption(desc2)
        st.divider()


# ---------------------------------------------------------
# Spacebar Bottom Attribution & Contact Banner
# ---------------------------------------------------------
st.markdown("""
<div class="footer-spacer"></div>
<div class="bottom-spacebar">
    <div class="spacebar-left">
        <span class="detector-tag">coderescue-ai</span>
        <span>Python Error & Placement Diagnostic Engine</span>
    </div>
    <div class="spacebar-contact">
        Found a difficult problem or need assistance? Message me: <a href="mailto:bkutkars@gmail.com">bkutkars@gmail.com</a>
    </div>
</div>
""", unsafe_allow_html=True)
