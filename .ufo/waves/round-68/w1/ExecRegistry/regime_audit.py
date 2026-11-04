#!/usr/bin/env python3
"""Regime/coverage audit around the R68-C1 census.

Reads git objects only.  Answers, for a revision:
  * every tools/round-N/**.{py,sh,mjs} blob and which inventory names it
    (own plan / foreign plan / registry row / none);
  * registry row shapes that the census grammar cannot see (non-round paths,
    paths not named by any plan, legacy rounds, foreign-only instruments);
  * every plan-named own-round path and its disposition;
  * every foreign-round citation and whether the cited blob exists.
Prints JSON.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

MARK_OPEN = "<!-- instrument-registry v2 -->"
MARK_CLOSE = "<!-- /instrument-registry -->"
PLAN_RE = re.compile(r"^plans/round-(\d+)-claims\.md$")
TOOL_RE = re.compile(r"tools/round-(\d+)/[A-Za-z0-9._/-]*?\.(?:py|sh|mjs)\b")
ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|")
BLOB_ROUND = re.compile(r"^tools/round-(\d+)/[A-Za-z0-9._/-]*?\.(?:py|sh|mjs)$")


def sh(root, *argv):
    p = subprocess.run(["git", "-C", root, *argv], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"git {' '.join(argv)} rc={p.returncode}: {p.stderr.strip()}")
    return p.stdout


def rows_of(skill):
    body = skill.split(MARK_OPEN, 1)[1].split(MARK_CLOSE, 1)[0]
    rows = []
    for line in body.splitlines():
        s = line.strip()
        m = ROW_RE.match(s)
        if m:
            cells = [c.strip() for c in s.strip("|").split("|")]
            rows.append({"path": m.group(1), "verdict": cells[2] if len(cells) > 2 else ""})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    plans = {}
    for p in sh(a.root, "ls-tree", "-r", "--name-only", a.rev, "--", "plans").splitlines():
        if PLAN_RE.match(p):
            plans[p] = sh(a.root, "show", f"{a.rev}:{p}")
    skill = sh(a.root, "show", f"{a.rev}:SKILL.md")
    blobs = [b for b in sh(a.root, "ls-tree", "-r", "--name-only", a.rev, "--", "tools").splitlines()
             if BLOB_ROUND.match(b)]
    rows = rows_of(skill)
    row_paths = {r["path"] for r in rows}

    own = {}       # round -> set(path) named by its own plan
    foreign = {}   # cited path -> set(source plan)
    for plan, text in plans.items():
        rnd = int(PLAN_RE.match(plan).group(1))
        for m in TOOL_RE.finditer(text):
            path = m.group(0)
            if int(m.group(1)) == rnd and path.startswith(f"tools/round-{rnd}/"):
                own.setdefault(rnd, set()).add(path)
            else:
                foreign.setdefault(path, set()).add(plan)

    named_by_own = set().union(*own.values()) if own else set()
    blob_set = set(blobs)
    out = {
        "rev": a.rev,
        "blob_count": len(blobs),
        "row_count": len(rows),
        "rows_non_round_path": sorted(p for p in row_paths if not BLOB_ROUND.match(p)),
        "rows_not_named_by_any_own_plan": sorted(p for p in row_paths if p not in named_by_own),
        "rows_legacy_round": sorted(p for p in row_paths
                                    if (m := BLOB_ROUND.match(p)) and int(m.group(1)) < 41),
        "blobs_unnamed_and_unregistered": sorted(b for b in blobs
                                                 if b not in named_by_own and b not in row_paths),
        "blobs_foreign_only": sorted(b for b in blobs
                                     if b not in named_by_own and b in foreign),
        "foreign_cited_paths": {p: sorted(s) for p, s in sorted(foreign.items())},
        "foreign_cited_absent_at_rev": sorted(p for p in foreign if p not in blob_set),
        "foreign_cited_absent_and_rowless": sorted(p for p in foreign
                                                   if p not in blob_set and p not in row_paths),
        "own_named_absent": sorted(p for p in named_by_own if p not in blob_set),
        "own_named_absent_with_row": sorted(p for p in named_by_own
                                            if p not in blob_set and p in row_paths),
        "own_named_legacy_absent": sorted(p for r, ps in own.items() if r < 41
                                          for p in ps if p not in blob_set),
        "per_round": {
            str(r): {
                "named": len(ps),
                "named_existing": len([p for p in ps if p in blob_set]),
                "registered": len([p for p in ps if p in row_paths]),
                "blobs": len([b for b in blobs if BLOB_ROUND.match(b).group(1) == str(r)]),
            } for r, ps in sorted(own.items())
        },
        "blobs_per_round_total": {},
    }
    for b in blobs:
        r = BLOB_ROUND.match(b).group(1)
        out["blobs_per_round_total"][r] = out["blobs_per_round_total"].get(r, 0) + 1
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
