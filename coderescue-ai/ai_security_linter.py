import ast
import re
import math

GENERIC_AI_NAMES = {
    "data", "data_list", "result", "result_list", "results", "item", "items",
    "item_list", "temp", "temp_val", "temp_data", "input_data", "output_data",
    "output_dict", "res", "ans", "dummy", "sample_data", "user_input", "temp_list",
    "final_result", "obj_list", "value_list", "processed_data"
}

AI_COMMENT_PATTERNS = [
    re.compile(r"^\s*#\s*(initialize|init)\b", re.IGNORECASE),
    re.compile(r"^\s*#\s*(loop through|iterate through|iterate over|for each)\b", re.IGNORECASE),
    re.compile(r"^\s*#\s*(check if|verify if|validate)\b", re.IGNORECASE),
    re.compile(r"^\s*#\s*(return the|return final|return result)\b", re.IGNORECASE),
    re.compile(r"^\s*#\s*(create a list|create an empty|set up)\b", re.IGNORECASE),
    re.compile(r"^\s*#\s*(import necessary|import required)\b", re.IGNORECASE),
    re.compile(r"^\s*#\s*(handle exceptions|error handling)\b", re.IGNORECASE),
    re.compile(r"^\s*#\s*(print the|output the)\b", re.IGNORECASE),
]

AI_DOCSTRING_PATTERNS = [
    re.compile(r"Parameters:\s*\n", re.IGNORECASE),
    re.compile(r"Args:\s*\n", re.IGNORECASE),
    re.compile(r"Returns:\s*\n", re.IGNORECASE),
    re.compile(r"Raises:\s*\n", re.IGNORECASE),
    re.compile(r"Example:\s*\n", re.IGNORECASE),
]

HALLUCINATED_OR_DEPRECATED_CALLS = {
    ("math", "round"): ("Built-in round()", "math.round() does not exist in Python; use the built-in round(x, n) function."),
    ("json", "loadf"): ("json.load()", "json.loadf() does not exist in standard json library. Use json.load(file_object)."),
    ("json", "loads_file"): ("json.load()", "json.loads_file() is a hallucinated API. Use json.load(file_object)."),
    ("dict", "has_key"): ("'key in dict'", "dict.has_key() was removed in Python 3. Use 'key in dict'."),
    ("list", "contains"): ("'item in list'", "list.contains() does not exist in Python. Use 'item in list'."),
    ("datetime", "to_string"): ("strftime()", ".to_string() does not exist on datetime objects. Use .strftime('%Y-%m-%d').")
}


class AISecurityAuditor(ast.NodeVisitor):
    def __init__(self, source_code):
        self.code = source_code
        self.lines = source_code.splitlines()
        self.total_lines = max(1, len(self.lines))
        
        # Attribution counters
        self.generic_name_count = 0
        self.total_identifiers = 0
        self.ai_comment_lines = set()
        self.docstring_lines = set()
        self.defensive_guard_count = 0
        self.functions = []
        
        # Security & Hallucination issues
        self.vulnerabilities = []
        self.hallucinations = []
        self.performance_issues = []
        
        # Scope tracking
        self.current_function = None

    def audit(self, tree):
        # 1. Text-level comment and docstring analysis
        for idx, line in enumerate(self.lines, start=1):
            stripped = line.strip()
            for pattern in AI_COMMENT_PATTERNS:
                if pattern.search(stripped):
                    self.ai_comment_lines.add(idx)
                    break

        # 2. Walk AST
        self.visit(tree)

        # 3. Compute Granular Line-by-Line Heatmap & Function Attribution
        return self._build_results()

    def visit_FunctionDef(self, node):
        prev_fn = self.current_function
        fn_data = {
            "name": node.name,
            "line": node.lineno,
            "endLine": getattr(node, "end_lineno", node.lineno),
            "generic_names": 0,
            "total_names": 0,
            "has_ai_docstring": False,
            "comment_count": 0,
            "vulnerabilities": 0,
            "defensive_guards": 0,
            "has_chained_regex": False,
        }
        self.current_function = fn_data

        # Check docstring
        docstring = ast.get_docstring(node)
        if docstring:
            doc_lines = len(docstring.splitlines())
            for l_idx in range(node.lineno, min(len(self.lines) + 1, node.lineno + doc_lines + 2)):
                self.docstring_lines.add(l_idx)
            # Check canonical AI structure
            matches = sum(1 for p in AI_DOCSTRING_PATTERNS if p.search(docstring))
            if matches >= 2:
                fn_data["has_ai_docstring"] = True

        self.generic_visit(node)
        self.functions.append(fn_data)
        self.current_function = prev_fn

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_Name(self, node):
        name_lower = node.id.lower()
        self.total_identifiers += 1
        if self.current_function:
            self.current_function["total_names"] += 1

        if name_lower in GENERIC_AI_NAMES:
            self.generic_name_count += 1
            if self.current_function:
                self.current_function["generic_names"] += 1

        self.generic_visit(node)

    def visit_Call(self, node):
        # 1. Security: subprocess with shell=True
        func_name = self._get_call_name(node.func)
        if "subprocess" in func_name or func_name in {"os.system", "os.popen"}:
            for kw in node.keywords:
                if kw.arg == "shell":
                    if isinstance(kw.value, ast.Constant) and bool(kw.value.value) is True:
                        self.vulnerabilities.append({
                            "severity": "CRITICAL",
                            "code": "SEC001",
                            "title": "Command Injection Risk (shell=True)",
                            "line": node.lineno,
                            "offendingLine": self.lines[node.lineno - 1] if node.lineno <= len(self.lines) else "",
                            "message": "Invoking system shells with 'shell=True' allows arbitrary shell command injection if inputs are unvalidated.",
                            "fix": "Set shell=False and pass arguments as an explicit sanitized list: ['cmd', 'arg1', 'arg2']."
                        })
                        if self.current_function:
                            self.current_function["vulnerabilities"] += 1

        # 2. Security: Insecure pickle.loads
        if "pickle.loads" in func_name or "pickle.load" in func_name:
            self.vulnerabilities.append({
                "severity": "HIGH",
                "code": "SEC002",
                "title": "Insecure Deserialization (pickle)",
                "line": node.lineno,
                "offendingLine": self.lines[node.lineno - 1] if node.lineno <= len(self.lines) else "",
                "message": "Deserializing untrusted pickle streams can execute arbitrary code on the host machine.",
                "fix": "Use safe serialized formats like JSON, MessagePack, or Protocol Buffers."
            })
            if self.current_function:
                self.current_function["vulnerabilities"] += 1

        # 3. Security: Weak hashing (MD5 / SHA1)
        if func_name in {"hashlib.md5", "hashlib.sha1"}:
            self.vulnerabilities.append({
                "severity": "MEDIUM",
                "code": "SEC003",
                "title": "Weak Cryptographic Hash",
                "line": node.lineno,
                "offendingLine": self.lines[node.lineno - 1] if node.lineno <= len(self.lines) else "",
                "message": f"'{func_name}' is cryptographically broken and vulnerable to collision attacks.",
                "fix": "Use SHA-256 (hashlib.sha256) or bcrypt/argon2 for passwords and secure tokens."
            })

        # 4. Hallucination check: Known phantom methods
        for (module_part, method_part), (alt, explanation) in HALLUCINATED_OR_DEPRECATED_CALLS.items():
            if method_part in func_name and module_part in func_name:
                self.hallucinations.append({
                    "line": node.lineno,
                    "method": func_name,
                    "title": "Hallucinated or Deprecated API",
                    "offendingLine": self.lines[node.lineno - 1] if node.lineno <= len(self.lines) else "",
                    "message": explanation,
                    "suggestion": f"Replace with {alt}."
                })

        # 5. Hallucination / Fragile AI Pattern: re.search().group() chained without null check
        if isinstance(node.func, ast.Attribute) and node.func.attr == "group":
            if isinstance(node.func.value, ast.Call):
                sub_name = self._get_call_name(node.func.value.func)
                if "re.search" in sub_name or "re.match" in sub_name:
                    self.hallucinations.append({
                        "line": node.lineno,
                        "method": "re.search().group() chaining",
                        "title": "Fragile Regex Match Access (AttributeError)",
                        "offendingLine": self.lines[node.lineno - 1] if node.lineno <= len(self.lines) else "",
                        "message": "Chaining .group() directly on re.search/re.match crashes with AttributeError if no match is found.",
                        "suggestion": "Assign match = re.search(...) first and verify 'if match:' before calling .group()."
                    })
                    if self.current_function:
                        self.current_function["has_chained_regex"] = True

        self.generic_visit(node)

    def visit_Assign(self, node):
        # 1. Security: Hardcoded API keys or Secrets
        for target in node.targets:
            if isinstance(target, ast.Name):
                name = target.id.lower()
                if any(k in name for k in ["api_key", "secret_key", "password", "auth_token", "jwt_secret", "private_key"]):
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        val = node.value.value
                        if len(val) >= 8 and not val.startswith("YOUR_") and not val.startswith("ENV_"):
                            self.vulnerabilities.append({
                                "severity": "HIGH",
                                "code": "SEC004",
                                "title": "Hardcoded Secret / API Key",
                                "line": node.lineno,
                                "offendingLine": self.lines[node.lineno - 1] if node.lineno <= len(self.lines) else "",
                                "message": f"Hardcoded secret detected in variable '{target.id}'. Exposing secrets in code risks credential leakage.",
                                "fix": "Read credentials from environment variables: os.environ.get('API_KEY')."
                            })

        # 2. SQL Injection: string formatting into query
        if isinstance(node.value, ast.JoinedStr):  # f-string
            for part in node.value.values:
                if isinstance(part, ast.Constant) and isinstance(part.value, str):
                    if any(sql in part.value.upper() for sql in ["SELECT ", "INSERT INTO ", "UPDATE ", "DELETE FROM ", "DROP "]):
                        self.vulnerabilities.append({
                            "severity": "CRITICAL",
                            "code": "SEC005",
                            "title": "Potential SQL Injection",
                            "line": node.lineno,
                            "offendingLine": self.lines[node.lineno - 1] if node.lineno <= len(self.lines) else "",
                            "message": "Using f-strings to format SQL queries permits SQL injection attacks.",
                            "fix": "Use parameterized queries: cursor.execute('SELECT * FROM tbl WHERE id = %s', (val,))"
                        })
                        break

        self.generic_visit(node)

    def visit_For(self, node):
        # Performance: range(len(x))
        if isinstance(node.iter, ast.Call):
            func_name = self._get_call_name(node.iter.func)
            if func_name == "range" and len(node.iter.args) == 1:
                arg = node.iter.args[0]
                if isinstance(arg, ast.Call) and self._get_call_name(arg.func) == "len":
                    self.performance_issues.append({
                        "line": node.lineno,
                        "code": "PERF001",
                        "title": "Anti-Pattern: range(len(...))",
                        "offendingLine": self.lines[node.lineno - 1] if node.lineno <= len(self.lines) else "",
                        "message": "Iterating over range(len(collection)) is unidiomatic and slower than direct iteration or enumerate().",
                        "fix": "Use 'for index, item in enumerate(collection):' or loop directly over items."
                    })

        # Performance: Quadratic string concatenation inside loop (s += chunk)
        for child in ast.walk(node):
            if isinstance(child, ast.AugAssign) and isinstance(child.op, ast.Add):
                if isinstance(child.target, ast.Name):
                    self.performance_issues.append({
                        "line": child.lineno,
                        "code": "PERF002",
                        "title": "Quadratic String Concatenation in Loop",
                        "offendingLine": self.lines[child.lineno - 1] if child.lineno <= len(self.lines) else "",
                        "message": "Repeated string concatenation (+=) inside loops causes O(N^2) memory reallocation.",
                        "fix": "Append strings to a list and combine with ''.join(parts) after the loop."
                    })

        self.generic_visit(node)

    def visit_If(self, node):
        # AI defensive guard check: if not isinstance(x, list): raise TypeError(...)
        if isinstance(node.test, ast.UnaryOp) and isinstance(node.test.op, ast.Not):
            if isinstance(node.test.operand, ast.Call):
                f_name = self._get_call_name(node.test.operand.func)
                if f_name == "isinstance":
                    if len(node.body) == 1 and isinstance(node.body[0], ast.Raise):
                        self.defensive_guard_count += 1
                        if self.current_function:
                            self.current_function["defensive_guards"] += 1
        self.generic_visit(node)

    def _get_call_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_call_name(node.value)}.{node.attr}"
        return ""

    def _build_results(self):
        # 1. Overall AI Probability (0 - 100)
        # Multi-factor statistical scoring
        generic_ratio = (self.generic_name_count / max(1, self.total_identifiers))
        ai_comment_ratio = len(self.ai_comment_lines) / self.total_lines
        ai_doc_ratio = len(self.docstring_lines) / self.total_lines

        factors = []
        score = 15  # baseline human code entropy

        if generic_ratio > 0.25:
            delta = min(35, int(generic_ratio * 70))
            score += delta
            factors.append(f"High density of generic identifiers ({self.generic_name_count} matches: data_list, result, etc.) [+{delta}%]")
        elif generic_ratio > 0.10:
            score += 15
            factors.append(f"Generic variable naming patterns detected [+{15}%]")

        if self.ai_comment_lines:
            delta = min(25, len(self.ai_comment_lines) * 8)
            score += delta
            factors.append(f"Step-by-step canonical LLM commentary patterns [+{delta}%]")

        if self.docstring_lines:
            has_sphinx = any(fn.get("has_ai_docstring") for fn in self.functions)
            if has_sphinx:
                score += 20
                factors.append("Formal canonical LLM docstring formatting (Parameters/Returns boilerplate) [+20%]")

        if self.defensive_guard_count >= 1:
            score += 10
            factors.append("Generic defensive guard clauses (isinstance checks) [+10%]")

        if any(fn.get("has_chained_regex") for fn in self.functions):
            score += 10
            factors.append("Chained regex without null validation (common AI hallucination pattern) [+10%]")

        overall_prob = max(5, min(96, score))

        classification = (
            "High Probability AI-Generated Boilerplate" if overall_prob >= 70
            else "Mixed / AI-Assisted Implementation" if overall_prob >= 40
            else "Human-Authored Logic"
        )

        # 2. Granular Line-by-Line Heatmap
        line_heatmap = []
        for line_num in range(1, self.total_lines + 1):
            line_str = self.lines[line_num - 1] if line_num - 1 < len(self.lines) else ""
            line_score = overall_prob
            line_factors = []

            # Determine line-level influences
            if line_num in self.ai_comment_lines:
                line_score = min(98, overall_prob + 30)
                line_factors.append("Canonical step-by-step AI comment")
            elif line_num in self.docstring_lines:
                line_score = min(95, overall_prob + 20)
                line_factors.append("AI docstring structure")
            elif any(w in line_str for w in GENERIC_AI_NAMES):
                line_score = min(90, overall_prob + 15)
                line_factors.append("Generic variable naming")
            else:
                # Normal code line
                line_score = max(10, overall_prob - 10)

            # Check if this line has a vulnerability or hallucination
            vuln_here = [v for v in self.vulnerabilities if v.get("line") == line_num]
            if vuln_here:
                line_score = min(99, line_score + 15)
                line_factors.append(f"Security Risk: {vuln_here[0]['title']}")

            halluc_here = [h for h in self.hallucinations if h.get("line") == line_num]
            if halluc_here:
                line_score = min(99, line_score + 15)
                line_factors.append(f"Hallucination: {halluc_here[0]['title']}")

            line_class = (
                "ai" if line_score >= 70
                else "assisted" if line_score >= 40
                else "human"
            )

            line_heatmap.append({
                "line": line_num,
                "code": line_str,
                "probability": line_score,
                "classification": line_class,
                "factors": line_factors or ["Standard procedural context"]
            })

        # 3. Function Breakdown
        func_summary = []
        for fn in self.functions:
            fn_score = overall_prob
            fn_factors = []
            if fn.get("has_ai_docstring"):
                fn_score += 15
                fn_factors.append("Structured LLM docstring")
            if fn.get("generic_names", 0) >= 2:
                fn_score += 15
                fn_factors.append(f"{fn['generic_names']} generic variables")
            if fn.get("vulnerabilities", 0) > 0:
                fn_score += 10
                fn_factors.append("Contains unreviewed security vulnerability")

            fn_score = max(5, min(95, fn_score))
            verdict = (
                "AI-Generated" if fn_score >= 70
                else "AI-Assisted" if fn_score >= 40
                else "Human-Authored"
            )

            func_summary.append({
                "name": fn["name"],
                "startLine": fn["line"],
                "endLine": fn["endLine"],
                "aiProbability": fn_score,
                "verdict": verdict,
                "reasons": fn_factors or ["Domain specific logic"]
            })

        # 4. Generate Human-Refactored Fix
        human_refactored = self._generate_human_refactor()

        # 5. Simulated GitHub Action PR comment
        total_risks = len(self.vulnerabilities)
        total_perf = len(self.performance_issues)
        risk_str = f" ({total_risks} security risk{'s' if total_risks != 1 else ''}, {total_perf} performance issue{'s' if total_perf != 1 else ''})" if (total_risks or total_perf) else ""

        pr_comment = (
            f"⚠️ **CodeRescue AI Audit**: Warning: **{overall_prob}% probability of unreviewed AI-generated boilerplate detected**{risk_str}.\n\n"
            f"- **Attribution Verdict**: {classification}\n"
            f"- **Key Indicators**: {', '.join(factors[:3]) if factors else 'Standard structure'}\n"
            f"- **Security Vulnerabilities**: {total_risks} detected\n"
            f"- **Performance Bottlenecks**: {total_perf} detected\n\n"
            f"> *Action Recommended*: Review granular heatmap and verify highlighted security issues before merging."
        )

        return {
            "overallProbability": overall_prob,
            "classification": classification,
            "attributionFactors": factors,
            "lineHeatmap": line_heatmap,
            "functionBreakdown": func_summary,
            "vulnerabilities": self.vulnerabilities,
            "hallucinations": self.hallucinations,
            "performanceBottlenecks": self.performance_issues,
            "humanRefactoredCode": human_refactored,
            "githubActionComment": pr_comment
        }

    def _generate_human_refactor(self):
        """Generates an idiomatic, human-crafted refactored version of the code."""
        lines = list(self.lines)
        modified = False

        # Fix shell=True
        for idx, l in enumerate(lines):
            if "shell=True" in l:
                lines[idx] = l.replace("shell=True", "shell=False")
                modified = True
            if "hashlib.md5(" in l:
                lines[idx] = l.replace("hashlib.md5(", "hashlib.sha256(")
                modified = True
            if "dict.has_key(" in l:
                lines[idx] = re.sub(r'(\w+)\.has_key\((\w+)\)', r'\2 in \1', l)
                modified = True
            if "math.round(" in l:
                lines[idx] = l.replace("math.round(", "round(")
                modified = True

        return "\n".join(lines) if modified else None


def audit_ai_code(source_code):
    try:
        tree = ast.parse(source_code)
    except Exception:
        # If syntax fails, return basic scan
        return {
            "overallProbability": 50,
            "classification": "Syntax Incomplete",
            "attributionFactors": ["Code contains syntax errors; static attribution estimated"],
            "lineHeatmap": [],
            "functionBreakdown": [],
            "vulnerabilities": [],
            "hallucinations": [],
            "performanceBottlenecks": [],
            "humanRefactoredCode": None,
            "githubActionComment": "⚠️ CodeRescue AI: Syntax errors prevent full security audit."
        }

    auditor = AISecurityAuditor(source_code)
    return auditor.audit(tree)
