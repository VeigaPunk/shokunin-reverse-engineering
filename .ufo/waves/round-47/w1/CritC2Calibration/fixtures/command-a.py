#!/usr/bin/env python3
"""Command A, verbatim from SCORECARD.md's `## Round 1` recipe block, parameterised by rev.

Usage: python3 -I -B command-a.py <rev> [--root LANE]
Prints one JSON line: mapped/knowledge_files/missing/dangling/citation_resolved_rules/
rule_blocks/coverage_score/depth_score, plus per-block resolution so a divergence from
tools/round-47/record.py's depth_pair can be pointed at a block.
"""
import json
import pathlib
import re
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"


def get(path, rev):
    r = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def main():
    global REPO
    rev = sys.argv[1]
    if "--root" in sys.argv:
        REPO = sys.argv[sys.argv.index("--root") + 1]
    paths = subprocess.run(["git", "-C", REPO, "ls-tree", "-r", "--name-only", rev,
                            "--", "corpus/knowledge"],
                           capture_output=True, text=True).stdout.splitlines()
    files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith(".md")}
    section = (get("corpus/README.md", rev) or "").split("## Coverage map\n", 1)[1] \
        .split("\n## ", 1)[0]
    mapped = set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+", section))
    craft = (get("SKILL.md", rev) or "").split("## Queue-drain craft ", 1)[1] \
        .split("\n## ", 1)[0]
    rules = re.split(r"(?m)^- \*\*", craft)[1:]
    pattern = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
    resolved, per = 0, []
    for i, rule in enumerate(rules, 1):
        refs = re.findall(pattern, rule)
        valid = bool(refs)
        for name, first, last in refs:
            body = get("corpus/knowledge/" + name, rev) or ""
            count = len(body.splitlines())
            start, end = int(first or 1), int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        resolved += valid
        per.append({"block": i, "resolved": valid, "knowledge_refs": len(refs),
                    "title": rule.split("\n", 1)[0][:52]})
    if "--repair-demo" in sys.argv:
        # arithmetic only: append one existing corpus/knowledge citation (the first the craft
        # section already cites elsewhere) with its full line range to block 24, then re-count.
        known = sorted({m[0] for m in re.findall(pattern, craft)})
        demo = known[0] if known else None
        count = len((get("corpus/knowledge/" + demo, rev) or "").splitlines()) if demo else 0
        def count_rules(text):
            out = []
            for i, rule in enumerate(re.split(r"(?m)^- \*\*", text)[1:], 1):
                refs = re.findall(pattern, rule)
                valid = bool(refs)
                for name, f, l in refs:
                    c = len((get("corpus/knowledge/" + name, rev) or "").splitlines())
                    st, en = int(f or 1), int(l or f or 1)
                    valid = valid and 1 <= st <= en <= c
                out.append((i, valid))
            return sum(v for _, v in out), len(out), [i for i, v in out if not v]
        anchor = "`plans/round-47-claims.md:45-113`"
        if demo and anchor in craft:
            alt = craft.replace(anchor, anchor + ", `corpus/knowledge/%s:1-%d`" % (demo, count), 1)
            before, after = count_rules(craft), count_rules(alt)
            print(json.dumps({"revision": rev,
                              "citation_used": "corpus/knowledge/%s:1-%d" % (demo, count),
                              "knowledge_line_count": count,
                              "before": {"resolved": before[0], "rules": before[1],
                                         "unresolved": before[2]},
                              "after": {"resolved": after[0], "rules": after[1],
                                        "unresolved": after[2]},
                              "note": "same predicate; one corpus/knowledge citation with a "
                                      "line selector added inside block 24"}, indent=1))
            return 0
        print(json.dumps({"reason": "anchor or citation unavailable"}))
        return 2
    print(json.dumps({"revision": rev, "mapped": len(files & mapped),
                      "knowledge_files": len(files), "missing": sorted(files - mapped),
                      "dangling": sorted(mapped - files),
                      "citation_resolved_rules": resolved, "rule_blocks": len(rules),
                      "coverage_score": round(10 * len(files & mapped) / len(files), 2),
                      "depth_score": round(10 * resolved / len(rules), 2),
                      "unresolved_blocks": [p for p in per if not p["resolved"]]},
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
