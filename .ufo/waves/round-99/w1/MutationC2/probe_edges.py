import json, os, shutil, struct, subprocess, sys
S = "/fast/scratch/hyaku/kaidoku-r99/MutationC2"
WAVE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-99/w1/MutationC2"
BASE = S + "/m/base/tools/round-99/upx-pe-repair.py"
base_pack = open(S + "/work-base/t32.upx", "rb").read()
pe = struct.unpack_from("<I", base_pack, 0x3C)[0]
FALIGN = pe + 24 + 36
NSEC = pe + 6
HDR = 992            # PackHeader offset in t32 pack (window start 960 + 32)
WIN = 960            # gate window start = UPX1 rawdataptr - 64
ASSERT = base_pack[HDR:HDR + 4] == b"UPX!"


def mutate(kind):
    b = bytearray(base_pack)
    if kind == "falign0":
        struct.pack_into("<I", b, FALIGN, 0)
    elif kind == "nsec2":
        struct.pack_into("<H", b, NSEC, 2)
    elif kind == "dup-header-at-window-start":
        b[WIN:WIN + 32] = b[HDR:HDR + 32]
    elif kind == "header-at-window-offset-1023":
        b[HDR:HDR + 32] = b"\0" * 32
        b[WIN + 1023:WIN + 1023 + 32] = base_pack[HDR:HDR + 32]
    return bytes(b)


def run(repair, inp, out):
    if os.path.exists(out):
        os.unlink(out)
    p = subprocess.run(["python3", "-I", "-B", repair, "--in", inp, "--out", out], capture_output=True, text=True)
    last = (p.stderr.strip().splitlines() or [""])[-1]
    return {"rc": p.returncode, "out_written": os.path.exists(out), "tail": last[:160]}


rows = []
for kind, mut in (("falign0", "M05"), ("nsec2", "M13"), ("dup-header-at-window-start", "M09"),
                  ("header-at-window-offset-1023", "M12")):
    inp = f"{S}/probe-{kind}.in"
    open(inp, "wb").write(mutate(kind))
    out = f"{S}/probe-{kind}.out"
    rb = run(BASE, inp, out)
    rm = run(f"{S}/mut/{mut}.py", inp, out)
    rows.append({"probe": kind, "mutant": mut, "base": rb, "mutant_result": rm,
                 "differs": (rb["rc"], rb["out_written"]) != (rm["rc"], rm["out_written"])})
    print(kind, mut, json.dumps(rows[-1]), flush=True)
rows.insert(0, {"fixture_check_pack_header_at_992": ASSERT})
json.dump(rows, open(f"{S}/probe_edges.json", "w"), indent=1)
shutil.copyfile(f"{S}/probe_edges.json", f"{WAVE}/probe_edges.json")
shutil.copyfile(S + "/probe_edges.py", f"{WAVE}/probe_edges.py")
print("DONE")
