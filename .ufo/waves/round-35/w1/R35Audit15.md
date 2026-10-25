# R35Audit15 — duplicate settle-total mutation

## Scope and retained evidence

Private lab only: `/tmp/r35-audit15-lab-76sNj7/kaidoku` (clone of lane HEAD `3ecf42981a0b63414de90ade643040d609dbb8a5`). No lane production file, corpus, counter, claim, report other than this assigned report, or VCS/index/jj state was modified. Baseline counter receipt is `/tmp/r35-audit15-baseline.json`; synthetic all-green receipt `/tmp/r35-audit15-green.json`; duplicate-key mutant receipt `/tmp/r35-audit15-mutant.json`.

The declared C2 target is all four D1–D4 defects closed; D2 requires lesson seat totals identical to the sum of both settle receipts. The counter at `tools/round-35/c2-calibration-counter.py` parses each JSON receipt with Python `json.loads`, adds `spawned`/`settled`/`dead` values, and compares that sum with the lesson line. Standard JSON loading accepts duplicate object keys and retains the last value.

### Commands and output

Baseline on lane HEAD:

`python3 -I -B tools/round-35/c2-calibration-counter.py --root . --base aa04633a686d49756763b1feed4be6830d5bb479 --freeze 3ecf42981a0b63414de90ade643040d609dbb8a5 --rev HEAD --json-out /tmp/r35-audit15-baseline.json`

Output: `C2_FAIL: D1_no_sources_change_after_base; D2_lesson_missing; D3_source_missing; D3_verified_at_missing; D3_recheck_missing; D3_source_not_s106; D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4; D4_section_missing:### Round-34 run-6 instrument registry` (exit 1). This establishes that HEAD is not a green state, not a mutation verdict.

The private lab was populated with synthetic receipts W1 `{spawned:20, settled:18, dead:2}` and W2 `{spawned:10, settled:9, dead:1}`, lesson total `30/27/3`, plus synthetic D1/D3/D4 conditions so the unmutated fixture scored `C2_CLEAN revision=HEAD` (exit 0). All changes were confined to the clone.

Mutant W1 JSON text: `{"spawned": 2, "settled": 2, "dead": 0, "spawned": 7}`; W2 unchanged. `json.loads` demonstrated resulting W1 mapping `{'spawned': 7, 'settled': 2, 'dead': 0}`. The prior lesson remained `spawned=30 settled=27 dead=3`, so the counter produced `C2_FAIL: D2_lesson_seat_mismatch` (exit 1), receipt `/tmp/r35-audit15-mutant.json`, failing list exactly `D2_lesson_seat_mismatch`.

## Finding and limits

The tested duplicated `spawned` field was detected here because last-key-wins changes the computed total. This does **not** establish duplicate-key rejection: a conflicting duplicate can be accepted and may evade this D2 check if the lesson line matches the parser's last-key-wins totals. Current test demonstrates arithmetic mismatch detection, not JSON uniqueness validation. It did not mutate other claims or test all duplicate-field placements. No lane changes or VCS operations were made; private lab commits are isolated to `/tmp`.
