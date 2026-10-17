## CLAIM
Re-audit luna-round-7 (records commit `6e2ee8f`), focused on W7's finding that the SCORECARD diff rewrites the coverage row instead of appending, against the arc criterion "appended, never rewritten".

## METHOD
Read-only Git. Numstat/-U0 diffs `411175e`→`6e2ee8f` (SCORECARD, LOG); LOG byte-prefix tests for all nine records commits; r1-r9 SCORECARD deletion census vs per-round sections; command A (`SCORECARD.md:93-123`) replayed from immutable Git objects at `411175e`, `3395b6d`, `a280e07`, `6e83a20`, HEAD; `PROTOCOL.md:420,447` and `templates/round-prompt.md` read. No probes, network, or tracked-file writes.

## FINDINGS
1. W7 reproduces exactly: +32/-1. The deletion is `SCORECARD.md:23` — the coverage row (72/72, `:11-60`, measured `2abd30f5`, luna-round-1 → 78/78, `:11-67`, measured `3395b6d`, luna-round-1 + luna-round-7); rest +31 append. LOG same commit: +24/-0, prefix-identical (55,754→57,274 B).
2. Command A replays 72/72 at `411175e`; 78/78, 9/9, 10.0/10.0, empty missing/dangling at `3395b6d` — the new row values are true.
3. Adjudication: the deleted line is the head "Owned axes" living row. `PROTOCOL.md:447` scopes append-only to LOG.md; `:420` defines SCORECARD rows with last-change round and the commit measured against. Across r1-r9 every SCORECARD deletion is head-only (r1 :23,53-55; r2 :25,56-62; r3 :24,61-66; r4 :68; r7 :23); zero fall inside per-round sections. r1 disclosed the same class as "evidence-field hygiene" (`SCORECARD.md:268`). Only a literal whole-file reading flags r7 — jointly with r1-r4.
4. Completing W7: the row is stale at HEAD. Command A at `a280e07`/`6e83a20`/HEAD → 79/79, yet `SCORECARD.md:23` still reads 78/78, `:11-67`, measured `3395b6d` (map now ends `:68`). r8 (`:550`) and r9 (`:604`) appended denominator 78→79/79 but deleted 0 SCORECARD lines; the head contradicts the tree.
5. W7's report-form finding is no violation: all four required sections present in order (`.ufo/reports/luna-round-7/kaidoku.md:6,19,35,58`) plus extras (`:42,63`); the contract says "Required sections, in order" and forbids none (`templates/round-prompt.md:60-74`).
6. W7's C9 finding also reproduces: `2026-10-16-l7-06-inspect-with-objdump.md` lacks literal `rea-agents@6.5.0` (grep exit 1); CB7's check is literal (`CB7.md:250`).

## THREATS
No probes/network; `PROTOCOL.md` read from the skill copy (numbering may differ). The round-10 goal's exact wording was not found in the repo or reachable fleet dirs (`.ufo/waves`, `.ufo/round-10`, `.ufo/state`, `prompts`) — adjudication rests on the protocol, the card's contract, and precedent; the stricter reading stands recorded in finding 3. Brief's HEAD `6e83a20`; actual HEAD `c343939` (additive only: LOG +16/-0, SCORECARD +12/-0, no axis claims).

## VERDICT
FINDING: r7's coverage-row edit is the card's own living-row update, not an append-only breach — but the row is stale at HEAD (78/78 vs measured 79/79) because r8/r9 never re-updated it.
