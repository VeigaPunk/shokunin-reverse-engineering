#!/usr/bin/env python3
"""Clause 7 binds a file outside the round-47 freeze. Reformat gate.py AFTER the freeze commit
and the counter flips to 1 while `frozen_path_changed` stays 0 and no frozen byte moved."""
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
REFORMATTED = ('    r = git(\n'
               '        root,\n'
               '        "log",\n'
               '        "-m",\n'
               '        "--diff-merges=first-parent",\n'
               '        "--name-status",\n'
               '        "-z",\n'
               '        "--format=",\n'
               '        f"{base}..{tip}",\n'
               '        "--",\n'
               '        *paths,\n'
               '        binary=True,\n'
               '    )\n')
assert ORIG_CALL in GATE_BODY


def git(d, *a, check=True):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, check=check)


def main():
    d = os.path.join(SCRATCH, "post-freeze-flip")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    git(d, "init", "-q")
    for k, v in (("user.email", "fx@r47"), ("user.name", "r47")):
        git(d, "config", k, v)
    files = {
        "SKILL.md": exact.skill_text(exact.good_block()),
        "plans/round-47-claims.md": exact.CLAIMS_BODY,
        "corpus/lessons/round-46.md": "lesson line\n" * 240,
        exact.SELF: EXACT_BODY,
        exact.GATE46: GATE_BODY,
    }
    for p, text in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(text)
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "freeze")
    freeze = git(d, "rev-parse", "HEAD").stdout.strip()
    top = gate.git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert top == d, (top, d)
    # only gate.py is reformatted; nothing in plans/round-47-claims.md or tools/round-47/ moves
    open(os.path.join(d, exact.GATE46), "w").write(GATE_BODY.replace(ORIG_CALL, REFORMATTED, 1))
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "ruff format --line-length 80 tools/round-46/gate.py")
    rev = git(d, "rev-parse", "HEAD").stdout.strip()
    before = git(d, "rev-parse", "%s:%s" % (freeze, exact.GATE46)).stdout.strip()
    after = git(d, "rev-parse", "%s:%s" % (rev, exact.GATE46)).stdout.strip()
    c_f, r_f = exact.evaluate(d, freeze, freeze, "v3", with_battery=False)
    c_r, r_r = exact.evaluate(d, freeze, rev, "v3", with_battery=False)
    out = {
        "fixture": d,
        "freeze": freeze, "rev": rev,
        "gate_blob_at_freeze": before, "gate_blob_at_rev": after,
        "gate_changed": before != after,
        "frozen_paths": r_r.get("frozen_derived"),
        "at_freeze": {"exit": c_f, "failing": r_f.get("failing"),
                      "frozen_path_changed": r_f.get("frozen_path_changed")},
        "at_rev": {"exit": c_r, "failing": r_r.get("failing"),
                   "frozen_path_changed": r_r.get("frozen_path_changed"),
                   "touched": r_r.get("touched"), "restored": r_r.get("restored")},
        "frozen_bytes_moved": [p for p in
                               ("plans/round-47-claims.md", "tools/round-47/exact.py")
                               if git(d, "rev-parse", "%s:%s" % (freeze, p)).stdout.strip()
                               != git(d, "rev-parse", "%s:%s" % (rev, p)).stdout.strip()],
    }
    print(json.dumps(out, indent=1))
    shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    main()
