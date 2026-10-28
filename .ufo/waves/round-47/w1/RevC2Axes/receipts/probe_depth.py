import json, os, re, subprocess, sys
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join("/fast/scratch/hyaku/kaidoku-r47/RevC2Axes", "tools/round-47"))
import record as R  # frozen bytes, 5017e1f

rev = sys.argv[1]
files = lambda p: R.gate.show(LANE, rev, p)
skill = files("SKILL.md")
craft = skill.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
rules = re.split(r"(?m)^- \*\*", craft)[1:]
KA = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
rows = []
for i, rule in enumerate(rules, 1):
    hard = R.HARD_REF.findall(rule)
    kn = re.findall(KA, rule)
    rows.append({"block": i, "record_refs": [h[0] + (":" + h[1] + ("-" + h[2] if h[2] else "") if h[1] else "") for h in hard],
                 "command_a_refs": [k[0] for k in kn]})
out = {"rev": rev,
       "record_py_depth_pair": R.depth_pair(files),
       "blocks": rows,
       "blocks_with_no_knowledge_ref": [r["block"] for r in rows if not r["command_a_refs"]]}
print(json.dumps(out, indent=1))
