## CLAIM
Independent raw-receipt score at inspection: 1 confirmed match out of 10; the complete score and delta versus PS3 are unavailable because nine leg receipts and PS3's report are absent.

## METHOD
Compared each available raw receipt with the frozen predictions in the dispatch. Read `.ufo/waves/luna-round-6/receipts/leg-1.md`; checked presence of `leg-1.md` through `leg-10.md` and `PS3.md` with a shell `test -f` loop.

## FINDINGS
`leg-1.md:3-11` records `npx -y rea-agents@6.5.0 --version`, stdout `6.5.0`, empty stderr, and exit 0. This exactly matches L1. The presence check output was: `leg-1 present`; `leg-2 missing` through `leg-10 missing`; `PS3 missing`. Thus 1/10 predictions is confirmed matched; L2-L10 are unscorable from raw receipts, not classifiable as outcome mismatches. Difference versus PS3 cannot be computed because its report is unavailable.

## THREATS
This is a filesystem snapshot while the wave is active; receipts and PS3 may appear later. I did not infer outcomes from other seats' reports.

## VERDICT
FINDING: only L1 can currently be re-scored from a raw receipt; full 10-leg independent score and PS3 comparison are unverifiable.
