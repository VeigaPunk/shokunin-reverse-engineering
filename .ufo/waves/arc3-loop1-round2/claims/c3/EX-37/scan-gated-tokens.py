import importlib.util, os, sys, json
spec = importlib.util.spec_from_file_location("census", "/var/tmp/ex37/instrument-before.py")
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
root = sys.argv[1]
hits, files = [], 0
for dp, dn, fn in os.walk(root):
    for f in sorted(fn):
        p = os.path.join(dp, f); files += 1
        try: lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
        except OSError: continue
        for i, ln in enumerate(lines, 1):
            if C.REA_GATE.search(ln):
                toks = {"pin": [m.group(0) for m in C.PIN.finditer(ln)],
                        "bare": [m.group(0) for m in C.VER.finditer(ln)],
                        "ptr": [m.group(0) for m in C.PTR.finditer(ln)],
                        "cache": [m.group(0) for m in C.CACHE.finditer(ln)]}
                toks = {k: v for k, v in toks.items() if v}
                hits.append({"rel": os.path.relpath(p, root), "line": i, "tokens": toks,
                             "would_be": "UNDECLARED" if C.scope_of(os.path.relpath(p, root), i)[0] is None else C.scope_of(os.path.relpath(p, root), i)[0]})
print(json.dumps({"files_scanned": files, "gated_token_lines": len(hits), "hits": hits}, indent=1))
