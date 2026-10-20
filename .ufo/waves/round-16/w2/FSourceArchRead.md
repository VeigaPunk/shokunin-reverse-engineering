# FSourceArchRead — empty `""` slot and LinkedHashMap bucket order vs emitted model fields

Round 16, C1 (and C2 coupling only). Read-only scout: no execution of `selection.py`,
`selfcheck.py`, `controls.py` or any fixture; no builds/tests/linters/formatters; no Java run;
no installs. Source S003 reopened from
`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`
member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` (plus `GoVer.java`);
data from the installed `typeinfo/golang/` tree.

Reviewed artifact state (sha256, mtime; files changed at 05:25–05:26 while this seat was
reading — the null-value filter and the `patch > 0` guard appeared mid-review):

| artifact | sha256 | mtime |
|---|---|---|
| `.ufo/waves/round-16/selection.py` | `c9e7eb226fb7e7cef2eba0fc85041e03cb4348d1886ff32627b3f6117a273042` | 05:26:09 |
| `.ufo/waves/round-16/selfcheck.py` | `965ef53eb5c8baeb816fcdf2ad837edb13c00c1c703e5b78adf94fb477e53715` | 05:26:06 |
| `.ufo/waves/round-16/selection-fixtures.json` | `ff2483d88ad77a39ef5fb2f6ad7310ba6d940094debe03dc6daa0e8b802fcaaa` | 05:15:50 |
| `.ufo/waves/round-16/negative-fixtures.json` | `b27a29ac16b9b02a7cfc3923748a6b1da192d79b298984e9d9071899c290b651` | 05:25:10 |
| `.ufo/waves/round-16/controls.py` | `5f9fe949d5a3ed3ff9116fec67774dc2e4fabc05c6d58242fa1ca7e7c159a917` | 05:20:37 |

## Source facts used

| Fact | Anchor |
|---|---|
| search list, literal `""` in unix slot for non-unix GOOS | GoApiSnapshot.java:108-109 |
| unix set (aix android darwin dragonfly freebsd hurd illumos ios linux netbsd openbsd solaris) | :180-181 |
| keep-set filter while streaming JSON | :212-218 |
| results `LinkedHashMap` built in `archNames` order; skip null/empty; skip null `GoArch` | :228-237 (empty :230-232, null :233-236) |
| result stored with the *requested* `GoVer` | :239 |
| base always `go<M.m.0>.json`; missing base returns before diff search | :122-126 |
| diff probe descending, condition `patch > 0` | :148-166 (loop :153-156) |
| filename construction `go<toString>.json<suffix>` | :168-172 |
| `getApiFile` two-part fallback is off the `get` path | :183-192 |
| reader stops after `endObject()`; trailing bytes never read | :215-226 |

## Verdict on the two named attack themes

**Empty `""` slot — bounded no-finding.** `selection.py:105-121` drops the slot and emits a
4-element order for non-unix GOOS. That is the only place the placeholder could surface:
`read()` skips it before `arches.get` (:230-232), and the results map is ordered by the same
list, so no bucket can ever contain it. A literal `""` top-level key in a base JSON is also
dropped by Java (results loop) and by the model (order never contains `""`), for unix and
non-unix goals alike. The decision is consistently stated in the knowledge doc (lines 25, 28),
`corpus/lessons/round-16.md:75`, the `arch_search_order` docstring (:105-110), the
`windows_omission` fixture (4-element order, base contains `unix`) and the negative
`missing-base-nonunix-arch-order` case. No observable divergence.

**LinkedHashMap order vs model fields — no parity defect in current code.** For any document
both parsers accept, `selection.py:256-262` reproduces all three filters of `read():228-237`:
membership restricted to the search order (the keep set), `""` excluded, first-occurrence
dedupe, and null values dropped (now at `selection.py:173`, matching the `arch != null` guard at
:233-236). The `keys` set destroys JSON order, and iteration over `order` reinstates the
LinkedHashMap priority; file order and alphabetical order both diverge from the expected lists,
so the property is genuinely tested (`exact_diff`, `lower_fallback`, `unix_order` have base key
order ≠ expected bucket order). Docs (`corpus/knowledge/2026-10-20-r16-go-selection-preview.md`
lines 26, 38) now say "non-null" and explain the null skip. No finding in the field derivation
itself.

## Concrete findings (both are evidence-coverage defects in produced C1 artifacts, not shipped-data errors)

### F1 — Low / calibration: the newly added null filter is unpinned by any fixture

- **Observed:** `selection.py:147-173` now returns only non-null top-level names
  (`[k for k, v in doc.items() if v is not None]`, line 173), and the knowledge doc (line 26
  "non-null", line 38 "omitting null values because Java `read:233-235` skips null arches")
  asserts that behavior. A static scan of all 26 cases in `selection-fixtures.json` (9) and
  `negative-fixtures.json` (17) finds **no** base document with a null-valued top-level bucket
  and no `raw` payload encoding one.
- **Why it matters:** reverting line 173 to `list(doc.keys())` would make a
  `{"all": null, "linux": {...}}` base report buckets `["linux","all"]`; every current case
  still passes, because the non-object fixture
  (`unsupported-shape-bucket-nonobject-preview`) uses a non-null array value. The claim added
  during this round is unguarded.
- **Minimal counterexample (hand-authored; no hashes):** request `1.21.0`, linux/amd64, files
  `{"go1.21.0.json": {"all": null, "linux": {"Funcs": {}, "Types": {}}}}` → expected
  `status: base_only`, `base_matching_buckets: ["linux"]`, `selected_patch: 0`.
- **Note:** whether Gson really returns null for a JSON `null` value is source-inferred
  (`Gson.fromJson(JsonReader, …)` NULL token), not executed; the project doc already asserts it.
  Confidence: high on the coverage gap, medium on Gson specifics.

### F2 — Low / calibration: `0 < cand` (`selection.py:244`) is now untested

- **Observed:** the new `if patch > 0:` guard (`selection.py:230`) means the `patch0` case
  (request `1.23.0`, which ships `patchverdiffs/go1.23.0.json.diff`) no longer reaches the
  candidate loop. No case in either fixture file has a request patch > 0 together with a
  `patchverdiffs/go<M.m>.0.json.diff` (static scan, 26 cases).
- **Why it matters:** Java's loop condition `patchVer.getPatch() > 0` (:153-156) never probes
  patch 0, so a `.0` diff must never be a candidate even for a nonzero request. A mutant that
  weakens line 244 to `cand >= 0` (guard intact) selects the `.0` diff as `fallback_diff` for
  request `1.21.3`; no current case fails, because `patch0` is insulated by the new guard and
  every other case has no `.0` diff.
- **Minimal counterexample:** request `1.21.3`, files
  `{"go1.21.0.json": {"all": {}}, "patchverdiffs/go1.21.0.json.diff": {}}` → expected
  `status: base_only`, `selected_diff: null`, `selected_patch: 0`,
  `base_matching_buckets: ["all"]`. (The `.0` diff must be created but never selected.)
- Confidence: high (fixture/code reading; no execution).

### F3 — Lowest / wording: `_top_level_keys` docstring overstates Java parity

- `selection.py:156-158` says non-object/unparseable JSON raises so the preview "never claims
  membership for a document the Java reader could not open". `read()` stops at
  `reader.endObject()` (:225-226) and never consumes trailing bytes, so with no diff selected a
  base `{"all": {}}` followed by garbage yields a Java snapshot containing `all` (with a diff,
  the base first passes through `JsonPatchApplier`, not modeled here), while
  `json.load` raises `JSONDecodeError("Extra data")` → `UnreadableError` / exit 2 (stdlib
  `JSONDecoder.decode`, verified locally). The divergence direction is conservative (false
  "unreadable", never a false bucket), and shipped bases are clean UTF-8 JSON. Suggest saying
  "Python-parseable" or recording the trailing-data divergence; no code change required for the
  C1 claim.
- Confidence: high on Python and Java control flow.

### F4 — Lowest / doc precision: `arch_search_order` is the get() list minus `""`, not the deduped results order

- For degenerate selectors the emitted list keeps duplicates (e.g. `goarch="all"` →
  `["linux-all","linux","unix","all","all"]`; `goarch="linux"` duplicates `linux`), while
  `read()`'s results map and `base_matching_buckets` dedupe. The knowledge doc line 25 and
  lesson line 75 call the field the "effective `read` order"; that is accurate for the *input*
  list, not the results map. No shipped GOOS/GOARCH pair hits this (GOARCH never equals `all`
  or the GOOS in Go's real value set), and no fixture pins it. Either state the distinction or
  dedupe the emitted list; no source-parity defect.

## Bounded divergences seen and not claimed as defects

- A diff candidate that exists but is not a regular file (directory/FIFO/socket named
  `goX.Y.Z.json.diff`) is treated as absent (`_describe_file`, `selection.py:130-131`) and the
  model falls back to a lower diff; Java would return the path from `getApiSnapshotFile` and
  fail later in patch reading. Synthetic tree only; no shipped entry.
- An unreadable `patchverdiffs/` directory is exit 2 (`selection.py:236-238`); Java's
  module-data probe returns null and yields base-only. The model labels this unreadable input,
  which the knowledge doc permits; not a selection-order issue.
- Non-object, non-null kept bucket values are reported as present while Java would fail parsing
  them; this is explicitly labelled by the `unsupported-shape-bucket-nonobject-preview` fixture
  and knowledge doc line 38. Correctly not presented as parity.

## C2 coupling check

`controls.py` contains no reference to `selection.py`, `arch_search_order`,
`base_matching_buckets` or the Go model files (grep over the current artifact), so the order
findings above do not implicate C2. The four outside-route corrections, the red-before control
and the knowledge/lesson wording are out of this seat's question.

## Limits / unknowns

- Not executed: `selection.py`, `selfcheck.py`, any fixture, Java/Gson, or Ghidra. Gson's null
  and parse behavior is source-inferred; Java control flow is source-read.
- `Application.getModuleDataFile` multi-root precedence and derived-data caching are not modeled
  (documented single-`--root` limit).
- The knowledge doc recheck (line 3) points at `.ufo/waves/round-16/verification.json`, which
  does not exist at review time (observed). L1's post-wave receipts must land at exactly that
  path or the recheck instruction is dangling.
- If `selection.py` moves again after 05:26:09, recheck F1/F2 against the new hash; the fixture
  files were last written before the null filter and the `patch > 0` guard.
