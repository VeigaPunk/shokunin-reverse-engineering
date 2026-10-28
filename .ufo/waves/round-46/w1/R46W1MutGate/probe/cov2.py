#!/usr/bin/env python3
"""Executable-line coverage of gate.py, docstring/def artifacts removed.

`sys.settrace` emits no `line` event for a `def` line or a docstring, so a naive
"uncovered = body - hit" overstates the holes. Here the executable line set comes
from the compiled code object (`dis.findlinestarts`, recursively into nested code),
which is exactly what the interpreter can report.
"""
import dis
import hashlib
import importlib.util
import json
import os
import sys

S = os.environ["HYAKU_SCRATCH"]
WHICH = sys.argv[1]
WHICH_TOOL = sys.argv[2]
TOOLS = os.path.join(S, WHICH, "tools", "round-46")
GATE = os.path.join(TOOLS, "gate.py")

sys.path.insert(0, TOOLS)
import gate  # noqa: E402
assert os.path.abspath(gate.__file__) == os.path.abspath(GATE), gate.__file__

spec = importlib.util.spec_from_file_location("cm", os.path.join(TOOLS, WHICH_TOOL + ".py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

exec_lines = set()


def walk(code):
    for _, ln in dis.findlinestarts(code):
        if ln:
            exec_lines.add(ln)
    for const in code.co_consts:
        if hasattr(const, "co_code"):
            walk(const)


walk(compile(open(GATE).read(), GATE, "exec"))

hit = set()
GT = os.path.abspath(GATE)


def tracer(frame, event, arg):
    if event == "call":
        return tracer if os.path.abspath(frame.f_code.co_filename) == GT else None
    if event == "line":
        hit.add(frame.f_lineno)
    return tracer


old = sys.gettrace()
sys.settrace(tracer)
try:
    code = mod.selftest()
finally:
    sys.settrace(old)

# attribute each executable line to the enclosing top-level function
import ast
tree = ast.parse(open(GATE).read())
owner = {}
for node in tree.body:
    if isinstance(node, ast.FunctionDef):
        for ln in range(node.lineno, node.end_lineno + 1):
            owner[ln] = node.name

per_fn = {}
for ln in sorted(exec_lines):
    fn = owner.get(ln, "<module>")
    per_fn.setdefault(fn, {"exec": [], "hit": []})
    per_fn[fn]["exec"].append(ln)
    if ln in hit:
        per_fn[fn]["hit"].append(ln)

out = {"dir": WHICH, "tool": WHICH_TOOL,
       "gate_sha256": hashlib.sha256(open(GATE, "rb").read()).hexdigest(),
       "selftest_exit": code,
       "total_exec_lines": len(exec_lines), "total_hit": len(hit & exec_lines),
       "functions": {fn: {"exec_lines": len(v["exec"]), "hit": len(v["hit"]),
                          "missed_lines": [ln for ln in v["exec"] if ln not in hit]}
                     for fn, v in per_fn.items()}}
print(json.dumps(out, indent=1))
