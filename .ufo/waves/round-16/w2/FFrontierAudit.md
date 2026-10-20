# FFrontierAudit — round-16 wave 2 advisory audit of C1/C2 artifacts

Scope: `selection.py`, `selfcheck.py`, `controls.py`, `selection-fixtures.json`, `negative-fixtures.json`, and the `w1/SelectorModel.md` and `w1/SelectorRunner.md` claims about them. Source law: `Base-src.zip` `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java`, `…/golang/GoVer.java`, `…/rtti/JsonPatch.java`, `…/rtti/JsonPatchApplier.java`, read in place from the installed Ghidra 12.1.4 archive. Data: installed `typeinfo/golang` (11 base files, 123 `patchverdiffs/*.diff`). Reference recipe: `SCORECARD.md` command A.

Nothing was executed. No tests, builds, linters, or `selfcheck.py`/`controls.py` runs. No packages, tools, or installs. Read-only `unzip -p`, `grep`, and `ls` were used on source and data only.

## Snapshot caveat

The three implementation files changed while this audit ran (mtimes 05:20:37 to 05:22:35). Findings below are against the post-change state:

| file | sha256 (prefix) | lines |
|---|---|---|
| `selection.py` | `1d2907b3…` | 307 |
| `selfcheck.py` | `f5c20c57…` | 414 |
| `controls.py` | `5f9fe949…` | 302 |

Two earlier-seen defects were already fixed in the current state and are **not** reported: the `int()`-before-length ordering in `parse_request` (now `selection.py:84-96`) and the missing bytecode guard (now `selfcheck.py:104-114`). One docstring typo is still present (see F12).

## Verdict

No defect found in the core `select_snapshot` logic. Arch order, `IS_GOOS_UNIX`, base naming, the patch-0 and same-minor rules, the nearest-lower-diff rule, and the `missing_base` short-circuit match the cited source. The defects below are contract, calibration, and latent-harness issues. None produces a false green on the current fixtures. The strongest one (F2) is latent: no current fixture triggers it.

## Findings

Severity is my calibration: H = could hide a wrong result, M = contract or claim mismatch a reviewer would rely on, L = cosmetic or latent.

### F1 (M) selfcheck exit code contradicts its own contract
- `selfcheck.py:399-401` catches `FixtureError` per case, prints `FAIL <id>: fixture error`, and continues. Final return is `1` (`:410`).
- Docstring `selfcheck.py:63-66` and `w1/SelectorRunner.md:40-41` both say malformed case schema → exit `2`.
- Not a false green: the case is counted as failed. The exit code is simply wrong per the documented contract.
- Fix direction: raise or return `2` on `FixtureError` from `run_case`.

### F2 (H, latent) forced-key expectations are silently discarded
- `selfcheck.py:243-244`: `if key in ("patch_applied", "evidence_class"): continue`.
- The forced check (`FORCED`, `_compare` head) compares the *result* to constants. The *expectation* is never compared.
- Consequence: a fixture expecting `"evidence_class": "provider"` or `"patch_applied": true` still passes on a non-error result. That is a false green for a wrong fixture.
- Current fixtures: grep finds no `"patch_applied": true` and no non-`source_model` `evidence_class` expectation, so this is latent.
- Fix direction: if an expectation disagrees with the forced value, fail the case or raise a harness error. Do not skip it.

### F3 (L, latent) positive-case vacuity guard is weaker than documented
- `selfcheck.py` `run_case` (around `:303-311`) rejects only an *empty* `expected`. The docstring (`:34-37`) and `SelectorRunner.md:32-33` say a positive case must assert at least one *result key*.
- `patch_applied` and `evidence_class` are present on every non-error result, so `{"expected": {"patch_applied": false}}` passes for any status.
- Latent: all current positive fixtures assert real keys.
- Fix direction: require at least one non-forced key.

### F4 (M) null-valued bucket is reported by the preview but dropped by source
- `selection.py:250-258` builds `keys = set(_top_level_keys(...))` from key names only. A bucket whose JSON value is `null` is therefore reported in `base_matching_buckets`.
- Source: `GoApiSnapshot.java:216-225` stores `gson.fromJson(reader, GoArch.class)` (a JSON `null` yields `null`), then `:228-236` keeps only `if (arch != null)`. The null bucket is dropped.
- `w1/SelectorModel.md:44-47` says `base_matching_buckets` is "exactly" the `read()` retention. That is inaccurate for null values.
- No fixture covers this. Suggested: add a negative fixture (`"all": null`) and either mirror the drop or label it as a known divergence.
- [INFERENCE] Gson's null-to-null mapping for a reflective `GoArch` is from Gson convention, not executed.

### F5 (L) document parsing is stricter than the Java streaming reader
- `selection.py:156` uses `json.load` on the whole file. That rejects trailing data and accepts `NaN`/`Infinity`.
- Java `read()` (`GoApiSnapshot.java:213-226`) opens the top-level object, streams keys, and calls `endObject()`. It never checks for end-of-document, so trailing bytes after the object are ignored.
- Java rejects non-strict tokens in skipped values (`skipValue`), Python accepts `NaN`.
- Net: Python can reject a base file Java accepts (trailing data), and accept one Java rejects (`NaN` in a skipped bucket). Neither case is in the fixtures.
- [INFERENCE] Gson strict-mode behavior is from the JsonReader contract, not executed.

### F6 (M, calibration) negative fixture pins a non-source outcome as green
- `negative-fixtures.json` id `unsupported-shape-bucket-nonobject-preview` (lines ~203-221) expects `status: base_only` with buckets `["all"]` for `"all": ["not","an","object"]`.
- Source: a JSON array into `GoArch` fails inside Gson at `GoApiSnapshot.java:222`, which propagates out of `read()`, so `get()` would throw rather than return a base-only snapshot.
- The fixture's own note admits this is a LIMITATION, but it still encodes model behavior as the expected value of a passing case.
- Fix direction: model it as a declared known divergence, not a source expectation.

### F7 (L, calibration) bucket-invariance claim is untested and its label does not distinguish cases
- `selection.py:280` emits `base_matching_buckets_source: "unpatched_base_file"` for every status, including `exact_diff` and `fallback_diff`.
- `w1/SelectorModel.md:86-90` says "a diff could add/remove/rename top-level buckets."
- Source: `JsonPatchApplier.applySection`/`findParent` only changes top-level keys via a length-1 `path`. Other sections only touch content under an existing bucket.
- Data: `grep -l '^@ \["[^"]*"\]'` over the 123 shipped diffs returns **0** files. Shipped diffs do change bucket *contents* (for example `@ ["linux","Funcs",…]`, `@ ["linux-amd64","Funcs",…]`), not bucket *membership*.
- Conclusion: the preview's bucket list is invariant for the shipped corpus. That fact is true but neither asserted nor fixture-tested. The label does not say "presence-only, content unpatched."
- Fix direction: either assert the invariant as a source-model observation with the grep count, or make the label conditional on `selected_diff` and say "presence only."

### F8 (M) frozen-baseline control ignores additions
- `controls.py:197-213` (`frozen_report`) iterates `before.blobs` only (`:200`). A file *added* under `.ufo/waves/round-14/`, `.ufo/waves/round-15/`, or `evidence/round-1-2026-10-15/` at `after` is not reported.
- This is a no-harm control. Additions to frozen trees are exactly what it should flag. Its `checked`/`unchanged` counts cannot show them.
- Fix direction: also list `after.blobs` under frozen prefixes and report `added_under_frozen`.

### F9 (L) dead or misleading code in controls
- `controls.py:33` `OLD_PREFIX_DIRS` is defined and never used. Confirmed by grep (single occurrence).
- `controls.py:145` `cell.strip() if index < len(row) else ""` inside `enumerate(row)` is always true. The conditional is dead.
- `controls.py:136-150` (`source_rows`) builds a dict by `row[1]`. Duplicate IDs silently collapse (last wins), so `rows_before`/`rows_after` undercount and a duplicate row is not reported. Current corpus has no duplicates (23 rows, 0 duplicate IDs), so this is latent.

### F10 (L) decode failures escape the documented exit-2 path in controls
- `controls.py:110` and `:125` (and `source_rows` decode) call `.decode("utf-8")` with no error handling. A non-UTF-8 blob raises `UnicodeDecodeError` → traceback, exit `1`.
- Docstring (`controls.py:16-17`) says exit `2` means usage, unresolvable revision, or missing anchor. A decode failure is outside that set but unlisted.

### F11 (L) base64 fixture error escapes the harness error path
- `selfcheck.py:145` `base64.b64decode(content["raw_b64"])` raises `binascii.Error` (a `ValueError`). `main` only catches `FixtureError` in the loop (`:399`), so it becomes a traceback and exit `1`, not `2`.

### F12 (L, cosmetic) docstring names the wrong flag
- `selfcheck.py:99` says `sys.dont_writebytecode`. The code (`:109`) correctly uses `sys.dont_write_bytecode`.

### F13 (L, comment) `_path_cmp` comment misdescribes its own fallback
- `selfcheck.py:191`: "A path outside the root falls back to its absolute spelling."
- In practice every *normal* result is already root-relative (`selection.py` emits `path.relative_to(root)`). `Path(raw).relative_to(root)` raises for those, so they take the same fallback. The comparison is still correct because the raw relative string equals the expectation. The comment describes a branch that mostly never runs as intended.

### F14 (L, latent) bool/int cross-equality in `_match`
- `selfcheck.py` `_match` checks identity only when the *expectation* is `bool`. An expected `0` or `1` is satisfied by `False` or `True` (`False == 0`). Latent: no current fixture expects a bare `0`/`1` against a bool. The `selected_patch: 0` expectations are ints against ints.

## Checked and not a defect

- `parse_request` (`selection.py:70-97`): length check before `int()` (`:84-87`), `fullmatch` (`:50`, `:79`), Java-int bound, `0.0.*` rejected (matches `GoVer.isInvalid` `GoVer.java:105-107`). Digit-limit `ValueError` is avoided on the current code.
- Arch order and `IS_GOOS_UNIX` (`selection.py:42-45`, `:100-116`) match `GoApiSnapshot.java:102-109` and `:180-181`. Empty `unix` slot dropped. Dedup handled by `seen` (`:238-244`).
- Base naming `go<M.m.0>.json` (`selection.py:190`) matches `getApiSnapshotJsonFile` `GoApiSnapshot.java:122-123`. `GoVer.toString()` (`GoVer.java:155-158`) emits no `-1` wildcard for concrete versions, so no `getApiFile` fallback is needed. The fallback is correctly not reproduced.
- Diff selection (`selection.py:213-232`) is equivalent to `getPatchVerDiffFile` (`GoApiSnapshot.java:148-166`): descending candidates `0 < cand ≤ patch` in the same minor, first readable wins. Patch 0 selects nothing. Name pattern matches `getApiSnapshotFile` output.
- `missing_base` short-circuit (`selection.py:191-208`) matches `getApiSnapshotJsonFile` returning null before diff lookup (`GoApiSnapshot.java:123-126`).
- Line-number anchors in `selection.py` and fixture notes spot-checked against the archive: `get` 102, return EMPTY 115, `getApiSnapshotJsonFile` 118, base 123, `getPatchVerDiffFile` 148, `getApiSnapshotFile` 168, `IS_GOOS_UNIX` 180, `getApiFile` 183, `read` 205, `beginObject` 215, `archNamesToKeep` 212, null/empty skip 230, `EMPTY` 242, `GoVer.parse` 62/65/70-74. All match.
- `selection-fixtures.json` (9 positive cases): each expected value recomputed by hand from the algorithm and the listed files. All consistent, including `unix_order` (`darwin`→`["darwin","unix","arm64","all"]`), `windows_omission` (`exact_diff`, `selected_patch` 2, no `unix`), `lower_fallback` (4 of 2,4 ≤5), `future_diff_ignored`, and `minor_isolation`.
- `negative-fixtures.json` (17 cases): every `expect_error` type matches the raising branch (`RequestError` for regex failures, `UnreadableError` for non-JSON and non-object base). `missing-base-*` cases agree with `getApiSnapshotFile` and the two-part-fallback exclusion. `corrupt-diff-still-selected` correctly does not parse the diff. Only F6 is a concern.
- `selfcheck.py` bytecode guard (`:104-114`) correctly restores the prior flag in `finally`.
- `controls.py` craft counting matches `SCORECARD.md` command A (the recipe block, `SCORECARD.md` ~84-124): same rule split, same `RULE_REF`, same `splitlines()` count, same `1 <= start <= end <= count` check, same missing-file → invalid path.
- `controls.py` `USED_BY_COLUMN = 11` checked against `corpus/SOURCES.md`: 23 rows, each with 13 `split('|')` fields, used-by at index 11, no duplicate IDs, no escaped pipes.
- `controls.py` `prefix_report`/`unchanged_report` use git blob SHAs and byte-prefix tests as documented. No semantic claim is made in the output.

## Not verified (limits)

- Not executed: no fixture run, no `selfcheck.py`, no `controls.py`, no `git` invocation beyond reading the source. Every finding above is static.
- Java behavior in F4 and F5 rests on the Gson/JsonReader contract, marked [INFERENCE].
- Installed data was checked for names, counts, and the absence of top-level diff sections only. Diff *contents* were not replayed.
- Only `SCORECARD.md` command A's craft section was compared; its coverage half was not in scope.

## Tooling

None installed or updated.

## Suggested L1 integration checks (not run here)

1. `python3 -I selfcheck.py --fixtures selection-fixtures.json --fixtures negative-fixtures.json` (expect 26 cases; F6 case currently green).
2. Re-check exit codes after F1 fix with a deliberately malformed fixture (`{"id": "x"}`, no `request`).
3. `python3 -I controls.py <before> <after>` once, pinned to the integration revisions.
