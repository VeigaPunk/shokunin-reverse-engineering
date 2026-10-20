# Round-16 wave-2 falsification: C1/C2 artifacts (FReportEvidence)

Scope: advisory audit of produced round-16 C1 (selection) and C2 (outside-route repairs) artifacts, read-only. No tests, builds, linters, formatters, or selfcheck/measure/controls runs were executed; all results below are source reading, grep-verified Java anchors, and hand traces. Expected-value checks are hand traces, not executions. L1 executes once after integration.

Tooling: none installed or updated. No pacman transaction. Only `readlink -f /usr/bin/python3` (-> python3.14) was run, to determine the CPython version for finding F1.

## Draft claims (concise)

- **C1 (depth).** For one supplied golang root and one strict stable `M.m.p` request, `selection.py` reports: the patch-0 base file (`go<M.m.p0>.json`), the nearest present same-minor diff with patch in `1..request`, selected patch, ordered base-bucket names, and raw path/size/SHA-256 for base and diff. `patch_applied` is `false`. `status` names a filename selection only, never patched content.
  - Limit: one root only (no Ghidra module-data search order). No diff is parsed or applied. Bucket membership is by top-level key only.
- **C2 (calibration).** The four round-15 routed items each have a present current artifact: (1) append-only `Round-16 correction` in the r15 knowledge entry with the `python3 -I` absolute argv; (2) SKILL.md:450 quote-fidelity row cites `.ufo/waves/round-15/boundary-fixtures/expected.json`; (3) `controls.py` emits argv/orig_argv; (4) SHONEN box 3 names 2026-10-15. QUALITY #18 is added.
  - Limit: all are presence/byte proxies. `measure.py` (the C1/C2 tally script) carries no producing argv. The invocation predicate is loose (F5).

## Per-axis limits

- **Depth:** source-law fidelity is strong (see No-finding list). The depth ceiling is the single-root model, unapplied diffs, and key-only bucket validation. Live `--request 1.24.5` evidence does not yet exist (F11).
- **Calibration:** `documentation-red.json` is presence-only (its own label says so). `measure.py` predicates are proxies. Current prose ("exercised", "exit 2 = invalid") outruns the artifacts in two places (F1, F11).

## Findings (ordered by severity)

### F1 — crash path escapes the documented exit-2 contract (defect, high confidence)
- `selection.py:83` calls `int(m.group(i))` **before** the length guard at `:86-91`. The comment at `:84-85` says the length check happens before `int()` and explicitly notes that `int()` on a >4300-digit string raises `ValueError`. The code does the opposite.
- `_VERSION_RE` (`:50`) accepts a canonical 5000-digit component, so `int()` raises `ValueError`.
- `main()` (`:289-295`) catches only `RequestError` and `UnreadableError`. The result is a traceback and exit 1, not the exit 2 JSON that the contract, `knowledge/2026-10-20-r16-go-selection-preview.md:34`, and SKILL.md:506 promise.
- Runtime: `/usr/bin/python3.14` (default int-str digit limit 4300, [INFERENCE] from CPython docs, not executed).
- Fix: move the length check before `int()` or catch `ValueError` in `parse_request`. Fix the comment.
- Handwritten fixture that would catch it (expected values only): a `negative-fixtures.json` case with `"request"` = the literal string `1.` + 5000 nines + `.0` (write the digits out in the JSON), `"expect_error": {"type": "RequestError"}`. Today it fails with `unexpected exception ValueError`. Companion boundary: `"request": "1.21.99999999999"` (11 digits) → `RequestError`, which the length guard already satisfies.

### F2 — other OSErrors escape `main`; unreadable diff dir silently means "no diff" (defect, medium; [INFERENCE] from pathlib semantics)
- `_describe_file` calls `path.is_file()` (`selection.py:125`) and `select_snapshot` calls `root.is_dir()` (`:186`) outside any try. `pathlib` ignores only ENOENT/ENOTDIR/EBADF/ELOOP; EACCES/EPERM propagate. `main` does not catch them → traceback, exit 1.
- `selection.py:215-217`: `iterdir()` `OSError` is swallowed to `entries = []`. An existing but unlistable `patchverdiffs/` yields `base_only` with exit 0 and no disclosure. That is a silent degrade in an evidence-producing probe.
- Fix: wrap these in `UnreadableError`; for `patchverdiffs/`, raise `UnreadableError` when the directory exists but cannot be listed.

### F3 — harness exit code for malformed case schema is 1, not 2 (defect, medium)
- `selfcheck.py:384-390`: a per-case `FixtureError` (malformed case, bad filename, empty expected) is printed as `FAIL ... fixture error` and the loop continues. Final return is `1` (`:399`).
- Contract text, `selfcheck.py:63-64`: "2 on harness-level failures (... malformed case schema)".
- Fix: abort with 2 on `FixtureError` from `run_case`, or count it separately.

### F4 — documented self-invocation never runs negative fixtures (defect, medium; doc/code drift)
- `selfcheck.py:81` and `:368-369`: default fixture set is `selection-fixtures.json` only.
- SKILL.md:506 documents `python3 -I .../selfcheck.py` with no `--fixtures`, so the 17 negative/boundary cases in `negative-fixtures.json` are not exercised by the documented command.
- The selfcheck docstring (`:17-18`) shows the two-file form. Either the SKILL row must pass both `--fixtures` flags, or the default must include both.

### F5 — C2 invocation predicate binds to the wrong anchor (calibration defect, medium)
- `measure.py:109-114` takes the first line matching `(?im)^.*correction.*$`. That is `r15 knowledge line 39` ("Named correction: round-14 lesson…"), not the `## Round-16 correction` heading at line 76. The section runs to EOF.
- It then matches `ISOLATION_FLAG` on the backticked `` `-I` `` at line 80 and `ABS_R15_SCRIPT` at line 83. So the field passes even if the Round-16 heading is absent, as long as prose and the command block remain.
- `documentation-red.json` uses the stricter `'Round-16 correction' in kn` predicate. The two disagree, so `C2_named_r15_correction_isolated_absolute_recheck` is not a reliable red→green witness.
- Fix: anchor the trigger to `^## Round-16 correction`.

### F6 — structural tallies in `measure.py` carry no producer (QUALITY #18 gap, medium)
- QUALITY row 18 (`corpus/QUALITY.md:28`) and `lessons/round-16.md:56` require structural/no-harm tallies to retain the producer and immutable inputs.
- `controls.py:281-295` does this (argv, orig_argv, executable, producing_command). `measure.py:127-157` emits C1/C2 booleans and tallies (`knowledge_files`, `mapped`, `sources_rows`, `tiers`, `statuses`) with no argv, executable, or command field. It does carry `revision`.
- `documentation-red.json`'s `producing_command_retained` predicate checks only `'argv' in controls.py`, so it cannot detect this.
- Fix: add the same `invocation` block to `measure.py`.

### F7 — C1 boundary fixtures have no presence field in measure (coverage gap, low)
- `measure.py:127-151` has `C1_selection_fixtures` and `C1_selection_selfcheck` but no `negative-fixtures.json` field, even though SKILL.md:506 and the knowledge entry rely on the negative file.

### F8 — dead constant (low)
- `controls.py:33` `OLD_PREFIX_DIRS` is defined and never used. `main` (`:264-267`) uses the literal strings. Delete it or use it.

### F9 — error-path `status` collides with the success namespace; extra keys beyond the wave contract (low)
- `selection.py:292` emits `{"status": "invalid_request" | "unreadable_input"}` on exit 2, in the same key that carries `missing_base/base_only/exact_diff/fallback_diff`.
- Success results also add `request_raw`, `goos`, `goarch`, `base_matching_buckets_source` (`:253-270`) beyond the wave-contract key list. These are additive and disclosed, but a consumer keyed on `status` can misread the error object. Consider `error` as a separate top-level key.

### F10 — `_match` lets expected `0` accept actual `False` (harness weakness, low)
- `selfcheck.py:207-213`: the identity rule applies only when the expected value is a bool. An expected int `0` (e.g., `selected_patch`) equals actual `False` because `False == 0`.
- No current implementation path emits `False` there, so this is latent. Fix: type-strict compare for non-bool expected values.

### F11 — claimed "exercised" evidence does not exist yet (calibration, medium; pending L1)
- `lessons/round-16.md:73` says "the exercised contrast includes 1.24.5→patch 5 despite installed patch 6". No fixture covers request 1.24.5, and `.ufo/waves/round-16/verification.json` does not exist in this snapshot.
- The same nonexistent file is cited as the retained execution record in `knowledge/2026-10-20-r16-go-selection-preview.md:3` and SKILL.md:506.
- Data check is real: `patchverdiffs/go1.24.5.json.diff` and `go1.24.6.json.diff` both exist in the installed tree (glob, read-only).
- Suggested handwritten fixture (no hashes): `request` `1.24.5`; files `go1.24.0.json` `{"all":{}}`, `patchverdiffs/go1.24.5.json.diff` `{}`, `patchverdiffs/go1.24.6.json.diff` `{}`; expected `status` `exact_diff`, `selected_patch` `5`, `selected_diff` `go1.24.5.json.diff`, `base` `go1.24.0.json`, `base_matching_buckets` `["all"]`.
- Until L1 runs and retains output, wording must say "planned/pending", not "exercised".

### F12 — preview status and exit 0 for buckets Java would fail to load (disclosed limit, low–medium)
- `negative-fixtures.json` case `unsupported-shape-bucket-nonobject-preview` expects `base_only` with `all` retained when `all` is a JSON array. Java's Gson read at `GoApiSnapshot.java:222` would fail on that bucket.
- The fixture note and knowledge entry line 38 disclose this. Still, `status: base_only` with exit 0 reads as a usable projection.
- Suggest an explicit `bucket_values_validated: false` (or `bucket_shape_checked: false`) field so the limit is machine-readable.

### F13 — `controls.py` robustness (low)
- `controls.py:71` decodes `ls-tree` output as UTF-8 text; a non-UTF-8 path raises `UnicodeDecodeError` (exit 1, not documented exit 2).
- `controls.py:143-150` `source_rows` silently overwrites duplicate source IDs.
- `controls.py:163-165` reports `appended_bytes` even when `prefix_preserved` is false, which misreads as append evidence.

### F14 — QUALITY #18 "supersedes" column (process, low)
- `QUALITY.md` header (lines 4-5) reserves the supersedes column for "a new row naming the row it supersedes". Row 18 supersedes nothing; its column reads "sharpens 1, 6". Either use "—" with the sharpening stated in the criterion, or define the column value.

## Fixture and source-law check (bounded no-finding)

- `IS_GOOS_UNIX` (12 members, `selection.py:42-45`) matches Java `GoApiSnapshot.java:180-181` exactly.
- Arch order `[goos-goarch, goos, unix?, goarch, all]` with empty slot dropped matches `:108-109` and `read:229-232`.
- Base-first: missing patch-0 base returns before diff search, matching `:122-126`. `selection.py:190-199` ✓.
- Diff scan: `0 < cand <= patch` within the same minor matches `getPatchVerDiffFile` loop `:153-155`. Patch 0 never probes, matching `:153`.
- Legacy two-part `getApiFile` (`:183-192`) is not reproduced; `selection.py` never calls it.
- Regex strictness rejects `1.21`, `1.021.0`, `v1.21.0`, `1.21.0.1`, `1.21.0+bad`, `1.21.-1`, and `0.0.x`.
- No path traversal: request is fully validated before any path is built, and `goos`/`goarch` never reach a path.
- Hand-traced all 9 positive and 17 negative/boundary cases in `selection-fixtures.json` and `negative-fixtures.json` against `selection.py` logic. No expected value mismatches found. Mental trace, not executed.
- Java anchors cited in the knowledge entry and fixture notes were grep-verified (line-numbered grep on `Base-src.zip:GoApiSnapshot.java`): `return read` 111; `getApiSnapshotJsonFile` 118-131; `getPatchVerDiffFile` 148-155; `getApiSnapshotFile` 168-176; `IS_GOOS_UNIX` 180-181; `getApiFile` 183; `read` 205-222; `reader.beginObject` 215; `archNamesToKeep` 212-218; empty-name skip 230; `JsonPatch.read` 136. One exception is F-note below.
- Anchor error (low): `negative-fixtures.json` case `missing-base-empty-root` note says "getApiSnapshotFile returns null at GoApiSnapshot.java:171". The null return is the `catch (IOException e)` branch at `:175-176`. Fix the note.
- r15 correction: `verification.json` argv (`:46-49`) is `python3 -I …`; revision `7ad23fe1735cd868ec203d93deb13bb2c42889ad` matches (`:2`); the quoted "ran twice" sentence is at knowledge line 52 ✓.
- SHONEN box 3 is `[~] Instructions executable…` (line 9); the measured line (line 10) names `2026-10-15` and lacks "this round" ✓.
- SKILL.md:450 quote-fidelity row contains `.ufo/waves/round-15/boundary-fixtures/expected.json`, and that file exists ✓.
- `corpus/lessons/round-16.md` exists and has a Mistakes table; QUALITY row 18 cites it ✓.
- `documentation-red.json` predicates (`'Round-16 correction' in kn`, the SKILL row path check) are stricter than measure's for the corresponding items, as F5 notes.

## Out of scope / not verified

- No Ghidra execution, no outside verifier run, no target work.
- Did not verify whether the r15 knowledge file is strictly append-only vs baseline bytes; that is `controls.py` `old_knowledge_prefix`, for L1 to run.
- F1 and F2 runtime behaviour is a [INFERENCE] from CPython documentation and source reading. L1 should confirm with one isolated invocation, e.g. `python3 -I selection.py --root <golang> --request 1.<5000 nines>.0 --goos linux --goarch amd64` (expected: traceback today, exit 1).

## Recommendations for L1 (verify once after integration)

1. Confirm F1 and F2 with the two isolated invocations above.
2. Run `selfcheck.py` with both fixture files (the F4 form), and confirm the handwritten F11 and F1 cases.
3. Run `measure.py` and `controls.py` against the baseline and after revisions; compare F5 and F6 fields.
4. Either create the `verification.json` retained record for round-16 or change the three "pending" references (F11).
