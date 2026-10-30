# ExecV5Baseline — R52-W1

Verdict: settled; v5 baseline reproduced exactly. Selftest was 18/18 (exit 0); frozen-corpus score covered 126 envelopes (exit 0), `pair_mismatch_count=0`, `evaluator_missing=0`.

Target `dmg_Z3_v3ddwrt_inode_table` currently routes to `legacy-body-failure` / `cross-read-legacy` in both table and evaluator (rule/step 7); this is the v5 behavior v6 is expected to correct.

Full commands, exits, stdout hashes, timestamp, target features and results: [baseline receipt](ExecV5Baseline/baseline-receipt.md). Machine status: `ExecV5Baseline/status.json`. No blockers or non-reproduction. Scratch output and work directory remain at `/fast/scratch/hyaku/kaidoku-r52/w1-ExecV5Baseline`.