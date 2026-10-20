# FScopeAndOutside — round-16 wave 2 attack on C1/C2 produced artifacts

Seat: `KaidokuR16.FScopeAndOutside` (leaf, no dispatch). Axes: depth, calibration.
Attack: C1 source-model vs held capability; prior-route learning vs round-15 spot-check; false expansion in produced drafts/integrated docs.

## Method, versions, limits

- Read: `.ufo/waves/round-16/selection.py`, `selfcheck.py`, `controls.py`, `selection-fixtures.json`, `negative-fixtures.json`, `claims.json`, `wave2-spec.json`, `documentation-red.json`; w1 reviews `ReviewBucketOrder.md`, `ReviewFixtureIndependence.md`, `SelectorModel.md`, `SelectorRunner.md`, `EntryDraft.candidate.md`, `CorrectionDraft.candidate.md`, `CriterionDraft.candidate.md`, `CraftDraft.candidate.md`, `AttackNovelty.md`, `AttackHonesty.md`, `Measure.md`; integrated `corpus/knowledge/2026-10-20-r16-go-selection-preview.md`, `corpus/lessons/round-16.md`, `corpus/lessons/round-15-verifier-spotcheck.md:175-195`.
- Source read-only from shipped `Base-src.zip`, members `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` (cited as GAS), `GoVer.java`, `JsonPatchApplier.java`, streamed to stdout; nothing written.
- Installed data read only via `ls`/`stat`/`grep`. No JSON parsing of the 10 MB bases; bucket claims about installed data are cited from w1 reviewers and marked as such.
- **Nothing executed**: not `selection.py`, `selfcheck.py`, `controls.py`, `measure.py`, no fixture runs, no hashing. Expected values below are hand-derived from GAS.
- **Concurrent edits observed during the read.** `selection.py` changed mid-review (now 315 lines; patch-0 diff listing is skipped, missing diff directory tolerated, other `OSError` raises `UnreadableError`). `selfcheck.py` changed mid-review (now 414 lines; importlib bytecode guard added at `:96-114`). Findings below are against those latest versions. Re-check if edited again.
- Tool installs/updates: none.

## Verdicts

- **C1 source-law faithfulness: mostly faithful, one source-law mismatch.** Search order, base-at-patch-0, missing-base short-circuit, nearest-lower-within-minor diff choice, patch-0 short-circuit, `getApiFile` non-use, and status mapping match GAS `:102-116`, `:118-146`, `:148-166`, `:168-178`, `:180-181`, `:205-240`. The mismatch is null-valued buckets (F1).
- **C1 not held: correctly labelled.** Round-16 lesson `:18`, CraftDraft candidate `:4,:13,:54`, and knowledge entry `:51` all state source-model only, not held. No held or capability claim found.
- **C2 round-15 routes: present in the working tree** (pending L1 execution). Route 1: `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:76` carries the named correction; recorded argv at `round-15/verification.json:33,50` names the absolute script path (per-entry `-I` not inspected). Route 2: `SKILL.md:450` names `.ufo/waves/round-15/boundary-fixtures/expected.json`. Route 3: `controls.py:292-294` retains `orig_argv` and `producing_command`. Route 4: `SHONEN.md:10` names historical 2026-10-15 round 1. Existence is bounded no-finding; quality of the correction text is outside this seat.
- **Calibration: the depth claim is over-worded in three places** (F2, F3, F7), and the harness that is supposed to pin it is looser than its docstrings (F4, F5, F8).

## Findings (ranked)

### F1 — MEDIUM-HIGH (C1 source-law). Null-valued top-level buckets counted as applicable

- `selection.py:147-167` `_top_level_keys` returns every top-level key regardless of value. `select_snapshot` `:250-256` counts any key in `order` as a matching bucket.
- GAS `:218-223`: a retained bucket is deserialized with `gson.fromJson(reader, GoArch.class)` and stored with `arches.put(archName, arch)`, even when `arch` is null. GAS `:233-236` then skips null (`if (arch != null)`), so it never enters `results` (`:237`) or lookup. [INFERENCE from Gson's reflective adapter returning Java null for a JSON null token; not executed.]
- Consequence: `base_matching_buckets` reports applicability for a bucket Java silently drops. No error is raised on either side, so this is a silent parity break. The knowledge entry row `2026-10-20-r16-go-selection-preview.md:26` ("top-level names") and claims C1 inherit it.
- Coverage gap: no selection or negative fixture uses a null bucket. Grep of both fixture files shows `null` only in expected `base`/`selected_diff`/`selected_patch`. The w1 reviewer reports no null bucket in the 11 shipped bases (`ReviewBucketOrder.md` §2; not re-verified here), so installed-data impact is likely nil. The defect is in the model's claim, not in shipped results.
- Fix: exclude keys whose value is `None` in `_top_level_keys`, or filter in `select_snapshot`.
- Handwritten fixture (expected values from GAS only):
  - id `null-bucket-not-retained`; request `1.21.0`; goos `linux`; goarch `amd64`
  - files `{"go1.21.0.json": {"all": {}, "linux-amd64": null}}`
  - expected: `status` `base_only`; `selected_patch` `0`; `base_matching_buckets` `["all"]`; `patch_applied` `false`; `evidence_class` `source_model`
- Sibling, already documented: `negative-fixtures.json:203-221` pins `base_only` for a non-object bucket, where GAS would throw (`:222` Gson read). The case note says so. It is labelled model behaviour, but it sits in a file described as source-law fixtures. Keep the label visible.

### F2 — MEDIUM (calibration). "Exercised" overclaim for the 1.24.5 contrast

- `corpus/lessons/round-16.md:73`: "the exercised contrast includes 1.24.5→patch 5 despite installed patch 6". The cited source is `w1/AttackNovelty.md:18`, which labels this `[INFERENCE: source-model expectations, not executed outputs]`. The lesson upgrades an inference to "exercised".
- `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:9`: "The strongest contrast is a request for 1.24.5". No retained run exists (`round-16/verification.json` absent), and no fixture carries 1.24.5. It appears only in `wave2-*.json` dispatch text and as a docstring example at `selfcheck.py:49`. `selection-fixtures.json` (9 cases) and `negative-fixtures.json` (17 cases) do not contain it.
- `LOG.md:1935` repeats the claim. LOG is outside this seat's write scope; a peer (`FAttackNoveltyFinal.md`) already flags it.
- Fix: either add the fixture below and let L1 run it, or reword lesson `:73`, entry `:9` and LOG `:1935` to "source-derived expectation, not exercised".
- Handwritten fixture: id `exact-patch5-not-patch6`; request `1.24.5`; files `{"go1.24.0.json": {"all": {}}, "patchverdiffs/go1.24.5.json.diff": {}, "patchverdiffs/go1.24.6.json.diff": {}}`; expected `status` `exact_diff`, `selected_patch` `5`, `selected_diff` `"patchverdiffs/go1.24.5.json.diff"`, `base` `"go1.24.0.json"`, `base_matching_buckets` `["all"]`. Source: GAS `:153-156` walks down from the requested patch.

### F3 — MEDIUM (calibration). "Applicability" versus unpatched key presence under a selected diff

- `selection.py:277-280` emits `base_matching_buckets` for every status, including `exact_diff` and `fallback_diff`, with `base_matching_buckets_source: "unpatched_base_file"`. The key name and claims C1 (`claims.json:6`, "ordered base-bucket applicability") read as resolution applicability.
- The source does not guarantee that a patch leaves top-level buckets unchanged. `JsonPatchApplier.java:83-93` adds or removes a bucket name when the section path has length 1. `SelectorModel.md:89-90` discloses this. The w1 reviewer simulated name-level resolution changes: 120/123 patches change at least one resolution for linux/amd64, darwin/arm64, windows/amd64, or freebsd/386 (`ReviewBucketOrder.md` D1; not re-verified here).
- The entry's limits (`:48`) disclose "unpatched", but no output field says resolution is not computed. The w1 reviewer's D1 asked for exactly that.
- Fix: rename to `base_key_presence_buckets`, or add a per-result `resolution_computed: false`. Reword the claim to "key presence in the unpatched base".

### F4 — MEDIUM (harness contract). Exit-code docs are wrong; harness exceptions escape

- `selfcheck.py:63-66` docstring: exit 2 on "malformed case schema". `SelectorRunner.md:40-41` repeats it.
- Code: a per-case `FixtureError` is caught at `:397-401`, printed as FAIL, and the loop continues. Final return at `:410` is 1. A malformed case therefore yields exit 1, not 2.
- Worse, non-`FixtureError` exceptions escape. `_materialize` `:144-145` calls `base64.b64decode(content["raw_b64"])`; invalid base64 raises `binascii.Error`, and a non-string value raises `TypeError`. `run_case` calls `_materialize` at `:323`, outside the `try` at `:324`, and `main` catches only `FixtureError`. Result: a traceback, the loop aborts, later cases never run, and the summary line never prints.
- Fix: wrap base64 decode in `FixtureError`; make a fixture error set a harness-failure flag that returns 2.

### F5 — MEDIUM (harness). Basename leniency hides base location; absolute paths are normalized

- `selfcheck.py:197-198`: a string expectation without `/` is compared by basename only. Every positive `base` expectation in `selection-fixtures.json` is basename-only (lines 41, 66, 89, 112, 137, 165, 192, 219). A mutant emitting `patchverdiffs/go1.21.0.json` as `base` passes.
- `selfcheck.py:199-200`: `Path(raw).relative_to(root)` raises `ValueError` for the relative paths the model emits, which falls through to raw comparison. An in-root absolute path is converted to relative and passes. So the docstring claim at `:188-192`, and `SelectorRunner.md:24-25` "mismatch explicitly", hold only for out-of-root absolute paths.
- `ReviewFixtureIndependence.md` F6 asked for exact root-relative expectations with basename as a separate, named mode. Not adopted.
- Fix: always compare the exact root-relative POSIX path; assert the emitted path is relative; keep basename only as a named mode.
- Handwritten check fixture: id `base-in-subdirectory-not-root`; request `1.21.0`; files `{"patchverdiffs/go1.21.0.json": {"all": {}}}`; expected `status` `missing_base`, `base` `null`.

### F6 — LOW (contract). Zero matching buckets reports `base_only`

- `selection.py:258-264` maps a readable base with no matching buckets to `base_only`, with `base_matching_buckets: []`.
- GAS `:239` returns a non-EMPTY snapshot with `isInvalid()` true (`:503-505`); `EMPTY` (`:115`, `:242`) is only for missing base. ReviewBucketOrder D5 asked that this not be conflated with missing base, and not be read as usable either. The status enum has no invalid state, so a consumer keyed on `status` reads `base_only` as usable.
- The entry discloses the case at `:49`. The enum still conflates.
- Fix: add a boolean such as `snapshot_usable`, or a status value.
- Handwritten fixture: id `zero-bucket-base-only`; request `1.21.0`; linux/amd64; files `{"go1.21.0.json": {"windows-amd64": {}}}`; expected `status` `base_only`, `base_matching_buckets` `[]`, `selected_patch` `0`. Source: GAS `:239`, `:503-505`.

### F7 — LOW (calibration). The `""` placeholder is a deliberate deviation, described as a fix

- `selection.py:105-121` filters `""` from `arch_search_order` (`if name`). The wave spec says "match exact get search order". The deviation is disclosed at knowledge `:25,:28` and `SelectorModel.md:61`.
- `corpus/lessons/round-16.md:75` calls this "Model/fixture integration fixes the ambiguous non-Unix slot". It is a choice. ReviewBucketOrder D3 recommended the opposite (emit `""`).
- `EntryDraft.candidate.md` Limit 11 still says "no emitted form is claimed". Stale now that fixtures pin omission. The draft is superseded, but the claim should not be carried forward.
- Fix: say "deliberate read-effective order; Java list literal retains `""` before `read` skips it" in the entry and lesson. Remove "fixes".

### F8 — LOW (harness strictness)

- `selfcheck.py:218-224`: the bool identity check runs only when `expected` is a bool. An expected int `0` accepts actual `False` (Python `0 == False`). Impact: `selected_patch: 0` would pass for `False`.
- `selfcheck.py:280-281`: `expect_error: true` accepts any `Exception`, including `AttributeError`/`TypeError` from a broken implementation. Latent: all 8 `expect_error` cases use typed specs. Recommend removing `true` or excluding non-library errors.
- `selfcheck.py:99` docstring names `sys.dont_writebytecode`; the real attribute is `sys.dont_write_bytecode` (`:108-109`). The guard itself is effective, since importlib's `SourceLoader` checks `sys.dont_write_bytecode`, so the `SelectorRunner.md:10-12` claim is now true [INFERENCE on importlib internals; not executed].

### F9 — LOW [INFERENCE]. Parse acceptance differs from Java, untested

- `selection.py:155-156`: `json.load` on a binary handle auto-detects UTF-8 BOM and UTF-16/32, and accepts `NaN`/`Infinity`. GAS `:214` reads through `InputStreamReader(is)` (default charset) into Gson's `JsonReader`. A BOM- or UTF-16-encoded base would be `base_only` in the model; Java likely rejects it. Not verified.
- Negative fixtures (17 cases) cover neither. Only the generic disclosure at knowledge `:47` applies.
- Fix: reject BOM/non-UTF-8 with `UnreadableError`, or add a disclosure fixture.

### F10 — LOW (harness). Escape-form ambiguity

- `selfcheck.py:144` and `:149` treat any dict containing key `raw_b64` or `raw` as an escape form. A JSON document with such a top-level key cannot be authored. Latent: no real Go arch bucket is named `raw`.

### F11 — LOW (controls.py). Duplicate-ID blind spot in the SOURCES immutability control

- `controls.py:136-150` builds `source_rows` as a dict keyed by ID. A duplicate `| S0NN |` row silently overwrites the earlier one. A mutated first row followed by an unchanged second row would compare as unchanged (`:226-234`). Requires adversarial insertion, but it is a false negative in a control whose claim is immutability.
- `controls.py:224` vs `:234` mixes a string sentinel and lists in one dict. Schema inconsistency, no correctness impact.
- Fix: detect duplicate IDs and fail with exit 2.

### F12 — LOW (calibration). Scalar and token-presence claims

- `corpus/lessons/round-16.md:10`: "All three owned finite proxies tie at 10.0". No retained artifact in this lane supports the figure. The lesson disclaims score inflation in the same paragraph. Cite the file or remove the number.
- `documentation-red.json` `producing_command_retained` is `'argv' in co`, a token-presence test. The lesson already calls it marker/presence evidence (`round-16.md:23,58`). Consistent; no action beyond keeping that wording.

## Bounded no-findings

- Search order (`selection.py:105-121` vs GAS `:108-109`), IS_GOOS_UNIX set (`:42-45` vs `:180-181`), base at patch 0 (`:194-196` vs `:122-123`), missing-base short-circuit (`:197-213` vs `:124-126`), patch-0 short-circuit (`:224`, vs `:153`), nearest-lower-within-minor (`:233-245` vs `:153-156`), status mapping (`:258-264`), dedup-in-order (`:250-256` vs `:228-237`) all match source as read.
- GoVer strictness (`:50-101` vs `GoVer.java:62-81,105-107`) matches the declared, deliberate divergence.
- The nine positive fixtures in `selection-fixtures.json` were checked against GAS and against their own file key sets. All nine expectations are consistent with source law. Arch order, bucket order, status, `selected_patch`, and `base_only`/`exact_diff`/`fallback_diff` boundaries agree. Digests and sizes are not asserted by fixtures, so none is invented.
- `controls.py` git reads (`:48-52`, `:71-100`) use only `ls-tree`, `show <rev>:<path>` and `rev-parse`; the worktree is never read. `craft_section` heading anchor matches `SKILL.md:81`.
- No held-capability or coverage-expansion claim appears in any produced draft or integrated doc; C1 is consistently "source model, not held".

## Proposed handwritten fixtures (not written; expected values from GAS only, no hashes)

1. `null-bucket-not-retained` (F1)
2. `exact-patch5-not-patch6` (F2)
3. `base-in-subdirectory-not-root` (F5)
4. `zero-bucket-base-only` (F6)

Harness-contract checks for F4 need a dedicated harness test, not a schema case.

## Recommended changes for L1 integration (ranked)

1. Fix F1 (null bucket) and add fixture 1. Correctness of the depth claim.
2. Reword or exercise F2 across lesson `:73`, entry `:9`, and LOG `:1935`.
3. Rename or annotate F3 so the field reads as key presence, not resolution.
4. Fix F4 exit codes and wrap `_materialize` errors; correct `SelectorRunner.md:40-41` to match.
5. Tighten F5 to exact root-relative comparison; add fixture 3.
6. Address F6 with an explicit field; add fixture 4.
7. Reword F7 to "deliberate deviation".
8. F8–F12 at discretion.

No checks were run by this seat; L1 owns the single execution pass.
