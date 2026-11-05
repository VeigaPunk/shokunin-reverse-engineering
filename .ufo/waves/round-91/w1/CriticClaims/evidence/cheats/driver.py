import importlib.util, hashlib, os, struct, sys
root = "/fast/scratch/hyaku/kaidoku-r91/CriticClaims/clone"
def load(p, n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(root, p))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
bat = load("tools/round-91/stop-boundary-battery.py", "bat")
rep = load("tools/round-87/upx-magic-repair.py", "r87")
r88 = load("tools/round-88/upx-chain-repair.py", "r88")
work = "/fast/scratch/hyaku/kaidoku-r91/CriticClaims/work/cheatlab/work"
os.makedirs(work, exist_ok=True)
env = bat.env_for(work)
print("upx sha256 ok:", bat.sha256_file(bat.UPX) == bat.UPX_SHA256)
print("jq pin ok:", bat.sha256_file("/usr/bin/jq") == bat.CARRIERS[0][2])
packed = bat.pack("/usr/bin/jq", work, env)
b0, blocks = bat.layout(packed, rep, r88)
last = blocks[-1]
t = bytearray(packed); struct.pack_into("<I", t, last["block"]+4, last["sz_cpr"]+7)
tampered = bytes(t)
for name in ("noop-rc2.py", "noop-rc0.py", "copy-rc0.py"):
    stub = os.path.join("/fast/scratch/hyaku/kaidoku-r91/CriticClaims/work/cheatlab", name)
    row = bat.score_cell(stub, tampered, last, env, work, packed, bat.packer_test)
    rec = bat.invoke(stub, packed, env, work)
    same = rec.get("rc") == 0 and rec.get("output") == packed
    print(f"{name}: tampered_class={row.get('class')} intact_rc={rec.get('rc')} intact_identity={same}")
