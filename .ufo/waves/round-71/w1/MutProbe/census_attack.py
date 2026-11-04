"""MutProbe-2 census attack: registries that must fail, one that must pass,
plus two false-green probes (empty owner cell, nine-cell row).
Runs the FROZEN registry-census.py (scratch copy, sha-verified) via its CLI
in --rev WORKTREE mode against isolated fixture roots. Read-only elsewhere.
"""
import json
import os
import shutil
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
CEN = os.path.join(S, "registry-census.py")
FX = os.path.join(S, "fixtures")
OPEN = "<!-- instrument-registry v2 -->"
CLOSE = "<!-- /instrument-registry -->"
HEADER = ("| tool | gate or probe - purpose | verdict map (exit codes) | self-test "
          "command | pinned-value path | write scope | owner |")
SEP = "|---|---|---|---|---|---|---|"


def row(*cells):
    return "| " + " | ".join(cells) + " |\n"


def table(*rows):
    return OPEN + "\n" + HEADER + "\n" + SEP + "\n" + "".join(rows) + CLOSE


good_a = row("`tools/a.py`", "gate - a", "0/1/2", "--selftest", "pin", "none", "kaidoku")
good_b = row("`tools/b.py`", "gate - b", "0/1/2", "--selftest", "pin", "none", "kaidoku")

CASES = {
    # name: (skill text, expected exit or None = record-only probe)
    "P1_pass-clean": (table(good_a, good_b), 0),
    "F1_seven-cells-empty-pinned": (
        table(row("`tools/a.py`", "gate - a", "0/1/2", "--selftest", "", "none", "kaidoku")), 1),
    "F2_two-rows-one-path": (table(good_a, good_a, good_b), 1),
    "F3_absent-path": (
        table(row("`tools/z.py`", "g", "0/1", "s", "p", "w", "kaidoku")), 1),
    "F4_marker-typo": (table(good_a).replace(CLOSE, "<!-- /instrument-registry-v2 -->"), 2),
    "F5_no-data-rows": (OPEN + "\n" + HEADER + "\n" + SEP + "\n" + CLOSE, 2),
    "X1_empty-owner-cell": (
        table(row("`tools/a.py`", "gate - a", "0/1/2", "--selftest", "pin", "none", "")), None),
    "X2_nine-cell-row": (
        table(row("`tools/a.py`", "g", "0/1", "s", "pin one", "pin two", "pin three",
                  "none", "kaidoku")), None),
}

results = []
for name, (skill, expect) in CASES.items():
    root = os.path.join(FX, name)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(os.path.join(root, "tools"))
    for n in ("a.py", "b.py"):
        with open(os.path.join(root, "tools", n), "w") as fh:
            fh.write("# fixture; never executed\n")
    with open(os.path.join(root, "SKILL.md"), "w") as fh:
        fh.write(skill)
    outp = os.path.join(FX, name + ".receipt.json")
    proc = subprocess.run(
        [sys.executable, "-I", "-B", CEN, "--root", root, "--rev", "WORKTREE",
         "--generate", "--out", outp],
        capture_output=True, text=True)
    payload = None
    if os.path.exists(outp):
        try:
            with open(outp) as fh:
                payload = json.load(fh)
        except json.JSONDecodeError:
            payload = None
    uneval = None
    if payload is None and proc.stderr.strip():
        try:
            uneval = json.loads(proc.stderr.strip().splitlines()[-1]).get("unevaluable")
        except (json.JSONDecodeError, IndexError):
            uneval = proc.stderr.strip()[-200:]
    results.append({
        "case": name,
        "expected_exit": expect,
        "exit": proc.returncode,
        "findings": (payload or {}).get("findings"),
        "nonconformant_defects": [r.get("defects") for r in
                                  ((payload or {}).get("nonconformant") or [])],
        "duplicates": (payload or {}).get("duplicates"),
        "rows": (payload or {}).get("rows"),
        "multicell_rows": (payload or {}).get("multicell_rows"),
        "legacy_rows": (payload or {}).get("legacy_rows"),
        "unevaluable": uneval,
        "receipt_written": os.path.exists(outp),
        "expected_match": (expect is None or proc.returncode == expect),
    })

with open(os.path.join(S, "census-results.json"), "w") as fh:
    json.dump(results, fh, indent=1)
print(json.dumps(results, indent=1))
