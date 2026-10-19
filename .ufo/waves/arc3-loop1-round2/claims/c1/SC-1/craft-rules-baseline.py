#!/usr/bin/env python3
"""SC-1 (c1, round 2, scribe): rule-block baseline/compare for the
Queue-drain craft section of SKILL.md.

The section is extracted the same way command A extracts it (split on
'## Queue-drain craft ' up to the next '\\n## '), then split on rule starts
'(?m)^- \\*\\*'. Each rule block = its lines up to (exclusive) the next rule
start or section end, with trailing newlines stripped, so a byte-identity
comparison on the prior blocks is insensitive to trailing blank-line
normalization at the section tail.

Modes:
  --root DIR --rev REV             baseline (git object) -> JSON to stdout
  --compare BASE.json [--skill F]  compare a candidate SKILL.md against BASE

Exit 0 always unless a mode input is unusable (exit 2).
"""
import argparse
import hashlib
import json
import subprocess
import sys

MARK = "## Queue-drain craft "
RULE = "^- **"


def section_of(text):
    if MARK not in text:
        return None
    tail = text.split(MARK, 1)[1]
    return MARK + tail.split("\n## ", 1)[0]


def blocks_of(section):
    lines = section.split("\n")
    starts = [i for i, ln in enumerate(lines) if ln.startswith("- **")]
    blocks = []
    for n, i in enumerate(starts):
        j = starts[n + 1] if n + 1 < len(starts) else len(lines)
        body = "\n".join(lines[i:j]).rstrip("\n")
        title = lines[i].split("**")[1] if "**" in lines[i] else lines[i]
        blocks.append({"index": n + 1, "title": title[:70],
                       "sha256": hashlib.sha256(body.encode()).hexdigest(),
                       "lines": body.count("\n") + 1})
    return blocks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--skill", default="SKILL.md")
    ap.add_argument("--compare")
    a = ap.parse_args()
    if a.compare:
        base = json.load(open(a.compare))
        text = open(a.skill, encoding="utf-8").read()
    else:
        if not a.rev:
            print("need --rev or --compare", file=sys.stderr)
            return 2
        r = subprocess.run(["git", "-C", a.root, "show", f"{a.rev}:{a.skill}"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("revision_unresolvable: %s" % r.stderr.strip(), file=sys.stderr)
            return 2
        text = r.stdout
    section = section_of(text)
    if section is None:
        print("section_absent", file=sys.stderr)
        return 2
    blocks = blocks_of(section)
    out = {
        "skill": a.skill,
        "section_lines": section.count("\n") + 1,
        "section_sha256": hashlib.sha256(section.encode()).hexdigest(),
        "rule_count": len(blocks),
        "blocks": blocks,
    }
    if a.compare:
        base_blocks = base["blocks"]
        n = min(len(base_blocks), len(blocks))
        diffs = [{"index": b["index"], "title": b["title"]}
                 for b, c in zip(base_blocks[:n], blocks[:n])
                 if b["sha256"] != c["sha256"]]
        out["baseline_rule_count"] = len(base_blocks)
        out["prior_blocks_compared"] = n
        out["prior_blocks_byte_identical"] = (len(diffs) == 0)
        out["prior_block_diffs"] = diffs
        out["appended_blocks"] = len(blocks) - len(base_blocks)
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
