import os
import shutil
import time
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

BRAIN_DIR = r"C:\Users\bkutk\.gemini\antigravity\brain\01eb1445-3678-4171-8288-318626c82406"
TARGET_DIR = r"C:\Users\bkutk\OneDrive\Desktop\codesource-1\coderescue-ai\media"
IMAGES_DIR = os.path.join(TARGET_DIR, "images")

os.makedirs(IMAGES_DIR, exist_ok=True)

# 1. Map existing 13 images
IMAGE_MAPPING = {
    "01_project_overview_banner.jpg": "coderescue_ai_banner_1792382949123.jpg",
    "02_user_avatar_auth_system.jpg": "coderescue_auth_avatar_system_1792383085337.jpg",
    "03_100_dsa_placement_arena.jpg": "coderescue_ai_dsa_arena_1792383087351.jpg",
    "04_submillisecond_code_judge.jpg": "coderescue_ai_dsa_judge_1792383087200.jpg",
    "05_ast_complexity_profiler.jpg": "coderescue_ai_complexity_profiler_png_1792383086850.jpg",
    "06_ast_syntax_error_engine.jpg": "coderescue_ai_ast_diagnostic_engine_1792383099954.jpg",
    "07_scope_name_error_resolver.jpg": "coderescue_scope_resolution_1792383096914.jpg",
    "08_mutable_default_arg_linter.jpg": "coderescue_anti_pattern_linter_1792383097532.jpg",
    "09_ai_attribution_heatmap.jpg": "code_rescue_ai_attribution_heatmap_1792383098911.jpg",
    "10_security_vulnerability_scanner.jpg": "coderescue_ai_security_scanner_1792383108489.jpg",
    "11_hallucinated_api_detector.jpg": "coderescue_ai_detector_1792383153960.jpg",
    "13_github_actions_pr_bot.jpg": "coderescue_ai_pr_bot_1792383116188.jpg",
    "14_accuracy_progress_analytics.jpg": "coderescue_ai_analytics_dashboard_1792383110566.jpg"
}

print("1. Copying generated AI images into media folder...")
for dest_name, src_name in IMAGE_MAPPING.items():
    src_path = os.path.join(BRAIN_DIR, src_name)
    dest_path = os.path.join(IMAGES_DIR, dest_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"  [OK] Copied {dest_name}")
    else:
        print(f"  [WARN] Source not found: {src_path}")

# 2. Render Image 12: Human-Refactored Fix Engine (high-res 16:9 1280x720)
print("2. Generating Image 12: Human-Refactored Fix Engine...")
img12_path = os.path.join(IMAGES_DIR, "12_human_refactored_fix_engine.png")

w, h = 1280, 720
img12 = Image.new("RGB", (w, h), color=(13, 17, 23))
draw12 = ImageDraw.Draw(img12)

# Background gradient
for y in range(h):
    r = int(10 + (25 - 10) * (y / h))
    g = int(14 + (27 - 14) * (y / h))
    b = int(24 + (45 - 24) * (y / h))
    draw12.line([(0, y), (w, y)], fill=(r, g, b))

# Header Banner
draw12.rectangle([(40, 30), (w - 40, 95)], fill=(22, 27, 34), outline=(48, 54, 61), width=2)
draw12.text((60, 48), "CodeRescue AI — Automated Human-Refactored Fix Engine", fill=(56, 189, 248))
draw12.text((w - 380, 52), "[DIFF REPAIR: VERIFIED SECURE]", fill=(34, 197, 94))

# Left Box: Bloated Vulnerable AI Code
draw12.rectangle([(40, 115), (590, 620)], fill=(18, 20, 26), outline=(239, 68, 68), width=2)
draw12.rectangle([(40, 115), (590, 160)], fill=(45, 15, 20))
draw12.text((60, 128), "[-] VULNERABLE AI BOILERPLATE (Pre-Refactor)", fill=(248, 113, 113))

left_code = [
    "# AI Generated Boilerplate with Flaws",
    "import subprocess",
    "import hashlib",
    "import math",
    "",
    "def process_data(items=[]):  # W001: Mutable Default",
    "    results = []",
    "    for i in range(len(items)):",
    "        val = math.round(items[i]) # Hallucinated API!",
    "        results.append(val)",
    "",
    "    # CWE-78: Dangerous shell injection",
    "    subprocess.run('echo ' + str(results), shell=True)",
    "",
    "    # CWE-327: Insecure weak hashing",
    "    token = hashlib.md5(b'user').hexdigest()",
    "    return results"
]
for idx, line in enumerate(left_code):
    color = (248, 113, 113) if "W001" in line or "CWE" in line or "shell=True" in line or "round(" in line else (148, 163, 184)
    draw12.text((60, 180 + idx * 24), line, fill=color)

# Center Bridge: Glowing Transformation Streams
draw12.line([(600, 360), (680, 360)], fill=(56, 189, 248), width=4)
draw12.polygon([(670, 350), (690, 360), (670, 370)], fill=(56, 189, 248))
draw12.text((610, 325), "AUTO-FIX", fill=(56, 189, 248))

# Right Box: Clean Idiomatic Human Code
draw12.rectangle([(690, 115), (1240, 620)], fill=(18, 26, 22), outline=(34, 197, 94), width=2)
draw12.rectangle([(690, 115), (1240, 160)], fill=(15, 45, 25))
draw12.text((710, 128), "[+] IDIOMATIC SECURE REFACTOR (CodeRescue AI Output)", fill=(74, 222, 128))

right_code = [
    "# Production-Grade Human Refactored",
    "import subprocess",
    "import hashlib",
    "from typing import Optional, List",
    "",
    "def process_data(items: Optional[List[float]] = None) -> List[int]:",
    "    if items is None:",
    "        items = []  # Fixed: Safe None initialization",
    "    ",
    "    # Fixed: Built-in round & list comprehension O(N)",
    "    results = [round(item) for item in items if item is not None]",
    "",
    "    # Fixed: shell=False prevents command injection",
    "    subprocess.run(['echo', str(results)], shell=False, check=True)",
    "",
    "    # Fixed: SHA-256 military-grade hashing",
    "    token = hashlib.sha256(b'user').hexdigest()",
    "    return results"
]
for idx, line in enumerate(right_code):
    color = (74, 222, 128) if "Fixed:" in line or "Optional" in line or "sha256" in line else (203, 213, 225)
    draw12.text((710, 180 + idx * 24), line, fill=color)

# Footer bar
draw12.rectangle([(40, 640), (w - 40, 690)], fill=(15, 23, 42), outline=(30, 41, 59))
draw12.text((60, 655), "Detector: coderescue-ai | Contact: bkutkars@gmail.com | 1-Click Code Modernization", fill=(148, 163, 184))
img12.save(img12_path)
print(f"  [OK] Saved Image 12: {img12_path}")

# Also copy Image 12 to brain directory for artifact consistency
shutil.copy2(img12_path, os.path.join(BRAIN_DIR, "12_human_refactored_fix_engine.png"))

# 3. BUILD COMPLETE EXPLANATION VIDEO
print("3. Synthesizing High-Definition Walkthrough Video (1280x720)...")
video_output_path = os.path.join(TARGET_DIR, "coderescue_explanation_walkthrough.mp4")

SCENES = [
    {
        "title": "Welcome to CodeRescue AI",
        "subtitle": "Real Python AST Error Detector, Placement DSA Arena & Security Linter",
        "image": "01_project_overview_banner.jpg",
        "bullets": [
            "100% Real Python AST static inspection & live runtime sandbox (zero mock)",
            "100-Question Python DSA Placement Arena with FAANG interview tagging",
            "Granular line-by-line AI attribution heatmap & OWASP security vulnerability scanner",
            "Fullstack deployment: Express backend (5000), Vite frontend (5173), Streamlit (8501)"
        ]
    },
    {
        "title": "Feature 01: Deterministic Avatar & Authentication",
        "subtitle": "Cryptographic SVG avatar generation from email hash with instant signup alerts",
        "image": "02_user_avatar_auth_system.jpg",
        "bullets": [
            "Zero external avatar API latency: Pure Python/JS deterministic color palette generation",
            "Unique biometric-inspired initials & gradient rings personalized to user email",
            "Signup notification dispatch to admin mentor (bkutkars@gmail.com)",
            "Persistent profile tracking with placement readiness score"
        ]
    },
    {
        "title": "Feature 02: 100 Python DSA Placement Arena",
        "subtitle": "Curated technical interview curriculum: 50 Easy, 30 Medium, 20 Hard problems",
        "image": "03_100_dsa_placement_arena.jpg",
        "bullets": [
            "Structured for LeetCode & Codeforces tier placement and internship readiness",
            "Categorized into Arrays, Two Pointers, Trees, Graphs, DP, Sliding Window & Greedy",
            "Tagged by top hiring companies: Google, Meta, Amazon, Microsoft, Apple, Uber",
            "Interactive starter code pre-loader and test case descriptions"
        ]
    },
    {
        "title": "Feature 03: Sub-Millisecond Code Judge",
        "subtitle": "High-performance Python test runner evaluating solutions in < 1 ms",
        "image": "04_submillisecond_code_judge.jpg",
        "bullets": [
            "Executes user Python functions in isolated, secure execution scope",
            "Robust deep-equality evaluation supporting nested structures, floats, and sets",
            "Instant feedback on sample tests vs. full comprehensive submission test cases",
            "Detailed test breakdown cards displaying inputs, expected vs actual outputs"
        ]
    },
    {
        "title": "Feature 04: AST Big-O Complexity Profiler",
        "subtitle": "Automated algorithmic interview advisor calculating Time & Space complexity",
        "image": "05_ast_complexity_profiler.jpg",
        "bullets": [
            "Parses loop nesting depth to identify O(N), O(N^2), and O(N^3) time complexities",
            "Detects recursion trees, sorting calls, and heap operations automatically",
            "Computes auxiliary space requirements (O(1) in-place vs O(N) hash table)",
            "Offers actionable technical interview tips for optimizing nested loops"
        ]
    },
    {
        "title": "Feature 05: AST Syntax Error Diagnostic Engine",
        "subtitle": "Pinpoints exact line and column numbers for syntax and formatting defects",
        "image": "06_ast_syntax_error_engine.jpg",
        "bullets": [
            "Diagnoses missing colons, unbalanced parentheses, and invalid tokens",
            "Translates cryptic Python exceptions into human-friendly explanations",
            "Visual code pointers showing exact error offset within the line",
            "Generates 1-click automated syntax repair suggestions"
        ]
    },
    {
        "title": "Feature 06: Lexical Scope & NameError Resolver",
        "subtitle": "Tracks Python LEGB scope hierarchy to catch undefined names and typos",
        "image": "07_scope_name_error_resolver.jpg",
        "bullets": [
            "Inspects symbol tables across Local, Enclosing, Global, and Builtin scopes",
            "Identifies variable typos before code execution even starts",
            "Flags missing imports (e.g., using 'math' without 'import math')",
            "Recommends closest matching defined identifiers in scope"
        ]
    },
    {
        "title": "Feature 07: Python Anti-Pattern Linter (W001)",
        "subtitle": "Detects mutable default arguments and subtle memory-sharing traps",
        "image": "08_mutable_default_arg_linter.jpg",
        "bullets": [
            "Flags dangerous function signatures like 'def append_item(val, container=[])'",
            "Explains why mutable defaults persist across repeated function calls",
            "Automatically generates the idiomatic 'container = None' fix",
            "Improves Python code quality according to PEP 8 standards"
        ]
    },
    {
        "title": "Feature 08: Granular AI Attribution Heatmap",
        "subtitle": "Line-by-line classification of AI boilerplate vs. human-authored code",
        "image": "09_ai_attribution_heatmap.jpg",
        "bullets": [
            "Evaluates code structure, repetitive comment patterns, and generic identifier names",
            "Calculates an overall AI boilerplate probability score (0% - 100%)",
            "Renders a visual color-coded heatmap (Red for AI boilerplate, Green for Human logic)",
            "Provides function-by-function breakdown of machine generation probability"
        ]
    },
    {
        "title": "Feature 09: Security Vulnerability Scanner",
        "subtitle": "Automated OWASP & CWE security audit for common AI-generated risks",
        "image": "10_security_vulnerability_scanner.jpg",
        "bullets": [
            "Detects dangerous 'subprocess(shell=True)' command injection (CWE-78)",
            "Identifies raw SQL injection strings and unparameterized queries (CWE-89)",
            "Flags outdated, broken cryptographic algorithms like MD5 & SHA-1 (CWE-327)",
            "Provides actionable mitigation instructions for every vulnerability"
        ]
    },
    {
        "title": "Feature 10: Hallucinated & Deprecated API Detector",
        "subtitle": "Catches non-existent functions commonly hallucinated by Large Language Models",
        "image": "11_hallucinated_api_detector.jpg",
        "bullets": [
            "Catches fake APIs like 'math.round()' (should be built-in 'round()')",
            "Catches deprecated Python 2 methods like 'dict.has_key()' (use 'key in dict')",
            "Catches non-existent methods like 'list.contains()' or 'json.loads_file()'",
            "Directly links to standard library equivalents"
        ]
    },
    {
        "title": "Feature 11: Automated Human-Refactored Fix Engine",
        "subtitle": "Transforms bloated, insecure AI code into clean, secure, idiomatic Python",
        "image": "12_human_refactored_fix_engine.png",
        "bullets": [
            "Replaces shell=True with safe parameter arrays and checks",
            "Upgrades weak cryptography to military-grade SHA-256 hashing",
            "Fixes hallucinated APIs and converts clumsy loops into clean list comprehensions",
            "Displays side-by-side diff comparison ready for immediate copying"
        ]
    },
    {
        "title": "Feature 12: Automated GitHub Actions PR Review Bot",
        "subtitle": "Simulated CI/CD bot posting automated pull request security and boilerplate reviews",
        "image": "13_github_actions_pr_bot.jpg",
        "bullets": [
            "Calculates overall AI boilerplate probability for open Pull Requests",
            "Summarizes detected security vulnerabilities and performance bottlenecks",
            "Provides copy-pasteable Markdown PR comments for team workflows",
            "Integrates directly into GitHub Actions CI pipelines"
        ]
    },
    {
        "title": "Feature 13: Accuracy & Progress Analytics",
        "subtitle": "Real-time time-series graph tracking code accuracy and placement skill growth",
        "image": "14_accuracy_progress_analytics.jpg",
        "bullets": [
            "Graphs accuracy percentage over consecutive code runs and DSA submissions",
            "Calculates historical average accuracy, total evaluations, and pass rate",
            "Displays DSA topic coverage bar charts across algorithmic domains",
            "Placement Readiness radial gauge estimating interview readiness"
        ]
    },
    {
        "title": "CodeRescue AI — Built by bkutkars@gmail.com",
        "subtitle": "Engine: coderescue-ai • Ready for Native Web & Streamlit Cloud",
        "image": "01_project_overview_banner.jpg",
        "bullets": [
            "Spacebar Attribution: Detector 'coderescue-ai' • Contact: bkutkars@gmail.com",
            "Full React Frontend running on http://localhost:5173",
            "Full Express Backend running on http://localhost:5000",
            "Streamlit Cloud Application running on http://localhost:8501",
            "Questions or mentoring? Message: bkutkars@gmail.com"
        ]
    }
]

FPS = 24
SECONDS_PER_SCENE = 3
FRAMES_PER_SCENE = FPS * SECONDS_PER_SCENE

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(video_output_path, fourcc, float(FPS), (w, h))

total_scenes = len(SCENES)
total_frames = total_scenes * FRAMES_PER_SCENE
current_frame_idx = 0

print(f"Rendering {total_scenes} scenes ({total_frames} frames total)...")

for s_idx, scene in enumerate(SCENES):
    img_filename = scene["image"]
    img_path = os.path.join(IMAGES_DIR, img_filename)
    
    # Load feature artwork
    if os.path.exists(img_path):
        raw_feat_img = Image.open(img_path).convert("RGB")
    else:
        raw_feat_img = Image.new("RGB", (560, 315), color=(30, 41, 59))
        
    feat_img = raw_feat_img.resize((560, 315), Image.Resampling.LANCZOS)
    
    # Render base frame
    for f_idx in range(FRAMES_PER_SCENE):
        frame_pil = Image.new("RGB", (w, h), color=(10, 14, 23))
        d = ImageDraw.Draw(frame_pil)
        
        # Subtle gradient
        for y in range(0, h, 4):
            val = int(12 + 10 * (y / h))
            d.rectangle([(0, y), (w, y+4)], fill=(val, val+4, val+14))
            
        # Top Header Bar
        d.rectangle([(30, 20), (w - 30, 85)], fill=(15, 23, 42), outline=(51, 65, 85), width=2)
        d.text((50, 35), f"CODERESCUE AI WALKTHROUGH — [{s_idx+1}/{total_scenes}]", fill=(56, 189, 248))
        d.text((50, 58), scene["title"].upper(), fill=(255, 255, 255))
        d.text((w - 340, 45), "ENGINE: coderescue-ai", fill=(148, 163, 184))

        # Paste Feature Artwork (Left pane)
        frame_pil.paste(feat_img, (40, 115))
        d.rectangle([(40, 115), (600, 430)], outline=(56, 189, 248), width=2)
        
        # Subtitle badge under image
        d.rectangle([(40, 445), (600, 500)], fill=(22, 27, 34), outline=(48, 54, 61))
        d.text((55, 462), scene["subtitle"][:70], fill=(203, 213, 225))
        if len(scene["subtitle"]) > 70:
            d.text((55, 480), scene["subtitle"][70:], fill=(148, 163, 184))

        # Right Card: Bullet points explanation
        d.rectangle([(630, 115), (w - 40, 620)], fill=(18, 24, 38), outline=(99, 102, 241), width=2)
        d.rectangle([(630, 115), (w - 40, 165)], fill=(30, 27, 75))
        d.text((650, 130), "SYSTEM MECHANISM & ARCHITECTURE", fill=(167, 139, 250))

        # Bullets
        for b_idx, bullet in enumerate(scene["bullets"]):
            y_pos = 185 + b_idx * 100
            d.ellipse([(655, y_pos + 6), (665, y_pos + 16)], fill=(56, 189, 248))
            
            # Word wrap bullet
            words = bullet.split()
            line1, line2 = "", ""
            for word in words:
                if len(line1) + len(word) < 48:
                    line1 += word + " "
                else:
                    line2 += word + " "
                    
            d.text((680, y_pos), line1, fill=(241, 245, 249))
            if line2:
                d.text((680, y_pos + 22), line2, fill=(148, 163, 184))

        # Bottom Spacebar Attribution
        d.rectangle([(0, 645), (w, h)], fill=(7, 10, 19))
        d.line([(0, 645), (w, 645)], fill=(99, 102, 241), width=2)
        
        # Spacebar elements
        d.rectangle([(40, 660), (180, 695)], fill=(79, 70, 229))
        d.text((52, 672), "coderescue-ai", fill=(255, 255, 255))
        d.text((200, 672), "Real Python AST Error Detector & 100 DSA Arena", fill=(203, 213, 225))
        
        # Email attribution
        d.text((w - 460, 672), "Found difficult? Message: bkutkars@gmail.com", fill=(56, 189, 248))

        # Animated progress bar
        progress = current_frame_idx / float(total_frames)
        d.rectangle([(0, 714), (int(w * progress), 720)], fill=(56, 189, 248))

        # Convert PIL to OpenCV BGR
        frame_cv = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
        out.write(frame_cv)
        current_frame_idx += 1

out.release()
print(f"  [OK] Video generated successfully at: {video_output_path}")

# Copy video to brain artifact dir
shutil.copy2(video_output_path, os.path.join(BRAIN_DIR, "coderescue_explanation_walkthrough.mp4"))
print("Done creating all media assets!")
