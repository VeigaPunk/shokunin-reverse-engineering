#!/usr/bin/env python3
"""Which lines of gate.py do the two counters' selftests actually execute?

Runs each counter's `selftest()` in-process under `sys.settrace` with a filename
filter on gate.py, then reports per-function covered/total lines and the exact
uncovered lines. `sys.settrace` records `line` events, so a function with zero
recorded lines was never entered.
"""
import ast
import hashlib
import json
import os
import sys

S = os.environ["HYAKU_SCRATCH"]
WHICH = sys.argv[1]
WHICH_TOOL = sys.argv[2]          # attest | registry
TOOLS = os.path.join(S, WHICH, "tools", "round-46")
GATE = os.path.join(TOOLS, "gate.py")

# gate.py first, so the counter module's `import gate` binds to THIS copy
sys.path.insert(0, TOOLS)
import gate  # noqa: E402
assert os.path.abspath(gate.__file__) == os.path.abspath(GATE), (
    "wrong gate bound: %s != %s" % (gate.__file__, GATE))

import importlib.util  # noqa: E402
spec = importlib.util.spec_from_file_location("counter_mod",
                                              os.path.join(TOOLS, WHICH_TOOL + ".py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# --- static picture: every function and its body lines ---------------------------
src = open(GATE).read()
tree = ast.parse(src)
funcs = {}
for node in tree.body:
    if isinstance(node, ast.FunctionDef):
        start = min([d.lineno for d in node.decorator_list] + [node.lineno])
        funcs[node.name] = (start, node.end_lineno)

hit = set()
GT = os.path.abspath(GATE)


def tracer(frame, event, arg):
    if event == "call":
        fn = frame.f_code.co_filename
        if os.path.abspath(fn) == GT:
            return tracer
        return None
    if event == "line":
        hit.add(frame.f_lineno)
    return tracer


old = sys.gettrace()
sys.settrace(tracer)
try:
    code = mod.selftest()
finally:
    sys.settrace(old)

out = {"dir": WHICH, "tool": WHICH_TOOL,
       "gate_sha256": hashlib.sha256(open(GATE, "rb").read()).hexdigest(),
       "selftest_exit": code, "functions": {}}
for name, (lo, hi) in sorted(funcs.items(), key=lambda kv: kv[1]):
    body = set(range(lo, hi + 1))
    covered = sorted(body & hit)
    out["functions"][name] = {"def_line": lo, "end_line": hi,
                              "lines": len(body), "covered": len(covered),
                              "entered": bool(covered),
                              "uncovered_lines": sorted(body - hit)}
out["total_covered"] = len(hit)
print(json.dumps(out, indent=1))
