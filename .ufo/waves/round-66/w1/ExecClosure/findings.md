# ExecClosure — R66-C1 frozen counter, single end-to-end run

Seat: ExecClosure (leaf). Instrument: `tools/round-66/closure-boundary.py`, run
read-only (`python3 -I -B`), never edited. Scratch `/fast/scratch/hyaku/kaidoku-r66/ExecClosure`
(deleted before yield). No re-runs.

## Instrument integrity

| check | value |
|---|---|
| sha256 before | `3c5cfb038d86cdde03fb659e1d42a44ffa5f42ccd019ab7ea9b52710d071045b` |
| sha256 after  | `3c5cfb038d86cdde03fb659e1d42a44ffa5f42ccd019ab7ea9b52710d071045b` |
| before == after | yes (`diff -u` clean) |
| frozen r65 pin actually on disk | `79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6` (equals `v1_pin` in every receipt) |

## `--verify` — exit 0, 5/5 arms, `ok: true`

Command exit `0`; stdout `verify.stdout` (1802 B), stderr `verify.stderr` (0 B, empty).
Receipt `verify.json` sha256 `7d2188b5ef2e73dd5978faa1afc936c96a188dc62ef189bf5ce21ac25243ea0a`.
Receipt top-level: `arms_total 5`, `passed 5`, `count 30`, `exit 0`, `ok true`.

| arm | passed | decision-bearing detail keys (values) |
|---|---|---|
| a1-guarded-fixture-green | true | `ok: true`, `cache_present: []`, `findings: []` |
| a2-unguarded-fixture-red | true | `ok: false`, `cache_present: ["__pycache__", "__pycache__/fixture_mod.cpython-315.pyc"]`, `findings: ["cache present after probe 2: __pycache__, __pycache__/fixture_mod.cpython-315.pyc"]`, `probe: {"ok": true, "message": "ok"}` |
| a3-real-manifest-count-green | true | `count_ok: true`, `entries: 30`, `ok: true`, `findings: []` |
| a4-truncated-manifest-red | true | `count_ok: false`, `entries: 29`, `ok: false`, `findings: ["count 29 != 30"]`, `dropped_entry: "d8-14.7.173/d8"` |
| a5-skip-run-no-closure | true | `closure: null`, `closure_claimed: false` |

Note the ordering fix is visible in a2: the probe itself succeeds (`probe.ok true`,
`message "ok"`), yet the post-probe cache scan flips `ok` to false and names the `.pyc` path —
i.e. the decision comes from step 3 (post-probe cache scan), not from a probe failure.
a1's detail carries no `probe` key; its decision keys are `ok`/`cache_present`/`findings`.

## `--manifest` — exit 0

Receipt `manifest.json` sha256 `305a340e91c9b70743c0a298c3686379da6e182b9cb4a5726e9d9001bc17b91f`.
`closure`: `entries 30`, `expected_count 30`, `count_ok true`, `ok true`, `findings []`,
`missing []`, `pin_mismatch []`, `cache_before []`, `cache_present []`,
`probe {"ok": true, "message": "ok"}`. Top-level `exit 0`.

## `--skip-run` — exit 1 (by design)

Receipt `skiprun.json` sha256 `1fe4d6be39f9f77730d883fe661ac049ecd0fd49fbe3b4b956763be56390ef73`.
`closure: null`, `closure_claimed: false`, `verified: false`, `exit: 1`, `skip_run: true`,
`receipts: []`, `runs_total: 0`, `runs_matching: 0`.
Exit 1 is the instrument's own contract for this mode (docstring "Exit: … 1 not verified";
`skip_run_receipt` hardcodes `"exit": 1`, returned by `main` at line 463), and `--selftest`
asserts `skiprun-exit == 1` (line 421). It is not an error: the receipt claims no closure.

## Toolchain cache

`find /home/vgpnk/.local/share/kaidoku-jsc -name '__pycache__' -o -name '*.pyc' | sort`
→ `toolchain-cache-after.txt`, 0 lines (sha256 `e3b0c442…7852b855`, the empty-file digest).
Nothing was written into the toolchain root.

## Summary

R66-C1's five boundary arms all passed on the single run; no exit-2, no stderr, instrument
byte-identical before/after, toolchain cache-free after all three modes.
