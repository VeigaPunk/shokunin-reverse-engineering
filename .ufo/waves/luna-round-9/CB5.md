# CB5 — instrument-home 2: where should known-limits live

## CLAIM
The two known census-instrument limits (round-4 F18 opener-detector breadth; round-5 SIZES comma-token normalization) belong in `SCORECARD.md` as one concise known-limits note at the measurement-recipes area (`SCORECARD.md:86-129`), cross-linked to the round-4/5 records — not in `corpus/QUALITY.md`, not in a new note file. Position drafted independently of X4; diff in Findings.

## METHOD
Read `SCORECARD.md:19-31,86-129,374-465,534-559`; `corpus/QUALITY.md:1-36`; `.ufo/reports/luna-round-4/kaidoku.md:30-46`; `.ufo/reports/luna-round-5/kaidoku.md:48-67`; `.ufo/waves/luna-round-5/X1.md:8-37` and `receipts/census-pre.sh:1-41`; `git ls-files .ufo`. Re-ran command A (`SCORECARD.md:92-123`, Git objects only) at HEAD `a280e07`; exit 0: `{"citation_resolved_rules": 9, "knowledge_files": 79, "mapped": 79, "missing": [], "dangling": [], "coverage_score": 10.0, "depth_score": 10.0, "rule_blocks": 9}`. Read `X4.md` only after drafting.

## FINDINGS
- SCORECARD already records both limits as instrument debt (`:407-410` r4; `:441-444`, `:458-460` r5) and owns the recipes (`:86-129`); limitation language is native there (`:21-25`).
- `corpus/QUALITY.md:1-6,7-25` is corpus-entry admission doctrine (rows cite lessons, replace-not-rewrite); a matcher defect is not an admission rule, so hosting it there conflates the measuring instrument with the content bar.
- Durability: `git ls-files .ufo/waves/luna-round-4 .ufo/waves/luna-round-5` → 0 tracked files; the census instrument copies are untracked/ephemeral, while SCORECARD, LOG and round reports are tracked (round-6/8 receipts were committed for durability, `SCORECARD.md:479-481`). A durable home must be tracked.
- Invariant safety: command A reads only `corpus/knowledge`, the README coverage map, and SKILL craft (recipe body `:94-122`), so an SCORECARD append cannot move 79/79+9/9 — re-run confirms unchanged.
- No in-repo `tools/` or limits note exists; a new file adds an unestablished surface.
- Diff vs X4: converge on SCORECARD as home, against moving limits to QUALITY.md, against a new note. Differences: (a) X4 anchors on fleet `AXES.md`/`PROTOCOL.md`; I anchor on in-repo charter plus tracked-vs-untracked evidence; (b) X4 leaves the site as "recipe/round record"; I prefer the recipes area for round-independence, with the round-9 record citing it rather than restating; (c) both leave QUALITY.md open to a later general admission rule — I'd require any such rule to be phrased as an admission criterion or not land.

## THREATS
Placement is a recommendation, not a re-test of the census. Convergence with X4 shares the same source records, so it is not independent corroboration of their truth. If a future detector retargets SCORECARD, the note must stay census-safe (no unfenced trap tokens) and the census re-run after the append.

## VERDICT
CLEAN — `SCORECARD.md` is the single durable home; X4 diff recorded (convergent; anchoring/placement differences only).
