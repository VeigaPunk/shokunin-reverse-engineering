#!/usr/bin/env python3
"""C1Struct probes: clause-1/2/3 edge behavior + the clause-8 allowlist tension."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
src = open(os.path.join(HERE, "drive.py")).read().split('base = show("SKILL.md")')[0]
exec(compile(src, "drive.py:prefix", "exec"))  # noqa: S102 — scratch-only reuse

base = show("SKILL.md")
GATE_CITE = ", `tools/round-46/gate.py:99` (the flag-order literal)"
REC_CITE = ", `tools/round-47/record.py:242-260` (the corrections re-derivation)"

probes = [
    ("probe-cite-gate46-honest-flag-citation",
     insert_block(base, BLOCK_B.replace(
         "(the predicate these rows are scored by).",
         "(the predicate these rows are scored by)" + GATE_CITE + ".", 1))),
    ("probe-cite-record47-inside-allowlist",
     insert_block(base, BLOCK_B.replace(
         "(the predicate these rows are scored by).",
         "(the predicate these rows are scored by)" + REC_CITE + ".", 1))),
    ("probe-marker-in-craft-preamble",
     insert_block(base, BLOCK_A).replace(
         "## Queue-drain craft rounds", "## Queue-drain craft rounds", 1)),
    ("probe-marker-twice-in-block",
     insert_block(base, BLOCK_B.replace(exact.MARKER, exact.MARKER + " " + exact.MARKER, 1))),
    ("probe-duplicate-24-numbering-decoy",
     insert_block(base, "- **24. Decoy block with the same number.** text\n\n" + BLOCK_B)),
    ("probe-backticked-exit-cells",
     insert_block(base, BLOCK_B.replace("| 1 |\n| R46-CL3", "| `1` |\n| R46-CL3", 1)
                  .replace("| order | 1 |", "| order | `1` |", 1))),
]

# marker in the craft section's preamble (outside any `- **` block)
head, sep, tail = base.partition("## Queue-drain craft ")
body, sep2, rest = tail.partition("\n## ")
probes[2] = ("probe-marker-in-craft-preamble",
             head + sep + "\nPreamble prose carrying " + exact.MARKER + "\n\n"
             + body.rstrip("\n") + "\n\n" + "## " + rest)

# block 24 placed inside the *next* section: marker present, but not a craft block
head, sep, tail = base.partition("## Config custody for live-probe rounds (SOP)")
assert sep
probes.append(("probe-block24-outside-craft-section",
               head + sep + "\n\n" + BLOCK_B.rstrip("\n") + "\n\n" + tail))

# marker quoted inside a fenced example in the next section
fenced = "## Config custody for live-probe rounds (SOP)"
probes.append(("probe-marker-in-fenced-example",
               head + fenced + "\n\n```\n" + exact.MARKER + "\n```\n\n" + tail))

out = {"cases": []}
for name, skill in probes:
    out["cases"].append(run(name, skill))
with open(os.path.join(HERE, "probes.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("WROTE", os.path.join(HERE, "probes.json"))
