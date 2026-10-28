# C1IdsArms — R48-C1 findings

## Frozen counter run
Command:

```sh
HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r48/C1IdsArms python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-48/meanings.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --json-out .ufo/waves/round-48/w1/C1IdsArms/receipt.json
```

Exit 1. Receipt: `receipt.json`. Exact observed result: marker occurrences 0, marker block count 0, 24 rule blocks; battery skipped because structural clause fails. Freeze paths unchanged (`frozen_path_changed: []`, `touched: 0`). SHA-256: receipt `b0cfe77e0d66e9bb68aaeb5ac14affaa49bee983d61619c3334788f1ef9e34e8`.

## Arm-permutation attack
The frozen revision contains no target table, so the requested comparison cannot be made against that artifact. I attempted an isolated helper harness, but the C1 module's census re-derivation loads `census_text` from `census2.py`; the test harness did not provide that module and failed with `KeyError: 'census_text'`. This is not a counter result and no green/red claim is made from it. Failed harness artifacts are not cited as successful evidence. The frozen `MUTATIONS` includes `permuted-arm`; source inspection shows v3 compares per-row arm against `EXPECTED_ARM` (meanings.py lines 351–370), while v2 only requires both routed IDs (372–375). This is source-level evidence, not a measured v2 green/v3 red result.

Fixture paths are reserved under `fixtures/`; there is no valid permutation fixture in this report. No lane source or frozen file was modified. No install performed. Tests/builds not run (not assigned).
