# R29-C2 independent rederivation

## Findings

- **Observation:** At source commit `18be864a528873b2b70d8c94e31f880290249e90`, the selector TSV has 178 selectors (26 `canonical`, 152 `c1`). The corresponding 178 responses contain 252 candidate entries.
- **Observation:** Per set, `canonical`: 53 entries, 38 predicted true, 15 predicted false, 0 mismatches; `c1`: 199 entries, 0 predicted true, 199 predicted false, 0 mismatches.
- **Observation:** Overall: 252 entries, 38 predicted true, 214 predicted false, 0 mismatches. No response or manifest errors were reported.
- **Inference — verdict: holds.** The claim “mismatches 0 of 252 entries; predicted_true 38, predicted_false 214” matches the independent rederivation.
- **Observation:** All 178 manifest SHA-256 values match their response-file bytes, and all 178 manifest UTC timestamps are later than the freeze commit time `2026-10-22T17:03:06-03:00` (the result of `git log -1 --format=%cI dbd87cfa09eb89306c4e07d3171a4556eb732024`).

The independent script reads the inputs from `git show <pinned-revision>:<path>`, uses the pinned canonical map, and compares each returned candidate's `filtered` boolean against canonical-key membership plus signature inequality. An absent signature is treated as different; a JSON `null` result list contributes zero candidate entries. The lane counter was not run or used as an input. No network lookup was made.

## Retained evidence

Producing command:

```sh
python3 /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecIndependentC2/rederive_c2.py; rc=$?; printf 'exit_code=%s\\n' "$rc"; sha256sum /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecIndependentC2/rederive_c2.py; exit "$rc"
```

Output excerpt (run UTC `2026-10-22T20:22:53Z`; explicit exit code `0`):

```text
"manifest_entries": 178,
"manifest_errors": [],
"manifest_sha256_matches": 178,
"manifest_utc_later_than_freeze": 178,
"per_set": {
  "c1": {"entries": 199, "mismatches": 0, "predicted_false": 199, "predicted_true": 0, "selectors": 152},
  "canonical": {"entries": 53, "mismatches": 0, "predicted_false": 15, "predicted_true": 38, "selectors": 26}
},
"response_errors": [],
"source_commit": "18be864a528873b2b70d8c94e31f880290249e90",
"total": {"entries": 252, "mismatches": 0, "predicted_false": 214, "predicted_true": 38, "selectors": 178}
exit_code=0
```

Artifact under the assigned scratch directory:

- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecIndependentC2/rederive_c2.py` — SHA-256 `99ab720e7ca985bd3ee684c4c970f9503964fbcb03cb54698b398d08d67040d3`.

## Scope, risks, and blockers

- Lane file changed: `.ufo/waves/round-29/w1/ExecIndependentC2.md` (this report only). No other lane or fleet files were written.
- No tools were installed.
- **Risk/limitation:** This rederivation validates the frozen repository evidence and manifest, not a new OpenChain network response.
- **Blockers:** None.
