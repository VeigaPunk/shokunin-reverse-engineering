#!/usr/bin/env python3
"""Third batch: unreadable-card matrix on the green C2 fixture, C2 side-branch rev,
and the corrected is-a-directory --json-out probe."""
import json, os, subprocess, sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/MutExitCodes")
import drive2 as D
from drive2 import sh, repo, put, commit, run, green_c2, S, C2

def clone(src, prefix):
    d = D.tempfile.mkdtemp(dir=S, prefix=prefix)
    sh(["git", "-C", d, "clone", "-q", src, "."], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "r47 fixture")):
        sh(["git", "-C", d, "config", k, v], check=True)
    return d

def main():
    d, base, land = green_c2()
    rec = D.run("c2-green-control", ["python3", "-I", "-B", os.path.join(d, "tools/round-47/record.py"),
                                     "--root", d, "--rev", land, "--no-battery"], 0, "control")
    assert rec["exit"] == 0

    # --- unreadable SCORECARD at rev, five ways -------------------------------------
    for name, mutate in (
        ("binary-utf8", lambda dd: put(dd, {"SCORECARD.md": b"\xff\xfe# card\n\x00\x80\n"})),
        ("is-a-directory", lambda dd: (os.remove(os.path.join(dd, "SCORECARD.md")),
                                       put(dd, {"SCORECARD.md/part.md": "x\n"}))),
        ("deleted", lambda dd: os.remove(os.path.join(dd, "SCORECARD.md"))),
    ):
        dd = clone(d, "card-" + name + "-")
        mutate(dd)
        r = commit(dd, "card " + name)
        D.run("c2-card-" + name, ["python3", "-I", "-B",
                                  os.path.join(dd, "tools/round-47/record.py"),
                                  "--root", dd, "--rev", r, "--no-battery"], 2,
              "SCORECARD unreadable at rev")

    # blob object removed, tree intact
    dd = clone(d, "card-objgone-")
    oid = sh(["git", "-C", dd, "rev-parse", "HEAD:SCORECARD.md"]).stdout.strip()
    obj = os.path.join(dd, ".git/objects", oid[:2], oid[2:])
    loose = os.path.exists(obj)
    if loose:
        os.chmod(obj, 0o600); os.remove(obj)
    D.run("c2-card-object-missing", ["python3", "-I", "-B",
                                     os.path.join(dd, "tools/round-47/record.py"),
                                     "--root", dd, "--rev", "HEAD", "--no-battery"], 2,
          "blob %s removed from .git/objects (loose=%s)" % (oid, loose))

    # worktree unreadable while committed bytes are fine: the graded surface is the object
    dd = clone(d, "card-perm-")
    os.chmod(os.path.join(dd, "SCORECARD.md"), 0o000)
    D.run("c2-card-worktree-chmod000", ["python3", "-I", "-B",
                                        os.path.join(dd, "tools/round-47/record.py"),
                                        "--root", dd, "--rev", "HEAD", "--no-battery"], 0,
          "worktree unreadability is invisible to a git-object reader")

    # --- --json-out target that IS a directory inside the fixture -------------------
    os.makedirs(os.path.join(d, "logs", "keep"), exist_ok=True)
    open(os.path.join(d, "logs", "keep", ".k"), "w").write("k\n")
    D.run("c2-jsonout-is-a-directory", [
        "python3", "-I", "-B", os.path.join(d, "tools/round-47/record.py"), "--root", d,
        "--rev", land, "--no-battery", "--json-out", os.path.join(d, "logs")], 2,
        "target is a directory: out_path accepts it, emit() cannot open it")

    # --- a rev on a side branch off the landing ------------------------------------
    dd = clone(d, "side-land-")
    sh(["git", "-C", dd, "checkout", "-q", "-b", "side", "HEAD"], check=True)
    put(dd, {"tools/x/keep.md": "x\nside\n"})
    side = commit(dd, "side after landing")
    D.run("c2-rev-side-branch-off-landing", [
        "python3", "-I", "-B", os.path.join(dd, "tools/round-47/record.py"),
        "--root", dd, "--rev", side, "--no-battery"], 0,
        "no freeze and no ancestry arm: any satisfying rev scores met")

    with open(os.path.join(S, "receipts3.jsonl"), "w") as fh:
        for x in D.OUT:
            fh.write(json.dumps(x) + "\n")
    print("\nPROBES=%d" % len(D.OUT), file=sys.stderr)

main()
