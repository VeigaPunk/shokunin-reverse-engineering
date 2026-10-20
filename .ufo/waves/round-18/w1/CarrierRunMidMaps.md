# CarrierRunMidMaps — R17-PINMAP forward fix (w1, round 18)

Seat: `KaidokuR18.CarrierRunMidMaps`. Contract bullet: `.ufo/waves/round-18/contract.md:128-131`.
Defect text: `corpus/lessons/round-17-verifier-spotcheck.md:137` (mid-run `pin_checks` retained verdicts, not maps).

## Files changed

- `.ufo/waves/round-17/tools/carrier-run.py`
- `.ufo/waves/round-17/tools/receipt-validate.py`

## Behavior (observation)

`carrier-run.py`:
- `run()` creates one run-wide `mid_map_counter` (carrier-run.py:374) passed into `_run_polled`
  (carrier-run.py:376-378, signature :444-445).
- Each throttled mid-run pin check now writes its full `pins.snapshot` map to
  `<out-dir>/pins/mid-<n>.json` with `n` from the run-wide counter — never per-step, so
  analyze + `--search` steps cannot overwrite each other's maps (carrier-run.py:499-512).
  The `pin_checks` entry gains `map_path` + `map_sha256` alongside the unchanged
  `taken_at_utc`/`equal`/`entries`/`changed`/`missing` keys. A failed write records
  `map_error` in the entry instead of staying silent (:513-516).
- Docstring updated (:7-9).

`receipt-validate.py`:
- New `verify_mid_maps` (:447-547), called from `validate_receipt` (:560) for every step's
  `pin_checks` entry:
  - `map_error` present → finding `mid_map_write_error`.
  - Neither `map_path` nor `map_sha256` → round-17 shape, skipped (verdict-only checks in
    `check_binding` :187-191 still apply). This keeps all 8 working-tree r17 receipts green.
  - One field present/malformed → `mid_map_incomplete`; missing file → `mid_map_missing`.
  - Recomputes the map file's sha256 → `mid_map_sha256_mismatch` on drift (the generic
    `walk_pairs` `<stem>_path`/`<stem>_sha256` convention at :304-314 also recomputes it; the
    mid-specific code names which commitment failed).
  - Parses the map; re-runs `pins.compare(pins_pre, mid_map)` and rechecks recorded
    `equal`/`changed`/`missing` → `mid_map_compare_mismatch`; also rechecks
    `taken_at_utc` and `entries` against the map's own record.
- Docstring gains step 5 (:25-30); selftest docstring updated (:703-705).

## Selftests (run once each, pasted verbatim)

```
$ python3 -I -B .../round-17/tools/carrier-run.py --selftest
SELFTEST: CLEAN cases=3
EXIT=0
```
cases 1→2→3: case 3 is new — carrier mutated before analyze → mid-run check records
`equal: False`, retains the full map under `out3/pins/`, digest re-verified, run exits 1
(carrier-run.py:680-715). Case 1 also asserts every pin_checks entry retains a verified
map (:649-652).

```
$ python3 -I -B .../round-17/tools/receipt-validate.py --selftest
SELFTEST: CLEAN cases=12
EXIT=0
```
cases 9→12: `carrier_mid_map_green` (intact retained map → 0),
`carrier_mid_map_tampered_red` (map bytes appended → exit 1 **and** finding
`mid_map_sha256_mismatch`, not merely the generic stem-walk code),
`carrier_mid_map_forged_red` (consistent digest, forged map content → exit 1 **and**
`mid_map_compare_mismatch`). The required tampered-mid-map red case is present.

## The 8 working-tree receipts (acceptance: exits stay 0)

`python3 glob` enumeration → subprocess run of the updated validator, pasted result:

```
paths: 8
validator_exit: 0
{"invalid": 0, "receipts": 8, "unreadable": 0, "valid": 8}
calib-esbuild-0.25.12 valid 349
calib-shfmt valid 345
pro-aether valid 347
pro-containerd-shim valid 345
pro-esbuild-0.21.5 valid 349
pro-esbuild-0.27.7 valid 349
pro-notesmd-cli valid 345
pro-op valid 357
```

All 8 exit 0 (29 `pin_checks` total, zero `map_path` fields → r17 verdict-only path taken,
verified by census before editing). `checks_performed` rose vs the pre-change validator
because each map-less `pin_checks` entry is now counted as an evaluated gate; no findings.

## Commands run

| Command | Exit |
|---|---|
| `ls runs/*/receipt.json` (listed 8; also errored — phantom `runs/run-log.txt/receipt.json` in this shell) | 2 |
| `python3 -c` pin_checks census over `runs/*/receipt.json` | 0 (29 checks, `has_map_path=False` ×8) |
| `python3 -I -B carrier-run.py --selftest` | 0 — `SELFTEST: CLEAN cases=3` |
| `python3 -I -B receipt-validate.py --selftest` | 0 — `SELFTEST: CLEAN cases=12` |
| shell-glob validator run (9 paths incl. phantom → `unreadable: 1`, overall exit 2; wrapper echoed 0) | 2 |
| Python glob + subprocess validator over the 8 real receipts | 0 — `valid: 8` |

Caveat (observation): this seat's bash glob expansion yielded a phantom
`runs/run-log.txt/receipt.json` (`run-log.txt` is a file, not a dir). Same quirk
RevPinChecksCode reported; use Python `glob`/`find` for receipt enumeration.

## Design notes (inference unless cited)

- Run-wide counter, not per-step: with `--search`, per-step `mid-1.json` names would
  overwrite and stale `map_sha256` values would turn a clean run red (peer
  RevPinChecksCode advisory concurred).
- `map_path`/`map_sha256` chosen deliberately to hit the existing `walk_pairs`
  `<stem>_path`+`<stem>_sha256` convention — digest recompute is enforced even if
  `verify_mid_maps` is bypassed.
- `CARRIER_REQUIRED`/`CARRIER_STEP_REQUIRED` untouched; `entries` stays an int;
  `check_binding`'s equal-only verdict branch unchanged for map-less checks.

## Risks / blockers

- `time.monotonic()` starts near 0 on a freshly booted host, so `now - last_pin_check
  (init 0.0) >= 30` may hold false briefly after boot → first-poll check could be skipped.
  Pre-existing semantics, not changed here. [INFERENCE]
- Tampered-map receipts produce two findings (generic `sha256_mismatch` + mid-specific)
  — intentional defense in depth, noisier output.
- Blockers: none. No installs performed (Python 3 stdlib only; pacman pause respected).

## L1 follow-up (CriticDiscernment RB-3): `--require-mid-maps`

Added to `receipt-validate.py` (no carrier-run change needed):

- `--require-mid-maps` (receipt-validate.py:923-926) → `validate_paths(..., require_mid_maps)`
  (:611, call :633-634) → `validate_receipt(..., require_mid_maps)` (:583, call :593-594) →
  `verify_mid_maps(..., require_mid_maps)` (:447).
- Under the flag, every `steps.*.pin_checks[]` entry missing `map_path`+`map_sha256` →
  `mid_map_missing` (:494-500), and an `analyze` step with no checks (absent or `[]`) →
  `mid_checks_absent` (:572-587). Without the flag the r17 verdict-only path is unchanged.
- `mid_entries_mismatch` (:477-482, both modes): a recorded `entries` that cannot equal
  `len(pins_pre.entries)` is a finding — a forged verdict-only entry cannot shrink the pin set.
- Output dict records `require_mid_maps` (:650).

### Selftests (run once, pasted verbatim)

```
$ python3 -I -B .../receipt-validate.py --selftest
SELFTEST: CLEAN cases=18
EXIT=0

$ python3 -I -B .../carrier-run.py --selftest
SELFTEST: CLEAN cases=3
EXIT=0
```
New receipt-validate cases: `carrier_r17_shape_green_without_flag` (0),
`carrier_flag_r17_shape_red` (1 + `mid_map_missing`), `carrier_flag_mid_map_green` (0),
`carrier_flag_checks_absent_red` (1 + `mid_checks_absent`),
`carrier_entries_forged_red_no_flag` and `_flag` (1 + `mid_entries_mismatch`).

### The 8 r17 receipts, both modes

```
flag=False exit=0 counts={"invalid": 0, "receipts": 8, "unreadable": 0, "valid": 8} findings=[]
flag=True  exit=1 counts={"invalid": 8, "receipts": 8, "unreadable": 0, "valid": 0} findings=["mid_map_missing"]
```

Flag off → unchanged (8/8 exit 0). Flag on → all 8 go red with `mid_map_missing`, which is
the intended r18 gate (they are r17-shape receipts). `mid_checks_absent` does not fire for
them because their `analyze` step does carry checks; `mid_entries_mismatch` does not fire
because `entries` matches `pins_pre`.

| Command (follow-up) | Exit |
|---|---|
| `receipt-validate.py --selftest` | 0 — `SELFTEST: CLEAN cases=18` |
| `carrier-run.py --selftest` | 0 — `SELFTEST: CLEAN cases=3` |
| 8 receipts, no flag (Python glob + subprocess) | 0 — `valid: 8` |
| 8 receipts, `--require-mid-maps` | 1 — `invalid: 8`, `mid_map_missing` |
| `ast.parse` both tools | 0 — both parse |
