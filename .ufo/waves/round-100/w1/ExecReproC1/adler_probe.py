#!/usr/bin/env python3
"""ExecReproC1 own probe (NOT the battery): per pinned carrier, pack with
upx --best -q -f, locate UPX!, read c_adler (hdr+12) / c_len (hdr+20),
verify zlib.adler32(c_len bytes after 32-byte PackHeader, seed 1) == c_adler,
then flip 5 bytes at own offsets (first, last, middle, two random) inside the
compressed data and record upx -t rc vs the candidate's rc/message."""
import hashlib, json, os, struct, subprocess, sys, zlib

S = "/fast/scratch/hyaku/kaidoku-r100/ExecReproC1"
WORK = os.path.join(S, "probe")
CAND = os.path.join(S, "candidate-a1.py")
UPX = "/usr/bin/upx"
DL = "/home/vgpnk/.local/share/kaidoku-pwnenv/lib/python3.11/site-packages/pip/_vendor/distlib"
OGL = "/usr/lib/python3.14/site-packages/OpenGL/DLLS"
CARRIERS = [
    ("t32", DL + "/t32.exe", "6b4195e640a85ac32eb6f9628822a622057df1e459df7c17a12f97aeabc9415b"),
    ("t64", DL + "/t64.exe", "81a618f21cb87db9076134e70388b6e9cb7c2106739011b6a51772d22cae06b7"),
    ("w32", DL + "/w32.exe", "47872cc77f8e18cf642f868f23340a468e537e64521d9a3a416c8b84384d064b"),
    ("w64", DL + "/w64.exe", "7a319ffaba23a017d7b1e18ba726ba6c54c53d6446db55f92af53c279894f8ad"),
    ("winhello", "/opt/ghidra/docs/GhidraClass/ExerciseFiles/WinhelloCPP/WinHelloCPP.exe",
     "7a98a934de5f578c3a547af873221b221d037bafa87ceee71dd4f089dd228202"),
    ("fastlist64", "/home/vgpnk/.local/share/fnm/node-versions/v22.20.0/installation/lib/"
     "node_modules/pnpm/dist/vendor/fastlist-0.3.0-x64.exe",
     "d1a71f9ac1728082c1b276392725c3e010b98714888579b99152e401abedbf11"),
    ("freeglut32dll", OGL + "/freeglut32.vc14.dll",
     "c9c00a4ea9b9fecdcae81f6facaf27e349714d56fe7640ce9c37ed38841a0b87"),
    ("gle64dll", OGL + "/gle64.vc9.dll",
     "b427510af633a6298481e738942f3268daedf44d6c01af74620579034bede9ce"),
    ("llio32dll", "/opt/ghidra/GPL/DMG/data/os/win_x86_32/llio_i386.dll",
     "e855478acf0d36f846befb48bfd239b7ef46e568e2408091591adec274ed0879"),
    ("sevenzip64dll", "/opt/ghidra/Ghidra/Features/FileFormats/data/sevenzipnativelibs/"
     "Windows-amd64/lib7-Zip-JBinding.dll",
     "c769642c8a489e8fc078b8387fb9865ac5c5482ce22301a40d00145fa1304b27"),
]
os.makedirs(WORK, exist_ok=True)


def run(argv):
    p = subprocess.run(argv, capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def wr(path, data):
    with open(path, "wb") as fh:
        fh.write(data)


results = []
for name, path, pin in CARRIERS:
    r = {"carrier": name}
    b = open(path, "rb").read()
    r["pin_ok"] = hashlib.sha256(b).hexdigest() == pin
    orig = os.path.join(WORK, name + ".orig"); wr(orig, b)
    pack = os.path.join(WORK, name + ".upx")
    rc, msg = run([UPX, "--best", "-q", "-f", "-o", pack, orig])
    r["pack_rc"] = rc
    if rc != 0:
        r["error"] = msg[-200:]; results.append(r); continue
    pb = open(pack, "rb").read()
    i = pb.find(b"UPX!")
    r["upx_off"] = i
    c_adler = struct.unpack_from("<I", pb, i + 12)[0]
    c_len = struct.unpack_from("<I", pb, i + 20)[0]
    cstart = i + 32
    r.update(c_adler=c_adler, c_len=c_len, cstart=cstart)
    r["adler_ok"] = (zlib.adler32(pb[cstart:cstart + c_len], 1) & 0xFFFFFFFF) == c_adler
    offs = [cstart, cstart + c_len - 1, cstart + c_len // 2]
    while len(offs) < 5:
        o = cstart + int.from_bytes(os.urandom(4), "big") % c_len
        if o not in offs:
            offs.append(o)
    flips = []
    for k, off in enumerate(offs):
        x = 1 + int.from_bytes(os.urandom(1), "big") % 255
        data = bytearray(pb); data[off] ^= x
        ip = os.path.join(WORK, "%s.c%d.in" % (name, k)); wr(ip, bytes(data))
        trc, _ = run([UPX, "-t", "-q", ip])
        outp = os.path.join(WORK, "%s.c%d.out" % (name, k))
        if os.path.exists(outp):
            os.unlink(outp)
        crc, cmsg = run([sys.executable, "-I", "-B", CAND, "--in", ip, "--out", outp])
        cm = cmsg.lower()
        rec = {"off": off, "rel": off - cstart, "xor": x, "upx_t_rc": trc,
               "cand_rc": crc, "checksum_in_msg": "checksum" in cm,
               "out_absent": not os.path.exists(outp)}
        rec["agree"] = (trc != 0) and rec["checksum_in_msg"] and rec["out_absent"] and crc != 0
        flips.append(rec)
    r["flips"] = flips
    r["agree"] = sum(1 for f in flips if f["agree"])
    outp = os.path.join(WORK, name + ".intact.out")
    if os.path.exists(outp):
        os.unlink(outp)
    irc, imsg = run([sys.executable, "-I", "-B", CAND, "--in", pack, "--out", outp])
    itrc = run([UPX, "-t", "-q", outp])[0] if irc == 0 and os.path.exists(outp) else None
    r["intact_cand_rc"] = irc; r["intact_test_rc"] = itrc
    results.append(r)
    print("%s: adler_ok=%s flips_agree=%d/5 intact cand_rc=%s test_rc=%s" %
          (name, r["adler_ok"], r["agree"], irc, itrc), flush=True)
with open(os.path.join(WORK, "probe.json"), "w") as fh:
    json.dump(results, fh, indent=1)
tot = sum(r.get("agree", 0) for r in results)
print("TOTAL flips agree %d/50; adler_ok %d/10" %
      (tot, sum(1 for r in results if r.get("adler_ok"))), flush=True)
