import hashlib, json, os, struct, subprocess, sys, time, shutil, tempfile
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r90/ScribeEntry/indep"
RC = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScribeEntry/receipts"
sys.path.insert(0, os.path.join(ROOT, "tools/round-88"))
import importlib.util
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
r87 = load(os.path.join(ROOT, "tools/round-87/upx-magic-repair.py"), "r87")
r88 = load(os.path.join(ROOT, "tools/round-88/upx-chain-repair.py"), "r88")
brk = load(os.path.join(ROOT, "tools/round-90/upx-break-repair.py"), "brk")
CARR = {"jq": "/usr/bin/jq", "xxd": "/usr/bin/xxd", "libz": "/usr/lib/libz.so.1.3.2", "dinit": "/usr/bin/docker-init"}
PINS = {"jq": "e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806", "xxd": "7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65", "libz": "6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9", "dinit": "0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115"}
def sha(b): return hashlib.sha256(b).hexdigest()
out = {"carriers": {}}
for k, p in CARR.items():
    p = os.path.realpath(p)
    raw = open(p, "rb").read()
    rec = {"path": p, "sha256_raw": sha(raw), "pin_ok": sha(raw) == PINS[k]}
    packed = os.path.join(S, f"{k}.packed")
    t0 = time.time()
    r = subprocess.run(["/usr/bin/upx", "--best", "-q", "-o", packed, p], capture_output=True, text=True)
    rec["pack_rc"] = r.returncode; rec["pack_s"] = round(time.time() - t0, 2)
    data = open(packed, "rb").read()
    rec["packed_sha256"] = sha(data); rec["packed_bytes"] = len(data)
    ph_off, ph = r87.find_packheader(data)
    rec["ph_off"] = ph_off; rec["u_len"] = ph["u_len"] if ph else None
    blocks = []
    best = (None, [])
    for m in r88.l_info_candidates(data, ph_off, ph):
        b0 = m + 20
        su0, _ = struct.unpack_from("<II", data, b0)
        if su0 == 0: continue
        method = data[b0 + 8]
        q, bl = b0, []
        while q + 12 <= ph_off:
            su, sc = struct.unpack_from("<II", data, q)
            if su == 0 or sc == 0 or sc > su or q + 12 + sc > ph_off or data[q + 8] not in (method, ph["method"]): break
            bl.append({"block": q, "sz_unc": su, "sz_cpr": sc}); q += 12 + sc
        if len(bl) > len(best[1]): best = (b0, bl)
    b0, bl = best
    method = data[b0 + 8]
    rec["b0"] = b0; rec["first_segment_blocks"] = len(bl)
    rec["stored_chain_sz_unc_sum"] = sum(b["sz_unc"] for b in bl)
    rec["blocks"] = bl[:8]
    found = brk.longest_prefix(data, r87, r88)
    _m, _b0, _ph, _bl, _meth = found
    st, si = brk.chain_ok(data, r87, b0, ph_off, ph)
    rec["stored_chain_ok"] = st
    rec["stored_accounted_total"] = brk.accounted(data, r88, b0, ph_off, method, ph, si) if st else None
    rec["stored_resume"] = si.get("resume") if st else None
    rec["sentinel"] = si.get("sentinel") if st else None
    out["carriers"][k] = rec
    print(k, rec["pack_rc"], rec["packed_bytes"], rec["u_len"], len(bl), rec["stored_chain_sz_unc_sum"], flush=True)
json.dump(out, open(os.path.join(RC, "indep-layout.json"), "w"), indent=1, default=str)
