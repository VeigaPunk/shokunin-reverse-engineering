# FFixtureComparator — round16 w2 falsification report

Scope: null-field handling, relative subdirectory assertions, and non-vacuity of expectations in `selfcheck.py`, with reach into `selection.py`, `controls.py`, `selection-fixtures.json`, `negative-fixtures.json`. Source read only. No tests, builds, linters, or fixture runs were executed. Every claim is a trace of the produced text at the cited lines; runtime confirmation is left to L1's single post-integration run.

Tools installed: none.

## Findings (ordered by severity)

### F1. Null expectations on path keys pass when the key is absent (vacuous)
- `selfcheck.py:234-256`. For `base` and `selected_diff`, line 235 reads `actual_entry = result.get(key)`. A missing key becomes `None`. The `exp is None` branch (254-256) only tests `actual_entry is not None`, so a missing key passes.
- The generic non-path branch guards this (261-263, `key not in result`). The path branch does not. The forced-invariant branch (224-230) uses a `"<missing>"` sentinel and is correct.
- Consequence: `{"base": null}` or `{"selected_diff": null}` passes even if `select_snapshot` stops emitting that key. Affected positive expectations include `missing_base_despite_diff` (selection-fixtures.json:13-14), `no_diff` (:90), `patch0` (:113), and the null-path expectations in the negative missing-base cases.
- Reachability: latent. Current `selection.py` always emits both keys (`selection.py:196-206`, `:264-265`), so no current fixture passes wrongly. A future key rename or drop goes undetected.
- Fix direction: apply the line-261 presence check to path keys before the None check.

### F2. Basename-only comparison leaves subdirectory and root placement unpinned in current fixtures
- `selfcheck.py:186-187`. Any expectation string without `/` compares `Path(raw).name` only.
- `selfcheck.py:189-191` is the only place subdirectories are checked, and only for slash-bearing expectations.
- Current fixtures using slashless expectations:
  - `negative-fixtures.json:234` (`corrupt-diff-still-selected`): `"selected_diff": "go1.21.2.json.diff"`. Selection could place this diff at the root or any other folder and the case still passes. The case exists to exercise `patchverdiffs/`, and it does not assert that folder. This is a real non-detection gap.
  - All positive `base` expectations: `selection-fixtures.json:41, 66, 89, 112, 137, 165, 192, 219` (`{"path": "go1.2X.0.json"}`). A regression reporting the base as `typeinfo/golang/go1.21.0.json` or any nested path passes these. `wrong-root-layout-files-nested` (negative-fixtures.json:98-108) catches only the nested-acceptance regression, and only through `missing_base`.
- Reachability: reachable now for `corrupt-diff-still-selected`. Current selection output is correct, so this is a detection gap, not a present false pass.
- Fix direction: drop basename mode and always compare the root-relative POSIX path. All current expectations are root-relative (`go1.21.0.json`, `patchverdiffs/...`), so this is free for them; only `negative-fixtures.json:234` needs a value change to `patchverdiffs/go1.21.2.json.diff`. `SelectorRunner.md:19-24` and `SelectorFixtures.md:37` document basename mode as intentional. That is a design call for L1.

### F3. Expectations for forced keys are silently discarded
- `selfcheck.py:231-233`: `patch_applied` and `evidence_class` in `expected` are skipped (`continue`). The forced check at 224-230 only validates the forced values (`False` / `"source_model"`).
- A fixture asserting `"patch_applied": true` or `"evidence_class": "provider"` passes whenever the forced value holds. The author's expectation is recorded as satisfied and never compared.
- Reachability: latent. Every current occurrence of these keys is `false` / `"source_model"` (selection-fixtures.json and negative-fixtures.json, grep-verified).
- Fix direction: compare the author's value to the forced value, or fail the case with a schema error when they differ.

### F4. The non-empty positive-case guard counts forced keys
- `selfcheck.py:303-307` checks `not expected`. `{"patch_applied": false, "evidence_class": "source_model"}` is non-empty, passes the guard, and after F3 asserts nothing that depends on the selection result. Any dict-returning `select_snapshot` passes.
- Reachability: latent. No current fixture has this shape.
- Fix direction: require at least one key outside `FORCED`.

### F5. `expect_error` matching is vacuous for empty or generic specs
- `selfcheck.py:268-283`:
  - `expect_error: ""` (string): line 274 `"" in name` is always true; any exception passes.
  - `expect_error: {"type": ""}`: line 278 `"" not in name` is false; line 282 returns true; any exception passes.
  - `expect_error: true` (269-270): any `Exception`, including `AttributeError`/`TypeError` from a bug in `selection.py`, passes.
  - Generic substrings such as `"Error"` pass any `*Error`.
- Reachability: latent for current fixtures. The eight current error negatives (`negative-fixtures.json:10, 21, 32, 43, 54, 65, 76, 87`) use `{"type": "RequestError"}` or `{"type": "UnreadableError"}` with no `contains`. A `RequestError` raised from any branch of `parse_request` passes, so these cases cannot tell which rejection rule fired (e.g. `1.21.-1` at `:65` vs `1.21.0+bad` at `:54`).
- Fix direction: reject empty strings and empty `type`/`contains` in `_error_ok` with `FixtureError`. Add `contains` to error negatives with a stable message substring. Treat `expect_error: true` as a schema error or document it as weak.

### F6. Null or absent `files`, and null `goos`/`goarch`, are silently accepted
- `selfcheck.py:122-123`: `files: null` is treated as an empty tree and returns without error. A typo in a `missing_base` positive case passes vacuously.
- `selfcheck.py:296-297`: `goos: null` / `goarch: null` reach `selection.arch_search_order` (`selection.py:111-114`) and raise `RequestError`. Under an `expect_error: {"type": "RequestError"}` case, a null typo passes for the wrong reason.
- Reachability: latent (no current fixture uses null for these keys).
- Fix direction: only absent `files` means empty tree; `files: null` raises `FixtureError`. Validate `goos`/`goarch` as non-null strings in `run_case`.

### F7. Harness crashes on malformed content instead of exit 2; exit codes contradict the docstring
- `selfcheck.py:133-136`: `base64.b64decode(content["raw_b64"])` is not wrapped. A non-string value raises `TypeError`; invalid padding raises `binascii.Error`. Neither is a `FixtureError`, so `main` (`:386-390`) does not catch them. The whole run dies with a traceback (exit 1), skipping later cases and the summary.
- `selfcheck.py:120-156`: `files: {".": ...}` maps to `root / Path(".")`. `Path(".").parts == ()` passes the `..` check at 130, so `write_text` hits `IsADirectoryError`. A parent collision (`"a": "x"` plus `"a/b": "y"`) raises `FileExistsError`/`NotADirectoryError`. All uncaught.
- `selfcheck.py:278-281`: non-string `type` or `contains` in `expect_error` raises `TypeError` (`t not in name`, `c not in msg`). That call sits inside `run_case`'s exception handler (`:316`), so it escapes the same way.
- `selfcheck.py:387-390`: a per-case `FixtureError` prints `FAIL ... fixture error` and counts as a failure, so the exit is 1. The module docstring (`:63-64`) says exit 2 is for "malformed case schema". Per-case schema errors and the crashes above all yield exit 1, which an outer receipt cannot distinguish from a mismatch.
- Fix direction: wrap `_materialize` and `_error_ok` internals so every schema problem raises `FixtureError`; `main` returns 2 on any `FixtureError` regardless of position.

### F8. Duplicate case IDs and duplicate JSON keys are not rejected
- `selfcheck.py:384-398`: the schema says `id` is unique, but no uniqueness check spans multiple `--fixtures` files. Duplicate ids produce ambiguous output.
- `selfcheck.py:106-117` uses default `json.loads`. A duplicated key inside `expected` silently keeps the last value, so a duplicate can hide a wrong expectation.
- Reachability: latent. The current two files have disjoint id sets (checked by reading the id fields).
- Fix direction: `object_pairs_hook` to reject duplicate keys; a seen-set of ids in `main`.

### F9. Dead and misdescribed relative-path branch
- `selfcheck.py:189-191`: `select_snapshot` emits already-relative paths (`selection.py:119-141`; `_describe_file` returns `relative_to(root)`). `Path(raw).relative_to(root)` with an absolute temp root therefore always raises `ValueError`, and the code falls back to `str(raw)`, which is the relative spelling.
- The result is correct only because of this fallback. The docstring at `selfcheck.py:177-181` and `SelectorRunner.md:24` describe an "absolute spelling" fallback that the code does not produce for real output.
- Impact: none on verdicts; it misleads a future reader about which path form is compared.
- Fix direction: after F2, compare `Path(raw).as_posix()` directly and delete the branch.

### F10. Bool/int equality leak in `_match`
- `selfcheck.py:207-213`: booleans compare by identity only when the *expected* side is bool. An expected `0` or `1` accepts `False` / `True` (Python `0 == False`). The docstring (`:60-61`) says booleans compare by identity, not truthiness; the reverse direction is not covered.
- Reachability: latent. No count or `selected_patch` field can carry a bool in current selection output.
- Fix direction: reject `isinstance(actual, bool) != isinstance(expected, bool)`.

### F11. `selection.py` silently demotes an unreadable or non-directory `patchverdiffs/` to "no diff"
- `selection.py:218-222`: `except OSError: entries = []`. A permission-denied directory, or a `patchverdiffs` that is a regular file (`NotADirectoryError`), yields `base_only` with exit 0.
- The module contract (`selection.py:66-67`, `:294-300`) says unreadable input where reading is required exits 2. This branch contradicts that without a comment explaining the choice.
- Possible source mirroring: Java `File.exists()` returns false on similar failures, so base-only may be the intended mirror. That is `[INFERENCE]`; the Java behaviour was not verified here (out of lane).
- Coverage: the fixture schema (`selfcheck.py:20-33`) has no mode/permission field, so the permission case cannot be exercised. A plain-file `patchverdiffs` (`:145-150`) can reach this branch, but no current fixture does. A regression here is currently undetectable.
- Fix direction: decide explicitly. Either raise `UnreadableError` for non-ENOENT errors, or document the `exists()` mirroring and add a fixture where `patchverdiffs` is a plain file.

### F12. `controls.py` source-row registry collapses duplicate IDs (hides immutable-cell changes)
- `controls.py:136-150`: `source_rows` builds a dict keyed by source ID. Duplicate `S###` rows silently overwrite earlier ones (last wins), and `rows_before`/`rows_after` (`:236-237`) count dict keys, not rows.
- Concrete miss: before `[S010 X, S010 Y]`, after `[S010 X', S010 Y]`. Both reduce to `{S010: Y}`, so `immutable_cells_unchanged` (`:238`) stays true though row X changed.
- Fix direction: `fail` on duplicate IDs in either revision.

### F13. `controls.py` handles absent-at-before inconsistently
- `controls.py:153-160`: `prefix_report` calls `before.get(path)`, which runs `git show` and `fail()`s (exit 2, "cannot read") when the path is absent at before. Absence at after is reported as data (`missing_at_after`).
- `controls.py:169-175` (`unchanged_report`) reports absent-at-before as data (`absent_at_before`).
- Impact: a missing `LOG.md` at the before revision is fatal in one helper and a reported observation in the other. The docstring (`controls.py:16-20`) reads exit 2 as "missing structural anchor", so the behaviour is defensible under one reading, but the two helpers disagree. Low.

## Bounded no-findings (checked, not defective)
- Forced-invariant comparison with sentinel (`selfcheck.py:224-230`) correctly fails on a missing `patch_applied`/`evidence_class`.
- Missing top-level expected keys are detected (`:261-263`); typoed sub-keys inside `base`/`selected_diff` dicts are detected (`:246-247`).
- Non-str/non-bool/non-None expectations for path keys are rejected (`:257-259`); list ordering is pinned by equality (`:212`) for `arch_search_order` and `base_matching_buckets`.
- `_materialize` rejects absolute and `..` names (`:127-131`); each case runs in a fresh temp root.
- Slash-bearing `selected_diff` expectations do pin the subdirectory: `selection-fixtures.json:42, 67, 220`.
- `run_case` compares after the `TemporaryDirectory` context exits (`:320-326`). Harmless: `_path_cmp` is purely lexical and `_describe_file` already hashed the bytes.
- Positive cases with empty `expected` and no `expect_error` are rejected (`:303-307`).

## Verification gaps
- Nothing executed (contract). All findings are from source trace; no runtime observation.
- F11's Java equivalence is unverified here.
- Negative-fixture expectations were checked for internal consistency against the source-model rules, not against Java behaviour.
- Permission-based selection branches cannot be exercised by the fixture schema; that is a coverage limit, not a verified behaviour.
