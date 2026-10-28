#!/usr/bin/env python3
"""Adversarial driver for tools/round-45/frozen-path-preflight.py (copy = ./gate.py).

Every fixture is its own repo under $S/fx/<case>; every gate call names --root <fixture>.
Records: command, exit, stdout sha256, UTC.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

S = os.environ["S"]
FX = os.path.join(S, "fx")
GATE = os.path.join(S, "gate.py")
RESULTS = []


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sh(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def g(root, *args):
    return sh(["git", "-C", root, *args])


def newrepo(name, files=None):
    d = os.path.join(FX, name)
    if os.path.exists(d):
        sh(["rm", "-rf", d])
    os.makedirs(d)
    g(d, "init", "-q", "-b", "main")
    g(d, "config", "user.email", "fx@preflight")
    g(d, "config", "user.name", "fx")
    for p, t in (files or {}).items():
        wr(d, p, t)
    return d


def wr(root, path, text, binary=False):
    full = os.path.join(root, path)
    os.makedirs(os.path.dirname(full) or root, exist_ok=True)
    with open(full, "wb" if binary else "w") as fh:
        fh.write(text)


def commit(root, msg):
    g(root, "add", "-A")
    r = g(root, "commit", "-q", "-m", msg)
    assert r.returncode == 0, (msg, r.stderr)
    return g(root, "rev-parse", "HEAD").stdout.strip()


def assert_toplevel(root):
    r = g(root, "rev-parse", "--show-toplevel")
    assert r.stdout.strip() == root, (r.stdout, root)


def gate(case, args, note):
    cmd = ["python3", "-I", "-B", GATE, *args]
    env = dict(os.environ)
    env["HYAKU_SCRATCH"] = S
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    out = r.stdout
    rec = {
        "case": case,
        "note": note,
        "argv": args,
        "cmd": " ".join(cmd),
        "exit": r.returncode,
        "stdout_sha256": hashlib.sha256(out.encode()).hexdigest(),
        "stdout": out.strip(),
        "stderr": r.stderr.strip(),
        "utc": utc(),
    }
    RESULTS.append(rec)
    print(json.dumps(rec, sort_keys=True))
    return rec


def verdict(rec):
    try:
        return json.loads(rec["stdout"])["verdict"]
    except Exception:
        return "?"
