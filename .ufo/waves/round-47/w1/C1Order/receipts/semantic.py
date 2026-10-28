#!/usr/bin/env python3
"""Measure what the flag order actually does to gate.history_touched (R46-CL6)."""
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r47/C1Order"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools/round-46"))
import gate  # noqa: E402

D = os.path.join(S, "merge-fx")


def g(*a, **kw):
    return subprocess.run(["git", "-C", D, *a], capture_output=True, text=True, **kw)


def build(resolution):
    shutil.rmtree(D, ignore_errors=True)
    os.makedirs(D)
    subprocess.run(["git", "-C", D, "init", "-q", "-b", "main"], check=True)
    for k, v in (("user.email", "c1order@round47"), ("user.name", "c1order merge")):
        g("config", k, v, check=True)
    assert subprocess.run(["git", "-C", D, "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True).stdout.strip() == D
    open(os.path.join(D, "frozen.txt"), "w").write("base\n")
    open(os.path.join(D, "other.txt"), "w").write("base\n")
    g("add", "-A", check=True)
    g("commit", "-q", "-m", "base", check=True)
    base = g("rev-parse", "HEAD").stdout.strip()
    g("checkout", "-q", "-b", "side", check=True)
    open(os.path.join(D, "frozen.txt"), "w").write("side\n")
    g("commit", "-q", "-am", "side changes frozen", check=True)
    side = g("rev-parse", "HEAD").stdout.strip()
    g("checkout", "-q", "main", check=True)
    open(os.path.join(D, "frozen.txt"), "w").write("main\n")
    g("commit", "-q", "-am", "main changes frozen", check=True)
    m = g("merge", "--no-ff", "side", "-m", "merge side")
    assert m.returncode != 0, "expected a conflict on frozen.txt"
    assert "frozen.txt" in m.stdout, m.stdout
    open(os.path.join(D, "frozen.txt"), "w").write(resolution)
    g("add", "frozen.txt", check=True)
    g("commit", "-q", "--no-edit", check=True)
    tip = g("rev-parse", "HEAD").stdout.strip()
    parents = g("rev-parse", "HEAD^1", "HEAD^2").stdout.split()
    return base, tip, parents, side


def log_order(base, tip, argv):
    r = subprocess.run(["git", "-C", D, "log", *argv, "--name-status",
                        "--format=%h", f"{base}..{tip}"],
                       capture_output=True, text=True)
    return {"argv": list(argv), "exit": r.returncode, "stdout": r.stdout,
            "stderr": r.stderr.strip(),
            "frozen_mentioned": "frozen.txt" in r.stdout,
            "lines": len([l for l in r.stdout.splitlines() if l.strip()])}


ORDER_ARGV = ["-m", "--diff-merges=first-parent"]
REVERSED_ARGV = ["--diff-merges=first-parent", "-m"]

out = {"cases": []}
for label, resolution in (("A-resolution-is-new-content", "merged\n"),
                          ("B-resolution-restores-first-parent", "main\n")):
    base, tip, parents, side = build(resolution)
    case = {"case": label, "resolution": resolution.strip(), "base": base, "tip": tip,
            "parents": parents,
            "correct_order": log_order(base, tip, ORDER_ARGV),
            "reversed_order": log_order(base, tip, REVERSED_ARGV),
            "gate_touched_correct_order": gate.history_touched(D, base, tip, ["frozen.txt"]),
            "gate_touched_reversed_order": None}
    # the same function with the argv literal swapped, executed from a copy
    src = open(os.path.join(LANE, "tools/round-46/gate.py")).read()
    swapped = src.replace('"-m", "--diff-merges=first-parent"',
                          '"--diff-merges=first-parent", "-m"', 1)
    assert swapped != src
    ns = {"__name__": "gate_swapped"}
    exec(compile(swapped, "gate_swapped.py", "exec"), ns)  # noqa: S102
    case["gate_touched_reversed_order"] = ns["history_touched"](
        D, base, tip, ["frozen.txt"])
    case["touched_differs"] = (case["gate_touched_correct_order"][0]
                               != case["gate_touched_reversed_order"][0])
    # isolate the MERGE: parent1..tip, so branch commits are out of range
    p1 = parents[0]
    case["merge_only"] = {
        "range": f"{p1}..{tip}",
        "correct_order": log_order(p1, tip, ORDER_ARGV),
        "reversed_order": log_order(p1, tip, REVERSED_ARGV),
        "gate_touched_correct_order": gate.history_touched(D, p1, tip, ["frozen.txt"]),
        "gate_touched_reversed_order": ns["history_touched"](D, p1, tip, ["frozen.txt"]),
    }
    case["merge_only"]["touched_differs"] = (
        case["merge_only"]["gate_touched_correct_order"][0]
        != case["merge_only"]["gate_touched_reversed_order"][0])
    out["cases"].append(case)

with open(os.path.join(S, "order-semantics.json"), "w") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print(json.dumps(out, indent=1, sort_keys=True))
