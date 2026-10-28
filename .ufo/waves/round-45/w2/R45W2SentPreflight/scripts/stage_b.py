#!/usr/bin/env python3
"""Attack (b): a change that is not in FREEZE..REV because REV is a sibling branch
(or the range is not what it claims)."""
import json
import os
import sys

sys.path.insert(0, os.environ["S"])
from run import RESULTS, assert_toplevel, commit, g, gate, newrepo, sh, verdict, wr

BASE = {"frozen/a.txt": "alpha\n", "other.txt": "o\n"}
ARGS = ["--pathspec", "frozen/", "--freeze-path", "frozen", "--require-pathspec"]


def b1_sibling_rev():
    """REV is a sibling branch: freeze is NOT its ancestor."""
    d = newrepo("b1", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    g(d, "checkout", "-q", "-b", "side")
    wr(d, "frozen/a.txt", "side\n")
    s = commit(d, "side touches frozen")
    g(d, "checkout", "-q", "main")
    wr(d, "other.txt", "main\n")
    commit(d, "main moves")
    rec = gate("b1-sibling-rev", ["--root", d, "--freeze", f, "--rev", s, *ARGS],
               "REV=sibling branch tip that contains the frozen change; expect 2")
    rec["ancestor"] = g(d, "merge-base", "--is-ancestor", f, s).returncode
    return rec


def b2_sibling_branch_tip_clean():
    """REV sibling with NO frozen change: still must be 2, never 0."""
    d = newrepo("b2", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    g(d, "checkout", "-q", "-b", "side")
    wr(d, "other.txt", "side\n")
    s = commit(d, "side other")
    g(d, "checkout", "-q", "main")
    wr(d, "other.txt", "main\n")
    commit(d, "main moves")
    return gate("b2-sibling-clean-rev", ["--root", d, "--freeze", f, "--rev", s, *ARGS],
                "REV=sibling with no frozen change; expect 2 (2 is never a pass)")


def b3_merge_of_sibling_into_range():
    """The sibling branch's frozen change IS merged into REV: base is an ancestor."""
    d = newrepo("b3", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    g(d, "checkout", "-q", "-b", "side")
    wr(d, "frozen/a.txt", "side\n")
    commit(d, "side touches frozen")
    g(d, "checkout", "-q", "main")
    wr(d, "other.txt", "main\n")
    commit(d, "main moves")
    g(d, "merge", "-q", "--no-ff", "side", "-m", "merge side")
    r = g(d, "rev-parse", "HEAD").stdout.strip()
    return gate("b3-merged-sibling", ["--root", d, "--freeze", f, "--rev", r, *ARGS],
                "sibling merged in; expect 1")


def b4_shallow_clone():
    """The gate in a shallow clone: the freeze object is absent."""
    src = newrepo("b4src", BASE)
    assert_toplevel(src)
    f = commit(src, "freeze")
    for i in range(3):
        wr(src, "other.txt", "v%d\n" % i)
        commit(src, "move %d" % i)
    wr(src, "frozen/a.txt", "late\n")
    r = commit(src, "late frozen change")
    cl = os.path.join(os.path.dirname(src), "b4clone")
    sh(["rm", "-rf", cl])
    sh(["git", "clone", "-q", "--depth", "1", "file://" + src, cl])
    toplevel = g(cl, "rev-parse", "--show-toplevel").stdout.strip()
    rec = gate("b4-shallow", ["--root", cl, "--freeze", f, "--rev", "HEAD", *ARGS],
               "shallow clone: freeze object absent; expect 2")
    rec["clone_toplevel_ok"] = toplevel == os.path.realpath(cl) or toplevel == cl
    rec["freeze_present_in_clone"] = g(cl, "cat-file", "-e", f + "^{commit}").returncode == 0
    return rec


def b5_rev_is_a_tree():
    """REV is not a commit at all."""
    d = newrepo("b5", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    return gate("b5-rev-not-commit", ["--root", d, "--freeze", f, "--rev", f + "^{tree}",
                                      *ARGS],
                "REV=tree; expect 2")


def b6_descendant_of_freeze_on_detached_path():
    """Frozen change is 3 commits back, range spans all of it."""
    d = newrepo("b6", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    wr(d, "frozen/a.txt", "one\n")
    commit(d, "touch 1")
    wr(d, "other.txt", "x\n")
    commit(d, "unrelated")
    wr(d, "other.txt", "y\n")
    r = commit(d, "unrelated 2")
    return gate("b6-deep", ["--root", d, "--freeze", f, "--rev", r, *ARGS],
                "frozen change 3 commits back, tip bytes differ; expect 1")


for fn in (b1_sibling_rev, b2_sibling_branch_tip_clean, b3_merge_of_sibling_into_range,
           b4_shallow_clone, b5_rev_is_a_tree, b6_descendant_of_freeze_on_detached_path):
    try:
        fn()
    except Exception as exc:
        print(json.dumps({"case": fn.__name__, "driver_error": f"{type(exc).__name__}: {exc}"}))

with open(os.path.join(os.environ["S"], "results-b.json"), "w") as fh:
    json.dump(RESULTS, fh, indent=1)
for r in RESULTS:
    print(r["case"], "exit=%s" % r["exit"], "verdict=%s" % verdict(r))
