#!/usr/bin/env python3
"""Count round-14 observables from immutable lane Git objects, not a worktree."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
revision = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", sys.argv[1]], text=True).strip()

def get(path):
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f"{revision}:{path}"], text=True)

paths = set(subprocess.check_output(["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", revision], text=True).splitlines())
knowledge = {Path(p).stem for p in paths if p.startswith("corpus/knowledge/") and p.endswith(".md")}
index = get("corpus/README.md").split("## Coverage map\n", 1)[1].split("\n## ", 1)[0]
mapped = set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+", index))
rows = [line.split("|") for line in get("corpus/SOURCES.md").splitlines() if re.match(r"^\|\s*S\d{3,}\s*\|", line)]
result = {
    "revision": revision,
    "C1_source_diagnosis_entries": int("corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md" in paths),
    "C2_quote_gate_instruments": int(".ufo/waves/round-14/tools/quote-fidelity.py" in paths),
    "C2_grounded_quality_criteria": int("quote-fidelity" in get("corpus/QUALITY.md")),
    "knowledge_files": len(knowledge),
    "mapped": len(knowledge & mapped),
    "missing": sorted(knowledge - mapped),
    "dangling": sorted(mapped - knowledge),
    "sources_rows": len(rows),
    "tiers": {t: sum(r[4].strip() == t for r in rows) for t in "ABC"},
    "statuses": {s: sum(r[8].strip() == s for r in rows) for s in ["queued", "mined", "rejected"]},
}
print(json.dumps(result, indent=2, sort_keys=True))
