#!/usr/bin/env python3
"""Frozen-path preflight: red before a commit that touches a claim's frozen paths.

M44-2 fix (corpus/lessons/round-44.md). The round-44 freeze-integrity rule was
enforced only when a counter scored, so a post-freeze commit could land files
under a frozen directory and the loss was discovered at scoring time. This gate
is meant to run on every candidate revision BEFORE the commit is treated as
landed.

Exit codes: 0 clean (no commit in FREEZE..REV touches a frozen path and every
frozen blob is unchanged), 1 violation, 2 could-not-evaluate.
"""
import argparse
import json
import os
import subprocess
import sys


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--freeze", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--pathspec", action="append", default=[],
                    help="frozen pathspec; repeatable. Default: none (tree backstop only)")
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)

    root = os.path.abspath(args.root)
    probe = git(root, "rev-parse", "--verify", args.freeze + "^{commit}")
    if probe.returncode != 0:
        return fail(2, "unknown freeze revision", args)
    base = probe.stdout.strip()
    probe = git(root, "rev-parse", "--verify", args.rev + "^{commit}")
    if probe.returncode != 0:
        return fail(2, "unknown rev revision", args)
    rev = probe.stdout.strip()
    probe = git(root, "merge-base", "--is-ancestor", base, rev)
    if probe.returncode != 0:
        return fail(2, "freeze is not an ancestor of rev", args)

    pathspec = ["--"] + args.pathspec if args.pathspec else []
    log = git(root, "log", "-m", "--diff-merges=first-parent", "--name-status",
              "--format=%x00%H", f"{base}..{rev}", *pathspec)
    if log.returncode != 0:
        return fail(2, "git log failed", args)

    touched = []
    commit = None
    for line in log.stdout.splitlines():
        if line.startswith("\x00"):
            commit = line[1:].strip()
            continue
        parts = line.split("\t")
        if len(parts) < 2 or not commit:
            continue
        status = parts[0]
        if status[:1] in {"M", "D", "R", "T", "U", "A", "C"}:
            for path in parts[1:]:
                touched.append({"commit": commit, "status": status, "path": path})

    # Tree backstop: every frozen path present at FREEZE must hash identically at REV.
    blob_changed = []
    if pathspec:
        listing = git(root, "ls-tree", "-r", "--name-only", base, *pathspec)
        if listing.returncode != 0:
            return fail(2, "ls-tree at freeze failed", args)
        for path in sorted(filter(None, listing.stdout.splitlines())):
            a = git(root, "rev-parse", f"{base}:{path}")
            b = git(root, "rev-parse", f"{rev}:{path}")
            if a.returncode or b.returncode or a.stdout != b.stdout:
                blob_changed.append(path)

    ok = not touched and not blob_changed
    receipt = {
        "gate": "frozen-path-preflight",
        "freeze": base,
        "rev": rev,
        "pathspec": args.pathspec,
        "touched": touched,
        "blob_changed": blob_changed,
        "verdict": "clean" if ok else "frozen_path_changed",
    }
    if args.json_out:
        with open(args.json_out, "w") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True)
    print(json.dumps(receipt, sort_keys=True))
    return 0 if ok else 1


def fail(code, reason, args):
    receipt = {"gate": "frozen-path-preflight", "verdict": "could_not_evaluate",
               "reason": reason, "exit_code": code}
    if args.json_out:
        with open(args.json_out, "w") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True)
    print(json.dumps(receipt, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
