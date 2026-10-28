#!/usr/bin/env python3
"""Adjacent probes for seat R46W1RevGateMerge, same receipt discipline.

  m  a tamper commit rewritten away by `git commit --amend` (unstated limit?)
  n  an uncommitted frozen tamper (is the documented `dirty` arm wired?)
  o  a squash merge whose RESOLUTION restores the bytes (purest form of brief (c))
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import time

S = os.environ["HYAKU_SCRATCH"]
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "31820472784284727546808acc31b3ea1e73919b"
FROZEN = ["plans/round-46-claims.md", "tools/round-46/gate.py",
          "tools/round-46/attest.py", "tools/round-46/registry.py",
          "tools/round-46/census.py", "tools/round-46/census.json"]
REC, OUT = [], {}
P = "tools/round-46/gate.py"


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def run(args, cwd=None):
    r = subprocess.run(args, cwd=cwd, capture_output=True)
    REC.append({"cmd": " ".join(args), "cwd": cwd, "exit": r.returncode,
                "stdout_sha256": hashlib.sha256(r.stdout).hexdigest(),
                "stdout": r.stdout.decode("utf-8", "surrogateescape"),
                "stderr": r.stderr.decode("utf-8", "surrogateescape")[:400],
                "utc": utc()})
    return r


def g(D, *a):
    return run(["git", "-C", D, *a])


def write(D, rel, data):
    p = os.path.join(D, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as fh:
        fh.write(data if isinstance(data, bytes) else data.encode())


def read(D, rel):
    with open(os.path.join(D, rel), "rb") as fh:
        return fh.read()


BLOBS = {}


def repo(name):
    D = os.path.join(S, "fx", name)
    if os.path.isdir(D):
        import shutil
        shutil.rmtree(D)
    os.makedirs(D)
    g(D, "init", "-q", "-b", "main")
    for k, v in (("user.email", "rev@gatemerge.invalid"),
                 ("user.name", "R46W1RevGateMerge"), ("commit.gpgsign", "false")):
        g(D, "config", k, v)
    assert os.path.realpath(g(D, "rev-parse", "--show-toplevel")
                            .stdout.decode().strip()) == os.path.realpath(D)
    for rel, data in BLOBS.items():
        write(D, rel, data)
    write(D, "notes.txt", "base\n")
    g(D, "add", "-A")
    g(D, "commit", "-q", "-m", "freeze")
    return D, g(D, "rev-parse", "HEAD").stdout.decode().strip()


def state(D, base, tip, label):
    code, rec = GATE.freeze_state(D, base, tip)
    OUT[label] = {"exit": code, "receipt": {k: rec.get(k) for k in
                 ("reason", "frozen_path_changed", "blob_changed", "touched", "restored")}}
    print(label, "exit", code, OUT[label]["receipt"])


def main():
    global BLOBS, GATE
    for rel in FROZEN:
        BLOBS[rel] = run(["git", "-C", LANE, "show", "%s:%s" % (FREEZE, rel)]).stdout
    spec = importlib.util.spec_from_file_location("g", os.path.join(S, "gate_frozen.py"))
    GATE = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(GATE)

    # m: amend rewrites the tamper away
    D, F = repo("m-amend")
    write(D, P, read(D, P) + b"TAMPER\n")
    g(D, "add", "-A"); g(D, "commit", "-q", "-m", "tamper")
    write(D, P, BLOBS[P])
    g(D, "add", "-A"); g(D, "commit", "-q", "--amend", "--no-edit", "--allow-empty")
    tip = g(D, "rev-parse", "HEAD").stdout.decode().strip()
    g(D, "log", "--oneline", "--format=%h %s", F + ".." + tip)
    OUT["m_amend_history"] = g(D, "log", "--oneline", "--name-status",
                               "--format=%h %s", F + ".." + tip).stdout.decode()
    state(D, F, tip, "m-amend-rewrites-tamper-away")

    # n: uncommitted tamper, tip == freeze
    D, F = repo("n-dirty")
    write(D, P, read(D, P) + b"DIRTY\n")
    OUT["n_git_status"] = g(D, "status", "--porcelain").stdout.decode()
    state(D, F, F, "n-uncommitted-tamper")
    OUT["n_gate_dirty_helper"] = GATE.dirty(D, [P, "plans/round-46-claims.md"])

    # o: squash merge, restore performed in the resolution
    D, F = repo("o-squash-resolution-restore")
    g(D, "checkout", "-q", "-b", "side", F)
    write(D, P, read(D, P) + b"SIDE-EDIT\n")
    write(D, "notes.txt", "base\nside\n")
    g(D, "add", "-A"); g(D, "commit", "-q", "-m", "side: tamper + notes")
    g(D, "checkout", "-q", "main")
    g(D, "merge", "--squash", "side")
    write(D, P, BLOBS[P])                     # the resolution restores the bytes
    g(D, "add", "-A")
    g(D, "commit", "-q", "-m", "squash-merge side, restore frozen bytes")
    tip = g(D, "rev-parse", "HEAD").stdout.decode().strip()
    OUT["o_squash_diff"] = g(D, "show", "--name-status", "--format=%h %s",
                             tip).stdout.decode()
    OUT["o_tree_equal"] = g(D, "diff", "--quiet", F, tip, "--",
                            "plans/round-46-claims.md", "tools/round-46/").returncode
    state(D, F, tip, "o-squash-resolution-restores")

    OUT["receipts"] = REC
    p = os.path.join(S, "extras_receipts.json")
    with open(p, "w") as fh:
        json.dump(OUT, fh, indent=1, sort_keys=True)
    print("wrote", p)


if __name__ == "__main__":
    main()
