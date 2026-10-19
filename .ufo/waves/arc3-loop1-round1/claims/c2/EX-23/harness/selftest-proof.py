#!/usr/bin/env python3
"""EX-23: prove a guard shape that keeps the existing 11 selftest cases green
and reaches the claim's 13 cases at exit 0 (reference recipe for EX-16).

guardC = guardB (guard block + verdict() CNE registration)
         + selftest per-case pin: the fixture run's expected.json carries the
           sha256 of the fixture table it was built with
         + a table_absent case skips writing the fixture table
Scratch expected-13.json = the committed case table + the two new rows.
"""
import hashlib
import json
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "head-citation-drift-probe.py")
CLEAN_EXPECTED = os.path.join(BASE, "head-expected.json")
GUARDB = os.path.join(BASE, "guardB.py")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


SELFTEST_OLD = '''                else:
                    root = build_fixture(case)
                    table = os.path.join(case_dir, "table.json")
                    json.dump(fixture_table(case), open(table, "w"))
'''
SELFTEST_NEW = '''                else:
                    root = build_fixture(case)
                    table = os.path.join(case_dir, "table.json")
                    if case != "table_absent":
                        json.dump(fixture_table(case), open(table, "w"))
'''
PIN_OLD = '''                expected = {"snapshots": digests}
                exp_file = os.path.join(case_dir, "expected.json")
                json.dump(expected, open(exp_file, "w"))
'''
PIN_NEW = '''                expected = {"snapshots": digests}
                # frozen-run guard: the fixture run pins the digest of the
                # table it was built with, so the guard stays universal
                if case == "table_tampered":
                    expected["frozen_run"] = {"table_sha256": "0" * 64}
                elif case == "table_absent":
                    expected["frozen_run"] = {
                        "table_sha256": sha256_bytes(b"absent on purpose")}
                else:
                    expected["frozen_run"] = {
                        "table_sha256": sha256_bytes(open(table, "rb").read())}
                exp_file = os.path.join(case_dir, "expected.json")
                json.dump(expected, open(exp_file, "w"))
'''


def main():
    src = open(GUARDB, encoding="utf-8").read()
    assert SELFTEST_OLD in src and PIN_OLD in src
    c = src.replace(SELFTEST_OLD, SELFTEST_NEW, 1).replace(PIN_OLD, PIN_NEW, 1)
    guardC = os.path.join(BASE, "guardC.py")
    open(guardC, "w", encoding="utf-8").write(c)

    exp = json.loads(open(CLEAN_EXPECTED, encoding="utf-8").read())
    exp["selftest"] = exp["selftest"] + [
        {"case": "table_tampered", "exit_code": 2, "finding": "pointer_table_tampered"},
        {"case": "table_absent", "exit_code": 2, "finding": "pointer_table_unreadable"},
    ]
    exp13 = os.path.join(BASE, "expected-13.json")
    json.dump(exp, open(exp13, "w"), indent=2)

    print("--- guardC selftest, 13-case table ---")
    p = subprocess.run([sys.executable, guardC, "--selftest", "--expected", exp13],
                       capture_output=True, text=True, timeout=300)
    for l in p.stdout.splitlines():
        if l.startswith("SELFTEST_CASE:") or l.startswith("CITATION_DRIFT_SELFTEST:"):
            print(l)
    print("exit=%d traceback=%s" % (p.returncode, "Traceback" in p.stderr))
    return p.returncode


if __name__ == "__main__":
    sys.exit(main())
