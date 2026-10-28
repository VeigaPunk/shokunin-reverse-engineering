#!/usr/bin/env python3
"""CritC2Scope probe: measure the C2 counter's declared scope against SCORECARD.md."""
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
import record  # noqa: E402

REV = sys.argv[1] if len(sys.argv) > 1 else "2e4ae434"


def files(path):
    r = subprocess.run(["git", "-C", LANE, "show", f"{REV}:{path}"],
                       capture_output=True, text=True)
    return None if r.returncode != 0 else r.stdout


CARD = files("SCORECARD.md")
lines = CARD.splitlines()
total = len(lines)

heads = [(m.start(), m.group(1), lines.count("\n") if False else CARD[:m.start()].count("\n") + 1)
         for m in re.finditer(r"(?m)^## Round (\d+)", CARD)]
allh = [(CARD[:m.start()].count("\n") + 1, m.group(1))
        for m in re.finditer(r"(?m)^## (.+)$", CARD)]

secs = record.sections(CARD)
in_scope_round = 0
scope_ranges = []
for pos_m in re.finditer(r"(?m)^## Round (\d+)", CARD):
    if pos_m.group(1) in [r for r, _ in secs]:
        pass
# exact scope line ranges: recompute programmatically
for pos, rnd in [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^## Round (\d+)", CARD)][-2:]:
    end = CARD.find("\n## ", pos + 1)
    end = end if end >= 0 else len(CARD)
    a = CARD[:pos].count("\n")
    b = CARD[:end].count("\n")
    scope_ranges.append((rnd, a, b, b - a))
axes_body = CARD.split("## Owned axes", 1)[1].split("\n## ", 1)[0]
axes_lines = axes_body.count("\n")
scope_lines = sum(r[3] for r in scope_ranges) + axes_lines

# atoms: in scope (counter) vs card-wide (all `## Round N` sections)
in_scope_atoms = []
for rnd, text in secs:
    in_scope_atoms.extend(record.collect(text, rnd, files, LANE, REV))
all_atoms = []
per_section = {}
for pos, rnd in [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^## Round (\d+)", CARD)]:
    end = CARD.find("\n## ", pos + 1)
    end = end if end >= 0 else len(CARD)
    a = record.collect(CARD[pos:end], rnd, files, LANE, REV)
    per_section.setdefault(CARD[:pos].count("\n") + 1, []).extend(a)
    all_atoms.extend(a)

all_round_scope_atoms = []
for key in sorted(per_section):
    all_round_scope_atoms.extend(per_section[key])

classes = lambda xs: {c: sum(1 for a in xs if a["class"] == c) for c in record.CLASSES}

# non-round top-level sections
round_lines = {ln for _, a, b, _ in scope_ranges for ln in range(a, b)}
roundish = set()
for pos, rnd in [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^## Round (\d+)", CARD)]:
    end = CARD.find("\n## ", pos + 1)
    end = end if end >= 0 else len(CARD)
    for ln in range(CARD[:pos].count("\n"), CARD[:end].count("\n")):
        roundish.add(ln + 1)
non_round = [(ln, t) for ln, t in allh if ln not in roundish]

print(json.dumps({
    "rev": REV,
    "card_total_lines": total,
    "round_section_headings": len(heads),
    "round_numbers": [h[1] for h in heads],
    "scope_sections": [r for r, _ in secs],
    "scope_ranges": scope_ranges,
    "owned_axes_body_lines": axes_lines,
    "scope_lines_total": scope_lines,
    "scope_line_fraction": round(scope_lines / total, 4),
    "atoms_in_scope": len(in_scope_atoms) + 2,
    "atoms_by_class_in_scope": classes(in_scope_atoms),
    "atoms_all_round_sections": len(all_atoms),
    "atoms_by_class_all_round_sections": classes(all_atoms),
    "atoms_out_of_scope": len(all_atoms) - len(in_scope_atoms),
    "non_round_sections": [{"line": ln, "text": t} for ln, t in non_round],
    "per_section_atom_counts": {ln: len(v) for ln, v in sorted(per_section.items())},
}, indent=1))
