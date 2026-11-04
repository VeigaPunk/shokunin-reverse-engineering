#!/usr/bin/env python3
"""Round-79 ScribeLesson re-derivations: five design-defect proofs.

Read-only against the lane: every instrument is copied into a scratch dir and
imported from there.  Nothing outside the scratch dir is written.

    TMPDIR=$S python3 -I -B prove.py <lane-root> <scratch-dir>

Prints one transcript; exits 0 when every expectation holds.
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

LANE = os.path.abspath(sys.argv[1])
SCRATCH = os.path.abspath(sys.argv[2])
RUN = tempfile.mkdtemp(prefix="scribelesson-prove-", dir=SCRATCH)
FAILS: list[str] = []


def check(name: str, observed, expected) -> None:
    ok = observed == expected
    print(f"  [{'ok' if ok else 'FAIL'}] {name}: {observed!r}"
          + ("" if ok else f"  (expected {expected!r})"))
    if not ok:
        FAILS.append(name)


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git_show(rev: str, path: str) -> bytes:
    return subprocess.check_output(
        ["git", "-C", LANE, "show", f"{rev}:{path}"])


for tool in ("tools/round-79/gate-mutation.py", "tools/round-79/pointer-bind.py"):
    shutil.copyfile(os.path.join(LANE, tool),
                    os.path.join(RUN, os.path.basename(tool)))
gm = load("gm", os.path.join(RUN, "gate-mutation.py"))
pb = load("pb", os.path.join(RUN, "pointer-bind.py"))

SOLE_REQUIRED = {"m03-near-miss-re-dead", "m05-atom-absent-bound",
                 "m08-validate-no-refusal-guard"}


def mutants() -> list[dict]:
    return [{"id": f"m{i:02d}-x", "declared_case": "c", "killed": True,
             "applied": True, "failed_cases": ["c"], "sole_detector": True}
            for i in range(1, 9)]


def receipt(**kw) -> dict:
    out = {"mutants_total": 8, "killed": 8, "survivors": 0, "survivor_ids": [],
           "declared_case_hits": 8, "target": {"sha256": "a" * 64},
           "target_pin": {"expected": "a" * 64, "matched": True},
           "pristine": {"ok": True, "failures": 0, "cases": 29}, "ok": False,
           "mutants": mutants()}
    out.update(kw)
    return out


def fixed_validate(r: dict) -> list[str]:
    defects = list(gm.validate_receipt(r)["defects"])
    pristine = r.get("pristine") or {}
    if pristine.get("ok") and pristine.get("cases") != 29:
        defects.append(f"pristine.ok with {pristine.get('cases')} cases, want 29")
    for m in r.get("mutants") or []:
        if m["id"] in SOLE_REQUIRED and m.get("killed") and not m.get("sole_detector"):
            defects.append(f"{m['id']}: killed but not by its declared case alone")
    return defects


print("== A1/A2  gate-mutation.py: predicate conjuncts recorded, never scored")
print(f"  ok path reads pristine.failures only: gate-mutation.py:236; ok at :313; "
      f"sole_detector written at :196/:269")
r1 = receipt(pristine={"ok": True, "failures": 0, "cases": 1})
print("  pristine.cases 1 (predicate: 29)")
check("A1 shipped validate -> no defect", gm.validate_receipt(r1)["defects"], [])
check("A1 fixed validate -> defect", fixed_validate(r1),
      ["pristine.ok with 1 cases, want 29"])
r2 = json.loads(json.dumps(receipt()))
r2["mutants"][2]["id"] = "m03-near-miss-re-dead"
r2["mutants"][2].update(failed_cases=["c", "c2", "c3"], sole_detector=False)
print("  m03 killed by three cases (predicate: that one case alone)")
check("A2 shipped validate -> no defect", gm.validate_receipt(r2)["defects"], [])
check("A2 fixed validate -> defect", fixed_validate(r2),
      ["m03-near-miss-re-dead: killed but not by its declared case alone"])
r3 = json.loads(json.dumps(r2))
r3["mutants"][2]["id"] = "m01-auth-dead"
print("  m01 killed by three cases (legitimately multi-detector at the freeze)")
check("A2 fixed validate stays clean for m01",
      [d for d in fixed_validate(r3) if "m01" in d], [])

print("== B  pointer-bind.py: two duplicate-cell precedence rules")
record = ("OMP `rea-agents@6.7.0` (`/h/omp.json:8`)\n"
          "Kimi `rea-agents@6.7.0` (`/h/kimi.toml:4126`)\n"
          "Kimi `rea-agents@6.7.0` (`/h/kimi.toml:4722`)\n"
          "`application.version=12.1.4` (`/h/Ghidra/application.properties:17`)\n"
          "(`/h/.bashrc:23-24`)\n(`/h/.bashrc:28-29`)\n")
bound = {c["id"]: c["pointer"] for c in pb.parse_record(record)[0]}
check("B kimi (dict comprehension, last wins)", bound["kimi-pin"], "/h/kimi.toml:4722")
check("B bashrc (re.search, first wins -- the stale cell)",
      bound["bashrc-exports"], "/h/.bashrc:23-24")
province = open(os.path.join(LANE, "PROVINCE.md"), encoding="utf-8").read()
live = {c["id"]: c["pointer"] for c in pb.parse_record(province)[0]}
print(f"  live PROVINCE.md bashrc cell: {live['bashrc-exports']} "
      f"(operative range at PROVINCE.md:27, historical .bashrc:63-69 at :28)")
check("B live cell is the operative range (by document order only)",
      live["bashrc-exports"].endswith(":28-29"), True)

print("== C  pointer-bind.py: the population floor is the parser's constant")
empty = pb.parse_record("")[0]
print(f"  empty record -> {len(empty)} checks: {[c['id'] for c in empty]}")
check("C empty record still reports 5 (the floor cannot fail)", len(empty), 5)
present = (len(pb.RE_PIN.findall(record)) + len(pb.RE_GHIDRA_PTR.findall(record))
           + len(pb.RE_BASHRC_PTR.findall(record)))
print(f"  record carries {present} pointer cells -> {len(pb.parse_record(record)[0])} checks")
check("C extra cell silently dropped",
      present - len(pb.parse_record(record)[0]), 1)

print("== D  pointer-bind.py: bind()'s line_count parameter is never read")
lines = ["a\n", '        "rea-agents@6.7.0",\n', "c\n", "d\n"]
check("D line_count=0 binds", pb.bind("f:2", ["rea-agents@6.7.0"], 0, lines)["matched"], True)
check("D line_count=999 binds identically",
      pb.bind("f:2", ["rea-agents@6.7.0"], 999, lines)["matched"], True)
check("D past-end bound comes from len(lines)",
      pb.bind("f:9", ["x"], 4, lines)["reason"],
      "line range 9-9 runs past end of file (4 lines)")

print("== E  pointer-bind.py: the read destination comes from the record's bytes")
outside = os.path.join(RUN, "outside.txt")
with open(outside, "w", encoding="utf-8") as handle:
    handle.write("GHIDRA_INSTALL_DIR=/x\n")
entry = pb.bind(f"{outside}:1", ["GHIDRA_INSTALL_DIR="], 1, pb.read_lines(outside))
check("E out-of-lane absolute path is read and bound", entry["matched"], True)
check("E receipt retains a digest, never the bytes",
      (len(entry["line_sha256"]), "line" in entry), (64, False))

print("== F  pre/selftest-gate.txt: the tally names no revision")
receipt_path = os.path.join(LANE, ".ufo/waves/round-79/pre/selftest-gate.txt")
tally = open(receipt_path, encoding="utf-8").read()
check("F tally carries the 29-case summary",
      tally.rstrip().splitlines()[-1], "SELFTEST cases=29 failures=0")
check("F tally carries no hex token (no rev, no digest)",
      [t for t in tally.replace(',', ' ').split() if len(t) >= 8
       and all(ch in "0123456789abcdef" for ch in t)], [])
blob = git_show("a1f9b81c", "tools/round-78/attack-gate.py")
import hashlib
check("F declaration blob equals the frozen pin",
      hashlib.sha256(blob).hexdigest(),
      "4e4baf00ef0cb34c5615155abd0a746b7e12a6a997340d32ce72c5402d32d2bf")
blade = os.path.join(RUN, "gate-at-decl.py")
open(blade, "wb").write(blob)
env = {k: os.environ.get(k, "") for k in ("HOME", "LANG", "PATH", "TMPDIR")}
proc = subprocess.run([sys.executable, "-I", "-B", blade, "--selftest"],
                      capture_output=True, text=True, env=env, cwd=RUN)
check("F re-run of the pinned blob reproduces the receipt byte-for-byte",
      (proc.stdout == tally,
       hashlib.sha256(proc.stdout.encode()).hexdigest()[:16],
       hashlib.sha256(tally.encode()).hexdigest()[:16]),
      (True,
       hashlib.sha256(tally.encode()).hexdigest()[:16],
       hashlib.sha256(tally.encode()).hexdigest()[:16]))

print("== G  the frozen R79-C2 counting command is refused by the frozen instrument")
claims = json.load(open(os.path.join(LANE, ".ufo/waves/round-79/claims.json"),
                        encoding="utf-8"))
c2 = next(c for c in claims["claims"] if c["id"] == "R79-C2")
print(f"  claims.json counting_command: {c2['counting_command']}")
check("G the frozen command omits --battery", "--battery" in c2["counting_command"],
      False)
frozen = git_show("ed68cd0a", "tools/round-79/pointer-bind.py")
frozen_path = os.path.join(RUN, "pb-freeze.py")
open(frozen_path, "wb").write(frozen)
printed = subprocess.run(
    [sys.executable, "-I", "-B", frozen_path, "--root", LANE,
     "--rev", "ed68cd0a", "--json-out", os.path.join(RUN, "g.json")],
    capture_output=True, text=True, env=env, cwd=RUN)
check("G the frozen command exits 2 and writes no receipt",
      (printed.returncode,
       os.path.exists(os.path.join(RUN, "g.json")),
       printed.stderr.strip()),
      (2, False,
       "usage: --battery --rev <rev> [--json-out <path>] [--control path-only]"))
with_flag = subprocess.run(
    [sys.executable, "-I", "-B", frozen_path, "--root", LANE,
     "--rev", "ed68cd0a", "--battery", "--json-out", os.path.join(RUN, "g2.json")],
    capture_output=True, text=True, env=env, cwd=RUN)
check("G the same bytes with --battery exit 0", with_flag.returncode, 0)
check("G the C1 command does carry --battery",
      "--battery" in next(c for c in claims["claims"]
                          if c["id"] == "R79-C1")["counting_command"], True)

print(f"\nRESULT: {len(FAILS)} failed checks" + (f": {FAILS}" if FAILS else ""))
sys.exit(1 if FAILS else 0)
