#!/usr/bin/env python3
"""Mutation-test the round-79 instruments' own selftests (seat MutInstruments)."""

import hashlib
import json
import os
import re
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
SELFTEST_LINE = re.compile(r"^SELFTEST cases=(?P<cases>\d+) failures=(?P<failures>\d+)$")

PB = "pointer-bind"
GM = "gate-mutation"

MUTANTS = [
    {
        "id": "pb-a-path-only",
        "instrument": PB,
        "edit": "bind() returns matched=True as soon as the pointed path exists "
                "(the path-only rule)",
        "anchor": '    if lines is None:\n'
                  '        out["reason"] = f"path {match.group(\'path\')} does not exist"\n'
                  '        return out\n'
                  '    if end > len(lines):\n',
        "replace": '    if lines is None:\n'
                   '        out["reason"] = f"path {match.group(\'path\')} does not exist"\n'
                   '        return out\n'
                   '    out["matched"] = True\n'
                   '    return out\n'
                   '    if end > len(lines):\n',
        "declared_case": "red-stale-line",
    },
    {
        "id": "pb-b-zero-based",
        "instrument": PB,
        "edit": "the pointed slice is taken 0-based (lines[start:end])",
        "anchor": "    pointed = lines[start - 1:end]\n",
        "replace": "    pointed = lines[start:end]\n",
        "declared_case": "green-line",
    },
    {
        "id": "pb-c-range-first-line",
        "instrument": PB,
        "edit": "a range is compared as its first line only "
                "(lines[start - 1:start])",
        "anchor": "    pointed = lines[start - 1:end]\n",
        "replace": "    pointed = lines[start - 1:start]\n",
        "declared_case": "green-range",
    },
    {
        "id": "pb-d-unparsed-never",
        "instrument": PB,
        "edit": "bind() never sets the unparsed flag (out[\"unparsed\"] = False)",
        "anchor": '    if not match:\n        out["unparsed"] = True\n',
        "replace": '    if not match:\n        out["unparsed"] = False\n',
        "declared_case": "red-no-line",
    },
    {
        "id": "pb-e-validate-range-guard",
        "instrument": PB,
        "edit": "validate_receipt drops the matched-without-a-1-based-range guard",
        "anchor": '        start, end = check.get("line_start"), check.get("line_end")\n'
                  '        if check.get("matched") and not (isinstance(start, int) '
                  'and isinstance(end, int)\n'
                  '                                         and 1 <= start <= end):\n'
                  '            defects.append(f"{check.get(\'id\')}: matched without a '
                  '1-based line range")\n',
        "replace": "",
        "declared_case": None,
    },
    {
        "id": "pb-f-nonparse-matched",
        "instrument": PB,
        "edit": "battery counts a record cell that does not parse as matched",
        "anchor": '            results.append({"id": check["id"], "pointer": "", '
                  '"tokens": [],\n'
                  '                            "path": "", "line_start": None, '
                  '"line_end": None,\n'
                  '                            "matched": False, "unparsed": True,\n',
        "replace": '            results.append({"id": check["id"], "pointer": "", '
                   '"tokens": [],\n'
                   '                            "path": "", "line_start": None, '
                   '"line_end": None,\n'
                   '                            "matched": True, "unparsed": True,\n',
        "declared_case": None,
    },
    {
        "id": "gm-e-absent-killed",
        "instrument": GM,
        "edit": "judge counts an absent declared case as killed "
                "(killed = absent or cases[declared] is False)",
        "anchor": "    killed = (not absent) and cases[declared] is False\n",
        "replace": "    killed = absent or cases[declared] is False\n",
        "declared_case": "red-case-absent",
    },
    {
        "id": "gm-f-validate-no-guard",
        "instrument": GM,
        "edit": "validate_receipt skips the killed-without-its-declared-case-failing "
                "guard",
        "anchor": '        if mutant.get("killed") and (\n'
                  '                mutant.get("case_absent")\n'
                  '                or mutant.get("declared_case") not in '
                  '(mutant.get("failed_cases") or [])):\n'
                  '            defects.append(f"{mutant.get(\'id\')}: killed without '
                  'its declared case failing")\n',
        "replace": "",
        "declared_case": None,
    },
    {
        "id": "gm-g-pristine-guard",
        "instrument": GM,
        "edit": "validate_receipt drops the pristine.ok-with-nonzero-failures guard",
        "anchor": '    if pristine.get("ok") and pristine.get("failures") != 0:\n'
                  '        defects.append("pristine.ok with nonzero failures")\n',
        "replace": "",
        "declared_case": None,
    },
    {
        "id": "gm-h-applied-guard",
        "instrument": GM,
        "edit": "validate_receipt drops the killed-without-an-applied-edit guard",
        "anchor": '        if mutant.get("killed") and mutant.get("applied") is not True:\n'
                  '            defects.append(f"{mutant.get(\'id\')}: killed without '
                  'an applied edit")\n',
        "replace": "",
        "declared_case": None,
    },
]

SOURCES = {
    PB: os.path.join(S, "pointer-bind.orig.py"),
    GM: os.path.join(S, "gate-mutation.orig.py"),
}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def parse_selftest(stdout):
    cases, cases_n, failures_n = {}, None, None
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            m = SELFTEST_LINE.match(line)
            if m:
                cases_n, failures_n = int(m.group("cases")), int(m.group("failures"))
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(entry, dict) and isinstance(entry.get("case"), str):
            cases[entry["case"]] = bool(entry.get("pass"))
    return cases, cases_n, failures_n


def run_selftest(path, work):
    env = {k: os.environ.get(k, "") for k in ("HOME", "LANG", "PATH", "TMPDIR")}
    proc = subprocess.run([sys.executable, "-I", "-B", path, "--selftest"],
                          capture_output=True, text=True, env=env, cwd=work,
                          timeout=120)
    return proc.returncode, proc.stdout, proc.stderr


def main():
    work = os.path.join(S, "run")
    outdir = os.path.join(work, "mutants")
    os.makedirs(outdir, exist_ok=True)
    texts = {}
    for name, path in SOURCES.items():
        with open(path, encoding="utf-8") as fh:
            texts[name] = fh.read()

    pristine = {}
    for name, path in SOURCES.items():
        rc, out, err = run_selftest(path, work)
        cases, n, fails = parse_selftest(out)
        pristine[name] = {
            "path": os.path.basename(path),
            "sha256": sha256(texts[name].encode()),
            "exit": rc, "cases": n, "failures": fails,
            "failing_cases": sorted(k for k, v in cases.items() if not v),
            "summary_present": n is not None,
            "ok": rc == 0 and n is not None and fails == 0 and not any(
                not v for v in cases.values()),
        }

    results = []
    for mut in MUTANTS:
        src = texts[mut["instrument"]]
        hits = src.count(mut["anchor"])
        rec = {"id": mut["id"], "instrument": mut["instrument"], "edit": mut["edit"],
               "declared_case": mut["declared_case"], "anchor_occurrences": hits,
               "applied": hits == 1, "exit": None, "cases": None, "failures": None,
               "failing_cases": [], "killed": False, "killed_by": [],
               "inconclusive": False, "syntax_ok": None,
               "sha256_before": sha256(src.encode()), "sha256_after": None}
        if hits != 1:
            rec["inconclusive"] = True
            rec["note"] = f"anchor occurs {hits} times, want exactly 1"
            results.append(rec)
            continue
        mutated = src.replace(mut["anchor"], mut["replace"], 1)
        rec["sha256_after"] = sha256(mutated.encode())
        path = os.path.join(outdir, mut["id"] + ".py")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(mutated)
        comp = subprocess.run([sys.executable, "-I", "-B", "-c",
                               "import py_compile,sys;"
                               "py_compile.compile(sys.argv[1],doraise=True)",
                               path], capture_output=True, text=True)
        rec["syntax_ok"] = comp.returncode == 0
        if comp.returncode != 0:
            rec["inconclusive"] = True
            rec["note"] = "mutated copy does not compile"
            rec["stderr_tail"] = comp.stderr.strip().splitlines()[-2:]
            results.append(rec)
            continue
        rc, out, err = run_selftest(path, work)
        cases, n, fails = parse_selftest(out)
        rec.update({"exit": rc, "cases": n, "failures": fails})
        rec["failing_cases"] = sorted(k for k, v in cases.items() if not v)
        if n is None:
            rec["inconclusive"] = True
            rec["note"] = "no SELFTEST summary"
            rec["stderr_tail"] = err.strip().splitlines()[-2:]
        else:
            rec["killed"] = bool(rc != 0 or fails or rec["failing_cases"])
            rec["killed_by"] = rec["failing_cases"]
        results.append(rec)

    survivors = [r["id"] for r in results if not r["killed"]]
    if any(r["inconclusive"] for r in results):
        survivors = [r["id"] for r in results if not r["killed"] and not r["inconclusive"]]
    receipt = {"schema": "kaidoku-r79-instrument-mutation-v1",
               "round": 79,
               "instrument_pins": {
                   "tools/round-79/pointer-bind.py": pristine[PB]["sha256"],
                   "tools/round-79/gate-mutation.py": pristine[GM]["sha256"]},
               "pristine": pristine,
               "mutants_total": len(results),
               "killed": sum(1 for r in results if r["killed"]),
               "survivors": len(survivors),
               "survivor_ids": survivors,
               "inconclusive_ids": [r["id"] for r in results if r["inconclusive"]],
               "mutants": results}
    with open(os.path.join(work, "receipt.json"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(receipt, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"pristine": {k: {"cases": v["cases"], "failures": v["failures"],
                                       "exit": v["exit"]}
                                   for k, v in pristine.items()},
                      "mutants_total": receipt["mutants_total"],
                      "killed": receipt["killed"],
                      "survivors": receipt["survivors"],
                      "survivor_ids": survivors,
                      "inconclusive": receipt["inconclusive_ids"],
                      "per_mutant": {r["id"]: {"killed": r["killed"],
                                               "by": r["killed_by"],
                                               "exit": r["exit"],
                                               "failures": r["failures"]}
                                     for r in results}}, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
