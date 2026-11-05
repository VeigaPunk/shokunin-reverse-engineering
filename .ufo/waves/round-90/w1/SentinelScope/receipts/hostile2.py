#!/usr/bin/env python3
"""Remaining write-scope cases for tools/round-90/upx-break-repair.py."""
import hashlib, json, os, shutil, subprocess, sys, time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
TOOL = LANE + "/tools/round-90/upx-break-repair.py"
S = "/fast/scratch/hyaku/kaidoku-r90/SentinelScope"
H = os.path.join(S, "hostile")
fx = json.load(open(os.path.join(S, "fx.json")))
src = fx["jq"]["tampered"]
REC = []


def ln(target, link):
    subprocess.run(["ln", "-s", target, link], check=False)


def sha(p):
    try:
        with open(p, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError as exc:
        return "<%s>" % exc.__class__.__name__


def run(name, out, timeout=60, watch=(), note=""):
    argv = [sys.executable, "-I", "-B", TOOL, "--in", src, "--out", out]
    t0 = time.time()
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout,
                           cwd=S)
        rc, so, se, tmo = p.returncode, p.stdout, p.stderr, False
    except subprocess.TimeoutExpired:
        rc, so, se, tmo = None, "", "", True
    tb = "Traceback (most recent call last)" in (se or "")
    rec = {"case": name, "rc": rc, "timeout": tmo, "traceback": tb,
           "wall_s": round(time.time() - t0, 3),
           "stdout": (so or "").strip()[-220:],
           "stderr_tail": (se or "").strip().splitlines()[-2:],
           "watched": {p2: sha(p2) for p2 in watch}, "note": note,
           "out_is_symlink": os.path.islink(out) if out else None,
           "out_exists": os.path.isfile(out) if out else None}
    REC.append(rec)
    print(json.dumps({k: rec[k] for k in ("case", "rc", "traceback", "out_exists",
                                          "out_is_symlink")}))
    if tb:
        print("   TB:", " | ".join(rec["stderr_tail"])[:300])
    if rec["stdout"]:
        print("   out:", rec["stdout"][:200])
    return rec


def main():
    d = os.path.join(H, "w2")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)

    ro = os.path.join(d, "rofile")
    open(ro, "wb").write(b"READONLY-FILE-CONTENT")
    os.chmod(ro, 0o444)
    r = run("H19-readonly-file-out", ro, watch=[ro])
    r["content_head"] = open(ro, "rb").read(16).decode("latin1")
    r["replaced_readonly_file"] = r["content_head"] != "READONLY-FILE-CO"

    dl = os.path.join(d, "dangling")
    ln(os.path.join(d, "nope-target"), dl)
    r = run("H20-dangling-symlink-out", dl)
    r["target_created"] = os.path.exists(os.path.join(d, "nope-target"))

    tgt = os.path.join(d, "adir")
    os.makedirs(tgt, exist_ok=True)
    sl = os.path.join(d, "dirlink")
    ln(tgt, sl)
    run("H21-dir-symlink-out", sl)

    run("H22-missing-parent", os.path.join(d, "nodir", "x"))

    nf = os.path.join(d, "afile")
    open(nf, "wb").write(b"x")
    run("H23-parent-is-file", os.path.join(nf, "x"))

    json.dump(REC, open(os.path.join(S, "hostile2.json"), "w"), indent=1,
              sort_keys=True)


main()
