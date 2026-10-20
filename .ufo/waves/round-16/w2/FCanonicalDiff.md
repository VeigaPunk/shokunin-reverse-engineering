# FCanonicalDiff — wave2 falsification report (round16, C1)

Seat: executor/leaf. Scope: authored adversarial fixture cases attacking C1's
canonical-diff-name and `patchverdiffs/` confinement laws; read current
`selection.py`, `selfcheck.py`, both fixture files, `claims.json`, and the S003
source (`Base-src.zip` → `GoApiSnapshot.java`, `GoVer.java`) for anchor
verification. **No implementation edit, no execution** (per contract: L1 runs
all checks once post-integration). Tool installs: none.

## Files changed

- `.ufo/waves/round-16/w2/CanonicalDiff-cases.json` — 11 cases, schema-conforming
  (validated: parse, unique ids, required keys, non-empty `expected` xor
  `expect_error`, no absolute/`..` fixture paths). Bare-list top level, matching
  `selection-fixtures.json`/`negative-fixtures.json`.

## Assigned attacks — verdict: both resisted by the produced artifacts

**A. Noncanonical leading-zero diff name must not win.** Guarded two ways:
request-side `_VERSION_RE` (selection.py:50) and file-side `_DIFF_NAME_RE`
(selection.py:55-56) both enforce `(0|[1-9][0-9]*)` canonical components, which
matches the source law exactly — `getPatchVerDiffFile` (GoApiSnapshot.java:148-166)
constructs probe names solely from `GoVer.toString()` = `"%d.%d.%d"`
(GoVer.java:155-158), so `go1.21.04.json.diff` is unnameable by the countdown.
Cases `noncanonical-leading-zero-diff-ignored`,
`noncanonical-decoys-lower-canonical-fallback` (leading zero in each of
major/minor/patch), `patch0-diff-and-leading-zero-lower-decoy`,
`noncanonical-diff-name-decoys` (wrong case, missing `.diff`, two-part legacy
name, non-diff file), and `noncanonical-request-leading-zero-patch`
(expect_error path) pin this from five angles.

**B. Root-level decoy diff never selected.** `diff_dir = root / "patchverdiffs"`
(selection.py:218); only that dir is scanned, matching the single fixed
relative path `typeinfo/golang/patchverdiffs/go%s.json.diff`
(GoApiSnapshot.java:153, 170-172). Cases `root-level-diff-decoy-never-selected`
(root decoy + lower canonical → fallback) and
`diff-outside-patchverdiffs-all-ignored` (root, sibling dir, and nested
`patchverdiffs/nested/` decoys → base_only) pin it.

**C. Bonus depth attack — numeric vs lexical ordering.** Real installed data
contains the 9→10 boundary (`patchverdiffs/go1.15.9..15.json.diff` present in
`ghidra_12.1.4_PUBLIC`). Cases `numeric-boundary-exact-patch10` and
`numeric-boundary-fallback-patch10` would expose a lexically-ordered "nearest
lower" bug: `'9' > '1'` so naive descending-name walk picks 9 for request
1.15.12. Implementation sorts numeric candidate tuples (selection.py:232) —
holds.

**D. Structural decoys.** `patchverdiffs-is-regular-file` (raw-string content
form → `iterdir` OSError → empty, :219-222) and
`directory-named-like-diff-skipped` (`is_file()` gate, :130-131, falls through
to patch 2). Both modeled faithfully.

## Residual observations (bounded; no defect claimed)

1. **Directory-named-like-diff divergence [INFERENCE, unproven against
   ResourceFile]:** model skips a directory named `go1.21.4.json.diff`
   (selection.py:130 `is_file()` → continues to patch 2). Source
   `getApiSnapshotFile` returns `rfile.getFile(true)` without an isFile check
   (GoApiSnapshot.java:172-176); whether a directory `File` would "win" the
   probe and then fail in `JsonPatch.read` (:136) is not established. My
   fixture pins the *model* law (byte-identity selection requires bytes) and
   its note says so explicitly; if L1 ever verifies `ResourceFile.getFile`
   semantics, this case may need recalibration — flagged, not hidden.
2. **Non-regular files unrepresentable:** `_materialize` (selfcheck.py:120-156)
   can only write regular files — symlink/FIFO decoys are out of fixture scope.
   `is_file()` follows symlinks; a dangling symlink → `is_file` False → skipped,
   consistent with model law, but untestable here.
3. **Probe-vs-scan equivalence holds for regular files** — Java's per-patch
   countdown returns the first existing path name; the model's
   max-canonical-candidate scan (:223-237) is equivalent except for the
   directory case in (1). Unreadable selected diff → `UnreadableError`
   (:138-139) vs source's late `JsonPatch.read` failure — same coarse outcome
   class (error, not silent fallback), consistent with the existing
   `corrupt-diff-still-selected` fixture's "no semantic validation" stance.

## Schema/expected-value basis

Expected values are handwritten derivations, no hashes asserted (path/status/
patch/order/bucket keys only; `sha256`/`size` deliberately absent — contract
forbids invented values). String-with-`/` path expectations
(`"patchverdiffs/go1.21.2.json.diff"`) are used where the subdir itself is the
claim, per selfcheck.py:48-51 semantics. One `expect_error` case uses
`{"type": "RequestError"}`.

## Suggested L1 verification (not run by me)

    python3 -I .ufo/waves/round-16/selfcheck.py \
      --fixtures .ufo/waves/round-16/selection-fixtures.json \
      --fixtures .ufo/waves/round-16/negative-fixtures.json \
      --fixtures .ufo/waves/round-16/w2/CanonicalDiff-cases.json

Expect 11/11 pass under the current implementation. If any fail, the
`diffs` output names the exact key — the designed-to-fail paths are lexical
sorting (numeric-boundary cases), regex coercion of leading zeros, and
root/nested decoy pickup.
