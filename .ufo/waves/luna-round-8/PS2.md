## CLAIM
L6–L10 cannot be scored: receipts for all five assigned legs are absent from the available round-8 evidence.

## METHOD
Scorer-only review; did not execute probes or infer outcomes. Compared available receipts with the frozen predictions: L6 `inspect_sqlite_database`, L7 `search_bytes`, and L8 `inspect_with_objdump` each TYPED-REFUSAL; L9 all six 6.5-only tool names absent from the 170-tool list; L10 `analyze` (or `inspect-binary-layout`) on jq RESULT. Checked `ls -la .ufo/waves/luna-round-8/receipts` and the receipt paths at 2026-10-16 20:53:26 -0300.

## FINDINGS
`ls -la .ufo/waves/luna-round-8/receipts` listed only `leg-1.md` (271 bytes); no `leg-6.md` through `leg-10.md` or tools/list receipt were present. Therefore none of the assigned classes, the six L9 name absences, or stdout hashes can be independently verified; verified prediction matches: 0/5 (unscorable, not mismatches).

## THREATS
Concurrent execution may add receipts after this snapshot. Absence here does not establish that a leg was not run.

## VERDICT
FINDING: L6–L10 are unscorable because their receipts are absent.
