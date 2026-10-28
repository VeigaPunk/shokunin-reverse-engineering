#!/usr/bin/env python3
"""Follow-ups: a true sibling REV (freeze not an ancestor), the dir-backstop defeat chain,
a mode-only change, and the relative --freeze-path spelling."""
import json
import os
import sys

sys.path.insert(0, os.environ["S"])
from run import RESULTS, assert_toplevel, commit, g, gate, newrepo, verdict, wr

BASE = {"tools/round-45/frozen.py": "v1\n", "tools/round-44/older.py": "o\n",
        "other.txt": "o\n"}
FP = "tools/round-45"
ARGS = ["--pathspec", "tools/round-45/", "--freeze-path", FP, "--require-pathspec"]


def true_siblings(name, touch_frozen):
    """freeze on main; side cut from the freeze's PARENT, so freeze is not an ancestor."""
    d = newrepo(name, BASE)
    assert_toplevel(d)
    root = commit(d, "root")
    g(d, "checkout", "-q", "-b", "side")
    if touch_frozen:
        wr(d, "tools/round-45/frozen.py", "side\n")
    else:
        wr(d, "other.txt", "side\n")
    s = commit(d, "side commit")
    g(d, "checkout", "-q", "main")
    f = commit(d, "freeze")
    wr(d, "tools/round-45/frozen.py", "main-after-freeze\n")
    commit(d, "main after freeze")
    anc = g(d, "merge-base", "--is-ancestor", f, s).returncode
    rec = gate(name, ["--root", d, "--freeze", f, "--rev", s, *ARGS],
               "true sibling: freeze is NOT an ancestor of REV; expect 2")
    rec["is_ancestor_rc"] = anc
    rec["freeze_in_side_history"] = g(d, "merge-base", f, s).stdout.strip() == f
    return rec


def f1_sibling_touching():
    return true_siblings("f1-true-sibling-touch", True)


def f2_sibling_clean():
    return true_siblings("f2-true-sibling-clean", False)


def f3_backstop_defeat():
    """Covering pathspec (passes covers()) + negative pathspec hiding the frozen dir
    + --freeze-path spelled ./-relative so both rev-parse probes fail."""
    d = newrepo("f3", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    wr(d, "tools/round-45/frozen.py", "CHANGED\n")
    r = commit(d, "touch frozen")
    rec = gate("f3-backstop-defeat",
               ["--root", d, "--freeze", f, "--rev", r,
                "--pathspec", "tools/", "--pathspec", ":(exclude)tools/round-45/",
                "--freeze-path", "./tools/round-45", "--require-pathspec"],
               "covering+negative pathspec, ./ freeze-path: expect 1, watch for 0")
    rec["revparse"] = {
        "base:./fp": g(d, "rev-parse", f + ":./tools/round-45").returncode,
        "tip:./fp": g(d, "rev-parse", r + ":./tools/round-45").returncode,
        "base:fp": g(d, "rev-parse", f + ":tools/round-45").returncode,
    }
    rec["log_with_negative"] = g(d, "log", "-m", "--diff-merges=first-parent",
                                 "--name-status", "--format=%h", f"{f}..{r}",
                                 "--", "tools/", ":(exclude)tools/round-45/").stdout.strip()
    return rec


def f4_negative_only_with_good_fp():
    """Same negative pathspec, correct freeze-path: the dir backstop must catch."""
    d = newrepo("f4", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    wr(d, "tools/round-45/frozen.py", "CHANGED\n")
    r = commit(d, "touch frozen")
    return gate("f4-negative-pathspec-good-fp",
                ["--root", d, "--freeze", f, "--rev", r,
                 "--pathspec", "tools/", "--pathspec", ":(exclude)tools/round-45/",
                 "--freeze-path", FP, "--require-pathspec"],
                "negative pathspec hides the dir, correct freeze-path: expect 1 via backstop")


def f5_mode_only():
    """Commit that changes only the mode bit of a frozen file."""
    d = newrepo("f5", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    os.chmod(os.path.join(d, "tools/round-45/frozen.py"), 0o755)
    r = commit(d, "mode only")
    rec = gate("f5-mode-only", ["--root", d, "--freeze", f, "--rev", r, *ARGS],
               "mode-only change to a frozen file; expect 1")
    rec["name_status"] = g(d, "log", "-m", "--diff-merges=first-parent", "--name-status",
                           "--format=%h", f"{f}..{r}", "--", FP).stdout.strip()
    return rec


def f6_relative_fp_alone():
    """--freeze-path ./tools/round-45 with the canonical pathspec: does the commit arm
    still fire, and does the receipt name the frozen path correctly?"""
    d = newrepo("f6", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    wr(d, "tools/round-45/frozen.py", "CHANGED\n")
    r = commit(d, "touch frozen")
    return gate("f6-relative-fp", ["--root", d, "--freeze", f, "--rev", r,
                                   "--pathspec", "tools/round-45/",
                                   "--freeze-path", "./tools/round-45",
                                   "--require-pathspec"],
                "./ freeze-path, canonical pathspec; expect 1")


for fn in (f1_sibling_touching, f2_sibling_clean, f3_backstop_defeat,
           f4_negative_only_with_good_fp, f5_mode_only, f6_relative_fp_alone):
    try:
        fn()
    except Exception as exc:
        print(json.dumps({"case": fn.__name__, "driver_error": f"{type(exc).__name__}: {exc}"}))

with open(os.path.join(os.environ["S"], "results-f.json"), "w") as fh:
    json.dump(RESULTS, fh, indent=1)
for r in RESULTS:
    print(r["case"], "exit=%s" % r["exit"], "verdict=%s" % verdict(r))
