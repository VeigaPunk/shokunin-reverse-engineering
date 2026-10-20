# FSourceBaseFirst — missing-base early return and getApiFile exclusion

Scope: the produced round-16 C1/C2 artifacts against the actual installed source,
not a hypothetical implementation. Attack: does `select_snapshot` place the
base-existence short-circuit where `GoApiSnapshot.getApiSnapshotJsonFile` does, and
does excluding `getApiFile` match the actual selector? Source/data/model evidence
only; nothing was executed (no selection.py/selfcheck.py/controls.py, no build, no
Java). Tooling: none installed or updated.

Observed artifact pin (files changed under me during review; these are the versions
this report judges):
`selection.py` mtime 2026-10-20T05:26:09-03:00, 12789 bytes; `selfcheck.py`
latest observed 2026-10-20T05:28:34-03:00, 19000 bytes; `selection-fixtures.json` 05:15:50;
`negative-fixtures.json` 05:25:10. A later edit supersedes any line here.

LSP note: no language server answers a member inside `Base-src.zip` and there is no
project Java server for the shipped tree, so control-flow claims below are direct
line reads of the archive member. `zipgrep` was used only for the caller census in
§2 and is labelled as such, never as semantic proof.

## 1. Missing-base early return — bounded no-finding

Source order (member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java`):

- `get()` L102-116: the only call is `getApiSnapshotJsonFile(goVer, monitor)`
  (L105); a null provider returns `GoApiSnapshot.EMPTY` (L115; `EMPTY` at
  L242). No second lookup, no diff attempt.
- `getApiSnapshotJsonFile()` L122-126: `baseVer = goVer.withPatch(0)` (L122),
  base via `getApiSnapshotFile(baseVer, "", "")` (L123), then
  `if (jsonFile == null) { return null; }` at L124-126 — **before**
  `getPatchVerDiffFile(goVer)` at L128. A present diff cannot rescue an absent
  base.
- `getApiSnapshotFile()` L168-178: name is
  `typeinfo/golang/<subdir>go<M.m.p>.json<suffix>` (L170-171) and any `IOException`
  becomes null (L175-176). `Application.getModuleDataFile` throws
  `FileNotFoundException` when the path is absent (`Application.java` L354-375,
  null at L364-367) **or is a directory** (L369-372); `GModule.findModuleFile`
  returns a resource only when `exists()` (`GModule.java` L147-155), and
  `FileResource.exists()` is plain `File.exists()` (`FileResource.java`
  L139-141). So absent, directory, and dangling-symlink bases all become null,
  i.e. `EMPTY`/missing base. Loose-file bytes are never opened on this path.

Produced model (`selection.py`): `base_rel` is `go<M.m.0>.json` (L201); the
missing-base return is L203-215, before the diff directory is touched at L230-246.
Output has `status: missing_base`, null base/diff/selected_patch, empty buckets,
`patch_applied: false`, exit 0 — the source outcome, with the sha256/size of *no*
file rather than an invented identity.

Fixture pins are consistent, not merely model-derived:
`selection-fixtures.json:3` (`missing_base_despite_diff`, diff present, base absent),
and `negative-fixtures.json:147` (`missing-base-diff-present-unreachable`),
`:111` (empty root), `:128` (two-part name), `:185` (non-unix order). No defect.

Edge rulings I checked by source, all matching the model:
- base is a directory → `Application.java:369-372` → null → missing_base; model
  `Path.is_file()` is False → missing_base.
- base is a dangling symlink → `exists()` false (`FileResource.java:139-141`) →
  null → missing_base; model is_file False → missing_base.
- base exists but is unreadable as a regular file → `FileResource.getResourceAsFile`
  returns the `File` without reading (`FileResource.java:149-151`), so the Java
  failure comes later when the provider is opened (`get()` declares IOException);
  model raises `UnreadableError` → exit 2. Both are errors, not missing_base; this
  is a boundary match, not file-identity parity.

## 2. getApiFile exclusion — bounded no-finding, stronger than the docstring

`GoApiSnapshot.getApiFile` L183-192 first tries `go<M.m.p>.json`, and only when that
is not a file **and patch == 0** retries `go<M.m>.json`. It is never reached from
`get()`: `get()` calls only `getApiSnapshotJsonFile` (L105), whose base lookup uses
`getApiSnapshotFile` (L123), never `getApiFile`.

Caller census: `zipgrep -n 'getApiFile'` over all installed
`Ghidra/**/lib/*-src.zip` returns exactly one hit, the declaration at
`GoApiSnapshot.java:183`. There is no in-tree caller in shipped source, so the
minor-only fallback is not on any shipped snapshot-selection path, not merely off
the `get()` branch. The model's exclusion (docstring `selection.py:20-22`) is
therefore correct. The two-part case is pinned by
`negative-fixtures.json:128` (`go1.21.json` present, request `1.21.0`, expected
`missing_base`), so a regression that grew a two-part fallback would fail rather
than pass silently.

Limit: this is shipped-source evidence. External scripts/Jython using the public
`getApiFile` are outside both the archive and the preview; the docs' "separate
utility" wording is accurate but does not establish runtime callers outside the
tree.

## 3. Concrete current defect (adjacent, not in the two named laws)

### D1 — diff filename components are unbounded, then converted with `int()`

- `selection.py:55-56` (`_DIFF_NAME_RE`) uses unbounded `[1-9][0-9]*` for all three
  components; `selection.py:242-243` runs `int(m.group(1))`, `int(m.group(2))`,
  `int(m.group(3))` on every matching directory entry.
- Counterexample by reading: a foreign entry
  `patchverdiffs/go1.21.<4301-or-more-digits>.json.diff` with a valid base present.
  On CPython with the default int-string digit limit (`sys.int_info
  .default_max_str_digits`, 4300 in 3.11+ — [INFERENCE], interpreter not run), the
  patch-component conversion raises `ValueError` inside `select_snapshot`.
  `main` catches only `(RequestError, UnreadableError)` (L308-314), so this is an
  uncaught traceback and exit 1, not the documented exit 2 and not the source
  outcome.
- Source outcome: `GoVer.toString()` components are Java `int`s (`GoVer.java`
  L155-159; int range at most 10 digits), and `getPatchVerDiffFile` (L153-156) only
  probes names generated from `patchVer`; a filename with a >10-digit component is
  never probed and is invisible to Java. The preview should ignore it, not convert
  it.
- The request path is already safe (`selection.py:87`, length check before `int()`);
  only the directory-entry path lacks the bound. Fix direction: bound
  `_DIFF_NAME_RE` components like `_VERSION_RE` (`0|[1-9][0-9]{0,9}`) or catch
  `ValueError` in the candidate loop.
- This was reported as FSourceCells F5 and is **still present** in the observed
  05:26 file; SelectorModel's note only claims the listing/gating fold, so L1 must
  not treat F5 as integrated.

## 4. Calibration observations (not asserted as source-law defects)

- **Unreadable `patchverdiffs/`:** `selection.py:230-238` raises `UnreadableError`
  on a `PermissionError`. Java's probes call `findModuleFile` → `exists()`
  (`GModule.java:147-155`, `FileResource.java:139-141`); under EACCES the child does
  not exist from the process's view, so every probe returns null and
  `getApiSnapshotJsonFile` returns the base provider (base_only, with a fallback
  warning for a nonzero request). [INFERENCE: JDK `File.exists()` false on EACCES;
  not executed.] The preview's fail-closed exit 2 is its own documented contract
  (module comment L221-228; knowledge entry's exit-2 sentence), so this is a
  disclosed model boundary — but the docs do not state that Ghidra would still
  select base_only there. Do not claim selection parity for an unreadable diff
  directory.
- **`missing_base` carries an arch order the source never builds:** `order` is
  computed at `selection.py:194` and emitted at L212; Java constructs
  `archSearchOrder` only inside the non-null provider branch
  (`GoApiSnapshot.java:105-111`). The value is a pure function of the inputs, and
  `negative-fixtures.json:185` pins the model, not a source observation on the
  missing-base state. Wording in fixtures/docs should keep it hypothetical for this
  status; no output value is wrong.
- **`base_matching_buckets` on an exact/fallback diff** is correctly labelled
  `unpatched_base_file` (`selection.py:280-286`), so the unpatched projection is not
  passed off as post-patch content.

## 5. Version-state notes L1 needs

- `selfcheck.py` at the latest observed version prints per-case `FixtureError`
  as `ERROR` and returns 2 (harness block L412-436), and the header documents that
  (L67-69); presence checks and authored forced-key expectations are also current
  (`_compare` L238-300). The earlier exit-1-on-schema-error mismatch no longer
  exists in this version; do not carry a stale finding forward.
- Negative fixtures are not in the default set (`selfcheck.py` default is sibling
  `selection-fixtures.json`). The getApiFile-exclusion and missing-base-with-diff
  pins live in `negative-fixtures.json`; one execution of
  `python3 -I .ufo/waves/round-16/selfcheck.py --fixtures .ufo/waves/round-16/selection-fixtures.json --fixtures .ufo/waves/round-16/negative-fixtures.json`
  is what exercises them. This is an execution instruction, not a claim that I ran
  it.
- D1 remains open at the observed revision; the other two named attacks need no
  implementation change.

## 6. Remaining unknowns / limits

- No Java or Python was run; EACCES and int-digit-limit behaviors are labelled
  inference. D1's exact digit threshold depends on the interpreter L1 uses.
- Module-data search roots, jars/derived-data cache and non-filesystem resources are
  not modelled; the preview takes one explicit root. A root that is absent yields
  exit 2, whereas an absent module-data root inside Ghidra would surface as
  missing_base; this split is a stated CLI boundary, not source parity.
- `getApiFile` callers outside shipped source (scripts, external tooling) were not
  and cannot be observed from the archive.
- Installs/updates: none.
