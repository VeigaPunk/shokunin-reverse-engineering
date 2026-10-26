#!/usr/bin/env python3
"""mutants.py -- show that absence-sweep.py's selftest is able to fail.

Each mutant is a byte-level patch of absence-sweep.py in $TMPDIR that reproduces one classic
false-absence mechanism. A mutant's own `--selftest` must report fail >= 1; a mutant whose selftest
stays green means the covering case does not exist and is reported as HARNESS-GAP.

Usage: python3 -I -B mutants.py [--script PATH] [--json]
Exit: 0 all mutants killed (selftest failed on them), 1 a mutant survived, 2 setup error.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

MUTANTS = [
    {
        "id": "M1-substring-suffix",
        "about": "endswith() on the joined claim instead of component-aligned match "
                 "(the plain `find -name`-shaped error: look-alikes count as hits)",
        "case_expected_red": "substring-decoy",
        "old": "                if parts[-n:] != claim_parts:\n",
        "new": "                if not ent.path.endswith('/'.join(claim_parts)):\n",
    },
    {
        "id": "M2-first-root-only",
        "about": "sweep only the first --root (the exact R38-CL1 false-green mechanism)",
        "case_expected_red": "present-second-root",
        "old": "    hits, stats = sweep(claim_parts, usable, max_hits)\n",
        "new": "    hits, stats = sweep(claim_parts, usable[:1], max_hits)\n",
    },
    {
        "id": "M3-swallow-root-errors",
        "about": "silently skip an unusable root instead of exit 2 (absence from a root never read)",
        "case_expected_red": "missing-root",
        "old": '        if not os.path.isdir(r):\n            errors.append("root is missing or not a directory: %s" % r)\n            continue\n',
        "new": '        if not os.path.isdir(r):\n            continue\n',
    },
    {
        "id": "M4-unreadable-subtree-as-absent",
        "about": "certify ABSENT even when subtrees could not be read",
        "case_expected_red": "unreadable-subtree-incomplete",
        "old": '    elif stats["skipped_dirs"]:\n        verdict, code = "INCOMPLETE", EXIT_ERROR\n',
        "new": '    elif stats["skipped_dirs"]:\n        verdict, code = "ABSENT", ABSENT\n',
    },
    {
        "id": "M7-no-glob-guard",
        "about": "accept a glob claim, which matches nothing and certifies a false ABSENT",
        "case_expected_red": "glob-claim",
        "old": '    if any(ch in claim for ch in "*?["):\n',
        "new": '    if False:\n',
    },
    {
        "id": "M6-no-anchor-note",
        "about": "drop the unanchored-claim warning, so a wrong-base ABSENT looks like a clean one",
        "case_expected_red": "unanchored-note",
        "old": '    if verdict == "ABSENT" and len(claim_parts) > 1 and not anchored:\n        note = (',
        "new": '    if False:\n        note = (',
    },
    {
        "id": "M5-no-root-dedupe",
        "about": "keep duplicate/nested roots, so one file is walked and listed twice",
        "case_expected_red": "nested-roots-dedup",
        "old": "        if any(rp == k or rp.startswith(k.rstrip(os.sep) + os.sep) for k in kept_real):\n            continue\n",
        "new": "        if False:\n            continue\n",
    },
]


def run_selftest(script):
    proc = subprocess.run([sys.executable, "-I", "-B", script, "--selftest"],
                          capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    summary = ""
    for line in out.splitlines():
        if line.startswith("SELFTEST "):
            summary = line
    failed_cases = [ln.split()[1] for ln in out.splitlines()
                    if ln.startswith("FAIL ")]
    return proc.returncode, summary, failed_cases, out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                    "absence-sweep.py"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    src = args.script
    if not os.path.isfile(src):
        sys.stderr.write("ERROR script not found: %s\n" % src)
        return 2
    base = tempfile.mkdtemp(prefix="absence-sweep-mutants-")
    results = []
    try:
        code, summary, failed, _ = run_selftest(src)
        results.append({"id": "M0-original", "killed": code == 0, "summary": summary,
                        "failed_cases": failed, "expect": "selftest green"})
        text = open(src).read()
        for m in MUTANTS:
            if text.count(m["old"]) != 1:
                results.append({"id": m["id"], "killed": False,
                                "summary": "PATCH-SITE-NOT-UNIQUE count=%d" % text.count(m["old"]),
                                "failed_cases": [], "expect": m["case_expected_red"]})
                continue
            path = os.path.join(base, m["id"] + ".py")
            with open(path, "w") as fh:
                fh.write(text.replace(m["old"], m["new"]))
            code, summary, failed, out = run_selftest(path)
            killed = code != 0 and bool(failed)
            results.append({"id": m["id"], "killed": killed, "summary": summary,
                            "failed_cases": failed, "expect": m["case_expected_red"],
                            "about": m["about"],
                            "covered_expectation": m["case_expected_red"] in failed})
    finally:
        shutil.rmtree(base, ignore_errors=True)

    if args.json:
        print(json.dumps(results, indent=1))
    else:
        for r in results:
            tag = "GREEN" if r["id"] == "M0-original" else ("KILLED" if r["killed"] else "SURVIVED")
            print("%-9s %-32s %s  failed=%s" % (tag, r["id"], r["summary"],
                                                ",".join(r["failed_cases"]) or "-"))
    bad = [r for r in results
           if (r["id"] == "M0-original" and not r["killed"])
           or (r["id"] != "M0-original" and not r["killed"])]
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
