#!/usr/bin/env python3
"""Attack (e): --pathspec matching a parent of the frozen dir (and related spellings),
plus the no-pathspec default (whole-tree scan)."""
import json
import os
import sys

sys.path.insert(0, os.environ["S"])
from run import RESULTS, assert_toplevel, commit, g, gate, newrepo, verdict, wr

BASE = {"tools/round-45/frozen.py": "v1\n", "tools/round-44/older.py": "o\n",
        "other.txt": "o\n"}
FP = "tools/round-45"


def mk(name):
    d = newrepo(name, BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    return d, f


def e1_pathspec_dot():
    d, f = mk("e1")
    wr(d, "tools/round-45/frozen.py", "CHANGED\n")
    r = commit(d, "touch frozen")
    return gate("e1-pathspec-dot", ["--root", d, "--freeze", f, "--rev", r,
                                    "--pathspec", ".", "--freeze-path", FP,
                                    "--require-pathspec"],
                "--pathspec . covers the frozen dir; expect 0/1, watch for 2")


def e2_pathspec_parent_slash():
    d, f = mk("e2")
    wr(d, "tools/round-45/frozen.py", "CHANGED\n")
    r = commit(d, "touch frozen")
    return gate("e2-pathspec-parent-slash", ["--root", d, "--freeze", f, "--rev", r,
                                             "--pathspec", "tools/", "--freeze-path", FP,
                                             "--require-pathspec"],
                "--pathspec tools/ covers the frozen dir; expect 0/1, watch for 2")


def e3_pathspec_parent_noslash():
    d, f = mk("e3")
    wr(d, "tools/round-45/frozen.py", "CHANGED\n")
    r = commit(d, "touch frozen")
    return gate("e3-pathspec-parent-noslash", ["--root", d, "--freeze", f, "--rev", r,
                                               "--pathspec", "tools", "--freeze-path", FP,
                                               "--require-pathspec"],
                "--pathspec tools covers the frozen dir; expect 0/1, watch for 2")


def e4_pathspec_dot_slash_relative():
    d, f = mk("e4")
    wr(d, "tools/round-45/frozen.py", "CHANGED\n")
    r = commit(d, "touch frozen")
    return gate("e4-pathspec-dotslash", ["--root", d, "--freeze", f, "--rev", r,
                                         "--pathspec", "./tools/round-45/",
                                         "--freeze-path", FP, "--require-pathspec"],
                "--pathspec ./tools/round-45/ (valid git) ; watch for 2")


def e5_pathspec_exact():
    d, f = mk("e5")
    wr(d, "tools/round-45/frozen.py", "CHANGED\n")
    r = commit(d, "touch frozen")
    return gate("e5-pathspec-exact", ["--root", d, "--freeze", f, "--rev", r,
                                      "--pathspec", "tools/round-45/",
                                      "--freeze-path", FP, "--require-pathspec"],
                "canonical invocation; expect 1")


def e6_narrow_pathspec_dir_backstop():
    """Pathspec narrower than the frozen dir; the dir-level tree backstop must catch it."""
    d, f = mk("e6")
    wr(d, "tools/round-45/frozen.py", "CHANGED\n")
    r = commit(d, "touch frozen")
    return gate("e6-narrow-pathspec", ["--root", d, "--freeze", f, "--rev", r,
                                       "--pathspec", "tools/round-45/[f]rozen.py",
                                       "--freeze-path", FP, "--require-pathspec"],
                "pathspec glob matches the changed file but not the dir; expect 1")


def e7_narrow_pathspec_other_file():
    """Pathspec magic that matches nothing under the changed file name."""
    d, f = mk("e7")
    wr(d, "tools/round-45/frozen.py", "CHANGED\n")
    r = commit(d, "touch frozen")
    rec = gate("e7-narrow-pathspec-nomatch", ["--root", d, "--freeze", f, "--rev", r,
                                              "--pathspec", "tools/round-45/[a]",
                                              "--freeze-path", FP, "--require-pathspec"],
               "pathspec under fp that matches nothing; dir tree backstop must catch it")
    rec["git_log_that_pathspec"] = g(d, "log", "--name-status", "--format=%h",
                                     f"{f}..{r}", "--", "tools/round-45/[a]").stdout.strip()
    return rec


def e8_narrow_pathspec_trailing_slash_freezepath():
    """Same narrow pathspec, but --freeze-path written with a trailing slash (same dir,
    the way --pathspec is normally spelled). Does the dir backstop still fire?"""
    d, f = mk("e8")
    wr(d, "tools/round-45/frozen.py", "CHANGED\n")
    r = commit(d, "touch frozen")
    rec = gate("e8-narrow-tslash-freezepath",
               ["--root", d, "--freeze", f, "--rev", r,
                "--pathspec", "tools/round-45/[a]", "--freeze-path", "tools/round-45/",
                "--require-pathspec"],
               "narrow pathspec + --freeze-path with trailing slash; expect 1, watch for 0")
    rec["rev_parse_trailing_slash"] = {
        "base:path/": g(d, "rev-parse", f + ":tools/round-45/").returncode,
        "tip:path/": g(d, "rev-parse", r + ":tools/round-45/").returncode,
        "base:path": g(d, "rev-parse", f + ":tools/round-45").stdout.strip(),
        "tip:path": g(d, "rev-parse", r + ":tools/round-45").stdout.strip(),
    }
    return rec


def e9_no_pathspec_at_all():
    """No --pathspec, no --require-pathspec: the documented default whole-tree scan.
    A commit touching only an unrelated path must NOT read as a frozen-path violation."""
    d, f = mk("e9")
    wr(d, "other.txt", "unrelated\n")
    r = commit(d, "unrelated only")
    return gate("e9-no-pathspec-clean-tree", ["--root", d, "--freeze", f, "--rev", r,
                                              "--freeze-path", FP],
                "clean tree, no frozen change, no --pathspec; expect 0")


def e10_no_pathspec_real_violation():
    d, f = mk("e10")
    wr(d, "tools/round-45/frozen.py", "CHANGED\n")
    r = commit(d, "touch frozen")
    return gate("e10-no-pathspec-violation", ["--root", d, "--freeze", f, "--rev", r,
                                              "--freeze-path", FP],
                "no pathspec, real frozen change; expect 1")


def e11_parent_of_frozen_dir_changed_only():
    """Pathspec = parent that also matches a NON-frozen sibling change."""
    d, f = mk("e11")
    wr(d, "tools/round-44/older.py", "CHANGED\n")
    r = commit(d, "touch round-44 sibling only")
    return gate("e11-parent-sibling", ["--root", d, "--freeze", f, "--rev", r,
                                       "--pathspec", "tools/", "--freeze-path", FP],
                "parent pathspec, non-frozen sibling changed; expect 1 (pathspec covers it)")


for fn in (e1_pathspec_dot, e2_pathspec_parent_slash, e3_pathspec_parent_noslash,
           e4_pathspec_dot_slash_relative, e5_pathspec_exact, e6_narrow_pathspec_dir_backstop,
           e7_narrow_pathspec_other_file, e8_narrow_pathspec_trailing_slash_freezepath,
           e9_no_pathspec_at_all, e10_no_pathspec_real_violation,
           e11_parent_of_frozen_dir_changed_only):
    try:
        fn()
    except Exception as exc:
        print(json.dumps({"case": fn.__name__, "driver_error": f"{type(exc).__name__}: {exc}"}))

with open(os.path.join(os.environ["S"], "results-e.json"), "w") as fh:
    json.dump(RESULTS, fh, indent=1)
for r in RESULTS:
    print(r["case"], "exit=%s" % r["exit"], "verdict=%s" % verdict(r))
