# ReviewerC2 — R85-C2 attack (depth), scoped findings

Full evidence: `.ufo/waves/round-85/w1/ReviewerC2/attack.md`; receipts in `.ufo/waves/round-85/w1/ReviewerC2/receipts/`.

## Verdicts (21 rows, frozen table `.ufo/waves/round-85/mutants.json`)
- SOUND 19, WEAK 2 (pc-token-metachar-drop-pipe, pc-token-allowlist-widened: sound for the declared mutant, sibling changes survive), FABRICATED 0.
- Candidate evidence: ExecPrintedCmd (7 rows), ExecPrintedRun (8 rows), ExecSourceBind (4 rows + cg-floor-le/sb-window/sb-two kept). Every r85 case calls a production entry point; none reads a tool's own source.

## Scorer attacks (frozen `tools/round-84/mutation-closure.py`, unmodified, sandbox roots)
- (a) always-red pristine case: CAUGHT (pristine_failed, 15 rows inconclusive, killed 6, ok false).
- (b) fabricated source-text cases (`b64(find) in open(__file__)`): NOT caught; 21/21, ok true. Depth needs case review; `ok` alone does not certify it.
- (c) name-level collateral credit: NOT caught; pc-cells-index-shift already fails three pre-existing names at BASE.
- (d) table shrink: NOT caught; r85 has no `claims.json` container, so the `fixtures.sha256` pin is unenforced (ok true at 20/20). Lane table unchanged (sha ef031dbe = declaration).

## Weakened-case check
No pre-existing case weakened. ExecPrintedCmd replaces the `sourced-row-rejected-status` registration with a strengthened function that keeps the queued assertion and adds a rejected row.

## Integration
ExecPrintedRun and ExecPrintedCmd both edit printed-command.py at the selftest tail: textual merge conflicts (1 block). Keeping both sides: selftest 36/36 green; with ExecSourceBind files the combined candidate scores killed 21/21 ok true; r84 regression 13/13 ok true (sandbox probe only, not a candidate of this seat).

## Blockers
None for the attack. Markers and candidates were present for all three seats.
