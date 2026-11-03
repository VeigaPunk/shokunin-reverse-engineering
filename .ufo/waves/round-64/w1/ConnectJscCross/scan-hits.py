#!/usr/bin/env python3
"""scan-hits.py - reproduce the ConnectJscCross r64 w1 surface scan.

Predicate (the seat order, verbatim):
    grep -rn -i -E 'jsc|view8|d8 |bytenode|ignition|v8 ?bytecode|loadjsc' \
        --include='*.md' --include='*.json' --include='*.py' .

over the lane, excluding .git/.jj/.ruff_cache and .ufo/waves/round-6[0-3].

Classification is path-based and mechanical (the six ordered class names of the seat order);
PROVINCE.md and LOG.md have no slot in that enum, so they are classed `other` with a sub-kind
and reported in full rather than dropped.

Usage:
    python3 -I -B scan-hits.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
        --out hits.tsv [--canonical-only]

Output columns: file<TAB>line<TAB>class<TAB>sub-kind<TAB>matched-tokens<TAB>snippet
Exit: 0 always; the scan is a read. Missing --root is a usage error (exit 2).

Checked at 2026-11-03: 4283 rows / 652 files; 326 canonical rows / 46 files.
"""
from __future__ import annotations

import argparse
import collections
import os
import re
import sys

PREDICATE = re.compile(r"jsc|view8|d8 |bytenode|ignition|v8 ?bytecode|loadjsc", re.I)
TOKENS = [
    ("jsc2js", re.compile(r"jsc2js", re.I)),
    ("view8", re.compile(r"view8", re.I)),
    ("loadjsc", re.compile(r"loadjsc", re.I)),
    ("bytenode", re.compile(r"bytenode", re.I)),
    ("ignition", re.compile(r"ignition", re.I)),
    ("v8-bytecode", re.compile(r"v8 ?bytecode", re.I)),
    ("jsc", re.compile(r"jsc", re.I)),
    ("d8-space", re.compile(r"d8 ", re.I)),
]
EXCLUDED_DIRS = {".git", ".jj", ".ruff_cache", "round-60", "round-61", "round-62", "round-63"}
EXTS = (".md", ".json", ".py")


def classify(rel: str) -> tuple[str, str]:
    parts = rel.split("/")
    if parts[0] == "SKILL.md":
        return "own-lane-skill", "skill"
    if parts[0] == "SCORECARD.md":
        return "own-lane-scorecard", "scorecard"
    if parts[0] == "LOG.md":
        return "other", "lane-log"
    if parts[0] == "PROVINCE.md":
        return "other", "province"
    if parts[0] in ("AGENTS.md", "MINT.md", "SHONEN.md", "README.md", "EXAMPLE.kama.md"):
        return "other", "lane-root-doc"
    if parts[0] == "plans":
        return "other", "frozen-plan"
    if parts[0] == "corpus":
        if len(parts) > 1 and parts[1] == "knowledge":
            return "own-lane-knowledge", "entry"
        if len(parts) > 1 and parts[1] == "lessons":
            return "own-lane-knowledge", "lesson"
        if len(parts) > 1 and parts[1] in ("SOURCES.md", "README.md", "QUALITY.md"):
            return "own-lane-knowledge", "registry-index"
        if len(parts) > 1 and parts[1] == "evidence":
            return "staged-elsewhere", "copied-control-tree"
        return "own-lane-knowledge", "other-corpus"
    if parts[0] == "tools":
        return "own-lane-tooling", "tool"
    if parts[0] == ".ufo":
        return "staged-elsewhere", "wave-artifact"
    if parts[0] in ("kaidoku-r26", "kaidoku-r51", "res", "evidence"):
        return "staged-elsewhere", "lane-legacy-dir"
    return "other", "unclassified"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--canonical-only", action="store_true",
                    help="drop staged-elsewhere rows from the output")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    rows: list[tuple[str, int, str, str, str, str]] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS and not d.startswith(".git")]
        for name in filenames:
            if not name.endswith(EXTS):
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            if any(part in EXCLUDED_DIRS for part in rel.split(os.sep)):
                continue
            try:
                with open(full, encoding="utf-8", errors="replace") as fh:
                    lines = fh.read().splitlines()
            except OSError:
                continue
            for lineno, line in enumerate(lines, 1):
                if not PREDICATE.search(line):
                    continue
                cls, kind = classify(rel)
                if args.canonical_only and cls == "staged-elsewhere":
                    continue
                toks = "|".join(n for n, rx in TOKENS if rx.search(line))
                rows.append((rel, lineno, cls, kind, toks, line.strip()[:150]))

    with open(args.out, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write("\t".join(str(v) for v in row) + "\n")
    counts = collections.Counter(r[2] for r in rows)
    print(f"rows={len(rows)} files={len({r[0] for r in rows})} classes={dict(sorted(counts.items()))}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
