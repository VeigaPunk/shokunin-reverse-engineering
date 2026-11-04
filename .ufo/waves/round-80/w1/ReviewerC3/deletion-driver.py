#!/usr/bin/env python3
"""ReviewerC3 independent deletion driver for R80-C3.

For each of the nine `defects.append(...)` clauses inside
tools/round-78/attack-gate.py's validate_receipt(), write a copy of the blob at
the measured revision with that one statement replaced by `pass`, then run
`python3 -I -B <copy> --selftest` under a four-key child env and read the case
JSON lines.

No import of the gate. No reuse of another seat's parser: the clause set is
found with ast before the expected line numbers are checked, and a mismatch is
a hard failure rather than a silent skip.
"""
import argparse
import ast
import hashlib
import json
import os
import pathlib
import subprocess
import sys

# Frozen order and prefixes, from plans/round-80-claims.md.
EXPECTED = [
    ("duplicate fixture id", 782),
    ("fixture ids", 785),
    (": fixture dir mismatch", 790),
    (": base.accepted is not a bool", 792),
    (": refused without a reason", 794),
    (": refused by ", 797),
    ("base_accepted does not re-derive", 801),
    ("refused does not re-derive", 804),
    ("instrument sha256 is not", 807),
]


def clause_nodes(tree):
    fn = next((n for n in ast.walk(tree)
               if isinstance(n, ast.FunctionDef) and n.name == "validate_receipt"),
              None)
    if fn is None:
        raise SystemExit("no validate_receipt in the blob")
    out = []
    for node in ast.walk(fn):
        if not isinstance(node, ast.Expr) or not isinstance(node.value, ast.Call):
            continue
        call = node.value
        fnc = call.func
        if (isinstance(fnc, ast.Attribute) and fnc.attr == "append"
                and isinstance(fnc.value, ast.Name) and fnc.value.id == "defects"):
            out.append(node)
    return sorted(out, key=lambda n: (n.lineno, n.col_offset))


def literal_text(node):
    arg = node.value.args[0]
    if isinstance(arg, ast.JoinedStr):
        parts = []
        for v in arg.values:
            if isinstance(v, ast.Constant):
                parts.append(str(v.value))
            else:
                parts.append("{" + ast.unparse(v.value) + "}")
        return "".join(parts)
    if isinstance(arg, ast.Constant):
        return str(arg.value)
    return ast.unparse(arg)


def mutate(src, node):
    lines = src.splitlines(keepends=True)
    indent = " " * node.col_offset
    out = lines[: node.lineno - 1] + [f"{indent}pass\n"] + lines[node.end_lineno:]
    return "".join(out)


def run_selftest(path, work, env):
    proc = subprocess.run([sys.executable, "-I", "-B", str(path), "--selftest"],
                          cwd=str(work), env=env, capture_output=True, text=True)
    cases, summary = [], None
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("SELFTEST "):
            summary = line
            continue
        if line.startswith("{"):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict) and "case" in obj and "pass" in obj:
                cases.append(obj)
    failing = [c["case"] for c in cases if not c["pass"]]
    return {
        "exit": proc.returncode,
        "cases": len(cases),
        "failing": failing,
        "summary": summary,
        "stdout_tail": proc.stdout.splitlines()[-1] if proc.stdout else "",
        "stderr_tail": proc.stderr.splitlines()[-3:] if proc.stderr else [],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--gate")
    ap.add_argument("--work", required=True)
    ap.add_argument("--json-out")
    args = ap.parse_args()

    work = pathlib.Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    if args.gate:
        blob = pathlib.Path(args.gate).read_bytes()
    else:
        blob = subprocess.run(["git", "-C", args.root, "show",
                               f"{args.rev}:tools/round-78/attack-gate.py"],
                              capture_output=True, check=True).stdout
    src = blob.decode()
    digest = hashlib.sha256(blob).hexdigest()

    tree = ast.parse(src)
    nodes = clause_nodes(tree)
    found = [(literal_text(n), n.lineno, n.end_lineno) for n in nodes]
    if len(nodes) != 9:
        raise SystemExit(f"expected 9 validate_receipt append sites, found {len(nodes)}")
    drift = []
    for (prefix, line), (text, got_line, end_line) in zip(EXPECTED, found):
        if line != got_line or prefix not in text:
            drift.append({"expected_prefix": prefix, "expected_line": line,
                          "got_line": got_line, "got_text": text})
    if drift:
        raise SystemExit("clause drift: " + json.dumps(drift))

    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
           "HOME": os.environ.get("HOME", str(work)),
           "TMPDIR": str(work),
           "LANG": "C.UTF-8"}
    if set(env) != {"PATH", "HOME", "TMPDIR", "LANG"}:
        raise SystemExit("child env is not four-key")

    pristine_path = work / "pristine.py"
    pristine_path.write_text(src)
    pristine = run_selftest(pristine_path, work, env)

    results = []
    for i, ((prefix, line), node) in enumerate(zip(EXPECTED, nodes), start=1):
        mutant = work / f"mut-{i:02d}.py"
        text = mutate(src, node)
        try:
            ast.parse(text)
            compiles = True
        except SyntaxError:
            compiles = False
        mutant.write_text(text)
        run = run_selftest(mutant, work, env)
        results.append({
            "n": i,
            "prefix": prefix,
            "line": line,
            "end_line": node.end_lineno,
            "literal": literal_text(node),
            "compiles": compiles,
            "mutant_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "cases": run["cases"],
            "failing": run["failing"],
            "failing_count": len(run["failing"]),
            "summary": run["summary"],
            "exit": run["exit"],
            "python_traceback": bool(run["stderr_tail"]),
            "verdict": ("killed" if compiles and run["cases"] > 0 and run["failing"]
                        else "survivor" if compiles and run["cases"] > 0
                        else "unevaluable"),
        })

    killed = [r["prefix"] for r in results if r["verdict"] == "killed"]
    survivors = [r["prefix"] for r in results if r["verdict"] == "survivor"]
    unevaluable = [r["prefix"] for r in results if r["verdict"] == "unevaluable"]
    receipt = {
        "seat": "ReviewerC3",
        "rev": args.rev,
        "blob_sha256": digest,
        "clauses": len(nodes),
        "pristine": {"cases": pristine["cases"],
                     "failures": len(pristine["failing"]),
                     "failing": pristine["failing"],
                     "summary": pristine["summary"],
                     "exit": pristine["exit"]},
        "deletion_tally": {
            "mutants": len(results),
            "killed": len(killed),
            "survivors": len(survivors),
            "unevaluable": len(unevaluable),
            "killed_by": killed,
            "survivor_clauses": survivors,
            "unevaluable_clauses": unevaluable,
        },
        "per_clause": results,
        "child_env_keys": sorted(env),
        "python": sys.version.split()[0],
    }
    text = json.dumps(receipt, indent=2, sort_keys=True)
    print(text)
    if args.json_out:
        pathlib.Path(args.json_out).write_text(text + "\n")
    return 0 if not unevaluable else 2


if __name__ == "__main__":
    sys.exit(main())
