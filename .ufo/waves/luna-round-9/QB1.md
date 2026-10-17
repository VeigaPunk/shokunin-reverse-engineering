# QB1 — quality gate, items 1–2 (lane B)

## CLAIM
Independent clause-level gate on the final item-1 text (RB1.md:14-24, new EOF erratum block for r4-16) and final item-2 text (RB2.md:13-28, SCORECARD round-9 record), diffed against the GB6 manifest copies and the FB1/YB1 mechanics findings. Text-only; no probes, network, or `/tmp`; only write is this file.

## METHOD
HEAD `a280e07`; `git diff --quiet HEAD --` clean; worktree sha256 == HEAD blob for r4-16 `622e3661…`, r12-01 `fb2cd812…`, PROVINCE `fe7f3f61…`, SCORECARD `0c722936…`. Command A (SCORECARD.md:93-123) rerun → 79/79, 9/9, 10.0/10.0. Reads: r4-16:727-733,750-754,875-925; r12-01:99-120; X1.md:12,32; CB4.md:9-11; round-4 report :43-46; round-5 report :50-56,63-67; `git show 7125dd4^:corpus/README.md:163`; python hex↔decimal.

## FINDINGS
Item 1 — every factual clause PASS: `:751-752` names exactly two sites vs r12-01:99-104 four sites; `:110-120` round-5 erratum; `:115-118` attribution, receipts gone. Mechanics reproduced: r4-16's 13/13 `## Errata` headings carry lane ids and blank-line prefixes (`awk` over all 13); RB1's heading has neither lane id nor leading blank, and GB6:9 ships no heading at all — YB1:12's r14-01-section misattribution applies to that form. RB1's text omits YB1's second stale locus `:730-733` (verified: five rows labeled row-7-class vs r12-01:105-108 narrowing to L195) — outside the assigned pointer; parent's call.
Item 2 — every factual clause PASS: X1.md:12 normalizes haystack only, `:32` raw comma needles (CB4.md:11 repro; 0x1c01dc8=29,367,752, 0x505b000=84,258,816 verified); F18 report :43-46; opener :63-67 with retained "Runtime-obs extended" confirmed at `7125dd4^` README:163. RB2's text carries the required bounds (ADJUDICATED not PASS; no score change/waiver; repair/retest). Two clean variants exist — RB2 merged vs GB6:12-13's Z2 wording plus Status line — pick exactly one.

## THREATS
"7 values" not re-derivable (receipts gone); F18's mechanism clause rests on VB2:9's re-execution, not mine. Wave live: more lane-B seats landed mid-gate (22:02). Post-landing: command A, prefix/byte-identity, and heading-blank checks at the integration revision.

## VERDICT
FINDING: both texts clause-verified; before landing add RB1's heading lane id + leading blank (r4-16's 13/13 precedent) and pick one item-2 wording (RB2 vs GB6:12-13); trim-vs-restate on item 1 and YB1's `:730-733` locus stay parent rulings; invariants 79/79 + 9/9 and byte-identity hold.
