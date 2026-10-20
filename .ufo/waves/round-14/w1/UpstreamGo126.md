# Round 14 — UpstreamGo126 (S004 GP-6528 commit inspection)

- Lane: `KaidokuR14.UpstreamGo126` (leaf scout; no subagent dispatch; no tests, gates, builds, or REA target runs)
- Axes named: `coverage`, `calibration`
- Access date: 2026-10-20 (UTC)
- Target: Reopen S004 exact GP-6528 commit (`385e8cd923d09f10b1a7874108e71748875fa174`) and inspect changed files and version range. Determine what it supports and what cannot be attributed to installed Ghidra 12.1.4. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
- Status: complete, evidence-backed, bounded.
- Tools: none installed or upgraded. Used pre-existing `curl` 8.12.1, `python3` 3.14.7, `unzip` 6.0, `grep` (GNU grep 3.11), `sha256sum`. No tools needed installing under RULES.md.

---

## 1. Sources opened

| id | source location | access date | exact location / identifier | quote (contiguous, ≤25 words) | notes & limitations |
|---|---|---|---|---|---|
| S004 | https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174 | 2026-10-20 | Git commit `385e8cd923d09f10b1a7874108e71748875fa174`, commit title | “GP-6528 add support for golang 1.26” (6 words) | Upstream commit on GitHub `master`; inspected via GitHub REST API and git patch. Unreleased code, not installed locally. |
| S004 | https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174 | 2026-10-20 | `GoRttiMapper.java` diff, line 79 replacement | `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.26");` (8 words) | Upstream version gate widening on master. |
| S003 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` | 2026-10-20 | Zip SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`; `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:79` | `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` (8 words) | Installed Ghidra 12.1.4 source archive. Confirms local gate excludes Go 1.26. |
| S007 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md` | 2026-10-20 | Installed file, line 1 | “Ghidra 12.1.4 Change History (September 2026)” (6 words) | Installed release documentation. Mentions 0 occurrences of `GP-6528`. |
| GitHub Releases | https://api.github.com/repos/NationalSecurityAgency/ghidra/releases | 2026-10-20 | Tag `Ghidra_12.1.4_build`, published `2026-09-21T17:38:59Z` | Tag `Ghidra_12.1.4_build` | Newest GitHub release is 12.1.4; compare against `385e8cd` shows diverged branch. |

---

## 2. Commit provenance and metadata

- **Commit SHA**: `385e8cd923d09f10b1a7874108e71748875fa174`
- **Parent SHA**: `c3fd55c9c8c482d1f67534fb86bf53ff905486f1`
- **Tree SHA**: `f18cc78bf24feac32586c9a66ce199a3a613f0af`
- **Author**: `dev747368 <48332326+dev747368@users.noreply.github.com>` — `2026-03-03T19:52:38Z`
- **Committer**: `dev747368 <48332326+dev747368@users.noreply.github.com>` — `2026-03-04T00:08:23Z`
- **Commit Message**: `GP-6528 add support for golang 1.26`
- **Stats**: 10 files changed, 78 insertions(+), 33 deletions(-)

---

## 3. Inventory of changed files and structural mechanisms

Inspection of the full patch (`curl -sS https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174.patch`) reveals 10 files modified across type information, RTTI mapping, binary parsing, and tests:

| # | File path | Status | Changes | Structural mechanism & semantics |
|---|---|---|---|---|
| 1 | `Ghidra/Features/Base/certification.manifest` | modified | +1, -0 | Registers `data/typeinfo/golang/go1.26.0.json` in the Ghidra module manifest. |
| 2 | `Ghidra/Features/Base/data/typeinfo/golang/go1.26.0.json` | added | +1, -0 (new file) | Typeinfo bootstrap snapshot for Go 1.26.0. Blob SHA `3f5c4d4c521410f06e24240b409a38d664e4303a`, size **10,556,117 bytes**. Contains serialized function parameter/return types and struct layouts for Go 1.26 stdlib. |
| 3 | `Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/golang/GoBuildId.java` | modified | +15, -1 | Adds `GO_BUIlDID_TRAILING_MAGIC = "\"\n \u00ff".getBytes(...)`. Updates `read(BinaryReader)`, `read(InputStream)`, and structure builder `toStructure` to validate trailing magic after the 83-byte build ID string. |
| 4 | `Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/golang/rtti/GoModuledata.java` | modified | +8, -5 | In `getFirstModuledata(GoRttiMapper context)`: adds fallback checking `context.getGoSection("go.module")` first; if present, reads `GoModuledata` from section start. Only falls back to `runtime.firstmoduledata` symbol if section is absent. |
| 5 | `Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/golang/rtti/GoPcHeader.java` | modified | +2, -2 | In Go 1.26, the `textStart` field was dropped from the runtime `pcHeader`. Changes `@FieldMapping(presentWhen = "1.18+")` to `@FieldMapping(presentWhen = "1.18-1.25")`. Updates `getTextStart()` to return `textStart != 0 ? programContext.getDataAddress(textStart) : null`. |
| 6 | `Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java` | modified | +1, -1 | Widens the version gate: `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")` → `GoVerRange.parse("1.15-1.26")`. |
| 7 | `Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/golang/rtti/types/GoBaseType.java` | modified | +5, -3 | Passes `programContext.getGoVer()` to `GoTypeFlag.parseFlags(...)`, `GoTypeFlag.Uncommon.isSet(...)`, and `GoTypeFlag.ExtraStar.isSet(...)`. |
| 8 | `Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/golang/rtti/types/GoMapType.java` | modified | +20, -5 | Adapts to Go 1.26 internal Swiss table map structure overhaul: restricts old fields (`bucket`, `keysize`, `elemsize`, `bucketsize`) to `@FieldMapping(presentWhen = "-1.25")`. Adds `group` field with `@FieldMapping(presentWhen = "1.26-")` and markup reference `getGroup`. Adds `public GoType getGroup()` and makes `getBucket()` null-safe. |
| 9 | `Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/golang/rtti/types/GoTypeFlag.java` | modified | +24, -12 | Restricts `UnrolledBitmap` flag (bit 4) to `1.22-1.23`. Adds `GCMaskOnDemand` (bit 4, `1.24-`) and `DirectIFace` (bit 5, `1.24-`). Adds version-aware `isSet(int i, GoVer ver)`, `isValid(int b, GoVer ver)`, and `parseFlags(int b, GoVer ver)`. |
| 10 | `Ghidra/Features/Base/src/test/java/ghidra/app/util/bin/format/golang/rtti/GoApiSnapshotGeneratorTest.java` | modified | +1, -4 | Cleans up test helper `createVersionedGoRoot(GoVer ver)` javadoc and formatting. |

---

## 4. What GP-6528 supports

GP-6528 provides complete upstream support for Go 1.26 binaries in Ghidra's Golang analyzer:

1. **Explicit version range**: Widens `GoRttiMapper.SUPPORTED_VERSIONS` to `"1.15-1.26"`.
2. **Bootstrap type information**: Ships `go1.26.0.json` (10.5 MB), enabling `GoApiSnapshot.get(...)` to load standard library types and function definitions for Go 1.26 without triggering `BootstrapInfoException`.
3. **Pclntab pcHeader alignment**: Accommodates the removal of `textStart` from `runtime.pcHeader` in Go 1.26 binaries by bounding `textStart` presence to `"1.18-1.25"`.
4. **Map RTTI schema evolution**: Accommodates Go's switch to Swiss table maps (`internal/runtime/maps`), substituting the older `bucket`/`bucketsize`/`keysize` layout with the new `group` type pointer for Go ≥ 1.26.
5. **Moduledata discovery**: Permits locating moduledata via the `go.module` section header even in stripped binaries where `runtime.firstmoduledata` symbol has been removed.
6. **Type flag accuracy**: Distinguishes Go 1.24+ `GCMaskOnDemand` and `DirectIFace` from older `UnrolledBitmap` flags.

---

## 5. What CANNOT be attributed to installed Ghidra 12.1.4

Evidence establishes four conclusive boundaries separating GP-6528 from the installed host environment (`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`):

### A. The release boundary (GP-6528 is absent from 12.1.4)
- **Installed release**: Ghidra 12.1.4 was built on `2026-09-21T17:38:59Z`.
- **Change history check**: `grep -c "GP-6528" $GHIDRA_INSTALL_DIR/docs/ChangeHistory.md` returns **0**.
- **Git branch topology**: Comparing the official release tag `Ghidra_12.1.4_build` with commit `385e8cd923d09f10b1a7874108e71748875fa174` via the GitHub API returns:
  `status: diverged`, `ahead: 559`, `behind: 1`.
  Similarly, for every other 12.1.x release (`12.1_build`, `12.1.1_build`, `12.1.2_build`, `12.1.3_build`), the release branch diverged and is `behind: 1`.
- **Upstream master topology**: Comparing `385e8cd` against `master` returns `status: ahead`, `ahead: 2056`, `behind: 0`.
- **Conclusion**: GP-6528 landed on `master` on 2026-03-04, but was **never backported** to the 12.1 patch release series. It is not present in Ghidra 12.1.4 or any release through September 2026.

### B. The version gate boundary (`1.15-1.25` vs `1.15-1.26`)
- In installed 12.1.4 (`Base-src.zip`, SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`), `GoRttiMapper.java:79` specifies:
  `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");`
- When an analyzer runs against a Go 1.26 binary, it triggers line 170:
  `if (!SUPPORTED_VERSIONS.contains(goVer))` → logs `"Untested Go version"`.

### C. The missing snapshot boundary (`go1.26.0.json` absent)
- Installed directory `$GHIDRA_INSTALL_DIR/Ghidra/Features/Base/data/typeinfo/golang/` contains exactly 11 JSON files:
  `go1.15.0.json` through `go1.25.0.json`.
- `go1.26.0.json` is **absent**.
- Execution trace in installed 12.1.4 code:
  1. `GoApiSnapshot.get(ver, ...)` searches for `go1.26.0.json`.
  2. Because the file does not exist, it returns `EMPTY`.
  3. `GoRttiMapper.initStructMappings()` catches the empty definition and raises:
     `BootstrapInfoException("Missing Go bootstrap type info, unable to extract Go RTTI info.")`.
  4. `GoRttiMapper.getSharedGoBinary(...)` catches `BootstrapInfoException`, logs it, and returns `null`.
  5. As a result, all Go RTTI extraction, package namespace resolution, and type-based symbol recovery are aborted for the program.

### D. The binary format incompatibility boundary
Even if an analyst were to manually bypass `SUPPORTED_VERSIONS` or inject a snapshot:
- Installed 12.1.4 `GoPcHeader.java:180` expects `textStart` on all `1.18+`. In Go 1.26, Go removed `textStart`, so parsing `runtime.pcHeader` produces an offset misalignment.
- Installed 12.1.4 `GoMapType.java` expects bucket-based map types and has no handling for Go 1.26 Swiss table `group` references.
- Installed 12.1.4 `GoTypeFlag.java` misinterprets Go 1.24+ `GCMaskOnDemand` and `DirectIFace` flags as obsolete `UnrolledBitmap`.
- Installed 12.1.4 `GoModuledata.java` lacks section-based discovery (`go.module`).

---

## 6. Impact on knowledge calibration (r4-10 Go collapse)

In round 4 (`corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:69-74`), the lane observed an `op-2.40.0` (Go 1.26.8) symbol recovery collapse where only 11,595 functions were recovered (11,588 left as `FUN_*`/`thunk_FUN_*`) compared to 33,060 named functions in `op-2.34.1` (Go 1.25.7).

r4-10 hypothesized:
> “Ghidra 12.1.4's Go analyzer cannot parse the Go 1.26 moduledata/pclntab layout (transient Missing Go bootstrap type info, unable to extract Go RTTI info seen in its ghidra.log during the session — dir since deleted, so this is observed-not-cited).”

The reopening of S004 and inspection of GP-6528 calibrates this claim with high fidelity:
- **Observed fact**: The collapse is caused directly by Ghidra 12.1.4's version gate (`1.15-1.25`) and missing `go1.26.0.json` snapshot, which triggers `BootstrapInfoException` and disables RTTI extraction.
- **Observed fact**: Upstream Ghidra developed the fix under GP-6528 (`385e8cd923d09f10b1a7874108e71748875fa174`), adding `go1.26.0.json` (10,556,117 bytes) and adapting `GoPcHeader` and `GoMapType` to Go 1.26 layout changes.
- **Observed fact**: GP-6528 resides only on upstream git `master` and is absent from Ghidra 12.1.4 (built September 2026).
- **Prohibited inference**: One MUST NOT attribute the lack of Go 1.26 symbol recovery in REA runs to target binary obfuscation, stripped pclntab tables, or general Ghidra failure. It is a documented version support boundary of installed 12.1.4.
- **Frontier implication**: Resolving Go ≥ 1.26 symbol recovery in Ghidra requires an operator-owned toolchain upgrade (e.g. to a future Ghidra 12.2 release carrying GP-6528).

---

## 7. Checks for L1 (unrun by this leaf scout)

Under the wave contract, no integration edits, test runs, or builds were executed in this lane. The following checks are designated for L1 integration:
- Verify that candidate knowledge entry `GoEntryDraft.candidate.md` cites `385e8cd923d09f10b1a7874108e71748875fa174` and distinguishes the installed gate (`1.15-1.25`) from upstream master (`1.15-1.26`).
- Verify that `RegistryDeltaDraft.candidate.md` updates S004's `used-by` without replacing prior references.
