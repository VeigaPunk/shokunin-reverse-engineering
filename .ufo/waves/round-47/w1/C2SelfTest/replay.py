#!/usr/bin/env python3
"""Replay the C2SelfTest clause-deletion matrix against a pinned record.py.

The source is `git show 1e2c3102:tools/round-47/record.py`
(sha256 c704c3d407325264f8e2d990a8873524b0c5bbbf52d5dcc10ee8df411c9d6fa7); each mutation
is a unified diff in `mutations.json` next to this file.  Every mutation is applied to a
scratch copy only: the lane tree is read-only for this seat.

    python3 replay.py --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
        --scratch /fast/scratch/.../C2SelfTest/replay [--only M03 M23]

For each mutation it prints: id, applied sha256 (must equal `mutated_sha256`), selftest
exit, and the case names that went red.  A mutation with `red=[]` is a clause the selftest
does not guard.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

PIN = "1e2c3102952dc636650095643c1963c833859019"
HERE = os.path.dirname(os.path.abspath(__file__))


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lane", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args(argv)
    spec = json.load(open(os.path.join(HERE, "mutations.json")))
    src = git(args.lane, "show", "%s:tools/round-47/record.py" % PIN).stdout
    got = hashlib.sha256(src.encode()).hexdigest()
    if got != spec["source_sha256"]:
        print(json.dumps({"reason": "source sha256 mismatch", "got": got,
                          "want": spec["source_sha256"]}))
        return 2
    gate = git(args.lane, "show", "%s:tools/round-46/gate.py" % PIN).stdout
    if not gate:
        print(json.dumps({"reason": "gate.py absent at %s" % PIN}))
        return 2
    rows = []
    for mid, mut in sorted(spec["mutations"].items()):
        if args.only and mid not in args.only:
            continue
        root = os.path.join(args.scratch, mid)
        shutil.rmtree(root, ignore_errors=True)
        os.makedirs(os.path.join(root, "tools/round-47"))
        os.makedirs(os.path.join(root, "tools/round-46"))
        path = os.path.join(root, "tools/round-47/record.py")
        open(path, "w").write(src)
        open(os.path.join(root, "tools/round-46/gate.py"), "w").write(gate)
        pr = subprocess.run(["patch", "-p0", "--forward", "--silent", "-i", "-"],
                            input=mut["diff"], text=True, cwd=root, capture_output=True)
        after = hashlib.sha256(open(path, "rb").read()).hexdigest()
        if pr.returncode != 0 or after != mut["mutated_sha256"]:
            rows.append({"id": mid, "error": "patch failed", "rc": pr.returncode,
                         "sha_match": after == mut["mutated_sha256"]})
            continue
        scr = os.path.join(root, "scratch")
        os.makedirs(scr, exist_ok=True)
        env = dict(os.environ, HYAKU_SCRATCH=scr, TMPDIR=scr)
        r = subprocess.run([sys.executable, "-I", "-B", path, "--root", root,
                            "--rev", "HEAD", "--selftest"],
                           capture_output=True, text=True, env=env, cwd=scr)
        m = re.search(r"RECORD_SELFTEST: cases=(\d+) failures=(\d+)", r.stdout)
        red = []
        if m:
            body = json.loads(r.stdout[r.stdout.index("{"):])
            red = [c["case"] for c in body["cases"] if not c["ok"]]
        rows.append({"id": mid, "clause": mut["clause"], "kind": mut["kind"],
                     "exit": r.returncode, "cases": int(m.group(1)) if m else None,
                     "red": red})
    for row in rows:
        if "error" in row:
            print("%s ERROR %s" % (row["id"], row["error"]))
        else:
            print("%s exit=%s cases=%s red=%s  # %s"
                  % (row["id"], row["exit"], row["cases"], row["red"] or "[]", row["clause"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
