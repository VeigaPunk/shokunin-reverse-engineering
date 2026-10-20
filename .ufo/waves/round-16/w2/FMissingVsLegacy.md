# FMissingVsLegacy — round16 wave2 falsification report

Scope: attack the produced C1 selection artifacts (`.ufo/waves/round-16/selection.py`,
`selfcheck.py`, `selection-fixtures.json`, `negative-fixtures.json`) on the missing_base /
legacy-filename / selected_diff-null surfaces, and author independent schema-conforming
adversarial cases. Source of truth: `GoApiSnapshot.java` + `GoVer.java` from shipped
`Base-src.zip` (Ghidra 12.1.4, S003). No implementation edits, no execution — expected
values are handwritten from source law and model semantics only.

`.ufo/waves/round-16/w2/MissingVsLegacy-cases.json` — 18 cases, bare-list schema
(identical to both existing fixture files; loadable via `--fixtures`). Materialization
forms exercised: JSON object, `{"raw": str}` (valid and corrupt payloads), `{"raw_b64": s}`;
expect_error forms used: `{"type": T}` mapping. No invented sha256/size values anywhere —
all `base`/`selected_diff` expectations use `null` or `{"path": ...}` only.

## Coverage vs. existing fixtures (non-duplication)

Already pinned elsewhere — not re-authored: exact-diff-without-base
(`missing_base_despite_diff`, `missing-base-diff-present-unreachable`), legacy
`go1.21.json` alone (`missing-base-two-part-name-no-fallback`), corrupt-diff-still-selected
(raw-string support on diff slot), non-JSON base (`unreadable-base-not-json`),
non-object base (`unreadable-base-json-array`), empty root (`missing-base-empty-root`),
wrong-root nesting (`wrong-root-layout-files-nested`), windows arch order
(`missing-base-nonunix-arch-order`), future-diff-ignored, minor-isolation.

New attack cells in my file:

- `missing-base-lower-diff-only` — lower same-minor diff does not rescue (only exact-patch
  was pinned before).
- `missing-base-diff-and-legacy-files` — combined legacy file + exact diff double-decoy.
- `missing-base-misnamed-diff-files` — `.diff` suffix missing, `.diff.bak`, and a correctly
  named diff at root level (outside `patchverdiffs/`).
- `missing-base-foreign-minor-and-noncanonical-diffs` — `go1.22.3.json.diff` +
  noncanonical `go1.21.03.json.diff` decoys.
- `missing-base-legacy-for-later-patch-request` — `go1.21.json` ignored even when request
  patch > 0 (base is always `withPatch(0)`).
- `missing-base-single-part-legacy` — `go1.json`, shorter than any Java fallback name.
- `missing-base-binary-diff-bytes` — `raw_b64` non-UTF8 diff bytes still unreachable.
- `missing-base-diff-nonunix-order` — missing_base under windows order.
- `legacy-file-ignored-when-base-present` — buckets must come from `go1.21.0.json` only;
  the legacy file plants `windows`/`bogus-os` keys that must not leak.
- `malformed-legacy-file-ignored` — corrupt `go1.21.json` must not raise while a valid
  base exists.
- `patchverdiffs-is-a-file` — regular file named `patchverdiffs` → base_only.
- `nested-diff-not-scanned` — `patchverdiffs/nested/go1.21.3.json.diff` invisible.
- `patch0-request-later-diff-ignored` — request `1.21.0` with `go1.21.7.json.diff` present:
  Java's `while (patchVer.getPatch() > 0)` (:151-152) never probes.
- `unreadable-base-with-exact-diff` — corrupt base + exact diff → UnreadableError
  (not missing_base, not exact_diff).
- `unreadable-empty-base` — zero-byte base → UnreadableError (distinct decode shape).
- `base-only-raw-string-valid-json` — positive use of `raw` on the base slot.

- `duplicate-selector-goos-eq-goarch` / `duplicate-selector-goarch-all` — added during
  F1 retraction: `List.of` retains duplicate arch names verbatim, so `arch_search_order`
  must contain repeated entries while `base_matching_buckets` dedups.

## Assigned attacks — bounded result

1. **Diffs without base do not rescue missing_base** — confirmed correctly modeled:
   base check precedes diff scan (`selection.py:195-213`; Java `getApiSnapshotJsonFile`
   :122-126). No defect; pinned harder in 6 new missing_base variants.
2. **Legacy `goM.m.json` not used by get path** — confirmed: only
   `go%d.%d.%d.json` with patch 0 is probed (`selection.py:195`; Java :170 via
   `GoVer.toString()`); `getApiFile`'s two-part retry (:183-190) is intentionally
- ~~F1 — `List.of` duplicate-element rejection not modeled~~ — **RETRACTED (self-error,
  corrected on L1 review).** `List.of` permits duplicate elements (verified empirically
  on JDK 21: `List.of("x","x")` succeeds; only `Set.of`/`Map.of` reject duplicates via
  `IllegalArgumentException`). Java `get()` (:108-109) therefore keeps duplicate arch
  names — e.g. `goos==goarch="x"` → `["x-x","x","x","all"]`, `goarch="all"` → trailing
  `["all","all"]` — exactly what Python's `arch_search_order` emits; only the empty
  string slot is filtered (`read()` isEmpty skip :230). NO divergence; now pinned by
  `duplicate-selector-goos-eq-goarch` and `duplicate-selector-goarch-all`. `List.of`
  does still throw NPE on null elements — consistent with contract validation
  (`RequestError` on non-string selectors).
- ~~F2 — Directory at diff path: Java selects then fails~~ — **RETRACTED on
  source re-verification.** `Application.getModuleDataFile`
  (Application.java:369-372) throws `FileNotFoundException` when the found resource
  `isDirectory()`; `getApiSnapshotFile` catches IOException → null (:173-174), so
  `getPatchVerDiffFile` skips a directory named `patchverdiffs/goM.m.p.json.diff`
  and continues the countdown — exactly matching the model's `is_file()` skip
  (`selection.py:130-131`). Directory-at-base-path likewise → null → EMPTY ↔
  missing_base. Consistent; fixture-inexpressible (materializer writes files only),
  recorded as verified-consistent rather than a defect.
- **F3 — Selector validation precedes root check** (`selection.py:187-192`): bad
  `goos`/`goarch` raises `RequestError` even for a missing root; Java builds the arch
  list only after the base ByteProvider exists, so the missing-base path never
  reaches `List.of` construction (EMPTY regardless of selectors). Consistent with the
  contract (unreadable root → exit 2 emission; selectors validated); noted as a
  divergence class, not a bug.
- **F4 — `patchverdiffs` as regular file → treated as empty** (`selection.py:218-222`,
  `except OSError: entries = []`) is consistent with Java (no diff file found → null
  → unpatched base :128-131) but silently swallows other OSErrors on the diff dir
  (e.g. EACCES) where a hostile caller might want unreadable. Fixture-pinned via
  `patchverdiffs-is-a-file`; informational.
- **F5 — Flat single-root approximation** of `Application.getModuleDataFile`
  (Java :168-174 searches all module data dirs, first match wins) is contract-scoped
  and already pinned by `wrong-root-layout-files-nested`; no new defect.

Bounded no-finding on: diff-selection order/countdown equivalence (dir-listing max ≤
patch ≡ Java's decremented probe — noncanonical names like `go1.21.03.json.diff` are
unreachable under both), minor isolation, `0.0.x` sentinel, base-bucket ordering/dedup,
`patch_applied:false` / `evidence_class` forcing (`selfcheck.py:89, 222-230`), and
path-expectation normalization (`selfcheck.py:174-191`).

## Limits

- Expected values handwritten; cases not executed against `selection.py` (L1 runs
  `python3 -I selfcheck.py --fixtures selection-fixtures.json --fixtures
  negative-fixtures.json --fixtures w2/MissingVsLegacy-cases.json` once post-integration;
  all cases must pass under current semantics or a real defect is surfaced).
- Fixture schema cannot materialize directories, symlinks, permissions, or a nonexistent
  root; the retracted-F2 directory question and F3 (error ordering) are therefore
  report-only.
- `expect_error` matching is type-name/message substring only (`selfcheck.py:268-283`);
  no Java exception class asserted per existing convention.

Tool installs/updates: none.
