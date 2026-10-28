#!/usr/bin/env python3
"""Follow-ups 2: prove the dir-tree backstop is the sole detector behind a negative
pathspec; test whether replace refs / grafts (which the gate does not disable) can make
a changed frozen path read clean; and run the real lane as a positive control."""
import json
import os
import sys

sys.path.insert(0, os.environ["S"])
from run import RESULTS, assert_toplevel, commit, g, gate, newrepo, verdict, wr

BASE = {"tools/round-45/frozen.py": "v1\n", "tools/round-44/older.py": "o\n",
        "other.txt": "o\n"}
FP = "tools/round-45"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "f762b7273e3f6ca3c710bb37d5de92a4a4417aec"


def g1_negative_pathspec_backstop_sole():
    """Negative pathspec hides the frozen dir from the commit arm; drop --require-pathspec
    so the gate can run, and see whether the dir-tree backstop alone catches."""
    d = newrepo("g1", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    wr(d, "tools/round-45/frozen.py", "CHANGED\n")
    r = commit(d, "touch frozen")
    rec = gate("g1-negative-pathspec-no-require",
               ["--root", d, "--freeze", f, "--rev", r,
                "--pathspec", "tools/", "--pathspec", ":(exclude)tools/round-45/",
                "--freeze-path", FP],
               "negative pathspec hides the dir; expect 1 from the dir-tree backstop")
    rec["log_negative"] = g(d, "log", "-m", "--diff-merges=first-parent", "--name-status",
                            "--format=%h", f"{f}..{r}", "--", "tools/",
                            ":(exclude)tools/round-45/").stdout.strip()
    return rec


def g2_replace_ref():
    """A replace ref rewrites the tip into a commit whose tree equals the freeze tree.
    The gate does not pass --no-replace-objects."""
    d = newrepo("g2", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    ftree = g(d, "rev-parse", f + "^{tree}").stdout.strip()
    wr(d, "tools/round-45/frozen.py", "CHANGED-BY-REPLACE-TEST\n")
    r = commit(d, "touch frozen")
    # build a commit with the freeze tree and the freeze as its parent
    fake = g(d, "commit-tree", ftree, "-p", f, "-m", "looks clean").stdout.strip()
    rep = g(d, "replace", r, fake)
    rec = gate("g2-replace-ref",
               ["--root", d, "--freeze", f, "--rev", r, "--pathspec", "tools/round-45/",
                "--freeze-path", FP, "--require-pathspec"],
               "replace ref rewrites tip to a clean tree; expect 1, watch for 0")
    rec["replace_rc"] = rep.returncode
    rec["replace_stderr"] = rep.stderr.strip()
    rec["tip_blob_without_replace"] = g(d, "rev-parse", r + ":tools/round-45/frozen.py").stdout.strip()
    rec["tip_blob_with_replace"] = g(d, "rev-parse", "--no-replace-objects",
                                     r + ":tools/round-45/frozen.py").stdout.strip()
    rec["worktree_bytes"] = open(os.path.join(d, "tools/round-45/frozen.py")).read()
    rec["show_tip_no_replace"] = g(d, "show", "--no-replace-objects", "--stat",
                                   "--format=%h %T", r).stdout.strip()
    return rec


def g3_grafts_file():
    """Same, via .git/info/grafts; git log with GIT_NO_REPLACE_OBJECTS unset."""
    d = newrepo("g3", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    ftree = g(d, "rev-parse", f + "^{tree}").stdout.strip()
    wr(d, "tools/round-45/frozen.py", "CHANGED-BY-GRAFT-TEST\n")
    r = commit(d, "touch frozen")
    fake = g(d, "commit-tree", ftree, "-m", "grafted clean").stdout.strip()
    with open(os.path.join(d, ".git/info/grafts"), "w") as fh:
        fh.write("%s\n" % fake)  # graft: r appears as a root commit with the freeze tree
    rec = gate("g3-graft",
               ["--root", d, "--freeze", f, "--rev", r, "--pathspec", "tools/round-45/",
                "--freeze-path", FP, "--require-pathspec"],
               "info/grafts makes the tip look like a clean root; expect 1, watch for 0")
    rec["graft_log"] = g(d, "log", "-m", "--diff-merges=first-parent", "--name-status",
                         "--format=%h %T", f"{f}..{r}", "--", FP).stdout.strip()
    return rec


def g4_lane_landing_control():
    """Positive control on the real lane: no frozen path changed FREEZE..HEAD."""
    return gate("g4-lane-head", ["--root", LANE, "--freeze", FREEZE, "--rev", "HEAD",
                                 "--pathspec", "tools/round-45/",
                                 "--freeze-path", "tools/round-45",
                                 "--pathspec", "plans/round-45-claims.md",
                                 "--freeze-path", "plans/round-45-claims.md",
                                 "--require-pathspec"],
                "real lane at HEAD: expect 0 clean")


def g5_lane_landing_rev():
    return gate("g5-lane-landing", ["--root", LANE, "--freeze", FREEZE,
                                    "--rev", "e715263cb51b713c342ab992d527fe9d61d6f8ff",
                                    "--pathspec", "tools/round-45/",
                                    "--freeze-path", "tools/round-45",
                                    "--pathspec", "plans/round-45-claims.md",
                                    "--freeze-path", "plans/round-45-claims.md",
                                    "--require-pathspec"],
                "real lane at the landing commit: expect 0 clean")


def g6_lane_empty_range():
    return gate("g6-lane-freeze-to-freeze", ["--root", LANE, "--freeze", FREEZE,
                                             "--rev", FREEZE,
                                             "--pathspec", "tools/round-45/",
                                             "--freeze-path", "tools/round-45",
                                             "--require-pathspec"],
                "real lane, empty range: expect 0")


for fn in (g1_negative_pathspec_backstop_sole, g2_replace_ref, g3_grafts_file,
           g4_lane_landing_control, g5_lane_landing_rev, g6_lane_empty_range):
    try:
        fn()
    except Exception as exc:
        print(json.dumps({"case": fn.__name__, "driver_error": f"{type(exc).__name__}: {exc}"}))

with open(os.path.join(os.environ["S"], "results-g.json"), "w") as fh:
    json.dump(RESULTS, fh, indent=1)
for r in RESULTS:
    print(r["case"], "exit=%s" % r["exit"], "verdict=%s" % verdict(r))
