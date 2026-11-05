# Supplementary draft — R98-C2 (calibration): the stop-boundary counter accepts its own honest verdict (round 98)

Not requested by name in the seat item; supplied because round 98 carries two claims and the C1 entry above cannot carry C2. Not written into `corpus/`.

source: S322/S323 family — the round-97 closure's routed defect 1; the verdict's own fourteen-key counts set comes from `tools/round-93/stop-boundary-repair-battery-v3.py` (`v3.score`, lines 288-300).
verified-at: 2026-11-05 (round 98; measured revision `72346895a35a74af18151b125934fa0c09fe1e3c`, receipt `.ufo/waves/round-98/l1/scores/c2-at-72346895a35a74af18151b125934fa0c09fe1e3c.json`)

## The defect

The landed round-97 counter `tools/round-97/stop-boundary-repair-battery-v7.py` allow-lists **nine** count keys while the verdict it certifies emits **fourteen** (`repaired`, `scored`, `wrong`, `unsafe`, `intact`, `far`, `far_refused`, `fresh_roundtrip`, `fresh_scored`, `fresh_far`, `fresh_far_refused`, `fresh_repaired`, `refused`, `silent`), so every honest public run is refused with `counts-missing-key:<k>` and the counter exits 1. The repair changes only the allow-list (v7 -> v8 adds the five missing keys to `COUNT_KEYS`) and adds one selftest case, `verify-catches-nine-key-stub`, that the nine-key stub is still refused on exactly those five keys.

## The measurement

| candidate counter | label | exit |
|---|---|---|
| `tools/round-98/stop-boundary-repair-battery-v8.py` | `legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1` | 0 |
| `tools/round-97/stop-boundary-repair-battery-v7.py` (control) | `legs passed 1 of 4; public 0; real14 0; stub9 0; extra 1` | 1 |

Frozen command:
`python3 -I -B tools/round-98/allowlist-check.py --counter tools/round-98/stop-boundary-repair-battery-v8.py --rev <rev> --work <scratch> --json-out <receipt>`
The four legs: `public` (the candidate's public run on the real battery exits 0 and prints `selfverify ok=True`), `real14` (the candidate's `count_problems` accepts the honest fourteen-key counts), `stub9` (it still refuses the round-97 nine-key stub), `extra` (it still refuses an unknown key). The v8 selftest reports `SELFTEST cases=24 failures=0` against v7's 23 cases, both exit 0.

## Limits

- This is an instrument repair (the lane's own record layer), not a carrier class and not a coverage move; the artefact class of round 98 is R98-C1.
- The allow-list is widened to the verdict's own key set, so a *new* key the verdict starts emitting would again refuse the public run; the check is a selftest case, not a bound on future verdict shapes.
- Round-97's routed defects 3-6 and defect 7 are not claimed here and stay open (see `plans/round-98-claims.md`).
