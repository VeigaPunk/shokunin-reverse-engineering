# ExecBaseArm — independent re-derivation of R79-C1's base arm

Seat: ExecBaseArm (leaf). Scope: the **base** arm only. The freeze arm is not
re-derived, re-measured or judged here. No lane file was edited; git was read-only
(`show`, `cat-file -s`).

## What was built

`mutate.py` (this dir) is an independent applier/parser/judge. It **never imports
and never executes** `tools/round-79/gate-mutation.py`. The eight frozen mutant
definitions are read as *data* — an `ast.literal_eval` of the `MUTANTS`
assignment in the tool blob at the freeze `ed68cd0a` — and are additionally
compared byte-for-byte against a hand transcription typed into `mutate.py`
(`TRANSCRIBED`). If the two disagree, or if any typed anchor does not occur
exactly once in the base blob, the arm is **unevaluable** (exit 2) rather than
scored. At this run: `mutant_table_cross_check.agree = true`, 8 entries,
0 mismatches.

Applier rules (own implementation):

- exactly one occurrence of the anchor, else **REFUSED** (never applied);
- a replacement identical to its anchor is refused as a no-op;
- a mutant is **KILLED** only when its declared case is *present* in the mutated
  copy's `--selftest` output **and fails** there;
- an **absent** declared case is a **SURVIVOR**, never a pass;
- a copy without a `SELFTEST cases=N failures=M` line is INCONCLUSIVE.

Execution: each copy is written to scratch and run as
`python3 -I -B <copy> --selftest` with cwd = the scratch run root, a 300 s
timeout, and an env whitelist of `HOME`, `LANG`, `PATH`, `TMPDIR` (TMPDIR set to
the seat scratch). Interpreter: Python 3.14.8. No network, no writes outside the
seat scratch and this evidence dir.

## Measured base arm — 29d2ca30b83a6a0d85b0aa979de0138fde1660e6

Target `tools/round-78/attack-gate.py`: 44856 bytes,
sha256 `961d5a23c1d38116f5b992434fa2295b5a90643b4a52233e205837ac73bf48c0`
(distinct from the freeze pin `4e4baf00…`, as expected — the declaration changed
this file).

Pristine base selftest, verbatim:

```
SELFTEST cases=26 failures=0
```

exit 0, 26 case names parsed, zero failing.

| mutant | anchor hits | copy differs | exit | killed | declared case absent | detectors | sole |
|---|---|---|---|---|---|---|---|
| m01-auth-dead | 1 | yes | 1 | **yes** | no | 2 (`red-auth-no-instrument`, `red-receipt-auth`) | no |
| m02-qualified-atom-dead | 1 | yes | 1 | **yes** | no | 1 (`red-qualified-atom`) | yes |
| m03-near-miss-re-dead | 1 | yes | 0 | no | **yes** | 0 | no |
| m04-negation-dead | 1 | yes | 1 | **yes** | no | 1 (`red-negated`) | yes |
| m05-atom-absent-bound | 1 | yes | 0 | no | **yes** | 0 | no |
| m06-near-miss-stems-empty | 1 | yes | 1 | **yes** | no | 2 (`red-near-miss`, `red-near-miss-plural`) | no |
| m07-mode-ok-always | 1 | yes | 1 | **yes** | no | 2 (`red-mode-link`, `red-mode-tree`) | no |
| m08-validate-no-refusal-guard | 1 | yes | 0 | no | **yes** | 0 | no |

Counts: `mutants_total 8`, `killed 5`, `survivors 3`.
Killed ids: `m01-auth-dead`, `m02-qualified-atom-dead`, `m04-negation-dead`,
`m06-near-miss-stems-empty`, `m07-mode-ok-always`.
Survivor ids: `m03-near-miss-re-dead`, `m05-atom-absent-bound`,
`m08-validate-no-refusal-guard`.

## Survivors are absent, not merely passing

The three survivors' declared cases do not exist anywhere in the base gate:
the pristine base case list is 26 names and contains none of
`red-near-miss-unparsed`, `red-atom-absent`, `red-validate-refused-no-reason`.
Their mutated copies print `SELFTEST cases=26 failures=0` at exit 0 — identical
shape to pristine. So each survivor is a *defect with no detector at all*, which
is exactly the round-78 population the freeze closes: `m03` and `m08` are the two
round-78 wave survivors, `m05` the uncovered atom-absent conjunct.

## Refusal control (does not apply an anchor twice)

| control case | intent | hits | outcome |
|---|---|---|---|
| `source-with-two-anchors` | literal duplicate anchor in the source text | 2 | **REFUSED**: "anchor occurs 2 times, want exactly 1" |
| `reapply-consumed-anchor` (m02) | re-apply an edit that consumed its anchor | 0 | **REFUSED**: "anchor occurs 0 times, want exactly 1" |
| `anchor-absent` | text containing no anchor | 0 | **REFUSED**: "anchor occurs 0 times, want exactly 1" |
| `reapply-embedding-anchor` (m01) | informational | 1 | applies again — **by design**, see note |

The fourth case is recorded rather than hidden: m01's replacement re-emits its own
anchor verbatim, so its anchor still occurs exactly once after the edit and a
second application is a legitimate second insertion, not a duplicate. It is marked
`informational` and excluded from `all_refused`; the hit count, not an
"already-applied" flag, decides. All three genuine refusal checks refused.

## Independent agreement with the claimant's base receipt

Mutant-by-mutant compare against `.ufo/waves/round-79/pre/c1-at-base.json`:
`killed`, `case_absent` and the exact `failed_cases` sets agree for **all 8**
mutants; totals agree (8 / 5 / 3) and the survivor list is identical. This is
reproduction by a second implementation, not a re-read of their numbers.

## Receipt

`base-arm-receipt.json` in this directory: `base` (rev, bytes, sha256, selftest
summary and 26 case names, mutants, killed/killed_ids, survivor/survivor_ids,
`declared_case_absent_ids`, `declared_case_absent_in_pristine_ids`),
`mutants_frozen_at`, `mutant_table_cross_check`, `refusal_control`, and
`reproduces_expected_base_arm: true`. Runner exit 0.

## Risks / limits

- The mutant table is parsed from the freeze blob as data (allowed by the seat);
  the hand-transcription cross-check is what makes a parser/transcription error
  loud instead of silent. It passed byte-for-byte.
- The base arm is measured on Python 3.14.8; the claim is about this interpreter
  on this host. No claim is made about other interpreters.
- `m01`, `m06`, `m07` are killed by two detectors, not one. That does not affect
  the frozen predicate (which asks that each declared case be present and fail);
  at the freeze the claimants additionally require `m03`/`m05`/`m08` to be each
  the sole failing case — a freeze-arm property this seat did not measure.
- This seat proves the base arm only. Whether the freeze arm reaches 8/8 is not
  asserted here.

## Tooling

No tool was installed or upgraded. Python 3.14.8 (system) used as-is; no pacman
transaction was attempted.
