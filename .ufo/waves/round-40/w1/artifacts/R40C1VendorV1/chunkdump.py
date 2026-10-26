import json, sys
def walk(entries, depth=0):
    for e in entries:
        for r in e.get("reports", []):
            t = r.get("__typename__")
            if t in ("ChunkReport", "UnknownChunkReport"):
                print(f"  depth={depth} {t} {r.get('start_offset')}->{r.get('end_offset')} size={r.get('size')} handler={r.get('handler_name')}")
            if t == "ExtractCommandFailedReport":
                print(f"  depth={depth} ExtractCommandFailed exit_code={r.get('exit_code')}")
        for s in e.get("subtasks", []):
            pass
for path in sys.argv[1:]:
    print(f"== {path}")
    d = json.load(open(path))
    walk(d)
