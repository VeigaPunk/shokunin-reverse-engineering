# CritControlAdequacy — R34-C2 control adequacy (round 34, run-6 re-dispatch, wave 1)

Seat: `L1Kaidoku34-2.CritControlAdequacy`. Scope: name the cheapest control that still skips the
claimed work and is not among the five committed controls; predict each candidate's counter verdict
from the code; say whether the frozen clauses catch it. Read-only on lane VCS; all probes run from
`/fast/scratch/hyaku/kaidoku-r34b/w1/CritControlAdequacy/` (copies only). No tool installed
(`python3 3.14.8` used as-is; no `uv`/`npx`/pacman transaction).

## 0. State observed before analysis (read this first)

- Frozen blobs unchanged: I read `tools/round-34/replay-gate.py`,
  `c2-shortcut-gate-counter.py`, both configs, `mini-fix/**` at worktree and at
  `c79bbe7b0959132b9873ff3431cf5eb313b58b33`; digests equal (`git show <rev>:<path> | sha256sum`
  == `sha256sum <worktree>` for both instruments). All 26 pins in `claims.json` match the worktree
  (`pinned=26 mismatched=0`, 2026-10-25T07:29Z).
- The lane advanced under this wave: tip is now `66b840274390d0868c913a544947f9eb40a4ffe6`, and
  `cd75b92e` already **stopped R34-C2** on an unregistered content-multiset shortcut. I did not
  reopen, rescore or relabel anything; this report attacks the **control set / clause set**, which
  the stop reasoning does not cover. No new stop is proposed — the claim is already stopped.
- `LOG.md:3099` already discloses in prose that "a 1,979-byte gate that runs no reader satisfies all
  six clauses". This report turns that into a named cheapest control, proves the receipt can be
  reproduced **byte-for-byte**, and shows why the repair routes listed in `claim-stop.json` (F1–F5)
  do not close it.

## 1. Answer

**Cheapest uncaught control: C1 — a gate that keys on the counter's own module name and returns
literal verdicts.** Delta to the pinned gate: **+16 / −1 lines** (one rename, one dispatch block);
production path spawns **nothing**. Observed: `GATE_COUNTER_OK`, all six clauses, exit 0
(`receipts/gate-name-sniff.json`, 2026-10-25T07:28:15Z). Strictest form (C1b, +18/−1) emits
registry-shaped rows, so **every measured field of its receipt equals the committed production
receipt** (`receipts/lane-c1b-mimic.json` == committed on `clauses/finding/met_target/exit/
selftest_failures/mutants_killed/green.positive_matched/green.shortcuts_below_target/red.classes`).

**Cheaper still, and not a gate control at all (C0e): the counter never records or validates
`--root`.** A 3-file synthetic root (`tools/round-34/{replay-gate.py,gate-config-mini.json,
gate-config-naive.json}`) containing a 2,242-byte stub that executes no reader, no counter and no
fixture produced a receipt **byte-identical** to the committed production receipt:
`sha256 = da78f44419ecf83935e1fe6b1cd72f611c5a0e7e03029e97580d515a0796f3e9` for both
(`cmp` → `IDENTICAL_BYTES`, 2026-10-25T07:35:04Z). `gate_path` reads `tools/round-34/replay-gate.py`,
`measured_revision` echoes the requested rev. There is no field left to distinguish it.

## 2. Mechanism — why every candidate below is invisible to the frozen clauses

1. **The two configs differ in exactly one token** (verified by JSON compare): `counter.argv[…][4]`
   is `mini-counter.py` vs `naive-counter.py`. `positive_control`, `predicate`, `schema`,
   `shortcuts`, `target` are identical. The only signal a gate can key on is the counter module
   name — which makes the key cheaper, not harder. (The "reads the red case's fixture names" idea
   from the brief cannot work: both configs name the same eight fixtures and the same seven readers.)
2. **The gate's selftest never uses the production argv.** `replay-gate.py:185-202` (`config_for`)
   builds every selftest config with `[sys.executable, "-I", "-B", str(root/"counter.py"),
   "--control-reader", "{reader}"]` (lines 189-190). So a production-only branch keyed on
   `mini-counter.py`/`naive-counter.py` is exercised by **zero** of the 12 selftest cases, and the
   three registered mutants (MUT-A/C/D, `replay-gate.py:165-171`) mutate branches the cheat does
   not use. `selftest_clean` and `mutants_killed` therefore certify the honest function, not the
   dispatch that production hits.
3. **All six clauses read the gate's self-report.** `c2-shortcut-gate-counter.py:112-119`:
   `selftest_clean` and `mutants_killed` read the gate's own `--selftest` JSON;
   `red_refused` reads `red.exit/red.verdict` and requires `"label-memorization" in red_classes`;
   `green_clean` reads `green.exit/green.verdict`; `green_positive_meets_target` reads a green row
   `matched == 8`; `gate_present` is `(root/args.gate).is_file()` (line 74) and then hardcoded
   `True` (line 119).
4. **`shortcuts_below_target` is computed (line 109) but is not in `clauses`.** C2 (below=0) and
   C1b (below=7) both pass; C1b fabricates the seven rows from `config["shortcuts"]` in five lines.
5. **No provenance exists to bind otherwise.** The receipt has no `root` and no instrument digest;
   `measured_revision` is `args.rev` verbatim (line 73) — `--rev NOT-A-REVISION-0xF00D` produced
   `met_target: true` with `measured_revision: "NOT-A-REVISION-0xF00D"`
   (`receipts/p5-freetext-rev.json`, 07:29Z). The counter never reads `claims.json`, never hashes
   the gate or the configs (`grep -n hashlib tools/round-34/c2-shortcut-gate-counter.py` → none),
   and `--gate` is a documented control escape hatch (line 69-70). C0e needs neither: it uses the
   **default** gate path in a fake root.

## 3. Candidates (predicted from code; *observed* = run)

| # | Control | Cost | Work skipped | Predicted verdict | Observed | Frozen clause that catches it |
|---|---------|------|--------------|-------------------|----------|-------------------------------|
| C0e | stub gate at the default path in a synthetic root; prints the production lines (no spawn) | 43 lines / 3 files, no delta to the pinned gate | everything | `GATE_COUNTER_OK` | **OK, receipt byte-identical** (`p2`, 07:35:04Z) | none |
| C0 | stub gate keyed on config basename in a synthetic root | 39 lines / 3 files | everything | `GATE_COUNTER_OK` | **OK**, exit 0 (`p1`, 07:28:11Z) | none (`gate_present` = path exists) |
| **C1** | **gate keyed on `naive-counter.py`/`mini-counter.py` in `config["counter"]["argv"]`; literal verdicts** | **+16/−1** | **all scoring; zero spawns** | `GATE_COUNTER_OK` | **OK, exit 0** (`gate-name-sniff`, 07:28:15Z); CLEAN/REFUSED with `mini-fix/` **deleted** (07:35:20Z) | none |
| C1b | C1 + emit the seven registry-shaped rows | +18/−1 | all scoring; receipt field-identical to production | `GATE_COUNTER_OK` | **OK**; identical to committed receipt except `gate_path` (`lane-c1b-mimic`, 07:32:45Z) | none |
| C2 | red keyed on the naive counter; green runs **only** the structural positive control | +19/−1 | the 7 shortcut scores | `GATE_COUNTER_OK` | **OK**, `below=0` (`gate-structural-only`, 07:28:16Z; lane 07:32:46Z) | none (row-count assert would) |
| C3 | three-line red fake; green honest | +10/−1 | the refusal demonstration | `GATE_COUNTER_OK` | **OK**, `below=7` (`gate-red-fake-only`, 07:28:17Z) | none |
| C4 | gate replays the committed control receipts' verdicts | ~+10 | everything | `GATE_COUNTER_OK` | not run (identical constant source to C1: three of five committed control receipts already carry `red=REFUSED`) | none |

No-spawn proof (mini-fix tree removed from the root; 2026-10-25T07:35:20Z):

| probe | exit | line |
|---|---|---|
| honest gate, green | 3 | `REPLAY_GATE_UNEVALUABLE finding=positive_control_absent` |
| C1 green | 0 | `REPLAY_GATE_CLEAN … shortcuts_below_target=0` |
| C1 red | 2 | `REPLAY_GATE_REFUSED … classes_over_target=label-memorization` |
| C1b green | 0 | `REPLAY_GATE_CLEAN … shortcuts_below_target=7` |
| C2 green | 3 | `REPLAY_GATE_UNEVALUABLE finding=counter_receipt_unreadable` |
| C3 green | 3 | `REPLAY_GATE_UNEVALUABLE finding=positive_control_absent` |

So C1/C1b run nothing at all; C2 runs exactly one artifact (the structural reader) and never a
registered shortcut; C3 keeps green honest but asserts the refusal.

## 4. Why the five committed controls do not cover this

`diff` against the pinned gate (2026-10-25T07:34Z): `gate-always-clean.py` = one line
(`if over:` → `if False:`), `gate-no-positive-check.py` = one line (MUT-C), `gate-vacuous-no-floor.py`
= one line (MUT-A), `gate-junk-clean.py` = an 11-line standalone stub. Four of five are
single-branch mutants of the **honest** function; the fifth is a fixed-CLEAN stub. None varies the
red/green discriminator (the counter argv), which is the only channel that distinguishes the two
cases. 5/5 MISS measures agreement on the four branches the author chose to mutate — it is not
evidence that a gate of this shape cannot skip the work.

## 5. Impacted axes

- **depth (primary).** The clause set does not entail the predicate. The predicate says shortcut
  readers *are scored under the counter's own predicate*; C1/C1b/C0e satisfy all six clauses with
  zero readers scored. The claim's evidence and its predicate are decoupled.
- **calibration.** `selftest_clean`/`mutants_killed` are self-attested by the blob under test, and
  the selftest's argv never matches production's, so the calibration measures a different code path.
- **coverage.** The class roster is a config constant; the gate cannot tell a dropped class from a
  scanned one (already disclosed as F3), and it cannot tell a scored class from an invented row
  (this report).
- No score change is proposed; owned axes stay 10→10 as the landed stop records.

## 6. Smallest safe correction

Additive instrument; **no frozen bytes touched** (kill rule keeps the six clauses, target, counter,
predicate and labels intact). The verifier must be the producer or re-deriver of the verdicts, and
must read pins/blobs from the **git object store at the measured rev**, never from the worktree or
from a caller-supplied `--root` (C0e forges both).

Draft: `tools/round-34/c2-bound-receipt.py` (new file; L1 lands it; pin its digest in the wave's
evidence container, not in the frozen `claims.json`).

```python
#!/usr/bin/env python3
"""Bind an R34-C2 receipt to the lane's git objects at the measured rev and re-derive
the red/green verdicts counter-side. Additive: no frozen instrument is edited."""
import argparse, hashlib, json, subprocess, sys, tarfile, tempfile, io
from pathlib import Path

GATE = "tools/round-34/replay-gate.py"
CONFIGS = {"red": "tools/round-34/gate-config-naive.json",
           "green": "tools/round-34/gate-config-mini.json"}
PINS = ".ufo/waves/round-34/r34b/instruments.json"   # enforced 26-pin container (F1 repair)

def git(repo, *args, data=False):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("git fail: " + " ".join(args))
    return r.stdout if data else r.stdout.decode()

def blob(repo, rev, path):
    return git(repo, "show", f"{rev}:{path}", data=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True); ap.add_argument("--rev", required=True)
    ap.add_argument("--receipt", required=True); ap.add_argument("--json-out")
    a = ap.parse_args()
    repo = Path(a.repo).resolve()
    commit = git(repo, "rev-parse", "--verify", a.rev + "^{commit}").strip()   # fabricated rev dies here
    pins = json.loads(blob(repo, commit, PINS))["instruments"]
    checks = {}
    # 1. executed gate must be the pinned blob at the rev (kills C0/C0e/C1/C1b/C2/C3/C4)
    gate_blob = blob(repo, commit, GATE)
    checks["gate_is_pinned_blob"] = hashlib.sha256(gate_blob).hexdigest() == pins[GATE]
    checks["configs_are_pinned"] = all(
        hashlib.sha256(blob(repo, commit, p)).hexdigest() == pins[p] for p in CONFIGS.values())
    receipt = json.loads(Path(a.receipt).read_text())
    checks["receipt_names_pinned_gate"] = receipt.get("gate_path") == GATE
    checks["receipt_rev_is_commit"] = receipt.get("measured_revision") == commit
    # 2. re-derive both verdicts from the tree at the rev, counter-side (no gate participation)
    with tempfile.TemporaryDirectory(prefix="c2-bound-") as work:
        subprocess.run(f"git -C {repo} archive {commit} tools/round-34 | tar -x -C {work}",
                       shell=True, check=True)
        derived = {}
        for kind, rel in CONFIGS.items():
            cfg = json.loads((Path(work) / rel).read_text())
            argv_t = cfg["counter"]["argv"]
            rows = []
            for spec in [cfg["positive_control"]] + cfg["shortcuts"]:
                reader = str(Path(work) / spec["path"])
                argv = [part.replace("{reader}", reader) for part in argv_t]
                out = subprocess.run(argv, cwd=work, capture_output=True, text=True,
                                     env={"PATH": "/usr/bin:/bin", "HOME": work, "LANG": "C"})
                payload = json.loads(out.stdout.strip().splitlines()[-1])
                rows.append({"class": spec["class"], "matched": payload["matched"],
                             "met_target": payload["met_target"]})
            derived[kind] = rows
    green = derived["green"]; red = derived["red"]
    checks["green_positive_meets_target"] = green[0]["matched"] == 8
    checks["green_all_shortcuts_below"] = all(not r["met_target"] for r in green[1:])
    checks["green_registers_all_seven"] = len(green) == 8
    checks["red_label_memorization_meets"] = any(
        r["class"] == "label-memorization" and r["met_target"] for r in red)
    checks["receipt_rows_match_derivation"] = (
        sorted((r["class"], r["met_target"]) for r in green) ==
        sorted((r["class"], r["met_target"]) for r in receipt["green"].get("rows", [])))
    ok = all(checks.values())
    out = {"rev": commit, "checks": checks, "met": ok, "derived": derived,
           "receipt": str(Path(a.receipt).resolve())}
    if a.json_out:
        Path(a.json_out).write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(("C2_BOUND_OK" if ok else "C2_BOUND_MISS") +
          " failed=" + (",".join(sorted(k for k, v in checks.items() if not v)) or "-"))
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
```

Effect table (what each check kills):

| check | C0/C0e | C1/C1b | C2 | C3 | C4 |
|---|---|---|---|---|---|
| `gate_is_pinned_blob` | killed | killed | killed | killed | killed |
| `configs_are_pinned` | killed | pass | pass | pass | pass |
| `receipt_rev_is_commit` | pass (rev reused) | pass | pass | pass | pass |
| independent re-derivation | killed | killed | killed | **killed** | killed |

The cheapest single check that closes this control class is `gate_is_pinned_blob` (one `git show`
+ one digest), **provided the pins are read from the rev and the blob is read from git**, not from
the root: C0e forges the worktree and would forge a worktree pin container too. The re-derivation
block is what makes the *predicate* (readers scored under the counter's own predicate) true rather
than asserted; it also subsumes the F3/F4 repairs (class-count drop, last-row mutant) because a
fabricated row set cannot reproduce per-reader `matched` values. Residual trust anchor: a rewritten
lane object DB with a self-consistent pin container; that is freeze-integrity's job at the rev, not
this instrument's.

Rejected repairs (insufficient alone): recording `root`/`argv` in the receipt (C0e forges them);
adding a `green.shortcuts_below_target == 7` clause (C1b fabricates 7 in five lines — observed);
adding a green row-count assertion (kills C2 only; C1b emits 8 rows); a "red-last selftest case"
(F4's route; the cheat lives in the dispatch, not in a row).

## 7. Evidence

Scratch root: `/fast/scratch/hyaku/kaidoku-r34b/w1/CritControlAdequacy/`
(`lane-copy/` = `cp -a tools/round-34`; `synthetic/`, `synthetic2/`, `no-minifix/`;
`candidates/`; `receipts/`).

Commands (all from that scratch root unless noted; `C=<lane>/tools/round-34/c2-shortcut-gate-counter.py`,
`REV=c79bbe7b0959132b9873ff3431cf5eb313b58b33`):

```
python3 -I -B $C --root lane-copy  --rev $REV --json-out receipts/p0-baseline.json        # exit 0, 07:28:09Z
python3 -I -B $C --root synthetic  --rev $REV --json-out receipts/p1-synthetic-root.json  # exit 0, 07:28:11Z
python3 -I -B $C --root lane-copy  --rev $REV --gate candidates/gate-name-sniff.py \
        --json-out receipts/gate-name-sniff.json                                          # exit 0, 07:28:15Z
python3 -I -B $C --root lane-copy  --rev $REV --gate candidates/gate-structural-only.py \
        --json-out receipts/gate-structural-only.json                                     # exit 0, 07:28:16Z
python3 -I -B $C --root lane-copy  --rev $REV --gate candidates/gate-red-fake-only.py \
        --json-out receipts/gate-red-fake-only.json                                       # exit 0, 07:28:17Z
python3 -I -B $C --root <LANE>     --rev $REV --gate candidates/gate-name-sniff-mimic.py \
        --json-out receipts/lane-c1b-mimic.json                                           # exit 0, 07:32:45Z
python3 -I -B $C --root <LANE>     --rev $REV --gate candidates/gate-structural-only.py \
        --json-out receipts/lane-c2-structural-only.json                                  # exit 0, 07:32:46Z
python3 -I -B $C --root synthetic2 --rev $REV --json-out receipts/p2-synthetic-exact.json # exit 0, 07:35:04Z
cmp receipts/p2-synthetic-exact.json <LANE>/.ufo/waves/round-34/r34b/after/c2-at-instruments.json
        # IDENTICAL_BYTES
python3 -I -B $C --root lane-copy  --rev NOT-A-REVISION-0xF00D \
        --json-out receipts/p5-freetext-rev.json                                          # exit 0, 07:29Z
```

`p0-baseline.json` sha256 `da78f44419ecf83935e1fe6b1cd72f611c5a0e7e03029e97580d515a0796f3e9`
equals the committed production receipt's digest — my harness reproduces the frozen result, so the
negative probes are not harness artefacts. `p2` has the same digest. Candidate digests:
`gate-name-sniff.py 6fd20675…`, `gate-name-sniff-mimic.py 330630e0…`,
`gate-structural-only.py 8f356f26…`, `gate-red-fake-only.py bbb76339…`,
`gate-synthetic-exact.py 610b4b02…`, `gate-synthetic-stub.py 5f1f5c51…`.
No ELF carrier, reader-as-program or fixture was executed as a program; readers ran only as python
under the counters, and the `mini-fix` tree was deleted in the no-spawn probes.

## 8. Verdict

**R34-C2 control set is inadequate, and the defect is not a clause-tuning defect: the six frozen
clauses are satisfiable — byte-for-byte — by a 16-line counter-name-keyed gate that runs no reader
(C1/C1b), and by a 3-file synthetic root with a 39-line stub that runs nothing at all (C0e,
`cmp` IDENTICAL). Cheapest uncaught control = C1; cheapest receipt-level skip = C0e. The claim is
already stopped at `cd75b92e` for the unregistered-class reason, so no new stop is proposed; the
required repair is a new counter-side bound-receipt verifier that reads pins and blobs from the git
object at the measured rev and re-derives both verdicts itself (`§6`), not a seventh clause, a
row-count assertion, or a recorded `root`/`argv`.**
