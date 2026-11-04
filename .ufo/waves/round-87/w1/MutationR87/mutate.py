#!/usr/bin/env python3
"""MutationR87 driver: single-edit mutants of the R87-C1 repair and counter.

Mutants are written into scratch from the pristine bytes read at
--lane (pinned sha256 asserted); production files are only ever read.
Each anchor must occur exactly once in the pristine source.
Usage: python3 -I -B mutate.py --lane <lane> --scratch <dir> --out <seat dir> [--jobs N]
"""
import argparse, concurrent.futures as cf, hashlib, json, os, subprocess, sys, time

REPAIR = "tools/round-87/upx-magic-repair.py"
COUNTER = "tools/round-87/upx-tamper-battery.py"
PIN = {REPAIR: "f4ebd152495dc832180fff3d1ca3447937a7dad121ba63d57872003ffcc49723",
       COUNTER: "0f2d2bd80108ded5282dbb8cbf79044357538458143c97ee591cc78e8e5384b0"}
PKG = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents"

R_MUT = [  # id, description, old, new
 ("R01", "checksum mod 251 -> 256", "% 251", "% 256"),
 ("R02", "checksum includes magic (buf[0:31])", "sum(buf[4:PH_SIZE - 1])", "sum(buf[0:PH_SIZE - 1])"),
 ("R03", "p_filesize offset 12 -> 8", "m = p - 12", "m = p - 8"),
 ("R04", "drop l_info version/format cross-check",
  'if d[m + 6] == ph["version"] and d[m + 7] == ph["format"]:', "if True:"),
 ("R05", "sentinel accepts nonzero word3 (method/ftid/cto8/unused)",
  ' and d[s + 8:s + 12] == b"\\0\\0\\0\\0"', ""),
 ("R06", "resume scan starts at stop instead of stop+1", "range(stop + 1, ph_off - 12)", "range(stop, ph_off - 12)"),
 ("R07", "walk_chain method-match check removed", "elif meth != method:", "elif False:"),
 ("R08", "resume-candidate method check removed", " or d[s + 8] != method or", " or"),
 ("R09", "PackHeader scan from the front (first, not last)",
  "range(n - PH_SIZE, lo - 1, -1)", "range(lo, n - PH_SIZE + 1)"),
 ("R10", "write UPX! at sentinel instead of sentinel+4", '"b_info_end": sentinel + 4', '"b_info_end": sentinel'),
 ("R11", "intact check inverted (rewrite only anchors already UPX!)",
  "if out[off:off + 4] != MAGIC:", "if out[off:off + 4] == MAGIC:"),
 ("R12", "drop the ELF/endianness gate",
  'if d[:4] != b"\\x7fELF" or len(d) < 64 or d[5] != 1:', "if len(d) < 64:"),
 ("R13", "drop the l_info anchor", '"l_info": l_magic, ', ""),
 ("R14", "PackHeader version gate dropped", "if version < 10 or fmt >= 128", "if fmt >= 128"),
 ("R15", "PackHeader length sanity dropped",
  "if not (0 < c_len <= n and 0 < u_len and 0 < u_file_size):", "if False:"),
 ("R16", "TAIL_WINDOW 512 -> 32", "TAIL_WINDOW = 512", "TAIL_WINDOW = 32"),
 ("R17", "resume candidate allows sz_cpr == sz_unc", "if not (0 < sz_cpr < sz_unc)", "if not (0 < sz_cpr <= sz_unc)"),
 ("R18", "walk_chain drops sz_cpr > sz_unc bound", " or sz_cpr > sz_unc or", " or"),
 ("R19", "refuse when first walk finds 0 blocks dropped", "if n1 == 0:", "if False:"),
 ("R20", "selftest exit forced 0", "return 0 if not fails else 1", "return 0"),
 ("R21", "intact flag inverted", '"intact": not restored', '"intact": bool(restored)'),
 ("R22", "l_info search from offset 0 and allows m<4", "if m >= 4 and m + 20 <= ph_off:", "if m + 20 <= ph_off:"),
]

C_MUT = [
 ("C01", "windows_only always True", '    """Every differing byte lies inside a 4-byte window that now reads UPX!."""\n',
  '    """Every differing byte lies inside a 4-byte window that now reads UPX!."""\n    return True, ""\n'),
 ("C02", "N2 control check removed", '"N2-corrupt-payload": not any(x["recovered"] for x in controls["N2-corrupt-payload"]),',
  '"N2-corrupt-payload": True,'),
 ("C03", "identity arm compares packed sha", 'arms["identity"] = usha == c["sha256"]',
  'arms["identity"] = usha == sha256_bytes(pbytes)'),
 ("C04", "identity arm accepts any successful unpack", 'arms["identity"] = usha == c["sha256"]',
  'arms["identity"] = usha is not None'),
 ("C05", "met ignores controls", "met = recovered == TARGET and all(ctl_ok.values())", "met = recovered == TARGET"),
 ("C06", "tamper leaves the last magic word", "return packed.replace(MAGIC, value)",
  "return packed.replace(MAGIC, value, max(packed.count(MAGIC) - 1, 0))"),
 ("C07", "precondition (upx -t fails on tampered) skipped", 'if pre_t["rc"] == 0:', "if False:"),
 ("C08", "test_ok arm always True", 'arms["test_ok"] = t["rc"] == 0', 'arms["test_ok"] = True'),
 ("C09", "repair_rc0 ignores exit code", 'arms["repair_rc0"] = rr["rc"] == 0 and os.path.isfile(outp)',
  'arms["repair_rc0"] = os.path.isfile(outp)'),
 ("C10", "N1 refuse always True", '"refused": n1["rc"] != 0', '"refused": True'),
 ("C11", "N3 ignores bytes (rc only)", 'same = n3["rc"] == 0 and os.path.isfile(n3o) and sha256_file(n3o) == sha256_bytes(pbytes)',
  'same = n3["rc"] == 0'),
 ("C12", "recovered ignores the rea arm", 'case["recovered"] = all(arms.values())',
  'case["recovered"] = all(v for k, v in arms.items() if k != "rea_recover")'),
 ("C13", "N2 flips no byte", "tb[mid] ^= 0xFF", "tb[mid] ^= 0x00"),
 ("C14", "T2 tamper value equals T1 (zero)", 'TAMPERS = {"T1-zero": b"\\x00\\x00\\x00\\x00", "T2-foreign": b"KDK!"}',
  'TAMPERS = {"T1-zero": b"\\x00\\x00\\x00\\x00", "T2-foreign": b"\\x00\\x00\\x00\\x00"}'),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def mutate(src, old, new):
    n = src.count(old)
    if n != 1:
        raise SystemExit(f"anchor count {n} for {old!r}")
    return src.replace(old, new)


def run(argv, cwd, timeout=3000):
    t0 = time.time()
    try:
        p = subprocess.run(argv, capture_output=True, text=True, cwd=cwd, timeout=timeout,
                           env={"PATH": os.environ["PATH"], "LANG": "C", "HOME": cwd, "TMPDIR": cwd})
        return {"rc": p.returncode, "out": (p.stdout + p.stderr).strip()[-600:], "secs": round(time.time() - t0, 1)}
    except subprocess.TimeoutExpired:
        return {"rc": None, "out": "timeout", "secs": round(time.time() - t0, 1)}


def summarize(receipt_path):
    try:
        r = json.load(open(receipt_path))
    except Exception as exc:
        return {"error": f"no receipt: {exc}"}
    if "unevaluable" in r:
        return {"exit": r.get("exit"), "unevaluable": r["unevaluable"], "met": r.get("met_target")}
    nonrea = [all(v for k, v in c["arms"].items() if k != "rea_recover") for c in r["cases"]]
    arms = {f'{c["carrier"]}/{c["tamper"]}': sorted(k for k, v in c["arms"].items() if not v) for c in r["cases"]}
    return {"exit": r["exit"], "met": r["met_target"], "recovered": r["recovered"],
            "nonrea_recovered": sum(nonrea), "controls_ok": r["controls_ok"],
            "false_arms": arms, "label": r["label"],
            "repaired_equals_packed": sum(1 for c in r["cases"] if c.get("repaired_equals_packed"))}


def counter_run(job):
    cid, counter, repair, rea, scratch, outdir = job
    w = os.path.join(scratch, "work", cid)
    os.makedirs(w, exist_ok=True)
    rj = os.path.join(outdir, "receipts", f"{cid}.json")
    argv = [sys.executable, "-I", "-B", counter, "--root", LANE, "--repair-cmd", repair,
            "--work", w, "--json-out", rj, "--pkg", PKG]
    if not rea:
        argv.append("--no-rea")
    res = run(argv, w)
    res["summary"] = summarize(rj)
    return cid, res


def main():
    global LANE
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane"); ap.add_argument("--scratch"); ap.add_argument("--out")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    LANE = a.lane
    os.makedirs(os.path.join(a.out, "receipts"), exist_ok=True)
    os.makedirs(os.path.join(a.scratch, "m"), exist_ok=True)
    before = {}
    src = {}
    for f in (REPAIR, COUNTER):
        b = open(os.path.join(a.lane, f), "rb").read()
        before[f] = sha(b)
        assert before[f] == PIN[f], (f, before[f])
        src[f] = b.decode()
    files, jobs, meta = {}, [], {}
    pr = os.path.join(a.scratch, "m", "R00-pristine-repair.py"); open(pr, "w").write(src[REPAIR])
    pc = os.path.join(a.scratch, "m", "C00-pristine-counter.py"); open(pc, "w").write(src[COUNTER])
    assert sha(open(pr, "rb").read()) == PIN[REPAIR] and sha(open(pc, "rb").read()) == PIN[COUNTER]
    # baselines
    jobs += [("B-repair", pc, pr, False), ("B-identity", pc, "identity", True),
             ("B-naive", pc, "naive-global", False)]
    for mid, desc, old, new in R_MUT:
        p = os.path.join(a.scratch, "m", f"{mid}.py")
        txt = mutate(src[REPAIR], old, new); open(p, "w").write(txt)
        meta[mid] = {"kind": "repair", "desc": desc, "old": old, "new": new, "sha256": sha(txt.encode()), "path": p}
        jobs.append((mid, pc, p, False))
    for mid, desc, old, new in C_MUT:
        p = os.path.join(a.scratch, "m", f"{mid}.py")
        txt = mutate(src[COUNTER], old, new); open(p, "w").write(txt)
        meta[mid] = {"kind": "counter", "desc": desc, "old": old, "new": new, "sha256": sha(txt.encode()), "path": p}
        jobs += [(f"{mid}-repair", p, pr, False), (f"{mid}-identity", p, "identity", True),
                 (f"{mid}-naive", p, "naive-global", False)]
    # selftests (cheap, serial)
    selft = {"R00": run([sys.executable, "-I", "-B", pr, "--selftest"], a.scratch),
             "C00": run([sys.executable, "-I", "-B", pc, "--selftest"], a.scratch)}
    for mid, m in meta.items():
        selft[mid] = run([sys.executable, "-I", "-B", m["path"], "--selftest"], a.scratch)
    results = {}
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        futs = [ex.submit(counter_run, (cid, c, r, rea, a.scratch, a.out)) for cid, c, r, rea in jobs]
        for f in cf.as_completed(futs):
            cid, res = f.result()
            results[cid] = res
            print(cid, res["secs"], json.dumps({k: v for k, v in res["summary"].items() if k != "false_arms"}), flush=True)
    after = {f: sha(open(os.path.join(a.lane, f), "rb").read()) for f in (REPAIR, COUNTER)}
    pristine_after = {"R00": sha(open(pr, "rb").read()), "C00": sha(open(pc, "rb").read())}
    json.dump({"before": before, "after": after, "pristine_copies_after": pristine_after,
               "meta": meta, "selftests": selft, "results": results},
              open(os.path.join(a.out, "raw-results.json"), "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
