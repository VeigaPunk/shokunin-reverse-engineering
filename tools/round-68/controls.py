#!/usr/bin/env python3
"""controls.py - round-68 do-nothing / shortcut controls for R68-C1 and R68-C2.

The round's two claims are met only by work a shortcut cannot do.  This driver
scores the shortcuts as controls, from committed inputs, and never runs REA,
upx or git:

  c1-base             the real census over the base revision's own bytes
                      (plans < round 68): -> mismatches 2 (r67 pair)
  c1-shortcut-self     a census whose scope is the registry's OWN rows (the
                      shortcut "compare the table with itself"): 0 mismatches
                      while the base defect exists -> false green
  c1-constant-zero     a census that returns 0 without reading anything ->
                      false green
  c2-packed-only       a verdict built from the packed-bytes arm alone (no
                      unpack, no identity, no recovery): not met
  c2-no-identity       unpack + recovery but identity dropped: not met
  c2-real              the committed full-run receipt at the base: met, 2 of 2

Exit 0 when every arm lands where the control declares it must; 1 otherwise
(the control is then not a control and the claim is refused before data).

Write scope: --json-out only.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys

TOOL = "tools/round-68/controls.py"
LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RC = os.path.join(LANE, "tools", "round-68", "registry-conformance.py")
PE = os.path.join(LANE, "tools", "round-68", "packed-elf.py")
BASE = "fcbe200f6739c38939e0dabf3f251de2cc6bd727"
PRE = os.path.join(LANE, ".ufo", "waves", "round-68", "l1", "pre")


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(*argv: str) -> str:
    return subprocess.run(["git", "-C", LANE, *argv], check=True,
                          capture_output=True, text=True).stdout


def arms() -> list[dict]:
    rc_mod = load(RC, "r68_registry")
    pe_mod = load(PE, "r68_packed")
    plans, skill, existing = rc_mod.read_revision(LANE, BASE)
    real = rc_mod.census(plans, skill, existing)
    rows = rc_mod.registry_rows(skill)
    self_plans: dict[str, str] = {}
    for row in rows:
        m = rc_mod.re.match(r"tools/round-(\d+)/", row["path"])
        if not m:
            continue
        self_plans.setdefault(f"plans/round-{int(m.group(1))}-claims.md", set()).add(row["path"])
    self_plans = {k: "\n".join(sorted(v)) for k, v in self_plans.items()}
    self_census = rc_mod.census(self_plans, skill, existing)
    self_scope = len({p for v in self_plans.values() for p in v.split()})
    zero = {**real, "unregistered": [], "duplicate_rows": [], "row_absent": [],
            "thin": [], "mismatches": 0, "ok": True}
    with open(os.path.join(PRE, "c2-dryrun-at-base.json"), encoding="utf-8") as fh:
        packed = json.load(fh)
    carriers = packed["carriers"]

    def refold(mutate) -> dict:
        out = []
        for c in carriers:
            arms_d = dict(c["arms"])
            mutate(arms_d)
            out.append({"id": c["id"], "arms": arms_d,
                        "ok": all(arms_d.values())})
        verdict = pe_mod.fold(out, packed["control_ok"], packed["target"])
        return {**verdict, "carriers": out}

    packed_only = refold(lambda a: a.update({"identity_ok": False, "recovery_ok": False}))
    no_identity = refold(lambda a: a.update({"identity_ok": False}))
    real_fold = {"carriers_matched": packed["carriers_matched"], "target": packed["target"],
                 "control_ok": packed["control_ok"], "met_target": packed["met_target"]}
    return [
        {"id": "c1-base", "expected": {"mismatches": 2, "names": [
            "tools/round-67/avm-le-counter.py",
            "tools/round-67/mutation-battery.py"]},
         "observed": {"mismatches": real["mismatches"], "unregistered": real["unregistered"],
                      "scope_size": real["scope_size"], "registry_rows": real["registry_rows"]},
         "ok": real["mismatches"] == 2 and real["unregistered"] == [
             "tools/round-67/avm-le-counter.py", "tools/round-67/mutation-battery.py"]},
        {"id": "c1-shortcut-self", "expected": {"mismatches": 0},
         "observed": {"mismatches": self_census["mismatches"],
                      "scope_size": self_census["scope_size"]},
         "ok": self_census["mismatches"] == 0 and self_census["scope_size"] == self_scope},
        {"id": "c1-constant-zero", "expected": {"mismatches": 0},
         "observed": {"mismatches": zero["mismatches"]}, "ok": zero["mismatches"] == 0},
        {"id": "c2-packed-only", "expected": {"met_target": False},
         "observed": packed_only, "ok": packed_only["met_target"] is False},
        {"id": "c2-no-identity", "expected": {"met_target": False},
         "observed": no_identity, "ok": no_identity["met_target"] is False},
        {"id": "c2-real", "expected": {"met_target": True, "carriers_matched": 2},
         "observed": real_fold,
         "ok": real_fold["met_target"] is True and real_fold["carriers_matched"] == 2},
    ]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    try:
        result = arms()
    except Exception as exc:  # noqa: BLE001 - a control driver reports, never guesses
        print(json.dumps({"schema": "kaidoku-r68-controls-v1", "error": repr(exc)}),
              file=sys.stderr)
        return 2
    green = [a["id"] for a in result if a["ok"]]
    payload = {"schema": "kaidoku-r68-controls-v1", "base": BASE,
               "control_arms": len(result), "arms": result,
               "green": green, "ok": len(green) == len(result)}
    text = json.dumps(payload, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
