source: own-work — `tools/round-76/record-audit.py` atom `D24_capability_rows`, with receipts `.ufo/waves/round-76/pre/c1-at-base.json`, `.ufo/waves/round-76/pre/c1-control-r75audit-at-base.json` and `.ufo/waves/round-76/l1/scores/c1-at-landing.json`; the outside population is `corpus/lessons/round-75-verifier-spotcheck.md` section 6 items 1-2
verified-at: 2026-11-04
recheck: `python3 -I -B tools/round-76/record-audit.py --root . --rev <rev> --json-out <receipt>` (atom `D24_capability_rows`)

# A repertoire claim is a row, and the row is a claim

The round-75 record ends with the sentence

> **Capabilities rows appended** in the table above (`## Capabilities`): `A12 case-independence closure` and
> `exact-grammar record audit`, each with its `l1/scores` receipt.

Neither row existed in the `## Capabilities` table. The round-75 audit could not see it: its atom set was the
ROUND-74 spot-check's routed set, and the round-74 capability-rows atom (its D8) had been dropped in the rewrite.
The record was green (`mismatch_count 0` over eight atoms, `.ufo/waves/round-76/pre/c1-control-r75audit-at-base.json`)
while a sentence about the lane's repertoire contradicted the card it pointed at.

## What the atom checks

`D24_capability_rows` parses every round section that claims capability rows entered, then requires, for each
claimed name:

- a row whose **first cell** is that name (exact match, not a substring);
- a description of at least eight words (a stub is not a capability);
- an evidence cell that names at least one path, and every named path must resolve at the measured revision
  (`git show <rev>:<path>` succeeds);
- a first-working-round cell whose digits include the claiming round.

Six red fixtures ship in the selftest, one per failure shape: absent row, empty evidence cell, absent evidence
path, round mismatch, stub description, and no claim line at all. Each is scored in-process by
`capability_defects(scorecard, exists)` with an injected `exists`, so the fixtures need no repository.

## The wrap that a line parser loses

The round-75 claim wraps across two source lines, and the backticked name straddles the wrap:

```
**Capabilities rows appended** in the table above (`## Capabilities`): `A12 case-independence
closure` and `exact-grammar record audit`, each with its `l1/scores` receipt.
```

A line-level parser extracts **zero** names (the first line ends inside the backticks) and would report
`names no capability` — a false defect on a correct record. The atom reads paragraphs: it joins the block between
blank lines, then splits the claim at `, each with` and at the first sentence period, and only then reads the
backticked tokens. A token carrying `/` or starting with `## ` is not a capability name (the line also backticks
`## Capabilities` and `l1/scores`).

## Why an existence check is the right strength

The atom does not re-run the capability's evidence or judge whether the receipt supports the sentence; it checks
that the pointer resolves. That is deliberate: an atom that re-derived each capability would duplicate every
round's counter, and its failure mode would be "the capability is weak", not "the record claims a row that does
not exist". The weaker check is the one this defect class needs, and the record's own counters carry the stronger
claims.

## Limits

- Only the `Capabilities rows appended` claim shape is seen. A round that says "a new capability" in prose without
  the claim phrase is not checked, and the atom's first failure mode is exactly that silence
  (`no round section claims ...`).
- The table is read by first cell; a row whose name is reworded in the table and not in the section is a defect
  (correctly), but so is a deliberate rename that updates only the table.
- Evidence paths are resolved at the measured revision, not at the round the capability claims: a pointer to a
  receipt that lands later than the claim would pass at the later revision and fail at the earlier one.
