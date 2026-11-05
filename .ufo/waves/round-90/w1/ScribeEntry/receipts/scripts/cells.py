import hashlib, json, os, struct, subprocess, sys, time, shutil
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r90/ScribeEntry/indep"
RC = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScribeEntry/receipts"
LAY = json.load(open(os.path.join(RC, "indep-layout.json")))["carriers"]
REPAIR = os.path.join(ROOT, "tools/round-90/upx-break-repair.py")
def sha(b): return hashlib.sha256(b).hexdigest()
cells = []
for k in ["jq", "xxd", "dinit", "libz"]:
    L = LAY[k]
    raw_sha = L["sha256_raw"]
    packed = open(os.path.join(S, f"{k}.packed"), "rb").read()
    for idx, blk in enumerate(L["blocks"] if False else []):
        pass
    # recompute full first-segment block list from packed bytes
    import importlib.util
    spec = importlib.util.spec_from_file_location("r88", os.path.join(ROOT, "tools/round-88/upx-chain-repair.py")); r88 = importlib.util.module_from_spec(spec); spec.loader.exec_module(r88)
    spec = importlib.util.spec_from_file_location("r87", os.path.join(ROOT, "tools/round-87/upx-magic-repair.py")); r87 = importlib.util.module_from_spec(spec); spec.loader.exec_module(r87)
    ph_off, ph = r87.find_packheader(packed)
    b0 = L["b0"]; method = packed[b0 + 8]
    q, bl = b0, []
    while q + 12 <= ph_off:
        su, sc = struct.unpack_from("<II", packed, q)
        if su == 0 or sc == 0 or sc > su or q + 12 + sc > ph_off or packed[q + 8] not in (method, ph["method"]): break
        bl.append({"block": q, "sz_unc": su, "sz_cpr": sc}); q += 12 + sc
    for idx, blk in enumerate(bl):
        for d in (-7, 7):
            v = blk["sz_cpr"] + d
            tam = bytearray(packed); struct.pack_into("<I", tam, blk["block"] + 4, v); tam = bytes(tam)
            w = os.path.join(S, "cells", f"{k}-b{idx}-{d:+d}")
            shutil.rmtree(w, ignore_errors=True); os.makedirs(os.path.join(w, "in"))
            inp = os.path.join(w, "in", "packed"); outp = os.path.join(w, "out")
            open(inp, "wb").write(tam)
            t0 = time.time()
            r = subprocess.run([sys.executable, "-I", "-B", REPAIR, "--in", inp, "--out", outp, "--info", outp + ".info.json"], capture_output=True, text=True, cwd="/")
            dt = round(time.time() - t0, 2)
            cell = {"carrier": k, "block_index": idx, "block_off": blk["block"], "stored": blk["sz_cpr"], "tamper": d, "value": v,
                    "in_chain_len": len(bl), "last_block": idx == len(bl) - 1, "repair_rc": r.returncode, "repair_stdout": r.stdout.strip()[:300],
                    "repair_stderr": r.stderr.strip()[-200:], "seconds": dt}
            if r.returncode == 0 and os.path.exists(outp):
                fixed = open(outp, "rb").read()
                diff = [i for i, (a, b) in enumerate(zip(tam, fixed)) if a != b]
                cell["len_equal"] = len(fixed) == len(tam)
                cell["diff_bytes"] = len(diff)
                cell["diff_in_window"] = all(blk["block"] + 4 <= i < blk["block"] + 8 for i in diff)
                cell["unchanged"] = fixed == tam
                cell["fixed_sz_cpr"] = struct.unpack_from("<I", fixed, blk["block"] + 4)[0]
                t = subprocess.run(["/usr/bin/upx", "-t", "-q", outp], capture_output=True, text=True)
                cell["upx_t_rc"] = t.returncode; cell["upx_t_tail"] = (t.stdout + t.stderr).strip().splitlines()[-1:] 
                dd = os.path.join(w, "dec")
                x = subprocess.run(["/usr/bin/upx", "-d", "-q", "-o", dd, outp], capture_output=True, text=True)
                cell["upx_d_rc"] = x.returncode
                if x.returncode == 0:
                    cell["unpacked_sha256"] = sha(open(dd, "rb").read())
                    cell["unpacked_eq_pin"] = cell["unpacked_sha256"] == raw_sha
            cell["isolation_listing"] = sorted(os.listdir(os.path.join(w, "in")))
            cells.append(cell)
            print(k, idx, d, cell["repair_rc"], cell.get("diff_bytes"), cell.get("diff_in_window"), cell.get("upx_t_rc"), cell.get("unpacked_eq_pin"), dt, flush=True)
json.dump(cells, open(os.path.join(RC, "indep-cells.json"), "w"), indent=1)
