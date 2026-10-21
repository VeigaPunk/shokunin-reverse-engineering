HOLDS — `_s_d3` marked D3 open (`substance: false`) in all four attacked commits.

## Source evidence
At S, `.ufo/waves/round-20/tools/routed-r19.py:508-526` requires a complete finding-free retained check for the manifest carrier set. Lines 530-548 accept a disarm record only when its action is `disarm`, its carrier paths equal the manifest set, and its timestamp is strictly later than every retained check; otherwise the check returns false. Lines 550-560 fall back to a live carrier check when no accepted disarm exists. The latest retained check record has `taken_at_utc: 2026-10-21T05:57:43.932121Z` (`.ufo/waves/round-20/evidence/carrier-guard/check-20261021T055743.932121Z.json:8`); the original disarm timestamp is `2026-10-21T05:57:43.966074Z` (`.../disarm.json:147`). The guard's disarm record fields are written at `.ufo/waves/round-20/tools/carrier-guard.py:457-464`. The lesson records the disarm recovery at `corpus/lessons/round-20.md:74-75` and the guard's stated limits at `:118-119`.

## Attacks and observations
Each isolated clone was detached at S (`5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9`) before committing one change. Every routed result had `D3: named=true, substance=false`; the full strict run exited 1 (it also reports unrelated D1, D2, D5, D6a, and D6c substance findings).

| Attack | Committed mutation | D3 observation |
|---|---|---|
| (a) early timestamp | `fb274dc7c17c8ef86b0a9a26f3e2afa832c69965`; set disarm time to `2026-10-21T05:57:43.932120Z`, one microsecond before the latest check | Open: `disarm.json is not later than every retained check record` |
| (b) different carrier set | `99701a7e4549fe212cb8e540548dd2b042197d54`; kept the complete disarm record shape and changed the first carrier path to existing `/usr/bin/true` (observed mode `755`, ctime_ns `1792498588066531733`) | Open: `disarm.json carrier set differs from predictions/carriers.tsv` |
| (c) other action | `5cbdd0f6bbfd8435aa3358a44ceb06fe382f1268`; changed `action` from `disarm` to `check` | Open: fallback fresh check failed with `CHECK findings=40 carriers_checked=20`; output includes `mode_restored` and `ctime_changed` findings |
| (d) no disarm | `20943fe8693c0de24ec1edce815bc89d8b8b8f38`; deleted `disarm.json`, leaving restored modes | Open: fallback fresh check failed with `CHECK findings=40 carriers_checked=20`; output includes `mode_restored` and `ctime_changed` findings |

Exact commands (captured routed exit code for each: 1):

```sh
python3 -I -B /tmp/attack-d3-hiPUsa/lane/.ufo/waves/round-20/tools/routed-r19.py --root /tmp/attack-d3-hiPUsa/lane --rev fb274dc7c17c8ef86b0a9a26f3e2afa832c69965 --strict
python3 -I -B /tmp/attack-d3-hiPUsa/case-b/.ufo/waves/round-20/tools/routed-r19.py --root /tmp/attack-d3-hiPUsa/case-b --rev 99701a7e4549fe212cb8e540548dd2b042197d54 --strict
python3 -I -B /tmp/attack-d3-hiPUsa/case-c/.ufo/waves/round-20/tools/routed-r19.py --root /tmp/attack-d3-hiPUsa/case-c --rev 5cbdd0f6bbfd8435aa3358a44ceb06fe382f1268 --strict
python3 -I -B /tmp/attack-d3-hiPUsa/case-d/.ufo/waves/round-20/tools/routed-r19.py --root /tmp/attack-d3-hiPUsa/case-d --rev 20943fe8693c0de24ec1edce815bc89d8b8b8f38 --strict
```

## Limits
Observation: all four `--strict` runs returned exit 1 with D3 open. Inference: the tested timestamp, carrier-set, action, and missing-record mutations do not bypass this recovery rule. No Go toolchain binary was executed. The LSP device was not available in the mounted tool inventory; grep was used only to locate `_s_d3`, and source claims above come from reading the revision-pinned file, not grep output. No tools were installed.