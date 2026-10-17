## CLAIM
L6–L10 cannot be scored against the preregistered classes from available receipts.

## METHOD
Scorer-only review. Listed `.ufo/waves/luna-round-6/receipts/` and read `MANIFEST.txt`; did not execute probe legs or infer outcomes. Predictions frozen in the dispatch: L6–L8 RESULT; L9–L10 TYPED-REFUSAL.

## FINDINGS
`ls -la .ufo/waves/luna-round-6/receipts` showed only `leg-1.md` and `MANIFEST.txt`. The manifest contains only `leg-1.md 24bfd90fb0463c2085e455964521cc85f1cff53bec638d3893e596c2869e2e91`. Receipts for L6–L10 were absent at review time, so none of the five outcomes or stdout hashes can be verified; no match count is supportable.

## THREATS
Concurrent execution may add receipts after this snapshot. This is a finding about evidence availability, not proof that the legs were not run.

## VERDICT
FINDING: L6–L10 are unscorable because their receipts are absent.
