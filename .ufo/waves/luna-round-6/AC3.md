## CLAIM
Run CB6’s frozen final census at HEAD `f0e8cdecb216d71cf7df974675c0f6b16ba4f82f` and report each gate.

## METHOD
Executed the fenced command in `CB6.md:8-367` from the repo root. The stdout, invocation, and stdout SHA-256 are recorded in `receipts/census-final.txt`; stdout SHA-256: `75ea5a8f6a735fb820a1759b47a7c3a0ef39323417d1261edfff9d4668fbc32e`.

## FINDINGS
- PASS: frozen HEAD; tracked-clean worktree (`tracked_dirty=0`); coverage-map token digest/count matches both baselines.
- PARTIAL: Command A matches the one parseable baseline; `census-laneB-pre.txt` has no parseable Command A record (1/2 sources), so its second comparison is unavailable.
- PASS: 20/20 receipts; recorded exit codes 0; stdout digest recheck matches 20/20; no class conflicts, route conflicts, version drift, or duplicate A/B receipt files.
- PASS: each lane scores 10/10 against predictions; agreement 10/10; no prediction mismatches. Census exits 0, `CENSUS RESULT: PASS`.
- WARN: L10 route diverges in both lanes; extra unverified digest labels in A7/B6; classes were structurally derived for A1,2,3,5,9,10 and B2,5,6. L2 routes use text scans.

## THREATS
The script warns rather than fails when a baseline lacks Command A data; therefore `commandA_ok=True` does not establish comparison against both baselines. Extra digest and L10 route warnings remain as reported by the frozen script.

## VERDICT
FINDING: Census PASS; Command A baseline comparison is only 1/2 sources because the lane-B baseline has no parseable record.
