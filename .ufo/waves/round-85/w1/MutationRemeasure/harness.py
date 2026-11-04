#!/usr/bin/env python3
"""MutationRemeasure harness (independent of tools/round-84/mutation-closure.py).

For each row of a mutant table:
  1. target bytes come from `git show <rev>:<target>` (or an overlay directory when --overlay is given
     and the overlay holds that target);
  2. the declared `find` must occur exactly once in those bytes (every edit, when `edits` is present);
  3. the target is written to <work>/pristine/<basename>, selftested (`python3 -I -B <copy> --selftest`,
     cwd=<work>, TMPDIR=<work>), and must be green (rc 0, no failing case);
  4. the mutant bytes are written over the same pristine path, selftested, and the pristine bytes are
     restored and re-hashed (must equal the pristine sha256) before the next row;
  5. KILLED only when: pristine green AND mutant rc != 0 AND declared_case is among the failing names
     parsed from the mutant output AND the mutant run did not crash with a traceback.
Failing names are parsed from (a) JSON objects carrying a "failures" list, (b) "selftest <name>: FAIL"
lines. Nothing else counts as a named failure; rc != 0 without a named failure is recorded as
"unnamed-failure" and is NOT a kill.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

LINE_FAIL = re.compile(r"^selftest (\S+): FAIL\b", re.M)
LINE_OK = re.compile(r"^selftest (\S+): ok\b", re.M)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_show(root, rev, path):
    p = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"], capture_output=True)
    return p.stdout if p.returncode == 0 else None


def parse_names(out: str):
    fails, names = set(), set()
    dec = json.JSONDecoder()
    i = 0
    while True:
        b = out.find("{", i)
        if b < 0:
            break
        try:
            val, end = dec.raw_decode(out[b:])
        except json.JSONDecodeError:
            i = b + 1
            continue
        i = b + end
        if isinstance(val, dict) and isinstance(val.get("failures"), list):
            fails |= {x for x in val["failures"] if isinstance(x, str)}
            names |= {x for x in (val.get("case_names") or []) if isinstance(x, str)}
    fails |= set(LINE_FAIL.findall(out))
    names |= set(LINE_OK.findall(out)) | fails
    return sorted(fails), sorted(names)


def selftest(copy: str, work: str):
    env = dict(os.environ, TMPDIR=work, PYTHONDONTWRITEBYTECODE="1")
    try:
        p = subprocess.run([sys.executable, "-I", "-B", copy, "--selftest"], cwd=work, env=env,
                           capture_output=True, text=True, timeout=600)
        rc, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        rc, out, err = 124, (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or ""), "timeout"
    fails, names = parse_names(out)
    m = re.search(r"^SELFTEST cases=(\d+) failures=(\d+)$", out, re.M)
    return {"rc": rc, "failing": fails, "case_names": names,
            "cases": int(m.group(1)) if m else None,
            "failures_declared": int(m.group(2)) if m else None,
            "traceback": "Traceback" in err or "Traceback" in out,
            "stderr_tail": err[-400:], "stdout_tail": out[-300:]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", required=True)
    ap.add_argument("--root", default="/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
    ap.add_argument("--rev", default="91eeb72f6a7b13dc96e826117956f90ed89ae3f3")
    ap.add_argument("--overlay", default=None, help="dir holding repo-relative candidate targets")
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default=None, help="comma list of row ids")
    a = ap.parse_args()
    table = json.loads(Path(a.table).read_text())
    rows = table["mutants"]
    if a.only:
        keep = set(a.only.split(","))
        rows = [r for r in rows if r["id"] in keep]
    work = Path(a.work)
    pdir = work / "pristine"
    pdir.mkdir(parents=True, exist_ok=True)
    # pristine bytes per target
    tgt_bytes, tgt_src, pristine_res = {}, {}, {}
    for r in rows:
        t = r["target"]
        if t in tgt_bytes:
            continue
        b, src = None, None
        if a.overlay and (Path(a.overlay) / t).exists():
            b, src = (Path(a.overlay) / t).read_bytes(), f"overlay:{a.overlay}/{t}"
        else:
            b, src = git_show(a.root, a.rev, t), f"git:{a.rev}:{t}"
        if b is None:
            sys.exit(f"target absent: {t}")
        tgt_bytes[t], tgt_src[t] = b, src
    for t, b in tgt_bytes.items():
        copy = pdir / Path(t).name
        copy.write_bytes(b)
        res = selftest(str(copy), str(work))
        res.update({"target": t, "source": tgt_src[t], "sha256": sha(b)})
        res["green"] = res["rc"] == 0 and not res["failing"]
        pristine_res[t] = res
    results = []
    for r in rows:
        t = r["target"]
        text = tgt_bytes[t].decode("utf-8")
        edits = r.get("edits") or [{"find": r["find"], "replace": r["replace"]}]
        counts = [text.count(e["find"]) for e in edits]
        entry = {"id": r["id"], "target": t, "declared_case": r["declared_case"],
                 "anchor_counts": counts}
        if any(c != 1 for c in counts):
            entry["status"] = "inconclusive-anchor"
            results.append(entry)
            continue
        mutated = text
        for e in edits:
            mutated = mutated.replace(e["find"], e["replace"], 1)
        assert mutated != text
        copy = pdir / Path(t).name
        pb = tgt_bytes[t]
        copy.write_bytes(mutated.encode("utf-8"))
        try:
            mres = selftest(str(copy), str(work))
        finally:
            copy.write_bytes(pb)
        restored = sha(copy.read_bytes()) == sha(pb)
        entry.update({"mutant_rc": mres["rc"], "mutant_failing": mres["failing"],
                      "mutant_cases": mres["cases"], "mutant_failures_declared": mres["failures_declared"],
                      "traceback": mres["traceback"], "pristine_restored_sha_ok": restored,
                      "pristine_green": pristine_res[t]["green"],
                      "declared_in_pristine_inventory": r["declared_case"] in pristine_res[t]["case_names"],
                      "stderr_tail": mres["stderr_tail"]})
        if not restored:
            entry["status"] = "harness-error-restore"
        elif not pristine_res[t]["green"]:
            entry["status"] = "inconclusive-pristine-red"
        elif mres["rc"] != 0 and r["declared_case"] in mres["failing"] and not mres["traceback"]:
            entry["status"] = "killed"
        elif mres["rc"] != 0 and not mres["failing"]:
            entry["status"] = "survived-unnamed-failure"
        elif mres["rc"] != 0 and mres["traceback"]:
            entry["status"] = "survived-crash"
        else:
            entry["status"] = "survived"
        results.append(entry)
    # final re-hash of pristine files
    final = {t: sha((pdir / Path(t).name).read_bytes()) == sha(b) for t, b in tgt_bytes.items()}
    killed = [e["id"] for e in results if e["status"] == "killed"]
    out = {"schema": "kaidoku-r85-mutation-remeasure-v1", "table": a.table,
           "table_sha256": sha(Path(a.table).read_bytes()), "rev": a.rev,
           "overlay": a.overlay, "pristine": pristine_res, "pristine_final_hash_ok": final,
           "rows": len(rows), "killed_count": len(killed), "killed": killed, "results": results}
    Path(a.out).write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({"rows": len(rows), "killed": len(killed), "killed_ids": killed,
                      "pristine_green": {t: p["green"] for t, p in pristine_res.items()}}, indent=1))


if __name__ == "__main__":
    main()
