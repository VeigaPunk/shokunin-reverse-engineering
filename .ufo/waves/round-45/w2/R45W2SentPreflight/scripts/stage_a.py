#!/usr/bin/env python3
"""Attack (a): frozen path changed in a merge commit / merge topology."""
import json
import os
import sys

sys.path.insert(0, os.environ["S"])
from run import (RESULTS, assert_toplevel, commit, g, gate, newrepo, verdict, wr)

BASE = {"frozen/a.txt": "alpha\n", "frozen/b.txt": "beta\n", "other.txt": "o\n"}


def a1_side_branch_merged():
    """Plain --no-ff merge of a side branch that changed a frozen path."""
    d = newrepo("a1", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    g(d, "checkout", "-q", "-b", "side")
    wr(d, "frozen/a.txt", "side\n")
    commit(d, "side changes frozen")
    g(d, "checkout", "-q", "main")
    wr(d, "other.txt", "main\n")
    commit(d, "main moves")
    g(d, "merge", "-q", "--no-ff", "side", "-m", "merge side")
    r = g(d, "rev-parse", "HEAD").stdout.strip()
    return gate("a1-merge-side-touch", ["--root", d, "--freeze", f, "--rev", r,
                                        "--pathspec", "frozen/", "--freeze-path", "frozen",
                                        "--require-pathspec"],
                "side branch changed frozen/a.txt, merged --no-ff; expect 1")


def a2_treesame_prune():
    """Side branch touches a frozen path then reverts it BEFORE the merge.

    The merge result is byte-identical to parent 1 for frozen/a.txt. Two commits in
    FREEZE..REV touched a frozen path; no later restore un-blocks. If git's default
    history simplification (TREESAME pruning, no --full-history) hides the side
    branch, the gate reports clean.
    """
    d = newrepo("a2", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    g(d, "checkout", "-q", "-b", "side")
    wr(d, "frozen/a.txt", "tampered\n")
    commit(d, "side tamper")
    wr(d, "frozen/a.txt", "alpha\n")
    commit(d, "side revert")
    g(d, "checkout", "-q", "main")
    wr(d, "other.txt", "main\n")
    commit(d, "main moves")
    g(d, "merge", "-q", "--no-ff", "side", "-m", "merge side")
    r = g(d, "rev-parse", "HEAD").stdout.strip()
    # ground truth: what plain full-history says about the range
    truth = g(d, "log", "--full-history", "--name-status", "--format=%h",
              f"{f}..{r}", "--", "frozen/").stdout
    rec = gate("a2-treesame-prune", ["--root", d, "--freeze", f, "--rev", r,
                                     "--pathspec", "frozen/", "--freeze-path", "frozen",
                                     "--require-pathspec"],
               "side branch tampered then reverted before merge; expect 1")
    rec["ground_truth_full_history"] = truth.strip().splitlines()
    print(json.dumps({"case": "a2-ground-truth",
                      "git log --full-history --name-status": rec["ground_truth_full_history"]}))
    return rec


def a3_evil_merge():
    """A change to a frozen path introduced inside the merge commit itself."""
    d = newrepo("a3", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    g(d, "checkout", "-q", "-b", "side")
    wr(d, "other.txt", "side\n")
    commit(d, "side other")
    g(d, "checkout", "-q", "main")
    wr(d, "other.txt", "main\n")
    commit(d, "main other")
    g(d, "merge", "-q", "--no-ff", "--no-commit", "side")
    wr(d, "frozen/a.txt", "evil\n")  # neither parent has this
    commit(d, "evil merge")
    r = g(d, "rev-parse", "HEAD").stdout.strip()
    return gate("a3-evil-merge", ["--root", d, "--freeze", f, "--rev", r,
                                  "--pathspec", "frozen/", "--freeze-path", "frozen",
                                  "--require-pathspec"],
                "merge commit itself writes frozen/a.txt; expect 1")


def a4_clean_merge():
    """False-positive probe: merge whose side branch touches nothing frozen."""
    d = newrepo("a4", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    g(d, "checkout", "-q", "-b", "side")
    wr(d, "other.txt", "side\n")
    commit(d, "side other")
    g(d, "checkout", "-q", "main")
    wr(d, "other.txt", "main\n")
    commit(d, "main other")
    g(d, "merge", "-q", "--no-ff", "side", "-m", "merge side")
    r = g(d, "rev-parse", "HEAD").stdout.strip()
    return gate("a4-clean-merge", ["--root", d, "--freeze", f, "--rev", r,
                                   "--pathspec", "frozen/", "--freeze-path", "frozen",
                                   "--require-pathspec"],
                "merge in range, nothing frozen touched; expect 0")


def a5_merge_second_parent_only():
    """Merge where the frozen change exists ONLY on the second parent, and the merge
    is `-s ours` (first parent taken wholesale). Tip bytes == freeze bytes."""
    d = newrepo("a5", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    g(d, "checkout", "-q", "-b", "side")
    wr(d, "frozen/a.txt", "side\n")
    commit(d, "side tamper")
    g(d, "checkout", "-q", "main")
    wr(d, "other.txt", "main\n")
    commit(d, "main other")
    g(d, "merge", "-q", "--no-ff", "-s", "ours", "side", "-m", "ours merge")
    r = g(d, "rev-parse", "HEAD").stdout.strip()
    return gate("a5-ours-merge", ["--root", d, "--freeze", f, "--rev", r,
                                  "--pathspec", "frozen/", "--freeze-path", "frozen",
                                  "--require-pathspec"],
                "-s ours drops the side change; side commit still touched frozen; expect 1")


for fn in (a1_side_branch_merged, a2_treesame_prune, a3_evil_merge, a4_clean_merge,
           a5_merge_second_parent_only):
    try:
        fn()
    except Exception as exc:
        print(json.dumps({"case": fn.__name__, "driver_error": f"{type(exc).__name__}: {exc}"}))

with open(os.path.join(os.environ["S"], "results-a.json"), "w") as fh:
    json.dump(RESULTS, fh, indent=1)
print("=== verdicts ===")
for r in RESULTS:
    print(r["case"], "exit=%s" % r["exit"], "verdict=%s" % verdict(r))
