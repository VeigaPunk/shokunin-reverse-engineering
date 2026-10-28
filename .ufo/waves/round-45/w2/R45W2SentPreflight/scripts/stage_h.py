#!/usr/bin/env python3
"""Follow-ups 3: does the one-word --no-replace-objects remediation close g2 without
regressing the selftest; is the blob arm alone (file freeze, no directory) also
replace-blind; and does a graft break the ancestor guard (safe 2)?"""
import hashlib
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.environ["S"])
from run import RESULTS, assert_toplevel, commit, g, newrepo, utc, wr

S = os.environ["S"]
GATE = os.path.join(S, "gate.py")
GATE_FIX = os.path.join(S, "gate-noreplace.py")


def run_gate(case, gatepath, args, note):
    cmd = ["python3", "-I", "-B", gatepath, *args]
    env = dict(os.environ)
    env["HYAKU_SCRATCH"] = S
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    rec = {"case": case, "note": note, "cmd": " ".join(cmd), "exit": r.returncode,
           "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
           "stdout": r.stdout.strip(), "stderr": r.stderr.strip(), "utc": utc()}
    RESULTS.append(rec)
    print(json.dumps({k: rec[k] for k in ("case", "exit", "note")}))
    return rec


def h0_selftest_fix():
    cmd = ["python3", "-I", "-B", GATE_FIX, "--selftest"]
    env = dict(os.environ)
    env["HYAKU_SCRATCH"] = S
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    rec = {"case": "h0-selftest-patched", "cmd": " ".join(cmd), "exit": r.returncode,
           "stdout_tail": r.stdout.strip().splitlines()[-1],
           "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(), "utc": utc()}
    RESULTS.append(rec)
    print(json.dumps(rec))
    return rec


def h1_fix_on_g2():
    d = os.path.join(S, "fx", "g2")
    f = g(d, "rev-list", "--max-parents=0", "HEAD").stdout.strip()
    r = g(d, "rev-parse", "HEAD").stdout.strip()
    return run_gate("h1-fix-on-replace-fixture", GATE_FIX,
                    ["--root", d, "--freeze", f, "--rev", r,
                     "--pathspec", "tools/round-45/", "--freeze-path", "tools/round-45",
                     "--require-pathspec"],
                    "patched gate on the replace-ref fixture; expect 1")


def h2_file_freeze_replace():
    """Blob arm alone: a FILE freeze (no directory entry to fall back on)."""
    d = newrepo("h2", {"plans/claims.md": "frozen v1\n", "other.txt": "o\n"})
    assert_toplevel(d)
    f = commit(d, "freeze")
    ftree = g(d, "rev-parse", f + "^{tree}").stdout.strip()
    wr(d, "plans/claims.md", "CHANGED\n")
    r = commit(d, "touch frozen file")
    fake = g(d, "commit-tree", ftree, "-p", f, "-m", "looks clean").stdout.strip()
    rep = g(d, "replace", r, fake)
    rec = run_gate("h2-file-freeze-replace", GATE,
                   ["--root", d, "--freeze", f, "--rev", r,
                    "--pathspec", "plans/claims.md",
                    "--freeze-path", "plans/claims.md"],
                   "file freeze + replace ref, unpatched gate; expect 1, watch for 0")
    rec["replace_rc"] = rep.returncode
    rec["real_blob"] = g(d, "rev-parse", "--no-replace-objects" and r + ":plans/claims.md"
                         ).stdout.strip()
    fixed = run_gate("h2b-file-freeze-replace-fixed", GATE_FIX,
                     ["--root", d, "--freeze", f, "--rev", r,
                      "--pathspec", "plans/claims.md",
                      "--freeze-path", "plans/claims.md"],
                     "same fixture, patched gate; expect 1")
    fixed["replace_rc"] = rep.returncode
    return rec


def h3_graft_root():
    """Graft the tip to be a root commit: the ancestor guard must refuse (2)."""
    d = newrepo("h3", {"frozen/a.txt": "alpha\n", "other.txt": "o\n"})
    assert_toplevel(d)
    f = commit(d, "freeze")
    wr(d, "frozen/a.txt", "CHANGED\n")
    r = commit(d, "touch frozen")
    with open(os.path.join(d, ".git/info/grafts"), "w") as fh:
        fh.write("%s\n" % r)
    return run_gate("h3-graft-root", GATE,
                    ["--root", d, "--freeze", f, "--rev", r, "--pathspec", "frozen/",
                     "--freeze-path", "frozen", "--require-pathspec"],
                    "graft makes REV a root; expect 2")


def h4_graft_reparent():
    """Graft the tip onto an unrelated root commit carrying the freeze tree."""
    d = newrepo("h4", {"frozen/a.txt": "alpha\n", "other.txt": "o\n"})
    assert_toplevel(d)
    f = commit(d, "freeze")
    ftree = g(d, "rev-parse", f + "^{tree}").stdout.strip()
    wr(d, "frozen/a.txt", "CHANGED\n")
    r = commit(d, "touch frozen")
    fake = g(d, "commit-tree", ftree, "-m", "unrelated clean root").stdout.strip()
    with open(os.path.join(d, ".git/info/grafts"), "w") as fh:
        fh.write("%s %s\n" % (r, fake))
    rec = run_gate("h4-graft-reparent", GATE,
                   ["--root", d, "--freeze", f, "--rev", r, "--pathspec", "frozen/",
                    "--freeze-path", "frozen", "--require-pathspec"],
                   "graft reparents REV onto a clean unrelated root; expect 2")
    rec["graft_log"] = g(d, "log", "--name-status", "--format=%h", f"{f}..{r}", "--",
                         "frozen/").stdout.strip()
    return rec


def h5_fix_on_lane():
    return run_gate("h5-fix-lane-head", GATE_FIX,
                    ["--root", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
                     "--freeze", "f762b7273e3f6ca3c710bb37d5de92a4a4417aec",
                     "--rev", "HEAD", "--pathspec", "tools/round-45/",
                     "--freeze-path", "tools/round-45",
                     "--pathspec", "plans/round-45-claims.md",
                     "--freeze-path", "plans/round-45-claims.md",
                     "--require-pathspec"],
                    "patched gate on the real lane; expect 0 (no regression)")


for fn in (h0_selftest_fix, h1_fix_on_g2, h2_file_freeze_replace, h3_graft_root,
           h4_graft_reparent, h5_fix_on_lane):
    try:
        fn()
    except Exception as exc:
        print(json.dumps({"case": fn.__name__, "driver_error": f"{type(exc).__name__}: {exc}"}))

with open(os.path.join(S, "results-h.json"), "w") as fh:
    json.dump(RESULTS, fh, indent=1)
for r in RESULTS:
    print(r["case"], "exit=%s" % r["exit"], r.get("stdout_tail", "")[:120])
