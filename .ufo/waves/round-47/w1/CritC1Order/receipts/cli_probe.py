#!/usr/bin/env python3
"""Full-CLI clause-7 falsification: exact.py exits 0 on a tampered frozen range.

Three one-history fixture repos, identical except for `tools/round-46/gate.py` and the
merge-only add/delete of `tools/round-47/decoy.txt`:
  R1 genuine gate.py, tamper present   -> expected frozen_path_changed (exit 2)
  R2 F2 gate.py (literal intact, no --format=), tamper present -> expected exit 0
  R3 F2 gate.py, no tamper             -> expected exit 0 (the forgery alone is not red)
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import datetime

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
import exact  # noqa: E402

SCRATCH = os.environ["HYAKU_SCRATCH"]
CLAIMS = open(os.path.join(LANE, "plans", "round-47-claims.md")).read()
EXACT_SRC = open(os.path.join(LANE, "tools", "round-47", "exact.py")).read()
GATE_SRC = open(os.path.join(LANE, "tools", "round-46", "gate.py")).read()
FORGED = GATE_SRC.replace('"--name-status", "-z",\n            "--format=",',
                          '"--name-status", "-z",')


def g(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True,
                          text=True, check=True)


def commit(root, msg):
    g(root, "add", "-A")
    g(root, "commit", "-qm", msg)
    return g(root, "rev-parse", "HEAD").stdout.strip()


def write(root, p, text):
    full = os.path.join(root, p)
    os.makedirs(os.path.dirname(full) or root, exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def build(root, gate_text, tamper, freeze_gate=None):
    g(root, "init", "-q")
    g(root, "config", "user.email", "fx@round47")
    g(root, "config", "user.name", "round47 fixture")
    top = g(root, "rev-parse", "--show-toplevel").stdout.strip()
    assert top == root, (top, root)
    write(root, "SKILL.md", exact.skill_text(exact.good_block(
        pin=hashlib.sha256(EXACT_SRC.encode()).hexdigest())))
    write(root, "plans/round-47-claims.md", CLAIMS)
    write(root, "tools/round-47/exact.py", EXACT_SRC)
    write(root, "tools/round-46/gate.py", freeze_gate or gate_text)
    write(root, "corpus/lessons/round-46.md", "lesson line\n" * 240)
    write(root, "tools/round-47/keep.py", "# kept\n")
    freeze = commit(root, "freeze")
    default = g(root, "symbolic-ref", "--short", "HEAD").stdout.strip()
    if freeze_gate is not None:
        write(root, "tools/round-46/gate.py", gate_text)
        commit(root, "landing rewrites gate.py only")

    write(root, "note.txt", "1\n")
    commit(root, "ordinary work")
    if tamper:
        g(root, "checkout", "-q", "-b", "side1")
        write(root, "side1.txt", "1\n")
        commit(root, "side1")
        g(root, "checkout", "-q", default)
        write(root, "main1.txt", "1\n")
        commit(root, "main1")
        r = subprocess.run(["git", "-C", root, "merge", "--no-ff", "--no-commit", "side1"],
                           capture_output=True)
        assert r.returncode == 0, r.stderr
        write(root, "tools/round-47/decoy.txt", "decoy\n")
        g(root, "add", "-A")
        g(root, "commit", "-qm", "merge side1 (adds frozen decoy)")
        g(root, "checkout", "-q", "-b", "side2")
        write(root, "side2.txt", "1\n")
        commit(root, "side2")
        g(root, "checkout", "-q", default)
        write(root, "main2.txt", "1\n")
        commit(root, "main2")
        r = subprocess.run(["git", "-C", root, "merge", "--no-ff", "--no-commit", "side2"],
                           capture_output=True)
        assert r.returncode == 0, r.stderr
        g(root, "rm", "-q", "tools/round-47/decoy.txt")
        g(root, "commit", "-qm", "merge side2 (deletes frozen decoy)")
    rev = g(root, "rev-parse", "HEAD").stdout.strip()
    return freeze, rev


def main():
    root, err = exact.gate.scratch("kaidoku-r47-cli-critc1-")
    assert not err, err
    out = {"exact_py_sha256": hashlib.sha256(EXACT_SRC.encode()).hexdigest(),
           "gate_py_sha256": hashlib.sha256(GATE_SRC.encode()).hexdigest(), "cases": []}
    try:
        for name, gate_text, tamper, *rest in (
                ("R1-genuine-tampered", GATE_SRC, True),
                ("R2-forged-tampered", FORGED, True),
                ("R3-forged-clean", FORGED, False),
                ("R4-forged-at-rev-only", FORGED, True, GATE_SRC)):
            d = tempfile.mkdtemp(dir=root, prefix=name[:2] + "-")
            freeze, rev = build(d, gate_text, tamper, rest[0] if rest else None)
            cmd = ["python3", "-I", "-B", "tools/round-47/exact.py",
                   "--root", d, "--freeze", freeze, "--rev", rev]
            t0 = datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")
            r = subprocess.run(cmd, cwd=d, capture_output=True, text=True)
            out["cases"].append({"case": name, "cwd": d, "cmd": cmd,
                        "freeze": freeze, "rev": rev,
                        "exit": r.returncode,
                        "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
                        "stderr_tail": r.stderr[-400:],
                        "stdout": r.stdout[:4000],
                        "utc": t0})
    finally:
        pass
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
