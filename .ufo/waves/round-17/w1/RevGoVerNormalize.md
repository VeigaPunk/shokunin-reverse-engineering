# RevGoVerNormalize — Ghidra 12.1.4 Go version normalization (W1, read-only)

Scope: exact path from `.go.buildinfo` version bytes to `Untested Go version [1.27.0]`, and what
Ghidra prints for a version it cannot parse. Sources are installed Ghidra 12.1.4 PUBLIC
(`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`), pilot logs, and one independent byte read of the
carrier. No REA analyze/search/decompile, no Ghidra/analyzeHeadless, no carrier execution, no installs.

Method note: source-derived claims are anchored to `Base-src.zip` members (path:line). Semantics were
cross-checked with a jshell 21.0.12 transcription of `GoVer.parse`/`compareTo`/`toString` and
`GoVerRange.parse`/`contains` (labelled MODEL; it is a copy, not a Ghidra run). The only live Ghidra
evidence is the retained pilot log.

## 1. Observation (pilot, fact)

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/pilot/shfmt-log/ghidra.log`

```
82 INFO  (GoRttiMapper) Reading Go binary info: target-58f765638eed.bin
83 ERROR (GoRttiMapper) Untested Go version [1.27.0]
84 WARN  (GoRttiMapper) Missing Go bootstrap type info, unable to extract Go RTTI info.
85 ERROR (GolangSymbolAnalyzer) Go symbol analyzer error: unable to get GoRttiMapper
86-89 same four lines again, ending with GolangStringAnalyzer
```

Independent byte read of `/usr/bin/shfmt` (sha256 `58f76563…ab459`, matches pilot/README.txt:7):
buildinfo header at file offset 3515584, ptrSize 8, flags 0x2 (inline strings), raw version bytes
`go1.27.0-X:nodwarf5`. The printed `[1.27.0]` is the raw string minus the `go` prefix and the
`-X:nodwarf5` experiment suffix; patch 0 was already present, so no component was invented.

Success-path contrast, `pilot/esbuild-0.25.12-log/ghidra.log:62-67`: `Using Go API snapshot for
1.23.12`, `Using Go API snapshot for version 1.23.12`, `Go version 1.23.12` for raw `go1.23.12`
(pilot/README.txt:8).

## 2. Exact normalization path

1. **Read raw string.** `GoBuildInfo.read` (`ghidra/app/util/bin/format/golang/GoBuildInfo.java:163-186`)
   validates the 14-byte magic, then for inline strings (`flags & 0x2`) `readStringInfo` seeks
   `startOffset + 32`, reads an unsigned LEB128 length and a UTF-8 byte string
   (`GoBuildInfo.java:391-396`). Pointer-form (pre-1.18) reads a Go string at the pointer
   (`:417-431`). Observed shfmt: `go1.27.0-X:nodwarf5` (`pilot/README.txt:7`, byte read above).
2. **Strip the `go` prefix — in GoBuildInfo, not GoVer.** `parseBuildInfo`:
   `if (versionString.startsWith("go")) versionString = versionString.substring(2);`
   (`GoBuildInfo.java:488-490`). Result `1.27.0-X:nodwarf5` is what the object stores and later
   writes into program info as `"Golang go version"` (`GoBuildInfo.java:351-352`,
   property name `GoVer.java:33`). Sharp edge: `GoVer.parse("go1.23.12")` alone is **INVALID**
   (regex kills from `g`), verified in MODEL.
3. **Parse to GoVer.** `GoBuildInfo.getGoVer()` re-parses on every call (`GoBuildInfo.java:237-239`).
   `GoVer.parse(s)` → `parse(s, 0)` (`GoVer.java:46-48`); body `GoVer.java:62-81`:
   `s.replaceAll("[^.0-9].*$", "")` keeps the leading `[0-9.]` run and truncates at the first other
   character (`:64-65`) → `1.27.0`; `.split("\\.")` → `[1,27,0]`; fewer than 2 parts → `INVALID`
   (`:66-68`); ints parsed, patch defaults to `missingPatchValue` when absent (`:69-75`).
   Result `GoVer(1,27,0)`.
4. **Range test.** `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")`
   (`ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:79`). `GoVerRange.parse` splits on
   `[+-]` and parses each bound with `parseWildcardPatch` (missing patch = -1)
   (`GoVerRange.java:42-57`, `GoVer.java:58-60`, `:72-74`), so the range is (1,15,-1)..(1,25,-1).
   `contains` is `start <= ver <= end` using `GoVer.compareTo` (`GoVerRange.java:83-87`), where a
   patch of -1 compares equal at equal major.minor (`GoVer.java:143-152`). Inside → no message;
   outside → next step.
5. **Print.** `Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer))`
   (`GoRttiMapper.java:170-172`); the brackets are literal in that format string. `%s` is
   `GoVer.toString()`: `patch != -1 ? "%d.%d.%d" : "%d.%d"` (`GoVer.java:154-159`).
   Net: `go1.27.0-X:nodwarf5` → strip `go` → truncate at `-` → `1.27.0` → `[1.27.0]`, exactly
   log line 83. Note the message prints the *normalized* value, never the raw build-info string.

Verified table (MODEL, exact transcribed code):

| input (post-`go`-strip)   | parse result | toString  | in 1.15-1.25 |
|---------------------------|--------------|-----------|--------------|
| `go1.27.0-X:nodwarf5`     | (1,27,0)     | `1.27.0`  | no           |
| `1.23.12`                 | (1,23,12)    | `1.23.12` | yes          |
| `1.25`                    | (1,25,0)     | `1.25.0`  | yes          |
| `1.25.9`                  | (1,25,9)     | `1.25.9`  | yes          |
| `1.26.0`, `1.27.0`, `2.0` | valid        | as-is     | no           |
| `1.14.9`                  | (1,14,9)     | `1.14.9`  | no           |

## 3. Unparseable version — what is printed

If the version string exists but `GoVer.parse` fails (`isInvalid()` = major==0 && minor==0,
`GoVer.java:105-107`), and no fallback option rescued it (`GoRttiMapper.java:154-159`):

```java
throw new BootstrapInfoException(
    "Invalid Go version string [%s]".formatted(buildInfo.getVersion()));   // GoRttiMapper.java:166-169
```

That exception is caught in `getSharedGoBinary` and logged at **WARN**:
`Msg.warn(GoRttiMapper.class, mbie.getMessage())` (`GoRttiMapper.java:114-116`), plus an analysis
MessageLog append when analysis is running (`:131-138`). Expected line:

```
WARN  (GoRttiMapper) Invalid Go version string [<version-after-go-strip>]
```

Key details:

- The bracket holds `buildInfo.getVersion()` — the **post-strip raw string**, not `GoVer.toString()`
  and not the build-info `go` prefix. So raw `go1` → `Invalid Go version string [1]`; raw `go` (empty)
  → `Invalid Go version string []`; raw `devel go1.27-abc` → `Invalid Go version string [devel go1.27-abc]`
  (the regex strips from `d`, giving `""`, which has <2 parts — MODEL). `0.0.0` can never be printed:
  the throw precedes every `toString` use.
- It is **not** `Untested`: `Untested` is only reached after a successful parse and range test
  (`GoRttiMapper.java:165-172`).
- Downstream, both Go analyzers then print their own error because the mapper is null:
  `ERROR (GolangSymbolAnalyzer) Go symbol analyzer error: unable to get GoRttiMapper`
  (`GolangSymbolAnalyzer.java:133-137`) and the same for `GolangStringAnalyzer.java:103-107`.
- If `.go.buildinfo` is entirely absent, `buildInfo == null` returns null without any version message
  (`GoRttiMapper.java:160-163`): only `Reading Go binary info` + the two analyzer errors. The
  `Invalid …` wording is reserved for present-but-unparseable data.
- Rescue path: analyzer option `Go version fallback` (`GoBuildInfo.java:48`,
  `GolangSymbolAnalyzer.java:129-131`) is consulted before the throw (`GoRttiMapper.java:154-159`;
  `GoBuildInfo.java:192-200`). Caveat: the fallback string is parsed by `GoVer.parse` **without** the
  `go` strip, so a user-supplied `go1.25` is rejected; `1.25` is required.
- The pilot never exercised the invalid path; the sequence above is read off source (INFERENCE),
  while all string literals and levels are exact from source.

## 4. Why `[1.27.0]` is followed by "Missing Go bootstrap type info"

- Base snapshot file is keyed only on major.minor with patch 0:
  `baseVer = goVer.withPatch(0)` (`GoVer.java:138-140`) and
  `typeinfo/golang/go%s.json` (`GoApiSnapshot.java:122-126, 168-172`). Installed data has
  `go1.15.0.json … go1.25.0.json` only — no `go1.26.0.json`/`go1.27.0.json` (directory listing).
- Base miss returns null and `GoApiSnapshot.get` yields `EMPTY` (`GoApiSnapshot.java:102-116`,
  `:242`), whose `getVer()` is `GoVer.INVALID`; the `Using Go API snapshot for version %s` INFO is
  gated on `!apiSnapshot.getVer().isInvalid()` (`GoRttiMapper.java:178-181`), so no snapshot line.
- The constructor then fails struct mapping and, because `apiSnapshot.isInvalid()` is
  `arches.isEmpty()` (`GoApiSnapshot.java:503-505`), throws `Missing Go bootstrap type info, unable
  to extract Go RTTI info.` (`GoRttiMapper.java:351-367`, literal at :359), logged as the observed
  WARN at `GoRttiMapper.java:114-116`. Matches shfmt log 82-85 byte-for-byte.
- Both analyzers re-enter the supplier (symbol at `FORMAT_ANALYSIS.after().after`,
  `GolangSymbolAnalyzer.java:74-79, 98-102`; string at `STRINGS_PRIORITY`), and a null result is not
  cached, hence the duplicated four-line block at log 86-89 (duplication observed; non-caching is
  INFERENCE from `TransientProgramProperties` returning null).

## 5. Snapshot-message calibration (matters for the C2 prediction table)

`GoApiSnapshot.getApiSnapshotJsonFile` (`:118-146`) and `getPatchVerDiffFile` (`:148-166`):

- Patch diff exists for the exact version → `INFO (GoApiSnapshot) Using Go API snapshot for X`
  (`:162-163`) and the base json is patched; observed for 1.23.12 (log 63), and
  `patchverdiffs/go1.23.12.json.diff` exists.
- No exact diff → `prevPatch()` walk (`GoVer.java:134-136`) down to patch 1; a found lower diff
  produces `WARN Falling back from X to Y for Go API snapshot` (`:158-161`). If none exists,
  `patchVer` reaches `.0`, `patchDiffFile` is null, and the WARN still names `X → Y` but the caller
  uses the unpatched base json (`:129-131`). Patch 0 skips the loop and logs the INFO (`:162-164`).
- Installed diffs: 1.20×14, 1.21×13, 1.22×12, 1.23×12, 1.24×6, **none for 1.25**. So a `go1.25.3`
  carrier predicts `WARN Falling back from 1.25.3 to 1.25.0`, while `go1.25.0` predicts the INFO —
  a cheap discriminator the pilot has not exercised.
- `read(...)` stores the **requested** GoVer in the snapshot object (`GoApiSnapshot.java:205, 239`),
  so `GoRttiMapper.java:179-180` always prints the requested normalized version even when the data
  came from a lower-patch base; it is not the file's version.
- Mismatch worth knowing: `:178` gates on `getVer().isInvalid()` while the constructor gates on
  `arches.isEmpty()`. A present json with no matching arch key (search order
  `goos-goarch, goos, unix, goarch, all`, `:108-109`) would log the snapshot INFO and then the
  Missing-bootstrap WARN. Not observed; source-only INFERENCE.

Boundary results (MODEL): 1.15.0 and 1.25.9 inside; 1.14.9, 1.26.0, 1.27.0, 2.0 outside. 1.26/1.27
also lack base json, so `Untested` is always followed by Missing bootstrap for them.

## 6. Calibration notes for the round

- The contract text (`W/contract.md`, predict.py section) says "`GoVer.parse`/`fromVersionString`".
  No `fromVersionString` exists in Ghidra 12.1.4 Base sources — a full scan of every `*.java` member
  of `Base-src.zip` for that literal returns nothing. Real entry points: `GoVer.parse(String)`,
  `GoVer.parseWildcardPatch(String)`, `GoVer.fromProgramProperties(Program)`, and
  `GoBuildInfo.getGoVer()`. Downstream wording should name those.
- `GoVer.parse` alone cannot consume a `go`-prefixed string; the strip is uniquely at
  `GoBuildInfo.java:488-490`. A predictor that strips in the wrong place (or not at all) will
  misclassify every real carrier as INVALID.
- Java `String.split("\\.")` drops only *trailing* empty strings: `1.2.` → `1.2.0`, `1.2.3.4` →
  `1.2.3` (extra component silently ignored), `.2.3`/`1..3` → INVALID, leading space → INVALID
  (MODEL). Don't emulate with Python's default `split`.
- Program info property `Golang go version` (`GoVer.java:33`) stores the post-strip original
  (`1.27.0-X:nodwarf5`), so re-reading it through `GoVer.fromProgramProperties` (`GoVer.java:89-93`)
  re-normalizes identically.
- Log line format observed in the retained logs: `YYYY-MM-DD HH:MM:SS LEVEL␠␠(Component) message␠␠`
  (`pilot/shfmt-log/ghidra.log:82-89`); levels are `INFO`, `WARN`, `ERROR` as emitted by `Msg`.

## 7. Search bounds / no-finding

- Scanned all `*.java` in `Base-src.zip` for the literals `Untested Go version`,
  `Invalid Go version string`, `Using Go API snapshot`, `Missing Go bootstrap type info`,
  `Golang go version`, `fromVersionString`. Hits are only the anchors cited above (plus
  `GoRttiMapper.java:359` for the last). No other place prints a GoVer.
- The `.gdt` files beside the json snapshots (`golang_1.15…1.23_anybit_any.gdt`) are generic
  data-type archives used by `ApplyDataArchiveAnalyzer` (`Ghidra/Features/Base/lib/Base-src.zip`:
  `ghidra/app/plugin/core/analysis/ApplyDataArchiveAnalyzer.java:288`), not part of this path; their
  absence for 1.24/1.25 is out of scope, not a second finding.
- `GolangAnalyzerOptions` source is not in `Base-src.zip`; the only option anchor used is the
  literal constant `GoBuildInfo.java:48` and its consumer `GolangSymbolAnalyzer.java:129-131`.

## 8. Confidence

- Observation (direct): raw build-info bytes and sha256; pilot log lines and their exact wording;
  installed snapshot/diff inventory; Ghidra source line anchors.
- Source-model (replicated, not run inside Ghidra): every parse/range/toString row in the tables.
- Inference (no carrier run, out of contract): the exact four-line unparseable sequence, the
  fallback-WARN predictions for 1.25.x, and the non-caching of a null mapper.
