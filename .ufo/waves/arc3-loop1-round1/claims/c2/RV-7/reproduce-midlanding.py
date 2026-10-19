#!/usr/bin/env python3
"""RV-7 — reproduce the mid-landing probe revision observed at 07:15:49.

At 2026-10-19T07:15:49-03:00 the real target `.ufo/gates/citation-drift/
citation-drift-probe.py` hashed to
`53a94df2628ddb1ca194a66cb5138d499ae465b086ea303917c01c1ef5ee43bd` and its
selftest read `FAILED cases=13 passed=1 failed=12 exit=1`. Twelve seconds later
it settled at `e2665074…` with 13/13 CLEAN.

This script turns that transient into a reproducible artifact: it derives the
intermediate revision from the landed probe by reverting exactly the last hunk of
PL-2's patch 1 (the selftest-harness pin injection and the two fixture
mutations), asserts the derived bytes hash to the observed sha, and re-runs the
selftest against the landed 13-case expected.json.

Read-only over the repo. Usage: python3 reproduce-midlanding.py
"""
import hashlib
import os
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
PROBE = os.path.join(REPO, ".ufo/gates/citation-drift/citation-drift-probe.py")
EXPECTED = os.path.join(REPO, ".ufo/gates/citation-drift/expected.json")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tmp", "midlanding")
OBSERVED = "53a94df2628ddb1ca194a66cb5138d499ae465b086ea303917c01c1ef5ee43bd"

HARNESS_PIN = '''                table_bytes = open(table, "rb").read()
                expected = {"snapshots": digests,
                            "pointer_table": {"sha256": sha256_bytes(table_bytes)}}'''
HARNESS_PIN_REVERTED = '''                expected = {"snapshots": digests}'''
FIXTURE_MUTATIONS = '''                if case == "table_tampered":
                    # the silent-clean shape: a valid table with no entries
                    # grades findings=0 at rc 0 without the frozen-run guard
                    open(table, "w").write(json.dumps({"entries": []}))
                elif case == "table_absent":
                    os.remove(table)
'''


def main():
    src = open(PROBE).read()
    mid = src
    for old, new in ((HARNESS_PIN, HARNESS_PIN_REVERTED), (FIXTURE_MUTATIONS, "")):
        assert old in mid, "hunk anchor missing — landed probe changed"
        mid = mid.replace(old, new, 1)
    got = hashlib.sha256(mid.encode()).hexdigest()
    print("derived intermediate sha256: %s" % got)
    print("observed at 07:15:49        : %s -> %s"
          % (OBSERVED, "MATCH" if got == OBSERVED else "DIFFERENT"))
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "probe-midlanding.py")
    open(path, "w").write(mid)
    env = dict(os.environ, TMPDIR=os.path.join(HERE, "tmp"))
    r = subprocess.run([sys.executable, path, "--selftest", "--expected", EXPECTED],
                       capture_output=True, text=True, env=env)
    print(r.stdout.strip())
    print("rc=%d" % r.returncode)
    return 0 if got == OBSERVED else 1


if __name__ == "__main__":
    sys.exit(main())
