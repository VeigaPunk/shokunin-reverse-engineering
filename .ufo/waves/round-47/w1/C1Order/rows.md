# C1Order — block 24 row(s) governed by R47-C1 clause 7 (`order`)

Paste-ready. The v3-arm cell is the bare token `order` (clause 5 strips backticks/spaces, then
requires equality with the vocabulary: `order: …` or `order-ish` fails).

## Row (R46-CL6)

```
| R46-CL6 one flag reorder (moving `-m` after `--diff-merges=first-parent`) duplicates the merge entry and reports a frozen path the merge never touched as changed | the argument order is a convention no clause reads, and the round-46 note names blindness where the measured effect is over-reporting | `order` | 1 |
```

Why this wording and not the landed one. The landed row (commit `e856beb5`, block 24) says the
reorder "prints a merge twice and blinds the arm". The first half is measured true; the second
is measured false — the reversed order is `--diff-merges=separate`, which is a *superset* of
`first-parent`, so it can only over-report. Receipt `receipts/order-semantics-D.json`:
`--freeze`/`--rev` over a merge whose side branch never touched `frozen.txt` gives
`exit 0, touched []` with the gate's order and `exit 2, reason frozen_path_changed,
touched ['frozen.txt'], restored ['frozen.txt']` with the reversed order. Both rows score
identically under the counter; only the stated consequence differs, and a craft row whose
stated consequence is false is the R46-V class defect this round exists to close.

## Refs line (the clause-7 share; the block's full Refs line must also carry the other rows')

```
  Refs: `corpus/lessons/round-46.md:65-70` (R46-CL6: the order-sensitive arm and its round-47 routing), `plans/round-47-claims.md:80-82` (clause 7: the literal present exactly once and the reversed pair zero times), `tools/round-47/exact.py:260-264` (the two counts that fill `gate_order_literal` and `gate_order_reversed`).
```

Selectors were resolved against the measured revision, not guessed:

| citation | file line count at rev | resolves |
|---|---|---|
| `corpus/lessons/round-46.md:65-70` | 102 | yes (`sed -n '65,70p'` prints R46-CL6 whole) |
| `plans/round-47-claims.md:80-82` | 190 at `5017e1f`, 211 at `62e33f7d` | yes (lines 80-82 are predicate 7) |
| `tools/round-47/exact.py:260-264` | 561 | yes (`n_ok, n_bad = gtext.count(ORDER), gtext.count(REVERSED)` at 260) |

Do **not** add `tools/round-46/gate.py` to the block: it is outside clause 8's validated path
set (`corpus/lessons/`, `corpus/knowledge/`, `plans/`, `tools/round-47/`), so the pointer to the
file clause 7 measures fails the block. Measured:
`receipts/variants.json` variant `v4-cites-the-measured-file` → exit 1,
`unresolved_citations: ["tools/round-46/gate.py: outside the validated path set"]`.

## Pins the block must carry for this row to be scored

| pin | value | computed by |
|---|---|---|
| `interpreter_sha256` | `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` | `git show <rev>:tools/round-47/exact.py \| sha256sum`; identical at `5017e1f`, `62e33f7d`, `1e2c3102` |
| `mutations_sha256` | `19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` | `sha256("\n".join(["substring-arm","duplicate-routed-id","stale-mutations-digest","flag-order-drift"]))` |
| mutation names in prose | `substring-arm`, `duplicate-routed-id`, `stale-mutations-digest`, `flag-order-drift` | clause 6 requires all four named in the block |

Not pinned by any clause, and measured for the record: `tools/round-46/gate.py` at the measured
revision is `c3ba6b93ef414e3795d2142d1d9a643a465a312593cdb9f3d8027553fd38897c`, with the
ordered literal once and the reversed pair zero times.

## Whole-block candidate

`receipts/candidate-SKILL.md` is the freeze `SKILL.md` plus this seat's four-row candidate
block (all rows written here so the counter could reach clause 7 and the battery). It scores
`exit 0`, `failing []`, battery `forgeries_total 4 / v2_green 4 / v3_green 0 / genuine_green 1
/ crash 0` (variant `v1-candidate-gate-clean`). Only the R46-CL6 row above is this seat's
draft; the other three carry the peers' tokens and exist to make the block measurable.
