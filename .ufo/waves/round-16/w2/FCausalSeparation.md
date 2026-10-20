# FCausalSeparation — C1 model vs C2 docs (wave 2, report only)

**Axes:** depth, calibration. **Scope:** produced round-16 artifacts only: `selection.py`, `selfcheck.py`, `selection-fixtures.json`, `negative-fixtures.json`, `controls.py`, `measure.py`, `documentation-red.json`, and the C2 doc lines they check. Source S003 = `Base-src.zip:ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` (+ `GoVer.java`); data = installed `typeinfo/golang`.

**Execution disclosure:** no lane script was executed; no tests, builds, linters, or verification were run. Evidence is static reading, `git show` reads at baseline `6235498`, and read-only stdlib Python over the installed base JSON, the installed `patchverdiffs/` headers, and the source zip (line-number mapping). No tools were installed or updated. Claims marked `[INFERENCE]` are unexecuted reasoning about runtime behavior.

## Bounded no-finding: C1 survives removal of C2 docs

- `selection.py` and `selfcheck.py` read only the `--root` argument, the sibling `selection.py`, and sibling fixture files (`selfcheck.py:79-81`, `:368-369`). A grep of both scripts and both fixture files for `corpus`, `SKILL`, `SHONEN`, `QUALITY`, `SOURCES`, `README`, `LOG`, `knowledge`, `controls`, `measure` returned no matches. Removing every C2 doc line cannot change `select_snapshot` output or fixture results.
- The reverse holds too. `controls.py` and `measure.py` never import or execute `selection.py`. `measure.py:131-133` only tests file presence in a commit. `documentation-red.json` is a fixed `git show` over `6235498`. So the C2 routes do not need the model.
- Sequencing constraint, not a defect: `controls.py:71` and `measure.py:70` read `git ls-tree` at a revision. Uncommitted edits (`git status`: `M SKILL.md`, `M SHONEN.md`, `M corpus/QUALITY.md`, `?? .ufo/waves/round-16/`, `?? corpus/knowledge/2026-10-20-r16-go-selection-preview.md`) are invisible to both. At `6235498`, all C2 fields read 0 (QUALITY row 18 absent; SHONEN line 9 says "this round"). L1 must commit before the C2 census means anything.

## C1 findings (selection.py, selfcheck.py, fixtures)

**C1-1. [Medium] Unreadable `patchverdiffs/` silently becomes `base_only`, exit 0.**
`selection.py:218-222`: `diff_dir.iterdir()` is wrapped in `except OSError: entries = []`. That swallows permission errors as well as absence. An existing but unlistable diff dir yields `status: base_only`, `selected_diff: null`, exit 0. The contract (`selection.py:294-300`, r16 entry "exit 2 means … a required read/parse could not be evaluated") says this must be exit 2.
Source does not support the silent drop. `GoApiSnapshot.java:168-172` resolves each diff by name via `Application.getModuleDataFile(...)`, so a diff's existence is not a listing outcome; the model's listing-based discovery cannot know presence when listing fails.
Repair: catch only `FileNotFoundError` / `NotADirectoryError` at `:221`; let other `OSError` become `UnreadableError`. No fixture covers this (see C1-9).

**C1-2. [Medium] Some unreadable-path errors escape `main()` as tracebacks, not the exit-2 JSON.**
`selection.py:130` (`path.is_file()`) sits outside the `try` at `:132-139`. `selection.py:191` (`root.is_dir()`) is also unguarded. `main()` at `:294` catches only `(RequestError, UnreadableError)`.
`[INFERENCE]` From CPython 3.14 `pathlib`: `is_file`/`is_dir` swallow only ENOENT/ENOTDIR/EBADF/ELOOP; EACCES propagates. An unsearchable root or base would then exit 1 with a traceback, not the documented exit 2 with `unreadable_input`.
Repair: wrap both in the `UnreadableError` path.

**C1-3. [Medium-low, fidelity] Bucket applicability counts key presence; source drops null-valued buckets.**
`selection.py:242-248` (`keys = set(_top_level_keys(...))`) counts any top-level key. Source `GoApiSnapshot.java:222-223` stores `gson.fromJson(...)` into `arches`, and `:228-236` retains only `if (arch != null)` (line 234).
`[INFERENCE]` Gson's reflective adapter returns null for a JSON `null` token, so `"linux-amd64": null` is reported applicable by the model and dropped by Java.
Installed-data check: all 11 base files (`go1.15.0.json`…`go1.25.0.json`) have object-valued top-level entries. No installed-data impact observed.

**C1-4. [Low-medium, fidelity] The base reader is not the Java reader, though `selection.py:147-153` says it is.**
The comment says the preview "never claims membership for a document the Java reader could not open". `json.load` at `selection.py:156` differs in two ways:
- It accepts `NaN`/`Infinity` (Python default `parse_constant`). `[INFERENCE]` Non-lenient Gson `JsonReader` rejects them. So the model can claim membership for a document Java cannot open, which is the exact outcome the comment forbids.
- It rejects trailing bytes after the top-level object. `[INFERENCE]` `GoApiSnapshot.java:215-237` reads to `endObject()` and closes without an EOF check, so Java opens such a file and the model refuses it.
Neither divergence is in the r16 entry's limits list. Repair: narrow the claim or add fixtures for both.

**C1-5. [Medium, calibration] Two fixtures pin non-source outcomes as PASS.**
- `negative-fixtures.json` `unsupported-shape-bucket-nonobject-preview` expects `base_only` with `base_matching_buckets: ["all"]`. Source: a non-object bucket makes Gson throw inside `read()` (`GoApiSnapshot.java:222`), so `get()` does not return `base_only`. The fixture's own note admits the divergence, but the expectation is asserted as passing.
- `negative-fixtures.json` `corrupt-diff-still-selected` expects `exact_diff`. Source: `JsonPatch.read` at `GoApiSnapshot.java:136` runs inside the derived-provider path, so a corrupt diff fails `get()`. The note says "selection only", but `selfcheck.py:331-336` prints `PASS … status=exact_diff` with no limitation marker, and the summary counts it as a source-law pass.
Repair: give these a separate class (for example `preview_divergence`) or tag them in the printed result.

**C1-6. [Low, depth gap, bounded no-finding on installed data] Diff-selected bucket lists are base-only by construction.**
`selection.py:269-272` computes buckets from the unpatched base. Source applies the diff (`GoApiSnapshot.java:134-144`) and filters the patched document (`:228-236`). The output labels this (`base_matching_buckets_source: "unpatched_base_file"`), so the label is honest. The claim wording "ordered base-bucket applicability" (`claims.json` C1) is accurate only for that label.
Installed-data scan: 123 diffs in `patchverdiffs/`. Their line format (`@ ["all","Funcs",…]`, not JSON) is never parsed by the model, which is correct for `patch_applied:false`. Every diff header's top-level bucket name is present in its same-minor base. No installed-data divergence is observed, so this is a structural limit only.
Fixture diffs are `{}` (`selection-fixtures.json` `exact_diff`, `lower_fallback`, `windows_omission`). No fixture exercises diff content.

**C1-7. [Low, citation drift] Two negative-fixture notes mis-cite the Java lines.**
`negative-fixtures.json` `missing-base-empty-root` and the `GO1.21.0.JSON` note cite `GoApiSnapshot.java:170` and `:171` for the filename build. The `"typeinfo/golang/%sgo%s.json%s"` string is at `:171`. The null return is in the `catch (IOException)` block at about `:174-175`, not `:171`. Other anchors check out: `get` `:102-117` (model says 102-116), arch order `:108-109`, `:122-126`, `:136`, `:153`, `:168-172`, `:180-181`, `:183-190`, `:215`, `:218`, `:222`, `:230-236`, `:239`, `:503-505`. `GoVer.java` anchors `:36`, `:62-81`, `:65`, `:66-67`, `:70-74`, `:155-158` all check.

**C1-8. [Low, dead code / misleading docstring] `selfcheck.py:183-191` path normalisation is not the path taken.**
`select_snapshot` reports root-relative paths (`selection.py:141`), so `relative_to(root)` at `selfcheck.py:189` never succeeds; the `str(raw)` fallback runs. The docstring at `:50-52` and `:174-181` describes absolute-path handling the current model never produces. Result is correct; the code and comments describe behavior that is not exercised.

**C1-9. [Low, test gaps] Behaviors with no fixture (all named above):**
- unreadable `patchverdiffs/` (C1-1), non-searchable root or base (C1-2);
- null-valued bucket (C1-3); NaN and trailing-bytes base (C1-4);
- `go1.21.4.json.diff` as a directory or broken symlink (`selection.py:233-236` silently skips; no source-verified equivalent);
- double-digit patch ordering (`1.21.10` with diffs `9` and `10`): `:232` sorts ints correctly, but nothing guards a regression to string order;
- `selfcheck.py:268-270` accepts `expect_error: true` (any `Exception`), so a model `TypeError` would pass. No fixture uses `true` today.

**Positive verification of handwritten fixture expectations (by reading, not running):** I checked every positive case in `selection-fixtures.json` and every non-error case in `negative-fixtures.json` against its own file keys and the `arch_search_order` rule (`selection.py:105-121`). All `base_matching_buckets` intersections are consistent with the fixture file contents, and no fixture expectation contains a hash, size, or invented digest. Provenance of "hand-authored" cannot be checked from git (fixtures are untracked); that is the author's assertion.

## C2 findings (controls.py, measure.py, documentation-red.json, doc lines)

Route status against `claims.json` C2 (four round-15 routes, plus QUALITY criterion, plus red-before control):

| Route | Current evidence | Status |
|---|---|---|
| Invocation consistency (routed defect 1) | r15 entry `## Round-16 correction` (worktree lines 76-91) gives the exact `python3 -I …/snapshot-inventory.py` argv; `measure.py:109-114` and `documentation-red.json` both read it | Discharged, but see C2-3 |
| Supplemental baseline discoverable (defect 2) | `SKILL.md:450` quote-fidelity row cites `.ufo/waves/round-15/boundary-fixtures/expected.json` (grep count 1); round-15 holds exactly one supplemental frozen baseline | Discharged (bounded no-finding) |
| Producing command for controls (defect 3) | `controls.py:281-295` embeds argv, `orig_argv`, executable, isolated flag; `measure.py:158` emits none | Partial, see C2-1 |
| Historical SHONEN wording (defect 4) | worktree `SHONEN.md:10` names `2026-10-15`; baseline line 10 said "this round" | Discharged (bounded no-finding; `measure.py:141-148` discriminates baseline vs worktree) |
| QUALITY criterion (row 18) | worktree `corpus/QUALITY.md:28`; absent at baseline, so `measure.py:134` discriminates | Discharged textually; see C2-1 |

**C2-1. [Medium] `measure.py` ships tallies without their producer.**
`measure.py:127-157` builds the result with `revision`, presence bits, `knowledge_files`, `mapped`, `missing`, `dangling`, `sources_rows`, `tiers`, `statuses`, and no `invocation`/`argv`/`executable`/`isolated`. `controls.py:281-295` does carry that block. QUALITY row 18 (`corpus/QUALITY.md:28`) requires that "Structural/no-harm tallies retain the producer and immutable inputs, not only unexplained booleans." `measure.py` is the C2 tally command the r16 SKILL/README rows cite, so its output fails the criterion it was written to satisfy.
Repair: add the same invocation block to `measure.py`.

**C2-2. [Medium] `documentation-red.json` `producing_command_retained` is not a falsifiable check.**
The embedded check is `bool(co) and 'argv' in co` on `controls.py` at each revision (`documentation-red.json`, `argv[3]`). Any file containing the token `argv` passes (`controls.py` contains `sys.argv` at `:247`, `:249`, `:282`). The baseline result of `false` is only because `controls.py` is absent at `6235498` (`co == ''`), so the red-before control shows absence, not retention. A `controls.py` with its invocation block deleted would still pass.
Repair: parse the emitted JSON and require the `invocation` keys, or drop the claim to "file present".

**C2-3. [Low] Two "correction present" tests disagree.**
- `documentation-red.json` requires the literal `Round-16 correction` heading plus the exact absolute argv string.
- `measure.py:109-114` picks the first line matching `(?im)^.*correction.*$`, which is the heading `## Relation to the outside correction` at worktree line 37 (same line at baseline), then requires any isolated absolute round-15 path anywhere after it.
The `measure.py` anchor does not bind to the correction section. Currently it passes via `:83`, which is inside the section, so there is no present false positive. But any later isolated absolute path would satisfy it even if the Round-16 section were deleted, and it accepts any spelling. Repair: anchor on the `Round-16 correction` heading, as the red-check does.

**C2-4. [Low] `SKILL.md:506` names an incomplete fixture command.**
The row's fixture cell says `python3 -I …/selfcheck.py` and lists both fixture files. The default run loads only `selection-fixtures.json` (`selfcheck.py:368-369`). `negative-fixtures.json` runs only with `--fixtures` (usage at `selfcheck.py:17-18`). The documented command therefore does not exercise the 17 negative cases.
Repair: give the exact two-`--fixtures` invocation in the row.

**C2-5. [Low, pending] Receipts referenced but absent.** `SKILL.md:506`, `corpus/README.md:36`, and the r16 entry's recheck line cite `.ufo/waves/round-16/verification.json`. It does not exist (`ls` error). This is L1's deliverable, not a defect today, but the docs assert it. If L1 does not write it, these three references dangle.

**C2-6. [Low, latent] `controls.py` row-collision blind spot.**
`controls.py:143-150` builds `source_rows` as a dict, so a duplicate `S`-ID keeps only the last row. `sources_registry` at `:216-243` then compares only that row, so an appended duplicate ID is neither an immutable violation nor an "added" row (set difference). Current `SOURCES.md` at baseline and worktree: 23 rows, 23 unique IDs (checked). No present defect; blind spot only.

**C2-7. [Low] `measure.py` C1 census omits `negative-fixtures.json`.** `measure.py:24` and `:132` count only `selection-fixtures.json`. The 17 negative cases are not in the census. Fine if intended; the SKILL row presents both as the fixture set.

## Calibration summary

- Supported without overclaim: C1 `patch_applied:false`, `evidence_class:'source_model'`, `base_matching_buckets_source`, the Java line citations for `get`/`getApiSnapshotJsonFile`/`getPatchVerDiffFile`/`IS_GOOS_UNIX`, and the r16 entry's "no provider recovery" boundary.
- Overclaimed: the r16 entry's "exit 2 means a required read/parse could not be evaluated" (contradicted by C1-1 and C1-2); the claim that the base parser never claims membership for a document Java could not open (C1-4); fixtures that assert a source divergence as passing (C1-5).
- Not checked and not claimed: any runtime behavior of the lane scripts; whether Gson/CPython behave as `[INFERENCE]` marks above; the historical op cause (remains UNKNOWN by the r15 entry).

## Suggested order for L1 (no edits made here)

1. Commit before running `measure.py` / `controls.py`; C2 fields read commits only.
2. Repair C1-1 and C1-2 before the single L1 execution. Both change exit codes and would make the r16 entry's exit-2 statement true.
3. Re-check C2-1 (`measure.py` producer block) and C2-2 (non-falsifiable red check) before recording the C2 receipts.
