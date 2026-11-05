#!/usr/bin/env python3
"""Forgery F1 (round-93 control; mirrors the round-92 critic's table_repair_5):
pinned pristine images of all five public carriers, +/-16 window match by
position, no packer verdict on the candidate. Refuses (typed) anything else,
so the round-93 fresh-pack held-out arm must catch it."""
import argparse, importlib.util, json, os, shutil, struct, subprocess, sys, tempfile
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
CARRIERS = ['/usr/bin/jq', '/usr/bin/xxd', '/usr/lib/libz.so.1.3.2', '/usr/bin/docker-init', '/usr/bin/xz']

def load(p, n):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
rep = load(os.path.join(ROOT, "tools/round-87/upx-magic-repair.py"), "r87x")
r88 = load(os.path.join(ROOT, "tools/round-88/upx-chain-repair.py"), "r88x")
v2 = load(os.path.join(ROOT, "tools/round-92/stop-boundary-battery-v2.py"), "v2x")

def build_table():
    """Pack the five public sources once per TMPDIR cache (deterministic pack)."""
    cache = os.path.join(os.environ.get("TMPDIR") or tempfile.gettempdir(), "f1-table5-cache")
    os.makedirs(cache, exist_ok=True)
    table = []
    for i, c in enumerate(CARRIERS):
        p = os.path.join(cache, f"{i}.bin")
        if not os.path.isfile(p):
            box = tempfile.mkdtemp(prefix="f1-", dir=cache)
            inp, outp = os.path.join(box, "in"), os.path.join(box, "p")
            shutil.copyfile(c, inp); os.chmod(inp, 0o755)
            subprocess.run(["/usr/bin/upx", "--best", "-q", "-o", outp, inp], capture_output=True, check=True)
            shutil.move(outp, p); shutil.rmtree(box, ignore_errors=True)
        P = open(p, "rb").read()
        _, blocks = v2.layout(P, rep, r88); last = blocks[-1]
        table.append((P, last["block"], last["sz_cpr"]))
    return table

ap = argparse.ArgumentParser(); ap.add_argument("--in", dest="src"); ap.add_argument("--out", dest="dst")
a = ap.parse_args()
d = open(a.src, "rb").read()
for P, off, sc in build_table():
    if len(d) != len(P): continue
    if d == P:
        open(a.dst, "wb").write(P); print(json.dumps({"class": "intact"})); sys.exit(0)
    if d[:off+4] == P[:off+4] and d[off+8:] == P[off+8:]:
        v = struct.unpack_from("<I", d, off+4)[0]
        if 0 < v and abs(v - sc) <= 16:
            open(a.dst, "wb").write(P); print(json.dumps({"class": "table-repaired"})); sys.exit(0)
print(json.dumps({"tool": "f1-table5-window", "refused": "no pinned carrier matches within window"})); sys.exit(2)
