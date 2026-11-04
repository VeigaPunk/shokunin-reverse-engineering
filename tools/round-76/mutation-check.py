#!/usr/bin/env python3
"""mutation-check.py - round-76 instrument (R76-C1/R76-C2 fixture closure).

Scores the round-76 instruments' own declared cases against nine one-point
mutants of the checks those cases exist for.  The round-76 wave's
MutationTester seat found five survivors on the first cut (a guard-masked
absent-row case, no wrapped-claim case, and three unexercised gate guards);
this battery is the closure: every mutant must be killed by its DECLARED case,
and a kill by some other case is reported as `killed_wrong_case`, never a kill.

Patch sets (one mutant each, applied to a scratch copy, never the lane file):

  d24-a  the absent-row check becomes a no-op          -> cap-absent-row-red
  d24-b  the evidence-pointer existence check removed  -> cap-absent-evidence-path-red
  d24-c  the first-working-round check removed         -> cap-round-mismatch-red
  d24-d  the stub-description check removed            -> cap-stub-description-red
  d24-e  the claim is read line-level, not paragraph   -> cap-wrapped-claim-accepts
  gate-f the static placeholder scan is skipped        -> prose-plan
  gate-g the child is spawned with shell=True          -> missing-required-arg
  gate-h the $OUT containment check is skipped         -> escape-out
  gate-i the argv allowlist check is skipped           -> script-outside

Exit: 0 every mutant killed by its declared case; 1 a survivor or a
wrong-case kill, each named; 2 could-not-evaluate (a patch site absent or
ambiguous, a pristine selftest not green, bad argv).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

AUDIT = "tools/round-76/record-audit.py"
GATE = "tools/round-76/plan-command.py"

MUTANTS = [
    {"name": "d24-a", "tool": AUDIT, "case": "cap-absent-row-red",
     "old": "            row = table.get(name)",
     "new": "            row = table.get(name) or next(iter(table.values()), None)"},
    {"name": "d24-b", "tool": AUDIT, "case": "cap-absent-evidence-path-red",
     "old": "            if absent:", "new": "            if False:"},
    {"name": "d24-c", "tool": AUDIT, "case": "cap-round-mismatch-red",
     "old": "            if str(claim[\"round\"]) not in re.findall(r\"\\d+\", row[3]):",
     "new": "            if False:"},
    {"name": "d24-d", "tool": AUDIT, "case": "cap-stub-description-red",
     "old": "            if len(row[1].split()) < 8:", "new": "            if False:"},
    {"name": "d24-e", "tool": AUDIT, "case": "cap-wrapped-claim-accepts",
     "old": "        text = \" \".join(part.strip() for part in para)",
     "new": "        text = para[0]"},
    {"name": "gate-f", "tool": GATE, "case": "prose-plan",
     "old": "    defects = static_defects(command)",
     "new": "    defects = []"},
    {"name": "gate-g", "tool": GATE, "case": "missing-required-arg",
     "old": "    proc = subprocess.run(argv, cwd=root, env=env, capture_output=True,",
     "new": "    proc = subprocess.run(argv, shell=True, cwd=root, env=env, capture_output=True,"},
    {"name": "gate-h", "tool": GATE, "case": "escape-out",
     "old": "        out_real = containment(out, work)",
     "new": "        out_real = out"},
    {"name": "gate-i", "tool": GATE, "case": "script-outside",
     "old": "    if not script.startswith(allow_prefix) or \"..\" in script:",
     "new": "    if False:"},
]


def selftest(root: str, tool: str, rev: str, work: str, kind: str) -> dict:
    argv = ["python3", "-I", "-B", tool]
    if kind == GATE:
        argv += ["--root", root, "--rev", rev, "--work", work]
    argv.append("--selftest")
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
           "HOME": os.path.join(work, "home"),
           "TMPDIR": os.path.join(work, "tmp"),
           "LANG": "C.UTF-8"}
    os.makedirs(env["HOME"], exist_ok=True)
    os.makedirs(env["TMPDIR"], exist_ok=True)
    proc = subprocess.run(argv, cwd=root, env=env, capture_output=True,
                          text=True, timeout=600, stdin=subprocess.DEVNULL)
    try:
        body = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"rc": proc.returncode, "cases": None, "failures": None,
                "stderr_tail": proc.stderr[-500:]}
    return {"rc": proc.returncode, "cases": body.get("cases"),
            "failures": body.get("failures"), "case_names": body.get("case_names")}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)
    os.makedirs(args.work, exist_ok=True)

    pristine = {tool: selftest(root, tool, args.rev,
                               tempfile.mkdtemp(dir=args.work, prefix="pristine-"),
                               tool)
                for tool in (AUDIT, GATE)}
    pristine_ok = all(row["rc"] == 0 and not row["failures"]
                      for row in pristine.values())
    if not pristine_ok:
        print(json.dumps({"unevaluable": "pristine selftest not green",
                          "pristine": pristine}, indent=1))
        return 2

    rows = []
    for mutant in MUTANTS:
        scratch = tempfile.mkdtemp(dir=args.work, prefix=mutant["name"] + "-")
        source = os.path.join(root, mutant["tool"])
        text = open(source, encoding="utf-8").read()
        hits = text.count(mutant["old"])
        if hits != 1:
            rows.append({**{k: mutant[k] for k in ("name", "tool", "case")},
                         "verdict": "unevaluable",
                         "detail": f"patch site occurs {hits} times"})
            shutil.rmtree(scratch, ignore_errors=True)
            continue
        copy = os.path.join(scratch, os.path.basename(mutant["tool"]))
        with open(copy, "w", encoding="utf-8") as fh:
            fh.write(text.replace(mutant["old"], mutant["new"], 1))
        rel = os.path.relpath(copy, root)
        row = selftest(root, rel, args.rev, scratch, mutant["tool"])
        failures = row["failures"] or []
        verdict = ("killed" if mutant["case"] in failures
                   else "killed_wrong_case" if failures
                   else "survivor")
        rows.append({**{k: mutant[k] for k in ("name", "tool", "case")},
                     "rc": row["rc"], "failures": failures,
                     "verdict": verdict,
                     "sole": failures == [mutant["case"]]})
        shutil.rmtree(scratch, ignore_errors=True)

    survivors = [r for r in rows if r["verdict"] != "killed"]
    receipt = {"schema": "kaidoku-r76-mutation-check-v1", "rev": args.rev,
               "root": root, "pristine": pristine, "mutants": rows,
               "survivor_count": len(survivors),
               "survivors": [r["name"] for r in survivors],
               "wrong_case": [r["name"] for r in rows
                              if r["verdict"] == "killed_wrong_case"],
               "ok": not survivors,
               "exit": 0 if not survivors else 1}
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return receipt["exit"]


if __name__ == "__main__":
    sys.exit(main())
