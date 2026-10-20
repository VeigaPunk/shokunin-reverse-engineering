# FPreviewNotValidation — wave-2 falsifier report (preview vs validation boundary)

Scope: authored `.ufo/waves/round-16/w2/PreviewNotValidation-cases.json` (21 cases, schema-conforming to selfcheck.py/selection-fixtures.json: bare case list, `files` values as JSON objects, raw strings, `{"raw": …}`, `{"raw_b64": …}`, and `expect_error` in dict/string forms). All expected values handwritten by tracing selection.py and GoApiSnapshot.java; no execution; sha256 asserted nowhere (sizes only, per no-invented-hashes). Attack axes per assignment: (a) corrupt/unparseable diff bytes still select on filename alone, (b) null-valued buckets vs names-only preview, (c) no semantic validity invented. Tool installs: none.

## Case summary (attack → expected, source anchor)

Corrupt/invalid diff selected filename-only:
- `pnv-corrupt-diff-shadows-valid-lower` — garbage bytes at `go1.21.4.json.diff` shadow a valid `go1.21.2.json.diff` → `fallback_diff`, patch 4. Java agrees: `getPatchVerDiffFile` (GoApiSnapshot.java:148-166) returns first present file; `JsonPatch.read` fails only inside the derived-provider lambda (:136) that `patch_applied:false` never runs. Also pins that `sorted(candidates, reverse=True)` (selection.py:245-251) does not continue past an unreadable-content candidate — a real divergence *would* appear only if the model ever content-validated.
- `pnv-empty-diff-selected-exact` — zero-byte diff, `{"size": 0}` asserted → `exact_diff`.
- `pnv-valid-json-wrong-schema-diff` — snapshot-shaped JSON in a `.diff` name → `exact_diff`; parses but wrong document kind, undetected by preview.
- `pnv-binary-diff-selected` — `raw_b64` `"/v4A"` (3 non-UTF-8 bytes) at exact name shadows valid patch-1 → `exact_diff`, `size:3`.

Filename-law edges:
- `pnv-diff-at-root-not-probed` — diff filename at root, not `patchverdiffs/` → `base_only` (:154 subdir arg).
- `pnv-noncanonical-diff-names-ignored` — `go1.21.02`, `.bak`, uppercase decoys → `base_only`; Java probes only canonical `GoVer.toString()` names.
- `pnv-patchverdiffs-is-file` — `patchverdiffs` as plain file → `NotADirectoryError` → `entries=[]` → `base_only` (selection.py:233-235).
- `pnv-diff-name-directory-skipped` — directory wearing the exact diff name is skipped (`is_file()`), lower valid diff selected → `fallback_diff` patch 1. Java consistent: `getDataFileInModule` throws FileNotFoundException for directories (Application.java ~368-371), so the countdown also proceeds.
- `pnv-base-name-directory-is-missing` — directory wearing `go1.21.0.json` → `missing_base`; same Java agreement.

Null-vs-names-only buckets (per parent's contract refinement; current `_top_level_keys` docstring at selection.py:147-158 now omits null-valued buckets — my expectations target that landed fix):
- `pnv-null-bucket-omitted` — `{"linux-amd64": null, ...}` → buckets `["linux","all"]`, NOT `["linux-amd64",...]`. Source law: Gson `fromJson` yields null GoArch for a JSON `null` value, dropped by the `arch != null` guard (GoApiSnapshot.java:233-235).
- `pnv-null-and-array-buckets-discriminating` — `amd64:null` omitted while `unix:[...]` retained names-only → `["unix","all"]`. Separates a null filter from blanket non-object filtering; runtime would actually fail GoArch deserialization on the array, but the names-only limitation is an allowed preview bound.

Preview-labelled unpatched buckets:
- `pnv-buckets-unpatched-despite-removing-diff` — a `{"Op":"remove","Path":"/linux-amd64"}` patch payload still leaves `base_matching_buckets: ["linux-amd64","all"]` with `base_matching_buckets_source: "unpatched_base_file"` pinned — the label is what keeps this honest (contract: "must be labelled so when diff selected").

Search-order/bucket asymmetry:
- `pnv-goos-equals-goarch-dedup` — `amd64/amd64` → `arch_search_order` retains duplicate `["amd64-amd64","amd64","amd64","all"]` (Java `List.of` keeps it) while buckets dedup → `["amd64-amd64","amd64","all"]`.
- `pnv-goos-unix-literal` — `goos="unix"` not in `IS_GOOS_UNIX` (:180-181) → single `unix` slot, no doubling.
- `pnv-empty-string-bucket-name` — `""` top-level key silently dropped for windows (empty slot filtered; matches skipValue path :216-224).

Request-parse boundary:
- `pnv-request-major-zero-minor-nonzero` — `0.5.0` accepted → `missing_base` (`isInvalid` is major==0 AND minor==0, GoVer.java:105-107).
- `pnv-request-invalid-sentinel` — `0.0.7` → `expect_error {"type":"RequestError","contains":"INVALID"}`.
- `pnv-request-patch-int-max` / `pnv-request-patch-int-overflow` — `2147483647` accepted (inclusive bound), `2147483648` → RequestError containing "Java int".
- `pnv-request-empty-goos` — `""` → RequestError containing "goos". Deliberate strict divergence: Java proceeds with raw strings.

## Defects / divergences found in produced artifacts

1. **selection.py stricter than source on trailing bytes (pinned as intentional divergence, not a bug to fix silently).** `pnv-base-trailing-junk` expects `UnreadableError`: `json.load` (selection.py:160-162) rejects trailing data after the top-level object, but Java `read()` loops `beginObject…endObject` (GoApiSnapshot.java:214-227) with no full-consumption assertion, so Gson tolerates trailing bytes. Model exit-2s where runtime proceeds. Worth a one-line docstring mention alongside the existing "stricter than GoVer.parse" disclosure; currently only implied.
2. **Empty `goos`/`goarch` divergence** (case above): Java proceeds (`List.of("-amd64", "", …)` — actually `""` survives `List.of`, gets skipped in the read loop); model RequestErrors. Contract-mandated ("non-empty"), pinned.
3. **w1 SelectorModel.md report vs current code — now consistent** (earlier `except OSError: entries=[]` gap I observed mid-wave was replaced by the landed FileNotFoundError/NotADirectoryError-vs-other-OSError split at selection.py:230-238; no residual defect).
4. **No defect in directory handling**: `is_file()` skip for both base- and diff-named directories matches `getDataFileInModule`'s directory rejection — verified against FileResource.getResourceAsFile and Application.getDataFileInModule rather than assumed.

## Bounds

- Not covered (unexpressible in fixture schema): symlinked diff/base files, unreadable-permission files, `patchverdiffs` containing a same-canonical-name with case-insensitive FS, sha256 collision assertions, and any runtime `JsonPatch` semantics (correctly out of scope).
- `pnv-diff-name-directory-skipped` Java-agreement relies on `getDataFileInModule`'s FileNotFoundException for directories — static-read confident, not runtime-verified.
- No checks/tests run; expected values are handwritten from code paths only. If L1's integrated run shows `pnv-null-*` failing, it means the null-filter edit was reverted — expected list `["linux-amd64","linux","all"]`/`["unix","amd64","all"]` under pre-filter semantics.
