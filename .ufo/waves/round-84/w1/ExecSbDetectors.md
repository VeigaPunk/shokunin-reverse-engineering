# ExecSbDetectors — r84-w1 report (source-bind boundary detectors)

Seat: executor, lane kaidoku-shokunin, round 84, L1 KaidokuR84. Scope: candidate selftest
extension of `tools/round-83/source-bind.py` with the two round-83 outside-review boundary
fixtures, plus mutation-closure demonstration on the candidate bytes. Frozen bytes were read,
never edited; the lane tree is unchanged.

## Candidate

- Full replacement candidate: `.ufo/waves/round-84/w1/ExecSbDetectors/candidates/source-bind.py`
  (sha256 `3986706e1502cbf90d414ce3cc0c837d12cc0e99f212d2980d87f24d4c3cc4cd`).
- Unified patch: `.ufo/waves/round-84/w1/ExecSbDetectors/candidates/source-bind.patch`
  (`a/tools/round-83/source-bind.py` → `b/tools/round-83/source-bind.py`, labels repo-relative;
  `git apply --check` clean, and applying it to the frozen bytes reproduces the candidate
  byte-for-byte — both asserted in scratch before cleanup).
- Change: two fixtures appended to `FIXTURES` before `unavailable`, plus a two-line comment.
  No predicate, counter, mutant table or fixture was altered; the grammar function, CLI and
  receipt shape are byte-identical to the frozen file outside the `FIXTURES` tuple.
  - `late-single-header`: exactly one line-start `source:` field on line 13 (0-based index 12),
    valid grammar, names `S299`; expected rc 1 (`fields[0][0] >= 12` → not attributed).
  - `duplicate-target-second`: two line-start `source:` fields, only the second names the
    target id; expected rc 1 (two fields → unbound). Under the `][-1:]` mutant the second
    field alone would be attributed (rc 0), so the case fails.
- Frozen baseline for comparison: `tools/round-83/source-bind.py` sha256
  `800a759e20096859a145cfbe3f95e199502f7aa38b8ca796575d00af5963db3c`, re-hashed unchanged
  after all work.

## Mutant verdicts (frozen `tools/round-84/mutation-closure.py` `score()`, rows taken verbatim from the frozen `.ufo/waves/round-84/mutants.json`)

Demonstrated on the candidate bytes committed in a private scratch fixture repo (toplevel
asserted equal to the fixture dir before any commit; no lane git/jj state touched):

- `sb-header-position` (find `if len(fields) != 1 or fields[0][0] >= 12:`): **killed** by its
  declared case `late-single-header` — mutant-run failures `['late-single-header']`,
  `declared_case_present true`, `anchor_occurrences 1`.
- `sb-duplicate-last` (find `if line.startswith("source:")]:` → `][-1:]`): **killed** by its
  declared case `duplicate-target-second` — mutant-run failures
  `['duplicate-target-second']`, `declared_case_present true`, `anchor_occurrences 1`.
- Receipt summary on candidate bytes: `mutants 2, killed 2, survivors [], inconclusive [],
  pristine_failed [], ok true`.
- Baseline on the frozen bytes, same two rows: `killed 0`, both `survived` with
  `declared_case_present false` (the frozen six-case population never declared either case) —
  the delta is exactly the two new cases; each mutant run fails only its own declared case.
- Receipts: `receipts/mutation-closure-sb.json` (both runs, repo heads
  `3733cfd3709dd087839aeedc040846541c849fbd` frozen-bytes, `089d45235c2054b14827a8a552b99c1f6e48ae10`
  candidate-bytes), `receipts/candidate-selftest.json`.

## Pristine summary

- Candidate `--selftest`: `passed true`, `working_root_preserved true`, 8/8 cases ok, exit 0.
  Per-case `rcs == [expected, expected]`, stable findings on the double run:
  `positive [0,0]`, `withdrawn [1,1]`, `malformed [1,1]`, `duplicate [1,1]`,
  `duplicate-after-window [1,1]`, `late-single-header [1,1]`,
  `duplicate-target-second [1,1]`, `unavailable [2,2]`.
- All six original fixtures keep their expected exit codes (evidence above; also present in
  the mutation-closure pristine target block: `green true`, `exit 0`,
  `case_names` listing all eight cases).

## Scope, guard and tooling compliance

- Writes limited to `.ufo/waves/round-84/w1/ExecSbDetectors/` (candidates + receipts) and this
  report at the trailer path. No production edits, no fleet/sibling writes, no lane git/jj
  mutations, no commits/pushes, no `task` spawns, no `agent://all`. Lane
  `tools/round-83/source-bind.py` hash verified unchanged.
- Fixture git repos lived only under scratch
  `/fast/scratch/hyaku/kaidoku-r84/ExecSbDetectors/` with `git rev-parse --show-toplevel`
  asserted equal to each fixture dir before committing; scratch seat dir removed before this
  yield (siblings' scratch dirs untouched).
- Tooling authorization (operator 2026-10-19): nothing installed or upgraded — host
  `python3 3.14.8` and `git 2.56.0` sufficed; RULES.md consulted for the channel rules.
- Not done here by scope: the frozen 13-row table run at BASE/after (`ExecMutantBase`/L1), the
  round-82 targets, and any predicate or container change.
