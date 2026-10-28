import sys, json
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r48/LabC1Meaning/mod/tools/round-48")
import meanings as M

rows = []
for line in open("/fast/scratch/hyaku/kaidoku-r48/LabC1Meaning/registry-rows.txt"):
    line = line.rstrip("\n")
    if not line.strip().startswith("| `"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    rows.append((cells[0].strip("` "), cells[2]))

out = []
for path, verdict in rows:
    cls = M.meaning_classes(verdict)
    segs = M._segments(verdict)
    out.append({"path": path, "classes": cls,
                "seg0": segs.get("0","")[:90], "seg1": segs.get("1","")[:90], "seg2": segs.get("2","")[:90]})
json.dump(out, open("/fast/scratch/hyaku/kaidoku-r48/LabC1Meaning/classes.json","w"), indent=1)
for o in out:
    c = o["classes"]
    if "error" in c:
        print("ERR ", o["path"], "->", c["error"])
    else:
        print("OK  ", o["path"], "->", c["0"], "|", c["1"], "|", c["2"])
