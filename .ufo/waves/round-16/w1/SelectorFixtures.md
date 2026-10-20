# SelectorFixtures — round-16 w1

Scope: author `.ufo/waves/round-16/selection-fixtures.json` (9 independent source-law cases) for the `selection.py` contract. Source/data/model evidence only; nothing executed.

## Files changed

- `.ufo/waves/round-16/selection-fixtures.json` (new, 5512 bytes, parses as JSON, top-level list of 9 cases)

## Source anchors (all `GoApiSnapshot.java`, Base-src.zip @ ghidra_12.1.4_PUBLIC)

- `get()` arch search order `List.of(goOS+"-"+goArch, goOS, IS_GOOS_UNIX.contains(goOS) ? "unix" : "", goArch, "all")` — lines 102–116 (order at 108–109). **L1 contract decision (IRC, this round): `arch_search_order` is the effective read order — the literal `""` placeholder that `List.of` produces for non-unix goos is omitted**, matching `read()`'s skip of empty names (230–232); source literal vs effective order is documented here. All fixtures assert the effective 4-element order for non-unix goos.
- `getApiSnapshotJsonFile()` — lines 118–146: `baseVer = goVer.withPatch(0)` (122), base lookup (123), early `null` on missing base **before** diff search (124–126 → `missing_base`); diff `null` → base ByteProvider unchanged (128–131 → `base_only`); diff present → derived patched provider (133–145, never applied by the model → `patch_applied:false`).
- `getPatchVerDiffFile()` — lines 148–166: `while (patchVer.getPatch() > 0 && ... == null) patchVer.prevPatch()` (153–156) → strictly-decreasing, exact-major.minor filename loop; highest diff ≤ request patch wins; diffs above the request are unreachable (`future_diff_ignored`); patch 0 terminates the loop regardless of files (`patch0`); warn vs info at 158–164.
- `getApiSnapshotFile()` — lines 168–178: filename `"typeinfo/golang/%sgo%s.json%s"`, subdir `""` for base / `"patchverdiffs/"` for diffs, suffix `""` / `".diff"`. Matches installed tree: `data/typeinfo/golang/go1.15.0.json…go1.25.0.json` + `patchverdiffs/go1.15.1.json.diff…`.
- `read()` — lines 205–240: retain only listed arch keys (218–221), emit in `archNames` order skipping null/empty (228–236) → `base_matching_buckets` = `arch_search_order ∩ base keys` in order, `""` never survives.
- `IS_GOOS_UNIX` — lines 180–181: 12-entry set incl. linux, darwin, freebsd; windows absent.
- `getApiFile()` two-name fallback (183–192) is **unused** by `get()`/`getApiSnapshotJsonFile` — fixtures deliberately omit the `go1.21.json` fallback filename; contract's "no getApiFile fallback" holds.

## Case → exercised law

| id | request | files (existence only) | expected status | law |
|---|---|---|---|---|
| missing_base_despite_diff | 1.21.4 | diff 1.21.4, no base | missing_base | early return 124–126 precedes diff search |
| exact_diff | 1.21.3 | base + diff 1.21.3 | exact_diff, patch 3 | first loop iteration hits |
| lower_fallback | 1.21.5 | base + diffs 1.21.2, 1.21.4 | fallback_diff, patch 4 | nearest-lower, skips .4-miss→.2 gap ordering |
| no_diff | 1.21.1 freebsd/386 | base only | base_only | freebsd ∈ unix set; buckets `[unix, all]` |
| patch0 | 1.23.0 | base + stray `go1.23.0.json.diff` | base_only | `patch > 0` guard ignores a patch-0 diff file |
| future_diff_ignored | 1.22.1 | base + diffs 1.22.3, 1.22.9 | base_only | loop starts at 1.22.1, never looks upward |
| minor_isolation | 1.21.2 | base 1.21.0 + 1.22.0; diffs 1.20.9, 1.22.1 | base_only | filename is exact `major.minor.patch`; no cross-minor fallback for base or diff |
| unix_order | 1.25.0 darwin/arm64 | base only | base_only | darwin ∈ unix set; order `[darwin-arm64, darwin, unix, arm64, all]`; `darwin-amd64` key excluded |
| windows_omission | 1.18.2 windows/amd64 | base + diff 1.18.2 | exact_diff, patch 2 | `""` dropped under L1's effective-order decision; installed `unix` key excluded from buckets |

## Calibration decisions (ambiguities resolved, stated for L1)

- **Top-level shape**: bare list of cases, per contract's "list of cases" (no envelope object).
- **files values**: JSON objects per contract. Real `.diff` files are a custom `@`-section patch format (observed installed `go1.15.1.json.diff`), not JSON — diffs carry `{}` as an existence marker; selection never parses content.
- **`base`/`selected_diff` dict values**: per L1 decision, expected asserts the relative `path` field only — `{"path": "go1.2X.0.json"}` / `{"path": "patchverdiffs/…json.diff"}` — never size/sha256 (no fabricated hash expectations; values stay hand-authored). Null remains asserted where required.
- **`""` in `arch_search_order`**: superseded by L1 decision — omitted everywhere (effective order); the literal-source `""` fact is retained in the anchor above for the model docs.
- **`patch0` stray diff**: adversarial file `patchverdiffs/go1.23.0.json.diff` pins the `> 0` guard; a runner matching diffs without the guard fails this case.
- Every case asserts `patch_applied:false`, `evidence_class:"source_model"`, `requested` echo — cheap seals against a runner that patches or escalates evidence class.
- **`selected_patch` semantics** (L1): `0` for `base_only` (reflects the selected `withPatch(0)` base), `null` only for `missing_base` where nothing is selected; integers for diff-selected statuses.

## Retained evidence

- `/tmp/gas/ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` (extracted from `~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`), lines cited above.
- Installed data dir `…/Base/data/typeinfo/golang/`: bases `go1.15.0`–`go1.25.0.json`, `patchverdiffs/` present.
- `python3 -c "json.load…"` syntax check only: 9 cases, valid JSON.

## Risks / blockers

- ~~arch_search_order `""` spec point~~ resolved by L1: effective order is contractual; fixtures updated.
- Nested-dict subset semantics: L1 accepted `{"path": …}` assertions; runner must support one-level nested subset matching on `base`/`selected_diff`.
- No live Ghidra `get()` execution (no target selected); model is source-derived, labelled `source_model`.

Tool installs: none. No build/test/lint run (single JSON syntax check on my own artifact only).
