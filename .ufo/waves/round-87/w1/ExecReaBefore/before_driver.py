#!/usr/bin/env python3
"""ExecReaBefore driver (round 87): before/after REA + runtime evidence for R87-C1.

Usage: python3 -I -B before_driver.py <scratch> <out.json>
Packs each pinned carrier with `upx --best -q`, tampers exactly as the counter's
tamper() (packed.replace(b"UPX!", value)), runs REA analyze / upx -t / upx -l /
upx -d / the binary itself on intact, T1-zero and T2-foreign, then runs the
committed repair candidate and REA-analyzes the `upx -d` output.
"""
import hashlib, json, os, shutil, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REPAIR = os.path.join(LANE, "tools/round-87/upx-magic-repair.py")
PKG = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents"
UPX = "/usr/bin/upx"
MAGIC = b"UPX!"
TAMPERS = {"T1-zero": b"\x00\x00\x00\x00", "T2-foreign": b"KDK!"}
CARRIERS = [
    ("jq", "/usr/bin/jq", "e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806", ["--version"]),
    ("xxd", "/usr/bin/xxd", "7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65", ["-v"]),
    ("libz", "/usr/lib/libz.so.1.3.2", "6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9", None),
    ("dinit", "/usr/bin/docker-init", "0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115", ["--version"]),
]
DECLARED = {"jq": 167, "xxd": 99, "libz": 184, "dinit": 1268}


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run(argv, env, timeout=900):
    try:
        p = subprocess.run(argv, capture_output=True, env=env, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"rc": None, "error": "timeout"}
    out = p.stdout.decode("utf-8", "replace")
    err = p.stderr.decode("utf-8", "replace")
    tail = (out + err).strip().splitlines()
    return {"rc": p.returncode, "stdout": out, "stderr": err, "last": tail[-1] if tail else ""}


def rea(path, env):
    r = run(["node", os.path.join(PKG, "scripts", "rea.mjs"), "analyze", "--format", "json", path], env)
    try:
        e = json.loads(r.get("stdout") or "{}")
    except json.JSONDecodeError:
        e = {}
    n = e.get("normalized_result") if isinstance(e, dict) else None
    counts = {k: n.get(k) for k in ("procedure_count", "segment_count", "string_count")} if isinstance(n, dict) else None
    extra = {}
    if isinstance(n, dict):
        for k in ("format", "arch", "entry_point", "packer", "packers", "warnings"):
            if k in n:
                extra[k] = n[k]
    return {"rc": r["rc"], "counts": counts, "evidence_id": e.get("evidence_id") if isinstance(e, dict) else None,
            "normalized_keys": sorted(n.keys()) if isinstance(n, dict) else None, "extra": extra,
            "stderr_last": (r.get("stderr") or "").strip().splitlines()[-1:] }


def upx_state(path, env, d, tag):
    t = run([UPX, "-t", path], env)
    l = run([UPX, "-l", path], env)
    un = os.path.join(d, tag + ".unpacked")
    u = run([UPX, "-d", "-q", "-o", un, path], env)
    return {"upx_t": {"rc": t["rc"], "last": t["last"]}, "upx_l": {"rc": l["rc"], "last": l["last"]},
            "upx_d": {"rc": u["rc"], "last": u["last"],
                      "sha256": sha(un) if u["rc"] == 0 and os.path.isfile(un) else None}}


def main():
    S, outp = sys.argv[1], sys.argv[2]
    env = {"HOME": os.path.join(S, "home"), "TMPDIR": os.path.join(S, "tmp"), "LANG": "C",
           "PATH": os.environ.get("PATH") or "/usr/bin"}
    os.makedirs(env["HOME"], exist_ok=True)
    os.makedirs(env["TMPDIR"], exist_ok=True)
    res = {"upx_version": run([UPX, "--version"], env)["stdout"].splitlines()[0],
           "upx_sha256": sha(UPX), "rea_pkgjson_sha256": sha(os.path.join(PKG, "package.json")),
           "repair_sha256": sha(REPAIR), "carriers": {}}
    for cid, src, pin, rargs in CARRIERS:
        d = os.path.join(S, cid)
        os.makedirs(d, exist_ok=True)
        orig = os.path.join(d, "orig")
        subprocess.run(["cp", "-p", src, orig], check=True)
        c = {"source": src, "orig_sha256": sha(orig), "pin_ok": sha(orig) == pin,
             "declared_orig_procedures": DECLARED[cid], "states": {}}
        packed = os.path.join(d, "packed")
        pk = run([UPX, "--best", "-q", "-o", packed, orig], env)
        c["pack"] = {"argv": f"{UPX} --best -q -o packed orig", "rc": pk["rc"], "last": pk["last"]}
        with open(packed, "rb") as fh:
            pb = fh.read()
        c["packed_sha256"] = hashlib.sha256(pb).hexdigest()
        c["magic_words"] = pb.count(MAGIC)
        c["magic_offsets"] = [i for i in range(len(pb)) if pb.startswith(MAGIC, i)]
        paths = {"orig": orig, "packed": packed}
        for tn, val in TAMPERS.items():
            tp = os.path.join(d, tn)
            with open(tp, "wb") as fh:
                fh.write(pb.replace(MAGIC, val))
            os.chmod(tp, os.stat(packed).st_mode & 0o7777)
            paths[tn] = tp
        for st, p in paths.items():
            s = {"sha256": sha(p), "size": os.path.getsize(p), "rea": rea(p, env)}
            if st != "orig":
                s.update(upx_state(p, env, d, st))
            if rargs is not None:
                r = run([p] + rargs, env, timeout=30)
                s["runtime"] = {"argv": [os.path.basename(p)] + rargs, "rc": r["rc"],
                                "stdout": r.get("stdout", "").strip(),
                                "stderr_last": (r.get("stderr") or "").strip().splitlines()[-1:]}
            c["states"][st] = s
        c["after"] = {}
        for tn in TAMPERS:
            rp = os.path.join(d, tn + ".repaired")
            rr = run([sys.executable, "-I", "-B", REPAIR, "--in", paths[tn], "--out", rp, "--json"], env, 300)
            try:
                rj = json.loads(rr.get("stdout") or "null")
            except json.JSONDecodeError:
                rj = rr.get("stdout")
            a = {"repair_rc": rr["rc"], "repair_json": rj, "repair_stderr_last": (rr.get("stderr") or "").strip().splitlines()[-1:]}
            if rr["rc"] == 0 and os.path.isfile(rp):
                a["repaired_sha256"] = sha(rp)
                a["repaired_equals_packed"] = sha(rp) == c["packed_sha256"]
                a.update(upx_state(rp, env, d, tn + ".repaired"))
                un = os.path.join(d, tn + ".repaired.unpacked")
                a["identity"] = a["upx_d"]["sha256"] == pin
                if os.path.isfile(un):
                    a["rea_unpacked"] = rea(un, env)
                    pc = (a["rea_unpacked"]["counts"] or {}).get("procedure_count")
                    a["procedure_count_matches_declared"] = pc == DECLARED[cid]
                if rargs is not None:
                    os.chmod(rp, 0o755)
                    r = run([rp] + rargs, env, timeout=30)
                    a["runtime_repaired"] = {"rc": r["rc"], "stdout": r.get("stdout", "").strip()}
            c["after"][tn] = a
        res["carriers"][cid] = c
    with open(outp, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
