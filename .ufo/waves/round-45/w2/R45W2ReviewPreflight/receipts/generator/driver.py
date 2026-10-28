#!/usr/bin/env python3
"""R45W2ReviewPreflight: adversarial fixtures against frozen-path-preflight v2."""
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r45/R45W2ReviewPreflight"
GATE = os.path.join(S, "preflight.py")
OUT = os.path.join(S, "receipts")
os.makedirs(OUT, exist_ok=True)
os.environ["TMPDIR"] = S
os.environ["HYAKU_SCRATCH"] = S


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def run(argv, cwd):
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def git(d, *args, check=False):
    code, out, err = run(["git", "-C", d, *args], S)
    if check and code != 0:
        raise RuntimeError("git %s failed: %s %s" % (" ".join(args), out, err))
    return code, out, err


def fixture(name):
    d = os.path.join(S, "fx", name)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    git(d, "init", "-q", check=True)
    git(d, "config", "user.email", "rev@r45", check=True)
    git(d, "config", "user.name", "rev r45", check=True)
    git(d, "config", "commit.gpgsign", "false", check=True)
    code, top, _ = git(d, "rev-parse", "--show-toplevel")
    assert top.strip() == d, (top, d)
    return d


def write(d, rel, text):
    full = os.path.join(d, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def commit(d, msg):
    git(d, "add", "-A", check=True)
    git(d, "commit", "-q", "-m", msg, check=True)
    return git(d, "rev-parse", "HEAD")[1].strip()


def gate(d, freeze, rev, pathspecs=("frozen/",), freeze_paths=("frozen",),
         check_dirty=False, dirty_pathspecs=(), require_pathspec=True):
    argv = [sys.executable, "-I", "-B", GATE, "--root", d,
            "--freeze", freeze, "--rev", rev]
    for ps in pathspecs:
        argv += ["--pathspec", ps]
    for fp in freeze_paths:
        argv += ["--freeze-path", fp]
    for dp in dirty_pathspecs:
        argv += ["--dirty-pathspec", dp]
    if check_dirty:
        argv.append("--check-dirty")
    if require_pathspec:
        argv.append("--require-pathspec")
    code, out, err = run(argv, S)
    try:
        body = json.loads(out.strip().splitlines()[-1])
    except Exception:
        body = {"unparsed": out, "stderr": err}
    rec = {
        "case": os.path.basename(d),
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "argv": argv,
        "exit": code,
        "stdout_sha256": sha(out),
        "stderr_sha256": sha(err),
        "stdout_head": out[:4000],
        "receipt": body,
    }
    with open(os.path.join(OUT, rec["case"] + ".json"), "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
    print(json.dumps({"case": rec["case"], "exit": code,
                      "stdout_sha256": rec["stdout_sha256"],
                      "verdict": body.get("verdict"),
                      "reason": body.get("reason"),
                      "touched": len(body.get("touched", [])) if isinstance(body.get("touched"), list) else body.get("touched"),
                      "blob_changed": body.get("blob_changed"),
                      "restored": body.get("restored"),
                      "dirty": body.get("dirty"),
                      "uncovered": body.get("uncovered_frozen_dirs")}, sort_keys=True))
    return rec


def raw(name, d, *args):
    code, out, err = run(["git", "-C", d, *args], S)
    rec = {"case": name, "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "argv": ["git", "-C", d, *args], "exit": code,
           "stdout_sha256": sha(out), "stdout": out, "stderr": err}
    with open(os.path.join(OUT, name + ".json"), "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
    print(json.dumps({"raw": name, "exit": code, "sha": sha(out)}, sort_keys=True))
    return out
