# W1 scout — Ghidra 12.1.4 `GoVer` parse/format (round 17)

Seat: `KaidokuR17.ScoutGoVer-3` (leaf, author-side advisory). Read-only: no edit outside this
report; no REA `analyze`/`search`/`decompile`; no Ghidra; no carrier executed.
Question: exactly how `go1.27.0-X:nodwarf5`, `go1.23.12`, `go1.20.12` and `""` are parsed and
formatted (pilot log shows `Untested Go version [1.27.0]`), and which inputs parse invalid/unknown.

## Verdict

Parsing is **two-stage**: `GoBuildInfo.parseBuildInfo` strips one leading `go`
(`Base-src.zip!ghidra/app/util/bin/format/golang/GoBuildInfo.java:488-490`), then
`GoVer.parse(String)` truncates at the first character that is neither `.` nor an ASCII digit
(`Base-src.zip!ghidra/app/util/bin/format/golang/GoVer.java:65`) and reads `major.minor[.patch]`
(default patch 0). So `go1.27.0-X:nodwarf5` → `1.27.0-X:nodwarf5` → **`1.27.0` (GoVer(1,27,0))**,
`go1.23.12` → **1.23.12**, `go1.20.12` → **1.20.12**, `""` → **INVALID (0,0,0)**.
`toString` prints `M.m.p` for any concrete patch (`GoVer.java:154-159`), which is why the log line
reads `[1.27.0]` and the `-X:nodwarf5` suffix is invisible in the log. `1.27.0` is outside
`SUPPORTED_VERSIONS = "1.15-1.25"` (`GoRttiMapper.java:79`) → ERROR `Untested Go version [1.27.0]`
(`GoRttiMapper.java:170-172`), and there is no `go1.27.0.json` snapshot → `GoApiSnapshot.EMPTY`.

## 1. Sources and method

- Source of truth: archive members of
  `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`
  (7,481,132 bytes, 3,865 members, Ghidra 12.1.4). Extracted read-only to `/tmp/base_src`;
  anchors below are written `Base-src.zip!<member>:<line>`.
- Static reads of carriers: `strings`, `readelf -x .go.buildinfo`, and the explicitly allowed
  `npx -y rea-agents@6.5.0 inspect-go-binary <path> --format json`. No execution.
- Semantics probe: `/tmp/gover_probe/ParseProbe.java` (JDK 21.0.12.1, `java ParseProbe.java`)
  contains a verbatim transcription of `GoVer.parse` + the `go`-strip; used only to enumerate
  Java regex/split/parseInt behavior. Source anchors, not the probe, define the model.
- Carrier pins match the pilot README byte-for-byte:
  `/usr/bin/shfmt` = `58f76563…ab459`, esbuild 0.25.12 = `bab29b2c…ced7014`
  (`.ufo/waves/round-17/pilot/README.txt:7-8`).

## 2. Pipeline (source-observed)

```
.go.buildinfo bytes
  → GoBuildInfo.readStringInfo   inline: startOffset+32, unsigned LEB128 len, UTF-8 bytes
                                 (GoBuildInfo.java:391-396; pointer form :418-427)
  → parseBuildInfo               if version startsWith("go") → substring(2)   (:488-490)
  → GoBuildInfo.version          stored post-strip                            (:205, :492)
  → GoBuildInfo.getGoVer()       = GoVer.parse(version)                       (:237-239)
  → GoVer.parse(s)               = parse(s, 0)                                (GoVer.java:46-48)
  → GoVer(major, minor, patch)   record                                       (GoVer.java:31)
```

- The version is read **only** from build info (ELF `.go.buildinfo`, PE `data` scan):
  `GoBuildInfo.java:44-46`, `:92-108`; read path `:163-186`. `runtime.buildVersion` is never used.
- The property written on the program is the **post-strip** string, despite the setter name:
  `setProgramPropertiesWithOriginalVersionString(props, getVersion())`
  (`GoBuildInfo.java:351-352`, `:233-235`). For shfmt the stored `"Golang go version"` property
  (`GoVer.java:33`) is `1.27.0-X:nodwarf5`, not `go1.27.0-X:nodwarf5`.
- Carrier confirms the inline layout byte-for-byte: at `.go.buildinfo` 0x35a4c0,
  `ff20476f…` + `08` (ptr size) + `02` (flags bit 1 = inline) + 16 zero pad + `13` (LEB128 len 19)
  + `go1.27.0-X:nodwarf5`. `readelf -x .go.buildinfo /usr/bin/shfmt`; REA inspect reports
  `header_offset=3515584`, `version_location={offset:3515617,bytes:19}`, `encoding="inline"`.

## 3. Exact parse algorithm (`GoVer.parse`, `GoVer.java:62-81`)

1. `Objects.requireNonNullElse(s, "")` — `null` becomes `""` (`:65`).
2. `.replaceAll("[^.0-9].*$", "")` — keep only the leading run of `.` and ASCII digits; truncate at
   the first other character and drop the rest (`:65`). In a Java character class `.` is literal and
   `^` not in first position is literal, so the class is exactly {dot, `0`…`9`}. The in-source
   comment (`:63`) shows the intended case: `"1.22.8 X:rangefunc"`.
3. `.split("\\.")`; if fewer than 2 parts → `INVALID` (`:66-68`). Java split removes trailing empty
   strings, so trailing dots vanish but an empty middle part survives.
4. `Integer.parseInt` on parts 0 and 1; part 2 → patch if present, else `missingPatchValue`
   (`parse` passes 0, `parseWildcardPatch` passes -1) (`:69-75`).
5. `NumberFormatException`, including int overflow, → `INVALID` (`:77-80`).

Sentinels: `INVALID = (0,0,0)` (`:35`), `ANY = (-1,-1,-1)` (`:36`).
`isInvalid()` is `major == 0 && minor == 0` (`:105-107`) — **not** record equality with `INVALID`, so a
successfully parsed `0.0.5` is also invalid. `isWildcard()` is `major == -1 && minor == -1`
(`:109-111`), which only `ANY` satisfies (`parseWildcardPatch` yields patch=-1 but major/minor ≥ 0).

Version comparison: `compareTo` compares major, then minor, then patch, **except that `:149` treats a
patch of -1 as equal to any patch**. That is how range endpoints `1.15`/`1.25`
(`GoVerRange.java:47,52`) contain `1.15.0` and `1.25.999` (`GoVerRange.java:83-87`).

Range syntax is a different input path: `GoVerRange.parse` splits on `[+-]` (`GoVerRange.java:43`)
and is used only for literal range strings (`GoRttiMapper.java:79`, `GoConstants.java:47,55`,
`GoVerSet.parse` via `GoRttiMapper.java:406`). A binary version string never goes through it, so the
`-` in `go1.27.0-X:nodwarf5` is not a range separator — it is simply the truncation point.

## 4. Formatting

`toString` (`GoVer.java:154-159`): `patch != -1 ? "M.m.p" : "M.m"`.

| Value | `toString()` |
|---|---|
| `GoVer(1,27,0)` (from `go1.27.0-X:nodwarf5`) | `1.27.0` |
| `GoVer(1,23,12)` | `1.23.12` |
| `GoVer(1,20,12)` | `1.20.12` |
| `INVALID` / `(0,0,0)` (from `""`) | `0.0.0` |
| `ANY` / `(-1,-1,-1)` | `-1.-1` |
| wildcard-patch `(1,27,-1)` (ranges only) | `1.27` |

Formatted values are consumers' inputs:

- log: `Msg.error(..., "Untested Go version [%s]".formatted(goVer))` → `[1.27.0]`
  (`GoRttiMapper.java:171`); analyzer info `"Go version %s"` → `Go version 1.23.12`
  (`Base-src.zip!ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java:139`).
- snapshot file name: `"typeinfo/golang/%sgo%s.json%s".formatted(subdir, goVer.toString(), suffix)`
  (`GoApiSnapshot.java:171`); the base lookup uses `goVer.withPatch(0)` (`:122-123`), so the base
  name is always `goM.m.0.json`, and patch diffs live in `patchverdiffs/goM.m.p.json.diff` (`:153-155`).

## 5. The four requested inputs (probe-verified)

| Raw buildinfo string | after `go` strip | `GoVer.parse` | formatted | downstream |
|---|---|---|---|---|
| `go1.27.0-X:nodwarf5` | `1.27.0-X:nodwarf5` | regex stops at `-` → `1.27.0` → `(1,27,0)` | `1.27.0` | not in 1.15–1.25 → ERROR `Untested Go version [1.27.0]` (`GoRttiMapper.java:170-172`); `go1.27.0.json` absent → `EMPTY` (`GoApiSnapshot.java:122-126,242`); pilot: `pilot/shfmt-log/ghidra.log:83` (again `:87`), then `:84` missing-bootstrap |
| `go1.23.12` | `1.23.12` | `(1,23,12)` | `1.23.12` | contained; base `go1.23.0.json` + exact diff → INFO labels `1.23.12` (`GoApiSnapshot.java:162-164`, `GoRttiMapper.java:178-181`); pilot: `pilot/esbuild-0.25.12-log/ghidra.log:63,64,67` |
| `go1.20.12` | `1.20.12` | `(1,20,12)` | `1.20.12` | contained; base `go1.20.0.json` + `patchverdiffs/go1.20.12.json.diff` both present (directory listing) → same two INFO labels; **not observed** (no 1.20.12 carrier in pilot) |
| `""` (`null` likewise) | `""` | 1 part → `INVALID (0,0,0)` | `0.0.0` (only if printed) | no `Untested` line and no snapshot; `getGoBinary` throws `Invalid Go version string []` (`GoRttiMapper.java:165-169`), logged WARN by `getSharedGoBinary` (`:114-117`) |

Probe output (verbatim logic): the four rows above plus controls
`"go1.23.12"` direct-to-`parse` (no strip) → INVALID, `"1.27.0 X:nodwarf5"` → 1.27.0,
`"1.27.0-X"` → 1.27.0, `"1.27.0+nodwarf5"` → 1.27.0.

## 6. Inputs that parse INVALID (fatal unless the fallback applies)

Probe-verified unless marked. `INVALID` ⇒ `BootstrapInfoException` at `GoRttiMapper.java:165-169`
with the **raw post-strip** string in the message (not the formatted record).

| Input | Why |
|---|---|
| `""`, `null` | one empty part (<2) |
| `"go1.27.0"`, `"go"`, `"v1.23.12"`, `"devel go1.27-abc"` | first char is not digit/dot; regex voids the whole string. `GoBuildInfo` strips only one leading `go`, so a raw buildinfo version that already lacks the prefix (or is `devel go…`, which Go uses for development toolchains) is invalid |
| `" 1.23.12"`, `"-1.27.0"`, `"+1.27.0"` | leading non-digit (note: **leading** whitespace is fatal; trailing is harmless) |
| `"1"`, `"1."`, `"."`, `".1"` | fewer than 2 dot-separated parts |
| `"1..2"`, `".1.2"` | empty numeric component → `NumberFormatException` |
| `"1.x.2"` | truncates to `"1."` → one part (contrast `"1.2.x"` → `1.2.0`, valid) |
| `"1.2147483648.0"`, `"1.99999999999.0"` | `Integer.parseInt` overflow (probe confirmed the latter) |
| `"0.0.0"`, `"0.0"`, `"0.0.5"` | parse succeeds but `isInvalid()` is major==0 && minor==0 (`GoVer.java:105-107`) |

Fallback asymmetry (source-observed, important for calibration):

- Two distinct names: the **program property** is `"Go version fallback"`
  (`GoBuildInfo.java:48`, written by `setFallbackVersion` `:188-190`); the **analyzer option label**
  is `"Fallback Go Version"` (`GolangSymbolAnalyzer.java:1311`, registered `:1328`, read `:1345`),
  copied into the property only when non-empty (`:129-131`).
- `fromFallbackInfo` parses that property **without** the `go` strip
  (`GoBuildInfo.java:192-201`, parse at `:195`). A fallback value of `go1.23.12` is therefore
  INVALID and ignored; it must be written `1.23.12`.
- The fallback is consulted only when `buildInfo == null || buildInfo.getGoVer().isInvalid()`
  (`GoRttiMapper.java:153-159`). It therefore **cannot** override a valid-but-untested version:
  for shfmt (1.27.0) the untested path runs unchanged even with a fallback set.
- If build info is entirely absent (no `.go.buildinfo`, no magic in the `.data` scan), `buildInfo`
  stays null and `getGoBinary` returns null before any version message (`GoRttiMapper.java:160-163`);
  only the two analyzer "unable to get GoRttiMapper" errors follow. The `Invalid …` wording is
  reserved for present-but-unparseable data.

## 7. Inputs that parse valid but are "unknown"/untested

`SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")` (`GoRttiMapper.java:79`); `contains` is
`GoVerRange.java:83-87`. `!contains` ⇒ ERROR at `GoRttiMapper.java:170-172`; not fatal at that point.

- `1.27.0` — the observed case (also any `1.27.x`, `1.28.x`, …).
- Any parsed `major > 1` (e.g. `2.0.0`), any `major==1 && minor > 25` (`1.26.0`, `1.100.0`), any
  `major==1 && minor < 15` (`1.14.9`, `1.9.0`), and non-zero-major oddities such as `0.1.0`.
- Contained despite looking odd: `1.25.999` (patch-wildcard comparison, `GoVer.java:149`), `1.15.0`.
- Invalid is caught before this test, so `0.0.5` is "invalid", never "untested".

Second-order unknown (missing snapshot), and the range/data alignment:

- Bundled data (`Ghidra/Features/Base/data/typeinfo/golang`) has base files
  `go1.15.0.json` … `go1.25.0.json` and 123 files under `patchverdiffs/`, including
  `go1.20.12.json.diff` and `go1.23.12.json.diff`; there is **no** `go1.26`/`go1.27` file or diff
  (verified by listing). The declared range and the data range coincide exactly in 12.1.4, so every
  untested version also has no base snapshot.
- With no base file, `getApiSnapshotJsonFile` returns `null` (`GoApiSnapshot.java:122-126`) and
  `get` returns `EMPTY` (`:115-116`, `:242`). The mapper then skips the snapshot INFO log because
  `EMPTY.getVer().isInvalid()` (`GoRttiMapper.java:178`).
- `EMPTY.isInvalid()` is `arches.isEmpty()` (`GoApiSnapshot.java:503-505`). The fatal
  `Missing Go bootstrap type info, unable to extract Go RTTI info.` is thrown only when struct
  mapping also throws while the snapshot is invalid (`GoRttiMapper.java:351-367`, message at
  `:358-360`). So `untested ⇒ missing_bootstrap` is the observed/default outcome here (shfmt
  `ghidra.log:84`) but not a logical entailment: if `registerStructures` succeeded, analysis would
  continue with no snapshot and no missing-bootstrap line. Also note `:360` calls
  `.formatted(goVer)` on a string with no `%s`, so the version is not appended to the message —
  consistent with the observed line.
- An in-range version whose json lacks a matching GOOS/GOARCH key would also read to empty arches
  (`GoApiSnapshot.java:228-239`); not reachable for linux/amd64 because every bundled json has an
  `all` key (checked keys of `go1.15.0`, `go1.23.0`, `go1.25.0`). GOOS/GOARCH come from build
  settings first, else loader/language mapping (`GoBuildInfo.java:272-275,306-309`, map `:65-71`).

## 8. Calibration notes for the round-17 contract and pilot

1. **Normalization must include the `go` strip.** `contract.md:64-65` takes
   `normalized_result.build_info.go_version` (raw, prefixed) and says to normalize "as Ghidra's
   `GoVer.parse`/`fromVersionString` would". No `fromVersionString` exists anywhere in Base-src.zip
   (grep of the full extraction: zero hits); the real functions are `GoVer.parse`
   (`GoVer.java:46,62`) and `GoBuildInfo.getGoVer` (`GoBuildInfo.java:237`). Applying `GoVer.parse`
   to the raw `go1.27.0-X:nodwarf5` yields INVALID, because the leading `g` voids the string;
   predict.py must strip one leading `go` first (then truncate). Expected labels are the
   normalized ones: `1.27.0`, `1.23.12`, `1.20.12`.
2. **Empty input** is not "untested": it is invalid-version (`GoRttiMapper.java:165-169`).
   `contract.md:73` (exit 2) is correct, but if an empty-version carrier is ever observed the expected
   log is WARN `Invalid Go version string []`, with **no** untested and **no** missing-bootstrap line.
3. **Log extraction** on the pilot shfmt log yields `untested_versions=["1.27.0"]` (lines 83, 87 —
   duplicated because the symbol and string analyzers each build a fresh mapper after the first
   failure) and `classification=bootstrap_missing` (line 84). The esbuild log yields
   `snapshot_labels=["1.23.12","1.23.12"]` (lines 63, 64) and `go_version_logged=["1.23.12"]` (line 67).
4. **Pilot retention gap:** `pilot/README.txt:7-8` attributes the raw versions to
   `rea inspect-go-binary`, but the pilot retains only `analyze` JSON (`shfmt.json`, `esb.json`);
   a jq sweep of every `version`-named key in both finds only Ghidra `12.1.4` and schema `1` — no
   `build_info.go_version`. `carrier-run.py` step 2 does retain `inspect-go.json`
   (`contract.md:35`); keep it as the record of the normalized input. I re-ran inspect read-only
   to confirm the field path and values (§9).
5. **Suffix provenance:** shfmt's build settings include `GOEXPERIMENT=nodwarf5` (observed via
   inspect; `GOOS=linux`, `GOARCH=amd64`). `[INFERENCE]` the `-X:` suffix is the toolchain's
   experiment marker carried in the version string; either way Ghidra discards it at the first `-`.
   Consequence: log-only evidence cannot distinguish `go1.27.0` from `go1.27.0-X:nodwarf5`; the
   suffix survives only in the buildinfo bytes and the post-strip `"Golang go version"` property.
6. **`1.20.12` row is prediction-only** here: no 1.20.12 carrier exists in the pilot and none was
   named for this scout. The parse result and both snapshot files are verified, the log labels are not.

## 9. Evidence produced by this scout (read-only)

| Artifact | Detail |
|---|---|
| `npx -y rea-agents@6.5.0 inspect-go-binary /usr/bin/shfmt --format json` | `/tmp/inspect_shfmt.json`, sha256 `a5ddc648011cc7437f22869110935849bde03df5bab3d6c17865c9c7bae57936`; `evidence_id ev_f8ef12a805b6b28bee4beed4cde7440efe567e22133db2a1fb1776d867f4a42a`; `go_version="go1.27.0-X:nodwarf5"`, `encoding="inline"`, `header_offset=3515584`, `version_location={offset:3515617,bytes:19}`, `GOEXPERIMENT=nodwarf5` |
| same for esbuild 0.25.12 | `/tmp/inspect_esb.json`, sha256 `a20a65deb3cf1cc2b9737537220891f366b2ad55275a0a276699a3dfdff85ebf`; `evidence_id ev_0cabcc66620bf9f201e2b0aaba63d9bd1998b4e498ec823c01dc186a73041626`; `go_version="go1.23.12"`, `header_offset=10027008`, `version_location={offset:10027041,bytes:9}` |
| raw buildinfo bytes | `readelf -x .go.buildinfo /usr/bin/shfmt` shows `08 02`, 16-byte pad, `13`, then 19 bytes `go1.27.0-X:nodwarf5` — exactly the layout `GoBuildInfo.java:392-396` reads |
| parse probe | `/tmp/gover_probe/ParseProbe.java`, JDK 21.0.12.1; enumerated the four inputs and the edge cases in §5–§7 |
| source extraction | `/tmp/base_src` (full Base-src.zip extraction) for cross-file grep; zero hits for `fromVersionString` |

Not done: no pacman/uv/cargo/npm install (npx used the already-cached `rea-agents@6.5.0`; no version
change observed, no host tool installed or upgraded); no carrier executed; no Ghidra or REA
analyze/search/decompile.

## 10. Remaining unknowns

- No 1.20.12 carrier was available, so its `1.20.12` snapshot-label observation is source+data
  derived, not measured.
- Whether `registerStructures` succeeds on any given 1.27 binary cannot be tested without running
  analyze; `EMPTY` makes the missing-bootstrap message possible, not certain.
- `GoVer.fromProgramProperties` has zero call sites in Base-src.zip; whether another Ghidra module
  uses it was not searched (only Base-src was examined). It is not on the mapper path.
- The `golang_1.15..1.23` `.gdt` archives in the same data directory are not referenced by Base-src
  Go code (they are user-applied via `ApplyDataArchiveAnalyzer`), so their absence for 1.24/1.25 was
  not treated as a version-path defect.

## 11. Cross-check against sibling W1 reports

Read after writing the above (no edits to their files). `w1/RevGoVerNormalize.md`,
`w1/ScoutGoBuildInfo.md`, `w1/ScoutGoApiSnapshotLog.md` independently report the same model —
`GoBuildInfo` strip at `:488-490`, `GoVer.parse` truncation at `:65`, `SUPPORTED_VERSIONS` at
`GoRttiMapper.java:79`, `Untested` printing the normalized `toString`, and the `missing_base` →
`EMPTY` path. No contradictions found. Two wording points where mine is more explicit and should be
preferred if they collide: (a) `fromFallbackInfo` parses the **property** `"Go version fallback"`
without the `go` strip, while `"Fallback Go Version"` is only the analyzer option label; (b) the
`Untested` line is printed from the normalized record, so the `-X:` suffix is not recoverable from
the log. Their shared caveat also holds: with `.go.buildinfo` absent there is no version message at all.
