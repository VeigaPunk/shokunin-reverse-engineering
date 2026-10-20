# FCanonicalHistorical — round-16 wave 2 source-read attack

Scope: produced round-16 artifacts `.ufo/waves/round-16/selection.py`, `selfcheck.py`,
`controls.py`, `selection-fixtures.json`, `negative-fixtures.json`, plus SHONEN/historic r14
qualification. Source law: `/tmp/r16src/ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java`
(sha256 765d25365a8c379c929097a6602df5fa75049f871eb0f610d5376d630d95eb7d, identical to the
Base-src.zip member; zip sha256 f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804
matches SOURCES.md S003) and `GoVer.java`.

Method: read-only. No tests, builds, linters, selfcheck or controls runs. One read-only Python
scan of the installed `patchverdiffs/*.json.diff` top-level `@ ["<key>"` path references against
each `go<M.m>.0.json` base key set (data analysis, not a test). No installs by this seat.

## Findings (severity order)

### F1 — medium — silent downgrade when `patchverdiffs/` is present but unlistable
`selection.py:218-222`:
```
diff_dir = root / _PATCH_SUBDIR
try:
    entries = list(diff_dir.iterdir())
except OSError:
    entries = []
```
Every `OSError` (permission denied, EIO, not-a-directory) becomes "no diffs", so an existing but
unreadable `patchverdiffs/` yields `status: base_only`, `selected_patch: 0`, `exit 0`. The module's own
contract (docstring; `UnreadableError` at `selection.py:65-67`, exit 2 for unreadable input) says this
must be exit 2. Only a genuinely absent directory (`FileNotFoundError`) should map to `[]`.
Inference, not executed: chmod-000 directory reproduces it.
Remedy direction: catch `FileNotFoundError` (and `NotADirectoryError`) only; re-raise others as
`UnreadableError`. No fixture covers this; add one only with a handwritten expectation.

### F2 — medium — a negative fixture pins a non-source outcome as its expected value
`negative-fixtures.json:202-221` (`unsupported-shape-bucket-nonobject-preview`) expects
`status: base_only`, `base_matching_buckets: ["all"]` for `{"all": ["not","an","object"]}`.
Source law: `read()` keeps `all` (`GoApiSnapshot.java:218-223`) and `gson.fromJson(reader, GoArch.class)`
(`:222`, `GoArch` is an object-shaped class at `:445-448`) cannot deserialize an array. The
exception propagates out of `get()` (`:102-116`), so Java does not return `base_only`. The note says
"LIMITATION CASE" and "do not expect UnreadableError", but the file is labelled source-law independent
fixtures, and `selfcheck` will fail any future implementation that correctly raises.
Calibration defect: the fixture encodes a known divergence as truth.
Remedy direction: move this case to a separate known-divergence file excluded from source-law pass
counts, or assert only the bucket-membership facts the preview is meant to model.
Also `selection.py:239-241` says buckets are computed "exactly like read()", which overclaims for
non-object buckets; narrow the docstring.

### F3 — low-medium — JSON-null bucket is reported as matching
`selection.py:242-248` builds `base_matching_buckets` from raw top-level key membership. Source:
`read()` stores `arches.put(archName, arch)` even when `arch` is null (`GoApiSnapshot.java:222-223`),
and the results loop skips null (`:233-235`, `arch != null`). Gson returns null for a JSON `null`
value, so `{"linux-amd64": null}` is absent from source results but present in the preview.
No fixture covers this. Handwritten expectation under source law, if added:
`{"all": null}` → `base_matching_buckets: []`, `status: base_only`.
Severity is low because the field is labelled `unpatched_base_file`, but the docstring at
`selection.py:239-241` still says "exactly like read()".

### F4 — low — inference only: strict JSON acceptance differs from Gson
`_top_level_keys` (`selection.py:154-163`) uses Python `json.load`, which accepts `NaN`, `Infinity`,
and `-Infinity`. Gson's `JsonReader` in default (non-lenient) mode rejects them, and the top-level
`skipValue()` for non-matching buckets (`GoApiSnapshot.java:219`) runs in that mode. A base with
`NaN` in a skipped bucket would fail source law and pass the preview. [INFERENCE: from Gson's
documented strict grammar; not executed.] Low priority; a `parse_constant` hook that raises
`UnreadableError` would close it.

### F5 — medium — harness-level malformed case exits 1, documented as exit 2
`selfcheck.py:63-65` documents exit 2 for "malformed case schema". The loop at `:384-390` catches
`FixtureError` per case, prints `FAIL <id>: fixture error`, and `continue`s. `main` then returns
`0 if npass == len(cases) else 1` (`:399`), so a schema error yields exit 1. Exit 2 is only reached
for file-level load errors (`:374-376`) and import failures.
Remedy direction: validate every case before the loop (or re-raise `FixtureError` from the loop),
so malformed schema returns 2.

### F6 — medium — expected values for forced keys are silently discarded
`selfcheck.py:231-233`:
```
for key, exp in expected.items():
    if key in ("patch_applied", "evidence_class"):
        continue  # already forced above
```
The forced check (`:224-230`) only compares the result to the constants `False` / `"source_model"`.
A fixture that writes `"patch_applied": true` or `"evidence_class": "api"` in `expected` is never
compared, and still PASSES when the result is correct. The docstring (`selfcheck.py:55-58`) says the
forced values apply "regardless of the case's own expectations", which describes the constants, not a
silent pass. A wrong handwritten expectation is therefore invisible.
Remedy direction: if the expectation differs from the forced constant, report it as a fixture error.
No current fixture uses `true` (checked: `grep` for `"patch_applied": true` in `round-16/*.json` returns
nothing), so this is latent.

### F7 — low — case `id` uniqueness is not enforced
Schema (`selfcheck.py:20-26`, docstring "unique string label") is checked only for presence and type
(`:290-292`). No duplicate detection exists in `run_case` or `main`. Two cases with the same id across
`--fixtures` files print ambiguous PASS/FAIL lines and both count. Current files: 9 positive and 17
negative ids; I did not confirm cross-file uniqueness by script. Latent.

### F8 — low — `_path_cmp` comment misdescribes its actual behavior
`selfcheck.py:174-191` says actual paths are compared "relative to the case's temp root". But
`selection.py:141` emits paths already relative to root (`path.relative_to(root).as_posix()`).
`Path(raw).relative_to(root)` with an absolute `root` raises `ValueError`, so the `except` branch returns
the already-relative string, and matching works only by accident. If `selection.py` ever emits an absolute
path, the same code would compare absolute spellings to the relative expectation and fail, which is
acceptable only if documented. Also `_match` (`:207-213`) enforces boolean identity but lets int `0`
match `False` for non-bool expectations (`False != 0` is False). Low.

### F9 — low, latent — duplicate source ids silently collapse in controls
`controls.py:136-150` builds `{row[1].strip(): ...}` with last-wins semantics. A duplicate `S###` row in
either revision silently shadows earlier rows, and `sources_registry` (`:216-243`) then never checks the
shadowed cells. Current state: no duplicate ids in HEAD or the worktree (checked by script). Latent;
add a duplicate-id `fail` to keep the immutable-cell check total.

### F10 — low — undocumented exit path on non-UTF-8 input in controls
`controls.py:51` and `:110`, `:125`, `:137` decode git output and blobs as strict UTF-8; `Rev.__init__`
(`:71-82`) decodes `ls-tree` output the same way. A non-UTF-8 path or blob raises `UnicodeDecodeError`,
exit 1 with a traceback. The documented contract (`controls.py:16-17`) is exit 2 for usage, unresolvable
revision, or missing anchor only. Remedy direction: catch `UnicodeDecodeError` into `fail()`.

## Verified no-findings (source-read or read-only data scan)

- **Search order and bucket lists.** `arch_search_order` (`selection.py:105-121`) matches
  `GoApiSnapshot.java:108-109`, including IS_GOOS_UNIX (`:180-181`) and dropping empty slots. All
  nine positive fixtures' `arch_search_order` and `base_matching_buckets` values were checked by hand
  against the file contents they declare (exact_diff, lower_fallback, no_diff, patch0,
  future_diff_ignored, minor_isolation, unix_order, windows_omission, missing_base_despite_diff). All
  correct under source law. Dedup via `seen` matches the LinkedHashMap order (`:228-237`).
- **Diff selection.** `getPatchVerDiffFile` (`GoApiSnapshot.java:148-166`) walks `prevPatch()` within
  the minor (`GoVer.java:134-136`, floor 0). `selection.py:224-237` takes the max candidate ≤ request in
  the same minor. Equivalent, including patch 0 → null and absent diffs → base only. Filename regex
  matches `GoVer.toString()` (`GoVer.java:155-159`). The `(0,0,*)` rejection matches `GoVer.isInvalid()`
  (`:105-107`).
- **Base file.** Patch-0 base name (`selection.py:195`) and missing-base short circuit match
  `:122-126`. The two-part `getApiFile` fallback is correctly not reproduced (`:183-192`, unused by `get()`).
- **Negative-fixture GoVer claims.** `GoVer.java:62-81` confirms the source notes: `v1.21.0` →
  `replaceAll` empties the string → INVALID (`:65-67`); `1.21.0+bad` strips to 1.21.0; `1.21.-1` →
  `1.21.0`; `1.021.0` accepted by `parseInt`; `1.21.0.1` ignores the fourth part (`:72-74`). The
  strict-reject expectations are design choices, correctly labelled as such.
- **Shipped patch data vs. the unpatched bucket label.** Scan of 123 installed diffs: every top-level
  `@ ["<key>"` path reference names an arch key present in its `go<M.m>.0.json` base (0 minors with missing
  keys). So for shipped data the unpatched `base_matching_buckets` label does not diverge from the
  patched bucket set in the top-level-key sense. Patch semantics below the top level were not modelled, and
  this scan does not prove the post-patch set. Scope limit only.
- **Error mapping.** `main` (`selection.py:278-303`) maps `RequestError`/`UnreadableError` to exit 2 with
  JSON on stdout, and `_top_level_keys` (`:147-167`) converts non-object JSON, JSON decode errors and
  `RecursionError` into `UnreadableError`. Consistent with the negative fixtures at `negative-fixtures.json:68-89`.
- **Forced invariants.** `patch_applied` is literal `False` and `evidence_class` is `"source_model"` in
  every non-error return (`selection.py:211-212`, `:273-274`).

## SHONEN and historic r14 qualification (target)

- **No `[x]` introduced.** `SHONEN.md` (12 lines) has four `[~]` boxes (`:5,7,9,11`). `git show HEAD:SHONEN.md`
  shows the same four `[~]`. The only SHONEN diff is box 3's evidence wording, which now names the historical
  2026-10-15 round 1 (matches r15 lesson route 4, `corpus/lessons/round-15-verifier-spotcheck.md:188`).
- **Historic r14 assertion qualified, anchors checked.** `corpus/knowledge/2026-10-14-r14-02-final-sweep.md:146-150`
  is the quoted claim ("four SHONEN gates are closed with named non-author verifier evidence"); the appended
  `Round-16 correction` section (lines 196-207) quotes it correctly, cites
  `corpus/lessons/round-15-verifier-spotcheck.md:192` for the withheld promotion/`[x]` authority (verified:
  line 192 says "No promotion, mint, or `[x]` authorization"), and states no new outside review. The r14 text
  itself is left unrewritten (append-only).
- **Stale anchor, historic only.** `LOG.md:149` cites `SHONEN.md:11-18`; SHONEN has 12 lines now. This is a
  historic LOG entry, not operative, and the correction supersedes it. No action required unless L1 wants a
  note.
- **SOURCES.md cell-level diff (script, HEAD vs worktree).** Only index 11 (`used-by`) changed, for S003
  and S023, with the old→new delta logged in the r16 lesson. No duplicate ids. The added line at the end is
  a list item, not a table row, so the controls regex does not count it.
- **SKILL anchor in SHONEN box 1.** Commit `3e99fbd6f05dc05341bdfbbd7e3b2b86785abc22` exists, and
  `SKILL.md:81` is the `## Queue-drain craft` heading at that commit (end line 314 not checked).

## Residual risk and verification gaps

- Nothing executed. F1, F3, F4 and F6 are source-read or inference-labelled; L1 should confirm with one
  unreadable-directory case (F1), one null-bucket case (F3) and one `patch_applied: true` expectation (F6)
  after integration. Do not treat any of these as runtime evidence.
- Gson behavior (null → null, object-expected failure on arrays, strict NaN) is from library knowledge plus
  the Java source paths cited, not from a run.
- No fixture covers F1, F3, F5 or F6; any added expectation must be handwritten from the source lines above,
  with no hashes invented.
- Host/tooling: none installed or updated by this seat.
