## CLAIM
Audit round-8 receipts for accidental 6.5.0 use; the required probe pin is 6.4.0.

## METHOD
Enumerated `.ufo/waves/luna-round-8/receipts/*.md`; only `leg-1.md` was present. Searched receipt contents for `6\.5\.0|6\.5`; result: no matches.

## FINDINGS
The sole available receipt pins `npx -y rea-agents@6.4.0` and reports stdout `6.4.0`, exit 0 (`receipts/leg-1.md:3-10`). No 6.5.0 leakage is observed there. Receipts for L2-L10 were absent at audit time, so their version pins cannot be checked.

## THREATS
Point-in-time inventory only; receipts created concurrently or later are not covered.

## VERDICT
FINDING: No leakage in available L1 receipt; full-set leakage check is unverifiable until L2-L10 receipts exist.
