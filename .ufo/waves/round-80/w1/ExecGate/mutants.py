#!/usr/bin/env python3
"""Round-80 R80-C3 probe: per-clause mutants of the candidate attack gate.

For each of the nine `defects.append(...)` clauses of `validate_receipt()`,
write a copy of the candidate in which exactly that statement is replaced by
`pass`, run the copy's `--selftest`, and report which declared cases fail.
A clause is bound only when its own declared case is the one that fails.

The nine clauses are located with `ast`, so the "exactly one occurrence"
claim is structural: the function must contain nine `defects.append` calls,
one per source position, and each splice is that call's span only.
"""

from __future__ import annotations

import ast
import json
import os
import pathlib
import subprocess
import sys

# Frozen clause prefixes, in source order (plans/round-80-claims.md).
CLAUSES = [
    ("G01-duplicate-fixture-id", "red-validate-duplicate-fixture-id",
     "duplicate fixture id"),
    ("G02-fixture-id-set", "red-validate-fixture-id-set",
     "fixture ids"),
    ("G03-fixture-dir", "red-validate-fixture-dir",
     ": fixture dir mismatch"),
    ("G04-base-accepted-bool", "red-validate-base-accepted-bool",
     ": base.accepted is not a bool"),
    ("G05-refused-no-reason", "red-validate-refused-no-reason",
     ": refused without a reason"),
    ("G06-refused-other-rule", "red-validate-refused-other-rule",
     ": refused by "),
    ("G07-base-accepted-count", "red-validate-base-accepted-count",
     "base_accepted does not re-derive"),
    ("G08-refused-count", "red-validate-refused-count",
     "refused does not re-derive"),
    ("G09-instrument-digest", "red-validate-instrument-digest",
     "instrument sha256 is not"),
]


def clause_calls(text: str) -> list[tuple[int, int, str]]:
    """Every `defects.append(...)` call inside validate_receipt(), in order.

    Returns (lineno, offset, source) sorted by source position.  Raises when
    the count is not nine or two calls share a start position, so a mutation
    can never silently hit the wrong statement.
    """
    tree = ast.parse(text)
    func = next(node for node in tree.body
                if isinstance(node, ast.FunctionDef)
                and node.name == "validate_receipt")
    calls = []
    for node in ast.walk(func):
        if (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "append"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "defects"):
            start = node.lineno
            stop = node.end_lineno
            src = "\n".join(text.splitlines()[start - 1:stop])
            calls.append((start, node.col_offset, src, stop,
                          node.end_col_offset))
    calls.sort(key=lambda c: (c[0], c[1]))
    if len(calls) != len(CLAUSES):
        raise SystemExit(f"expected {len(CLAUSES)} defects.append clauses, "
                         f"found {len(calls)}")
    starts = {(c[0], c[1]) for c in calls}
    if len(starts) != len(calls):
        raise SystemExit("two defects.append clauses share a start position")
    return calls


def splice(text: str, call) -> str:
    """Replace one `defects.append(...)` statement with `pass`."""
    lineno, col, _src, end_lineno, end_col = call
    lines = text.splitlines(keepends=True)
    head = "".join(lines[:lineno - 1]) + lines[lineno - 1][:col]
    last = lines[end_lineno - 1]
    tail = last[end_col:] if len(last) > end_col else ""
    tail += "".join(lines[end_lineno:])
    return head + "pass" + tail


def run_selftest(path: pathlib.Path, scratch: pathlib.Path) -> dict:
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
           "HOME": os.environ.get("HOME", str(scratch)),
           "TMPDIR": str(scratch), "LANG": "C.UTF-8"}
    proc = subprocess.run([sys.executable, "-I", "-B", str(path), "--selftest"],
                          capture_output=True, text=True, cwd=scratch,
                          env=env, timeout=300)
    cases: list[dict] = []
    summary = None
    for line in proc.stdout.splitlines():
        line = line.strip()
        if line.startswith("SELFTEST "):
            summary = line
        elif line.startswith("{"):
            cases.append(json.loads(line))
    return {"exit": proc.returncode, "summary": summary, "cases": cases,
            "stdout": proc.stdout, "stderr": proc.stderr}


def main(argv: list[str]) -> int:
    ap_src = pathlib.Path(argv[1]).resolve()
    scratch = pathlib.Path(argv[2]).resolve()
    out = pathlib.Path(argv[3]).resolve()
    scratch.mkdir(parents=True, exist_ok=True)
    (out / "mutants").mkdir(parents=True, exist_ok=True)

    text = ap_src.read_text()
    calls = clause_calls(text)
    pristine = run_selftest(ap_src, scratch)
    pristine_failing = [c["case"] for c in pristine["cases"] if not c["pass"]]

    rows = []
    for (clause_id, case_name, prefix), call in zip(CLAUSES, calls):
        stmt = call[2]
        if prefix not in stmt:
            raise SystemExit(f"{clause_id}: prefix {prefix!r} absent from "
                             f"clause at line {call[0]}")
        mutant = splice(text, call)
        if mutant == text:
            raise SystemExit(f"{clause_id}: mutation changed nothing")
        if text.count(stmt) != 1:
            raise SystemExit(f"{clause_id}: statement is not unique in source")
        path = scratch / f"mutant-{clause_id}.py"
        path.write_text(mutant)
        assert path.read_text() == mutant
        run = run_selftest(path, scratch)
        failing = [c["case"] for c in run["cases"] if not c["pass"]]
        (out / "mutants" / f"{clause_id}.txt").write_text(run["stdout"])
        rows.append({
            "clause": clause_id,
            "line": call[0],
            "prefix": prefix,
            "declared_case": case_name,
            "cases": len(run["cases"]),
            "failures": len(failing),
            "failing": failing,
            "own_case_failed": case_name in failing,
            "other_cases_failed": [c for c in failing if c != case_name],
            "isolating": failing == [case_name],
            "exit": run["exit"],
            "summary": run["summary"],
        })

    bound = [r for r in rows if r["isolating"]]
    report = {
        "candidate": str(ap_src),
        "candidate_sha256": __import__("hashlib").sha256(
            ap_src.read_bytes()).hexdigest(),
        "clauses": len(rows),
        "bound": len(bound),
        "survivors": [r["clause"] for r in rows if not r["isolating"]],
        "pristine": {"cases": len(pristine["cases"]),
                     "failures": len(pristine_failing),
                     "failing": pristine_failing,
                     "summary": pristine["summary"],
                     "exit": pristine["exit"]},
        "mutants": rows,
        "ok": (len(rows) == 9 and len(bound) == 9
               and len(pristine["cases"]) == 37 and not pristine_failing),
    }
    (out / "mutants.json").write_text(json.dumps(report, indent=1,
                                                 sort_keys=True) + "\n")
    print(json.dumps({k: report[k] for k in
                      ("clauses", "bound", "survivors", "pristine", "ok")},
                     sort_keys=True))
    for row in rows:
        print(json.dumps({k: row[k] for k in
                          ("clause", "declared_case", "failures", "failing",
                           "isolating")}, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
