# FCriterionGrounding — round 16 wave 2 (source-read attack on QUALITY #18 and the four outside-route closures)

Scope: `corpus/QUALITY.md` row 18, `corpus/lessons/round-16.md` (Mistakes, route links), the four routed duties at `corpus/lessons/round-15-verifier-spotcheck.md:181-188`, and the produced C1/C2 artifacts under `.ufo/waves/round-16/` (`selection.py`, `selfcheck.py`, `controls.py`, fixtures, `documentation-red.json`). Source reads only: no tests, builds, linters, formatters, selection runs, selfcheck runs, controls runs, or verification. No installs or updates. Baseline `6235498b4112350eebce0812a74af1781fc0ee88`.

Snapshot caveat: during this read other seats changed the wave files. The bytes cited below are the versions I read: `selection.py` `#C295` (the earlier `#58BF` read is superseded; its int-before-length defect is repaired), `selfcheck.py` `#C53D`/`#EEF6` (bytecode guard present; the loader sets `sys.dont_write_bytecode`, lines 108-113), `controls.py` `#9C9A` (unchanged). Nothing is committed: `SKILL.md`, `SHONEN.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `LOG.md`, and the r14/r15 knowledge entries are modified; `corpus/lessons/round-16.md`, `corpus/knowledge/2026-10-20-r16-go-selection-preview.md`, and `.ufo/waves/round-16/` are untracked.

## Verdict

- QUALITY #17 is unchanged. The only QUALITY hunk against baseline is one added line (row 18) after row 17 (`git diff 6235498b -- corpus/QUALITY.md`: no removed or changed line).
- The lesson link resolves. `corpus/lessons/round-16.md` exists (an earlier glob missed it), and its Mistakes table rows 54-57 map one-to-one onto routes 1-4 at `round-15-verifier-spotcheck.md:185-188`.
- All four routes are present in the working tree. Route 4 (`SHONEN.md:10`) is uncommitted and HEAD still has the defective wording. Route 1's registry alignment is in `SKILL.md:487`. Route 2 is in `SKILL.md:450`. Route 3 is `controls.py`'s argv retention.
- QUALITY #18 is grounded for its core clauses but overreaches in three places (F2), and the registry row it governs fails its own "exercised argv or named variant" rule (F1).

## Verified no-finding (bounded)

- Route 1: `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:76-91` is an appended `## Round-16 correction` block. `git diff --numstat` shows 17 insertions and 0 deletions, so the prior bytes are a prefix. The correction names the exact argv at `:83`, which matches the `-I` absolute form in `SKILL.md:487`.
- Route 2: `SKILL.md:450` (quote-fidelity row, pinned-values cell) now names `.ufo/waves/round-15/boundary-fixtures/expected.json`. The `SKILL.md` diff against baseline rewrites rows 450 and 487 and appends a round-16 section (22 insertions, 2 deletions in total).
- Route 3: `controls.py:281-294` retains `sys.argv`, `sys.orig_argv`, `shlex.join`, `isolated`, and resolved revisions (`:255-260`), with `conformance_gate: false`. The historic `no-harm-controls.json` check is not relabelled as retained, consistent with `round-16.md:56`.
- Route 4 worktree: `SHONEN.md:10` now reads "historical 2026-10-15 operator-steered round 1", with box text and marks unchanged. HEAD still reads "this round executed". L1 must commit it, or route 4 is not closed.
- Source table: `corpus/SOURCES.md` S003 and S023 differ from baseline only in the `used-by` cell (field diff after splitting on `|`). No S-row was added, removed, or changed in another cell. The only other change is a journal line appended after the table.
- r14 final-sweep (`corpus/knowledge/2026-10-14-r14-02-final-sweep.md`): 12 added lines, 0 removed, a named round-16 correction.
- Positive selection fixtures (`selection-fixtures.json`, 9 cases): I traced every `expected` block by hand against `selection.py` logic (`select_snapshot`, lines 170-275 in `#C295`). Each expected status, `selected_patch`, `base_matching_buckets` order, and `arch_search_order` is consistent. Examples: `windows_omission` gives `["windows-amd64","windows","amd64","all"]` with `""` dropped; `unix_order` gives `["darwin","unix","arm64","all"]`; `minor_isolation` ignores the 1.20.9 and 1.22.1 diffs.
- Hashes: neither fixture file contains a `sha256` key (grep count 0 in both). No invented digest or pass.
- Installed data for the lesson's example: `patchverdiffs/` holds `go1.24.5.json.diff` and `go1.24.6.json.diff`, so "1.24.5 with patch 6 installed → select 5" is consistent.
- Repaired defects: the int-before-length conversion in `selection.py` (was `:83`) is fixed in `#C295` (`:83-91`). The `RecursionError` path maps to `UnreadableError` (`:157-160`).

## Findings

### F1 — Medium — registry row fails the rule QUALITY #18 imposes on it

`SKILL.md:506` (`go-selection-preview`, "Fixture check" column) documents the self-invocation `python3 -I .../round-16/selfcheck.py`. That argv runs only the default fixture file: `selfcheck.py:81` sets `DEFAULT_FIXTURES = selection-fixtures.json`, and `main()` uses it when `--fixtures` is absent. The same row's "Pinned values" cell says `negative-fixtures.json` holds hand-authored expectations, and that file has 17 cases. The documented command never exercises them. The `selfcheck.py` docstring (lines 17-18) gives the two-flag form, and the row does not label the one-flag form as a variant. QUALITY #18's first clause ("either matches the exercised isolation flags and paths or explicitly names an unexercised variant") is violated by the very row the round adds.
Fix (for L1 to choose): document `--fixtures selection-fixtures.json --fixtures negative-fixtures.json`, or label the default-only argv as an unexercised variant. Confidence: high (directly from the file text).

### F2 — Medium — QUALITY #18 has clauses beyond the lesson evidence the header requires

The QUALITY header (`corpus/QUALITY.md:3-5`) says criteria are "grown only from lessons", and each must cite the lesson that produced it. Grounded parts of row 18: the recheck-argv clause (route 1, `round-15...:185`), the structural-tally producer clause (route 3, `:187`, and `round-16.md:56`), the SHONEN historical-round clause (route 4, `:188`, narrowed), and the author-side-is-not-outside clause (`round-15...:179`; `round-16.md:24`). Three clauses go beyond the cited Mistakes rows (`round-16.md:54-57`):

1. "Execution evidence retains the producing argv/snippet, measured revision, stdout/stderr and exit" (universal over all execution evidence). Route 3 asks only for producing argv or snippet and immutable input revisions, for structural tallies. No route, row, or cited lesson line asks for output or exit capture on all execution.
2. "Every supplemental frozen baseline is discoverable from its existing gate registry row." Route 2 (`round-15...:186`) names one file, `boundary-fixtures/expected.json`. The universal has no enumeration and no check. The only control for it, `documentation-red.json` (`supplement_discoverable`), tests a single literal path substring in the `quote-fidelity` row, so it cannot discriminate "every".
3. "Promotion evidence names its historical round/date." Route 4 (`round-15...:188`) concerns SHONEN box 3's evidence line. Generalizing to all promotion evidence is not in any lesson.

Confidence: high on the text comparison; the "grown only from lessons" judgement is the header's own rule. Recommend narrowing the three clauses to what the lesson grounds, or citing additional lesson evidence, before the row is committed.

### F3 — Low — the red-before control cannot discriminate the producer clause

`documentation-red.json` (argv line 6) sets `producing_command_retained = bool(co) and 'argv' in co`, where `co` is `controls.py` at the baseline. At baseline `controls.py` does not exist, so the check is false. Any later file containing the substring `argv` passes it. It does not test that a retained output carries its own producing command, which is what QUALITY #18's first clause requires. `round-16.md:61` says the control "is able to detect the named omissions", which overstates a substring presence check. Lesson line 58 partly concedes this. Recommend that L1 label the control as presence-only in the lesson and in #18's cited "why", or replace the check with an exact-argv test. Confidence: high.

### F4 — Low/Medium — null-valued bucket keys are counted as applicable, unlike Java

`selection.py:167` (`_top_level_keys` returns `list(doc.keys())`) and `:242-248` (buckets) count any top-level key present, including a key whose value is JSON `null`. Java `read()` (`GoApiSnapshot.java:222-223`) calls `gson.fromJson(reader, GoArch.class)`. [INFERENCE: Gson's reflective adapter returns `null` for a JSON `null` token.] That stores `null`, and `:233-236` (`arch != null`) skips it. So the Java result omits the bucket, while the preview lists it in `base_matching_buckets`. Non-object values are documented as a limitation (`negative-fixtures.json`, `unsupported-shape-bucket-nonobject-preview`), but the `null` case is not in the documented limits or in any fixture. C1's claim is "ordered base-bucket applicability", so this is a real over-claim. Suggested fixture (hand-authored): `{"linux-amd64": null, "all": {}}` on linux/amd64 expects `base_matching_buckets: ["all"]`. Confidence: medium (depends on the Gson inference above).

### F5 — Low — `base_only` is reported even when the Java snapshot would be invalid

When `base_matching_buckets` is `[]`, for example windows against a linux-only base, `select_snapshot` still returns `status: base_only`. Java `read()` then returns a `GoApiSnapshot` with an empty map, and `isInvalid()` is true (`GoApiSnapshot.java:503-505`), not `EMPTY`. The preview emits no usable/invalid flag, so a consumer reading `base_only` cannot tell a usable snapshot from an empty one. The registry row's "Generic `all` can survive" line covers only the populated case. Recommend an explicit field or a documented limit. Confidence: high on the output shape; medium on how consumers read it.

### F6 — Low — an unreadable `patchverdiffs/` is silently treated as absent

`selection.py:218-222`: `except OSError: entries = []`. A permission failure on the diff directory yields `base_only` with no diagnostic. The Java probe (`GoApiSnapshot.java:168-178`) is equally silent (only a `Msg.info`), so this matches Java, but it departs from the preview's own exit-2 "unreadable input" contract. Confidence: high on the code; low impact.

### F7 — Low — `selfcheck.py` exit status contradicts its docstring

The docstring (lines 63-66) says exit 2 covers "malformed case schema". `main()` catches `FixtureError` per case (`selfcheck.py:403-405`), prints `FAIL`, and continues. The final `return 0 if npass == len(cases) else 1` (`:414`) then yields exit 1. A malformed fixture, or a positive case with empty `expected` (`run_case`, `:304-307`), therefore exits 1 instead of 2. Confidence: high.

### F8 — Low — `_match` lets numeric expectations match booleans

`selfcheck.py:219-224`: the identity rule covers only expected booleans. An expected `0` matches actual `False` through `!=`, and expected `1` matches `True`. No current fixture expects an int where a bool is produced, so this is latent. Confidence: high.

### F9 — Low — `expect_error: true` masks harness defects

`selfcheck.py:284-285`: `spec is True` accepts any `Exception`, including a `ValueError` or `TypeError` from a selection bug (the class of defect repaired in `#C295`). No current fixture uses `true` (grep: none), but the schema advertises it (docstring line 40). Recommend fixtures name a type. Confidence: high.

### F10 — Low — `controls.py` cannot see duplicate source IDs

`controls.py:144-150` and `:216-243` build a dict keyed by the S-id. Duplicate rows collapse to the last occurrence, so an appended duplicate is not reported as `added_rows`, and a change to the first occurrence is hidden. The "zero rows added" claim (`round-16.md:80`) depends on this map. Recommend a duplicate-ID assertion in the report. Confidence: high on the mechanism; not exercised.

### F11 — Low — asymmetric missing-path handling

`prefix_report` (`controls.py:153-166`) and `Rev.get` (`:91-100`) abort with exit 2 when `LOG.md` is absent at BEFORE, while `unchanged_report` (`:169-178`) reports `absent_at_before`. Whether a missing BEFORE path falls under the documented "unresolvable revision or missing structural anchor" (`controls.py:16`) is arguable; the code does not say. Confidence: high on behaviour; minor.

### F12 — Low — QUALITY #18's supersedes cell

`corpus/QUALITY.md:28` says "sharpens 1, 6; no change to 17". The header requires that a new row name the row it supersedes. "Sharpens" is not defined and no text of rows 1 or 6 changed. Row 10 uses the same wording (`sharpens 8`), so this is a precedent rather than a new defect. Confidence: medium.

### F13 — Process — the closure is uncommitted

`SHONEN.md:10` (route 4), `SKILL.md:450/487` (routes 1-2), `QUALITY.md:28` (#18) and `corpus/lessons/round-16.md` are not committed. `round-16.md:28` and the knowledge correction cite untracked files. L1 must commit the set together, or the closure claims are not reproducible from HEAD.

## Not verified / limits

- Nothing was executed. Expected-value traces are by hand. The Gson null-value behavior (F4) is an inference from the reflective adapter's usual contract, not an executed check.
- Only `selection.py`'s single-root model was read. Java `getModuleDataFile` (`GoApiSnapshot.java:170-171`) can resolve other module data directories. That is the documented "unmodeled module resolution" limit (`round-16.md:91`), not a defect.
- The `SKILL.md` registry rows and `corpus/QUALITY.md` may still change in this wave. Findings bind to the tags listed above.
- No outside-review authority is claimed. This is an author-seat advisory finding set.
