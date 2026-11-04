#!/usr/bin/env python3
"""Independent recon of validate_receipt()'s refusal clauses and deletion tally.

Reads tools/round-78/attack-gate.py read-only; every generated mutant lives in
this script's own directory under /fast/scratch.  No git writes, no /tmp.
"""

from __future__ import annotations

import ast
import contextlib
import hashlib
import importlib.util
import io
import json
import pathlib
import subprocess
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
GATE = LANE / "tools" / "round-78" / "attack-gate.py"
BASE_REV = "16dfa009bf143080dfcdfc5f9ec34bd359536d90"
WORK = pathlib.Path(__file__).resolve().parent
PY = sys.executable or "python3"


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def literal_prefix(arg: ast.expr) -> str:
    """The first non-empty literal segment of the message argument."""
    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
        return arg.value
    if isinstance(arg, ast.JoinedStr):
        for value in arg.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str) \
                    and value.value:
                return value.value
    return ""


def find_clauses(src: str) -> tuple[list[dict], dict]:
    tree = ast.parse(src)
    func = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "validate_receipt":
            func = node
            break
    if func is None:
        raise SystemExit("validate_receipt not found")

    found: list[dict] = []
    # walk with an explicit parent chain so the enclosing `if` test is exact
    stack: list[ast.AST] = []

    def visit(node: ast.AST) -> None:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) \
                and isinstance(node.value.func, ast.Attribute) \
                and node.value.func.attr == "append" \
                and isinstance(node.value.func.value, ast.Name) \
                and node.value.func.value.id == "defects":
            enclosing_if = next((n for n in reversed(stack)
                                 if isinstance(n, ast.If)), None)
            arg = node.value.args[0] if node.value.args else None
            found.append({
                "index": len(found) + 1,
                "lineno": node.lineno,
                "end_lineno": node.end_lineno,
                "col_offset": node.col_offset,
                "end_col_offset": node.end_col_offset,
                "message_literal": literal_prefix(arg),
                "message_literal_stripped": literal_prefix(arg).strip(),
                "message_expr": ast.unparse(arg) if arg is not None else None,
                "condition": ast.unparse(enclosing_if.test)
                if enclosing_if is not None else None,
                "condition_lineno": enclosing_if.lineno
                if enclosing_if is not None else None,
            })
            return
        stack.append(node)
        for child in ast.iter_child_nodes(node):
            visit(child)
        stack.pop()

    for stmt in func.body:
        visit(stmt)
    return found, {"function_lineno": func.lineno,
                   "function_end_lineno": func.end_lineno}


def mutate(src: str, clause: dict, replacement: str = "pass") -> str:
    lines = src.splitlines(keepends=True)
    s, e = clause["lineno"] - 1, clause["end_lineno"] - 1
    head = lines[s][:clause["col_offset"]]
    tail = lines[e][clause["end_col_offset"]:]
    return "".join(lines[:s] + [head + replacement + tail] + lines[e + 1:])


def instrument(src: str, clause: dict, idx: int) -> str:
    lines = src.splitlines(keepends=True)
    s = clause["lineno"] - 1
    probe = " " * clause["col_offset"] + f"_CLAUSE_TRACE.append({idx})\n"
    return "".join(lines[:s] + [probe] + lines[s:])


def run_selftest(path: pathlib.Path) -> dict:
    proc = subprocess.run([PY, "-I", "-B", str(path), "--selftest"],
                          capture_output=True, text=True, cwd=str(WORK),
                          env={"TMPDIR": str(WORK), "PATH": "/usr/bin:/bin",
                               "LANG": "C.UTF-8"})
    cases, failures, failing = [], None, []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if line.startswith("{") and '"case"' in line:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            cases.append(rec["case"])
            if not rec.get("pass"):
                failing.append(rec["case"])
        elif line.startswith("SELFTEST"):
            parts = dict(p.split("=") for p in line.split()[1:])
            failures = int(parts["failures"])
    return {"exit": proc.returncode, "cases": len(cases),
            "failures": failures, "failing_cases": failing,
            "stderr_tail": proc.stderr.strip().splitlines()[-3:]}


RUNNER = r'''
import contextlib, importlib.util, io, json, sys
path = sys.argv[1]
spec = importlib.util.spec_from_file_location("gatemod", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    code = mod.selftest()
tail = [l for l in buf.getvalue().splitlines() if l.startswith("SELFTEST")]
print(json.dumps({"exit": code, "trace": getattr(mod, "_CLAUSE_TRACE", None),
                  "selftest": tail[-1] if tail else None}))
'''


def run_runner(path: pathlib.Path) -> dict:
    runner = WORK / "_runner.py"
    if not runner.exists():
        runner.write_text(RUNNER)
    proc = subprocess.run([PY, "-I", "-B", str(runner), str(path)],
                          capture_output=True, text=True, cwd=str(WORK),
                          env={"TMPDIR": str(WORK), "PATH": "/usr/bin:/bin"})
    try:
        return json.loads(proc.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return {"error": proc.stderr.strip()[-800:], "stdout": proc.stdout[-400:]}


def load_module(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location("gate_pristine", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    src = GATE.read_text()
    gate_sha = sha256_file(GATE)
    clauses, func_info = find_clauses(src)
    declared = [
        "duplicate fixture id",
        "fixture ids",
        ": fixture dir mismatch",
        ": base.accepted is not a bool",
        ": refused without a reason",
        ": refused by ",
        "base_accepted does not re-derive",
        "refused does not re-derive",
        "instrument sha256 is not",
    ]
    for clause, prefix in zip(clauses, declared):
        clause["declared_prefix"] = prefix
        clause["declared_in_literal"] = prefix in clause["message_literal"]

    # --- pristine -------------------------------------------------------
    pristine = run_selftest(GATE)

    # --- per-clause deletion tally -------------------------------------
    tally = []
    mutants_dir = WORK / "mutants"
    mutants_dir.mkdir(exist_ok=True)
    for clause in clauses:
        mut = mutate(src, clause)
        path = mutants_dir / f"clause-{clause['index']:02d}.py"
        path.write_text(mut)
        result = run_selftest(path)
        result.update({"index": clause["index"],
                       "prefix": clause["declared_prefix"],
                       "killed": bool(result["failures"])})
        tally.append(result)

    # --- which clauses fire during the pristine selftest ----------------
    inst_src = src
    # insert from the last clause backwards so earlier offsets stay valid
    for clause in sorted(clauses, key=lambda c: -c["lineno"]):
        inst_src = instrument(inst_src, clause, clause["index"])
    marker = "def validate_receipt(receipt: dict) -> dict:\n"
    if marker not in inst_src:
        raise SystemExit("cannot anchor trace list")
    inst_src = inst_src.replace(marker, "_CLAUSE_TRACE = []\n\n\n" + marker, 1)
    inst_path = WORK / "instrumented-gate.py"
    inst_path.write_text(inst_src)
    trace_run = run_runner(inst_path)

    # --- fireability probes on the pristine module ----------------------
    mod = load_module(GATE)
    A = mod.ATTACKS
    digest = sha256_file(GATE)

    def fx(a, **over):
        d = {"id": a["id"], "fixture": a["fixture"], "base": {"accepted": True},
             "refused": False, "rule": a["rule"], "reasons": []}
        d.update(over)
        return d

    def receipt(fixtures, **over):
        r = {"fixtures": fixtures,
             "base_accepted": sum(1 for f in fixtures
                                  if (f.get("base") or {}).get("accepted")),
             "refused": sum(1 for f in fixtures if f.get("refused")),
             "instrument": {"path": "tools/round-78/attack-gate.py",
                            "sha256": digest}}
        r.update(over)
        return r

    dup = [fx(a) for a in A] + [fx(A[0])]
    probes = {
        1: receipt(dup),
        2: receipt([fx(a) for a in A[1:]]),
        3: receipt([fx(a) for a in A]),
        4: receipt([fx(a) for a in A]),
        5: receipt([fx(a) for a in A]),
        6: receipt([fx(a) for a in A]),
        7: receipt([fx(a) for a in A], base_accepted=len(A) - 1),
        8: receipt([fx(a) for a in A], refused=1),
        9: receipt([fx(a) for a in A],
                   instrument={"path": "tools/round-78/attack-gate.py",
                               "sha256": "0" * 64}),
    }
    # clause-specific perturbations
    probes[3]["fixtures"][0]["fixture"] = "not-the-declared-dir"
    probes[4]["fixtures"][0]["base"] = {"accepted": "yes"}
    probes[5]["fixtures"][0]["refused"] = True
    probes[5]["fixtures"][0]["reasons"] = []
    probes[5]["refused"] = 1
    probes[6]["fixtures"][0]["refused"] = True
    probes[6]["fixtures"][0]["reasons"] = [{"rule": "not_the_declared_rule"}]
    probes[6]["refused"] = 1

    fire = []
    for clause in clauses:
        i = clause["index"]
        defects = mod.validate_receipt(probes[i])["defects"]
        seg = clause["declared_prefix"]
        hits_seg = [d for d in defects if seg in d]
        hits_head = [d for d in defects if d.startswith(seg)]
        fire.append({"index": i, "prefix": seg,
                     "fired": bool(hits_seg),
                     "fires_as_startswith": bool(hits_head),
                     "fired_message": hits_seg[0] if hits_seg else None,
                     "defects": defects})

    # --- traced clause set ---------------------------------------------
    trace = trace_run.get("trace") or []
    traced_unique = sorted(set(trace))

    out = {
        "gate": str(GATE),
        "base_rev": BASE_REV,
        "gate_sha256": gate_sha,
        "gate_sha256_at_base": sha256_file(WORK / "_base-gate.py")
        if (WORK / "_base-gate.py").exists() else None,
        "clause_count": len(clauses),
        "function": func_info,
        "clauses": clauses,
        "pristine": pristine,
        "deletion_tally": tally,
        "selftest_trace": {"trace": trace, "fired_clauses": traced_unique,
                           "case_count": trace_run.get("selftest")},
        "fireability": fire,
        "attack_count": len(A),
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
