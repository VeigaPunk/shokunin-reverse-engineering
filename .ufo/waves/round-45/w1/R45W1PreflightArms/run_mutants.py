#!/usr/bin/env python3
"""Round-45 wave-1 arm test: mutation-test tools/round-45/frozen-path-preflight.py.

Read-only on the lane tree. Every mutant is applied to a private COPY under
/fast/scratch; the frozen original is only ever read and hashed.

detector = the instrument's own `--selftest` (the bounded behavioral detector).
A mutant is KILLED iff at least one named selftest case flips expect -> got.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

SEAT = ("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/"
        ".ufo/waves/round-45/w1/R45W1PreflightArms")
SRC = ("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/"
       "tools/round-45/frozen-path-preflight.py")
S = "/fast/scratch/hyaku/kaidoku-r45/R45W1PreflightArms"
REC = os.path.join(SEAT, "receipts")

# ---------------------------------------------------------------- mutant set

DIRTY_BLOCK = '''    dirty = []
    if check_dirty:
        scope_paths = dirty_pathspecs or pathspecs
        dscope = ["--"] + scope_paths if scope_paths else []
        st = git(root, "status", "--porcelain", "-z", *dscope)
        if st.returncode != 0:
            return 2, {"reason": "git status failed"}
        dirty = [e for e in st.stdout.split("\\x00") if e.strip()]
'''

LOG_ARM = '''    scope = ["--"] + pathspecs if pathspecs else []
    log = git(root, "log", "-m", "--diff-merges=first-parent", "--name-status",
              "--format=%x00%H", f"{base}..{tip}", *scope)
    if log.returncode != 0:
        return 2, {"reason": "git log failed"}

    touched, commit = [], None
    for line in log.stdout.splitlines():
        if line.startswith("\\x00"):
            commit = line[1:].strip()
            continue
        parts = line.split("\\t")
        if len(parts) < 2 or not commit:
            continue
        status = parts[0]
        if status[:1] in {"M", "D", "R", "T", "U", "A", "C"}:
            for path in parts[1:]:
                touched.append({"commit": commit, "status": status, "path": path})
'''

PATHSPEC_ARM = '''    if require_pathspec:
        missing = [fp for fp in freeze_paths
                   if tree_at(root, base, fp) and not covers(pathspecs, fp)]
        if missing:
            return 2, {"reason": "pathspec_required", "uncovered_frozen_dirs": missing}
'''

MUTANTS = [
    {
        "id": "m1",
        "arm": "dirty (--check-dirty)",
        "what": "delete the --check-dirty block (arm removed; `dirty` stays [])",
        "old": DIRTY_BLOCK,
        "new": "    dirty = []\n",
    },
    {
        "id": "m2",
        "arm": "restored",
        "what": "make the `restored` list never populate (drop the append branch)",
        "old": '        elif any(t["path"] == path for t in touched):\n'
               '            restored.append(path)\n',
        "new": "        # mutant m2: restore classifier never fires\n",
    },
    {
        "id": "m3",
        "arm": "pathspec (--require-pathspec)",
        "what": "--require-pathspec returns 0 without checking anything",
        "old": PATHSPEC_ARM,
        "new": '    if require_pathspec:\n'
               '        return 0, {"reason": "pathspec_required", "checked": False,\n'
               '                    "pathspec": pathspecs}\n',
    },
    {
        "id": "m4",
        "arm": "commit (git log --name-status)",
        "what": "drop the commit-log arm, keep only the blob comparison (touched == [])",
        "old": LOG_ARM,
        "new": "    # mutant m4: commit-log arm dropped; blob comparison only\n"
               "    touched = []\n",
    },
    # ---- exploratory probes beyond the assigned four (holes, not arms) ----
    {
        "id": "x1",
        "arm": "covers() direction [exploratory]",
        "what": "covers() accepts an ANCESTOR pathspec (fp.startswith(p)) instead of a descendant",
        "old": '    return any(p.rstrip("/") == fp or p.rstrip("/").startswith(fp + "/") for p in pathspecs)\n',
        "new": '    return any(p.rstrip("/") == fp or fp.startswith(p.rstrip("/") + "/") for p in pathspecs)\n',
    },
    {
        "id": "x2",
        "arm": "--dirty-pathspec narrowing [exploratory]",
        "what": "ignore --dirty-pathspec: scope the dirty arm by --pathspec only",
        "old": "        scope_paths = dirty_pathspecs or pathspecs\n",
        "new": "        scope_paths = pathspecs  # mutant x2: --dirty-pathspec ignored\n",
    },
    {
        "id": "x3",
        "arm": "dirty arm untracked entries [exploratory]",
        "what": "dirty arm ignores `??` (untracked) entries",
        "old": '        dirty = [e for e in st.stdout.split("\\x00") if e.strip()]\n',
        "new": '        dirty = [e for e in st.stdout.split("\\x00")\n'
               '                 if e.strip() and not e.startswith("??")]\n',
    },
    {
        "id": "x4",
        "arm": "blob [exploratory]",
        "what": "blob arm records nothing (blob_changed stays [])",
        "old": "            blob_changed.append(path)\n",
        "new": "            pass  # mutant x4: blob arm records nothing\n",
    },
]

# ---------------------------------------------------------------- helpers


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def run_selftest(pyfile, tag):
    """Run `python3 -I -B <pyfile> --selftest` with scratch-only temp dirs."""
    tmp = os.path.join(S, "tmp", tag)
    os.makedirs(tmp, exist_ok=True)
    env = dict(os.environ)
    env["TMPDIR"] = tmp
    env["HYAKU_SCRATCH"] = tmp
    env.pop("HYAKU_SCRATCH_PATH", None)
    cmd = [sys.executable, "-I", "-B", pyfile, "--selftest"]
    t0 = utc()
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=tmp)
    t1 = utc()
    cases, summary = [], None
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "selftest" in obj:
            cases.append(obj)
    for line in proc.stdout.splitlines():
        if line.startswith("PREFLIGHT_SELFTEST:"):
            summary = line.strip()
    red = [c["selftest"] for c in cases if not c["ok"]]
    rec = {
        "tag": tag,
        "instrument_sha256": sha(pyfile),
        "command": "TMPDIR=%s HYAKU_SCRATCH=%s %s" % (tmp, tmp, " ".join(cmd)),
        "started_utc": t0,
        "finished_utc": t1,
        "exit": proc.returncode,
        "stdout_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest(),
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "summary": summary,
        "cases": cases,
        "red_cases": red,
    }
    if summary:
        # PREFLIGHT_SELFTEST: cases=11 failures=0
        parts = dict(p.split("=") for p in summary.split(":", 1)[1].split())
        rec["cases_n"] = int(parts["cases"])
        rec["failures_n"] = int(parts["failures"])
    shutil.rmtree(tmp, ignore_errors=True)
    return rec


def mutate(src_text, m):
    if src_text.count(m["old"]) != 1:
        raise SystemExit("mutant %s: anchor count %d != 1"
                         % (m["id"], src_text.count(m["old"])))
    out = src_text.replace(m["old"], m["new"])
    if out == src_text:
        raise SystemExit("mutant %s: no-op" % m["id"])
    return out


def main():
    os.makedirs(REC, exist_ok=True)
    os.makedirs(S, exist_ok=True)
    pristine_sha = sha(SRC)
    with open(SRC, "r", encoding="utf-8") as fh:
        src = fh.read()

    results = {"seat": "R45W1PreflightArms", "instrument": SRC,
               "instrument_sha256_at_freeze_arg": "633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b",
               "instrument_sha256_observed": pristine_sha,
               "scratch": S, "runs": [], "verdicts": []}

    # 1. pristine copy + baseline (twice, as the restored-bytes control)
    pdir = os.path.join(S, "pristine")
    shutil.rmtree(pdir, ignore_errors=True)
    os.makedirs(pdir)
    pcopy = os.path.join(pdir, "frozen-path-preflight.py")
    shutil.copy2(SRC, pcopy)
    assert sha(pcopy) == pristine_sha

    base1 = run_selftest(pcopy, "baseline-1")
    results["runs"].append(base1)
    with open(os.path.join(REC, "baseline-1.json"), "w") as fh:
        json.dump(base1, fh, indent=1, sort_keys=True)

    expected = {c["selftest"]: c["expect"] for c in base1["cases"]}
    baseline_green = base1["exit"] == 0 and base1.get("failures_n") == 0

    # 2. mutants, each in its own copy of the instrument
    for m in MUTANTS:
        mdir = os.path.join(S, m["id"])
        shutil.rmtree(mdir, ignore_errors=True)
        os.makedirs(mdir)
        mfile = os.path.join(mdir, "frozen-path-preflight.py")
        mutated = mutate(src, m)
        with open(mfile, "w", encoding="utf-8") as fh:
            fh.write(mutated)
        rec = run_selftest(mfile, m["id"])
        rec["mutant"] = m["id"]
        rec["arm"] = m["arm"]
        rec["what"] = m["what"]
        rec["mutated_sha256"] = sha(mfile)
        flips = []
        got = {c["selftest"]: c["got"] for c in rec["cases"]}
        for name, exp in expected.items():
            if name in got and got[name] != exp:
                flips.append({"case": name, "expect": exp, "got": got[name]})
        rec["flips"] = flips
        rec["case_count_matches_baseline"] = (len(rec["cases"]) == len(expected))
        rec["killed"] = bool(flips) and baseline_green
        rec["verdict"] = ("killed" if rec["killed"]
                          else "survived" if baseline_green
                          else "inconclusive-baseline-red")
        results["runs"].append(rec)
        results["verdicts"].append({"mutant": m["id"], "arm": m["arm"],
                                    "verdict": rec["verdict"],
                                    "red_cases": [f["case"] for f in flips],
                                    "exit": rec["exit"],
                                    "summary": rec["summary"]})
        with open(os.path.join(REC, m["id"] + ".json"), "w") as fh:
            json.dump(rec, fh, indent=1, sort_keys=True)
        shutil.rmtree(mdir, ignore_errors=True)

    # 3. restored-bytes control: pristine bytes again, after all mutants
    base2 = run_selftest(pcopy, "baseline-2-restored")
    results["runs"].append(base2)
    with open(os.path.join(REC, "baseline-2-restored.json"), "w") as fh:
        json.dump(base2, fh, indent=1, sort_keys=True)

    def shape(r):
        return (r["exit"], r.get("cases_n"), r.get("failures_n"),
                sorted(r["red_cases"]))

    results["restored_bytes"] = {
        "sha256_before": base1["instrument_sha256"],
        "sha256_after": base2["instrument_sha256"],
        "bytes_identical": base1["instrument_sha256"] == base2["instrument_sha256"],
        "stdout_sha256_before": base1["stdout_sha256"],
        "stdout_sha256_after": base2["stdout_sha256"],
        "stdout_bit_identical": base1["stdout_sha256"] == base2["stdout_sha256"],
        "behavioral_shape_before": shape(base1),
        "behavioral_shape_after": shape(base2),
        "behavioral_shape_identical": shape(base1) == shape(base2),
        "note": ("stdout carries fixture commit SHAs, which are not reproducible; "
                 "determinism is asserted on exit/cases/failures/red-set"),
    }
    results["instrument_sha256_after_all_runs"] = sha(SRC)
    results["instrument_untouched"] = results["instrument_sha256_after_all_runs"] == pristine_sha
    with open(os.path.join(REC, "mutation-matrix.json"), "w") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    shutil.rmtree(S, ignore_errors=True)
    print(json.dumps({"verdicts": results["verdicts"],
                      "baseline": base1["summary"],
                      "restored": results["restored_bytes"]["behavioral_shape_identical"],
                      "instrument_untouched": results["instrument_untouched"]},
                     indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
