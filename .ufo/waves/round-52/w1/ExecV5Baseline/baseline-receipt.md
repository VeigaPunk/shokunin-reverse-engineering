# R52 v5 triage baseline

Captured 2026-10-30 UTC. Scratch: `/fast/scratch/hyaku/kaidoku-r52/w1-ExecV5Baseline`.

## Selftest
- Command: `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50-c3/sqfs-triage-v5.py --selftest --work /fast/scratch/hyaku/kaidoku-r52/w1-ExecV5Baseline/v5st`
- Exit: 0. Stdout SHA-256: `74d9918a6aae6705ceec1edfb9f028f109d4a62775220e5f25dca68fe16b7b00`
- Observed: selftest 18 cases, pass 18, fail 0.

## Frozen-corpus score
- Command: `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50-c3/sqfs-triage-v5.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 1439dfe9dadb5c3cbc525658b300c23f3013cf87 --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 --envelopes /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/ --json-out /fast/scratch/hyaku/kaidoku-r52/w1-ExecV5Baseline/score.json`
- Exit: 0. Stdout SHA-256: `3ef9dffd7b8481fbaa76fef89b807e98c2d5b3100ac99b419e891813bd6970de`
- Captured UTC: `2026-10-30T10:47:20Z` (after both commands; stdout files in scratch).
- Observed: 126 envelopes; `pair_mismatch_count=0`; `evaluator_missing=[]` (0); `verdict=met`.
- Target `dmg_Z3_v3ddwrt_inode_table`: table and evaluator both label `legacy-body-failure`, action `cross-read-legacy`; table rule 7, evaluator step 7, `match=true`. Feature evidence: `BE=yes`, handler/failing handler `squashfs_v3_ddwrt`, gap kind `extractor-failure`, `SR=no`, `P=0`, operation `extract_firmware`, provider `unblob`.
- JSON report (contains the exact target row and full score): `$S/score.json` in scratch; intentionally not retained in the seat artifacts.

No result discrepancy from requested v5 baseline. The designated v6 correction must change this target's routing rather than preserve the v5 result.