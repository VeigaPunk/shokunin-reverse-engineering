#!/usr/bin/env python3
"""Round-31 freeze-integrity gate (mistake M31-2).

The round-31 counters compare a frozen input in the tree with the same path at --rev,
and tools/round-30/prefreeze-gate.py checks the pins at the freeze commit; neither
notices a frozen input edited in a commit AFTER the freeze (wave-1 CtlC2RewritePred:
the counter and the prefreeze gate both passed an amended predictions.tsv).

This gate reads Git objects only.  For round <N> it finds the freeze commit (the first
commit reachable from --rev that adds .ufo/waves/round-<N>/claims.json), reads the
`instruments` and `frozen_inputs` digests from the claims file AT THE FREEZE COMMIT,
and requires every pinned path at --rev to hash to that digest and to have no commit
touching it in freeze..rev.

  python3 -I -B tools/round-31/freeze-integrity.py --root <LANE> --round <N> [--rev <REV>]

Prints one line per pin and `freeze-integrity: CLEAN pins=K` (exit 0) or
`freeze-integrity: FAIL ...` (exit 1); exit 2 when the freeze commit is absent.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys


def git(root, *args, binary=False):
    env = {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}
    p = subprocess.run(["git", "-C", root] + list(args), capture_output=True, env=env)
    return p.returncode, (p.stdout if binary else p.stdout.decode())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--round", required=True)
    ap.add_argument("--rev", default="HEAD")
    a = ap.parse_args()
    claims = ".ufo/waves/round-%s/claims.json" % a.round
    rc, out = git(a.root, "log", "--format=%H", "--diff-filter=A", a.rev, "--", claims)
    commits = out.split()
    if rc != 0 or not commits:
        print("freeze-integrity: ERROR no commit adds %s at %s" % (claims, a.rev))
        return 2
    freeze = commits[-1]
    rc, text = git(a.root, "show", "%s:%s" % (freeze, claims))
    pins = {}
    for key in ("instruments", "frozen_inputs"):
        pins.update(json.loads(text).get(key, {}))
    bad = 0
    for path, digest in sorted(pins.items()):
        rc, blob = git(a.root, "show", "%s:%s" % (a.rev, path), binary=True)
        got = hashlib.sha256(blob).hexdigest() if rc == 0 else "absent"
        rc2, touched = git(a.root, "log", "--format=%h", "%s..%s" % (freeze, a.rev), "--", path)
        touched = touched.split()
        ok = got == digest and not touched
        bad += not ok
        print("%s\t%s\tsha=%s\tcommits_after_freeze=%s" % ("ok" if ok else "FAIL", path, got[:12],
                                                          ",".join(touched) or "0"))
    if bad:
        print("freeze-integrity: FAIL pins=%d changed=%d freeze=%s rev=%s" % (len(pins), bad, freeze[:12], a.rev))
        return 1
    print("freeze-integrity: CLEAN pins=%d freeze=%s rev=%s" % (len(pins), freeze[:12], a.rev))
    return 0


if __name__ == "__main__":
    sys.exit(main())
