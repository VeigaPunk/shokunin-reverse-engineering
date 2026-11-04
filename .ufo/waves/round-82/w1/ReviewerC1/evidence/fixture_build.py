#!/usr/bin/env python3
"""ReviewerC1 r82: build private fixture repo with faithful pins + retained receipts.

Bytes for counter/binder/receipts come from `git -C LANE show HEAD:<path>` so the
fixture is byte-faithful to the measured revision eb227c4694e16cb8fae74df0eea2f07643b46124.
No lane file is written; all writes are inside the scratch fixture dir.
"""
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SCRATCH = "/fast/scratch/hyaku/kaidoku-r82/ReviewerC1"
REPO = SCRATCH + "/fixture/fixture-repo"
REV = "eb227c4694e16cb8fae74df0eea2f07643b46124"

COUNTER = "tools/round-81/record-integration.py"
BINDER = "tools/round-80/pointer-bind.py"
LANDING = ".ufo/waves/round-81/l1/scores/c2-at-landing.json"
FORGED_UNDER = ".ufo/waves/round-81/w1/ExecCounter/undersized-pristine.json"
FORGED_DIRTY = ".ufo/waves/round-81/w1/ExecCounter/dirty-pristine-summary.json"

COPY_FILES = [COUNTER, BINDER, LANDING, FORGED_UNDER, FORGED_DIRTY]


def sh(argv, **kw):
    return subprocess.run(argv, check=True, capture_output=True, text=True, **kw).stdout


def git_bytes(rev, path):
    return subprocess.check_output(["git", "-C", LANE, "show", f"{rev}:{path}"])


def main():
    digests = {}
    for p in COPY_FILES:
        b = git_bytes(REV, p)
        digests[p] = hashlib.sha256(b).hexdigest()
        dst = os.path.join(REPO, p)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as f:
            f.write(b)
    # pin sanity for the fixture copies
    assert digests[COUNTER] == "52c829c604a5aac9306458cc6291b8cc648d3999ccf2eec0348666e582d524d6"
    assert digests[BINDER] == "a5755ba1884f0c8d695d16289edbf5dff420e72d7552d424c2cc2df7bb94a438"

    def git(*args):
        return sh(["git", "-C", REPO, *args])

    git("init", "-q")
    top = git("rev-parse", "--show-toplevel").strip()
    assert top == os.path.realpath(REPO), f"toplevel mismatch: {top}"
    git("add", "-A")
    git("-c", "user.email=reviewer-c1@scratch.invalid",
        "-c", "user.name=ReviewerC1", "commit", "-qm",
        "control: retained r81 receipts + pinned instruments at eb227c4 bytes")
    head = git("rev-parse", "HEAD").strip()
    out = {"fixture": REPO, "control_commit": head, "source_rev": REV,
           "digests": digests}
    with open(SCRATCH + "/evidence/fixture-control.json", "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
