#!/usr/bin/env python3
"""Attack (d): symlinks under the frozen pathspec, pointing outside; plus the dirty arm."""
import json
import os
import sys

sys.path.insert(0, os.environ["S"])
from run import RESULTS, assert_toplevel, commit, g, gate, newrepo, verdict, wr

BASE = {"frozen/a.txt": "alpha\n", "other.txt": "o\n"}
ARGS = ["--pathspec", "frozen/", "--freeze-path", "frozen", "--require-pathspec"]
OUTSIDE = os.path.join(os.environ["S"], "outside")


def link(root, path, target):
    full = os.path.join(root, path)
    os.makedirs(os.path.dirname(full) or root, exist_ok=True)
    if os.path.lexists(full):
        os.remove(full)
    os.symlink(target, full)


def mkoutside():
    os.makedirs(OUTSIDE, exist_ok=True)
    with open(os.path.join(OUTSIDE, "secret.txt"), "w") as fh:
        fh.write("outside-v1\n")


def d1_unchanged_symlink():
    """Frozen symlink to an outside file, unchanged in REV -> repo content unchanged."""
    mkoutside()
    d = newrepo("d1", BASE)
    assert_toplevel(d)
    link(d, "frozen/out", os.path.join(OUTSIDE, "secret.txt"))
    f = commit(d, "freeze")
    wr(d, "other.txt", "changed\n")
    r = commit(d, "unrelated")
    return gate("d1-unchanged-symlink", ["--root", d, "--freeze", f, "--rev", r, *ARGS],
                "frozen symlink to outside, untouched; expect 0")


def d2_retargeted_symlink():
    mkoutside()
    d = newrepo("d2", BASE)
    assert_toplevel(d)
    link(d, "frozen/out", os.path.join(OUTSIDE, "secret.txt"))
    f = commit(d, "freeze")
    link(d, "frozen/out", "/etc/passwd")
    r = commit(d, "retarget symlink")
    return gate("d2-retargeted-symlink", ["--root", d, "--freeze", f, "--rev", r, *ARGS],
                "symlink target text changed; expect 1")


def d3_file_to_symlink():
    mkoutside()
    d = newrepo("d3", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    link(d, "frozen/a.txt", os.path.join(OUTSIDE, "secret.txt"))
    r = commit(d, "file -> symlink")
    return gate("d3-file-to-symlink", ["--root", d, "--freeze", f, "--rev", r, *ARGS],
                "frozen file replaced by symlink; expect 1")


def d4_dir_to_symlink():
    """The whole frozen directory replaced by a symlink to an outside dir."""
    mkoutside()
    d = newrepo("d4", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    import shutil
    shutil.rmtree(os.path.join(d, "frozen"))
    link(d, "frozen", OUTSIDE)
    r = commit(d, "dir -> symlink")
    return gate("d4-dir-to-symlink", ["--root", d, "--freeze", f, "--rev", r, *ARGS],
                "frozen dir replaced by outside symlink; expect 1")


def d5_outside_target_mutated_only():
    """The outside target changes but the repo does not: the gate must stay clean."""
    mkoutside()
    d = newrepo("d5", BASE)
    assert_toplevel(d)
    link(d, "frozen/out", os.path.join(OUTSIDE, "secret.txt"))
    f = commit(d, "freeze")
    with open(os.path.join(OUTSIDE, "secret.txt"), "w") as fh:
        fh.write("outside-v2-MUTATED\n")
    wr(d, "other.txt", "changed\n")
    r = commit(d, "unrelated")
    rec = gate("d5-outside-mutation", ["--root", d, "--freeze", f, "--rev", r, *ARGS],
               "outside target mutated, repo untouched; expect 0")
    rec["status_porcelain"] = g(d, "status", "--porcelain").stdout.strip()
    return rec


def d6_symlink_inside_repo():
    """Frozen symlink -> a repo file outside the frozen dir that changes afterwards."""
    d = newrepo("d6", BASE)
    assert_toplevel(d)
    wr(d, "target.txt", "t1\n")
    link(d, "frozen/ptr", "../../target.txt")
    f = commit(d, "freeze")
    wr(d, "target.txt", "t2\n")
    r = commit(d, "target moves")
    return gate("d6-inside-symlink-target", ["--root", d, "--freeze", f, "--rev", r, *ARGS],
                "link blob unchanged, target changed; expect 0 (link text is the content)")


def d7_dirty_untracked_in_frozen():
    """--check-dirty with an untracked file inside the frozen dir."""
    d = newrepo("d7", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    wr(d, "frozen/new.txt", "untracked\n")
    return gate("d7-dirty-untracked", ["--root", d, "--freeze", f, "--rev", f,
                                       "--check-dirty", *ARGS],
                "untracked file inside frozen dir; expect 1")


def d8_dirty_pathspec_excludes_frozen():
    """--dirty-pathspec narrows the status scan away from the dirty frozen file."""
    d = newrepo("d8", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    wr(d, "frozen/a.txt", "DIRTY\n")
    rec = gate("d8-dirty-pathspec-excludes", ["--root", d, "--freeze", f, "--rev", f,
                                              "--check-dirty", "--dirty-pathspec", "other/",
                                              *ARGS],
               "frozen/a.txt dirty but --dirty-pathspec=other/ ; expect 1, watch for false 0")
    rec["status_porcelain"] = g(d, "status", "--porcelain").stdout.strip()
    return rec


def d9_dirty_symlink_mode_only():
    """chmod on a frozen file: mode change, but the dirty arm compares worktree to index."""
    d = newrepo("d9", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    g(d, "config", "core.fileMode", "true")
    os.chmod(os.path.join(d, "frozen/a.txt"), 0o755)
    rec = gate("d9-dirty-mode", ["--root", d, "--freeze", f, "--rev", f,
                                 "--check-dirty", *ARGS],
               "frozen/a.txt chmod 755 uncommitted; expect 1")
    rec["status_porcelain"] = g(d, "status", "--porcelain").stdout.strip()
    return rec


for fn in (d1_unchanged_symlink, d2_retargeted_symlink, d3_file_to_symlink, d4_dir_to_symlink,
           d5_outside_target_mutated_only, d6_symlink_inside_repo, d7_dirty_untracked_in_frozen,
           d8_dirty_pathspec_excludes_frozen, d9_dirty_symlink_mode_only):
    try:
        fn()
    except Exception as exc:
        print(json.dumps({"case": fn.__name__, "driver_error": f"{type(exc).__name__}: {exc}"}))

with open(os.path.join(os.environ["S"], "results-d.json"), "w") as fh:
    json.dump(RESULTS, fh, indent=1)
for r in RESULTS:
    print(r["case"], "exit=%s" % r["exit"], "verdict=%s" % verdict(r))
