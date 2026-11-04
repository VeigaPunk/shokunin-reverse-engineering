#!/usr/bin/env python3
"""Mutation harness for the round-80 seat MutInstruments.

One-edit mutants of an instrument, judged by its own `--selftest`:

  * pristine run first (recorded, not scored as a mutant),
  * each mutant anchor asserted to occur exactly once in the pristine bytes,
  * the mutant source syntax-checked with compile() (no pycache written),
  * the mutant `--selftest` run under a FOUR-KEY child env (PATH/HOME/TMPDIR/LANG
    only, nothing inherited),
  * `killed` = a `SELFTEST cases=N failures=M` summary is present and M >= 1;
    no summary (or a syntax error) is `inconclusive`, never `killed`.

Usage:
  mutation-harness.py --spec SPEC.json --work WORKDIR --json-out OUT.json

Spec shape:
  {"targets": [{"name": ..., "path": <abs>, "selftest_args": [...],
                "mutants": [{"id": ..., "anchor": ..., "replacement": ...,
                             "edit": <prose>}]}]}

The target is copied into WORKDIR/<name>/<mutant>.py; the lane file is never
written and the instrument's own directory is never the cwd of a mutant run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

SUMMARY = re.compile(r"^SELFTEST cases=(\d+) failures=(\d+)$", re.MULTILINE)
CASE_LINE = re.compile(r'^\{"case":')
ENV_KEYS = ("PATH", "HOME", "TMPDIR", "LANG")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def child_env(work: str) -> dict:
    """Exactly four keys; nothing else is inherited."""
    return {"PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin"),
            "HOME": os.environ.get("HOME", "/root"),
            "TMPDIR": work,
            "LANG": os.environ.get("LANG", "C.UTF-8")}


def run_selftest(path: pathlib.Path, selftest_args: list[str], work: str) -> dict:
    argv = [sys.executable, "-I", "-B", str(path), *selftest_args, "--selftest"]
    proc = subprocess.run(argv, capture_output=True, text=True,
                          env=child_env(work), cwd=str(path.parent), timeout=300)
    text = proc.stdout + ("\n" + proc.stderr if proc.stderr else "")
    match = SUMMARY.search(proc.stdout)
    failing = []
    for line in proc.stdout.splitlines():
        if CASE_LINE.match(line):
            try:
                case = json.loads(line)
            except json.JSONDecodeError:
                continue
            if case.get("pass") is False:
                failing.append(case.get("case"))
    summary_found = match is not None
    cases = int(match.group(1)) if match else None
    failures = int(match.group(2)) if match else None
    return {"argv": argv, "exit": proc.returncode,
            "summary_present": summary_found,
            "cases": cases, "failures": failures,
            "failing_cases": failing,
            "stdout_tail": "\n".join(proc.stdout.splitlines()[-4:]),
            "stderr_tail": "\n".join(proc.stderr.splitlines()[-4:])}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--json-out", required=True)
    args = ap.parse_args(argv)

    spec = json.loads(pathlib.Path(args.spec).read_text(encoding="utf-8"))
    work = pathlib.Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    out: dict = {"schema": "mutinstruments-r80-v1", "work": str(work),
                 "targets": [], "mutants": [], "survivors": [],
                 "inconclusive": [], "spec_errors": []}

    for target in spec["targets"]:
        src = pathlib.Path(target["path"]).resolve()
        if not src.is_file():
            out["spec_errors"].append(f"{target['name']}: absent {src}")
            continue
        raw = src.read_bytes()
        text = raw.decode("utf-8")
        tdir = work / target["name"]
        tdir.mkdir(parents=True, exist_ok=True)
        pristine = tdir / "pristine.py"
        pristine.write_bytes(raw)
        selftest_args = target.get("selftest_args") or []

        base = run_selftest(pristine, selftest_args, str(tdir))
        out["targets"].append({
            "name": target["name"], "path": str(src), "sha256": sha256(raw),
            "bytes": len(raw), "pristine": {
                "exit": base["exit"], "cases": base["cases"],
                "failures": base["failures"],
                "summary_present": base["summary_present"],
                "failing_cases": base["failing_cases"],
            },
            "anchor_checks": [],
        })
        tindex = len(out["targets"]) - 1

        for mut in target["mutants"]:
            occurrences = text.count(mut["anchor"])
            anchor_ok = occurrences == 1
            out["targets"][tindex]["anchor_checks"].append(
                {"id": mut["id"], "occurrences": occurrences, "ok": anchor_ok})
            record = {"target": target["name"], "id": mut["id"],
                      "edit": mut.get("edit", ""),
                      "anchor_occurrences": occurrences}
            if not anchor_ok:
                record.update({"verdict": "inconclusive",
                               "reason": "anchor does not occur exactly once"})
                out["mutants"].append(record)
                out["inconclusive"].append(record["target"] + "/" + record["id"])
                continue
            mutated = text.replace(mut["anchor"], mut["replacement"], 1)
            mpath = tdir / f"{mut['id']}.py"
            mpath.write_text(mutated, encoding="utf-8")
            try:
                compile(mutated, str(mpath), "exec")
            except SyntaxError as exc:
                record.update({"verdict": "inconclusive",
                               "reason": f"does not compile: {exc}"})
                out["mutants"].append(record)
                out["inconclusive"].append(record["target"] + "/" + record["id"])
                continue
            run = run_selftest(mpath, selftest_args, str(tdir))
            killed = bool(run["summary_present"] and (run["failures"] or 0) >= 1)
            verdict = ("killed" if killed else
                       "survived" if run["summary_present"] else "inconclusive")
            record.update({
                "mutant_sha256": sha256(mutated.encode("utf-8")),
                "exit": run["exit"], "cases": run["cases"],
                "failures": run["failures"],
                "summary_present": run["summary_present"],
                "killed_by": sorted(run["failing_cases"]),
                "sole_detector": killed and len(run["failing_cases"]) == 1,
                "survived": verdict == "survived",
                "verdict": verdict,
            })
            if verdict == "inconclusive":
                record["stdout_tail"] = run["stdout_tail"]
                record["stderr_tail"] = run["stderr_tail"]
                out["inconclusive"].append(record["target"] + "/" + record["id"])
            if verdict == "survived":
                out["survivors"].append({"target": record["target"],
                                         "id": record["id"],
                                         "edit": record["edit"],
                                         "case_that_would_kill": mut.get("killer_case"),
                                         "mutant": str(mpath)})
            out["mutants"].append(record)

    pathlib.Path(args.json_out).write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    summary = {"targets": len(out["targets"]),
               "mutants": len(out["mutants"]),
               "killed": sum(1 for m in out["mutants"] if m.get("verdict") == "killed"),
               "survived": sum(1 for m in out["mutants"] if m.get("verdict") == "survived"),
               "inconclusive": len(out["inconclusive"]),
               "spec_errors": out["spec_errors"]}
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
