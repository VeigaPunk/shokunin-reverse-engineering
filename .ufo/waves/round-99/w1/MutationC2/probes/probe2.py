import json, os, shutil, stat, struct, subprocess
S = "/fast/scratch/hyaku/kaidoku-r99/MutationC2"
WAVE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-99/w1/MutationC2"
BASE = S + "/m/base/tools/round-99/upx-pe-repair.py"
UPX = "/usr/bin/upx"
PK = open(S + "/work-base/t32.upx", "rb").read()
GLE_BOTH = open(S + "/work-base/gle64dll.both.in", "rb").read()
PEG = struct.unpack_from("<I", GLE_BOTH, 0x3C)[0]
GST = PEG + 24 + struct.unpack_from("<H", GLE_BOTH, PEG + 20)[0]
PE = struct.unpack_from("<I", PK, 0x3C)[0]
ST = PE + 24 + struct.unpack_from("<H", PK, PE + 20)[0]
HDR = 992
WIN = 960
D = S + "/probe2"
shutil.rmtree(D, ignore_errors=True)
os.makedirs(D)


def fix_ck(b, off):
    b[off + 31] = sum(b[off + 4:off + 31]) % 251


def run(repair, inp, out):
    if os.path.isfile(out):
        os.unlink(out)
    p = subprocess.run(["python3", "-I", "-B", repair, "--in", inp, "--out", out], capture_output=True, text=True)
    last = (p.stderr.strip().splitlines() or [""])[-1]
    ut = None
    if p.returncode == 0 and os.path.exists(out):
        ut = subprocess.run([UPX, "-t", "-q", out], capture_output=True).returncode
    return {"rc": p.returncode, "out": os.path.exists(out), "tail": last[:120], "upx_t_rc": ut,
            "traceback": "Traceback" in p.stderr}


def cmp(name, mut, data, extra=None):
    inp = f"{D}/{name}.in"
    open(inp, "wb").write(data)
    out = f"{D}/{name}.out"
    rb = run(BASE, inp, out)
    rm = run(f"{S}/mut/{mut}.py", inp, out)
    row = {"probe": name, "mutant": mut, "base": rb, "mutant_result": rm,
           "differs": (rb["rc"], rb["out"], rb["traceback"]) != (rm["rc"], rm["out"], rm["traceback"])}
    if extra:
        row.update(extra)
    print(json.dumps(row), flush=True)
    return row


rows = []
# M10: valid header at 992 plus checksum-invalid look-alike with nonzero lengths at 960
b = bytearray(PK); look = bytearray(PK[HDR:HDR + 32]); look[31] ^= 1; b[WIN:WIN + 32] = look
rows.append(cmp("M10-checksum-invalid-lookalike", "M10", bytes(b)))
# M11: the only header sits at window start 960 (rptr-64), not 961
b = bytearray(PK); b[WIN:WIN + 32] = PK[HDR:HDR + 32]; b[HDR:HDR + 32] = b"\0" * 32
rows.append(cmp("M11-header-at-window-start-only", "M11", bytes(b)))
# M13: NumberOfSections = 2
b = bytearray(PK); struct.pack_into("<H", b, PE + 6, 2)
rows.append(cmp("M13-two-sections", "M13", bytes(b)))
# M19: c_len beyond file size, valid checksum
b = bytearray(PK); struct.pack_into("<I", b, HDR + 16, len(PK) + 5000); struct.pack_into("<I", b, HDR + 20, len(PK) + 1000); fix_ck(b, HDR)
rows.append(cmp("M19-clen-beyond-file", "M19", bytes(b)))
# M21: version 15, valid checksum
b = bytearray(PK); b[HDR + 4] = 15; fix_ck(b, HDR)
rows.append(cmp("M21-version-15", "M21", bytes(b)))
# M23: c_len == u_len, valid checksum
b = bytearray(PK); cl = struct.unpack_from("<I", b, HDR + 20)[0]; struct.pack_into("<I", b, HDR + 16, cl); fix_ck(b, HDR)
rows.append(cmp("M23-clen-equals-ulen", "M23", bytes(b)))
# M05: FileAlignment zero
b = bytearray(PK); struct.pack_into("<I", b, PE + 24 + 36, 0)
rows.append(cmp("M05-filealign-zero", "M05", bytes(b)))
# M13 already above; M09: duplicate valid header
b = bytearray(PK); b[WIN:WIN + 32] = PK[HDR:HDR + 32]
rows.append(cmp("M09-duplicate-valid-header", "M09", bytes(b)))
# M12: only header at window offset 1023
b = bytearray(PK); b[HDR:HDR + 32] = b"\0" * 32; b[WIN + 1023:WIN + 1023 + 32] = PK[HDR:HDR + 32]
rows.append(cmp("M12-header-at-window-offset-1023", "M12", bytes(b)))
# M01: last section raw end not FileAlignment-aligned; file cut at raw end (unaligned)
secs = [(struct.unpack_from("<I", PK, ST + 40 * k + 16)[0], struct.unpack_from("<I", PK, ST + 40 * k + 20)[0]) for k in range(3)]
rs, rp = secs[-1]
new_rs = rs - 100
b = bytearray(PK); struct.pack_into("<I", b, ST + 40 * 2 + 16, new_rs)
cut = bytes(b[:rp + new_rs])
rows.append(cmp("M01-unaligned-last-raw-end", "M01", cut))
# M07: --out is an existing directory
dd = D + "/dirout"; os.makedirs(dd)
inp = D + "/M07.in"; open(inp, "wb").write(PK)
rb = run(BASE, inp, dd)
dlist_b = sorted(os.listdir(D))
rm = run(S + "/mut/M07.py", inp, dd)
rows.append({"probe": "M07-out-is-directory", "mutant": "M07", "base": rb, "mutant_result": rm,
             "dir_entries_after_mutant": sorted(os.listdir(dd)), "siblings_after_base": dlist_b,
             "siblings_after_mutant": sorted(os.listdir(D)),
             "differs": (rb["rc"], rb["tail"]) != (rm["rc"], rm["tail"])})
print(json.dumps(rows[-1]), flush=True)
# M08: pre-existing <out>.tmp sentinel
ds = D + "/M08"; os.makedirs(ds)
out = ds + "/out.bin"; sent = out + ".tmp"
open(sent, "wb").write(b"SENTINEL")
rb = run(BASE, inp, out); base_sent = open(sent, "rb").read().decode() if os.path.exists(sent) else None
open(sent, "wb").write(b"SENTINEL")
rm = run(S + "/mut/M08.py", inp, out); mut_sent = open(sent, "rb").read().decode() if os.path.exists(sent) else None
rows.append({"probe": "M08-preexisting-tmp-sentinel", "mutant": "M08", "base": rb, "mutant_result": rm,
             "sentinel_after_base": base_sent, "sentinel_after_mutant": mut_sent,
             "differs": base_sent != mut_sent})
print(json.dumps(rows[-1]), flush=True)
# M14: output mode
out = D + "/M14.out"
rb = run(BASE, inp, out); base_mode = oct(stat.S_IMODE(os.stat(out).st_mode)) if rb["out"] else None
rm = run(S + "/mut/M14.py", inp, out); mut_mode = oct(stat.S_IMODE(os.stat(out).st_mode)) if rm["out"] else None
rows.append({"probe": "M14-output-mode", "mutant": "M14", "base_mode": base_mode, "mutant_mode": mut_mode,
             "base": rb, "mutant_result": rm, "differs": base_mode != mut_mode})
print(json.dumps(rows[-1]), flush=True)
# M25: section-2 name left unrepaired; compare outputs on gle64 both-tamper input
out_b = D + "/M25.base.out"; out_m = D + "/M25.mut.out"
inp = D + "/gle64.both.in"; open(inp, "wb").write(GLE_BOTH)
rb = run(BASE, inp, out_b); shutil_b = open(out_b, "rb").read() if rb["out"] else b""
rm = run(S + "/mut/M25.py", inp, out_m); shutil_m = open(out_m, "rb").read() if rm["out"] else b""
rows.append({"probe": "M25-section2-name-unrepaired-gle64", "mutant": "M25", "base": rb, "mutant_result": rm,
             "bytes_differ": shutil_b != shutil_m, "names_base": shutil_b[ST:ST + 40 * 3:40][:0] or [shutil_b[GST + 40 * k:GST + 40 * k + 8].rstrip(b"\0").decode("latin1") for k in range(3)] if shutil_b else None,
             "names_mutant": [shutil_m[GST + 40 * k:GST + 40 * k + 8].rstrip(b"\0").decode("latin1") for k in range(3)] if shutil_m else None,
             "differs": shutil_b != shutil_m})
print(json.dumps(rows[-1]), flush=True)
json.dump(rows, open(S + "/probe2.json", "w"), indent=1)
os.makedirs(WAVE + "/probes", exist_ok=True)
shutil.copyfile(S + "/probe2.json", WAVE + "/probes/probe2.json")
shutil.copyfile(S + "/probe2.py", WAVE + "/probes/probe2.py")
shutil.copyfile(S + "/probe_edges.py", WAVE + "/probes/probe_edges.py")
shutil.copyfile(S + "/probe_edges.json", WAVE + "/probes/probe_edges.json")
shutil.copyfile(S + "/probe_pop.py", WAVE + "/probes/probe_pop.py")
print("DONE")
