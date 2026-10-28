import runpy, sys, tempfile, os, json
real = tempfile.mkdtemp
log = []
def rec(*a, **k):
    log.append({"dir": k.get("dir"), "prefix": k.get("prefix"), "gettempdir": tempfile.gettempdir()})
    return real(*a, **k)
tempfile.mkdtemp = rec
target, out = sys.argv[1], sys.argv[2]
sys.argv = [target, "--selftest"]
try:
    runpy.run_path(target, run_name="__main__")
except SystemExit as e:
    pass
finally:
    open(out, "w").write(json.dumps(log, indent=1))
