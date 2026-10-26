#!/usr/bin/env python3
"""citation-gate.py — dead-pointer gate for lane lesson/record citations.

Class (round-41 closure D2): a committed record (lesson, report, score) cites a
wave-report path that does not resolve as a git object at the revision that
contains the record.  This gate reads the record's bytes at `--rev` and checks
every wave-relative pointer token against the tree at that same revision:

  * shorthand tokens `w1/...`, `w2/...`, `l1/...`, `l2/...` are resolved
    against `--wave-root` (default `.ufo/waves/round-41`);
  * explicit tokens `.ufo/waves/<round>/w1/...` (etc.) are resolved against the
    repository root;
  * brace groups `{1..6}` / `{A,B,C,D}` are expanded and every alternative must
    resolve.

Resolution uses `git cat-file -e <rev>:<path>` (a path is resolvable iff it
names an existing blob or tree in that commit).  Exit 0 when every pointer
resolves; exit 1 with the dead-pointer list otherwise.  Only the Python
standard library and `git` (read-only) are used.
"""
import argparse
import re
import subprocess
import sys
from pathlib import PurePosixPath

SHORTHAND = re.compile(r"(?<![\w./-])(?:w[12]|l1|l2)/\S+")
EXPLICIT = re.compile(
    r"(?<![\w./-])\.ufo/waves/[\w./-]+/(?:w[12]|l1|l2)/\S+"
)
_TRAIL = ",.;:)]}\"'`*"
_BARE = re.compile(r"^[\w./-]+$")


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", repo, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def expand_braces(tok):
    """Expand `{1..6}` / `{A,B,C,D}` brace groups (as in the lessons)."""
    m = re.search(r"\{([^}]*)\}", tok)
    if not m:
        return [tok]
    inner = m.group(1)
    parts = []
    if "," not in inner and ".." in inner:
        lo, hi = inner.split("..", 1)
        if lo.isdigit() and hi.isdigit():
            parts = [str(i) for i in range(int(lo), int(hi) + 1)]
    if not parts:
        parts = inner.split(",")
    head, tail = tok[: m.start()], tok[m.end():]
    return [head + p + tail for p in parts]


def resolvable(repo, rev, path):
    return git(repo, "cat-file", "-e", f"{rev}:{path}").returncode == 0


def candidates(repo, rev, tok, wave_root):
    """Return [(cand_path, ok)] for a token (brace-expanded)."""
    out = []
    for rt in expand_braces(tok):
        cand = rt if rt.startswith(".ufo/") else str(PurePosixPath(wave_root) / rt)
        out.append((cand, resolvable(repo, rev, cand)))
    return out


def scan(repo, rev, text, wave_root):
    seen = set()
    found = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for tok in SHORTHAND.findall(line) + EXPLICIT.findall(line):
            tok = tok.rstrip(_TRAIL)
            if not _BARE.match(tok):
                continue
            key = (lineno, tok)
            if key in seen:
                continue
            seen.add(key)
            found.append((lineno, line.strip(), tok, candidates(repo, rev, tok, wave_root)))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--wave-root", default=".ufo/waves/round-41")
    ap.add_argument("--file", action="append", required=True,
                    help="record path (repo-relative), scanned at --rev")
    ap.add_argument("--list", action="store_true",
                    help="print every token with resolution status")
    args = ap.parse_args()

    problems = []
    total = 0
    for rel in args.file:
        out = git(args.repo, "show", f"{args.rev}:{rel}")
        if out.returncode != 0:
            print(f"FATAL: cannot read {args.rev}:{rel}")
            return 2
        for lineno, line, tok, cands in scan(args.repo, args.rev, out.stdout,
                                             args.wave_root):
            total += 1
            for cand, ok in cands:
                if args.list:
                    flag = "OK  " if ok else "DEAD"
                    print(f"{flag} {rel}:{lineno} {tok} -> {cand}")
                if not ok:
                    problems.append((rel, lineno, tok, cand, line))

    print(f"citations checked: {total}")
    for rel, lineno, tok, cand, line in problems:
        print(f"DEAD {rel}:{lineno} {tok} (not in tree at {args.rev})")
        print(f"      line: {line[:200]}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
