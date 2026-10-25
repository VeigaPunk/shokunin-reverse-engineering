# CritControlAdequacy — R34-C2 control adequacy (round 34, run-6 re-dispatch, wave 1)

Seat: `L1Kaidoku34-2.CritControlAdequacy`. Scope: name the cheapest control that still skips the
claimed work and is not among the five committed controls; predict each candidate's counter verdict
from the code; say whether the frozen clauses catch it. Read-only on lane VCS; every probe ran from
`/fast/scratch/hyaku/kaidoku-r34b/w1/CritControlAdequacy/` on copies. No tool installed or upgraded
(`python3 3.14.8`; no `uv`/`npx`/pacman transaction).

## 0. State observed before analysis (read this first)

- Frozen blobs unchanged: I read `tools/round-34/replay-gate.py`, `c2-shortcut-gate-counter.py`,
  both configs and `mini-fix/**` at worktree and at `c79bbe7b0959132b9873ff3431cf5eb313b58b33`;
  digests equal (`git show <rev>:<path> | sha256sum` == `sha256sum <worktree>` for both
  instruments). All 26 pins in `claims.json` match the worktree (`pinned=26 mismatched=0`,
  2026-10-25T07:29Z).
- The lane advanced under this wave: tip is now `66b840274390d0868c913a544947f9eb40a4ffe6`, and
  `cd75b92e` already **stopped R34-C2** on an unregistered content-multiset shortcut. I reopened,
  rescored and relabelled nothing; this report attacks the **control set / evidence chain**, which
  the stop reasoning does not cover. No new stop is proposed — the claim is already stopped.
- `LOG.md:3099` already discloses in prose that "a 1,979-byte gate that runs no reader satisfies all
  six clauses". This report names the cheapest instance, proves the receipt can be reproduced
  **byte-for-byte**, and shows that the repair routes listed in `claim-stop.json` (F1–F5) do not
  close the class.

## 1. Answer

**Cheapest uncaught control: C1 — a gate that keys on the counter's own module name and returns
literal verdicts.** Delta to the pinned gate: **+16 / −1 lines** (one rename, one dispatch block);
the production path spawns **nothing**. Observed `GATE_COUNTER_OK`, all six clauses, exit 0
(`receipts/gate-name-sniff.json`, 2026-10-25T07:28:15Z). Strictest form (C1b, +18/−1) fabricates
the seven registry rows, so its receipt equals the committed production receipt on **every field the
six clauses read** (`clauses/finding/met_target/exit/selftest_failures/mutants_killed/
green.positive_matched/green.shortcuts_below_target/red.classes_over_target`, and `green.line`) —
`receipts/lane-c1b-mimic.json` differs only in `gate_path` and in the red line's cosmetic
`shortcuts_below_target=0`, a string no clause reads (C0e below removes even that difference).

**Cheaper still, and not a gate control at all (C0e): the counter never records or validates
`--root`.** A three-file synthetic root (`tools/round-34/{replay-gate.py,gate-config-mini.json,
gate-config-naive.json}`) holding a 2,242-byte stub that executes no reader, no counter and no
fixture produced a receipt **byte-identical** to the committed production receipt — both
`sha256 = da78f44419ecf83935e1fe6b1cd72f611c5a0e7e03029e97580d515a0796f3e9`
(`cmp` → `IDENTICAL_BYTES`, 2026-10-25T07:35:04Z). `gate_path` reads
`tools/round-34/replay-gate.py`; `measured_revision` echoes the requested rev. No field is left to
distinguish it.

## 2. Mechanism — why every candidate below is invisible to the frozen clauses

1. **The two configs differ in exactly one token** (verified by JSON compare): `counter.argv[3]` is
   `mini-counter.py` vs `naive-counter.py`. `positive_control`, `predicate`, `schema`, `shortcuts`
   and `target` are identical. The only signal a gate can key on is the counter module name — which
   makes the key cheaper, not harder. (The brief's "reads the red case's fixture names" idea cannot
   work here: both configs name the same eight fixtures and the same seven readers.)
2. **The gate's selftest never uses the production argv.** `replay-gate.py:185-202` (`config_for`)
   builds every selftest config with `[sys.executable, "-I", "-B", str(root/"counter.py"),
   "--control-reader", "{reader}"]` (lines 189-190). A production-only branch keyed on
   `mini-counter.py`/`naive-counter.py` is exercised by **zero** of the 12 selftest cases, and the
   three registered mutants (MUT-A/C/D, `replay-gate.py:165-171`) mutate branches the cheat does not
   use. `selftest_clean` and `mutants_killed` therefore certify the honest function, not the
   dispatch production hits.
3. **All six clauses read the gate's self-report.** `c2-shortcut-gate-counter.py:112-119`:
   `selftest_clean`/`mutants_killed` read the gate's own `--selftest` JSON; `red_refused` reads
   `red.exit/red.verdict` plus `"label-memorization" in red_classes`; `green_clean` reads
   `green.exit/green.verdict`; `green_positive_meets_target` reads one green row `matched == 8`;
   `gate_present` is `(root/args.gate).is_file()` (line 74), then hardcoded `True` (line 119).
4. **`shortcuts_below_target` is computed (line 109) but is not in `clauses`.** C2 (below=0) and C1b
   (below=7) both pass; C1b fabricates the seven rows from `config["shortcuts"]` in five lines.
5. **No provenance exists to bind otherwise.** The receipt has no `root` and no instrument digest;
   `measured_revision` is `args.rev` verbatim (line 73) — `--rev NOT-A-REVISION-0xF00D` printed
   `GATE_COUNTER_OK` with `measured_revision: "NOT-A-REVISION-0xF00D"`
   (`receipts/p5-freetext-rev.json`, 07:29Z). The counter never reads `claims.json` and never hashes
   the gate or configs (`grep -n hashlib tools/round-34/c2-shortcut-gate-counter.py` → none), and
   `--gate` is a documented control escape hatch (lines 69-70). C0e needs neither: it uses the
   **default** gate path in a fake root.

## 3. Candidates (predicted from code; *observed* = run)

| # | Control | Cost | Work skipped | Predicted verdict | Observed | Frozen clause that catches it |
|---|---------|------|--------------|-------------------|----------|-------------------------------|
| C0e | stub gate at the default path in a synthetic root; prints the production lines, spawns nothing | 47 lines / 3 files | everything | `GATE_COUNTER_OK` | **OK, receipt byte-identical** (`p2`, 07:35:04Z) | none |
| C0 | stub gate keyed on config basename in a synthetic root | 39 lines / 3 files | everything | `GATE_COUNTER_OK` | **OK**, exit 0 (`p1`, 07:28:11Z) | none (`gate_present` = path exists) |
| **C1** | **gate keyed on `naive-counter.py`/`mini-counter.py` in `config["counter"]["argv"]`; literal verdicts** | **+16/−1** | **all scoring; zero spawns** | `GATE_COUNTER_OK` | **OK, exit 0** (`gate-name-sniff`, 07:28:15Z); still CLEAN/REFUSED with `mini-fix/` **deleted** (07:35:20Z) | none |
| C1b | C1 plus the seven registry-shaped rows | +18/−1 | all scoring; claused fields identical to production | `GATE_COUNTER_OK` | **OK**; equals the committed receipt on every claused field and `green.line`; differs only in `gate_path` and the red line's unread below-count (`lane-c1b-mimic`, 07:32:45Z) | none |
| C2 | red keyed on the naive counter; green runs **only** the structural positive control | +19/−1 | the seven shortcut scores | `GATE_COUNTER_OK` | **OK**, `below=0` (`gate-structural-only`, 07:28:16Z; lane 07:32:46Z) | none |
| C3 | three-line red fake; green honest | +10/−1 | the refusal demonstration | `GATE_COUNTER_OK` | **OK**, `below=7` (`gate-red-fake-only`, 07:28:17Z) | none |
| C4 | gate replays the committed control receipts' verdicts | ~+10 | everything | `GATE_COUNTER_OK` | not run; same constant source as C1 (two of the five committed control receipts already carry `red=REFUSED`) | none |

No-spawn proof (the `mini-fix` tree deleted from the root; 2026-10-25T07:35:20Z):

| probe | exit | line |
|---|---|---|
| honest gate, green | 3 | `REPLAY_GATE_UNEVALUABLE finding=positive_control_absent` |
| C1 green | 0 | `REPLAY_GATE_CLEAN … shortcuts_below_target=0` |
| C1 red | 2 | `REPLAY_GATE_REFUSED … classes_over_target=label-memorization` |
| C1b green | 0 | `REPLAY_GATE_CLEAN … shortcuts_below_target=7` |
| C2 green | 3 | `REPLAY_GATE_UNEVALUABLE finding=counter_receipt_unreadable` |
| C3 green | 3 | `REPLAY_GATE_UNEVALUABLE finding=positive_control_absent` |

C1/C1b execute nothing at all; C2 executes exactly one artifact (the structural reader) and never a
registered shortcut; C3 keeps green honest but asserts the refusal.

## 4. Why the five committed controls do not cover this

`diff` against the pinned gate (2026-10-25T07:34Z): `gate-always-clean.py` is one line
(`if over:` → `if False:`), `gate-no-positive-check.py` one line (MUT-C), `gate-vacuous-no-floor.py`
one line (MUT-A), `gate-junk-clean.py` an 11-line standalone stub. Four of five are single-branch
mutants of the **honest** function; the fifth is a fixed-CLEAN stub. None varies the red/green
discriminator (the counter argv), the gate blob or the root. 5/5 MISS measures agreement on the four
branches the author chose to mutate; it is not evidence that a gate of this shape cannot skip the
work.

## 5. Impacted axes

- **depth (primary).** The clause set does not entail the predicate. The predicate says shortcut
  readers *are scored under the counter's own predicate*; C1/C1b/C0e satisfy all six clauses with
  zero readers scored. Evidence and predicate are decoupled.
- **calibration.** `selftest_clean`/`mutants_killed` are self-attested by the blob under test, and
  the selftest's argv never matches production's, so calibration measures a different code path.
- **coverage.** The class roster is a config constant: the gate cannot tell a dropped class from a
  scanned one (disclosed as F3) nor a scored class from an invented row (this report).
- No score change is proposed; owned axes stay 10→10 as the landed stop records.

## 6. Smallest safe correction

**Impossibility first.** C0e's receipt is byte-identical to the production receipt, so no post-hoc
field check can bind it. Recording `root`/`argv` in the receipt, adding a
`shortcuts_below_target == 7` clause, or asserting a green row count are all forgeable in the same
47 lines (C1b already emits seven rows; C0e already emits the right counts). The defect is the
evidence chain: the receipt is produced by the object under test and scored by a counter that reads
only that self-report, with the tree and the gate supplied by the caller.

**Correction (additive; no frozen byte touched; kill rule intact).**

1. A new pinned verifier-*producer* emits the receipt of record. It derives everything from the
   lane's git objects at the measured rev: extract `tools/round-34` at the rev, hash the bytes it is
   about to run, execute the pinned gate and both configs from that extraction, and independently
   re-derive every reader row by invoking the config's own counter argv. One receipt carries
   `tree_sha256`, the executed blobs' digests, the verifier's own digest, argv/cwd/UTC, the gate
   verdicts, and the derived rows; `met` requires (class, matched, met_target) agreement on **both**
   configs.
2. The six clauses stay exactly as frozen. The candidates in §3 become control gates that must MISS;
   they do, because none is in the producer's execution path.
3. Pin the producer digest in the wave's evidence envelope (not in frozen `claims.json`) and make the
   L1 run it in the lane; any other receipt is not evidence.

Tested file: `/fast/scratch/hyaku/kaidoku-r34b/w1/CritControlAdequacy/candidates/c2-bound-receipt.py`
(sha256 `ef1963ecf8810565fad5d17570472a2b8b2e2e26ea3f5f78cd0962f1689807c1`), run at
2026-10-25T07:42:59Z → `C2_BOUND_OK failed=-`, exit 0, `tree_sha256 e6bed50bf38a60c8…`:

```python
#!/usr/bin/env python3
"""Produce (and verify) the R34-C2 receipt from the lane's git objects at the measured rev.

Additive: no frozen instrument is edited. The receipt this emits is evidence of what
*this* process executed -- the pinned subtree extracted from `rev`, hashed before it ran,
and re-derived per reader counter-side -- not of what a gate reported about itself.
"""
import argparse
import hashlib
import io
import json
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path

GATE = "tools/round-34/replay-gate.py"
CONFIGS = {"red": "tools/round-34/gate-config-naive.json",
           "green": "tools/round-34/gate-config-mini.json"}
CLAIMS = ".ufo/waves/round-34/r34b/claims.json"
SUBTREE = "tools/round-34"


def git(repo, *args):
    run = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    if run.returncode != 0:
        raise SystemExit("git fail: " + " ".join(args) + " :: " + run.stderr.decode()[:200])
    return run.stdout


def sha(data):
    return hashlib.sha256(data).hexdigest()


def manifest(root):
    rows = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            rows.append((str(path.relative_to(root)), sha(path.read_bytes())))
    return sha(json.dumps(rows, sort_keys=True).encode()), dict(rows)


def derive(work, kind):
    config = json.loads((work / CONFIGS[kind]).read_text())
    rows = []
    for spec in [config["positive_control"]] + config["shortcuts"]:
        reader = str(work / spec["path"])
        argv = [part.replace("{reader}", reader) for part in config["counter"]["argv"]]
        run = subprocess.run(argv, cwd=work, capture_output=True, text=True,
                             env={"PATH": "/usr/bin:/bin", "HOME": str(work), "LANG": "C"})
        payload = json.loads(run.stdout.strip().splitlines()[-1])
        rows.append({"class": spec["class"], "matched": payload["matched"],
                     "met_target": payload["met_target"]})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--rev", required=True)
    parser.add_argument("--receipt", help="compare against an existing counter receipt")
    parser.add_argument("--json-out")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    commit = git(repo, "rev-parse", "--verify", args.rev + "^{commit}").decode().strip()
    pins = json.loads(git(repo, "show", f"{commit}:{CLAIMS}"))["claims"][0]["pins"]
    checks = {}
    with tempfile.TemporaryDirectory(prefix="c2-bound-") as work:
        work = Path(work)
        tarfile.open(fileobj=io.BytesIO(git(repo, "archive", commit, SUBTREE))).extractall(work)
        tree_digest, files = manifest(work)
        executed = {rel: files[rel] for rel in (GATE, *CONFIGS.values())}
        checks["executed_blobs_are_pinned"] = all(executed[rel] == pins[rel] for rel in executed)
        rows = {kind: derive(work, kind) for kind in CONFIGS}
        # the pinned gate's own verdicts, run from the same extracted tree
        gate_out = work / "gate.json"
        verdicts = {}
        for kind, rel in CONFIGS.items():
            run = subprocess.run([sys.executable, "-I", "-B", str(work / GATE), "--root",
                                  str(work), "--config", str(work / rel), "--json-out",
                                  str(gate_out)], cwd=work, capture_output=True, text=True)
            verdicts[kind] = {"exit": run.returncode, "line": run.stdout.strip().splitlines()[-1],
                              "payload": json.loads(gate_out.read_text())}
            gate_out.unlink()
    green, red = rows["green"], rows["red"]
    checks["green_positive_meets_target"] = green[0]["matched"] == 8
    checks["green_registers_eight"] = len(green) == 8
    checks["green_all_shortcuts_below"] = all(not row["met_target"] for row in green[1:])
    checks["red_label_memorization_meets"] = any(
        row["class"] == "label-memorization" and row["met_target"] for row in red)
    checks["gate_refuses_red"] = (verdicts["red"]["exit"] == 2
                                  and verdicts["red"]["payload"]["verdict"] == "REPLAY_GATE_REFUSED")
    checks["gate_clears_green"] = (verdicts["green"]["exit"] == 0
                                   and verdicts["green"]["payload"]["verdict"] == "REPLAY_GATE_CLEAN")
    def shape(rows):
        return [(r["class"], r["matched"], r["met_target"]) for r in rows]

    checks["gate_rows_agree_with_derivation"] = (
        shape(verdicts["green"]["payload"]["rows"]) == shape(green)
        and shape(verdicts["red"]["payload"]["rows"]) == shape(red))
    if args.receipt:
        old = json.loads(Path(args.receipt).read_text())
        checks["receipt_matches_reproduction"] = (
            old.get("green", {}).get("positive_matched") == green[0]["matched"]
            and old.get("green", {}).get("shortcuts_below_target") ==
            sum(1 for row in green[1:] if not row["met_target"])
            and sorted(old.get("red", {}).get("classes_over_target") or []) ==
            sorted(row["class"] for row in red if row["met_target"] and row["class"] != "structural"))
    ok = all(checks.values())
    receipt = {"schema": 1, "rev": commit, "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "verifier_sha256": sha(Path(__file__).read_bytes()), "argv": sys.argv,
               "cwd": str(Path.cwd()), "tree_sha256": tree_digest, "executed": executed,
               "checks": checks, "met": ok, "derived": rows,
               "gate_verdicts": {k: {"exit": v["exit"], "line": v["line"]} for k, v in verdicts.items()}}
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(receipt, indent=1, sort_keys=True) + "\n")
    print(("C2_BOUND_OK" if ok else "C2_BOUND_MISS")
          + " failed=" + (",".join(sorted(k for k, v in checks.items() if not v)) or "-"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
```

What each candidate loses (none of them is in the producer's execution path):

| candidate | why it cannot pass | decisive check |
|---|---|---|
| C0e, C0 | the producer never reads a caller root; a stub receipt has no `tree_sha256`/`derived`/`verifier_sha256` | receipt shape + `executed_blobs_are_pinned` |
| C1 | its green set has one row; the honest set has eight | `green_registers_eight`, `gate_rows_agree_with_derivation` |
| C1b | fabricated rows are all `matched: 0`; the honest `size-keyed` row is `matched: 1` | `gate_rows_agree_with_derivation` (matched level, both configs) |
| C2 | green rows = the positive control only; below-count 0 vs 7 | `green_registers_eight`, `green_all_shortcuts_below` |
| C3 | its red rows are two rows (`structural 8`, `label-memorization 8`); honest red has eight, with `size-keyed=1` | `gate_rows_agree_with_derivation` (red) |
| C4 | same falsified rows as C1 | as C1 |

Rejected repairs (each tested or falsified by C1b/C0e): recording `root`/`argv` in the receipt;
adding `green.shortcuts_below_target == 7` (C1b fabricates 7); a green row-count assertion (C1b emits
8; kills C2 only); a "red-last selftest case" (F4's route — the cheat is in the dispatch, not in a
row); hashing the worktree under `--root` (C0e forges the worktree, so hash the bytes extracted from
git). Note also that the F1 repair container `.ufo/waves/round-34/r34b/instruments.json` **does not
exist at the measured rev** (`git show c79bbe7b:.ufo/.../instruments.json` → `fatal: … exists on
disk, but not in 'c79bbe7b…'`, exit 1), so a rev-bound verifier must read `claims[0].pins` at the rev
as the draft does.

**Residual limit, stated honestly.** A fabricated producer receipt is not distinguishable by field
checks alone; what the correction removes is the *cheap* path (a 47-line stub producing byte-identical
JSON). Reproducing the producer's receipt now requires running the pinned bytes, and an independent
seat can confirm a receipt in one 4.2 s run (`C2_BOUND_OK`, same `tree_sha256` and `derived`).

## 7. Evidence

Scratch root `/fast/scratch/hyaku/kaidoku-r34b/w1/CritControlAdequacy/` (`lane-copy/` = `cp -a
tools/round-34`; `synthetic/`, `synthetic2/`, `no-minifix/`; `candidates/`; `receipts/`).
`C=<lane>/tools/round-34/c2-shortcut-gate-counter.py`, `REV=c79bbe7b0959132b9873ff3431cf5eb313b58b33`.

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
python3 -I -B candidates/c2-bound-receipt.py --repo <LANE> --rev $REV \
        --receipt <LANE>/.ufo/waves/round-34/r34b/after/c2-at-instruments.json \
        --json-out receipts/p6-bound-produce.json                                         # C2_BOUND_OK, exit 0, 07:42:59Z
```

`p0-baseline.json` sha256 `da78f44419ecf83935e1fe6b1cd72f611c5a0e7e03029e97580d515a0796f3e9`
equals the committed production receipt's digest, so my harness reproduces the frozen result and the
negative probes are not harness artefacts. `p2` carries the same digest. Honest derivation from the
rev's blobs (`p6`): green rows `structural 8 / all-false 0 / size-keyed 1 / fixed-slice 0 /
digest-keyed 0 / string-scan 0 / record-order-replay 0 / label-memorization 0`; red rows identical
except `label-memorization 8`. Candidate digests: `gate-name-sniff.py 6fd20675…`,
`gate-name-sniff-mimic.py 330630e0…`, `gate-structural-only.py 8f356f26…`,
`gate-red-fake-only.py bbb76339…`, `gate-synthetic-exact.py 610b4b02…`,
`gate-synthetic-stub.py 5f1f5c51…`, `c2-bound-receipt.py ef1963ec…`.
No ELF carrier, reader-as-program or fixture was executed as a program; readers ran only as python
under the counters, and the `mini-fix` tree was deleted in the no-spawn probes.

## 8. Verdict

**R34-C2's control set is inadequate, and the defect is not clause tuning: the six frozen clauses are
satisfiable — byte-for-byte — by a 16-line counter-name-keyed gate that runs no reader (C1/C1b), and
by a 3-file synthetic root with a 47-line stub that runs nothing at all (C0e, `cmp` IDENTICAL).
Cheapest uncaught control = C1; cheapest receipt-level skip = C0e. The claim is already stopped at
`cd75b92e` for the unregistered-class reason, so no new stop is proposed; the required repair is a
pinned verifier-producer that extracts, hashes, executes and re-derives from the git objects at the
measured rev and emits the receipt of record (`§6`, tested `C2_BOUND_OK` 07:42:59Z), not a seventh
clause, a row-count assertion, or a recorded `root`/`argv`.**
