# FSourceLabel — requested label vs selected-patch bytes, and the EMPTY metadata limit

Seat: KaidokuR16.FSourceLabel (scout, leaf). Axes: **depth**, **calibration**.
Evidence class: S003 source members + produced round-16 artifacts + installed-data names.
No execution: `selection.py`, `selfcheck.py`, any fixture, Java/Gson/Ghidra, build, test or lint;
no target, provider or install. Findings are static source reads.

Artifacts pinned while reviewing (churn observed; see Limits):

- `.ufo/waves/round-16/selection.py` sha256 `6917da09fe61644a0e091e4e1763eda89c32db9de02aa29dad9d275cd50ef430`, 331 lines, mtime 05:33:40.
- `.ufo/waves/round-16/selection-fixtures.json` `ff2483d8…`; `negative-fixtures.json` `b27a29ac…`.
- `corpus/knowledge/2026-10-20-r16-go-selection-preview.md` `f2514564…`.
- `selfcheck.py` changed twice under review (`42458e1f…` → `240be5f3…`); **no finding below relies on it.**
- S003: `Base-src.zip` members `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java`,
  `ghidra/app/util/bin/format/golang/GoVer.java`; also `Ghidra/Framework/Generic/lib/Generic-src.zip`
  member `ghidra/framework/Application.java`.

Assigned attack: does `requested` (the normalized input) describe the bytes actually selected by
`base`/`selected_diff`/`selected_patch`, and what happens at the `GoApiSnapshot.EMPTY` boundary?

## Verdict on the assigned attack — no misselection on the readable-regular-file model

Re-derived by hand from S003 (not executed); all 9 positive and 17 negative fixture expectations
were re-read and re-derived, and no wrong expected value, invented hash/size or asserted pass was found:

- Base is always `go<M>.<m>.0.json` (`GoApiSnapshot.java:122-123`); absence returns before the diff
  probe (`:124-126`) → `missing_base`, null base/diff/patch. Match.
- Patch `p == 0` never enters the walk (`:153`) → base provider, patch 0. Match (`patch0` fixture).
- `p > 0` walks `q = p … 1` within the same minor, first present wins (`:153-156`); the preview's
  numeric max over canonical same-minor names in `1..p` is equivalent for a readable directory of
  regular files; `q == p` is `exact_diff`, `q < p` is `fallback_diff`, none is `base_only`.
- `selected_patch` is filename-derived, never a content digest; a selected diff is hashed but not
  parsed or applied (`:134-144` is the Java path the preview does not run). The knowledge entry's
  "exact requested **filename**" wording is accurate.
- `requested` is passed to `read` only after a provider exists (`:105-113`), and Java stores the
  *requested* GoVer even when the applied diff is a lower fallback (`:239`) — so on `fallback_diff`
  the object label and the diff's own patch genuinely differ. The preview emits both values.
- Installed names observed: bases `go1.15.0.json … go1.25.0.json`; `patchverdiffs/go1.15.1…go1.24.6.json.diff`.
  Request 1.24.7 selects diff 6 (fallback); a 1.25.x request has no same-minor diff (base only).

Boundary already bounded elsewhere and not re-reported: a `patchverdiffs/` that cannot be listed is
refused with exit 2 (`selection.py:240-248`) rather than Java's IOException→null→base-only. That is
the interface's declared "unreadable input" choice, covered by FSourceDiffOrder §2.3; it does not
change any emitted selection.

## FSL-1 — Low / calibration: the `requested` row asserts a stored Java label the EMPTY path does not have

- Doc: `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:24` —
  "The model's explicit normalized input; Java passes the original GoVer to `read` at `:111` and
  stores it at `:239`." The Java half is stated without a status qualifier.
- Source: `get` calls `read(...)` only inside `if (bp != null)` (`GoApiSnapshot.java:105-113`); a null
  provider returns `EMPTY` (`:115`), and `EMPTY` stores `GoVer.INVALID = (0,0,0)` (`:242`;
  `GoVer.java:35`). `read` does store the caller's GoVer at `:239` — but that line is unreachable on
  `missing_base`.
- Artifact: `requested` is emitted on every status (`selection.py:216` for `missing_base`,
  `:283` otherwise) and is always the caller's normalized string. On `missing_base` it therefore
  labels no Java snapshot; the Java object is `EMPTY`/`INVALID`. No output field carries that
  distinction — `status: "missing_base"` is the only signal.
- This is not a misselection and the module docstring plus the table's missing-base row do say
  `EMPTY`. The defect is the *unqualified* `requested` row: a reader can carry "a stored version
  label exists" into the one status where it does not.
- Smallest correction (docs only): scope the row — "when a provider exists; on `missing_base` `get`
  returns `EMPTY`, whose stored GoVer is `INVALID`, so `requested` is an input echo, not the object's
  label." A `snapshot_version: null` field would be a contract change and is not required.

## FSL-2 — Low / maintainability + calibration: `requested` and `request_raw` cannot diverge, and no fixture pins either

- `parse_request` rejects leading zeros, two-part forms, wildcard patch, suffixes and trailing text
  (`selection.py:79-101`), so `normalized = "%d.%d.%d" % …` (`:205`) reproduces `request`
  byte-for-byte for every accepted input. `requested` (`:216`, `:283`) and `request_raw`
  (`:217`, `:284`) are the same string in every emitted result.
- No fixture asserts `request_raw`, `goos` or `goarch`: the asserted result keys across both fixture
  files are only `status`, `requested`, `base`, `selected_diff`, `selected_patch`,
  `arch_search_order`, `base_matching_buckets`, `patch_applied`, `evidence_class`. The equality
  invariant is therefore untested, and the second key is dead weight under the current grammar.
- Options: drop `request_raw` (the wave contract does not require it), or keep it as an explicitly
  future-facing escape hatch for a relaxed grammar and pin `request_raw == requested` in one case.
  The C1 phrase "requested normalized input" should not be read as evidence that the model parses or
  normalizes arbitrary `GoVer` forms; it rejects them before any normalization.

## Calibration guard — do not "repair" the directory-at-diff-name skip

`_describe_file` returns `None` for a non-regular path (`selection.py:141-142`) and the walk continues.
One sibling finding reads Java as *selecting* a directory named `goM.m.p.json.diff`. The shipped
framework does the opposite: `Application.getDataFileInModule` throws `FileNotFoundException` when
the found resource `isDirectory()` (`Generic-src.zip:ghidra/framework/Application.java:369-372`), and
`getApiSnapshotFile` catches `IOException` → `null` (`GoApiSnapshot.java:175-177`), so the walk
continues exactly as the model does. `patchverdiffs` itself being a regular file also resolves to a
missing child → `null` → base-only (`Application.java:364-367`). No change is warranted.

## Overlap checked, deliberately not re-reported

- Null-valued bucket: the code now filters it (`selection.py:183`) and docs `:26`/`:38` say so, but
  the shared fixtures still contain no `"all": null` base. FSourceArchRead F1 / FBucketPriority F1
  already propose that case; their reading matches mine.
- Empty-object base `{}` vs `missing_base`: covered by FParseVsMissing's proposed case 12.
- Runner materialization / duplicate-id exit leaks: FFixtureComparator F7/F8; `selfcheck.py` moved
  after I read it, so I make no claim on its current bytes.
- Numeric-vs-lexicographic diff fixture gap: FSourceDiffOrder §3.

## Limits

- Source read only; no JVM, Gson, Ghidra, provider or target execution. No claim about Gson's runtime
  null mapping is used here; the Java `arch != null` guard is source-visible.
- Single `--root`; module-data precedence, derived-data cache and source/loaded-class identity are
  unmodeled and already disclosed in the entry.
- `selection.py` changed during this review (last read digest `6917da09…`). If it moves again,
  FSL-1/FSL-2 anchors must be re-read at the new digest; their line numbers are current for that file.
- The entry's recheck points at `.ufo/waves/round-16/verification.json`, absent at review time (also
  observed by FSourceArchRead). L1's post-wave receipt must land at that path or the recheck is
  dangling; not counted as a defect here.

Tools installed or upgraded: none.

Report: .ufo/waves/round-16/w2/FSourceLabel.md
