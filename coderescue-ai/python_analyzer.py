import sys
import os
import ast
import json
import builtins
import subprocess
import traceback
import tempfile
import re
from ai_security_linter import audit_ai_code

BUILTIN_NAMES = set(dir(builtins))

class PythonCodeInspector(ast.NodeVisitor):
    def __init__(self, source_code):
        self.source_code = source_code
        self.lines = source_code.splitlines()
        self.issues = []
        # Stack of scopes for name resolution
        self.scopes = [set(BUILTIN_NAMES)]
        # Track imported names
        self.imported_names = set()

    def current_scope(self):
        return self.scopes[-1]

    def add_issue(self, severity, line, col, end_line, end_col, code, title, message, suggestion=None, fix_patch=None):
        self.issues.append({
            "severity": severity,  # "error", "warning", "info"
            "line": max(1, line or 1),
            "column": max(1, col or 1),
            "endLine": max(1, end_line or line or 1),
            "endColumn": max(1, end_col or col or 1),
            "code": code,
            "title": title,
            "message": message,
            "suggestion": suggestion,
            "fixPatch": fix_patch
        })

    def visit_FunctionDef(self, node):
        # Register function name in current scope
        self.current_scope().add(node.name)

        # Check mutable default arguments: def foo(x=[])
        for default in node.args.defaults + node.args.kw_defaults:
            if default is not None and isinstance(default, (ast.List, ast.Dict, ast.Set)):
                type_name = type(default).__name__.lower()
                self.add_issue(
                    severity="warning",
                    line=default.lineno,
                    col=default.col_offset + 1,
                    end_line=getattr(default, 'end_lineno', default.lineno),
                    end_col=getattr(default, 'end_col_offset', default.col_offset + 1),
                    code="W001",
                    title="Mutable Default Argument",
                    message=f"Default argument is a mutable {type_name}. It is evaluated once and shared across all calls.",
                    suggestion=f"Use 'None' as the default and initialize '{type_name}()' inside the function."
                )

        # Check function name vs operation heuristics (e.g. def add(a, b): return a - b)
        fn_name = node.name.lower()
        if "add" in fn_name or "sum" in fn_name:
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.BinOp) and isinstance(sub_node.op, ast.Sub):
                    self.add_issue(
                        severity="warning",
                        line=sub_node.lineno,
                        col=sub_node.col_offset + 1,
                        end_line=getattr(sub_node, 'end_lineno', sub_node.lineno),
                        end_col=getattr(sub_node, 'end_col_offset', sub_node.col_offset + 1),
                        code="L001",
                        title="Logic Inconsistency",
                        message=f"Function is named '{node.name}', but uses subtraction ('-') in its body.",
                        suggestion="Did you mean to use addition ('+') instead of '-'?"
                    )
        elif "sub" in fn_name or "minus" in fn_name or "diff" in fn_name:
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.BinOp) and isinstance(sub_node.op, ast.Add):
                    self.add_issue(
                        severity="warning",
                        line=sub_node.lineno,
                        col=sub_node.col_offset + 1,
                        end_line=getattr(sub_node, 'end_lineno', sub_node.lineno),
                        end_col=getattr(sub_node, 'end_col_offset', sub_node.col_offset + 1),
                        code="L002",
                        title="Logic Inconsistency",
                        message=f"Function is named '{node.name}', but uses addition ('+') in its body.",
                        suggestion="Did you mean to use subtraction ('-') instead of '+'?"
                    )

        # Check unreachable code after return or raise
        returned = False
        for stmt in node.body:
            if returned:
                self.add_issue(
                    severity="warning",
                    line=stmt.lineno,
                    col=stmt.col_offset + 1,
                    end_line=getattr(stmt, 'end_lineno', stmt.lineno),
                    end_col=getattr(stmt, 'end_col_offset', stmt.col_offset + 1),
                    code="W002",
                    title="Unreachable Code",
                    message="This statement cannot be reached because the previous line returns or raises an error.",
                    suggestion="Remove or reposition code after return or raise."
                )
                break
            if isinstance(stmt, (ast.Return, ast.Raise)):
                returned = True

        # Create new scope for function arguments and body
        fn_scope = set()
        for arg in node.args.args + node.args.posonlyargs + node.args.kwonlyargs:
            fn_scope.add(arg.arg)
        if node.args.vararg:
            fn_scope.add(node.args.vararg.arg)
        if node.args.kwarg:
            fn_scope.add(node.args.kwarg.arg)

        self.scopes.append(fn_scope)
        self.generic_visit(node)
        self.scopes.pop()

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        self.current_scope().add(node.name)
        class_scope = set()
        self.scopes.append(class_scope)
        self.generic_visit(node)
        self.scopes.pop()

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname or alias.name.split('.')[0]
            self.current_scope().add(name)
            self.imported_names.add(name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            name = alias.asname or alias.name
            self.current_scope().add(name)
            self.imported_names.add(name)
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            for sub in ast.walk(target):
                if isinstance(sub, ast.Name):
                    self.current_scope().add(sub.id)
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        if isinstance(node.target, ast.Name):
            self.current_scope().add(node.target.id)
        self.generic_visit(node)

    def visit_For(self, node):
        for sub in ast.walk(node.target):
            if isinstance(sub, ast.Name):
                self.current_scope().add(sub.id)
        self.generic_visit(node)

    def visit_ListComp(self, node):
        comp_scope = set()
        for gen in node.generators:
            for sub in ast.walk(gen.target):
                if isinstance(sub, ast.Name):
                    comp_scope.add(sub.id)
        self.scopes.append(comp_scope)
        self.generic_visit(node)
        self.scopes.pop()

    def visit_DictComp(self, node):
        self.visit_ListComp(node)

    def visit_SetComp(self, node):
        self.visit_ListComp(node)

    def visit_Compare(self, node):
        # Check comparison with literals using `is`
        for op, comparator in zip(node.ops, node.comparators):
            if isinstance(op, (ast.Is, ast.IsNot)):
                if isinstance(comparator, (ast.Constant, ast.Num, ast.Str)):
                    val = getattr(comparator, 'value', None)
                    if val is not None and val is not True and val is not False:
                        self.add_issue(
                            severity="warning",
                            line=node.lineno,
                            col=node.col_offset + 1,
                            end_line=getattr(node, 'end_lineno', node.lineno),
                            end_col=getattr(node, 'end_col_offset', node.col_offset + 1),
                            code="W003",
                            title="Comparison to Literal via 'is'",
                            message="'is' checks identity in memory, not value equality. Literals should use '==' or '!='.",
                            suggestion="Use '==' or '!=' instead of 'is'."
                        )
            elif isinstance(op, (ast.Eq, ast.NotEq)):
                if isinstance(comparator, ast.Constant) and comparator.value is None:
                    self.add_issue(
                        severity="info",
                        line=node.lineno,
                        col=node.col_offset + 1,
                        end_line=getattr(node, 'end_lineno', node.lineno),
                        end_col=getattr(node, 'end_col_offset', node.col_offset + 1),
                        code="H001",
                        title="Idiomatic None Check",
                        message="Comparing with '== None' is discouraged in Python (PEP 8).",
                        suggestion="Use 'is None' or 'is not None'."
                    )

        # Self-comparison: x == x
        if len(node.comparators) == 1 and isinstance(node.left, ast.Name) and isinstance(node.comparators[0], ast.Name):
            if node.left.id == node.comparators[0].id:
                self.add_issue(
                    severity="warning",
                    line=node.lineno,
                    col=node.col_offset + 1,
                    end_line=getattr(node, 'end_lineno', node.lineno),
                    end_col=getattr(node, 'end_col_offset', node.col_offset + 1),
                    code="L003",
                    title="Tautological Comparison",
                    message=f"Variable '{node.left.id}' is compared against itself.",
                    suggestion="Verify if one side was intended to compare with a different variable or value."
                )

        self.generic_visit(node)

    def visit_BinOp(self, node):
        # Division by zero literal
        if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                self.add_issue(
                    severity="error",
                    line=node.lineno,
                    col=node.col_offset + 1,
                    end_line=getattr(node, 'end_lineno', node.lineno),
                    end_col=getattr(node, 'end_col_offset', node.col_offset + 1),
                    code="E001",
                    title="Division by Zero",
                    message="Dividing by literal zero will crash with ZeroDivisionError.",
                    suggestion="Change the divisor to a non-zero value or guard it with a condition."
                )
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if node.type is None:
            self.add_issue(
                severity="warning",
                line=node.lineno,
                col=node.col_offset + 1,
                end_line=getattr(node, 'end_lineno', node.lineno),
                end_col=getattr(node, 'end_col_offset', node.col_offset + 1),
                code="W004",
                title="Bare 'except:' Clause",
                message="A bare 'except:' catches KeyboardInterrupt and SystemExit, preventing clean program termination.",
                suggestion="Use 'except Exception:' instead of bare 'except:'."
            )
        self.generic_visit(node)

    def visit_Name(self, node):
        # Variable name shadowing built-in
        if isinstance(node.ctx, ast.Store):
            if node.id in {"list", "dict", "str", "int", "set", "tuple", "len", "print", "id", "type", "input"}:
                self.add_issue(
                    severity="warning",
                    line=node.lineno,
                    col=node.col_offset + 1,
                    end_line=getattr(node, 'end_lineno', node.lineno),
                    end_col=getattr(node, 'end_col_offset', node.col_offset + 1),
                    code="W005",
                    title="Shadowing Python Built-in",
                    message=f"Variable '{node.id}' overrides Python's built-in '{node.id}'.",
                    suggestion=f"Rename variable to something like '{node.id}_val' or 'my_{node.id}' to avoid collisions."
                )
        elif isinstance(node.ctx, ast.Load):
            # Check if name is defined in any active scope
            is_defined = any(node.id in s for s in reversed(self.scopes))
            if not is_defined:
                self.add_issue(
                    severity="error",
                    line=node.lineno,
                    col=node.col_offset + 1,
                    end_line=getattr(node, 'end_lineno', node.lineno),
                    end_col=getattr(node, 'end_col_offset', node.col_offset + 1),
                    code="E002",
                    title="Undefined Variable (NameError)",
                    message=f"'{node.id}' is used here but is not defined in any enclosing scope.",
                    suggestion=f"Define or initialize '{node.id}' before using it, or verify spelling."
                )
        self.generic_visit(node)


def diagnose_syntax_error(code, err):
    line = err.lineno or 1
    col = err.offset or 1
    msg = str(err.msg)
    lines = code.splitlines()
    error_line = lines[line - 1] if 0 <= line - 1 < len(lines) else ""

    suggestion = "Review Python syntax near this line."
    fix = None

    msg_lower = msg.lower()
    if "expected ':'" in msg_lower or "colon" in msg_lower:
        suggestion = "Add a colon ':' at the end of this statement line."
        if error_line.strip() and not error_line.rstrip().endswith(":"):
            new_lines = list(lines)
            new_lines[line - 1] = error_line.rstrip() + ":"
            fix = "\n".join(new_lines)

    elif "was never closed" in msg_lower or "unclosed" in msg_lower:
        suggestion = f"Check for an unclosed bracket '(', '[', '{{' or unclosed string quote on line {line}."

    elif "unexpected indent" in msg_lower:
        suggestion = "Align the indentation with the preceding code block (recommended: 4 spaces)."

    elif "expected an indented block" in msg_lower:
        suggestion = "Add an indented code block (or 'pass') after this statement."
        new_lines = list(lines)
        indent = " " * (len(error_line) - len(error_line.lstrip()) + 4)
        new_lines.insert(line, indent + "pass")
        fix = "\n".join(new_lines)

    elif "invalid syntax" in msg_lower:
        if error_line.strip().startswith("print ") and "(" not in error_line:
            val = error_line.strip()[6:]
            indent = error_line[:len(error_line) - len(error_line.lstrip())]
            suggestion = "In Python 3, print is a function: use print(...) with parentheses."
            new_lines = list(lines)
            new_lines[line - 1] = f"{indent}print({val})"
            fix = "\n".join(new_lines)
        elif "=" in error_line and any(k in error_line for k in ["if ", "elif ", "while "]) and "==" not in error_line and "!=" not in error_line and "<=" not in error_line and ">=" not in error_line:
            suggestion = "Did you mean '==' for comparison instead of single '=' assignment?"
            new_lines = list(lines)
            new_lines[line - 1] = error_line.replace("=", "==")
            fix = "\n".join(new_lines)

    return {
        "severity": "error",
        "line": line,
        "column": col,
        "endLine": getattr(err, 'end_lineno', line),
        "endColumn": getattr(err, 'end_offset', col),
        "code": "SYNTAX_ERR",
        "title": type(err).__name__,
        "message": msg,
        "offendingLine": error_line,
        "suggestion": suggestion,
        "suggestedCode": fix
    }


def execute_safely(code, timeout=3):
    """Executes python code safely in a separate process with a timeout, capturing stdout & stderr."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    try:
        proc = subprocess.run(
            [sys.executable, "-u", tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=tempfile.gettempdir()
        )
        stdout = proc.stdout
        stderr = proc.stderr
        exit_code = proc.returncode

        runtime_error = None
        if exit_code != 0 and stderr:
            lines = stderr.strip().splitlines()
            err_line_no = None
            err_type = "RuntimeError"
            err_msg = lines[-1] if lines else "Script failed"

            if ":" in lines[-1]:
                err_type, _, detail = lines[-1].partition(":")
                err_type = err_type.strip()
                err_msg = detail.strip()

            for l in reversed(lines):
                if 'File "' in l and ', line ' in l:
                    try:
                        parts = l.split(', line ')
                        err_line_no = int(parts[1].split(',')[0].strip())
                        break
                    except Exception:
                        pass

            runtime_error = {
                "type": err_type,
                "message": err_msg,
                "line": err_line_no,
                "traceback": stderr
            }

        return {
            "success": exit_code == 0,
            "stdout": stdout,
            "stderr": stderr,
            "runtimeError": runtime_error
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Execution timed out after {timeout} seconds (potential infinite loop).",
            "runtimeError": {
                "type": "TimeoutExpired",
                "message": f"Execution timed out after {timeout} seconds. Check for infinite loops (e.g. while without break).",
                "line": None,
                "traceback": f"TimeoutExpired: Process ran longer than {timeout} seconds."
            }
        }
    finally:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass


def generate_smart_fix(code, issues):
    """Produces fixed code if possible based on detected issues."""
    lines = code.splitlines()
    modified = False

    for issue in issues:
        code_id = issue.get("code")
        ln = issue.get("line")
        if not (1 <= ln <= len(lines)):
            continue
        idx = ln - 1

        if code_id == "L001":
            if "-" in lines[idx]:
                lines[idx] = lines[idx].replace("-", "+", 1)
                modified = True
        elif code_id == "L002":
            if "+" in lines[idx]:
                lines[idx] = lines[idx].replace("+", "-", 1)
                modified = True
        elif code_id == "W003":  # x is 'literal' -> x == 'literal'
            lines[idx] = lines[idx].replace(" is ", " == ")
            modified = True
        elif code_id == "H001":  # x == None -> x is None
            lines[idx] = lines[idx].replace(" == None", " is None")
            lines[idx] = lines[idx].replace(" != None", " is not None")
            modified = True
        elif code_id == "W004":  # except: -> except Exception:
            if lines[idx].strip() == "except:":
                indent = lines[idx][:len(lines[idx]) - len(lines[idx].lstrip())]
                lines[idx] = f"{indent}except Exception:"
                modified = True

    if modified:
        return "\n".join(lines)
    return None


def analyze(source_code, execute=True):
    result = {
        "validSyntax": True,
        "syntaxError": None,
        "issues": [],
        "execution": None,
        "suggestedFix": None,
        "stats": {
            "totalLines": len(source_code.splitlines()),
            "charCount": len(source_code),
            "errorCount": 0,
            "warningCount": 0,
            "infoCount": 0
        }
    }

    # 1. AST Syntax Check
    tree = None
    try:
        tree = ast.parse(source_code)
    except (SyntaxError, IndentationError, TabError) as e:
        result["validSyntax"] = False
        syn_err = diagnose_syntax_error(source_code, e)
        result["syntaxError"] = syn_err
        result["issues"].append(syn_err)
        result["stats"]["errorCount"] += 1
        result["suggestedFix"] = syn_err.get("suggestedCode")
        return result

    # 2. Static AST Inspection
    inspector = PythonCodeInspector(source_code)
    inspector.visit(tree)
    result["issues"].extend(inspector.issues)

    # 3. Execution (if syntax is valid and execution requested)
    if execute:
        exec_res = execute_safely(source_code)
        result["execution"] = exec_res
        if exec_res.get("runtimeError"):
            re_err = exec_res["runtimeError"]
            result["issues"].append({
                "severity": "error",
                "line": re_err.get("line") or 1,
                "column": 1,
                "endLine": re_err.get("line") or 1,
                "endColumn": 1,
                "code": "RUNTIME_ERR",
                "title": f"Runtime {re_err['type']}",
                "message": re_err["message"],
                "suggestion": f"Check line {re_err.get('line') or 'in traceback'} where {re_err['type']} was raised.",
                "traceback": re_err.get("traceback")
            })

    # Update counts
    for issue in result["issues"]:
        sev = issue.get("severity")
        if sev == "error":
            result["stats"]["errorCount"] += 1
        elif sev == "warning":
            result["stats"]["warningCount"] += 1
        elif sev == "info":
            result["stats"]["infoCount"] += 1

    # Try generating a fix
    result["suggestedFix"] = generate_smart_fix(source_code, result["issues"])

    # 4. Real AI Attribution, Granular Line Heatmap & Security Audit
    result["aiAttribution"] = audit_ai_code(source_code)

    return result


if __name__ == "__main__":
    execute_flag = "--no-exec" not in sys.argv
    if len(sys.argv) > 1 and sys.argv[1] == "--stdin":
        input_code = sys.stdin.read()
    elif len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            input_code = f.read()
    else:
        input_code = sys.stdin.read()

    analysis = analyze(input_code, execute=execute_flag)
    print(json.dumps(analysis, indent=2))
