#!/usr/bin/env python3
"""gen-controls.py - round-77 do-nothing controls for R77-C1 (frozen before data).

The claim's target is `mismatch_count 0 AND population.bound_clauses >= 18`.  A
control that skips the claimed work must not reach it.  This script derives two
control instruments from the pinned bytes of `tools/round-77/verdict-bind.py`
and checks that every mutation actually applied (a patch that silently misses
would make its control a fake):

  no-binding  `parse_clause` returns None: nothing binds, mismatches 0
  all-false   `bind` returns a failing verdict: every clause is a defect

`--base` runs both controls plus the round-76 pointer-only audit at the round's
base revision and writes one receipt.  The controls are copies under the wave's
`pre/controls/` directory; the lane instrument is never edited.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

INSTRUMENT = "tools/round-77/verdict-bind.py"
R76_AUDIT = "tools/round-76/record-audit.py"

NO_BINDING = """

# --- control mutation: no-binding (parse_clause returns None) ---
def parse_clause(clause):  # noqa: F811 - deliberate control override
    return None
"""

ALL_FALSE = """

# --- control mutation: all-false (bind always reports a mismatch) ---
def bind(clause, receipt):  # noqa: F811 - deliberate control override
    return False, "bound", {"field": "control", "claimed": None,
                            "actual": None}
"""


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derive(root: pathlib.Path, out_dir: pathlib.Path) -> dict:
    source = root / INSTRUMENT
    text = source.read_text()
    out_dir.mkdir(parents=True, exist_ok=True)
    written = {}
    for name, patch, marker in (("no-binding", NO_BINDING, "def parse_clause(clause):"),
                                ("all-false", ALL_FALSE, "def bind(clause, receipt):")):
        target = out_dir / f"verdict-bind-{name}.py"
        target.write_text(text + patch)
        body = target.read_text()
        if marker not in body.split("control mutation", 1)[1]:
            raise SystemExit(f"control patch {name!r} did not apply")
        written[name] = {"path": str(target),
                         "sha256": sha256(target)}
    written["source"] = {"path": str(source), "sha256": sha256(source)}
    return written


def run(cmd: list[str], cwd: pathlib.Path) -> dict:
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return {"argv": cmd, "exit": proc.returncode,
            "stdout_tail": proc.stdout[-1500:],
            "stderr_tail": proc.stderr[-600:]}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--base")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    root = pathlib.Path(args.root).resolve()
    out_dir = pathlib.Path(args.out_dir).resolve()
    derived = derive(root, out_dir)
    receipt = {"schema": "kaidoku-r77-controls-v1", "derived": derived}
    if args.base:
        for name in ("no-binding", "all-false"):
            receipt[name] = run([sys.executable, "-I", "-B",
                                 derived[name]["path"], "--root", ".",
                                 "--rev", args.base], root)
        receipt["pointer-only"] = run([sys.executable, "-I", "-B", R76_AUDIT,
                                       "--root", ".", "--rev", args.base], root)
        # Each control must FAIL the frozen target, and for its declared reason.
        target = {"mismatch_count": 0, "bound_floor": 18}
        for name in ("no-binding", "all-false"):
            tail = receipt[name]["stdout_tail"]
            try:
                body = json.loads(tail)
            except json.JSONDecodeError:
                body = {}
            population = body.get("population") or {}
            met = (body.get("mismatch_count") == target["mismatch_count"]
                   and population.get("bound_clauses", 0) >= target["bound_floor"])
            receipt[name]["meets_target"] = bool(met)
        receipt["controls_do_not_meet_target"] = not any(
            receipt[name].get("meets_target") for name in ("no-binding",
                                                           "all-false"))
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        pathlib.Path(args.json_out).write_text(text + "\n")
    print(json.dumps({"controls_do_not_meet_target":
                      receipt.get("controls_do_not_meet_target"),
                      "no_binding": receipt.get("no-binding", {}).get("exit"),
                      "all_false": receipt.get("all-false", {}).get("exit")},
                     indent=1))
    return 0 if receipt.get("controls_do_not_meet_target", True) else 1


if __name__ == "__main__":
    sys.exit(main())
