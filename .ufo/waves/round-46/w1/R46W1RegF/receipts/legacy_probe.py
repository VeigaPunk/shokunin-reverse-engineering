import json, sys
S, L = sys.argv[1], sys.argv[2]
sys.path.insert(0, L + "/tools/round-46")
import registry
line = [l for l in open(L + "/SKILL.md", encoding="utf-8") if l.startswith("| `tools/round-45/c1-counter.py`")][0].rstrip("\n")
HEAD = ("| tool | gate or probe - purpose | verdict map (exit codes) | "
        "self-test command | pinned-value path | write scope | owner |")
SEP = "|---|---|---|---|---|---|---|"
skill = ("# x\n\n<!-- instrument-registry v2 -->\n" + HEAD + "\n" + SEP + "\n"
         + line + "\n<!-- /instrument-registry -->\n")
cen = {"paths": ["tools/round-45/c1-counter.py"]}
files = lambda p: json.dumps(cen).encode() if p == "tools/round-46/census.json" else b"x"
code, rec = registry.score(skill, files, "r46", "v2", "probe")
cells = [c.strip() for c in line.strip().strip("|").split("|")]
print(json.dumps({"case": "existing-round-45-row-verbatim", "exit": code,
                  "cells_in_row": len(cells), "cell2_is": cells[2][:40],
                  "exit_keys_in_cell2": sorted(set(registry.EXITMAP.findall(cells[2]))),
                  "exit_keys_in_cell3": sorted(set(registry.EXITMAP.findall(cells[3]))),
                  "header_ok": rec["header"] == registry.HOUSE,
                  "thin": rec["thin"], "unregistered": rec["unregistered"],
                  "failing": rec["failing"]}, sort_keys=True))
