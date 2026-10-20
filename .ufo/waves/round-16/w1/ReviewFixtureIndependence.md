# ReviewFixtureIndependence — round-16 w1 (reviewer, leaf)

Scope: review of handwritten selection/negative fixture expectations against source law, independent of any implementation. Read-only. No checks, builds, tests, or fixture runs executed. No installs or updates made.

## Candidate artifacts at review time

- `.ufo/waves/round-16/selection-fixtures.json`: **absent** (SelectorFixtures pending per wave1-result.json).
- `.ufo/waves/round-16/negative-fixtures.json`: **absent** (NegativeFixtures pending).
- `selfcheck.py` / `selection.py`: **absent**.

Therefore this review checks the source contract and the proposed failure modes, not candidate expectations. Every "fixture defect" below is a predicted failure of the spec as written and must be re-checked when files land. Nothing here is a pass.

## Source law (anchors)

Source: `Base-src.zip:ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` and `.../golang/GoVer.java`.

| Law | Anchor |
|---|---|
| Base is always `go<M.m>.0.json`; request patch is not used for base | L122 `goVer.withPatch(0)`; L168-171 `typeinfo/golang/%sgo%s.json%s` |
| Missing base returns before any diff lookup, so a diff alone yields nothing | L124 `if (jsonFile == null) return null;` precedes L128 `getPatchVerDiffFile` |
| Diff lookup: exact first, then strictly lower patch, same major.minor only | L153-155 loop: guard `patch > 0`, probe `patchverdiffs/go<ver>.json.diff`, `prevPatch()` |
| Patch 0 never probes a diff | L153 guard `patchVer.getPatch() > 0` false for patch 0 |
| `prevPatch` floors at 0 | GoVer.java L134 `patch > 0 ? patch - 1 : 0` |
| No diff found → base returned unpatched (only the warn path differs) | L128-131 `patchDiffFile == null` branch; L158-163 warn text |
| Legacy `go<M.m>.json` fallback exists but is not on the `get` path | L183-191 `getApiFile`; the `get` path (L102-116) calls only `getApiSnapshotJsonFile` |
| Arch search order | L108-109 `[goos-goarch, goos, IS_GOOS_UNIX.contains(goos) ? "unix" : "", goarch, "all"]` |
| `""` placeholder is silently dropped; absent keys are skipped | L230 `if (archName == null || archName.isEmpty()) continue;` ; L218 skip non-kept keys |
| `IS_GOOS_UNIX` = aix, android, darwin, dragonfly, freebsd, hurd, illumos, ios, linux, netbsd, openbsd, solaris | declared between `getApiSnapshotFile` and `getApiFile` |
| Missing resource → `null` (IOException swallowed), not an error | L168-178 `catch (IOException e) return null` |
| `GoVer.parse` strips from the first char not in `[.0-9]` onward, then splits on `.` | GoVer.java L65 `replaceAll("[^.0-9].*$", "")`; L66 `parts.length < 2 → INVALID`; L72 patch default 0 for `parse(s)` (L46) |

Data facts (read from the installed golang directory; names only, nothing computed):
- Bases: `go1.15.0.json` through `go1.25.0.json` (11 files). No `go1.14.*`, no `go1.26.*`. No `go1.X.json` (no-patch) names.
- Diffs: `patchverdiffs/` contains no `.0` diffs. Contiguous from `.1`: 1.15 (1-15), 1.16 (1-15), 1.17 (1-13), 1.18 (1-10), 1.19 (1-13), 1.20 (1-14), 1.21 (1-13), 1.22 (1-12), 1.23 (1-12), 1.24 (1-6). **No 1.25 diffs.**
- Top-level bucket keys of `go1.22.0.json` and `go1.25.0.json` are identical: `386, all, amd64, arm, arm64, cgo, darwin, darwin-amd64, darwin-amd64-cgo, darwin-arm64, darwin-arm64-cgo, linux, linux-386, linux-386-cgo, linux-amd64, linux-amd64-cgo, linux-arm, linux-arm-cgo, linux-arm64, linux-arm64-cgo, linux-cgo, unix, windows, windows-386, windows-386-cgo, windows-amd64, windows-amd64-cgo`.
- Diff file format is **line-oriented text, not JSON** (`go1.22.5.json.diff` begins `@ ["all","Funcs","archive/zip.fileEntryLess","Position"]` then `- "..."` / `+ "..."` lines; 1196 lines).

## Findings (ranked)

**F1 (high) — `missing_base despite diff` must expect `selected_diff: null` and `selected_patch: null`.**
Source returns before the diff lookup (L122-128). A fixture that plants `patchverdiffs/go1.22.5.json.diff` without `go1.22.0.json` and expects a non-null `selected_diff` or `selected_patch: 5` encodes the failure the source rules out. Expected: `status: missing_base`, `base: null`, `selected_diff: null`, `selected_patch: null`.

**F2 (high) — `patch0` must be `base_only` even when a patch-0 diff is planted.**
A tree containing `patchverdiffs/go1.22.0.json.diff` with request `1.22.0` expects `base_only`, `selected_diff: null`. Source never probes patch-0 diffs (L153 guard). Same for request `1.22.1` when only `go1.22.0.json.diff` exists: prevPatch floors at 0 (GoVer L134), the loop exits, result is `base_only`, not `fallback_diff`. Any expectation of `fallback_diff` to patch 0 is a defect.

**F3 (high) — `future diff ignored` and `minor isolation` must be tested with the 'wrong' diff present.**
- Future: request `1.22.5`, only `go1.22.6.json.diff` planted → `base_only`, selected_patch null (loop only walks downward, L155).
- Minor: request `1.23.4`, only `go1.22.4.json.diff` planted → `base_only` on `go1.23.0.json`; if `go1.23.0.json` is absent the result is `missing_base`, not a borrowed 1.22 base (L122 uses the requested minor).
Fixtures that assert `fallback_diff` for either are source-law violations.

**F4 (high) — Schema cannot express negative outcomes.**
The shared contract's case schema is `id, request, goos, goarch, files, expected`, with `expected` a subset of the JSON output. Exit-2 cases (negative patch, malformed versions, unreadable JSON, unsupported shape, nonexistent root) have no `expect_exit` / `expect_error` field, so they cannot be checked as exit codes. NegativeFixtures and SelectorRunner must agree on such a field before either writes cases. Until then the "keep invalid-input expectations distinct from source outcomes" rule (negative-fixtures item target) has no field to carry the distinction.

**F5 (high) — Hand-authored `sha256`/`size` cannot satisfy "expected values not computed".**
`base` and `selected_diff` carry `path,size,sha256`. For the real installed files, hand-typed digests are invented values. For temp-tree fixtures, bytes depend on the runner's JSON serializer (`files` maps to JSON objects), so size/sha are not authorable by hand. Expectation must either omit `size`/`sha256` or derive them from the runner's own written bytes at run time (not a handwritten constant). Flag any hard-coded digest as invented.

**F6 (medium) — `selfcheck` basename normalization hides directory defects.**
Shared contract: "path basename normalization for base/selected_diff when expected string". Source distinguishes `typeinfo/golang/go1.22.0.json` (base) from `typeinfo/golang/patchverdiffs/go1.22.5.json.diff` (diff). A selector returning `go1.22.5.json.diff` at the root, or a base copied into `patchverdiffs/`, passes basename comparison. Expected values should be root-relative paths (`patchverdiffs/go1.22.5.json.diff`), with basename normalization as a separate, explicit mode.

**F7 (medium) — Subset comparison and `null` expectations.**
Expectations such as `selected_diff: null` / `selected_patch: null` are only meaningful if the runner treats an explicit `null` as "key must be null" rather than "skip". Otherwise `missing_base` and `base_only` cases pass vacuously. Runner (SelectorRunner) must assert presence and nullness.

**F8 (medium) — `windows omission` is ambiguous between two readings.**
Source (L108-109, L230): for `windows` the search list is `[windows-amd64, windows, "", amd64, all]`, and `""` is discarded at read time. The effective buckets are `windows-amd64, windows, amd64, all`; `unix` is never searched. A fixture expecting `arch_search_order` to include `"unix"` for windows is a defect; a fixture that drops `""` from `arch_search_order` but keeps it in the pre-read list is a normalization that must be declared. The spec must say which list `arch_search_order` reports (pre-filter with `""`, or effective without). Expectations should pin the effective list and state that choice.
Real-data check (keys above): `windows-amd64`→ matched `windows-amd64, windows, amd64, all` (4 buckets); `linux-amd64`→ matched all 5 (`linux-amd64, linux, unix, amd64, all`).

**F9 (medium) — `unix order` should not rely on goos inventing the set.**
`IS_GOOS_UNIX` is a closed set. Use `linux` or `darwin` for the unix case, and `windows` (not in the set) for omission. Any other goos (e.g., `js`, `wasip1`, `plan9`) gets no `unix` entry; a negative case for unknown goos is a CLI-validation question, not a source outcome (see F12).

**F10 (medium) — Lower-fallback fixtures should use real data as well as temp trees.**
Real-data expectations that can be checked by reading the data directory only (none computed):
- `1.22.5` → `exact_diff`, base `go1.22.0.json`, selected_diff `patchverdiffs/go1.22.5.json.diff`, selected_patch 5.
- `1.22.13` → `fallback_diff`, selected_patch 12 (no 1.22.13 diff; 1.22.12 present).
- `1.15.16` → `fallback_diff`, selected_patch 15.
- `1.24.7` → `fallback_diff`, selected_patch 6.
- `1.22.0` → `base_only` (no `.0` diff exists).
- `1.25.1` → `base_only` (no 1.25 diffs at all; source emits `Falling back from 1.25.1 to 1.25.0` in logs only).
- `1.23.0` → `base_only`.
- `1.26.0` → `missing_base`; `1.14.9` → `missing_base`.

**F11 (medium) — Legacy `go1.X.json` trap is not covered by the spec.**
`getApiFile` (L183-191) would select `go1.22.json` for patch 0; the live `get` path does not. A fixture that plants `go1.22.json` (no patch) with request `1.22.0` must expect `missing_base`. The spec's "no getApiFile filename fallback" is only a prose line; add an explicit case.

**F12 (medium) — Malformed-version expectations conflate source behavior with CLI validation.**
Source behavior from `GoVer.parse` (GoVer.java L65-75), as written:
- `go1.22.5` → `""` → INVALID (source). 
- `1.22.-1` → cut at `-` → `1.22.` → parts `[1,22]` → **accepted as 1.22.0** (source). A negative-patch case expecting exit 2 is a CLI rule, not a source outcome; label it so.
- `1.22.5x`, `1.22.5 X:rangefunc`, `1.22.5.6` → accepted as 1.22.5 (source).
- `1..5`, `1.x`, `1`, `""`, `2147483648` patch → INVALID (source).
- `01.22.5` → accepted as 1.22.5, but `requested` string handling is undefined.
- `1.22` → accepted (patch default 0) by source; CLI contract says M.m.p.
Negative fixtures must state for each case whether the expected result is "source-accepted" or "CLI-rejected by design", since the two disagree on `1.22.-1` and `1.22`.

**F13 (medium) — "unreadable JSON" and "unsupported shape" have no defined contract.**
Source streams and validates the whole base JSON (L205-232; skipped keys are still parsed). The shared contract's selection.py computes `path,size,sha256` and does not require parsing. A corrupt base can therefore produce exit 0 with `base` populated, or exit 2 if the Python parses it. Fixtures must pick one, and the contract must say whether malformed JSON is "unreadable" (exit 2). Expectation currently unspecified.

**F14 (medium) — "wrong-root no base" conflates two cases.**
- Existing root with no `go1.X.0.json` → source `missing_base` (L168-178 returns null; not an error) → exit 0.
- Nonexistent `--root` → contract says exit 2 (unreadable).
Fixtures must name which one they test; a single "wrong-root" expectation cannot be both.

**F15 (low) — Diff-file fixtures as JSON objects are not faithful.**
The fixture schema maps relative filenames to JSON objects. Real `.diff` content is line-oriented text (see Data facts). Selection never parses diffs, so a `{}` placeholder is harmless for status, but it is not a faithful diff. Fixtures should mark diff entries as opaque text/existence markers, not JSON.

**F16 (low) — Request-key echo undefined.**
`requested` is in the output but normalization (`01.22.5`, `1.22`) is not specified. Expectations on `requested` should be the literal input string, or the normalization must be stated.

**F17 (low) — Base-only label not defined.**
Contract: "Base-only matching is unpatched preview and must be labelled so when diff selected." No key, value, or field name is specified. Fixtures cannot assert a label that has no name. Define the field before writing expectations, or remove the requirement from fixture scope.

## Calibration notes

- No candidate expectation was available, so no fixture was judged correct or incorrect. Findings are predictions from source law and are marked as such.
- Real-data expectations in F10 are limited to what the directory listing shows. Digests and sizes were not computed or read.
- `patch_applied: false` and `evidence_class: source_model` should hold for every status; fixtures should assert them on every case (no status produces `true`).

## Verification gaps

- Candidate `selection-fixtures.json` and `negative-fixtures.json` did not exist at review time; F1-F3, F7, F11-F14 must be re-checked against the files once written.
- No runner behavior observed; F6/F7 are read from the shared contract text only.
- Diff file bodies were sampled at 15 lines; their semantics were not read beyond the header.
- `GoApiSnapshot.getApiSnapshotJsonFile` is shown reading `fsService` derived providers; I did not trace Ghidra's `Application.getModuleDataFile` resolution beyond L168-178.

## Install/update record

None. No tools installed or updated.
