#!/usr/bin/env python3
"""SentinelInputs adversarial probe of tools/round-99/upx-pe-repair.py at Bk.

Requirements under test (seat spec):
  * exit status only 0 or 2
  * no traceback on stderr
  * on rc 0: no file left besides --out
  * on rc 2: --out must not exist
  * victim behind a symlink --out stays untouched
  * bounded time per input (wall kill at TMO seconds; RLIMIT_AS 1 GiB on capped cases)
"""
import hashlib
import json
import os
import random
import resource
import shutil
import struct
import subprocess
import sys
import time

TOOL = "/fast/scratch/hyaku/kaidoku-r99/SentinelInputs/clone/tools/round-99/upx-pe-repair.py"
PACKS = {
    "t32": "/fast/scratch/hyaku/kaidoku-r99/SentinelInputs/packs/t32.upx",
    "w64": "/fast/scratch/hyaku/kaidoku-r99/SentinelInputs/packs/w64.upx",
    "freeglut32dll": "/fast/scratch/hyaku/kaidoku-r99/SentinelInputs/packs/freeglut32dll.upx",
}
ROOT = "/fast/scratch/hyaku/kaidoku-r99/SentinelInputs/cases"
TMO = 20.0
TMO_CPU = 15
PY = sys.executable
RESULTS = []


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def layout(b):
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    n = struct.unpack_from("<H", b, pe + 6)[0]
    opt = struct.unpack_from("<H", b, pe + 20)[0]
    falign = struct.unpack_from("<I", b, pe + 24 + 36)[0]
    st = pe + 24 + opt
    return pe, n, opt, falign, st


def snap(d):
    out = {}
    for dirpath, dirnames, filenames in os.walk(d):
        for name in dirnames + filenames:
            p = os.path.join(dirpath, name)
            rel = os.path.relpath(p, d)
            out[rel] = "dir" if os.path.isdir(p) and not os.path.islink(p) else "f"
    return out


def _limits():
    resource.setrlimit(resource.RLIMIT_AS, (1 << 30, 1 << 30))
    resource.setrlimit(resource.RLIMIT_CPU, (TMO_CPU, TMO_CPU))


def run_case(cid, workdir, inp, out, capped=False, extra=None):
    before = snap(workdir)
    cmd = [PY, "-I", "-B", TOOL, "--in", inp, "--out", out, "--json"]
    t0 = time.monotonic()
    timed_out = False
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=TMO, cwd=workdir,
                           preexec_fn=_limits if capped else None)
        rc, so, se = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        timed_out = True
        rc, so, se = None, "", ""
    dt = time.monotonic() - t0
    after = snap(workdir)
    out_abs = out if os.path.isabs(out) else os.path.join(workdir, out)
    out_rel = os.path.relpath(out_abs, workdir)
    v = []
    if timed_out:
        v.append("timeout>%.0fs" % TMO)
    elif rc not in (0, 2):
        v.append("rc=%d" % rc)
    if "Traceback (most recent call last)" in se:
        v.append("traceback")
    if rc == 0:
        strays = [k for k in after if k not in before and k != out_rel]
        if strays:
            v.append("stray-files:%s" % ",".join(strays[:5]))
    if rc == 2 and os.path.lexists(out_abs) and not os.path.isdir(out_abs):
        v.append("out-written-on-rc2")
    r = {"id": cid, "rc": rc, "secs": round(dt, 3), "violation": v,
         "stderr_tail": se[-240:], "stdout_tail": so[-160:], "cmd": cmd}
    if extra:
        r.update(extra)
    RESULTS.append(r)
    return r


def main():
    shutil.rmtree(ROOT, ignore_errors=True)
    os.makedirs(ROOT)
    rng = random.Random(0x5EED99)
    packs = {}
    for name, path in PACKS.items():
        with open(path, "rb") as fh:
            packs[name] = fh.read()
    seq = [0]

    def case_dir(tag):
        seq[0] += 1
        d = os.path.join(ROOT, "%04d_%s" % (seq[0], tag))
        os.makedirs(d)
        return d

    def add_in(d, data, name="in.bin"):
        with open(os.path.join(d, name), "wb") as fh:
            fh.write(data)
        return os.path.join(d, name)

    def std(d):
        return os.path.join(d, "in.bin"), os.path.join(d, "out.bin")

    # A: random byte flips across DOS header, PE header, section table  (450)
    for pname, data in packs.items():
        pe, n, opt, falign, st = layout(data)
        hi = min(st + 40 * n, len(data))
        for k in range(150):
            d = case_dir("hdrflip-%s" % pname)
            b = bytearray(data)
            for _ in range(rng.randint(1, 8)):
                b[rng.randrange(0, hi)] = rng.randrange(256)
            add_in(d, bytes(b))
            run_case("hdrflip-%s-%d" % (pname, k), d, *std(d))
    # B: flips confined to the section table (180)
    for pname, data in packs.items():
        pe, n, opt, falign, st = layout(data)
        for k in range(60):
            d = case_dir("secflip-%s" % pname)
            b = bytearray(data)
            for _ in range(rng.randint(1, 6)):
                b[rng.randrange(st, st + 40 * n)] = rng.randrange(256)
            add_in(d, bytes(b))
            run_case("secflip-%s-%d" % (pname, k), d, *std(d))
    # C: FileAlignment 0 / 1 / 0xFFFFFFFF, bare and with a header flip (18)
    for pname, data in packs.items():
        pe, n, opt, falign, st = layout(data)
        for fa in (0, 1, 0xFFFFFFFF):
            for variant in ("bare", "flipped"):
                d = case_dir("falign-%s-%#x" % (pname, fa))
                b = bytearray(data)
                struct.pack_into("<I", b, pe + 24 + 36, fa)
                if variant == "flipped":
                    b[rng.randrange(pe, st)] ^= 0xFF
                add_in(d, bytes(b))
                run_case("falign-%s-%#x-%s" % (pname, fa, variant), d, *std(d))
    # D: NumberOfSections 0xFFFF, 0, 1 (9)
    for pname, data in packs.items():
        pe, n, opt, falign, st = layout(data)
        for ns in (0xFFFF, 0, 1):
            d = case_dir("nsec-%s-%d" % (pname, ns))
            b = bytearray(data)
            struct.pack_into("<H", b, pe + 6, ns)
            add_in(d, bytes(b))
            run_case("nsec-%s-%d" % (pname, ns), d, *std(d))
    # E: rawdataptr+size overflowing 32 bits (9)
    for pname, data in packs.items():
        pe, n, opt, falign, st = layout(data)
        variants = [("last-max", {n - 1: (0xFFFFFFFF, 0xFFFFFFFF)}),
                    ("last-high", {n - 1: (0xFFFFF000, 0x10000)}),
                    ("all-max", {k: (0xFFFFFFFF, 0xFFFFFFFF) for k in range(n)})]
        for vn, edits in variants:
            d = case_dir("ovf-%s-%s" % (pname, vn))
            b = bytearray(data)
            for k, (rs, rp) in edits.items():
                struct.pack_into("<II", b, st + 40 * k + 16, rs, rp)
            add_in(d, bytes(b))
            run_case("ovf-%s-%s" % (pname, vn), d, *std(d))
    # F: degenerate sizes (4)
    for tag, data in (("empty", b""), ("one-M", b"M"), ("one-ff", b"\xff"),
                      ("63b-MZ", b"MZ" + b"\x00" * 61)):
        d = case_dir("size-" + tag)
        add_in(d, data)
        run_case("size-" + tag, d, *std(d))
    # P: wild e_lfanew pointers (12)
    for pname, data in packs.items():
        for pev in (0x7FFFFFF0, len(data) - 30, 0x30, 0x3D):
            d = case_dir("lfanew-%s" % pname)
            b = bytearray(data)
            struct.pack_into("<I", b, 0x3C, pev)
            add_in(d, bytes(b))
            run_case("lfanew-%s-%#x" % (pname, pev), d, *std(d))
    # O: truncations at 10% / 50% / end-1 (9)
    for pname, data in packs.items():
        for frac in (0.1, 0.5, 0.999):
            d = case_dir("cut-%s" % pname)
            add_in(d, data[:max(1, int(len(data) * frac))])
            run_case("cut-%s-%g" % (pname, frac), d, *std(d))
    # G: directory as --in
    d = case_dir("in-dir")
    os.makedirs(os.path.join(d, "adir"))
    run_case("in-dir", d, os.path.join(d, "adir"), os.path.join(d, "out.bin"))
    # H: FIFO as --in, no writer (expected hang: no timeout in the tool)
    d = case_dir("in-fifo-nowriter")
    os.mkfifo(os.path.join(d, "in.fifo"))
    run_case("in-fifo-nowriter", d, os.path.join(d, "in.fifo"), os.path.join(d, "out.bin"))
    # H2: FIFO with a writer that closes immediately (EOF -> empty input)
    d = case_dir("in-fifo-eof")
    os.mkfifo(os.path.join(d, "in.fifo"))
    writer = subprocess.Popen(
        [PY, "-c", "import sys; open(sys.argv[1], 'wb').close()", os.path.join(d, "in.fifo")],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    run_case("in-fifo-eof", d, os.path.join(d, "in.fifo"), os.path.join(d, "out.bin"))
    writer.wait(timeout=30)
    # K: dangling symlink and self-loop as --in
    d = case_dir("in-dangling")
    os.symlink(os.path.join(d, "gone.bin"), os.path.join(d, "in.bin"))
    run_case("in-dangling", d, *std(d))
    d = case_dir("in-loop")
    os.symlink(os.path.join(d, "in.bin"), os.path.join(d, "in.bin"))
    run_case("in-loop", d, *std(d))
    # U: unbounded input under RLIMIT_AS 1 GiB and RLIMIT_CPU 15 s
    d = case_dir("in-devzero-capped")
    run_case("in-devzero-capped", d, "/dev/zero", os.path.join(d, "out.bin"), capped=True)
    # I: symlink --out pointing at a victim file (3 packs)
    for pname, data in packs.items():
        d = case_dir("out-symlink-%s" % pname)
        add_in(d, data, "in.bin")
        victim = os.path.join(d, "victim.txt")
        with open(victim, "w") as fh:
            fh.write("DO NOT TOUCH\n")
        os.symlink(victim, os.path.join(d, "out.bin"))
        r = run_case("out-symlink-%s" % pname, d, *std(d))
        with open(victim, "rb") as fh:
            got = sha_bytes(fh.read())
        ok = got == sha_bytes(b"DO NOT TOUCH\n")
        if not ok:
            r["violation"].append("victim-modified")
        r["victim_untouched"] = ok
        r["out_still_symlink"] = os.path.islink(os.path.join(d, "out.bin"))
    # I2: --out symlink to a victim inside a read-only directory (1)
    d = case_dir("out-symlink-dangling-target")
    add_in(d, packs["t32"], "in.bin")
    os.symlink(os.path.join(d, "missing-dir", "victim"), os.path.join(d, "out.bin"))
    run_case("out-symlink-dangling-target", d, *std(d))
    # J: --out in a read-only directory (1)
    d = case_dir("out-rodir")
    add_in(d, packs["t32"], "in.bin")
    os.makedirs(os.path.join(d, "ro"))
    os.chmod(os.path.join(d, "ro"), 0o555)
    r = run_case("out-rodir", d, os.path.join(d, "in.bin"), os.path.join(d, "ro", "out.bin"))
    r["ro_leftovers"] = sorted(snap(os.path.join(d, "ro")))
    os.chmod(os.path.join(d, "ro"), 0o755)
    # L: --out in a missing directory (1)
    d = case_dir("out-nodir")
    add_in(d, packs["t32"], "in.bin")
    run_case("out-nodir", d, os.path.join(d, "in.bin"), os.path.join(d, "no-such-dir", "out.bin"))
    # M: --out is an existing directory (1)
    d = case_dir("out-isdir")
    add_in(d, packs["t32"], "in.bin")
    os.makedirs(os.path.join(d, "outdir"))
    run_case("out-isdir", d, os.path.join(d, "in.bin"), os.path.join(d, "outdir"))
    # N: --in == --out (1)
    d = case_dir("in-eq-out")
    add_in(d, packs["t32"], "in.bin")
    run_case("in-eq-out", d, os.path.join(d, "in.bin"), os.path.join(d, "in.bin"))

    rcs = {}
    for r in RESULTS:
        rcs[str(r["rc"])] = rcs.get(str(r["rc"]), 0) + 1
    viol = [r for r in RESULTS if r["violation"]]
    summary = {"cases": len(RESULTS), "rc_histogram": rcs,
               "max_runtime_secs": round(max(r["secs"] for r in RESULTS), 3),
               "timeout_cap_secs": TMO, "violations": len(viol)}
    with open("/fast/scratch/hyaku/kaidoku-r99/SentinelInputs/results.json", "w") as fh:
        json.dump({"summary": summary, "violations": viol, "results": RESULTS}, fh, indent=1)
    print(json.dumps(summary))
    for r in viol:
        print("VIOLATION", r["id"], r["rc"], r["secs"], r["violation"])


if __name__ == "__main__":
    main()
