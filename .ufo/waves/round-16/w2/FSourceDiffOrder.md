# FSourceDiffOrder — canonical-name numeric max vs the same-minor descending walk

Seat: KaidokuR16.FSourceDiffOrder (scout, leaf). Axes: **depth**, **calibration**.
Evidence class: source + produced round-16 artifacts. No execution of `selection.py`/`selfcheck.py`,
no builds/tests/linters, no target, no provider. Advisory only.

Artifacts read (all absolute paths in this repo unless noted):

- `.ufo/waves/round-16/selection.py` (315 lines)
- `.ufo/waves/round-16/selfcheck.py`, `.ufo/waves/round-16/selection-fixtures.json`,
  `.ufo/waves/round-16/negative-fixtures.json`, `.ufo/waves/round-16/measure.py`
- `corpus/knowledge/2026-10-20-r16-go-selection-preview.md`
- `.ufo/waves/round-16/w1/ReviewLowerDiff.md`
- S003 source archive `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`
  members `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` and
  `ghidra/app/util/bin/format/golang/GoVer.java`
- Resolution chain used by the selector: `Ghidra/Framework/Generic/lib/Generic-src.zip`
  (`ghidra/framework/Application.java`, `getDataFileInModule`), `Ghidra/Framework/Utility/lib/Utility-src.zip`
  (`ghidra/framework/GModule.java`, `findModuleFile`), `Ghidra/Framework/Utility/lib/Utility-src.zip`
  (`generic/jar/ResourceFile.java`, `getFile`)

No `lsp` device is mounted in this seat; Python has no server for these files and the Java source lives
inside an archive. Semantic anchors below were traced by direct archive-member reads with line numbers,
not by text-grep inference over an editor buffer.

## 1. The equivalence claim, and whether it holds

**OBSERVATION — source law.** `getPatchVerDiffFile` (`GoApiSnapshot.java:148-166`) starts at the requested
`GoVer` and moves `prevPatch()` while `patch > 0` and the constructed name is absent:

- `:153-155` loop; `:154` calls `getApiSnapshotFile(patchVer, "patchverdiffs/", ".diff")`.
- `GoVer.prevPatch` (`GoVer.java:134-136`) is `new GoVer(major, minor, patch > 0 ? patch-1 : 0)`: minor never moves.
- `GoVer.toString` (`GoVer.java:155-160`) is `"%d.%d.%d"` for any patch != -1, i.e. canonical ASCII decimal.
- `getApiSnapshotFile` (`:168-178`) builds `typeinfo/golang/%sgo%s.json%s`; absence surfaces as
  `FileNotFoundException` and is caught to `null` (`:175-177`).
- Presence is `File.exists()` (`GModule.findModuleFile`, `GModule.java:147-155`) **and not a directory**
  (`Application.getDataFileInModule`, `Application.java:369-372`); a directory therefore behaves exactly
  like absence and the walk continues downward.

So the walk's result is: `max { q in [1, p] : goM.m.q.json.diff exists, is not a directory }`, else null.

**OBSERVATION — implementation.** `selection.py:215-245` enumerates `patchverdiffs/` once, matches the canonical
name with `_DIFF_NAME_RE` (`:55-57`, same `GoVer.toString` shape), keeps `0 < cand <= patch` (`:238`),
sorts descending numerically (`:240`), and takes the first entry `_describe_file` can describe (`:241-245`).
`_describe_file` (`:124-144`) returns `None` for a non-regular path and raises `UnreadableError` if a regular
file cannot be read.

**Verdict.** For the modeled case — one root, canonical names, candidates that are regular readable files —
this is **equivalent** to the source walk, including the two non-obvious cases:

- a **directory** named `goM.m.p.json.diff` is skipped by `is_file()` and the loop continues to the next lower
  patch, matching Java's directory→`FileNotFoundException`→`null` continuation;
- **patch 0**: `:224` skips the listing and `:238` excludes 0, matching the `patch > 0` guard at `:153`.

I found **no defect in the numeric comparison itself**: `sorted(..., reverse=True)` over Python ints is a true
numeric max; leading-zero and non-canonical names are excluded by the fullmatch; other-minor names are filtered
numerically at `:236`; higher-than-request patches are excluded at `:238`. Confidence: high (source read, not executed).

## 2. Where the word "equivalent" is too broad — bounded boundary note (low)

The code comment `selection.py:215-221` and the knowledge row ("greatest present positive patch not above the
request") present the listing as an equivalent replacement without qualifying the presence predicate. Three
adversarial-only conditions sit outside that equivalence — one changes the selected entry, two change only the
failure surface. None occur in the installed data (all bases/diffs are regular files) and none are reachable
through `selfcheck._materialize`, which writes regular files only.

1. **Special files.** A FIFO/socket/device named `goM.m.p.json.diff` is `exists() && !isDirectory()`, so Java
   selects it (`Application.java:369-372`); `Path.is_file()` is false, so the preview silently skips it and may
   select a *lower* patch (`selection.py:130`, `:241-245`). Selection actually differs here, unlike the directory case.
2. **Unreadable regular candidate.** Java's selector is name-only and returns the file; the preview must read it to
   emit `size`/`sha256`, so `_describe_file` raises (`:138-139`) and the CLI exits 2. This is a refusal rather than a
   wrong selection and is covered by the documented exit-2 contract ("a required read/parse could not be evaluated").
3. **Unlistable `patchverdiffs/`.** Java probes child names and `exists()` is false under EACCES, yielding base-only;
   the preview raises `UnreadableError` (`:230-232`) and exits 2. Again a refusal, defensible, but not what Java returns.

**Rejected attack hypothesis (calibration):** an over-long canonical component (e.g. a 5000-digit patch) would make
`int()` raise `ValueError` outside the CLI's exception tuple. This is **unreachable** in the modeled plain-directory
tree: Linux `NAME_MAX` is 255 on the tested paths, and Python's minimum configurable int-string limit is 640, so a
255-byte filename can never trip the conversion guard. No code change is warranted; do not add a check for it.

**Unverified, low-probability:** `"%d.%d.%d".formatted` uses the JVM default locale; if a non-ASCII-locale Formatter
localized `%d` digits, Java's probed names would not be canonical ASCII. Standard JDK behavior localizes digits only
with the grouping flag, so this should not fire, but no JDK Formatter source ships in this tree to confirm it.
[INFERENCE] It does not affect installed-data selection under an ASCII default locale; not a round-16 defect.

## 3. Concrete artifact defect — the produced fixtures cannot detect the law they claim (medium)

The suite has **no case where numeric and lexicographic same-minor ordering disagree**, so the flagship
"nearest lower, not lexicographic" property is inspection-only.

- `selection-fixtures.json:51-75` (`lower_fallback`, request 1.21.5, diffs 2 and 4): picks 4 under both orders.
- Every other selecting case has at most one in-range candidate or only single-digit exact matches
  (`exact_diff` 3, `patch0` 0, `future_diff_ignored` 3/9 above request, `windows_omission` 2,
  `negative-fixtures.json` `corrupt-diff-still-selected` 2).
- `minor_isolation` (`:147-173`) catches only a *cross-minor* lexicographic max; a same-minor string sort passes it.
- Net: a regression from numeric `max` to string `max` inside the same minor leaves **all 9 positive and 17 negative
  cases green**. The documented real-data recheck (knowledge entry `recheck:` line) uses `1.24.7`, whose candidates
  are 1..6 — also non-discriminating.
- The wave-1 review already derived the discriminators and asked for them: `w1/ReviewLowerDiff.md:33-53`
  (`1.24.10 -> 6`, `1.19.20 -> 13`, `1.19.10 -> 10`, with the string-order counterexamples). They are absent from
  the produced fixture file.

Handwritten cases to close the gap (expected values are source-derived, subset-of-result; no sizes or hashes are
asserted, consistent with `selfcheck._compare` and `PATH_KEYS`):

```json
{
  "id": "numeric_not_lexicographic_fallback",
  "request": "1.21.15",
  "goos": "linux",
  "goarch": "amd64",
  "files": {
    "go1.21.0.json": {"all": {}},
    "patchverdiffs/go1.21.9.json.diff": {},
    "patchverdiffs/go1.21.10.json.diff": {}
  },
  "expected": {
    "status": "fallback_diff",
    "base": {"path": "go1.21.0.json"},
    "selected_diff": {"path": "patchverdiffs/go1.21.10.json.diff"},
    "selected_patch": 10,
    "base_matching_buckets": ["all"],
    "patch_applied": false,
    "evidence_class": "source_model"
  }
}
```

Source derivation: probes 15..11 are absent, 10 is present, 9 is never reached (`GoApiSnapshot.java:153-155`);
status is fallback because 10 != 15. A string-descending implementation picks 9.

```json
{
  "id": "exact_two_digit_patch",
  "request": "1.21.10",
  "goos": "linux",
  "goarch": "amd64",
  "files": {
    "go1.21.0.json": {"all": {}},
    "patchverdiffs/go1.21.9.json.diff": {},
    "patchverdiffs/go1.21.10.json.diff": {}
  },
  "expected": {
    "status": "exact_diff",
    "base": {"path": "go1.21.0.json"},
    "selected_diff": {"path": "patchverdiffs/go1.21.10.json.diff"},
    "selected_patch": 10,
    "base_matching_buckets": ["all"],
    "patch_applied": false,
    "evidence_class": "source_model"
  }
}
```

This also pins the status discriminator (`diff_patch == patch`) at a multi-digit patch.

```json
{
  "id": "noncanonical_diff_name_ignored",
  "request": "1.21.3",
  "goos": "linux",
  "goarch": "amd64",
  "files": {
    "go1.21.0.json": {"all": {}},
    "patchverdiffs/go1.21.03.json.diff": {}
  },
  "expected": {
    "status": "base_only",
    "base": {"path": "go1.21.0.json"},
    "selected_diff": null,
    "selected_patch": 0,
    "base_matching_buckets": ["all"],
    "patch_applied": false,
    "evidence_class": "source_model"
  }
}
```

Source derivation: `toString()` can never emit `03`, so Java probes `go1.21.3.json.diff`, then 2 and 1, and returns
null (`:153-155`, `GoVer.java:155-160`). This pins the **canonical-filename** half of the claim: an implementation
that scans any `go<digits>.<digits>.<digits>` name and normalizes ints would select patch 3 and pass today's suite.

## 4. Limits

- No real Ghidra/JVM execution, so the equivalence is a source model; class-vs-source consistency and multi-root
  module resolution (`Application.findModuleFile`, search-root priority) are unmodeled, as the knowledge entry
  already states.
- The equivalence is **result-level, not operational**. A request such as `1.21.2147483647` is admitted by the
  preview's int bound and yields `base_only` immediately when no diff exists; the Java walk performs ~2^31
  filesystem probes before returning the same null. No selected file differs, but the two are not interchangeable
  as probes under a time bound. Not a defect; the docs already disclaim a countdown probe.
- The three boundary conditions in §2 are not representable by the current fixture runner and are not defects on the
  installed data; §3 is the only finding I recommend acting on.
- Severity framing: §1 no-finding (high confidence), §2 low/adversarial/partly documented, §3 medium evidence gap,
  §4 unverified. No pass, score, admission, or target-capability claim is made.
