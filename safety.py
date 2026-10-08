"""Static safety check for student hero files.

Best effort for a classroom, NOT a perfect sandbox: heroes may only import a
few harmless modules and may not use file/eval/introspection tricks.
Used by match.py (so the server AND check_hero.py both apply it)."""
import ast

ALLOWED_IMPORTS = {"base", "random", "math", "itertools", "functools", "collections",
                   "typing", "dataclasses", "enum", "statistics"}
BANNED_NAMES = {"open", "eval", "exec", "compile", "getattr", "setattr", "delattr", "globals",
                "locals", "vars", "dir", "input", "breakpoint", "exit", "quit", "help", "memoryview"}
BANNED_ATTRS = {"f_globals", "f_locals", "f_back", "f_builtins", "f_code", "gi_frame", "gi_code",
                "cr_frame", "tb_frame", "tb_next", "func_globals", "mro"}


def check_source(source):
    """Return a list of problems (empty list = file is allowed)."""
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return [f"line {e.lineno}: SyntaxError: {e.msg}"]
    except (ValueError, RecursionError, MemoryError):
        return ["the file cannot be read as Python code"]
    problems = []
    ok_list = ", ".join(sorted(ALLOWED_IMPORTS))
    for node in ast.walk(tree):
        line = getattr(node, "lineno", "?")
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] not in ALLOWED_IMPORTS:
                    problems.append(f"line {line}: import '{a.name}' is not allowed (allowed: {ok_list})")
        elif isinstance(node, ast.ImportFrom):
            if node.level or (node.module or "").split(".")[0] not in ALLOWED_IMPORTS:
                problems.append(f"line {line}: import from '{node.module}' is not allowed (allowed: {ok_list})")
        elif isinstance(node, ast.Attribute):
            dunder = node.attr.startswith("__") and node.attr.endswith("__") and node.attr != "__init__"
            if dunder or node.attr in BANNED_ATTRS:
                problems.append(f"line {line}: '.{node.attr}' is not allowed")
        elif isinstance(node, ast.Name):
            if node.id in BANNED_NAMES or (node.id.startswith("__") and node.id.endswith("__")):
                problems.append(f"line {line}: '{node.id}' is not allowed")
        elif isinstance(node, ast.Constant) and isinstance(node.value, str) and "__" in node.value:
            problems.append(f"line {line}: text containing '__' is not allowed")
    return problems
