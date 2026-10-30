# ExecCensusDrift — round 51 wave 1

## Frozen census drift at base

Exact command:
```sh
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-48/census2.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab
```
Exit `0`; stdout SHA-256 `2bb5be19b3f054292a35ad54f4603361ff3f7580d83f26d0bb824a60a6d01869`; UTC `2026-10-30T04:57:23.818302+00:00`. Output:
```json
{
 "paths": 42,
 "named_but_absent": [],
 "per_file": {
  "plans/round-41-claims.md": 12,
  "plans/round-42-claims.md": 10,
  "plans/round-43-claims.md": 9,
  "plans/round-44-claims.md": 5,
  "plans/round-45-claims.md": 6,
  "plans/round-46-claims.md": 4,
  "plans/round-47-claims.md": 4,
  "plans/round-48-claims.md": 5
 }
}
```
Comparing that census with the base SKILL `<!-- instrument-registry v2 -->` marker region: **55 registered paths, 42 listed; 13 outside**. All are still registered (none vanished from the registry):
```
tools/round-49/c1-controls.py
tools/round-49/c1-counter.py
tools/round-49/c1-oracle.py
tools/round-49/c1-run.py
tools/round-49/c1-run.sh
tools/round-49/c2-mismatch.py
tools/round-50-c3/sqfs-triage-v5.py
tools/round-50/c1-controls.py
tools/round-50/c1-counter.py
tools/round-50/c1-run.sh
tools/round-50/c2-record.py
tools/round-50/fetch-vendor.py
tools/round-50/selftest-r49-c2.py
```
No duplicate registered paths. Census2's own census result is 42 (claims-derived through round 48); it does not include later round-49/50 registry rows.

## census3 draft and production procedure

Draft: `.ufo/waves/round-51/w1/ExecCensusDrift/census3.json` (SHA-256 `3ddbcf7bcec01ca63e8bed6a56b77f4d8976e56364c0b940f084f85057159ffd`). It records supersession of `tools/round-48/census2.json` specifically for the surface “marker-bound instrument-registry path inventory,” with provenance command shape, UTC, and base revision. At the eventual freeze REV, run the scoped instrument in generate mode against the frozen registry bytes, e.g.:
```sh
python3 -I -B .ufo/waves/round-51/w1/ExecCensusDrift/census3.py --root "$ROOT" --rev "$REV" --generate --out "$OUT/census3.json"
```
The instrument reads `SKILL.md` and referenced path existence at REV using `git show`, requires exactly one pair of markers, validates normalized exact cell-0 paths, rejects duplicate rows and missing paths, and records the supersession/provenance. Do not derive from the old claims-path scan. Regenerate after final R51 registry rows are added; current JSON is a base-revision specimen, not the final census.

## Frozen consumer check

`tools/round-50/c2-record.py` references census logic only in atom B9: `census_paths(c)` enumerates `tools/round-49` at BASE and `tools/round-50` at REV (excluding control-fixtures), then checks each path against the marker-bound registry, entry command, verdict map and other row requirements. It does not read `tools/round-48/census2.json`. `tools/round-50/selftest-r49-c2.py` yielded no census2 references. Thus replacing census2.json does not break these named consumers: B9 computes its own scoped path set from tree listings, and checks registration rather than census2 content.

## Executable draft and receipts

Added scoped draft `.ufo/waves/round-51/w1/ExecCensusDrift/census3.py`. It extracts exact cell-0 paths from REV's registry marker block, rejects malformed/duplicate rows and missing referenced paths, and supports `--generate`, `--check`, `--historical`, and `--selftest`. `--check` reports both `census_outside` (registered but absent from census) and `census_unregistered` (census but absent from registry), with exit 0 only when both sets and duplicates are empty. `--historical` compares frozen census2 against the registry. It does not alter frozen round-48 code.

Receipts; stdout hashes, UTC `2026-10-30T05:53:33Z`:

| Exact command | Exit | stdout SHA-256 | Observed result |
|---|---:|---|---|
| `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-51/w1/ExecCensusDrift/census3.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab --selftest` | 0 | `5feeefb7f93f7afd84b6a96ab2f454fe6fcccdb4258a922a6e84bd9863961d5b` | clean + extra/missing/duplicate/unknown cases all expected |
| `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-51/w1/ExecCensusDrift/census3.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab --historical` | 1 | `95077e6319eed3bf6b939e45a88317c0edc8b03045cfb415f6ccbc3edd257b49` | 55 registry / 42 census, outside 13, unregistered 0 (expected drift) |

Both were synthetic/offline or frozen-byte reads. Scratch removed after evidence capture.

## v6 census_outside semantics

`census_outside` is the exact set difference between registry paths and census paths for the instrument's declared scope. It measures registered paths omitted from the census; positive means omission/violation, zero means no in-scope registered path is outside. Compare normalized exact paths, distinguish registry-only from census-only paths, and do not call a path outside merely because it is absent from the registry.

No lane files modified; no REA/data run, tests, builds, or formatters run. No tools installed.
