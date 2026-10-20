# FMistakeAudit — round 16 wave 2 (advisory, leaf)

Scope: attack the produced C1 (selection.py, selfcheck.py, fixtures) and C2 (four routed duties) artifacts. Advisory only; no corpus, implementation, or LOG edits; no new corpus entry.

Marker legend: [OBSERVED] read in this turn at the cited anchor · [INFERENCE] derived from source reading, not executed · [NOT EXECUTED] nothing here was run as a test, build, lint, or verification.

## Execution boundary and audited snapshot

- No selection.py, selfcheck.py, controls.py, or fixture was executed. No tests, builds, linters, formatters, or verification runs. No installs or upgrades (none needed); no pacman.
- Read-only commands used: file reads, `git diff`/`git show` on the working tree and HEAD, `unzip -p` of `Base-src.zip` (source read only), `sha256sum`, and a JSON parse of `round-15/boundary-fixtures/expected.json`.
- Files were being rewritten by sibling seats during this audit (selection.py 302→307 lines; selfcheck.py 403→414 lines; mtimes 05:20–05:22). Findings below are against the 2026-10-20 08:23Z snapshot. L1 must re-hash before its single run.

| file | sha256 (08:23Z) |
|---|---|
| selection.py | 1d2907b323883129d4e5c4ddb3415a1998947dcb2c4ecde625b8868996544848 |
| selfcheck.py | f5c20c57cb87fee90f54b4f139c3c2bcf3cac8924d5acfd69ed04099df00a20b |
| controls.py | 5f9fe949d5a3ed3ff9116fec67774dc2e4fabc05c6d58242fa1ca7e7c159a917 |
| selection-fixtures.json | ff2483d88ad77a39ef5fb2f6ad7310ba6d940094debe03dc6daa0e8b802fcaaa |
| negative-fixtures.json | a92b3abbe878bc6aace5f9345f9266288556f4dd2a49abcb6f74971a78e4da9c |

Source anchor: Ghidra 12.1.4 `Base-src.zip` member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` [OBSERVED]. Line anchors: get() 102–116, arch list 108, getApiSnapshotJsonFile 118–, base-patch-0 122, null base 124, null diff 129, getPatchVerDiffFile 148, getApiSnapshotFile 168, IS_GOOS_UNIX 180–181, read() 205–, arches.put 223, results loop 229–235, `arch != null` 234.

## Part 1 — C1 defects (selection.py / selfcheck.py)

Ranked by impact. Severity is my judgment.

### F1 — selfcheck exit code contradicts its own contract (medium; high confidence) [OBSERVED]
- `selfcheck.py:399-401`: a per-case `FixtureError` (malformed case schema) prints `FAIL … fixture error` and `continue`s.
- `selfcheck.py:410`: returns `0 if npass == len(cases) else 1`, so a malformed case yields exit 1.
- Docstring `selfcheck.py:63-65` says exit 2 covers "harness-level failures (… malformed case schema)".
- Fix: count fixture errors separately and return 2 when any occurred. Do not fold them into the mismatch count.
- Fixture to add: none needed for the fix itself; a malformed-case fixture would pin it (for example a case with `expected: {}` and no `expect_error`, which should exit 2).

### F2 — bucket applicability ignores JSON-null values; source excludes them (low–medium; medium confidence) [OBSERVED anchors / INFERENCE on Gson]
- `selection.py:242` builds `keys = set(_top_level_keys(...))`, so key presence alone decides membership. Buckets at `:245-248` are then listed.
- Source: `GoApiSnapshot.java:222-223` stores every requested key's parsed value via `arches.put`, and `:229-235` keeps only `arch != null`.
- [INFERENCE] Gson's reflective adapter returns null for a JSON `null` token, so a null-valued bucket would be dropped by the source but reported as a match by the preview. This is inferred from Gson behavior and was not executed.
- Impact: `base_matching_buckets` (the C1 "ordered base-bucket applicability" claim) can overstate a bucket that the source never retains.
- Fix: derive membership from values, e.g. `{k for k, v in doc.items() if v is not None}`. Requires `_top_level_keys` to return values or a second pass.
- Hand-authored candidate fixture (expectation from source reading, not from execution): files `{"go1.21.0.json": {"all": {}, "linux": null}}`, request `1.21.0`, goos `linux`, goarch `amd64`. Expect `status: base_only`, `selected_patch: 0`, `base_matching_buckets: ["all"]`. This is an expectation from reading, not a verified result.

### F3 — unreadable patchverdiffs directory silently becomes "no diff" (low–medium; calibration) [OBSERVED]
- `selection.py:219-222`: `diff_dir.iterdir()` `except OSError: entries = []`. An existing but unreadable `patchverdiffs/` yields `status: base_only`, exit 0.
- Contrast: an unreadable diff *file* raises `UnreadableError` (`selection.py:138-139`), and the module contract says unreadable input exits 2 (`selection.py:294-300`).
- The output then asserts absence of a diff that was never observed.
- Source note [INFERENCE]: `getApiSnapshotFile` (GoApiSnapshot.java:168–177) catches `IOException` and returns null, so the source also treats failure as absence. A faithful preview could mirror that, but then it must say "diff_dir_unreadable" in the output rather than present base_only as observed.
- Fix options: (a) raise `UnreadableError` for any `OSError` except `FileNotFoundError`/`NotADirectoryError`; or (b) keep the source-faithful absence and add an explicit `diff_dir_status` field. Choose one and pin it; do not leave it silent.

### F4 — `_match` treats numeric expectations as bool-equal (low; calibration) [OBSERVED]
- `selfcheck.py:218-223`: only a *bool* expectation uses identity. A non-bool expectation falls through to `!=`, so expected `1` matches actual `True` and expected `0` matches `False` (Python `1 == True`).
- The docstring (`selfcheck.py:59-61`) says booleans compare by identity, which is only true for bool expectations.
- Impact: the harness can pass a case whose result is a bool where the expectation is an int. No current fixture hits this, so it is latent.
- Fix: in `_match`, reject bool/int cross-type equality, e.g. `type(actual) is not type(expected)` for scalars.

### F5 — fixture coverage gaps (medium for regression; not a defect in the code)
- No fixture guards the length-before-int ordering at `selection.py:83-96`. The current file is correct there (length check precedes `int()`), but nothing would catch a regression. The earlier snapshot (05:10–05:20 reads) had `int()` before the length check, with a comment claiming the opposite; that is fixed in the current file [OBSERVED].
- Hand-authored negative candidates (expectations only; not run): request `"9"*11 + ".0.0"` → `RequestError`; request `"1"*5000 + ".0.0"` → `RequestError`. The second case fails on an un-guarded `int()` with `ValueError`, which the runner reports as "unexpected exception", so it has teeth.
- No fixture covers F2 (null bucket) or F3 (unreadable diff dir). F3 cannot be expressed in the current schema (no permission field), so it stays a documented limitation.

### F6 — low notes (no action required)
- `selfcheck.py` `_materialize`: a JSON-object file whose top-level key is literally `raw` or `raw_b64` is treated as a directive, not content. Real Go arch names cannot collide, so this is latent only.
- `selfcheck.py` `main`: duplicate case ids across fixture files are not detected; output lines would be ambiguous.
- `selection.py` `select_snapshot` docstring labels bucket computation as "unpatched base file" and the output carries `base_matching_buckets_source`. Adequate; no defect.

## Part 2 — No-finding (bounded)

- Arch search order and `IS_GOOS_UNIX`: match `GoApiSnapshot.java:108-109` and `:180-181` for the unix/linux/darwin/windows cases exercised by fixtures [OBSERVED].
- Diff selection: candidate filter `0 < cand <= patch` in the same minor, descending first-present, equals the source loop in `getPatchVerDiffFile` (`:148-166`) for the stable-version domain accepted by `parse_request` [OBSERVED / INFERENCE on equivalence over readable files].
- Hand-check of all 9 positive and 17 negative fixture expectations against the current `selection.py` logic: no disagreement found. Expectations were not executed.
- `controls.py` craft replication: `controls.py:110-133` matches SCORECARD command A (`SCORECARD.md:92-123`, lines 103–117) on pattern, split, range, bare-citation defaults, and missing-file handling. Bounded: replication only, not a semantic audit (as its own docstring says).
- `SOURCES.md` immutable-cell check: the working-tree diff changes S003 and S023 only at cell index 11 (`used-by`). Row count 23→23, no added or removed rows. Immutable cells unchanged [OBSERVED].

## Part 3 — Four routed duties (C2): evidence / captured-by / fix / marker limit

Routing source: `corpus/lessons/round-15-verifier-spotcheck.md:185-188` [OBSERVED].

| # | Routed duty | Evidence in working tree | Captured-by (red-before) | Fix status | Marker limit |
|---|---|---|---|---|---|
| 1 | `-I` invocation consistency | `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md` gained a 17-line append-only section "Round-16 correction" (diff: 0 deletions). Its argv matches the `verification.json` record (`--ghidra`, `--select 1.24.7 1.25.7 1.26.8`; absolute script path) [OBSERVED]. SKILL.md go-snapshot-inventory row updated in place to `python3 -I` plus absolute path. | `.ufo/waves/round-16/documentation-red.json` at baseline `6235498`: `invocation_correction: false`, resolved 0/4, exit 1 [OBSERVED]. | Applied. | Text-level correction only. The `-I` spelling was not re-executed; retained stdout is round-15 bytes. Correction states it is "not a claim of equivalence" with the old spelling. [NOT EXECUTED] |
| 2 | Supplemental frozen baseline discoverability | SKILL.md quote-fidelity row now cites `.ufo/waves/round-15/boundary-fixtures/expected.json`. File exists and parses (keys `manifests`, `sources`) [OBSERVED]. | Same red file: `supplement_discoverable: false` at baseline. | Applied. | The row's claim that the file runs "with the same script's `--frozen` flag" is not evidenced by the pinned file, which states no command. [INFERENCE] Only other supplemental baselines were not enumerated by me. |
| 3 | Producing commands for controls | `controls.py:13-15` docstring and `:281-295` `invocation` block: `argv`, `orig_argv`, `executable`, `isolated`, `producing_command` [OBSERVED]. SKILL row `round16-structural-controls` says argv and revisions are retained. | Red file: `producing_command_retained: false` at baseline, where controls.py was absent. | Applied. | The red check is substring-only (`'argv' in co`), so it does not prove the field exists in output. L1 should read the emitted JSON `invocation` block, not rely on the check. Retention depends on the caller storing stdout. The round-15 boolean remains without its own command, as intended (append-only). |
| 4 | Historical SHONEN wording | SHONEN.md box 3: "this round" → "historical 2026-10-15 operator-steered round 1". Label supported by `corpus/lessons/2026-10-15-round-1.md:1` ("operator-steered r1") [OBSERVED]. `[~]` marks unchanged. LOG.md diff has a route-4 entry [OBSERVED]. | Red file: `historical_shonen: false` at baseline. | Applied. | Lesson line 190 notes SHONEN is canonical-seed regenerated, not append-only; the change is disclosed in LOG. No new `[x]` authority. |

Discovered historical-gate items (correction candidates, not new entries):

- D-a. SKILL.md go-selection-preview row says execution results are "retained in `verification.json`". `.ufo/waves/round-16/verification.json` does **not** exist at 08:23Z [OBSERVED]. This is a forward reference. L1 must create it from its single run, or the row must be corrected. Pending, not failed.
- D-b. The round-15 `recheck:` at `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:3` remains the non-isolated spelling by design (append-only; the correction is appended beneath). Keep it.
- D-c. QUALITY.md criterion 18 (new row) cites the lesson and the four routes; it sharpens 1 and 6 as stated. Consistent with the four-route table above [OBSERVED].

## Part 4 — Summary of concrete defects to fix before L1 run

1. F1 selfcheck exit code (`selfcheck.py:399-410`): fixture errors must exit 2. High confidence.
2. F2 null-bucket membership (`selection.py:242-248`): derive from values; add the hand-authored fixture above. Medium confidence on the Gson inference.
3. F3 silent unreadable diff directory (`selection.py:219-222`): raise or label. Calibration choice.
4. F4 bool/int cross-equality (`selfcheck.py:218-223`): tighten scalar comparison. Low.
5. F5 add digit-length negative fixtures (hand-authored expected `RequestError`). Regression guard.
6. D-a create `verification.json` at L1 execution or correct the SKILL row.

No tool installs, updates, or upgrades were made or required by this audit.
