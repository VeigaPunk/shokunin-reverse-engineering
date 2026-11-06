import re, sys, json
text = open(sys.argv[1], encoding="utf-8").read()
assert text.count("<!-- instrument-registry v2 -->") == 1 and text.count("<!-- /instrument-registry -->") == 1
body = text.split("<!-- instrument-registry v2 -->", 1)[1].split("<!-- /instrument-registry -->", 1)[0]
rows = []
for ln, line in enumerate(body.splitlines(), 1):
    if not line.startswith("| `"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    rows.append({"line": ln, "path": cells[0].strip("`"), "n_cells": len(cells),
                 "selftest_cell": cells[3] if len(cells) >= 4 else "", "all": cells})
COUNT = re.compile(r"\d+\s*(?:selftest\s+)?cases\b|cases\s*[=:]\s*\d+|\d+/\d+\s*cases|pass\s+\d+|\d+/\d+")
SELF = re.compile(r"--selftest|selftest|self-test", re.I)
out = []
for r in rows:
    c = r["selftest_cell"]
    out.append({"path": r["path"], "line": r["line"], "n_cells": r["n_cells"],
                "mentions_selftest": bool(SELF.search(c)), "states_count": bool(COUNT.search(c)),
                "selftest_cell": c})
json.dump(out, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
print("rows", len(out))
print("rows with selftest mention and no count:", sum(1 for o in out if o["mentions_selftest"] and not o["states_count"]))
print("rows with count:", sum(1 for o in out if o["states_count"]))
print("rows with fewer than 4 cells:", sum(1 for o in out if o["n_cells"] < 4))
print("duplicate paths:", len(out) - len({o["path"] for o in out}))
