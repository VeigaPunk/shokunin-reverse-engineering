#!/usr/bin/env python3
"""Fixture attacks on the invocation shape the seat's attack-2 command used.

Imports the byte-frozen interpreter from this scratch dir (sha256 633ebc05...),
builds private repos under the seat scratch dir, and calls evaluate() directly.
Read-only w.r.t. the lane; every fixture lives under $S/fx.
"""
import importlib.util
import json
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r45/R45W2PreflightReal"
spec = importlib.util.spec_from_file_location("pf", os.path.join(S, "frozen-preflight.py"))
pf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pf)


def git(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


def write(d, path, text):
    full = os.path.join(d, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def commit(d, msg):
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", msg)
    r = git(d, "rev-parse", "HEAD")
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def mk(name):
    d = os.path.join(S, "fx", name)
    subprocess.run(["rm", "-rf", d], check=True)
    os.makedirs(d)
    git(d, "init", "-q")
    git(d, "config", "user.email", "fx@seat")
    git(d, "config", "user.name", "fx seat")
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    write(d, "frozen/a.txt", "alpha\n")
    write(d, "frozen/sub/b.txt", "beta\n")
    write(d, "plan/claims.md", "frozen claims\n")
    write(d, "other.txt", "other\n")
    return d


out = []

# F1: a commit that modifies a frozen FILE the caller did not declare.
d = mk("f1")
F = commit(d, "freeze")
write(d, "plan/claims.md", "claims edited after freeze\n")
R = commit(d, "edit claims")
a = pf.evaluate(d, F, R, ["frozen/"], ["frozen"], False, [], True)
b = pf.evaluate(d, F, R, ["frozen/", "plan/claims.md"],
                ["frozen", "plan/claims.md"], False, [], True)
out.append({"fixture": "F1-frozen-file-outside-declared-pathspec",
            "commit": R,
            "under_declared": {"code": a[0], "touched": a[1]["touched"],
                               "blob_changed": a[1]["blob_changed"],
                               "verdict": a[1]["verdict"]},
            "fully_declared": {"code": b[0], "touched": b[1]["touched"],
                               "blob_changed": b[1]["blob_changed"],
                               "verdict": b[1]["verdict"]}})

# F2: touch then restore a frozen file the caller did not declare (history arm).
d = mk("f2")
F = commit(d, "freeze")
write(d, "plan/claims.md", "tampered\n")
commit(d, "tamper")
write(d, "plan/claims.md", "frozen claims\n")
R = commit(d, "restore")
a = pf.evaluate(d, F, R, ["frozen/"], ["frozen"], False, [], True)
b = pf.evaluate(d, F, R, ["frozen/", "plan/claims.md"],
                ["frozen", "plan/claims.md"], False, [], True)
out.append({"fixture": "F2-touch-restore-outside-declared-pathspec",
            "under_declared": {"code": a[0], "restored": a[1]["restored"],
                               "blob_changed": a[1]["blob_changed"],
                               "verdict": a[1]["verdict"]},
            "fully_declared": {"code": b[0], "restored": b[1]["restored"],
                               "blob_changed": b[1]["blob_changed"],
                               "verdict": b[1]["verdict"]}})

# F3: --dirty-pathspec replaces the dirty scope (the block-22 stated false-clean).
d = mk("f3")
F = commit(d, "freeze")
write(d, "frozen/a.txt", "uncommitted\n")
narrow = pf.evaluate(d, F, F, ["frozen/"], ["frozen"], True, ["other/"], True)
full = pf.evaluate(d, F, F, ["frozen/"], ["frozen"], True, [], True)
out.append({"fixture": "F3-dirty-pathspec-replaces-scope",
            "narrowed": {"code": narrow[0], "dirty": narrow[1]["dirty"],
                         "verdict": narrow[1]["verdict"]},
            "unmodified_scope": {"code": full[0], "dirty": full[1]["dirty"],
                                 "verdict": full[1]["verdict"]}})

print(json.dumps(out, indent=1, sort_keys=True))
