import importlib.util, sys, re, os
spec = importlib.util.spec_from_file_location("gate", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/local-source-gate.py")
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
root = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
text, prov = g.read_sources(root, sys.argv[1] if len(sys.argv) > 1 else None, None)
print("provenance:", prov)
rows = g.parse_rows(text)
print("rows_total:", len(rows))
for row in rows:
    url_cell = row["cells"][1]
    paths = [p for p in g.external_paths(url_cell) if not g.inside(os.path.normpath(p), root)]
    if not paths:
        continue
    pins = g.digests_in(g.URL.sub(" ", url_cell))
    print("ROW", row["id"], "pins:", [p[:12] for p in pins])
    for p in paths:
        print("   path:", p)
