#!/usr/bin/env python3
"""EX-05 (c1, round 2): command A (SCORECARD.md recipe A) over a WORKTREE file.

Recipe A reads `git show <REV>:SKILL.md`; the scratch SKILL.md under test is
not a git object, so this variant reads the given worktree file instead and
resolves citations against the worktree corpus/knowledge. The only deviation
from recipe A is the SKILL.md source; corpus line counts come from the
worktree as well (equal to the committed trees for every file in scope here).

Usage: python3 commandA-worktree.py [path-to-SKILL.md]
"""
import json
import pathlib
import re
import sys


def main(skill_path="SKILL.md"):
    root = pathlib.Path(".")
    paths = sorted(p for p in root.glob("corpus/knowledge/*.md"))
    files = {p.stem for p in paths}
    readme = (root / "corpus/README.md").read_text(encoding="utf-8")
    section = readme.split("## Coverage map\n", 1)[1].split("\n## ", 1)[0]
    mapped = set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+", section))
    text = pathlib.Path(skill_path).read_text(encoding="utf-8")
    craft = text.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    rules = re.split(r"(?m)^- \*\*", craft)[1:]
    pattern = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
    resolved = 0
    for rule in rules:
        refs = re.findall(pattern, rule)
        valid = bool(refs)
        for name, first, last in refs:
            p = root / "corpus/knowledge" / name
            if not p.exists():
                valid = False
                continue
            count = len(p.read_text(encoding="utf-8").splitlines())
            start, end = int(first or 1), int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        resolved += valid
    print(json.dumps({"skill_source": skill_path, "mapped": len(files & mapped),
                      "knowledge_files": len(files),
                      "missing": sorted(files - mapped),
                      "dangling": sorted(mapped - files),
                      "citation_resolved_rules": resolved,
                      "rule_blocks": len(rules),
                      "coverage_score": round(10 * len(files & mapped) / len(files), 2),
                      "depth_score": round(10 * resolved / len(rules), 2)},
                     sort_keys=True))


if __name__ == "__main__":
    main(*sys.argv[1:])
