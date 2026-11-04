import hashlib, json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

S = "/fast/scratch/hyaku/kaidoku-r87/ExecRepairCases"
CAND = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-87/w1/ExecRepairCases/candidate/upx-magic-repair.py"
UPX = "/usr/bin/upx"
CARRIERS = {"jq": "/usr/bin/jq", "xxd": "/usr/bin/xxd", "libz": "/usr/lib/libz.so.1.3.2",
            "dinit": "/usr/bin/docker-init"}
RUNARGS = {"jq": ["--version"], "xxd": ["-v"], "dinit": ["--version"]}
MODES = {"best": ["--best"], "1": ["-1"], "lzma": ["--lzma"], "best-brute": ["--best", "--brute"]}
TAMPERS = {"T1": b"\0\0\0\0", "T2": b"KDK!"}
ENV = {"PATH": "/usr/bin", "LANG": "C", "HOME": S + "/home", "TMPDIR": S + "/tmp"}
M = b"UPX!"


def sha(b): return hashlib.sha256(b).hexdigest()


def run(argv, timeout=900):
    t = time.time()
    try:
        p = subprocess.run(argv, capture_output=True, text=True, env=ENV, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip().splitlines()[-1:], round(time.time() - t, 1)
    except subprocess.TimeoutExpired:
        return "timeout", [], round(time.time() - t, 1)


def runout(path, args):
    try:
        p = subprocess.run([path, *args], capture_output=True, env=ENV, timeout=30)
        return p.returncode, sha(p.stdout + p.stderr)
    except Exception as e:  # noqa
        return repr(e), None


def offs(b):
    r, i = [], b.find(M)
    while i != -1:
        r.append(i); i = b.find(M, i + 1)
    return r


def one(cid, mode):
    d = f"{S}/probe/{cid}-{mode}"; os.makedirs(d, exist_ok=True)
    orig = open(CARRIERS[cid], "rb").read()
    src = f"{d}/orig"; open(src, "wb").write(orig); os.chmod(src, 0o755)
    packed = f"{d}/packed"
    if os.path.exists(packed): os.remove(packed)
    rc, tail, secs = run([UPX, *MODES[mode], "-q", "-o", packed, src], timeout=300)
    row = {"carrier": cid, "mode": " ".join(MODES[mode]), "pack_rc": rc, "pack_s": secs,
           "orig_sha256": sha(orig)}
    if rc != 0:
        row["pack_tail"] = tail; return [row]
    pb = open(packed, "rb").read()
    row.update(packed_sha256=sha(pb), packed_size=len(pb), magic_offsets=offs(pb))
    ref = runout(src, RUNARGS[cid]) if cid in RUNARGS else None
    rows = []
    for tn, tv in TAMPERS.items():
        r = dict(row, tamper=tn)
        tb = pb.replace(M, tv); tp = f"{d}/{tn}.t"; open(tp, "wb").write(tb)
        r["tampered_sha256"] = sha(tb)
        r["pre_upx_t_rc"] = run([UPX, "-t", "-q", tp])[0]
        out = f"{d}/{tn}.r"
        p = subprocess.run([sys.executable, "-I", "-B", CAND, "--in", tp, "--out", out, "--json"],
                           capture_output=True, text=True, env=ENV)
        r["repair_rc"] = p.returncode
        if p.returncode != 0:
            r["repair_err"] = p.stderr.strip(); rows.append(r); continue
        info = json.loads(p.stdout)
        ob = open(out, "rb").read()
        r["repaired_sha256"] = sha(ob)
        r["anchors"] = info["anchors"]; r["walk"] = info["walk"]
        r["unrestored_offsets"] = [o for o in row["magic_offsets"] if ob[o:o + 4] != M]
        diff = [i for i in range(len(ob)) if ob[i] != tb[i]] if len(ob) == len(tb) else None
        r["windows_only"] = diff is not None and all(
            any(o <= i < o + 4 and ob[o:o + 4] == M for o in info["anchors"].values()) for i in diff)
        r["equals_packed"] = ob == pb
        r["upx_t_rc"] = run([UPX, "-t", "-q", out])[0]
        un = f"{d}/{tn}.u"
        if os.path.exists(un): os.remove(un)
        urc = run([UPX, "-d", "-q", "-o", un, out])[0]
        r["upx_d_rc"] = urc
        r["identity"] = urc == 0 and os.path.isfile(un) and sha(open(un, "rb").read()) == sha(orig)
        if ref is not None:
            os.chmod(out, 0o755)
            r["runs_like_orig"] = runout(out, RUNARGS[cid]) == ref
            os.chmod(tp, 0o755)
            r["tampered_runs_like_orig"] = runout(tp, RUNARGS[cid]) == ref
        rows.append(r)
    return rows


if __name__ == "__main__":
    os.makedirs(S + "/home", exist_ok=True); os.makedirs(S + "/tmp", exist_ok=True)
    jobs = [(c, m) for c in CARRIERS for m in MODES]
    with ThreadPoolExecutor(8) as ex:
        res = [r for rows in ex.map(lambda a: one(*a), jobs) for r in rows]
    json.dump(res, open(sys.argv[1], "w"), indent=1, sort_keys=True)
    for r in res:
        print("|", " | ".join(str(r.get(k)) for k in (
            "carrier", "mode", "tamper", "pack_rc", "pack_s", "magic_offsets", "unrestored_offsets",
            "repair_rc", "windows_only", "upx_t_rc", "identity", "runs_like_orig",
            "tampered_runs_like_orig", "repair_err")), "|")
