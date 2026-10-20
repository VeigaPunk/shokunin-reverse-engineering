# NegativeFixtures — round-16 w1

## Deliverable
Created `.ufo/waves/round-16/negative-fixtures.json` — 17 handwritten cases, JSON-validated structurally (17 cases, `expected`/`expect_error` mutually exclusive), not executed, no live writes. Schema per shared contract (list of `{id, request, goos, goarch, files, expected}`) extended via coordination with KaidokuR16: `expect_error: {"type": "RequestError"|"UnreadableError"}` for reject cases, `{"raw": "..."}` file sentinel for verbatim non-JSON bytes, `note` annotation field. SelectorRunner's selfcheck.py already implements this mapping.

## Case inventory

**Invalid input (expect_error RequestError — exit2 contract, distinct from source outcomes):**
- `invalid-request-two-part` ("1.21"), `invalid-request-leading-zero` ("1.021.0"), `invalid-request-v-prefix` ("v1.21.0"), `invalid-request-four-part` ("1.21.0.1"), `invalid-request-suffix` ("1.21.0+bad"), `invalid-request-negative-patch` ("1.21.-1").

**Unreadable source data (expect_error UnreadableError — parse failure, not missing_base):**
- `unreadable-base-not-json` (raw non-JSON base), `unreadable-base-json-array` (top-level `[` fails the `beginObject` step, GoApiSnapshot.java:215).

**Source outcomes (exit0, status-keyed):**
- `wrong-root-layout-files-nested`, `missing-base-empty-root`, `missing-base-two-part-name-no-fallback`, `missing-base-diff-present-unreachable`, `missing-base-case-sensitive-name`, `missing-base-nonunix-arch-order` (all `missing_base`, nulls, `patch_applied:false`).
- `unsupported-shape-bucket-nonobject-preview` → `base_only`, buckets `["all"]`, `selected_patch:0` — model previews bucket keys only, no value-schema validation (limitation recorded per L1).
- `corrupt-diff-still-selected` → `exact_diff`, `selected_patch:2`, `selected_diff` pinned as `{"path": "patchverdiffs/go1.21.2.json.diff"}` (subdir path, not basename — w2 comparator ruling) — model selects/hashes diff bytes; `JsonPatch.read` (GoApiSnapshot.java:136) lives in the patch path that `patch_applied:false` never runs.
- `unretained-bucket-not-in-search-order` → `base_only`, buckets `["all"]` — `archNamesToKeep` skip (GoApiSnapshot.java:212-218).

## Source anchors used
- `getApiSnapshotJsonFile` base-before-diff short-circuit: GoApiSnapshot.java:118-126.
- `getPatchVerDiffFile` nearest-lower walk: :148-156; fallback warn :160.
- Exact filename `typeinfo/golang/%sgo%s.json%s`: :168-172; `GoVer.toString` = M.m.p: GoVer.java:155-158.
- `getApiFile` two-part fallback :183-190 is legacy external-API only — `missing-base-two-part-name-no-fallback` pins the contract's "no filename fallback" rule.
- `archSearchOrder` List.of: :108-109; IS_GOOS_UNIX: :180-181; empty-name drop: :230 (non-unix slot omitted in emitted order).
- `GoVer.parse` leniency (GoVer.java:62-75: default patch, regex suffix strip, ignores 4th component) — most malformed-version fixtures intentionally reject what source parse accepts; strict M.m.p is the contract, noted per-case. Exception: `v1.21.0` is rejected by BOTH (source truncates at the leading 'v' → empty → INVALID); its note states agreement, not divergence.

## Distinctions kept
- `RequestError` = bad `--request` grammar; `UnreadableError` = present-but-unparseable file; `missing_base` = absent base — three separate failure classes, never conflated.
- SafetyTrust correction applied: unreadable notes assert only the API-level failure (reader `beginObject` step / `get()` declares `throws IOException`); no specific Java exception class is claimed, none was observed.
- Nonexistent root is NOT expressible through fixtures (runner materializes a real temp dir); omitted rather than faked — `missing-base-empty-root`/`wrong-root-layout` cover readable-wrong-root per L1.
- Corrupt diff is selected, not rejected: identity/selection only, no semantic validation — limitation, not a bug claim.

## Limits / risks
- Expectations handwritten from source; not executed (per contract — L1 runs selfcheck once post-integration).
- `base_matching_buckets` not pinned on `missing_base` cases (contract specifies the key but not its no-base value); pinned keys limited to contract-explicit nulls/false.
- Schema extensions (`expect_error`, `raw`, `note`) assume SelectorRunner implementation as confirmed by KaidokuR16.

Tool installs/updates: none.
Report: .ufo/waves/round-16/w1/NegativeFixtures.md
