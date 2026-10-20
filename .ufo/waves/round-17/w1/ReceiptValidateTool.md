# ReceiptValidateTool — receipt-validate.py

## Files changed
- `kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py` (new, sole artifact; ~450 lines, stdlib only, `python3 -I` compatible)

## Contract coverage (contract.md:106-108)
`receipt-validate.py RECEIPT.json...` recomputes every recorded file sha256, re-runs pins.compare on recorded pre/post, checks required fields. Exit 0 valid / 1 invalid (findings listed) / 2 unreadable or pins.py unavailable.

## Behavior (observation — implemented and selftested)
- **pins import**: `importlib.util.spec_from_file_location` from `Path(__file__).resolve().parent / "pins.py"` — absolute-path sibling import, same idiom as `retain.py:36,51-58`. Absent pins.py → exit 2.
- **Shape classification** (`classify`): `carrier` when `steps` list + `carrier` dict present; `retain` when `argv` + `pins_compare` present; else `unknown` (+ `unrecognized_shape` finding).
- **Required fields**: retain set from contract.md:27-28 verbatim (`RETAIN_REQUIRED`); carrier set from contract.md:43-47 (`CARRIER_REQUIRED`) plus per-step `{argv, cwd, exit, *_path/*_sha256, started*/ended*}` and `carrier.path` + one digest key.
- **Digest re-verification** (`walk_pairs`): generic recursive walk over the whole receipt except `pins_pre`/`pins_post` (handled separately). Three commitment forms verified: `{path, sha256[,bytes|size]}`, `{path, sha256_pre/sha256_post}`, and `<stem>_path`+`<stem>_sha256` siblings (covers retain.py:133-136 `stdout_path`/`stdout_sha256`). Cycle-safe via `id()` set.
- **Newest-digest precedence**: `sha256_post > sha256 > sha256_pre`; for pin entries, `pins_post` authoritative — a `pins_pre` entry whose path also appears in `pins_post` is skipped, so a file legitimately changed during the run is not falsely flagged.
- **pins.compare rerun** (`rerun_pins_compare`): calls `pins.compare(pre, post)` on recorded snapshots and compares `{equal, changed, missing, errors}` (list fields order-insensitive); timestamp fields excluded since they are instants, not recomputable.
- Missing/unreadable files, sha256 and size/bytes mismatches, missing fields, forged `pins_compare` all produce `{code, where, path?...}` findings; `where` is a `$.path[index]`-style locator.

## Selftest evidence (observation)
`python3 -I .../receipt-validate.py --selftest` → `SELFTEST: CLEAN cases=5`, exit 0. Cases: (1) green retain-shaped receipt → 0; (2) **tampered pinned file red → 1 with `sha256_mismatch` naming the path** (the required red case); (3) forged `pins_compare.changed` → 1; (4) green minimal carrier-shaped receipt (with `retained_logs[].files{name:{path,sha256,bytes}}`) → 0; (5) nonexistent receipt path → 2. Fixtures under `tempfile.mkdtemp`, removed in `finally`.

## Limits / risks
- Inference: carrier-run.py's exact step/retained-logs key names were not yet readable when I wrote this (contract gives descriptive, not literal, names for steps). I required `{argv, cwd, exit, stdout_path, stdout_sha256, stderr_path, stderr_sha256}` + `started*`/`ended*` prefixes — matches the contract's enumeration; if CarrierRunTool diverges, validation yields `missing_field` findings rather than exit 2.
- Recorded limitation in the docstring: validation proves "recorded digests match bytes now", not integrity during the run window; a file tampered then restored cannot be detected — same caveat pins.py itself documents.
- `pins_pre` entries with a recorded `{"error": ...}` are skipped (nothing recorded to recompute), but `pins.compare` rerun still catches an `equal: true` forgery since errors force `equal=false`.
- Snapshot `taken_at_utc`/`monotonic_ns` values are trusted (cannot recompute instants).
- Unrecognized receipt shapes still get the generic digest walk, so partial receipts remain verifiable.

## Installs
None.
