#!/usr/bin/env python3
"""Reachability probes for the survivors of run_mutants.py.

For each surviving mutant, run the pristine module and the mutated module on the
SAME fixture repo (evaluate() is read-only) and print both (code, receipt). If the
pair differs, the mutant is a real behavioural change that the selftest is blind to
(a coverage hole), not an equivalent mutant.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import hashlib
import time

SEAT = ("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/"
        ".ufo/waves/round-45/w1/R45W1PreflightArms")
SRC = ("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/"
       "tools/round-45/frozen-path-preflight.py")
S = "/fast/scratch/hyaku/kaidoku-r45/R45W1PreflightArms/probes"
REC = os.path.join(SEAT, "receipts")

sys.path.insert(0, os.path.join(SEAT))
from run_mutants import MUTANTS, mutate, sha  # noqa: E402


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


def w(d, rel, text):
    full = os.path.join(d, rel)
    os.makedirs(os.path.dirname(full) or d, exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def commit(d, msg):
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", msg)
    return git(d, "rev-parse", "HEAD").stdout.strip()


def repo(kind):
    d = os.path.join(S, "repo-" + kind + "-" + str(time.time_ns()))
    os.makedirs(d)
    git(d, "init", "-q")
    git(d, "config", "user.email", "probe@selftest")
    git(d, "config", "user.name", "probe")
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    w(d, "frozen/a.txt", "alpha\n")
    w(d, "frozen/b.txt", "beta\n")
    w(d, "other.txt", "other\n")
    f = commit(d, "freeze")
    if kind == "restored":
        w(d, "frozen/a.txt", "tampered\n")
        commit(d, "tamper")
        w(d, "frozen/a.txt", "alpha\n")
        r = commit(d, "restore")
        return d, f, r
    if kind == "nested":
        w(d, "frozen/inner/a.txt", "inner\n")
        f = commit(d, "add nested freeze dir")
        return d, f, f
    if kind == "untracked":
        w(d, "frozen/stray.txt", "stray\n")          # never `git add`
        return d, f, f
    if kind == "dirty-outside-scope":
        w(d, "frozen/b.txt", "uncommitted\n")
        return d, f, f
    if kind == "scoped-out":
        # the commit touches frozen/a.txt but the log scope (--pathspec other.txt)
        # excludes it: only the blob arm can see this change.
        w(d, "frozen/a.txt", "changed\n")
        r = commit(d, "touch a frozen path outside the log scope")
        return d, f, r
    if kind == "clean":
        return d, f, f
    raise SystemExit("unknown kind " + kind)


PROBES = [
    {"id": "m2b", "mutant": "m2", "repo": "restored",
     "args": (["frozen/"], ["frozen"], False, [], True),
     "question": "does removing the restore classifier change the VERDICT, and does it "
                 "change the `restored` receipt field?"},
    {"id": "x1b", "mutant": "x1", "repo": "nested",
     "args": (["frozen"], ["frozen/inner"], False, [], True),
     "question": "does an ANCESTOR pathspec cover a nested frozen dir? pristine refuses, x1 accepts."},
    {"id": "x2b", "mutant": "x2", "repo": "dirty-outside-scope",
     "args": (["frozen/"], ["frozen"], True, ["other.txt"], True),
     "question": "with --dirty-pathspec other.txt, is a dirty frozen file still reported?"},
    {"id": "x3b", "mutant": "x3", "repo": "untracked",
     "args": (["frozen/"], ["frozen"], True, [], True),
     "question": "is an UNTRACKED file under the frozen dir reported as dirty?"},
    {"id": "x4b", "mutant": "x4", "repo": "scoped-out",
     "args": (["other.txt"], ["frozen"], False, [], False),
     "question": "a frozen path changed OUTSIDE the commit-log scope: does the blob arm "
                 "still refuse the revision when --pathspec does not cover --freeze-path?"},
]


def main():
    os.makedirs(S, exist_ok=True)
    os.makedirs(REC, exist_ok=True)
    os.environ["TMPDIR"] = S
    os.environ["HYAKU_SCRATCH"] = S
    with open(SRC, "r", encoding="utf-8") as fh:
        src = fh.read()
    mt = {m["id"]: m for m in MUTANTS}

    # materialise pristine + each needed mutant module once
    mods = {"pristine": os.path.join(S, "pristine.py")}
    shutil.copy2(SRC, mods["pristine"])
    for pid in ("m2", "x1", "x2", "x3", "x4"):
        p = os.path.join(S, pid + ".py")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(mutate(src, mt[pid]))
        mods[pid] = p
    loaded = {k: load(v, "probe_" + k) for k, v in mods.items()}

    out = {"seat": "R45W1PreflightArms", "instrument_sha256": sha(SRC),
           "scratch": S, "probes": []}
    for p in PROBES:
        d, f, r = repo(p["repo"])
        pathspecs, freeze_paths, check_dirty, dirty_ps, req_ps = p["args"]
        row = {"probe": p["id"], "mutant": p["mutant"], "repo_kind": p["repo"],
               "args": {"pathspec": pathspecs, "freeze_path": freeze_paths,
                        "check_dirty": check_dirty, "dirty_pathspec": dirty_ps,
                        "require_pathspec": req_ps},
               "freeze": f, "rev": r, "question": p["question"], "runs": {}}
        for tag in ("pristine", p["mutant"]):
            mod = loaded[tag]
            t0 = utc()
            try:
                code, receipt = mod.evaluate(d, f, r, pathspecs, freeze_paths,
                                             check_dirty, dirty_ps, req_ps)
                err = None
            except Exception as exc:
                code, receipt, err = None, None, "%s: %s" % (type(exc).__name__, exc)
            row["runs"][tag] = {"module": mods[tag], "module_sha256": sha(mods[tag]),
                                "utc": t0, "code": code, "receipt": receipt,
                                "error": err}
        pr, mu = row["runs"]["pristine"], row["runs"][p["mutant"]]
        row["code_differs"] = pr["code"] != mu["code"]
        row["receipt_differs"] = pr["receipt"] != mu["receipt"]
        row["reachable"] = bool(row["code_differs"] or row["receipt_differs"])
        row["delta"] = {
            "code": [pr["code"], mu["code"]],
            "restored": [pr["receipt"].get("restored") if pr["receipt"] else None,
                         mu["receipt"].get("restored") if mu["receipt"] else None],
            "dirty": [pr["receipt"].get("dirty") if pr["receipt"] else None,
                      mu["receipt"].get("dirty") if mu["receipt"] else None],
            "verdict": [pr["receipt"].get("verdict") if pr["receipt"] else None,
                        mu["receipt"].get("verdict") if mu["receipt"] else None],
            "reason": [pr["receipt"].get("reason") if pr["receipt"] else None,
                       mu["receipt"].get("reason") if mu["receipt"] else None],
        }
        out["probes"].append(row)
        with open(os.path.join(REC, p["id"] + ".json"), "w") as fh:
            json.dump(row, fh, indent=1, sort_keys=True)
        shutil.rmtree(d, ignore_errors=True)

    with open(os.path.join(REC, "reachability.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps([{"probe": r["probe"], "reachable": r["reachable"],
                       "delta": r["delta"]} for r in out["probes"]], indent=1))
    shutil.rmtree(S, ignore_errors=True)


if __name__ == "__main__":
    main()
