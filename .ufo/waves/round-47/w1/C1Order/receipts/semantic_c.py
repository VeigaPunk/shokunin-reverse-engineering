#!/usr/bin/env python3
"""Case C: a merge whose second-parent commits predate the measured base.

The gate's real range is freeze..rev, so a side branch cut before the freeze puts ONLY the
merge commit in range. That is the minimal fixture on which the flag order changes
gate.history_touched's answer.
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

D = os.path.join(S, "merge-fx-c")


def g(*a, **kw):
    return subprocess.run(["git", "-C", D, *a], capture_output=True, text=True, **kw)


shutil.rmtree(D, ignore_errors=True)
os.makedirs(D)
subprocess.run(["git", "-C", D, "init", "-q", "-b", "main"], check=True)
g("config", "user.email", "c1order@round47", check=True)
g("config", "user.name", "c1order caseC", check=True)
assert subprocess.run(["git", "-C", D, "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip() == D
open(os.path.join(D, "frozen.txt"), "w").write("base\n")
open(os.path.join(D, "other.txt"), "w").write("base\n")
os.makedirs(os.path.join(D, "plans"), exist_ok=True)
open(os.path.join(D, "plans/round-47-claims.md"), "w").write(
    "# claims\n\n## Frozen paths (exact)\n\n- `frozen.txt`\n- `other.txt`\n\n## After\n\ntail\n")
g("add", "-A", check=True)
g("commit", "-q", "-m", "c0", check=True)
g("checkout", "-q", "-b", "side", check=True)
open(os.path.join(D, "frozen.txt"), "w").write("side\n")
g("commit", "-q", "-am", "side: frozen=side", check=True)      # predates the base
g("checkout", "-q", "main", check=True)
open(os.path.join(D, "frozen.txt"), "w").write("main\n")
open(os.path.join(D, "other.txt"), "w").write("moved\n")
g("commit", "-q", "-am", "freeze point", check=True)
base = g("rev-parse", "HEAD").stdout.strip()                    # the measured base
m = g("merge", "--no-ff", "side", "-m", "merge side")
assert m.returncode != 0 and "frozen.txt" in m.stdout, m.stdout
open(os.path.join(D, "frozen.txt"), "w").write("main\n")        # resolution == parent1 bytes
g("add", "frozen.txt", check=True)
g("commit", "-q", "--no-edit", check=True)
tip = g("rev-parse", "HEAD").stdout.strip()

src = open(os.path.join(LANE, "tools/round-46/gate.py")).read()
swapped = src.replace('"-m", "--diff-merges=first-parent"',
                      '"--diff-merges=first-parent", "-m"', 1)
assert swapped != src
ns = {"__name__": "gate_swapped"}
exec(compile(swapped, "gate_swapped.py", "exec"), ns)  # noqa: S102


def run(argv):
    r = subprocess.run(["git", "-C", D, "log", *argv, "--name-status", "-z",
                        "--format=", f"{base}..{tip}", "--", "frozen.txt"],
                       capture_output=True, text=True)
    return {"argv": list(argv), "exit": r.returncode, "raw": r.stdout,
            "tokens": [t for t in r.stdout.split("\0") if t.strip()]}


out = {
    "base": base, "tip": tip,
    "range": f"{base}..{tip}",
    "commits_in_range": g("rev-list", f"{base}..{tip}").stdout.split(),
    "correct_order": run(["-m", "--diff-merges=first-parent"]),
    "reversed_order": run(["--diff-merges=first-parent", "-m"]),
    "gate_touched_correct_order": gate.history_touched(D, base, tip, ["frozen.txt"]),
    "gate_touched_reversed_order": ns["history_touched"](D, base, tip, ["frozen.txt"]),
    "blob_changed": gate.blob_changed(D, base, tip, [("frozen.txt", False)]),
}
# the gate's own verdict shape, both orders
out["gate_receipt_correct"] = gate.freeze_state(D, base, tip, "plans/round-47-claims.md")
out["gate_receipt_reversed"] = ns["freeze_state"](D, base, tip, "plans/round-47-claims.md")
with open(os.path.join(S, "order-semantics-C.json"), "w") as fh:
    json.dump(out, fh, indent=1, sort_keys=True, default=str)
print(json.dumps(out, indent=1, sort_keys=True, default=str))
