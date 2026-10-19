#!/usr/bin/env python3
"""EX-45 sim-landing check (scratch).

Build a scratch Git repo holding the WORKTREE bytes of every file the landed
pointer table cites (citing files + extracted targets), commit it, and probe the
landed table against that rev. This grades the table against the state that will
be committed (C2's revised custody README/tool, any C1 landing) rather than
against HEAD's committed bytes -- the post-landing surface.

Usage: sim-landing.py --root REPO --table TABLE --expected EXPECTED --out TXT
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile


def sh(args):
    return subprocess.run(args, capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--table", required=True)
    ap.add_argument("--expected", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    probe = os.path.join(root, ".ufo/gates/citation-drift/citation-drift-probe.py")
    table = json.load(open(os.path.join(root, a.table)))
    paths = set()
    for e in table.get("entries", []) + table.get("quoted", []):
        paths.add(e["file"])
        if e.get("target"):
            paths.add(e["target"])
    base = tempfile.mkdtemp(prefix="ex45-simland-", dir="/var/tmp")
    sh(["git", "init", "-q", base])
    missing = []
    for p in sorted(paths):
        src = os.path.join(root, p)
        if not os.path.isfile(src):
            missing.append(p)
            continue
        dst = os.path.join(base, p)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    # probe + table + expected are read from disk paths (not the fixture tree)
    sh(["git", "-C", base, "add", "-A"])
    sh(["git", "-C", base, "-c", "user.email=e@x", "-c", "user.name=e",
        "commit", "-qm", "sim-landing (worktree bytes)"])
    tp = os.path.join(base, "table-copy.json")
    ep = os.path.join(base, "expected-copy.json")
    shutil.copy2(os.path.join(root, a.table), tp)
    shutil.copy2(os.path.join(root, a.expected), ep)
    out = []
    for mode in (["--strict"], []):
        p = sh(["python3", probe, "--root", base, "--rev", "HEAD", "--table", tp,
                "--expected", ep] + mode)
        txt = p.stdout.decode("utf-8", "replace")
        out.append("== mode %s rc=%d" % (" ".join(mode) or "(default)", p.returncode))
        out.append(txt.rstrip())
    out.append("== worktree-missing files: %s" % (missing or "none"))
    out.append("== files copied: %d" % (len(paths) - len(missing)))
    txt = "\n".join(out)
    print(txt)
    if a.out:
        open(a.out, "w").write(txt + "\n")
    shutil.rmtree(base, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())