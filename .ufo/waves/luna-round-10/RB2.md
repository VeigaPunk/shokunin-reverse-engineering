## CLAIM
Complete the raced debt-ledger seats DB4–DB6: with D1–D6 now all present, reconcile D4 against D1–D3, re-verify D5's closure anchors, and re-run D6's omission check. Read-only; only this note written.

## METHOD
Read `.ufo/waves/luna-round-10/D1.md`–`D6.md`, `.ufo/reports/luna-round-{1..9}/kaidoku.md`, `SCORECARD.md`, `SHONEN.md`, `.ufo/waves/luna-round-7/BB5.md`. Race evidence: `stat -c '%y'` on D1–D6/C1; `D4.md:2,5`; `D6.md:5`. Re-ran D5's hash command; grepped each report-named item against D1–D6. No probes, no sibling writes. `git diff --quiet HEAD --` before write → clean.

## FINDINGS
- **Race confirmed:** `D4.md:2` "D1–D3 inputs were not yet available; the wave glob returned C1.md only"; `D6.md:5` `ls … D4.md → No such file or directory` (exit 2). mtimes: D6 22:32:20 < D4 22:33:09 < D3 22:34:00 < D1 22:35:41; D2 (22:32:25) predates D4's write but is unreferenced — consistent with early input capture; no content contradiction found.
- **DB4:** D4's closed/carried/retired buckets agree with D1–D3/D5. Its residual "fifth short-count … unavailable/ambiguous" resolves to R7: report `:3-4` (59 commissioned + 5-seat backfill), `SCORECARD.md:510-511` (59+5 = 128), `BB5.md:2` (count audit 64+59+5=128). D4's standalone presence-omissions (G1, G9, R2 misnamed report, C4 unpersisted census, R4 no-peeking/S2 — `D1.md:10-11`; A-manifest L1-only, BB7/8 overwrite — `D2.md:10`) are all cross-covered.
- **DB5:** D5's hash claim reproduces exactly: `sha256sum` → `dc740c46…` (L7), `224965bad…` (L5); `B2.md:10`'s `a910c6cd…` mismatch stands. `SCORECARD.md:70-72`'s pointer-correction-plus-content-debt note is consistent with D4 carrying the README:160/:128 content debt.
- **DB6 union residue:** no D file names X6 (`R1:66`), V11a misnamed V27.md and R09's deferred pre-integration review (`R4:65-66`), R5 `:73` box-4 province-version sub-question, VB3 absence (`R9:55-56`). All seat/record-level; none is domain debt and none changes a status.

## THREATS
Document-based; mtimes bound writes, not input reads; "no D-entry" ≠ open; /tmp and live state uninspected; cross-lane outbound items (K1) are outside this seat.

## VERDICT
FINDING: race completable, no contradictions; fifth short-count = R7 (implied, not self-labeled); residual no-D-entry items: X6, V11a, R09, R5-box4, VB3.
