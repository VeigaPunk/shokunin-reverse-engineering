"""Independent static sweep of the A2 registry (no counter code): row path exists, self-test flags
appear in the tool source, and for argparse tools, every flag the cell names is registered via add_argument."""
import json, os, re, sys
CLONE = sys.argv[1]
rows = json.load(open(sys.argv[2]))
FLAG = re.compile(r"(?<![\w-])(--[a-z][a-z0-9-]*)")
ADD = re.compile(r"add_argument\(\s*((?:['\"]-[^'\"]+['\"]\s*,?\s*)+)")
out = []
for r in rows:
    path = r["path"]
    cell = r["selftest_cell"]
    full = os.path.join(CLONE, path)
    rec = {"line": r["line"], "path": path, "exists": os.path.isfile(full), "flags_in_cell": [], "missing_in_source": [],
           "not_registered_argparse": [], "argparse": False}
    if not rec["exists"]:
        out.append(rec); continue
    src = open(full, encoding="utf-8", errors="replace").read()
    reg = set()
    for m in ADD.finditer(src):
        reg.update(re.findall(r"['\"](-[^'\"]+)['\"]", m.group(1)))
    rec["argparse"] = "add_argument(" in src
    # only the flags written against this tool's own invocation, i.e. the cell text
    flags = sorted(set(FLAG.findall(cell)))
    rec["flags_in_cell"] = flags
    for f in flags:
        if f not in src:
            rec["missing_in_source"].append(f)
        elif rec["argparse"] and f not in reg:
            rec["not_registered_argparse"].append(f)
    out.append(rec)
json.dump(out, open(sys.argv[3], "w"), indent=1)
print("rows", len(out), "missing files", sum(not o["exists"] for o in out))
print("rows with a cell flag absent from source", sum(bool(o["missing_in_source"]) for o in out))
print("rows with a cell flag not registered by argparse", sum(bool(o["not_registered_argparse"]) for o in out))
for o in out:
    if (not o["exists"]) or o["missing_in_source"] or o["not_registered_argparse"]:
        print(o["line"], o["path"], "exists=%s" % o["exists"], "absent=%s" % o["missing_in_source"], "unregistered=%s" % o["not_registered_argparse"])
