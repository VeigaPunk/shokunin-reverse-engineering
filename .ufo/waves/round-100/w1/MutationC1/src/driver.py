#!/usr/bin/env python3
"""MutationC1 driver: one-point mutants of upx-pe-repair.py (candidate) and
pe-upx-corrupt-battery.py (detector), scored with the frozen battery command shape."""
import hashlib, json, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r100/MutationC1"
BASE = f"{S}/pristine"
A1 = "a610671d7a01e1d762eb7103e6ee9f8a2be287ed"
TARGET = ("recovered 30 of 30; decoy 9 of 9; intact 10 of 10; overlay 20 of 20; "
          "truncated 40 of 40; corrupt 40 of 40; refused 2 of 2; cli 3 of 3; static 1 of 1; "
          "exec 1 of 1; effective 119 of 119")
BATTERY_REL = "tools/round-100/pe-upx-corrupt-battery.py"
REPAIR_REL = "tools/round-100/upx-pe-repair.py"

REPAIR_MUTANTS = [
    ("R1-cs-plus-31",   "    cs = i + PH_LEN\n", "    cs = i + 31\n"),
    ("R2-cs-plus-33",   "    cs = i + PH_LEN\n", "    cs = i + 33\n"),
    ("R3-ne-to-eq",     "    if got != c_adler:\n", "    if got == c_adler:\n"),
    ("R4-slice-end-m1", "got = zlib.adler32(bytes(b[cs:cs + c_len]))",
                        "got = zlib.adler32(bytes(b[cs:cs + c_len - 1]))"),
    ("R5-slice-start-p1", "got = zlib.adler32(bytes(b[cs:cs + c_len]))",
                        "got = zlib.adler32(bytes(b[cs + 1:cs + c_len]))"),
    ("R6-struct-be",    'struct.unpack_from("<III", b, i + 12)', 'struct.unpack_from(">III", b, i + 12)'),
    ("R7-token-typo",   '"checksum: adler32 of compressed data %08x != c_adler %08x"',
                        '"cheksum: adler32 of compressed data %08x != c_adler %08x"'),
    ("R8-uadler-read",  'struct.unpack_from("<III", b, i + 12)', 'struct.unpack_from("<III", b, i + 8)'),
    ("R9-adler-seed0",  "got = zlib.adler32(bytes(b[cs:cs + c_len]))",
                        "got = zlib.adler32(bytes(b[cs:cs + c_len]), 0)"),
    ("R10-bound-ge",    "    if cs + c_len > len(b):\n", "    if cs + c_len >= len(b):\n"),
    ("R11-crc32",       "got = zlib.adler32(bytes(b[cs:cs + c_len]))",
                        "got = zlib.crc32(bytes(b[cs:cs + c_len]))"),
    ("R12-trunc-token", '"truncated: compressed data ends at %d > file %d bytes"',
                        '"cut: compressed data ends at %d > file %d bytes"'),
    ("R13-msg-detail",  '"checksum: adler32 of compressed data %08x != c_adler %08x"',
                        '"checksum: %08x != %08x"'),
    ("R14-clamp-len",   '        raise Refuse("truncated: compressed data ends at %d > file %d bytes" % (cs + c_len, len(b)))\n',
                        "        c_len = len(b) - cs\n"),
    ("R15-struct-iih",  'struct.unpack_from("<III", b, i + 12)', 'struct.unpack_from("<IIH", b, i + 12)'),
]

BATTERY_MUTANTS = [
    ("B1-off-minus-1",  "    off = cstart + secrets.randbelow(c_len)\n", "    off = cstart - 1\n"),
    ("B2-xor-zero",     "    x = 1 + secrets.randbelow(255)\n", "    x = 0\n"),
    ("B3-off-past-end", "    off = cstart + secrets.randbelow(c_len)\n", "    off = cstart + c_len\n"),
    ("B4-rc-neq-0",     'ok = rrc == 2 and not os.path.exists(out) and "checksum" in msg',
                        'ok = rrc != 0 and not os.path.exists(out) and "checksum" in msg'),
    ("B5-token-broader", 'ok = rrc == 2 and not os.path.exists(out) and "checksum" in msg',
                        'ok = rrc == 2 and not os.path.exists(out) and "check" in msg'),
    ("B6-drop-outfile", 'ok = rrc == 2 and not os.path.exists(out) and "checksum" in msg',
                        'ok = rrc == 2 and "checksum" in msg'),
    ("B7-one-cell",     'for k in ("a", "b"):', 'for k in ("a",):'),
    ("B8-exec-off-by1", "    extra = execs[1:]\n", "    extra = execs[2:]\n"),
    ("B9-drop-execveat", '"trace=execve,execveat"', '"trace=execve"'),
    ("B10-no-violations", 'violations = [e for e in EXEC_LOG if e["extra"]]', "violations = []"),
    ("B11-window-31",   "    return i + 32, c_len\n", "    return i + 31, c_len\n"),
    ("B12-clen-u_len",  'c_len = struct.unpack_from("<I", packed, i + 20)[0]',
                        'c_len = struct.unpack_from("<I", packed, i + 24)[0]'),
    ("B13-corrupt-ctr", 'n["corrupt"] += ok', 'n["corrupt"] += 1'),
]


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def apply_mut(text, old, new):
    n = text.count(old)
    assert n == 1, f"non-unique anchor ({n} hits): {old[:60]!r}"
    return text.replace(old, new, 1)


def prepare_repair_run(name, old, new):
    run = f"{S}/runs/{name}"
    os.makedirs(run, exist_ok=True)
    clone = f"{run}/clone"
    shutil.copytree(f"{S}/clone", clone, symlinks=True)
    top = subprocess.run(["git", "-C", clone, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    assert top.stdout.strip() == os.path.realpath(clone), f"toplevel mismatch {name}: {top.stdout}"
    p = os.path.join(clone, REPAIR_REL)
    text = open(p, encoding="utf-8").read()
    mut = apply_mut(text, old, new)
    open(p, "w", encoding="utf-8").write(mut)
    subprocess.run(["git", "-C", clone, "add", REPAIR_REL], check=True, capture_output=True)
    r = subprocess.run(["git", "-c", "user.name=MutationC1", "-c", "user.email=mut@scratch.invalid",
                        "-C", clone, "commit", "-q", "-m", f"mutant {name}"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    rev = subprocess.run(["git", "-C", clone, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    return {"kind": "repair", "run": run, "clone": clone, "rev": rev,
            "mut_sha": sha_b(mut.encode()), "battery": f"{BASE}/pe-upx-corrupt-battery.py"}


def prepare_battery_run(name, old, new):
    run = f"{S}/runs/{name}"
    os.makedirs(run, exist_ok=True)
    mut_text = apply_mut(open(f"{BASE}/pe-upx-corrupt-battery.py", encoding="utf-8").read(), old, new)
    bp = f"{run}/battery.py"
    open(bp, "w", encoding="utf-8").write(mut_text)
    return {"kind": "battery", "run": run, "clone": f"{S}/clone", "rev": A1,
            "mut_sha": sha_b(mut_text.encode()), "battery": bp}


def run_one(job):
    name = job["name"]
    run = job["run"]
    os.makedirs(run, exist_ok=True)
    w = f"{run}/work"
    o = f"{run}/receipt.json"
    cmd = [sys.executable, "-I", "-B", job["battery"], "--root", job["clone"],
           "--repair", REPAIR_REL, "--rev", job["rev"], "--work", w, "--json-out", o]
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=job["run"])
    dt = time.time() - t0
    label = p.stdout.strip()
    rec = {}
    if os.path.exists(o):
        rec = json.load(open(o))
    return {"name": name, "kind": job["kind"], "mut_sha": job["mut_sha"], "rev": job["rev"],
            "exit": p.returncode, "label": label, "met": rec.get("met"),
            "counter_sha": rec.get("counter_sha256"), "repair_sha": rec.get("repair_sha256"),
            "secs": round(dt, 1), "receipt": o,
            "stderr_tail": p.stderr.strip()[-200:]}


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else "all"
    bat_bytes = open(f"{BASE}/pe-upx-corrupt-battery.py", "rb").read()
    rep_bytes = open(f"{BASE}/upx-pe-repair.py", "rb").read()
    lane_bat = subprocess.run(["git", "-C", LANE, "show", f"{A1}:{BATTERY_REL}"],
                              capture_output=True).stdout
    assert sha_b(bat_bytes) == sha_b(lane_bat), "pristine battery copy != A1 battery"
    jobs = []
    if only in ("all", "baseline"):
        jobs.append({"name": "BASELINE", "kind": "baseline", "run": f"{S}/runs/BASELINE",
                     "clone": f"{S}/clone", "rev": A1, "mut_sha": sha_b(rep_bytes),
                     "battery": f"{BASE}/pe-upx-corrupt-battery.py"})
    if only in ("all", "repair"):
        for name, old, new in REPAIR_MUTANTS:
            jobs.append(dict(prepare_repair_run(name, old, new), name=name))
    if only in ("all", "battery"):
        for name, old, new in BATTERY_MUTANTS:
            jobs.append(dict(prepare_battery_run(name, old, new), name=name))
    os.makedirs(f"{S}/runs", exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(run_one, jobs))
    summary = {"A1": A1, "target": TARGET, "pristine_battery_sha": sha_b(bat_bytes),
               "pristine_repair_sha": sha_b(rep_bytes), "results": results}
    json.dump(summary, open(f"{S}/summary.json", "w"), indent=1)
    for r in results:
        ok = "MET" if r["met"] else "not-met"
        print(f"{r['name']:22s} {r['kind']:8s} exit={r['exit']} {ok} {r['secs']:6.1f}s "
              f"mut={r['mut_sha'][:12]} :: {r['label'][:110]}")


if __name__ == "__main__":
    main()
