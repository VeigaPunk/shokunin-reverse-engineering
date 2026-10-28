#!/usr/bin/env python3
"""R46W1MutC1Checks: mutation campaign against tools/round-46/attest.py --selftest.

Two byte-sets are attacked:
  base = tools/round-46/attest.py at 31820472 (the freeze named in the seat prompt; 15 cases)
  head = tools/round-46/attest.py at the pinned/HEAD bytes (16 cases; sha256 e6c44d2d...)

Each mutant is ONE semantic change to one check. A mutant is KILLED when a selftest case
that is green in the baseline goes red; a survivor is a coverage hole and we name the case
that should have caught it.
"""
import concurrent.futures as cf
import datetime
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r46/R46W1MutC1Checks"
BASE = os.path.join(S, "base")   # frozen at 31820472
HEAD = os.path.join(S, "head")   # pinned bytes (e6c44d2d...)
MUT = os.path.join(S, "mutants")
REC = os.path.join(S, "receipts")

# (id, description, version-specific old/new pairs)
MUTANTS = [
    ("m1-marker-count", "clause 1: marker_occurrences != 1 -> < 1 (a doubled marker passes)",
     {"*": ("        if occurrences != 1:\n", "        if occurrences < 1:\n")}),

    ("m2-not-last", "clause 1: drop the is-last-craft-block check",
     {"*": ('        if hard and not receipt["block_is_last"]:\n'
            '            failing.append("marker block is not the last craft block")\n',
            "")}),

    ("m3-header-prefix", "clause 2: header cells matched by prefix instead of equality",
     {"*": ('            header_ok = header == spec["header"]\n',
            '            header_ok = (len(header) == len(spec["header"]) and\n'
            '                         all(h.startswith(s) for h, s in\n'
            '                             zip(header, spec["header"])))\n')}),

    ("m4-rows-floor-8", "clause 3: r46 min_rows 13 -> 8",
     {"*": ('"v2 arm", "exit"], "min_rows": 13,', '"v2 arm", "exit"], "min_rows": 8,')}),

    ("m5-drop-exit-cell", "clause 3: drop the exit-cell membership check",
     {"*": ('        bad_exit = [r for r in rows if exit_col is None or exit_col >= len(r)\n'
            '                    or r[exit_col].strip("` ") not in {"0", "1", "2"}]\n'
            '        if bad_exit:\n'
            '            failing.append(f"exit cells outside {{0,1,2}}: {len(bad_exit)}")\n',
            '        bad_exit = []\n')}),

    ("m6-drop-routed", "clause 4: drop the routed-id check",
     {"*": ('            missing = [i for i in ROUTED if i not in found]\n',
            '            missing = []\n')}),

    ("m7-vocab-whole-row", "clause 4: vocabulary matched by substring over the whole row, "
                           "not the arm cell",
     {"*": ('            novocab = [r for r in rows if len(r) > arm_col\n'
            '                       and not any(t in r[arm_col].lower() for t in ARMS)]\n',
            '            novocab = [r for r in rows\n'
            '                       if not any(t in " ".join(r).lower() for t in ARMS)]\n')}),

    ("m8-pin-by-length", "clause 6: sha256 pin compared by length only",
     {"*": ('                if got != want:\n',
            '                if len(got or "") != len(want):\n')}),

    # --- extra probes beyond the required eight ---
    ("m9-drop-allowlist", "clause 5: citations outside the validated path set accepted",
     {"*": ('        if not name.startswith(spec["allow"]):\n',
            '        if False and not name.startswith(spec["allow"]):\n')}),

    ("m10-drop-refs-min", "clause 5: refs_min floor dropped",
     {"*": ('        if len(refs) < spec["refs_min"]:\n',
            '        if False:\n')}),

    ("m11-no-line-selector", "clause 5: hard profile stops requiring a line selector",
     {"base": ('        if spec["require_line"] and not first:\n',
               '        if False and spec["require_line"] and not first:\n'),
      "head": ('        if hard and spec["require_line"] and not first:\n',
               '        if False and hard and spec["require_line"] and not first:\n')}),

    ("m12-must-cite-refs", "clause 5: does not cite round-45.md accepted",
     {"base": ('        for name in spec["must_cite_refs"]:\n'
               '            if name not in cited:\n'
               '                failing.append(f"does not cite {name}")\n',
               '        for name in []:\n'
               '            if name not in cited:\n'
               '                failing.append(f"does not cite {name}")\n'),
      "head": ('            for name in spec["must_cite_refs"]:\n'
               '                if name not in cited:\n'
               '                    failing.append(f"does not cite {name}")\n',
               '            for name in []:\n'
               '                if name not in cited:\n'
               '                    failing.append(f"does not cite {name}")\n')}),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_selftest(d):
    name = os.path.basename(d)
    tmp = os.path.join(d, "tmp")
    scr = os.path.join(d, "scr")
    os.makedirs(tmp, exist_ok=True)
    os.makedirs(scr, exist_ok=True)
    env = dict(os.environ, TMPDIR=tmp, HYAKU_SCRATCH=scr)
    t0 = utc()
    r = subprocess.run([sys.executable, "-I", "-B", os.path.join(d, "attest.py"),
                        "--root", "/nonexistent", "--freeze", "deadbeef",
                        "--rev", "deadbeef", "--selftest"],
                       cwd=d, env=env, capture_output=True, text=True, timeout=1800)
    out = r.stdout + r.stderr
    cases, failures, parsed = [], None, None
    for line in r.stdout.splitlines():
        if line.startswith("ATTEST_SELFTEST:"):
            failures = int(line.split("failures=")[1])
            cases = int(line.split("cases=")[1].split()[0])
            break
    body = r.stdout.split("ATTEST_SELFTEST:", 1)[1].split("\n", 2)[-1] if "ATTEST_SELFTEST:" in r.stdout else ""
    for chunk in (body, r.stdout.split("\n}", 1)[0] if False else ""):
        try:
            parsed = json.loads(chunk)["cases"]
            break
        except Exception:
            parsed = None
    if parsed is None:
        i = r.stdout.find("\n{")
        if i >= 0:
            try:
                parsed = json.loads(r.stdout[i:])["cases"]
            except Exception:
                parsed = None
    return {
        "dir": d, "utc": t0, "exit": r.returncode, "cases": cases,
        "failures": failures, "stdout_sha256": sha(out.encode()),
        "stdout_head": out.splitlines()[0][:160] if out else "",
        "case_rows": parsed,
    }


def build(ver, mid, spec_pairs):
    src = BASE if ver == "base" else HEAD
    d = os.path.join(MUT, f"{ver}-{mid}")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for f in ("attest.py", "gate.py"):
        shutil.copy2(os.path.join(src, f), os.path.join(d, f))
    p = os.path.join(d, "attest.py")
    text = open(p).read()
    pair = spec_pairs.get(ver) or spec_pairs["*"]
    old, new = pair
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{ver}/{mid}: anchor occurs {n} times, expected 1")
    newtext = text.replace(old, new, 1)
    open(p, "w").write(newtext)
    diff = list(difflib.unified_diff(text.splitlines(True), newtext.splitlines(True),
                                     "attest.orig.py", "attest.mut.py", n=1))
    with open(os.path.join(d, "mutant.diff"), "w") as fh:
        fh.writelines(diff)
    return d, sha(newtext.encode()), sha(text.encode()), "".join(diff)


def main():
    os.makedirs(MUT, exist_ok=True)
    os.makedirs(REC, exist_ok=True)
    jobs = {}
    # baselines: fresh copies so the working dirs never mix
    for ver, src in (("base", BASE), ("head", HEAD)):
        d = os.path.join(MUT, f"{ver}-baseline")
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        for f in ("attest.py", "gate.py"):
            shutil.copy2(os.path.join(src, f), os.path.join(d, f))
        jobs[f"{ver}-baseline"] = d
    meta = {}
    for mid, desc, pairs in MUTANTS:
        for ver in ("base", "head"):
            d, h_new, h_old, diff = build(ver, mid, pairs)
            meta[f"{ver}-{mid}"] = {"mutant": mid, "ver": ver, "desc": desc,
                                    "sha_mutant": h_new, "sha_orig": h_old,
                                    "diff": diff}
            jobs[f"{ver}-{mid}"] = d
    results = {}
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(run_selftest, d): k for k, d in jobs.items()}
        for f in cf.as_completed(futs):
            k = futs[f]
            try:
                results[k] = f.result()
            except Exception as exc:  # noqa: BLE001
                results[k] = {"dir": jobs[k], "exit": "harness-error",
                              "error": f"{type(exc).__name__}: {exc}"}
    summary = {"utc": utc(), "runs": results, "meta": meta}
    with open(os.path.join(REC, "summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)

    for ver in ("base", "head"):
        base = results[f"{ver}-baseline"]
        print(f"== {ver} baseline: exit={base['exit']} cases={base['cases']} "
              f"failures={base['failures']} sha={base['stdout_sha256'][:12]}")
        if base.get("case_rows") is None:
            print("   baseline case rows unparsed; head:", base["stdout_head"])
            continue
        ok = {c["case"]: c["ok"] for c in base["case_rows"]}
        green = [c["case"] for c in base["case_rows"] if c["ok"]]
        print(f"   green cases: {green}")
        for mid, desc, _ in MUTANTS:
            r = results[f"{ver}-{mid}"]
            rows = r.get("case_rows")
            flipped, reason = [], ""
            if rows is None:
                reason = f"unparsed/exit={r['exit']} head={r.get('stdout_head','')[:60]}"
            else:
                for c in rows:
                    if ok.get(c["case"]) and not c["ok"]:
                        flipped.append(c["case"])
            verdict = "KILLED" if flipped else "SURVIVED"
            print(f"   {mid:22s} exit={r['exit']} failures={r['failures']} "
                  f"{verdict} flipped={flipped} {reason}")
    print("summary:", os.path.join(REC, "summary.json"))


if __name__ == "__main__":
    main()
