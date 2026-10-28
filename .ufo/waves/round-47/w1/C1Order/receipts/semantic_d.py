#!/usr/bin/env python3
"""Case D: the flag order flips the GATE VERDICT on a frozen path the merge never touched.

Design: the side branch never touches the frozen path; the base commit (parent 1) does, so the
side tree still carries the pre-base bytes. `--diff-merges=separate` (what `-m` means when it
comes last) then reports the frozen path as changed by the merge, though the merge introduced
no such change on the mainline.
"""
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r47/C1Order"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools/round-46"))
import gate  # noqa: E402

D = os.path.join(S, "merge-fx-d")


def g(*a, **kw):
    return subprocess.run(["git", "-C", D, *a], capture_output=True, text=True, **kw)


shutil.rmtree(D, ignore_errors=True)
os.makedirs(D)
subprocess.run(["git", "-C", D, "init", "-q", "-b", "main"], check=True)
g("config", "user.email", "c1order@round47", check=True)
g("config", "user.name", "c1order caseD", check=True)
assert subprocess.run(["git", "-C", D, "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip() == D
os.makedirs(os.path.join(D, "plans"))
open(os.path.join(D, "plans/round-47-claims.md"), "w").write(
    "# claims\n\n## Frozen paths (exact)\n\n- `frozen.txt`\n\n## After\n\ntail\n")
open(os.path.join(D, "frozen.txt"), "w").write("base\n")
open(os.path.join(D, "unfrozen.txt"), "w").write("base\n")
g("add", "-A", check=True)
g("commit", "-q", "-m", "c0", check=True)
g("checkout", "-q", "-b", "side", check=True)
open(os.path.join(D, "unfrozen.txt"), "w").write("side\n")   # side never touches the frozen path
g("commit", "-q", "-am", "side: unfrozen only", check=True)
g("checkout", "-q", "main", check=True)
open(os.path.join(D, "frozen.txt"), "w").write("main\n")      # the base commit touches it
g("commit", "-q", "-am", "freeze point", check=True)
base = g("rev-parse", "HEAD").stdout.strip()
m = g("merge", "--no-ff", "side", "-m", "merge side")
assert m.returncode == 0, m.stderr        # clean auto-merge: no resolution edit involved
tip = g("rev-parse", "HEAD").stdout.strip()

src = open(os.path.join(LANE, "tools/round-46/gate.py")).read()
swapped = src.replace('"-m", "--diff-merges=first-parent"',
                      '"--diff-merges=first-parent", "-m"', 1)
assert swapped != src
ns = {"__name__": "gate_swapped"}
exec(compile(swapped, "gate_swapped.py", "exec"), ns)  # noqa: S102

c_ok, r_ok = gate.freeze_state(D, base, tip, "plans/round-47-claims.md")
c_bad, r_bad = ns["freeze_state"](D, base, tip, "plans/round-47-claims.md")
out = {
    "repo": D, "base": base, "tip": tip,
    "commits_in_range": g("rev-list", f"{base}..{tip}").stdout.split(),
    "side_touched": g("show", "--name-only", "--format=", "HEAD^2").stdout.split(),
    "touched_correct": gate.history_touched(D, base, tip, ["frozen.txt"]),
    "touched_reversed": ns["history_touched"](D, base, tip, ["frozen.txt"]),
    "verdict_correct": {"exit": c_ok, "reason": r_ok.get("reason"),
                        "touched": r_ok.get("touched"),
                        "frozen_path_changed": r_ok.get("frozen_path_changed"),
                        "restored": r_ok.get("restored")},
    "verdict_reversed": {"exit": c_bad, "reason": r_bad.get("reason"),
                         "touched": r_bad.get("touched"),
                         "frozen_path_changed": r_bad.get("frozen_path_changed"),
                         "restored": r_bad.get("restored")},
    "verdict_differs": (c_ok, r_ok.get("touched")) != (c_bad, r_bad.get("touched")),
}
with open(os.path.join(S, "order-semantics-D.json"), "w") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print(json.dumps(out, indent=1, sort_keys=True))
