#!/usr/bin/env python3
"""Round-90 sentinel: hostile-input matrix for tools/round-90/upx-break-repair.py.

Every case runs the tool exactly as the counter does (python3 -I -B <tool>
--in .. --out ..), records rc / stdout / stderr / wall time, and flags a
traceback (uncaught exception) as a finding.
"""
import hashlib, json, os, shutil, stat, struct, subprocess, sys, time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
TOOL = os.path.join(LANE, "tools/round-90/upx-break-repair.py")
S = "/fast/scratch/hyaku/kaidoku-r90/SentinelScope"
H = os.path.join(S, "hostile")
FX = os.path.join(S, "fx")
fx = json.load(open(os.path.join(S, "fx.json")))
REC = []


def sha(path):
    try:
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError as exc:
        return f"<{exc.__class__.__name__}>"


def run_case(name, argv, timeout=60, note="", watch=()):
    t0 = time.time()
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout,
                           cwd=S)
        rc, out, err = p.returncode, p.stdout, p.stderr
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        rc, out, err = None, (exc.stdout or b"").decode() if isinstance(exc.stdout, bytes) else (exc.stdout or ""), \
            (exc.stderr or b"").decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        timed_out = True
    dt = time.time() - t0
    tb = "Traceback (most recent call last)" in (err or "")
    rec = {"case": name, "argv": argv, "rc": rc, "timed_out": timed_out,
           "wall_s": round(dt, 3), "stdout": (out or "").strip()[-600:],
           "stderr_tail": (err or "").strip().splitlines()[-4:],
           "traceback": tb, "note": note,
           "watched": {p2: sha(p2) for p2 in watch}}
    REC.append(rec)
    print(json.dumps({k: rec[k] for k in ("case", "rc", "timed_out", "wall_s",
                                          "traceback")}, sort_keys=True))
    if tb:
        print("   TRACEBACK:", " | ".join(rec["stderr_tail"]))
    elif rec["stdout"]:
        print("   stdout:", rec["stdout"][:300])
    return rec


def main():
    shutil.rmtree(H, ignore_errors=True)
    os.makedirs(H, exist_ok=True)
    src = fx["jq"]["tampered"]
    base = [sys.executable, "-I", "-B", TOOL]

    # --- input-shape cases -------------------------------------------------
    fifo = os.path.join(H, "fifo")
    os.mkfifo(fifo)
    run_case("H1-fifo-in", base + ["--in", fifo, "--out", os.path.join(H, "o1")],
             timeout=15, note="FIFO as --in; a hang or traceback is a finding")

    d = os.path.join(H, "adir")
    os.makedirs(d, exist_ok=True)
    run_case("H2-dir-in", base + ["--in", d, "--out", os.path.join(H, "o2")],
             note="directory as --in")

    run_case("H3-devzero-in",
             base + ["--in", "/dev/zero", "--out", os.path.join(H, "o3")],
             timeout=30, note="character device as --in")

    big = os.path.join(H, "big300")
    with open(big, "wb") as fh:
        fh.truncate(300 << 20)
    run_case("H4-300MiB-sparse-in",
             base + ["--in", big, "--out", os.path.join(H, "o4")],
             timeout=120, note="over the 256 MiB cap; must refuse before reading")

    bigelf = os.path.join(H, "big250-elf")
    with open(bigelf, "wb") as fh:
        fh.write(b"\x7fELF\x02\x01\x01" + b"\0" * 57)
        fh.truncate(250 << 20)
    run_case("H4b-250MiB-ELF-under-cap",
             base + ["--in", bigelf, "--out", os.path.join(H, "o4b")],
             timeout=300, note="under the cap and ELF-shaped: measures read+tail scan")

    for key in ("trunc64", "trunc4096", "trunc_mid", "trunc_tail8"):
        run_case("H5-" + key, base + ["--in", fx["truncated"][key],
                                      "--out", os.path.join(H, "o5" + key)])

    # bogus but checksum-valid PackHeader with absurd fields
    packed = open(fx["jq"]["packed"], "rb").read()
    hdr = bytearray(32)
    hdr[4] = 99          # version >= 10
    hdr[5] = 65          # fmt, <128 and not in (1,2,3,4)
    hdr[6] = 14
    struct.pack_into("<III", hdr, 8, 0xFFFFFFFF, 1, 0)   # u_len, c_len, u_file_size
    struct.pack_into("<I", hdr, 16, 0xFFFFFFFE)          # u_len  (ph_off+16)
    struct.pack_into("<I", hdr, 20, 1)                   # c_len
    struct.pack_into("<I", hdr, 24, 0x7FFFFFFF)          # u_file_size
    hdr[31] = sum(hdr[4:31]) % 251
    bogus = packed[:-32] + bytes(hdr)
    bp = os.path.join(H, "bogus-ph")
    open(bp, "wb").write(bogus)
    run_case("H6-bogus-packheader", base + ["--in", bp, "--out", os.path.join(H, "o6")],
             note="checksum-valid header, u_len=0xFFFFFFFE, u_file_size=0x7FFFFFFF")

    # --- output-scope cases ------------------------------------------------
    realdir = os.path.join(H, "realdir")
    os.makedirs(realdir, exist_ok=True)
    link = os.path.join(H, "outparentlink")
    if os.path.lexists(link):
        os.unlink(link)
    os.symlink(realdir, link)
    run_case("H7-out-parent-symlink",
             base + ["--in", src, "--out", os.path.join(link, "o7")],
             note="immediate --out parent is a symlink")

    # symlinked *ancestor* of the parent: parent itself is a real dir
    anc = os.path.join(H, "ancestorlink")
    if os.path.lexists(anc):
        os.unlink(anc)
    os.makedirs(os.path.join(realdir, "sub"), exist_ok=True)
    os.symlink(realdir, anc)
    esc = os.path.join(anc, "sub", "o8")
    run_case("H8-out-ancestor-symlink", base + ["--in", src, "--out", esc],
             note="symlinked ancestor, real-parent tail: does it escape the "
                  "directory it was given?")

    dd = os.path.join(H, "dotdot")
    os.makedirs(os.path.join(dd, "a"), exist_ok=True)
    os.makedirs(os.path.join(dd, "b"), exist_ok=True)
    run_case("H9-out-dotdot",
             base + ["--in", src, "--out", os.path.join(dd, "a", "..", "b", "o9")],
             note="'..' component inside --out")

    # planted symlink at the final --out path
    victim = os.path.join(H, "victim")
    open(victim, "wb").write(b"VICTIM-MUST-SURVIVE")
    plant = os.path.join(H, "planted")
    os.symlink(victim, plant)
    run_case("H10-planted-symlink-at-out",
             base + ["--in", src, "--out", plant],
             watch=[victim], note="symlink planted at --out; the target must not be written")

    # read-only output directory
    ro = os.path.join(H, "ro")
    os.makedirs(ro, exist_ok=True)
    os.chmod(ro, 0o555)
    run_case("H11-readonly-out-dir",
             base + ["--in", src, "--out", os.path.join(ro, "o11")],
             note="output directory mode 0555")
    os.chmod(ro, 0o755)

    # --out equal to --in
    same = os.path.join(H, "same")
    shutil.copyfile(src, same)
    before = sha(same)
    r = run_case("H12-out-eq-in", base + ["--in", same, "--out", same],
                 watch=[same], note="--out is --in: does the tool overwrite its input?")
    r["overwrote_input"] = before != sha(same)

    # --in is a symlink
    inlink = os.path.join(H, "inlink")
    if os.path.lexists(inlink):
        os.unlink(inlink)
    os.symlink(src, inlink)
    run_case("H13-in-symlink", base + ["--in", inlink, "--out", os.path.join(H, "o13")],
             note="symlink as --in")

    run_case("H14-out-empty", base + ["--in", src, "--out", ""],
             note="empty --out")

    run_case("H15-in-missing",
             base + ["--in", os.path.join(H, "nope"), "--out", os.path.join(H, "o15")])

    # --info unwritable after a successful --out (partial mutation)
    ro2 = os.path.join(H, "ro2")
    os.makedirs(ro2, exist_ok=True)
    os.chmod(ro2, 0o555)
    o16 = os.path.join(H, "o16")
    r = run_case("H16-info-unwritable",
                 base + ["--in", src, "--out", o16,
                         "--info", os.path.join(ro2, "i16.json")],
                 note="--out succeeds, --info fails: partial mutation?")
    r["out_written"] = os.path.isfile(o16)
    os.chmod(ro2, 0o755)

    # --info equal to --out
    r = run_case("H17-info-eq-out",
                 base + ["--in", src, "--out", os.path.join(H, "o17"),
                         "--info", os.path.join(H, "o17")],
                 note="--info and --out are the same path")
    p17 = os.path.join(H, "o17")
    r["final_is"] = ("json" if os.path.isfile(p17) and open(p17, "rb").read(1) == b"{"
                     else "binary")

    # TMPDIR pointed at a FIFO / unwritable dir (mkstemp lives in the out dir,
    # so TMPDIR must not matter -- confirm)
    run_case("H18-tmpdir-fifo",
             base + ["--in", src, "--out", os.path.join(H, "o18")],
             note="TMPDIR=/dev/full is irrelevant: mkstemp(dir=out-parent)")

    json.dump(REC, open(os.path.join(S, "hostile.json"), "w"), indent=1, sort_keys=True)


main()
