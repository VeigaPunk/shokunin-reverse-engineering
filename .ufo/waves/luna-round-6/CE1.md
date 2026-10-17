## CLAIM
The available canonical pre-state controls can be run at the supplied HEAD, but CA6’s final census cannot be consolidated because its source artifact is unavailable.

## METHOD
Searched `.ufo/waves/luna-round-6/CA6.md` and repository-wide `**/CA6.md` with `Glob`; both returned no matches. Ran a self-contained, read-only Git-object census based on Command A (`SCORECARD.md:92-123`) plus a sorted coverage-map token count/digest. Full runnable command and receipt: `.ufo/waves/luna-round-6/receipts/census-pre.txt`.

## FINDINGS
At HEAD `f0e8cdecb216d71cf7df974675c0f6b16ba4f82f`, Command A returned 72/72 mapped knowledge files, empty missing/dangling sets, 9/9 citation-resolved rules, and coverage/depth 10.0. The coverage map had 72 tokens; sorted-token SHA-256: `c538284bd40fec6c039b6c2f18e7202f6390e0ca1ce92ea8a0c50e20a58651a0`. The stdout digest and full output are in the receipt. HEAD remained unchanged; status showed no tracked modifications.

This records the canonical Command A + map-token pre-state only. It is not represented as CA6’s final 10-leg census, a live REA result, or evidence for host/config drift checks.

## THREATS
Without CA6’s final census, its additional predicates and expected output cannot be independently established; reconstructing them by guess would invalidate the consolidation. The pre-state is a baseline, not a post-battery comparison.

## VERDICT
FINDING: CA6’s final census was unavailable; only canonical Command A and the map-token pre-state were runnable and measured.
