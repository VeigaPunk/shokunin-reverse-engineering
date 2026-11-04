# Seat MutInstruments — round 79, wave 1

Mutation-tests the two round-79 instruments' own `--selftest` suites: does any
conjunct of `pointer-bind.py` / `gate-mutation.py` survive a one-edit mutation
with every selftest case still green?

## Frozen inputs

| instrument | freeze path | sha256 | pristine selftest |
|---|---|---|---|
| pointer binder | `tools/round-79/pointer-bind.py@ed68cd0a` | `91d23dade98d831f8a709e50b8b9925ccb8930f74956993e058c143f24e80a90` | 16 cases, 0 failures, exit 0 |
| mutation battery | `tools/round-79/gate-mutation.py@ed68cd0a` | `682f1e7873dcc6ee47355c2cee3aa9359ef519ace6ef0eda5dd8f7135709c86d` | 11 cases, 0 failures, exit 0 |

Both digests equal `claims.json.instruments`. Both pristine suites were run
standalone and again inside the driver ahead of the mutants (same bytes, same
counts): the baseline is green, so every red result below is attributable to the
mutation.

## Method

`drive.py` copies each instrument from the freeze blob into scratch, asserts the
anchor occurs exactly once, applies the one edit, compiles the copy, runs
`python3 -I -B <copy> --selftest` with a restricted env and an explicit
`TMPDIR`, and reads the case JSON lines plus the `SELFTEST cases=… failures=…`
summary. `killed` = summary present and the run reports ≥1 failing case; a copy
that does not compile or prints no summary is `inconclusive`, never a kill. No
lane file was written.

## Mutants (10: the six required, four extra)

| id | instrument | one edit | exit | failures | killed | killed_by |
|---|---|---|---|---|---|---|
| `pb-a-path-only` (a) | pointer-bind | `bind()` returns `matched=True` as soon as the pointed path exists, before the range/token checks | 1 | 4 | yes | `green-range-digest`, `red-past-end`, `red-range-token-outside`, `red-stale-line` |
| `pb-b-zero-based` (b) | pointer-bind | pointed slice taken 0-based: `lines[start:end]` | 1 | 1 | yes | `green-line` (sole) |
| `pb-c-range-first-line` (c) | pointer-bind | range compared as its first line only: `lines[start-1:start]` | 1 | 1 | yes | `green-range` (sole) |
| `pb-d-unparsed-never` (d) | pointer-bind | `bind()` never sets `unparsed`: `out["unparsed"] = False` on the no-line branch | 1 | 1 | yes | `red-no-line` (sole) |
| `pb-e-validate-range-guard` | pointer-bind | `validate_receipt` drops the matched-without-a-1-based-range guard | 0 | 0 | **no** | — |
| `pb-f-nonparse-matched` | pointer-bind | `battery()` records a cell that does not parse as `matched: True` | 0 | 0 | **no** | — |
| `gm-e-absent-killed` (e) | gate-mutation | `judge`: `killed = absent or cases[declared] is False` (an absent declared case counts as killed) | 1 | 1 | yes | `red-case-absent` (sole) |
| `gm-f-validate-no-guard` (f) | gate-mutation | `validate_receipt` drops the killed-without-its-declared-case-failing guard | 0 | 0 | **no** | — |
| `gm-g-pristine-guard` | gate-mutation | `validate_receipt` drops the `pristine.ok`-with-nonzero-failures guard | 0 | 0 | **no** | — |
| `gm-h-applied-guard` | gate-mutation | `validate_receipt` drops the killed-without-an-applied-edit guard | 0 | 0 | **no** | — |

Required six: `pb-a`, `pb-b`, `pb-c`, `pb-d`, `gm-e` killed; **`gm-f` survives**.
Every anchor occurred exactly once (`anchor_occurrences: 1`); every diff is one
contiguous hunk (2 added lines, 1-for-1 swaps, or 2–4 removed lines); every
mutant copy compiled.

A first `gm-g` variant deleted the `pristine = …` binding together with the
guard and died with `NameError` before printing a summary. That is a
non-behavioural mutant: it was re-cut as a guard-only deletion and is reported
`inconclusive → discarded`, not as a survivor.

## Survivors and the case that would kill each

All five were proven with `verify_cases.py`: each proposed assertion returns
`True` on the pristine module (it finds the defect) and `False` on the mutant
(it does not). `missing-case-proof.json`:

| survivor | missing case (one sentence) | pristine | mutant |
|---|---|---|---|
| `pb-e-validate-range-guard` | A case that validates a forged pointer receipt whose matched check sits at `line_start: 0` and requires a defect, pinning the 1-based-range guard. | True | False |
| `pb-f-nonparse-matched` | A case that calls `battery()` with `git_show` stubbed to a record whose Ghidra pointer cell does not parse and requires that cell to come back `matched False`/`unparsed True`. | True | False |
| `gm-f-validate-no-guard` | A case whose forged gate receipt is `killed` with `case_absent: true` and its declared case listed in `failed_cases`, so its only defect is this guard, and that requires a defect. | True | False |
| `gm-g-pristine-guard` | A case whose forged gate receipt has `pristine.ok: true` with `failures: 2` and requires a defect. | True | False |
| `gm-h-applied-guard` | A case whose forged gate receipt is `killed` with `applied: false` and its declared case failing, and requires a defect. | True | False |

## Findings

1. **The required mutant (f) survives the instrument's own selftest.**
   `gm-f-validate-no-guard` deletes the guard that implements R79-C1's kill rule
   "a mutant counted killed while its declared case is absent from the selftest
   output or passes there" at the receipt level, and all 11 cases stay green.
   `red-forged-kill` does reach that guard (its 8 forged mutants trip it), but
   its assertion is only `bool(defects)`; the `declared_case_hits` re-derivation
   keeps the case green once the guard is gone. The guard is exercised but not
   pinned.
2. **`validate_receipt` guards are broadly unpinned.** Three of the four
   receipt-level refusal guards survive deletion: declared-case-failing,
   `pristine.ok` with nonzero failures, and killed-without-an-applied-edit. Each
   is a clause of a frozen kill rule with no isolating case.
3. **`battery()` receipt construction has no coverage at all.** No selftest case
   calls `battery`, so the parse-failure cell (`pb-f`) and the battery-level
   `unparsed`/`ok` poles can be inverted without a red case. The `--battery`
   path is only checked by running it against the lane, not by the instrument's
   own suite.
4. **What is pinned is pinned well at the primitive.** `bind()`'s 1-based slice
   is killed by `green-line` alone, the range-vs-first-line defect by
   `green-range` alone, the path-only rule by four cases including the declared
   one, and `bind()`'s `unparsed` by `red-no-line` alone; `judge`'s absent-case
   rule is killed by `red-case-absent` alone. These are single-detector kills,
   so the mutation is attributable to one named case.
5. **No claim defect.** The survivors are holes in the *selftests*, not in the
   batteries' measured outcomes: neither frozen predicate (R79-C1 8/8/0,
   R79-C2 5/5/0) is contradicted. `validate`'s own defect list is green on the
   pristine instruments.

## Integrity / restoration

- Lane instruments were never opened for writing: worktree sha256 equals the
  freeze blob and the `claims.json` pin for both paths
  (`lane_unchanged_since_freeze: true`, `claim_pins_match: true`).
- All mutants live in scratch (`/fast/scratch/hyaku/kaidoku-r79/MutInstruments/`)
  and were removed after the receipts were copied here.
- Receipts: `receipt.json` (per-mutant diff, before/after sha256, exit,
  failing_cases, proof rows), `missing-case-proof.json`, `drive.py`,
  `verify_cases.py`.
- No git/jj write, no commit, no push, no checkout; no system package change
  (no install was needed).

## Risks

- `pb-f`'s proof stubs `git_show` in-process; it demonstrates the branch
  decision, not a full `--battery` run from a fixture repo.
- The proposed cases are suggestions for the L1 to route; none was written into
  `tools/round-79/`, so the gap remains open at this receipt.
- `pb-a` is killed by four cases, not one; if the L1 wants one-case
  attributability for the path-only rule, `red-stale-line` is that case and the
  other three are incidental detectors.
