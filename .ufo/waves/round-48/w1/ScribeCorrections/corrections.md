# Draft — `## Record corrections — round 48` (SCORECARD.md)

Paste-ready block. Both lines verified to re-derive under the frozen
`tools/round-48/record2.py` grammar at rev `663f30ee` (HEAD at verification
time): exit 0 `score()` on the candidate card, `corrections_bad []`,
`quotes_corrected [{quote: "exempted 2", corrected: 1}]`, round-47 floor
`seats_via_correction true`. Evidence: `receipts/verify-out.json`.

## Placement rules (mandatory — measured, not stylistic)

1. Append the block **after** the `## Round 48 — …` section (or at the end of
   the card), never between a round heading and the end of its body: inserting
   the heading inside `## Round 47` truncates that section at `\n## `, which
   loses the section's path/rev/claim atoms **and** the receipt citation the
   `quote` correction needs (`probe-placement.json`: exit 1, failing
   `round-47: no path atom / no rev atom / names no claim id /
   corrections that do not re-derive: 1`).
2. Each correction is a **single line**. The parser reads each `^- corrects …`
   line alone; continuation lines are ignored, so anything the counter needs
   must be on the bullet's own line.
3. `quote` statement order matters: the **first**
   `atoms|exempted|corrections|mismatches N` token in the statement is the one
   that binds. `exempted 1` must stay the first such token (the later
   `"exempted 2"` inside quotes is prose and does not rebind; verified).
4. The `seats` claim must state `<n> waves, <total> seats total` (the oracle's
   `CORR_SEATS` grammar) and equal `(len(dispatch files), sum(spawn))`.

## The block

```markdown
## Record corrections — round 48

Append-only repair of the atoms `tools/round-48/record2.py` re-derives; each
`corrects` line below supersedes the value it names and is itself re-derived by
the counter at the measured revision.

- corrects seats round-47: 1 wave, 75 seats total — `.ufo/waves/round-47/w1-dispatch.json` reports `counts.spawn 75` and is the only dispatch file for the round; the section names no seat total.
- corrects quote round-47: exempted 1 — the cited receipt `.ufo/waves/round-47/l1/scores/c2-at-A7.json` exempts one atom (a list of one element), where the section quotes "exempted 2".
```

## Why each line re-derives

- `seats round-47` → oracle `dispatch_counts("47")` reads
  `.ufo/waves/round-47/w{i}-dispatch.json` at the measured rev: `w1` yields
  `counts.spawn 75`, `w2` is absent → derived `(1 wave, 75 seats)` = claimed
  `(1, 75)`. Satisfies `record2`'s completeness floor (`seats_via_correction`)
  for the round-47 section, which carries no seat atom. Forged variants
  (`2 waves, 75`, `1 wave, 74`, `1 wave, 76`, missing-grammar `75 seats`) all
  rejected — `receipts/verify-out.json` check D.
- `quote round-47` → `_quote_correction` binds `exempted 1`: the round-47
  section quotes `exempted 2` (`quoted [2]`, so `1` is not already stated), and
  the section's cited receipt
  `.ufo/waves/round-47/l1/scores/c2-at-A7.json` has `exempted` = a list of one
  element → `quote_value` = 1 = stated value → backed. Clause 4 then binds the
  stale quote: `quotes_corrected [{round-47, "exempted 2" → 1}]`. A forged
  correction stating `exempted 2` is rejected ("the section already quotes that
  value" / unbacked — `c1-at-A7.json` carries no `exempted` cell).
