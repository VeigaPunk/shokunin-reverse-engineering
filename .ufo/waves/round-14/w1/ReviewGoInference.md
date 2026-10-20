# Round 14 — W1 ReviewGoInference: does Go version gating causally explain the op 2.40.0 symbol loss?

Lane: leaf reviewer, no subagent dispatch. Scope: reopen S003 (installed Ghidra 12.1.4 `Base-src.zip`) and the historical `op` compiler/symbol-count evidence in `corpus/`. No REA calls, no Ghidra runs, no builds, no tests, no target execution. Access date for every source below: 2026-10-20.

## Verdict

1. **Version gating does not causally explain the loss in the installed code.** The `1.15-1.25` range is advisory: an out-of-range version logs `Msg.error` and analysis continues. The gate cannot by itself make the mapper null, so it cannot by itself disable the Go analyzers. `OBSERVATION` (source).
2. **Remaining hypothesis, not established:** the loss sits somewhere in a bundle of version-dependent defects that the installed 12.1.4 parser does not handle for go1.26.x. The upstream fix for the same version range changes seven code files plus adds a snapshot, not just the range string. Which element produced the loss on `op` 2.40.0 is `UNKNOWN`; no retained log, no controlled rebuild, and no replay exists.
3. **Strongest support for the family of causes:** (a) the installed snapshot lookup has no `go1.26` file, (b) the installed moduledata lookup has no section-based route and the 2.40.0 binary has no `firstmoduledata` symbol, (c) upstream GP-6528 changed layout-dependent fields for 1.26. These are source/binary facts; their causal effect on the `op` run is `INFERENCE`.
4. **Strongest support for the observed failure site:** the only retained log line ("Missing Go bootstrap type info…") is thrown from the mapper constructor's struct registration, before any pclntab/moduledata parsing. `OBSERVATION` of the code path; the log itself is `OBSERVED-NOT-RETAINED` (see Gaps).

## Sources opened

| id | location | identity | quote / observation |
|---|---|---|---|
| S003 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` | SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` (matches registry) | Members extracted read-only to `/var/tmp/kaidoku-r14-w1-src/` (see Reproduction) |
| S003a | `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:79` | — | “public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");” |
| S003b | `GoRttiMapper.java:170-172` | — | “if (!SUPPORTED_VERSIONS.contains(goVer) ) {” then “Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer));” — no `throw`, no `return` |
| S003c | `GoRttiMapper.java:174-187` | — | `GoApiSnapshot.get(...)` is called unconditionally after the gate; the mapper is constructed at :187 |
| S003d | `GoRttiMapper.java:351-367` (`initStructMappings`) | — | `catch (IOException e) { if (apiSnapshot.isInvalid()) { // a normal'ish situation where we don't have type info for this arch/binary` → `throw new BootstrapInfoException("Missing Go bootstrap type info, unable to extract Go RTTI info." …` |
| S003e | `GoRttiMapper.java:102-129` (`getSharedGoBinary`) | — | catches `BootstrapInfoException` (warn + analyzer message) and `IOException` (error); both paths `return null` (:125) |
| S003f | `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:102-116`, `:118-146`, `:168-178` | — | `get` returns `GoApiSnapshot.EMPTY` (:115) when no snapshot is found; `getApiSnapshotJsonFile` returns `null` when `typeinfo/golang/go<major.minor.0>.json` is absent (:124-126) |
| S003g | `GoApiSnapshot.java:148-166` (`getPatchVerDiffFile`) | — | Walks patch numbers down to 0 and logs “Falling back from %s to %s for Go API snapshot” (:159-160) |
| S003h | `ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java:105-107, 133-137, 155, 238` | — | `canAnalyze` = golang cspec; `goBinary == null` → `Msg.error(… "unable to get GoRttiMapper"); return false;`; `markupGoFunctions` (:155) → `markupSession.createFunctionIfMissing(funcname, funcns, funcAddr)` (:238) for every pclntab funcdata |
| S003i | `GolangSymbolAnalyzer.java:181-184` | — | `catch (IOException e) { Msg.error(this, "Go analysis failure", e); } return false;` — a mid-markup IOException leaves partial results |
| S003j | `GolangStringAnalyzer.java:103-107` | — | Same null-return behavior for the string analyzer |
| S003k | `ghidra/app/util/bin/format/golang/rtti/GoModuledata.java:415-423` | — | `getFirstModuledata` returns `null` when the `runtime.firstmoduledata` symbol is absent; no section-based lookup |
| S003l | `GoRttiMapper.java:1116-1139` (`findFirstModuledata`) | — | Fallback: pclntab search, then moduledata search; throws `IOException("Invalid Go moduledata…")` if `!result.isValid()` (:1134-1137) |
| S003m | `GoPcHeader.java:180-182` | — | `@FieldMapping(presentWhen = "1.18+")` on `textStart` (open-ended; includes 1.26) |
| S003n | `rtti/types/GoTypeFlag.java:33, 55-63` | — | `UnrolledBitmap(1 << 4, GoVerRange.parse("1.22-"))`; `isValid(b, ver)` returns `b <= maxMask` over flags valid for `ver`; no flag above bit 4 exists in the installed table |
| S003o | `GoRegisterInfoManager.java:73-85`; `Processors/x86/data/languages/x86-64-golang.register.info` | — | Missing register info falls back to a default with a warning; installed register-info versions are `1.17-` and `-1.16` (open-ended, covers 1.26) |
| S003p | `Ghidra/Features/Base/data/typeinfo/golang/` (installed) | — | Snapshot JSON present for `go1.15.0` … `go1.25.0` only (11 files). `patchverdiffs/` covers 1.15–1.24 only (no 1.25.x, no 1.26.x). No `go1.26*` file anywhere under the install (`find`, count 0). `golang_1.15…1.23_anybit_any.gdt` only. Not referenced by `GoRttiMapper` (`super(program, null)`, `GoRttiMapper.java:331`) |
| S003q | `Processors/x86/data/languages/x86.opinion:40-50` | — | ELF e_machine 62 matches both the `gcc` and the `golang` constraint; no version predicate. Which cspec the `op` import actually selected is not recorded |
| UP | upstream commit `385e8cd923d09f10b1a7874108e71748875fa174`, `https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174.patch` | downloaded 2026-10-20 with `curl`; patch SHA-256 `f44945bc879d46f2e16624f7823246416d625229e57930db13a040862c170538`; commit header dated 2026-03-03 (“GP-6528 add support for golang 1.26”) | Ten files changed; see Finding 3 |
| OP | `/var/cache/pacman/pkg/1password-cli-2.40.0-2-x86_64.pkg.tar.zst` | package SHA-256 `fb3e38a7d2eaa7444c2aa0ccd56ae45444c07728c623c984939faf92bcf8d850`; extracted `usr/bin/op` SHA-256 `8d029d2cd7112177132b1b20ef0b6012ba9a9dd9ef48d7f7660f2e8071d4f7b2` (matches corpus prefix `8d029d2c…`), 43,475,106 bytes | Read-only `tar`, `grep -a`, `readelf -S/-s` (no execution) |
| C1 | `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md` | — | Historical op counts (Finding 5) |
| C2 | `corpus/knowledge/2026-10-13-r2-version-diff-compare.md:41, 169` | — | Same counts; row 14 is the same replayed run as r4-10 row 2 (`ev_0b3c8101…`) |
| C3 | `corpus/SOURCES.md:9` (S003 row) | — | “Inspect the installed parser's declared Go range and missing-snapshot path before attributing recovery loss to a binary layout change.” |

Local tool installs or updates in this lane: **none**. `curl` was used only to fetch the upstream patch; `tar`, `grep`, `readelf`, `unzip`, `sha256sum` were already present.

## Findings

### Finding 1 — The installed gate is advisory (strong, source)

- `GoRttiMapper.java:170-172` logs `Untested Go version` and falls through. Nothing after the `if` returns or throws.
- `GoVerRange.contains` (`GoVerRange.java:83-87`) with `GoVer.compareTo` (`GoVer.java:142-152`, patch `-1` is ignored) gives: `1.25.7` in range, `1.26.8` out of range. The range boundary is therefore exactly the major.minor split `op` 2.34.1 (go1.25.7) vs 2.40.0 (go1.26.8).
- Consequence: any loss attributable to the 1.25 cap would have to arrive through a *later* branch that reads the version. No such branch exists in the code read.

Support: strong for "gate alone does not stop analysis." Not tested against any binary.

### Finding 2 — The observed message is constructor-side, and snapshot absence only selects its wording (strong, source)

- The string "Missing Go bootstrap type info, unable to extract Go RTTI info." is thrown from exactly one site: `initStructMappings` (`GoRttiMapper.java:358-360`), in the constructor (:330-349), before `init()` (:444) reads any pclntab/moduledata structure.
- That throw requires two conditions: `registerStructures` throws `IOException`, and `apiSnapshot.isInvalid()`.
- `apiSnapshot` is invalid for go1.26.8: no `go1.26.0.json` exists in the installed data (S003p), so `get` returns `EMPTY` (S003f).
- Crucially, `registerStructures` does not consult the snapshot. It looks up struct data types in the program and built-in data type managers (`DataTypeMapper.java:172-198, 282-295`). The snapshot only decides which message is thrown.
- The `IOException` branch (`initStructMappings` else-path, :364-365) and the `BootstrapInfoException` branch both return `null` from `getSharedGoBinary`. So for this site, snapshot absence changes the log text, not the analyzer outcome.
- **What is still unexplained:** why `registerStructure` failed for go1.26.8. The struct data-type source was not traced to the point of knowing whether a `runtime.moduledata`/`GoPcHeader` struct is present for a 1.26 program. `UNKNOWN`.

Support: strong that snapshot absence is not, by itself, the outcome-level cause at this site. Strong that the observed message is from the constructor. Cause of the struct failure: unknown.

### Finding 3 — Upstream fix for 1.26 is a bundle; the gate string is one of about eight deltas (strong, source)

The upstream commit `385e8cd…` changes ten files. Grouped by effect (quotes from the patch, `+`/`-` lines verbatim):

1. Gate: `-	public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` / `+	… GoVerRange.parse("1.15-1.26");` (`GoRttiMapper.java`).
2. Snapshot: `create mode 100644 Ghidra/Features/Base/data/typeinfo/golang/go1.26.0.json` (plus `certification.manifest` entry).
3. First-moduledata lookup: `MemoryBlock memblk = context.getGoSection("go.module");` added ahead of the symbol lookup (`GoModuledata.java`, hunk at patch line ~96–118). The installed `getFirstModuledata` (S003k) has no such route.
4. PcHeader layout: `-	@FieldMapping(presentWhen = "1.18+")` / `+	@FieldMapping(presentWhen = "1.18-1.25")` on `textStart` (`GoPcHeader.java`), plus a null-guard in the adjacent `getDataAddress` accessor. Upstream's own edit closes the range at 1.25, i.e. upstream treats `textStart` as absent in 1.26. The installed `1.18+` makes it present for 1.26.
5. Map type layout: `GoMapType.java` adds a `group` field `presentWhen = "1.26-"` and makes `bucket`, `elemsize`/`ValueSize`, and related fields `presentWhen = "-1.25"`.
6. Type flags: `GoTypeFlag.java` changes `UnrolledBitmap` to `"1.22-1.23"`, adds `GCMaskOnDemand(1<<4, "1.24-")` and `DirectIFace(1<<5, "1.24-")`, and changes `isSet`/`isValid` to be version-aware. The installed table (S003n) has neither the 1.24+ bit 5 nor per-version validity.
7. Build ID: `GoBuildId.java` adds a trailing magic (`"\"\n \u00ff"`) and returns `null` if it does not match.
8. Base-type version awareness: `GoBaseType.java` passes `programContext.getGoVer()` into flag checks.

Support: strong that the installed code lacks 1.26 handling beyond the gate and the snapshot file. This does not show which item causes the `op` loss.

### Finding 4 — Binary-side facts for the 2.40.0 carrier (observed, read-only)

- Package and extracted-binary hashes match the corpus (`8d029d2c…`), so the carrier is the same file the corpus measured (sha prefix only; the corpus does not pin a full digest for the run).
- `go1.26.8` string occurs 2 times (`grep -a -o`).
- Sections present: `.gopclntab`, `.typelink`, `.itablink`, `.go.module`, `.noptrdata`, `.go.buildinfo`. No `.symtab` in `readelf -S`; `readelf -s` prints zero rows (stripped).
- `runtime.firstmoduledata` occurs 0 times as a byte string; `runtime.mstart0` 2; `_rt0_amd64_linux` 1; `runtime.rt0_go` 1; `main.main` 1.
- Implication: on this carrier, the installed symbol-based moduledata lookup (`GoModuledata.java:418-421`) returns null and falls through to the search path (`findFirstModuledata`, S003l). Whether that search succeeds for 1.26 is `UNKNOWN`. The upstream `go.module` section route (Finding 3.3) is the one the binary can serve directly.

Support: observed; the causal effect on the run is `INFERENCE`.

### Finding 5 — Historical count evidence (corpus), with what it does and does not establish

Corpus claims (`corpus/knowledge/2026-10-13-r4-10-real-version-pair.md`):

- Row 1: `op-2.34.1` → `33,060 procs / 76,550 strings / 18 segs` (`ev_c0cfbcce9695…`).
- Row 2: `op-2.40.0` → `11,595 procs / 76,338 strings / 16 segs` (`ev_0b3c8101fa5f…`).
- Lines 66–73: `op-2.34.1` (`go1.25.7`) ≈ 32,933 namespaced names; `op-2.40.0` (`go1.26.8`) 11,588 `FUN_*`/`thunk_FUN_*`, sole real name `entry`. Also cites a transient `Missing Go bootstrap type info…` line “seen in its `ghidra.log` … dir since deleted, so this is observed-not-cited” (:72–73).
- Row 6: `search "main.main"` on `op-2.40.0` returns 0 hits, described as “no `main.main` exists in this version's inventory.”

Assessment:

- The 2.40.0 count and FUN fraction are `OBSERVATION` from the corpus's own run log (REA 6.4.0-era; Ghidra 12.1.4). The raw evidence directory `/tmp/rea-r4` is gone; no retained receipt exists in `corpus/` or `.ufo/` for these counts. Treat as corpus-recorded, not re-verified.
- The 2.34.1 side cannot be checked here: `1password-cli-2.34.1` is not in the pacman cache (only 2.40.0-2 and 2.41.0-1 are). Its counts are `UNVERIFIED` locally.
- `r2` and `r4` report the same `op-2.40.0` evidence ID (`ev_0b3c8101…`). That is one replayed run, not two independent observations.
- The `main.main` row overreads: an inventory miss does not show the string is absent from the binary; `grep -a` finds one occurrence in `op-2.40.0`. The recovery gap is inside Ghidra, not in the bytes.
- Analyzer link: `createFunctionIfMissing` (S003h, `GolangSymbolAnalyzer.java:238`) is the only creator of pclntab-derived functions in this path. If the Go analyzer does not run, the ~21k fewer procedures in 2.40.0 is what the code predicts. This is `INFERENCE`, consistent with, but not proof of, a null-mapper outcome.

### Finding 6 — Causal test scorecard

| Hypothesis | Source support | Binary support | Run support | Status |
|---|---|---|---|---|
| H1: 1.25 range cap disables analysis | Against: gate is advisory (F1) | None | None | Rejected as a direct cause in installed code |
| H2: missing go1.26 snapshot disables analysis | Against outcome: both branches return null; snapshot only changes message (F2) | Snapshot absent (S003p) | Message consistent with it | Not sufficient; selects wording only |
| H3: struct registration fails for go1.26 programs | Yes: the only throw site of the observed message (F2) | None | Observed message (log not retained) | Supported as the failure site; cause `UNKNOWN` |
| H4: moduledata/pcHeader layout changed in 1.26 (upstream says so) | Yes (F3) | `go.module` present, `firstmoduledata` symbol absent (F4) | None direct | Plausible; not isolated |
| H5: type-flag bit 5 / map layout changed in 1.24+/1.26 | Yes (F3.5–3.6) | Not checked in the binary | None | Plausible; not isolated |
| H6: Go analyzer simply never ran on 2.40.0 (null mapper) | Yes (F2, S003h) | Consistent with the stripped carrier | Consistent with FUN ratio and count drop | Most parsimonious; not directly observed |
| H7: the import selected a non-golang cspec | Opinion has no version predicate (S003q) | Unknown | Unknown | Not version-driven; unverified |

Calibrated answer to the assignment question: **version gating remains a hypothesis at best, and the installed code shows it is not the causal stop.** The loss is best explained, as a hypothesis, by H6 with the struct/moduledata/layout family (H3/H4) as its possible triggers. No single hypothesis is established.

## Forbidden conclusions

- “The 1.25 version gate caused the `op` 2.40.0 symbol loss.” Contradicted by the advisory gate (F1).
- “Snapshot absence caused the loss.” Snapshot absence only changes which message is thrown at the constructor site (F2).
- “Ghidra 12.1.4 cannot analyze Go 1.26.” Not tested beyond one stripped binary, one run, and one Go version. Upstream `GP-6528` exists on master and is not in the installed release.
- “The upstream commit makes installed 12.1.4 support Go 1.26.” Installed copy is pre-commit; S004 is a master-branch source only.
- “`op` 2.40.0 has no `main.main`.” The byte string occurs once in the binary (`grep -a`). The corpus row is an inventory miss.
- “11,595 is the true procedure count of `op` 2.40.0.” It is the count Ghidra recovered under a given analyzer state.
- “The 33,060 → 11,595 drop is due to the toolchain alone.” The two binaries differ in CLI source, size (41.2 vs 43.5 MB), and Go toolchain. No controlled rebuild exists.
- “Round 2 and round 4 are two independent confirmations of the 2.40.0 counts.” They share one replayed evidence ID.
- “go1.25.7 is fully supported.” Its snapshot is the base `go1.25.0.json` via fallback (S003g). The installed flag table also lacks the 1.24+ bit that upstream added, which is an untested inconsistency.
- “Version selects the Ghidra compiler spec for ELF.” The opinion table (S003q) has no version predicate. The cspec actually chosen for `op` was not recorded.

## Gaps and limits

- **Retained logs:** none. The transient `ghidra.log` cited by corpus is gone; `~/.ghidra` is absent; no Ghidra application log exists under `/var/tmp` or `/tmp` with those strings (only copies of the corpus entry matched).
- **Controlled comparison:** no same-source rebuild under two Go toolchains, no 1.25.7 vs 1.26.8 same-source pair, and no 2.34.1 binary here.
- **Struct data-type source:** not traced; cause of `registerStructure` failure is unknown.
- **`findFirstModuledata` search success on 2.40.0:** not traced past the code shown (S003l).
- **Flag/tflag values:** not parsed from the binary; H5 untested.
- **Snapshot discovery scope:** `Application.getModuleDataFile` may search other module-data roots; I only verified the installed Base data directory. No `go1.26*` file exists under the install or `~/.ghidra`.
- No REA run, no Ghidra run, no test or build executed.

## Reproduction (read-only)

```
sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip
unzip -o -q <that zip> 'ghidra/app/util/bin/format/golang/*' 'ghidra/app/plugin/core/analysis/Golang*' -d /var/tmp/kaidoku-r14-w1-src
nl -ba ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java | sed -n '79p;170,172p;351,367p'
curl -sL https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174.patch -o ghidra-385e8cd.patch
tar --zstd -xOf /var/cache/pacman/pkg/1password-cli-2.40.0-2-x86_64.pkg.tar.zst usr/bin/op > op-2.40.0 && sha256sum op-2.40.0
grep -a -o "main\.main" op-2.40.0 | wc -l ; readelf -S op-2.40.0 | grep -i "go\.\|pclntab"
```

Scratch extractions under `/var/tmp/kaidoku-r14-w1-src` and `/var/tmp/kaidoku-r14-w1-op` were removed after this report; no finding depends on them. Re-derive from the archive, patch, and package named above using the commands in this section.

## Residual risk for L1

- Do not promote H1 or H2 into any SOURCES `teaches` cell or knowledge entry as a causal explanation. The S003 `teaches` cell is already correct in spirit; it should not be read as establishing layout causality.
- Any knowledge entry on this topic must state: gate advisory; snapshot absence affects message at one site; upstream fix is a multi-file bundle; 2.34.1 side unverified locally; counts are corpus-recorded and not re-verified.
- The `main.main` “no such procedure” wording in `2026-10-13-r4-10-real-version-pair.md` row 6 is an overclaim; it should be corrected to “no inventory row” in any append-only errata.
