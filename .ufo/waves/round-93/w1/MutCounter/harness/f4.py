#!/usr/bin/env python3
# F4 (MutCounter scratch forger): five public pinned images PLUS the fresh-pack image
# for the constant nonce "0"*16 of /usr/bin/env, window-matched like table5-window.py.
import importlib.util, json, os, sys, tempfile
CLONE = "/fast/scratch/hyaku/kaidoku-r93/MutCounter/clone"
def load(p, n):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
mod = load(os.path.join(CLONE, "tools/round-93/stop-boundary-repair-battery-v3.py"), "v3f4")
v2 = mod.v2
rep = load(os.path.join(CLONE, v2.R87), "r87f4"); r88 = load(os.path.join(CLONE, v2.R88), "r88f4")
def build_table():
    work = tempfile.mkdtemp(prefix="f4-", dir=os.environ.get("TMPDIR") or None)
    env = v2.env_for(work)
    table = []
    for cid, src, pin in v2.CARRIERS:
        P = v2.pack(src, work, env)
        _, blocks = v2.layout(P, rep, r88); last = blocks[-1]
        table.append((P, last["block"], last["sz_cpr"]))
    mut, _ = mod.mutate_source(open("/usr/bin/env", "rb").read(), "0" * 16)
    mp = os.path.join(work, "zero-src.bin"); open(mp, "wb").write(mut)
    P0 = v2.pack(mp, work, env)
    _, blocks = v2.layout(P0, rep, r88); last = blocks[-1]
    table.append((P0, last["block"], last["sz_cpr"]))
    return table
import argparse
ap = argparse.ArgumentParser(); ap.add_argument("--in", dest="src"); ap.add_argument("--out", dest="dst")
a = ap.parse_args()
d = open(a.src, "rb").read()
for P, off, sc in build_table():
    if len(d) != len(P): continue
    if d == P:
        open(a.dst, "wb").write(P); print(json.dumps({"class": "intact"})); sys.exit(0)
    if d[:off+4] == P[:off+4] and d[off+8:] == P[off+8:]:
        v = __import__("struct").unpack_from("<I", d, off+4)[0]
        if 0 < v and abs(v - sc) <= 16:
            open(a.dst, "wb").write(P); print(json.dumps({"class": "table-repaired"})); sys.exit(0)
print(json.dumps({"tool": "f4-zero-pin", "refused": "no pinned image matches within window"})); sys.exit(2)
