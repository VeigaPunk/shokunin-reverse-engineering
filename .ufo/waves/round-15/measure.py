#!/usr/bin/env python3
"""Count round-15 observables from immutable lane Git objects, not the worktree.

Usage: python3 .ufo/waves/round-15/measure.py <revision>

Reads only committed bytes at <revision> through `git show` and `git ls-tree`.
Every C1/C2 field is a bounded presence proxy: 1 means the named file or
wording exists in that commit, never that it is sourced, correct, admitted, or
that any target, provider, or gate was exercised. Map and source figures are
bookkeeping counts, not domain coverage. Exit 0 after a completed census; 2 on
usage or a missing structural anchor. This script computes no verdict.
"""
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

C1_ENTRY = "corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md"
C1_TOOL = ".ufo/waves/round-15/snapshot-inventory.py"
C2_MARKER = "Round-15 correction \u2014 virtual-dispatch advisory"  # U+2014 em dash
C2_PHRASE = re.compile(r"must not be submitted", re.IGNORECASE)
ROW17 = re.compile(r"^\|\s*17\s*\|")
SOURCE_ROW = re.compile(r"^\|\s*S\d{3,}\s*\|")
MAP_ENTRY = re.compile(r"2026-10-\d{2}-[a-z0-9-]+")


def git(*args):
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], text=True, encoding="utf-8"
    )


def fail(message):
    print(f"measure.py: {message}", file=sys.stderr)
    raise SystemExit(2)


def main():
    if len(sys.argv) != 2:
        fail("usage: measure.py <revision>")
    try:
        revision = git(
            "rev-parse", "--verify", f"{sys.argv[1]}^{{commit}}"
        ).strip()
    except (subprocess.CalledProcessError, OSError) as error:
        fail(f"cannot resolve commit {sys.argv[1]!r}: {error}")

    def get(path):
        try:
            return git("show", f"{revision}:{path}")
        except (subprocess.CalledProcessError, OSError):
            fail(f"cannot read {path} at {revision}")

    paths = set(git("ls-tree", "-r", "--name-only", revision).splitlines())
    quality = get("corpus/QUALITY.md")
    lesson = get("corpus/lessons/round-14.md")
    readme = get("corpus/README.md")
    sources = get("corpus/SOURCES.md")

    try:
        coverage = readme.split("## Coverage map\n", 1)[1].split("\n## ", 1)[0]
    except IndexError:
        fail("corpus/README.md has no delimited '## Coverage map' section")

    knowledge = {
        Path(path).stem
        for path in paths
        if path.startswith("corpus/knowledge/") and path.endswith(".md")
    }
    mapped = set(MAP_ENTRY.findall(coverage))

    rows = [
        line.split("|")
        for line in sources.splitlines()
        if SOURCE_ROW.match(line)
    ]
    if not rows:
        fail("corpus/SOURCES.md has no source rows")

    def cell(row, index):
        return row[index].strip() if index < len(row) else ""

    row17 = next((line for line in quality.splitlines() if ROW17.match(line)), "")

    result = {
        "revision": revision,
        "C1_round15_knowledge_entry": int(C1_ENTRY in paths),
        "C1_snapshot_inventory_tool": int(C1_TOOL in paths),
        "C2_quality_row17_manual_only_wording": int(
            bool(row17) and bool(C2_PHRASE.search(row17))
        ),
        "C2_round14_lesson_correction_marker": int(C2_MARKER in lesson),
        "knowledge_files": len(knowledge),
        "mapped": len(knowledge & mapped),
        "missing": sorted(knowledge - mapped),
        "dangling": sorted(mapped - knowledge),
        "sources_rows": len(rows),
        "tiers": dict(sorted(Counter(cell(row, 4) for row in rows).items())),
        "statuses": dict(sorted(Counter(cell(row, 8) for row in rows).items())),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
