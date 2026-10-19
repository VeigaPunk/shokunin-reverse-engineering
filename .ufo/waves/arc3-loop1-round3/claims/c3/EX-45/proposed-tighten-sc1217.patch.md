# Proposed change — tighten `readme175-sc1217`'s needle (chain C3, wave arc3-loop1-round3)

Author: seat EX-45 (needle-quality review) · target:
`.ufo/gates/citation-drift/pointer-table.json`, entry `readme175-sc1217`.
**NOT APPLIED this round** — the round's landed pair is
`pointer-table.json` `bfc42f1b…` / `expected.json` `d97dd60a…`, and any table
edit requires the F3 re-pin in the same commit (below). This is a
future-round proposal, patch-text only, per the seat rules.

## Why (measured, not asserted)

- The entry's note claims: "the frontier bullet's retirement citation must land
  on the retirement line, not merely somewhere in the file."
- Measured at HEAD `c07af80` (`evidence/landed-slack.txt`, entry
  `readme175-sc1217`): the must_match `rerun id-stability` occurs on **6**
  SCORECARD.md lines — `1121, 1155, 1216, 1266, 1282, 1318` — so any renumbering
  of the citation inside `[1216, 1318]` (and the ±duplicate neighbourhood) still
  probes clean. Empirically: `SCORECARD.md:1216` → `:1318` = **green**
  (base needle), `:1217` = red. Slack **+102 lines**.
- The claimed specificity ("the retirement line") is therefore not what the
  needle grades; it grades "a line carrying the phrase".

## The change (one field + the note)

Before (landed, verbatim from the table):

```json
{"id": "readme175-sc1217", "kind": "extracted", "file": "corpus/README.md",
 "line": 175, "pattern": "SCORECARD\\.md:(\\d+)", "target": "SCORECARD.md",
 "target_group": 1, "must_match": "rerun id-stability",
 "note": "the frontier bullet's retirement citation must land on the retirement line, not merely somewhere in the file."}
```

After (proposed):

```json
{"id": "readme175-sc1217", "kind": "extracted", "file": "corpus/README.md",
 "line": 175, "pattern": "SCORECARD\\.md:(\\d+)", "target": "SCORECARD.md",
 "target_group": 1,
 "must_match": "pre-fall wall text \\(R2 — next README-touching round\\); rerun id-stability\\.",
 "note": "the frontier bullet's retirement citation must resolve to the pre-fall wall record; the tightened needle is unique in SCORECARD.md (the one line carrying the full phrase), so a renumbering to any other 'rerun id-stability' line now reddens."}
```

The replacement phrase is literal (no wildcards), bounded, and **unique** in
SCORECARD.md: `grep -c 'pre-fall wall text (R2 — next README-touching round); rerun id-stability' SCORECARD.md` = **1** (at `:1216`).

## Verification of the proposal (run by this seat, fixtures under /var/tmp)

```
as-is (cited :1216):                  rc=0 findings=[]            GREEN
renumbered to :1318 (old needle GREEN): rc=1 citation_dead         RED  <- the catch
off-by-one to :1217:                  rc=1 citation_dead          RED
```

## Landing procedure (the F3 coupling)

1. Edit the entry in `.ufo/gates/citation-drift/pointer-table.json`.
2. `sha256sum .ufo/gates/citation-drift/pointer-table.json`.
3. Update `expected.json` → `pointer_table.sha256` in the SAME commit.
4. `python3 .ufo/gates/citation-drift/citation-drift-probe.py --rev HEAD --strict`
   → expect `clean findings=0 exit=0`; default mode; `--selftest` → 13/13.
5. Re-run the slack measurement (`claims/c3/EX-45/evidence/scripts/slack.py`) —
   expect slack 0 for this entry.

Residual risk of the proposal: the phrase is a record of the pre-fall wall
state; if SCORECARD.md's own record sentence is ever reworded (append-only
convention says it will not be), the needle reddens by design. That is the
trade a specificity pin makes; the alternative (keep the loose needle) is
recorded in `needles.md` §4-A9.