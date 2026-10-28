#!/usr/bin/env python3
"""Attack (c): pathnames that break the `--name-status` line parser (no -z)."""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.environ["S"])
from run import RESULTS, assert_toplevel, commit, g, gate, newrepo, utc, verdict, wr

BASE = {"frozen/a.txt": "alpha\n", "other.txt": "o\n"}
ARGS = ["--pathspec", "frozen/", "--freeze-path", "frozen", "--require-pathspec"]


def c_newline():
    """A frozen path whose name contains a newline, touched in REV."""
    d = newrepo("c1", BASE)
    assert_toplevel(d)
    name = "frozen/nl\nname.txt"
    wr(d, name, "v1\n")
    f = commit(d, "freeze")
    wr(d, name, "v2\n")
    r = commit(d, "touch newline name")
    rec = gate("c1-newline-name", ["--root", d, "--freeze", f, "--rev", r, *ARGS],
               "frozen name with \\n touched; expect 1")
    rec["raw_log"] = g(d, "log", "-m", "--diff-merges=first-parent", "--name-status",
                       "--format=%x00%H", f"{f}..{r}", "--", "frozen/").stdout
    return rec


def c_tab():
    """A frozen path whose name contains a tab, touched in REV."""
    d = newrepo("c2", BASE)
    assert_toplevel(d)
    name = "frozen/tab\tname.txt"
    wr(d, name, "v1\n")
    f = commit(d, "freeze")
    wr(d, name, "v2\n")
    r = commit(d, "touch tab name")
    rec = gate("c2-tab-name", ["--root", d, "--freeze", f, "--rev", r, *ARGS],
               "frozen name with \\t touched; expect 1")
    rec["raw_log"] = g(d, "log", "-m", "--diff-merges=first-parent", "--name-status",
                       "--format=%x00%H", f"{f}..{r}", "--", "frozen/").stdout
    return rec


def c_tab_restored():
    """Tab name: touched then restored -> `restored` arm needs exact path equality."""
    d = newrepo("c3", BASE)
    assert_toplevel(d)
    name = "frozen/tab\tname.txt"
    wr(d, name, "v1\n")
    f = commit(d, "freeze")
    wr(d, name, "tampered\n")
    commit(d, "tamper")
    wr(d, name, "v1\n")
    r = commit(d, "restore")
    return gate("c3-tab-restored", ["--root", d, "--freeze", f, "--rev", r, *ARGS],
                "tab name tampered then restored; expect 1 via touched")


def c_u2028_quotepath_off():
    """core.quotePath=false + a name containing U+2028: str.splitlines() splits on it."""
    d = newrepo("c4", BASE)
    assert_toplevel(d)
    g(d, "config", "core.quotePath", "false")
    name = "frozen/ls\u2028name.txt"
    wr(d, name, "v1\n")
    f = commit(d, "freeze")
    wr(d, name, "v2\n")
    r = commit(d, "touch u2028 name")
    raw = g(d, "log", "-m", "--diff-merges=first-parent", "--name-status",
            "--format=%x00%H", f"{f}..{r}", "--", "frozen/").stdout
    rec = gate("c4-u2028-quotepath-off", ["--root", d, "--freeze", f, "--rev", r, *ARGS],
               "U+2028 name, quotePath=false; expect 1 (check the receipt path)")
    rec["raw_log_repr"] = repr(raw)
    rec["raw_log_line_count_splitlines"] = len(raw.splitlines())
    rec["raw_log_line_count_split_nl"] = len(raw.split("\n"))
    return rec


def c_backslash():
    """A name containing a backslash: git quotes it; rev-parse gets the quoted form."""
    d = newrepo("c5", BASE)
    assert_toplevel(d)
    name = "frozen/bs\\name.txt"
    wr(d, name, "v1\n")
    f = commit(d, "freeze")
    wr(d, name, "v2\n")
    r = commit(d, "touch backslash name")
    rec = gate("c5-backslash-name", ["--root", d, "--freeze", f, "--rev", r, *ARGS],
               "backslash name touched; expect 1")
    rec["raw_log"] = g(d, "log", "-m", "--diff-merges=first-parent", "--name-status",
                       "--format=%x00%H", f"{f}..{r}", "--", "frozen/").stdout
    return rec


def c_clean_weird():
    """False-positive probe: weird-named frozen file present and untouched."""
    d = newrepo("c6", BASE)
    assert_toplevel(d)
    writenames = ["frozen/nl\nname.txt", "frozen/tab\tname.txt"]
    for n in writenames:
        wr(d, n, "v1\n")
    f = commit(d, "freeze")
    wr(d, "other.txt", "changed\n")
    r = commit(d, "unrelated")
    return gate("c6-weird-but-clean", ["--root", d, "--freeze", f, "--rev", r, *ARGS],
                "weird names present, unrelated commit only; expect 0")


def c_new_weird_after_freeze():
    """A weird-named path ADDED inside the frozen dir after the freeze."""
    d = newrepo("c7", BASE)
    assert_toplevel(d)
    f = commit(d, "freeze")
    wr(d, "frozen/new\tfile.txt", "added\n")
    r = commit(d, "add weird file")
    return gate("c7-add-weird", ["--root", d, "--freeze", f, "--rev", r, *ARGS],
                "A-status weird name inside frozen dir; expect 1")


for fn in (c_newline, c_tab, c_tab_restored, c_u2028_quotepath_off, c_backslash,
           c_clean_weird, c_new_weird_after_freeze):
    try:
        fn()
    except Exception as exc:
        print(json.dumps({"case": fn.__name__, "driver_error": f"{type(exc).__name__}: {exc}"}))

with open(os.path.join(os.environ["S"], "results-c.json"), "w") as fh:
    json.dump(RESULTS, fh, indent=1)
for r in RESULTS:
    print(r["case"], "exit=%s" % r["exit"], "verdict=%s" % verdict(r))
