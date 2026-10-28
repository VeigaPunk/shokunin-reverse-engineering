#!/usr/bin/env python3
"""End-to-end: run the full frozen counter (battery included) on a gate.py whose merge arm
passes the literal pair in the correct order but AFTER `--`, so the flags are inert."""
import json
import os
import shutil
import subprocess
import sys

SCRATCH = sys.argv[1]
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
T47 = os.path.join(LANE, "tools", "round-47")
T46 = os.path.join(LANE, "tools", "round-46")
sys.path.insert(0, T47)
sys.path.insert(0, T46)
import gate          # noqa: E402
import exact         # noqa: E402

GATE_BODY = open(os.path.join(T46, "gate.py")).read()
EXACT_BODY = open(os.path.join(T47, "exact.py")).read()
ORIG_CALL = ('    r = git(root, "log", "-m", "--diff-merges=first-parent", "--name-status", "-z",\n'
             '            "--format=", f"{base}..{tip}", "--", *paths, binary=True)\n')
FORGED_CALL = ('    r = git(root, "log", "--name-status", "-z",\n'
               '            "--format=", f"{base}..{tip}", "--", *paths,\n'
               '            "-m", "--diff-merges=first-parent", binary=True)\n')
assert ORIG_CALL in GATE_BODY


def git(d, *a, check=True):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, check=check)


def make(gate_text, name):
    d = os.path.join(SCRATCH, "e2e-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    git(d, "init", "-q")
    for k, v in (("user.email", "fx@r47"), ("user.name", "r47")):
        git(d, "config", k, v)
    for p, text in {"SKILL.md": exact.skill_text(exact.good_block()),
                    "plans/round-47-claims.md": exact.CLAIMS_BODY,
                    "corpus/lessons/round-46.md": "lesson line\n" * 240,
                    exact.SELF: EXACT_BODY,
                    exact.GATE46: gate_text}.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(text)
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "freeze")
    rev = git(d, "rev-parse", "HEAD").stdout.strip()
    assert gate.git(d, "rev-parse", "--show-toplevel").stdout.strip() == d
    return d, rev


def main():
    out = {}
    for name, gate_text in (("control", GATE_BODY),
                            ("forged-flags-after-pathspec",
                             GATE_BODY.replace(ORIG_CALL, FORGED_CALL, 1))):
        d, rev = make(gate_text, name)
        code, receipt = exact.evaluate(d, rev, rev, "v3", with_battery=True)
        bat = receipt.get("battery") or {}
        out[name] = {
            "fixture": d, "rev": rev,
            "counter_exit": code,
            "failing": receipt.get("failing"),
            "frozen_path_changed": receipt.get("frozen_path_changed"),
            "gate_order_literal": receipt.get("gate_order_literal"),
            "gate_order_reversed": receipt.get("gate_order_reversed"),
            "battery": {k: bat.get(k) for k in
                        ("forgeries_total", "v2_green", "v3_green", "genuine_green", "crash")},
            "battery_fixtures": bat.get("fixtures"),
            "met_target": receipt.get("met_target"),
        }
        shutil.rmtree(d, ignore_errors=True)
    # absent gate.py: could-not-evaluate (2) or not-met (1)?
    d = os.path.join(SCRATCH, "e2e-no-gate")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    git(d, "init", "-q")
    for k, v in (("user.email", "fx@r47"), ("user.name", "r47")):
        git(d, "config", k, v)
    skill = exact.skill_text(exact.good_block())
    for p, text in {"SKILL.md": skill,
                    "plans/round-47-claims.md": exact.CLAIMS_BODY,
                    "corpus/lessons/round-46.md": "lesson line\n" * 240,
                    exact.SELF: EXACT_BODY}.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(text)
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "freeze without gate.py")
    rev = git(d, "rev-parse", "HEAD").stdout.strip()
    assert gate.git(d, "rev-parse", "--show-toplevel").stdout.strip() == d
    code, receipt = exact.score(skill, lambda p: gate.show(d, rev, p), "v3", rev, battery=None)
    out["no-gate-py"] = {"fixture": d, "rev": rev, "score_exit": code,
                         "failing": receipt.get("failing")}
    out["no-gate-py"]["evaluate_exit"] = exact.evaluate(d, rev, rev, "v3",
                                                       with_battery=False)[0]
    shutil.rmtree(d, ignore_errors=True)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
