# R35Audit33 — C2 settle JSON schema review (scribe, wave 1)

Seat: `R35Audit33` (scribe). Item: **Review C2 settle JSON schema.** Scope: read-only
(no lane writes except this report; no VCS mutation; no subagents; no `/fast/scratch`
scans; no pacman). Milestone: build evidence and first falsifications.

## 1. Frozen schema contract — derived from the instrument

Source: `tools/round-35/c2-calibration-counter.py` (frozen; pin in
`.ufo/waves/round-35/claims-canonical.json`). D-2 parsing, lines 89–113:

- `SETTLE_FILES = [".ufo/waves/round-35/w1-settle.json",
  ".ufo/waves/round-35/w2-settle.json"]` (lines 26–29).
- Each file is read as a **git blob at the measured revision**
  (`git show <rev>:<path>`, lines 40–42). A file absent from the blob → `D2_settle_missing:<sf>`.
- `json.loads` failure → `D2_settle_unparseable:<sf>`.
- Root must be a JSON object (`isinstance(obj, dict)`), else `D2_settle_shape:<sf>`.
- Required keys — `spawned`, `settled`, `dead` — each must satisfy
  `isinstance(v, int)`, else `D2_settle_missing_field:<sf>:<key>`.
- Totals are summed across both files; the lesson line
  `Seat accounting (round 35): spawned=(\d+) settled=(\d+) dead=(\d+)`
  (regex, line 109) must equal the sums exactly, else `D2_lesson_seat_mismatch`.

Minimal green shape (instrument's own selftest fixtures, lines 188–191), one file each:
`{"spawned": 2, "settled": 2, "dead": 0}`; sums 4/4/0 ↔ lesson line
`Seat accounting (round 35): spawned=4 settled=4 dead=0`. Red fixture (lines 209–211)
uses 99/99/0 and is rejected. Extra keys are permitted (no strict schema rejection).

## 2. Evidence (read-only observations)

- Current `.ufo/waves/round-35/` contains **no** `w1-settle.json` / `w2-settle.json`
  (glob of full wave tree), and `corpus/lessons/round-35.md` does not exist. D-2
  targets are absent at HEAD.
- `w1-dispatch.json` counts: `spawn=64`, `resume=0`, `total=64` — advisory expected
  `spawned` for the w1 settle receipt (the instrument itself never cross-checks against dispatch).
- Historical settle receipts, all without a `settled` key:
  - `.ufo/waves/round-34/w1-settle.json` — `spawned/completed/cancelled/dead`, `seats[]`.
  - `.ufo/waves/round-33/w1-settle.json` — `spawned/completed/cancelled/dead`, `seats[]`.
  - `.ufo/waves/round-32/a2audit-settle.json`, `a2residual-settle.json` —
    `completed/cancelled/dead`, no `spawned`, no `settled`.
  - Grep for `"settled":` across `.ufo/waves/**/*.json`: **no matches**.
- Base control `.ufo/waves/round-35/controls/c2-do-nothing.json` (instrument run at base
  `aa04633a…`, freeze `2323d197…`): exit 1, `failing` lists seven D1/D3/D4 items and
  `D2_lesson_missing` — **no** `D2_settle_*` rows (see F3).

## 3. Findings / first falsifications

- **F1 — schema drift: `settled` is a round-35-only key.** No prior settle receipt in
  the lane uses it. Copying the r33/r34 (or r32) template verbatim fails D-2 with
  `D2_settle_missing_field:<sf>:settled` (and, for r32, `:spawned`). The round-35
  builder must emit `spawned`/`settled`/`dead` explicitly; `completed`/`cancelled`
  are not read.
- **F2 — commit-before-measure timing.** D-2 reads blobs at the measured revision.
  Receipts present only in the worktree read as missing (`D2_settle_missing`). Both
  settle files must be committed before any measurement that must pass.
- **F3 — diagnostic masking.** The settle-receipt loop runs only inside the `else` of
  lesson-missing (lines 80–113): if `corpus/lessons/round-35.md` is absent, malformed,
  missing or wrong settle receipts produce no D-2 diagnostic at all (observed: base
  control shows only `D2_lesson_missing`). Exit remains 1 (honest fail), but the
  failure report is incomplete.
- **F4 — type/consistency laxness (advisory, within frozen predicate).**
  `isinstance(v, int)` accepts booleans; no non-negative bound; no invariant checks
  (`settled + dead == spawned`, `seats` length vs `spawned`, or linkage to dispatch
  `spawn=64`). None of these is in the frozen predicate, so no scope alteration is
  proposed — but the schema as enforced is minimal.
- **F5 — freeze context (outside settle schema).** `freeze-status.md` candidly records
  `INSTRUMENT_REVISED`: the freeze-integrity gate failed at `f1ea3a6d…` (pins vs
  later counter bytes); `claims-canonical.json` supersedes `claims-frozen.json`, and
  the counter's predicate identity check reads `claims-canonical.json` at the `--freeze`
  revision. Scoring decisions inherit this debt; the settle schema itself is unaffected.

## 4. Required shape for a passing D-2 (exact)

Both committed blobs at the measured revision:

```json
{ "spawned": <int>, "settled": <int>, "dead": <int> }
```

`corpus/lessons/round-35.md` must contain `AAdjacencyCite` and `31/32`, and a line
matching `Seat accounting (round 35): spawned=<S> settled=<M> dead=<K>` where
`(S,M,K)` equals the pairwise sums of the two receipts.

## 5. Limits

- Review was read-only; the counter was not re-executed (ground truth from the base
  control receipt; selftest fixtures quoted from instrument source).
- Writes: this report only. No VCS/index/jj mutation, no fleet/sibling access, no
  scratch scans, no package installs.
