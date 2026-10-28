#!/usr/bin/env python3
"""Measures the two `## Owned axes` fractions at a revision, two ways.

`recipe_a` is SCORECARD.md's "Measurement recipes / A" body verbatim (only the
revision comes from argv, as in the card). `depth_pair` / `coverage_pair` are
the frozen `tools/round-47/record.py` derivations the R47-C2 counter actually
uses for the `axes` atoms.

Usage: python3 -I -B measure_axes.py --root <lane> --rev <REV>
"""
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys


def recipe_a(root, rev):
    """SCORECARD.md measurement recipe A, verbatim except cwd comes from --root."""
    def get(path):
        return subprocess.check_output(["git", "-C", root, "show", f"{rev}:{path}"], text=True)

    paths = subprocess.check_output(["git", "-C", root, "ls-tree", "-r", "--name-only", rev,
                                     "--", "corpus/knowledge"], text=True).splitlines()
    files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith(".md")}
    section = get("corpus/README.md").split("## Coverage map\n", 1)[1].split("\n## ", 1)[0]
    mapped = set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+", section))
    craft = get("SKILL.md").split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    rules = re.split(r"(?m)^- \*\*", craft)[1:]
    pattern = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
    resolved = 0
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
    return {"mapped": len(files & mapped), "knowledge_files": len(files),
            "missing": sorted(files - mapped), "dangling": sorted(mapped - files),
            "citation_resolved_rules": resolved, "rule_blocks": len(rules)}


def counter_pairs(root, rev):
    sys.path.insert(0, os.path.join(root, "tools", "round-47"))
    sys.path.insert(0, os.path.join(root, "tools", "round-46"))
    import gate  # noqa: PLC0415
    import record  # noqa: PLC0415

    files = lambda p: gate.show(root, rev, p)  # noqa: E731
    return {"coverage": list(record.coverage_pair(root, rev, files)),
            "depth": list(record.depth_pair(files))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", required=True)
    args = ap.parse_args()
    resolved = subprocess.run(["git", "-C", args.root, "rev-parse", "--verify",
                               args.rev + "^{commit}"], capture_output=True, text=True)
    if resolved.returncode != 0:
        print(json.dumps({"reason": "unknown revision", "rev": args.rev}))
        return 2
    rev = resolved.stdout.strip()
    out = {"rev": rev, "recipe_a": recipe_a(args.root, rev),
           "record_pairs": counter_pairs(args.root, rev)}
    out["recipe_a_depth_fraction"] = "%d/%d" % (
        out["recipe_a"]["citation_resolved_rules"], out["recipe_a"]["rule_blocks"])
    out["recipe_a_coverage_fraction"] = "%d/%d" % (
        out["recipe_a"]["mapped"], out["recipe_a"]["knowledge_files"])
    out["record_depth_fraction"] = "%d/%d" % tuple(out["record_pairs"]["depth"])
    out["record_coverage_fraction"] = "%d/%d" % tuple(out["record_pairs"]["coverage"])
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
