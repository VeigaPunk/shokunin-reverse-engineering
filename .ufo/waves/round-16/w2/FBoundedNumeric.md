# FBoundedNumeric — wave2 falsifier report

Attack named: **C1 — highest installed patch must not override request; bounded-numeric diff selection** (plus adjacent numeric-boundary and name-grammar edges). Target: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/selection.py` + `selfcheck.py`, against S003 `GoApiSnapshot.java` (Base-src.zip, Ghidra 12.1.4).

## Deliverable

`w2/BoundedNumeric-cases.json` — 11 schema-conforming cases, IDs `bounded-*`, handwritten expectations (no hashes asserted). Conforms to the `selfcheck.py` schema (selfcheck.py:20-45): bare case list, `files` values exercised as JSON objects, bare verbatim strings, and `{"raw": str}`; three `expect_error` cases use the `{"type": ...}` mapping form.

- `bounded-exact-request-beats-higher-installed` — assigned C1a: request 1.24.5, diffs 5+6 installed → `exact_diff`, patch 5.
- `bounded-fallback-nearest-lower-not-far-lower` — assigned C1b: request 1.19.20, diffs 2+13 → `fallback_diff`, patch 13.
- `bounded-numeric-not-lexicographic-fallback` — 1.22.20 with diffs 9+10 → patch 10; kills any string-sorted selector ('9' > '1').
- `bounded-patch0-diff-filename-not-selected` — `go1.23.0.json.diff` present for request 1.23.1 → `base_only` (Java loop guard `patch > 0`, GoApiSnapshot.java:153-154).
- `bounded-unbounded-patch-filename-ignored` — `go1.22.2147483648.json.diff` (int max+1) for request 1.22.3 → `base_only`.
- `bounded-noncanonical-diff-names-ignored` — leading-zero, plural-suffix, uppercase, `.bak` decoys → `base_only`.
- `bounded-request-at-java-int-max` — request/diff at 2147483647 → `exact_diff` (ceiling is representable).
- `bounded-request-patch-over-java-int`, `bounded-request-digit-run-too-long`, `bounded-request-invalid-sentinel` — `expect_error {"type": "RequestError"}` mapping cases (overflow, 11-digit component, 0.0.x INVALID sentinel).
- `bounded-raw-base-verbatim-json` — bare-string base JSON; plan9 (non-`IS_GOOS_UNIX`, GoApiSnapshot.java:180-181) 4-element arch order.

## Findings against current artifacts

**No blocking defect found in the C1 surface.** Verified by reading, not execution:

- `selection.py:223-237` filters candidates to same major+minor with `0 < cand <= patch` and takes the descending first → cannot select a higher installed patch; both assigned C1 expectations pass by inspection.
- `int()` components vs lexicographic naming → numeric ordering correct (`bounded-numeric-not-lexicographic-fallback` discriminates).
- `selected_patch` reports 0 on base-only (selection.py:266-267), consistent with fixtures.
- `_DIFF_NAME_RE` (selection.py:55-56) rejects all decoy name mutations in `bounded-noncanonical-diff-names-ignored`.
- Request bounds: regex + >10-digit pre-check + int-max check (selection.py:79-96) cover all three error cases; `RequestError` → CLI exit 2 (selection.py:302-308).

## Bounded observations (not defects under the stated contract)

1. **Directory-masquerade divergence (bounded, unverified direction).** `selection.py:232-236` skips non-regular-file diff candidates and falls back to a lower diff. Java `getApiSnapshotFile` (GoApiSnapshot.java:168-177) checks `ResourceFile` existence, not regularity; whether `Application.getModuleDataFile` returns directories was not verifiable from Base-src.zip alone. If it does, source behavior on a directory named `go1.24.5.json.diff` is selection-then-failure at `JsonPatch.read` (:136), where the model reports `fallback_diff`. Selection outcome difference only; both ends stop before a usable snapshot. No fixture case authored — expected value not derivable from source alone.
2. **`int()` on filename patch lacks the >10-digit pre-check** given to requests (selection.py:227 vs 87-90). Unreachable in practice: NAME_MAX ≤ 255 on POSIX filesystems caps components at 255 digits, far below Python's ~4300-digit int-string limit. Latent only.
3. Both findings hold only in the model plane: `patch_applied:false` and `evidence_class:"source_model"` remain truthful either way.

## Limits

- No execution: fixture expected values are handwritten from source law; L1 runs selfcheck once after integration.
- `ResourceFile.getFile(true)`/`Application.getModuleDataFile` directory semantics unresolved (class sources outside Base-src.zip); observation 1 is explicitly labeled unverified.
- Cases extend but do not replace existing fixtures; install/upgrade activity: none.

Report: `.ufo/waves/round-16/w2/FBoundedNumeric.md`
