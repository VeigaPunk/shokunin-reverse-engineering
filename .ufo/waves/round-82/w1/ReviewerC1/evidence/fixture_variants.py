#!/usr/bin/env python3
"""ReviewerC1 r82: commit forged-state variants into the private fixture repo.

Each variant is its own commit so each gate battery run pins an exact rev.
Writes only inside the scratch fixture; git -C absolute; toplevel asserted.
"""
import copy
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SCRATCH = "/fast/scratch/hyaku/kaidoku-r82/ReviewerC1"
REPO = SCRATCH + "/fixture/fixture-repo"
REV = "eb227c4694e16cb8fae74df0eea2f07643b46124"
LANDING = ".ufo/waves/round-81/l1/scores/c2-at-landing.json"
FORGED_UNDER = ".ufo/waves/round-81/w1/ExecCounter/undersized-pristine.json"
FORGED_DIRTY = ".ufo/waves/round-81/w1/ExecCounter/dirty-pristine-summary.json"


def lane_bytes(path):
    return subprocess.check_output(["git", "-C", LANE, "show", f"{REV}:{path}"])


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], check=True,
                          capture_output=True, text=True).stdout


def landing():
    return copy.deepcopy(json.loads(lane_bytes(LANDING).decode("utf-8")))


def idx(cases, name):
    return next(i for i, r in enumerate(cases)
                if isinstance(r, dict) and r.get("case") == name)


def write_commit(path, data: bytes, msg):
    dst = os.path.join(REPO, path)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    top = git("rev-parse", "--show-toplevel").strip()
    assert top == os.path.realpath(REPO), f"toplevel mismatch: {top}"
    git("add", "-A")
    git("-c", "user.email=reviewer-c1@scratch.invalid",
        "-c", "user.name=ReviewerC1", "commit", "-qm", msg)
    head = git("rev-parse", "HEAD").strip()
    return {"commit": head, "path": path, "sha256": hashlib.sha256(data).hexdigest()}


def main():
    variant = sys.argv[1]
    if variant == "ce1-bool-int":
        r = landing()
        r["pristine"]["exit"] = False
        r["pristine"]["summary"] = [11, False]
        r["survivors"] = False
        r["mutants"] = True
        out = write_commit(FORGED_DIRTY,
                           json.dumps(r, indent=1).encode() + b"\n",
                           "CE1: bool-for-int in summary/exit/survivors/mutants")
    elif variant == "ce3-dup-original":
        r = landing()
        pc = r["pristine"]["cases"]
        pc[idx(pc, "record-fixture-committed-duplicate")] = dict(
            pc[idx(pc, "green-validate-consistent")])
        out = write_commit(FORGED_UNDER,
                           json.dumps(r, indent=1).encode() + b"\n",
                           "CE3: duplicated original row, 10 distinct of 11")
    elif variant == "ce5-killed-field":
        r = landing()
        r["killed"] = 0
        r["ok"] = False
        out = write_commit(FORGED_UNDER,
                           json.dumps(r, indent=1).encode() + b"\n",
                           "CE5: recorded killed 0 / ok false, data otherwise genuine")
    elif variant == "malformed":
        out = write_commit(FORGED_UNDER, b'{ "pristine": [ truncated',
                           "malformed JSON at forged-under path")
    else:
        raise SystemExit(f"unknown variant {variant}")
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    sys.exit(main())
