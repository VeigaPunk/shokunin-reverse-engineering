import importlib.util, json, os, tempfile, sys
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
kill = load("tree/tools/round-96/kill-rule-v2.py", "kk")
# Mutant writer: replace BEFORE fsync (ordering inverted), fsync still called once (on the replaced file)
def write_receipt_inverted(path, receipt):
    d = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(dir=d, prefix=os.path.basename(path) + ".", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=True); fh.write("\n"); fh.flush()
    os.replace(tmp, path)
    with open(path, "rb") as fh:
        os.fsync(fh.fileno())
class M: pass
m = M(); m.write_receipt = write_receipt_inverted
res = kill.c_fsync(m, "/fast/scratch/hyaku/kaidoku-r96/SentinelWrite/fsync-demo")
print("K-fsync verdict on fsync-after-replace writer:", res)
