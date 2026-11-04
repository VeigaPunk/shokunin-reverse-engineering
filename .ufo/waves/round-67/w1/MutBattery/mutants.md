# R67-C2 battery mutants — seat MutBattery (round 67, w1)

Instrument under test: `tools/round-67/mutation-battery.py`, frozen
sha256 `cabc0a0b6a47ca00d3e5c20e9795ba4c129b44a3c14a882d69f9c6b2534851ab`
(scratch copy `receipts/base/mutation-battery.py`, hash-identical).
Revision `a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92`. Pinned r66 counters
untouched: `closure-boundary.py` `3c5cfb03…1045b`, `coverage-selfcheck.py`
`1be9d046…55aa`.

Every mutant was built from the frozen bytes, written to
`/fast/scratch/hyaku/kaidoku-r67/MutBattery/mut/N*.py`, and driven through the
battery's own three modes against the real lane
(`--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev a7a4ce69…`), with
`--work`, `--out` and `TMPDIR` inside the scratch tree. Nothing was written to
the lane, `tools/`, `corpus/evidence/`, or any sibling seat.

## Baseline (pristine copy, same harness)

| mode | receipt | result | exit |
|---|---|---|---|
| `--selftest` | `receipts/base/BASE-selftest.json` | `SELFTEST CLEAN cases=9 failures=0` | 0 |
| `--score` | `receipts/base/BASE-score.json` | killed_before 0, survived_before 2, killed_after 2, verified true | 0 |
| `--control` | `receipts/base/BASE-control.json` | killed_before 0, survived_before 2, control_ok true | 0 |

`--score` per mutant: `closure-arm-true` fails `arm-false-bound`;
`coverage-equiv-true` fails `equiv-doctored-bound` + `equiv-doctored-diffs`;
both `before_selftest_exit 0`. This reproduces the committed before-arms
exactly (`.ufo/waves/round-67/l1/pre/selftest-c2.json` 9 cases,
`control-dryrun-c2.json` 0/2, `score-dryrun-at-base.json` killed_after 2,
verified). The baseline is green, so a red mutant result would be meaningful and
a green one is a survival.

## Result table

Uniform detectors = the battery's own `--selftest` **and** `--score` (plus
`--control`, the mode that owns the third mutated expression). "Caught" means the
mode exited non-zero, or an emitted field contradicts the frozen before-arm.

| mutant | defect (one hunk each) | sha256 | `--selftest` | `--score` | `--control` | caught | verdict |
|---|---|---|---|---|---|---|---|
| N1 | `EXPECTED_CASE` accepts any failing case name (`bool(failed_cases)`) | `ddb8fcca…513a8` | rc 0, 9 cases, 0 fail | rc 0, verified true, killed_after 2 | rc 0, 0/2 | no | **survived** |
| N2 | `killed_after` drops the case-name condition (`after_rc != 0` alone) | `84b6db28…d8824` | rc 0, 9 cases, 0 fail | rc 0, verified true, killed_after 2 | rc 0, 0/2 | no | **survived** |
| N3 | `control()` reports `survived_before` as killed | `049e7c8d…0420` | rc 0, 9 cases, 0 fail | rc 0, verified true, killed_after 2 | rc 0, **killed_before 2 / survived_before 0**, control_ok true | no (contradicts pinned before-arm only) | **survived** |
| N4 | `selftest()` drops the `equiv-doctored-diffs` case | `c51b3bbf…c2e28` | rc 0, **8 cases**, 0 fail | rc 0, verified true, killed_after 2 | rc 0, 0/2 | no (case count vs pinned 9 only) | **survived** |
| N5 | `score()` treats a missing `after_out` as a kill | `cdd3f989…0bbdab` | rc 0, 9 cases, 0 fail | rc 0, verified true, killed_after 2 | rc 0, 0/2 | no | **survived** |

No mutant is caught by any mode of the instrument. For N1, N2, N3 and N5 the
`--score` receipt is **byte-identical to the pristine receipt except
`counter.sha256`** (verified by JSON comparison with the self-hash masked); N4
differs only in the coverage mutant's `after_failed_cases` (diffs case gone) while
still reporting `killed_after 2`, `verified true`, exit 0.

Exact argv for every run: `receipts/commands.txt`; raw stdout/stderr with exit
codes: `receipts/logs/*.log`; mutant bytes: `receipts/N*/mutation-battery-N*.py`;
diffs: `receipts/diffs/*.diff`; machine summary: `receipts/summary.json`.

Because the battery has no seam for supplying a mutant set, three probes
substitute the *injector* functions in-process (monkeypatched module attributes)
and then run the frozen `score()`/`selftest()` code path against the real pinned
repo. They are probes, not CLI receipts, and are labelled as such.

---

## N1 — any failing case name counts as the kill

```diff
@@ -348,7 +348,7 @@
             "after_selftest_exit": after_rc,
             "after_failed_cases": failed_cases,
-            "killed_after": after_rc != 0 and EXPECTED_CASE[name] in failed_cases,
+            "killed_after": after_rc != 0 and bool(failed_cases),
```

Expected detector: the `--score` verdict (the only place `EXPECTED_CASE` is read).
Actual: `--selftest` rc 0 (9 cases), `--score` rc 0 verified true, `--control`
rc 0 — nothing fires, because the battery's own injected mutants fail exactly
the expected case, so `bool(failed_cases)` is true on the same runs that the
name match accepts.

Probe A (wrong-defect pair: `arm()→False`, `recipe_a_equivalence()→False`; the
after-detector then fails `arm-true-bound` and
`{equiv-honest-true, equiv-doctored-diffs}` — no expected case; both mutants
still survive their own r66 selftests, so `killed_before` stays 0):

| battery | killed_before | killed_after | verified | exit |
|---|---|---|---|---|
| pristine | 0 | 0 | false | 1 |
| **N1** | **0** | **2** | **true** | **0** |

N1 therefore issues a green R67-C2 certificate for a mutant pair whose declared
defects are untouched. Survival with a demonstrated false positive.

## N2 — `after_rc != 0` alone

```diff
-            "killed_after": after_rc != 0 and EXPECTED_CASE[name] in failed_cases,
+            "killed_after": after_rc != 0,
```

Expected detector: `--score`. Actual: identical to pristine on all three modes
(rc 0, verified true). Probe A: same false certificate as N1 (killed_after 2,
verified true, exit 0 vs pristine 0 / false / 1). Probe D (unimportable mutants,
no receipt written) shows N2 is strictly weaker than N1: it reports
`killed_after 2` where pristine reports 0
(`receipts/base/detectors.json`, `receipts/base/probes.json`). Survival; any
non-zero exit of the after-detector — including a crash-before-receipt — reads
as a kill.

## N3 — `control()` before/after swap

```diff
@@ -288,8 +288,8 @@
            "survivors_total": len(SURVIVORS),
-           "killed_before": len(verdicts) - survived,
-           "survived_before": survived,
+           "killed_before": survived,
+           "survived_before": len(verdicts) - survived,
            "verdicts": verdicts,
            "control_ok": survived == len(SURVIVORS)}
```

Expected detector: the `--control` receipt. Actual: `--control` exits **0** and
prints `killed_before 2`, `survived_before 0`, `control_ok true` — the exact
opposite of the claim's "the round-66 selftests alone leave both survivors alive
(0 of 2)" and of the committed before-arm `control-dryrun-c2.json`
(`killed_before 0`, `survived_before 2`). `--selftest` and `--score` do not call
`control()` and stay green. The instrument cannot catch its own swapped
before-arm; only a diff against the pinned receipt does. This is the
green-exit variant of the swap (the `control_ok`/exit fields are left computing
the true survivor count); the loud variant would exit 1 and be self-evident.

## N4 — dropped `equiv-doctored-diffs` case

```diff
-    check("equiv-doctored-diffs", bool(ok_d.get("recipe_a_diffs")), True)
```

Expected detector: `--selftest` case inventory. Actual: `--selftest` exits 0
printing `SELFTEST CLEAN cases=8 failures=0`; `--score` exits 0 with
killed_after 2 (the coverage mutant still trips `equiv-doctored-bound`, so the
kill survives the dropped assertion). Nothing inside the battery binds the case
count or the case list; the committed before-arm
(`selftest-c2.json`, 9 cases, `evidence.equiv_diffs = [coverage_score, mapped]`)
is the only thing that notices. Loss of the corroborating assertion: a
`recipe_a_equivalence` that refuses with an empty diff map is no longer
distinguished from one that refuses with a named mismatch.

## N5 — missing `after_out` treated as a kill

```diff
-            "killed_after": after_rc != 0 and EXPECTED_CASE[name] in failed_cases,
+            "killed_after": after_rc != 0 and (EXPECTED_CASE[name] in failed_cases
+                                               or not after_out.is_file()),
```

Expected detector: `--score` verdict. Actual: byte-identical `--score` receipt
to pristine apart from the self-hash; `--selftest` 9/0 rc 0; `--control` 0/2.

Reachability of the mutated branch: `selftest()` returns 1 without writing its
receipt only on the two early `could-not-evaluate` returns (instrument absent /
import failure). Probe D (both injected mutants made unimportable by appending a
syntax error) reaches it:

| battery | killed_before | killed_after | verified | exit |
|---|---|---|---|---|
| pristine | 2 | 0 | false | 1 |
| **N5** | 2 | **2** | false | 1 |

The verdict does not flip, because an unimportable mutant also fails the before
`run_selftest`, so `killed_before` is 2 and `verified` stays false. In every
reachable state I could construct, N5 inflates the `killed_after` field of an
already-red receipt rather than converting red to green. A crash variant (probe
C: `arm()` raises on a false condition) never reaches the mutated expression —
the exception escapes `score()` entirely (see F5). So N5 survives the detectors
with **masked** impact: no false certificate demonstrated, a lying field
demonstrated.

---

## Findings for the wave (disclosed gaps, not repairs)

- **F1 (N1, N2)** — the battery's `--score` verdict layer is unbound: no
  assertion anywhere tests that a mutant failing a *non-target* case is not
  counted as killed. Under probe A both mutants certify `verified true, exit 0`
  for a pair that leaves the declared defects in place. A green R67-C2
  certificate therefore says "the after-detector exited non-zero", not "the
  declared defect was killed" — unless the receipt's `after_failed_cases` is read
  case-by-case.
- **F2 (N3)** — `--control` can print the inverse before-arm with exit 0. The
  only detector is the pinned before-arm receipt; the control must not be
  regenerated from the instrument under test.
- **F3 (N4)** — the 9-case inventory is unbound; a dropped case passes as
  `cases=8` clean. Case-count binding is external (before-arm fixture) too.
- **F4 (N5)** — a missing after-receipt is accepted as a kill. Masked today by
  the pinned before-arm, but the `killed_after` field of a red receipt is not
  trustworthy evidence of a kill.
- **F5 (robustness, beyond the five mutants)** — `score()` does not wrap the
  after `selftest(...)` call. A counter that raises inside the battery's own
  checks (probe C: `arm()` raising on a false condition, the r66 shape where an
  invariant is asserted rather than returned) terminates the whole run with a
  traceback: process rc 1, **no receipt written at all**, not the documented
  `2 could-not-evaluate` (`receipts/logs/crash-cli.log`,
  `receipts/base/probes.json` probe C for all six copies). This is identical in
  the frozen bytes, so it is an instrument gap, not a mutant survival.
- **F6** — because N1/N2/N3/N5 produce byte-identical `--score` receipts modulo
  `counter.sha256`, the receipt's only self-identifying field is the hash of the
  battery that wrote it. Any consumer that does not pin
  `cabc0a0b…851ab` cannot tell a weakened battery from the frozen one.

None of these contradict the R67-C2 predicate on the frozen bytes: the pristine
instrument still reports killed_before 0 / killed_after 2 / verified true at
`a7a4ce69…`, and both real survivors are killed by the named cases. They are
limits on what that green receipt is evidence *of*.

## Restoration evidence

- Frozen `tools/round-67/mutation-battery.py` sha256 before and after the seat:
  `cabc0a0b6a47ca00d3e5c20e9795ba4c129b44a3c14a882d69f9c6b2534851ab`
  (unchanged; never opened for writing).
- `tools/round-66/closure-boundary.py` `3c5cfb038d86cdde03fb659e1d42a44ffa5f42ccd019ab7ea9b52710d071045b`
  and `tools/round-66/coverage-selfcheck.py` `1be9d046cea38a96a4b62d038f7dbc76e8ea611000af4aee3b91a6def86555aa`
  unchanged before/after (`receipts/hashes.txt`).
- Mutant bytes re-hashed after all runs; hashes match the ones built
  (`receipts/hashes.txt`), so every detector ran on the bytes reported here.
- Post-run check on the *actual frozen path* after every probe (scratch
  `receipts/post/`): `--score` rc 0, verified true, killed_before 0,
  killed_after 2, receipt self-hash `cabc0a0b…851ab`; `--selftest` rc 0,
  `SELFTEST CLEAN cases=9 failures=0`. The restored/pristine bytes behave
  exactly as the baseline.
- `git -C kaidoku-shokunin status --porcelain` shows no modification from this
  seat (only pre-existing round-67 untracked artefacts).
- Bytecode: every CLI run used `-I -B`. The in-process probes imported the
  frozen r66 counters by path *without* `-B`, which likely created the
  gitignored `tools/round-66/__pycache__/closure-boundary.cpython-314.pyc`
  (mtime 21:57:03, inside the probe window; the `__pycache__` directory at
  21:22:55 and `coverage-selfcheck.cpython-314.pyc` predate this seat). No
  source file under `tools/` was opened for writing, the pinned sha256 values
  are unchanged, and the cache is derived, gitignored and not load-bearing for
  any verdict. It was left in place because peer seats run the same instrument.
- Scratch `/fast/scratch/hyaku/kaidoku-r67/MutBattery` removed before yield;
  nothing under `/tmp` used.

## Limits

- Five mutants, as assigned; no statement about `fixture_repo`, `run_selftest`
  env handling, or the counters themselves was tested here.
- Probes A/C/D monkeypatch the injector functions to reach states the CLI
  cannot construct. They exercise the frozen `score()`/`selftest()` bodies and
  the real pinned counters; they are not CLI receipts and are not counted as
  such.
- Probe C is a stimulus outside the two declared round-66 survivors, used only
  to reach N5's branch and F5.
- No repair attempted: `tools/` is frozen, and a surviving mutant is a coverage
  finding.
