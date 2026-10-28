#!/usr/bin/env python3
"""Recipe A, verbatim from SCORECARD.md `## Measurement recipes` A, run in a given repo.

`python3 -I -B recipeA.py <repo-dir> <rev>` -> the recipe's own JSON line.
"""
import json
import pathlib
import re
import subprocess
import sys

repo, rev = sys.argv[1], sys.argv[2]


def git(*args):
    return subprocess.check_output(["git", "-C", repo, *args], text=True)


def get(path):
    return git("show", f"{rev}:{path}")


paths = git("ls-tree", "-r", "--name-only", rev, "--", "corpus/knowledge").splitlines()
files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith(".md")}
section = get("corpus/README.md").split("## Coverage map\n", 1)[1].split("\n## ", 1)[0]
mapped = set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+", section))
craft = get("SKILL.md").split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
rules = re.split(r"(?m)^- \*\*", craft)[1:]
pattern = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
resolved = 0
per_rule = []
for rule in rules:
    refs = re.findall(pattern, rule)
    valid = bool(refs)
    for name, first, last in refs:
        try:
            count = len(get("corpus/knowledge/" + name).splitlines())
            start, end = int(first or 1), int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        except subprocess.CalledProcessError:
            valid = False
    resolved += valid
    per_rule.append(1 if valid else 0)
print(json.dumps({"revision": rev, "mapped": len(files & mapped),
                  "knowledge_files": len(files), "missing": sorted(files - mapped),
                  "dangling": sorted(mapped - files), "citation_resolved_rules": resolved,
                  "rule_blocks": len(rules),
                  "coverage_score": round(10 * len(files & mapped) / len(files), 2),
                  "depth_score": round(10 * resolved / len(rules), 2),
                  "uncited_rules": [i + 1 for i, v in enumerate(per_rule) if not v]},
                 sort_keys=True))
