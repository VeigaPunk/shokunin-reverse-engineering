# FBucketPriority — w2 adversarial fixture cases: bucket priority, `all` dedup, windows-no-unix

Scope: authored 18 new independent schema-conforming cases at
`.ufo/waves/round-16/w2/BucketPriority-cases.json` attacking the produced C1
artifacts (`selection.py` + fixture schema in `selfcheck.py`), plus a bounded
defect review of the bucket-matching surface. No implementation edit, no
execution of the model or runner. Source law read directly from
`Base-src.zip` (`GoApiSnapshot.java`) and `Utility-src.zip`
(`generic/jar/ResourceFile.java`) / `Generic-src.zip`
(`ghidra/framework/Application.java`) at `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/`.

## Files written

- `.ufo/waves/round-16/w2/BucketPriority-cases.json` — bare-list of 18 cases,
  selfcheck.py schema (`files` uses both `{}` JSON objects and raw/`{"raw":…}`
  strings; `expect_error` uses `{"type":…}` mapping form). Handwritten
  expected values only; no size/sha256 assertions anywhere.

## Case inventory (attack → source anchor)

| id | attack | anchor |
|---|---|---|
| linux_priority_reverse_key_order | file key order is exact reverse of search order; buckets must follow search priority | read() 228-237 iterates `archNames`, not parsed keys |
| linux_priority_skips_absent_slots | absent slots skipped; `linux` beats `amd64`; base without `all` still base_only | 218-224 filter + 228-237 order |
| linux_exact_diff_unpatched_buckets | diff selected → buckets still unpatched base, label asserted | 133-144 merge never runs; contract label clause |
| linux_fallback_diff_unpatched_buckets | nearest-lower diff + file-order `all`-first base | getPatchVerDiffFile 148-166 |
| dedup_all_when_goos_is_all | `goos="all"` puts `all` twice in the list; first occurrence wins → `all` outranks `amd64` | List.of 108-109 retains dup; LinkedHashMap 228-237 keeps first |
| dedup_all_when_goos_and_goarch_all | triple `all` collapses to one bucket; emitted order keeps literals | same |
| windows_never_matches_unix | windows slot is `""`; `unix` key present in file must not match | IS_GOOS_UNIX 180-181; `""` dropped 230-232 |
| windows_unix_only_content_shadowed | only unix+amd64+all present → windows request sees `[amd64, all]` | w1 ReviewBucketOrder D3 counterexample |
| windows_fallback_diff_no_unix_unpatched | unix exclusion under fallback_diff + label | 148-166 + label clause |
| null_valued_bucket_not_applicable | **falsification**: null-valued key must be omitted (Java value-presence) vs model key-presence | read() 233-236 `arch != null` |
| goos_unix_literal_not_in_unix_set | literal `goos="unix"` is NOT in IS_GOOS_UNIX; `unix` still matches via the goos slot | 180-181, 108-109 |
| goos_case_sensitive_no_unix | `Linux` ∉ set → no unix slot, `linux`/`unix` keys inapplicable | exact-match contains 180-181 |
| zero_matching_buckets_still_base_only | zero retained buckets = non-EMPTY-but-isInvalid, not missing_base | isInvalid 503-505; w1 D5 unresolved |
| directory_at_base_path_is_missing_base | directory occupying base name → missing_base even with diff present | Application.java:369-372 dir→FileNotFoundException→null; 124-126 early return |
| directory_at_diff_path_falls_to_lower | directory occupying exact diff name → falls to 1.21.2, not selected | Application.java:369-372; loop 153-156 |
| patchverdiffs_as_plain_file | non-directory `patchverdiffs` → base_only, no error | findModuleFile miss → null diff → 128-131 |
| empty_goos_request_error | `goos:""` → RequestError (contract extension; Java would not reject) | contract non-empty selector |
| empty_goarch_request_error | symmetric for goarch | contract |

## Findings against produced artifacts

### F1 — MEDIUM (model divergence, latent). Null-valued bucket counted as applicable

`selection.py:242-248` computes `keys = set(_top_level_keys(...))` then tests
`name in keys` — key **presence** only. Java `read()` builds `arches` from
deserialized values and applies `arch != null` at GoApiSnapshot.java:233-236,
so a top-level `"linux": null` is present as a key but NOT retained. A
base file with `{"linux": null, "amd64": {}, "all": {}}` under linux/amd64:
model would report `["linux","amd64","all"]`; Java retains
`["amd64","all"]`. Latent only — w1 ReviewBucketOrder's data scan found no
null bucket in the 11 shipped bases. Fixture `null_valued_bucket_not_applicable`
pins source-truth (omission); per L1's refinement (model owner filters
top-level nulls) the case is intended to pass after that filter lands; if
"top-level key preview" is the settled contract instead, the case records
the divergence explicitly rather than silently passing a presence-only
runner. Related but distinct: `negative-fixtures.json`'s
`unsupported-shape-bucket-nonobject-preview` deliberately keeps a non-object
*non-null* bucket (`"all": [...]`), consistent with Java (`gson.fromJson`
returns non-null GoArch). That case and mine are complementary, not in
conflict: null → dropped, non-null-wrong-shape → retained.

### F2 — LOW (documented parity, asserted). Literal duplicates in `arch_search_order`

For `goos="all"` (or `goarch="all"`, or `goos="unix"` patterns), Java's
`List.of` (108-109) retains the literal duplicate; `read()` dedups at
228-237 by first occurrence. `arch_search_order` in selection.py:115-121
mirrors the literal list (empties dropped) so duplicates surface — faithful,
but it means `arch_search_order` is the *literal* order while
`base_matching_buckets` is the *deduped* order. Cases
`dedup_all_when_goos_is_all` / `_when_goos_and_goarch_all` pin both
behaviors; a dedup-first-emission runner and a no-dedup-buckets runner both
fail.

### F3 — confirmed parity (not defects): directory-vs-file and non-dir `patchverdiffs`

`Application.getDataFileInModule` (Application.java:369-372) throws for
directories → `getApiSnapshotFile` catches IOException → null, exactly the
model's `is_file()` gate (`_describe_file` at selection.py:130-131) and the
`iterdir()` OSError-to-empty handling (selection.py:219-222). The three
fixtures pin this for base path, diff path, and the subdir itself — they
discriminate `exists()`-only or name-only-scanning runners.

### F4 — noted, unpinned. `patchverdiffs` when base dir unreadable mid-run

`diff_dir.iterdir()` swallows any OSError (selection.py:219-222), including
permission-denied on `patchverdiffs/`, reporting `base_only` rather than
`unreadable`. Java's loop is a per-name probe, so a permission failure there
also manifests as "no diff" — the model's blanket OSError swallow is wider
but coincides on the observable outcome. Recorded as a limit note; not
fixturable without chmod support in the schema.

## Calibration notes (decisions asserted, stated for L1)

- Every base-present case asserts `base_matching_buckets_source:
  "unpatched_base_file"` (L1 calibration invariant); the one missing-base
  case asserts `null` (selection.py:210 emits `None` there — consistent
  with "null when base missing" in SelectorModel.md:64-66).
- `arch_search_order` asserted on every non-error case including
  missing_base (list computed before base lookup, selection.py:186-188) —
  consistent with existing `missing-base-nonunix-arch-order` precedent.
- `selected_patch`: `0` on base_only, `null` on missing_base, integer on
  diff-selected — per L1's settled semantics (SelectorFixtures.md:41,
  SelectorModel.md:15-16); all cases conform.
- Fixture shape: bare list (SelectorFixtures.md:35); `{"path": …}` assertions
  only for `base`/`selected_diff` (SelectorFixtures.md:37); raw-string files
  used for `linux_priority_reverse_key_order` (guarantees key order through
  the serializer) and the two plain-file/directory-occupier cases;
  `expect_error` uses the `{"type": …}` mapping form.
- Disjointness: my 18 ids do not collide with `selection-fixtures.json` (9)
  or `negative-fixtures.json` (17). `windows_never_matches_unix` /
  `windows_fallback_diff_no_unix_unpatched` extend `windows_omission`
  (which covers only exact_diff, all-buckets-present) — stated in-case.

## Verification gaps / limits

- Nothing executed: no selfcheck run, no model import, no Ghidra runtime.
  Expected values derived solely from GoApiSnapshot.java /
  Application.java / contract docs; if any expectation diverges from the
  produced model's actual behavior, the case itself is the finding.
- `null_valued_bucket_not_applicable` is the only case whose pass/fail
  encodes a live contract decision (F1); the rest assert settled law.
- No size/sha256 expectations (contract: handwritten values only).
- Single JSON syntax check on my own artifact only (see below); no
  tests/builds/linters run per contract.

## Retained evidence

- `GoApiSnapshot.java` (Base-src.zip, ghidra_12.1.4_PUBLIC): get() 102-116,
  search order 108-109, getApiSnapshotJsonFile 118-146, getPatchVerDiffFile
  148-166, getApiSnapshotFile 168-178, IS_GOOS_UNIX 180-181, read() 205-240
  (null-bucket check 233-236, ordered emit 228-237), isInvalid 503-505.
- `ghidra/framework/Application.java` (Generic-src.zip): getDataFileInModule
  354-374, directory rejection 369-372.
- `generic/jar/ResourceFile.java` (Utility-src.zip): getFile(boolean) 246-252.
- Model: `.ufo/waves/round-16/selection.py` (order 105-121, describe 124-144,
  key scan 147-167, select 170-275); `.ufo/waves/round-16/selfcheck.py`
  schema lines 20-61, materialize 120-156, compare 216-265.
- Contract decisions: `w1/SelectorFixtures.md`, `w1/SelectorModel.md`,
  `w1/ReviewBucketOrder.md` (D1-D5, esp. D3 windows/unix and D5 zero-match).

Tool installs/updates: none. Commands run: file reads and `unzip -l`/`-p`
listings only, plus one `python3 -c "json.load"` syntax check on my own
fixture file.
