# Scout — GoRttiMapper: the four Go log lines, their emitting branches, and whether "Untested" halts

Seat: KaidokuR17.ScoutGoRttiMapper-3 (advisory, read-only). Axes: calibration, depth.

Sources:
- `SRC` = `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`;
  members cited as `Base-src.zip:<member>:<line>` (archive extracted read-only to /tmp/gormall).
- `DATA` = `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang`.
- `pilot/shfmt-log/ghidra.log`, `pilot/esbuild-0.25.12-log/ghidra.log` (paths relative to `.ufo/waves/round-17/`).

Labels: **OBSERVED** = read in a file/artifact; **INFERENCE** = derived from source, not executed.
No REA analysis, no Ghidra launch, no carrier execution. Only file written: this report. No installs.

## 0. One-line answer

`Untested Go version` is a **log-only range check** (`Msg.error`, no throw/return); it never stops
processing. What stops shfmt is the *next and independent* gate: an EMPTY Go API snapshot makes
`initStructMappings` fail on its first structure lookup → `BootstrapInfoException("Missing Go
bootstrap type info…")` → `getSharedGoBinary` warns and returns null → each Go analyzer logs its own
error and returns false.

## 1. Exact anchors and emitting branch

| Log line (pilot) | Level | Source anchor | Enclosing unit | Branch that emits it |
|---|---|---|---|---|
| `Reading Go binary info: <name>` | INFO | `Base-src.zip:ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:106` | `getSharedGoBinary` :102-129, supplier lambda :104-125 | Unconditional first statement of the supplier, on every per-analysis-session cache miss (before `getGoBinary`) |
| `Untested Go version [x]` | ERROR | `GoRttiMapper.java:170-172` (literal :171) | `getGoBinary` :151-188 | `!SUPPORTED_VERSIONS.contains(goVer)`, range defined :79 as `parse("1.15-1.25")`; `Msg.error` only |
| `Using Go API snapshot for version X` | INFO | `GoRttiMapper.java:179-180` | `getGoBinary` :174-185 | After `GoApiSnapshot.get(...)` returns and `!apiSnapshot.getVer().isInvalid()` (:178) |
| `Missing Go bootstrap type info…` | WARN | thrown :358-360; branch :351-361 | `initStructMappings`, called from the ctor at :348 | `registerStructures` threw `IOException` **and** `apiSnapshot.isInvalid()` (:356) |

Adjacent line in the esbuild block: `Using Go API snapshot for %s` — INFO,
`Base-src.zip:ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:163`, emitted by
`getPatchVerDiffFile` :148-165 only when a base json exists and either an exact patch diff or patch 0
is selected.

Sibling branches (so the four are not confused with near-misses):

- invalid/unparseable version string → `BootstrapInfoException("Invalid Go version string…")`
  :166-169 (same WARN catcher as the missing-bootstrap line).
- struct failure with a **valid** snapshot → `IOException("Invalid Go bootstrap struct mapping
  info…")` :363-365, caught at :118-123 and logged as ERROR `Failed to read Go info` (with stack).
- no build info at all → `null` at :160-163, no message, no analyzers.

## 2. Does "Untested" stop processing? **No.**

Code proof: :170-172 is a bare `if` whose only body is `Msg.error(...)` — no throw, no `return`, no
flag. Control falls through to the snapshot lookup (:174-185) and the constructor (:187). The only
hard failures in `getGoBinary` are the invalid-version throw (:166-169), a cancelled snapshot fetch
(:183-185), and whatever the constructor throws (:187 → `GoRttiMapper` :329-349).

The range constant is used nowhere else: `SUPPORTED_VERSIONS` appears only at :79 (definition), :170
(this check) and :269-272 (public `getAllSupportedVersions()`, itself unused). A scan of every
`*-src.zip` under `Ghidra/{Framework,Features}` finds no other Go consumer; the `FileFormats`
`SUPPORTED_VERSIONS` hits are Android ART/OAT/VDEX constants, unrelated. So the range is advisory
provenance, not a gate.

Observed proof: shfmt `ghidra.log:82-84` continues past `Untested` into snapshot lookup and the
constructor; the RTTI stop is the bootstrap WARN at :84. Auto-analysis otherwise continues
(`AutoAnalysisManager` timing table starts at `shfmt:90`; log ends normally).

Boundary semantics (matters for a log classifier): `parse("1.15-1.25")` yields wildcard-patch
bounds (`GoVerRange.java:42-57`), and `GoVer.compareTo` treats `patch == -1` as equal
(`GoVer.java:143-152`); hence any `1.25.x` is in range, while `1.26.0`/`1.27.0` are out. The
`[1.27.0]` in `shfmt:83` is out on the minor number.

INFERENCE: if a matching snapshot were shipped for an out-of-range version, `Untested` would still
print and the run could proceed — the range check neither consults nor gates snapshot data. The real
question is file existence (see §5).

## 3. shfmt (Go 1.27.0) — why the block looks like this

Log: 82 `Reading` → 83 `Untested` → 84 `Missing bootstrap` → 85 symbol-analyzer error; the same
triple repeats 86-89 → string-analyzer error.

1. `Reading` at :106, once per caller. The result is cached per analysis session through
   `TransientProgramProperties` (`GoRttiMapper.java:103-105`), but **null is not stored**
   (`TransientProgramProperties.java:106-112`: supplier returns null → `return null` before
   `addProperty`). Hence two full attempts 10 s apart, one per analyzer
   (`GolangSymbolAnalyzer.java:133-137`, `GolangStringAnalyzer.java:103-107`). A third potential
   caller, `GolangDWARFFunctionFixup.java:283-289`, did not fire: DWARF analysis was skipped
   (`shfmt:81`), and neither log contains a DWARF fix-up line.
2. `Untested` at :171 with `goVer = GoBuildInfo.getGoVer()` (`GoBuildInfo.java:237-239`), outside
   the range. Non-fatal.
3. Snapshot lookup: base version `goVer.withPatch(0)` = 1.27.0; `getApiSnapshotJsonFile`
   (`GoApiSnapshot.java:118-146`, file probe :168-176) looks for `typeinfo/golang/go1.27.0.json`.
   `DATA` ships only `go1.15.0.json` … `go1.25.0.json` (11 files) → null → `GoApiSnapshot.get`
   returns `EMPTY` (:102-115; `EMPTY = (GoVer.INVALID, Map.of())` :242). Consequence: **no
   `GoApiSnapshot` line at all**, and mapper :178 suppresses its own snapshot line because the
   version sentinel is invalid. Absence of *both* snapshot lines is the signature of a missing base
   json; a missing patch diff would instead warn at :158-160.
4. Constructor :329-349 → `new GoTypeManager` (:346; ctor :81-87) → `initStructMappings` (:348).
   `registerStructures` walks `GOLANG_STRUCTMAPPED_CLASSES` in list order (:295-300); the first entry
   is `GoModuledata` (`@StructureMapping("runtime.moduledata")`, `GoModuledata.java:37`; the class is
   only `StructureMarkup`, `:38`, not `StructureReader`). `DataTypeMapper.registerStructure`
   (:172-198) resolves the name through `GoRttiMapper.getType` (:380-396) →
   `GoTypeManager.findTypeRec` (:402-455). `"runtime.moduledata"` is not a primitive, is absent from
   `typeNameIndex` (seeded empty; written only by conversion/caching at :237, :397, :574) and
   `apiSnapshot.getTypeDef` returns null (:449); result null → `registerStructure` throws
   `IOException("Missing struct definition…")` (:180-181). Caught at :355; `apiSnapshot.isInvalid()`
   is true → `BootstrapInfoException` with literal :358-360.
5. `getSharedGoBinary` catch :114-117: `Msg.warn` (:115) + `logAnalyzerMsg` (:116); supplier returns
   null (:125); each analyzer logs its ERROR and returns false (`:135` / `:105`).

Three calibrating details:

- The fine-grained cause never reaches the log: the `registerStructure` `IOException` is discarded
  by :355-361, which branches only on `apiSnapshot.isInvalid()`. So log:84 identifies the *gate*, not
  the missing structure.
- The WARN carries **no version**: the literal at :359-360 has no format specifier, so
  `.formatted(goVer)` is a no-op (OBSERVED: log:84 contains no version, unlike log:83).
- Why not `GoName` failing first: `GoName` implements `StructureReader` (`GoName.java:42`) and
  `DataTypeMapper.java:179` exempts `StructureReader` classes with a single name from the
  missing-struct throw. Indeed `"GoName"` is not present in `go1.23.0.json` (`"runtime.name"` is), so
  successful 1.23 registration does not prove every annotated name exists.

## 4. esbuild (Go 1.23.12) — the same anchors, success path

`62 Reading` (:106) → `63 GoApiSnapshot: Using Go API snapshot for 1.23.12`
(`GoApiSnapshot.java:163`: base `go1.23.0.json` exists and `patchverdiffs/go1.23.12.json.diff`
exists, so the exact-diff INFO branch of :148-165) → `64 GoRttiMapper: Using Go API snapshot for
version 1.23.12` (:179-180; `read` sets `ver` to the *requested* version, `GoApiSnapshot.java:205`
and :239) → `65/66` `GoTypeManager` :208 (`Discovered … unindexed`, called from `init` :142) then
:144 (`Found … Go types`) → `67` `GolangSymbolAnalyzer:139` (`Go version 1.23.12`).

Registration succeeds because `go1.23.0.json` contains `"runtime.moduledata"` (OBSERVED) and the
`"linux-amd64"` arch key (OBSERVED top-level keys), so `getTypeDef` returns a `GoStructDef` that
`convertApiTypeDef`/`convertStructDef` turn into a `StructureDataType` (`GoTypeManager.java:449`,
:468-475, :559). No `Untested` (in range), no fallback WARN (exact patch diff).

## 5. Log-signature discrimination (the useful calibration)

| Condition | `GoApiSnapshot` line | mapper `Using…` line | Bootstrap outcome |
|---|---|---|---|
| no base json (shfmt 1.27.0) | none | none | Missing bootstrap — OBSERVED |
| base json + exact patch diff (esbuild 1.23.12) | INFO :163 | INFO, version echoed | success — OBSERVED |
| base json, patch 0 (x.y.0) | INFO :163 | INFO, version echoed | success — INFERENCE |
| base json, no diff for requested patch (e.g. 1.25.x; `DATA` has **0** `go1.25` diffs) | WARN `Falling back from A to B…` :158-160 | INFO, version echoed as A | success — INFERENCE |
| base json but no GOOS/GOARCH/`all` entry retained | INFO :163 | INFO, version echoed | Missing bootstrap — INFERENCE |

The last row is a real asymmetry: :178 tests `getVer().isInvalid()` (a version sentinel), while :356
tests `isInvalid()` (the arches map, `GoApiSnapshot.java:503-505`; `read` can return an empty map,
:229-239). So `Using Go API snapshot for version X` is **not** proof that bootstrap data was
retained. Refinement for C2's prediction law: `missing_bootstrap ⟺ GoApiSnapshot.isInvalid()`
(arches empty); "selection == missing_base" is the practical proxy because `archSearchOrder` always
ends with `"all"` (`GoApiSnapshot.java:108-109`) and every shipped json carries an `all` key.
Since this predicate is silent, an extractor must treat *absence of both snapshot lines* as
missing-base, and must not collapse it with the diff-fallback WARN case.

Extraction note for the contract: `Untested Go version` is an ERROR-level line from `GoRttiMapper`
that is **not** fatal; `Missing Go bootstrap type info` is WARN-level and *is* the terminal RTTI
condition. Severity alone must not drive classification.

## 6. Cross-check against C2 / contract predictions

- shfmt: predicted (out-of-range + missing base) matches observation field-for-field —
  `untested_version = "1.27.0"`, `snapshot_label` absent, `missing_bootstrap = true`.
- esbuild: `snapshot_label = "1.23.12"` (both lines agree), `missing_bootstrap = false`.
- Prediction-law refinement and the extractor caveat above.
- Data inventory relevant to future predictions: 11 base json (1.15.0-1.25.0), 123 patch diffs
  (max 1.24.6; 0 for 1.25.x), 9 `.gdt` (1.15-1.23). No Java source in any installed `*-src.zip`, and
  no non-Java resource string, references the `.gdt` names (searched `anybit`); the RTTI bootstrap
  path in source never opens them. Their consumer (if any) is outside this path — **not verified**.
- Falsifiable checks available to L1 (none executed here): (a) a 1.25.x carrier should emit
  `Falling back from 1.25.x to 1.25.0 for Go API snapshot` then `Using Go API snapshot for version
  1.25.x` and succeed; (b) a 1.24.7+ carrier (no diff beyond 1.24.6) should fall back to 1.24.6;
  (c) a carrier whose in-range GOOS/GOARCH has no json entry would show INFO + Missing bootstrap
  together.

## 7. Adjacent lines inside the two assigned ranges (anchors only)

- esbuild 62-75: 63 `GoApiSnapshot.java:163`; 64 `GoRttiMapper.java:179-180`; 65
  `GoTypeManager.java:208`; 66 `:144`; 67 `GolangSymbolAnalyzer.java:139`; 68-70
  `GoTypeManager.java:416-417`; 71 `GolangSymbolAnalyzer.java:327`; 72-73 `:328-331`; 74 `:164`;
  75 `:168`.
- shfmt 82-89: 82 `GoRttiMapper.java:106`; 83 `:171`; 84 `:358-360` via `:115`; 85
  `GolangSymbolAnalyzer.java:135`; 86-88 same as 82-84; 89 `GolangStringAnalyzer.java:105`.

## 8. Gaps / confidence

- No Ghidra/REA execution. The first-failing class (`GoModuledata`) is INFERENCE from list order
  (:295) plus its name being absent from an EMPTY snapshot; the underlying `IOException` text is
  swallowed (:355-361) and cannot be recovered from the log.
- 1.25.x fallback signature is source-derived only; no such carrier exists in the pilot.
- `.gdt` role unverified: search bounds were all `*.java` members of every installed `*-src.zip`,
  decompressed strings of `Base.jar`, and non-Java resource strings under the Ghidra tree.
- Confidence: high on all four anchors and on "Untested is non-fatal" (direct source + observation);
  medium on the exact first-failing structure (inference marked above).
