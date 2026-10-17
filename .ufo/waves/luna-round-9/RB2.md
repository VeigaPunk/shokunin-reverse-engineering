## CLAIM
Item-2 final gate: certify the final census-instrument-limits text and its home — `SCORECARD.md`'s new luna-round-9 record, single site, not `corpus/QUALITY.md`.

## METHOD
Read Z2, Q2, VB2, CB5, X4, B1–B4, E1, H, H4, Z5, CB2, P0–P2 at HEAD `a280e07`; verified every cited line by read (X1.md:12,32; CB4.md:11; r4 report :43-46; r5 report :50-56,63-67; SCORECARD.md:407-410,458-460; QUALITY.md:7-25). Re-ran Command A (`SCORECARD.md:93-123`, `REV=HEAD`) and tracked/PROVINCE diffs. No probes, network, or writes beyond this file.

## FINDINGS
- Command A exit 0: `{"citation_resolved_rules":9,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":79,"mapped":79,"missing":[],"rule_blocks":9}`; `git diff --quiet HEAD --` and `-- PROVINCE.md` both exit 0 (Q2/VB2/CB2 concur).
- Z2's text substantiated clause-by-clause; VB2's re-check refines F18's mechanism (unsatisfiable conjunct = replacement-pair/refuted encoding, not "z=1 line-count"). B2's imperative/standalone-section form rejected (B3/E1 guard; CB4/H4 duplication/waiver risks).
- Home: `SCORECARD.md` (tracked; already owns the instrument-debt record `:407-410,:458-460`); `corpus/QUALITY.md` rejected (admission doctrine, `:7-25`). Site: round-9 record; CB5's recipes-area preference recorded as dissent — declined (duplicates `:453-460` per CB4; B1 warns against standing gates).
Final item-2 text (append inside the new round-9 section; SCORECARD.md ends :559):

```text
Known census-instrument limits (rounds 4–5, carried; ADJUDICATED, not PASS).
The round-5 SIZES check passed comma-grouped needles (`29,367,752` /
`84,258,816`) into comma-normalizing text, so no correct input could pass
(`.ufo/waves/luna-round-5/X1.md:12,32`; `.ufo/waves/luna-round-5/CB4.md:11`;
`.ufo/reports/luna-round-5/kaidoku.md:50-56`). Round-4 F18's predicate was
structurally unsatisfiable — its unsatisfiable conjunct is the
replacement-pair/refuted-encoding test — while the stale wording was absent,
and the round-5 README-opener detector matched the retained "Runtime-obs
extended" opener, not the corrected content
(`.ufo/reports/luna-round-4/kaidoku.md:43-46`;
`.ufo/reports/luna-round-5/kaidoku.md:63-67`). These are instrument limits,
not corpus-content verdicts; documentation only — no score change and no
waiver: new mismatches stay evidence-adjudicated until the affected matcher
is repaired and retested.
```

## THREATS
VB2/CB5 landed during this gate (21:59–22:00). No live census re-run; the F18 mechanism follows VB2's re-execution, not r4's parenthetical. Nothing is landed at a280e07: post-landing Command A and non-target byte-identity remain for integration (G4/CB2).

## VERDICT
CLEAN — final item-2 text and home certified; land verbatim in SCORECARD.md's luna-round-9 record.
