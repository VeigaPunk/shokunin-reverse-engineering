#!/usr/bin/env python3
"""Reversibility cross-checks: citation shift, lesson pointer resolution, surviving deps."""
import json
import re
import subprocess
import sys

CLONE = "/fast/scratch/hyaku/kaidoku-r45/R45W2Rollback/clone"
LAND = "e715263cb51b713c342ab992d527fe9d61d6f8ff"
PRE = "9ff920cd"
A1 = "1f4b27f82353d6544dc0c8048b3cfdadd8525d12"
TIP = "0ee50aaff516571aa607769bbbdf19a3db90dfa5"


def git(*args):
    return subprocess.run(["git", "-C", CLONE, *args], capture_output=True, text=True)


def show(rev, path):
    r = git("show", f"{rev}:{path}")
    return r.stdout if r.returncode == 0 else None


def tracked(rev):
    return git("ls-tree", "-r", "--name-only", rev).stdout.splitlines()


def exists(rev, path):
    return git("cat-file", "-e", f"{rev}:{path}").returncode == 0


out = {}

# 1. SKILL.md line-citation shift caused by the mid-file insertion.
pre_lines = (show(PRE, "SKILL.md") or "").splitlines()
land_lines = (show(LAND, "SKILL.md") or "").splitlines()
pat = re.compile(r"SKILL\.md:(\d+)(?:-(\d+))?")
refs = []
for p in tracked(LAND):
    if not p.endswith(".md") or p.startswith(".ufo/") or p.startswith("corpus/evidence/"):
        continue
    t = show(LAND, p) or ""
    for m in pat.finditer(t):
        refs.append({"file": p, "cited": int(m.group(1)), "raw": m.group(0)})
after = [r for r in refs if r["cited"] > 545]
shift = 43
out["skill_line_refs_total"] = len(refs)
out["skill_line_refs_past_insert_point"] = len(after)
out["citation_shift"] = {
    "same_text_at_landing_line": sum(1 for r in after if pre_lines[r["cited"] - 1] == land_lines[r["cited"] - 1]),
    "changed_by_insertion": sum(1 for r in after if pre_lines[r["cited"] - 1] != land_lines[r["cited"] - 1]),
    "repaired_by_removing_43_lines": sum(1 for r in after
                                         if pre_lines[r["cited"] - 1] != land_lines[r["cited"] - 1]
                                         and pre_lines[r["cited"] - 1] == land_lines[r["cited"] - 1 + shift]),
}
out["shifted_refs"] = [f'{r["file"]} {r["raw"]}' for r in after]

# 2. Lesson / registry pointers per revision.
pointers = [
    ".ufo/waves/round-45/w1/R45W1SrcS138Fix/report.md",
    ".ufo/waves/round-45/w1/R45W1InhSweepEvidence",
    ".ufo/waves/round-45/w1/R45W1CensusDupClass",
]
out["pointer_resolution"] = {}
for rev in (LAND, A1, TIP):
    reg = git("ls-tree", "-r", "--name-only", rev, "--", ".ufo/waves/round-45/w1")
    out["pointer_resolution"][rev[:8]] = {
        "R45W1Reg_entries": len([l for l in reg.stdout.splitlines() if "R45W1Reg" in l]),
        "pointers": {p: exists(rev, p) for p in pointers},
    }
hist = git("log", "--all", "--oneline", "--diff-filter=A", "--",
           ".ufo/waves/round-45/w1/R45W1InhSweepEvidence*")
out["InhSweepEvidence_ever_added"] = hist.stdout.strip() or None

# 3. Surviving SKILL.md text that names the removed surface.
mutants = json.load(open("/fast/scratch/hyaku/kaidoku-r45/R45W2Rollback/mutants.json"))
out["surviving_dependencies"] = {}
for tag, rev in mutants.items():
    text = show(rev, "SKILL.md") or ""
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        if ("block 22" in low or "freeze-integrity-table" in low
                or "round-44/45 instrument registry" in low or "registry-scope" in low):
            hits.append({"line": i, "text": line.strip()[:120]})
    out["surviving_dependencies"][tag] = hits

print(json.dumps(out, indent=1, sort_keys=True))
