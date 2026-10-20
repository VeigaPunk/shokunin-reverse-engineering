# Round 15 w1 — Go snapshot resource format review (ReviewSnapshotSchema)

seat: KaidokuR15.ReviewSnapshotSchema (leaf, read-only review)
scope: installed Ghidra 12.1.4 Go API snapshot resources and the code that selects/parses them. No tool written. No corpus, SOURCES, LOG, SCORECARD, MANIFEST, or SKILL edits. No builds, tests, gates, or target execution.
axes served: C1 depth (installed snapshot inventory and source-selection decision record) and C1 calibration (corrections to the round-14 diagnosis).

## Method and provenance

- Source reads (opened, anchors below): `Base-src.zip` members `rtti/GoApiSnapshot.java`, `rtti/JsonPatch.java`, `rtti/JsonPatchApplier.java`, `rtti/GoRttiMapper.java`, `rtti/GoTypeManager.java`, `structmapping/DataTypeMapper.java`, `GoVer.java`, `GoVerRange.java`, `GoBuildInfo.java`, `plugin/core/analysis/GolangSymbolAnalyzer.java`.
- Installed resources: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/` (11 base JSON files, 123 patch diffs, 9 GDT files).
- Inventory commands: stdlib Python read-only parsing of the installed JSON and diff files, plus `sha256sum`, `ls`, and `unzip -p | grep` over the source archive. Nothing was written except this report and a temporary member list at `/tmp/r15w1_members.txt` (outside the repository; removed after use).
- Not done: no Ghidra run, no patch application to produce derived snapshots, no Gson/Ghidra jar inspection, no target binary. Every behavioral statement below is a **source-derived prediction** unless labeled as an observed installed-file fact.
- Tool installs/updates: none.

## 1. Installed snapshot inventory (observed, read-only)

Base files: `typeinfo/golang/go{M}.{m}.0.json`. Full SHA-256 from `sha256sum`; bytes from `ls -l`; top-level keys and "all" counts from json.load.

| file | bytes | SHA-256 | top keys | all.Funcs | all.Types | unreachable `-cgo`/`cgo` keys |
|---|---:|---|---:|---:|---:|---:|
| go1.15.0.json | 4267141 | cd070f2165716fd63643c722e50722295367fb7d36ff7a153d56178877da5b10 | 26 | 12453 | 2421 | 10 |
| go1.16.0.json | 4671548 | d668acd92c30102dc85243c4ef580d5294e6c6f494d16f45a95c42959de00dee | 28 | 12809 | 2526 | 11 |
| go1.17.0.json | 6100205 | fb1f31849c303642739cfe907f810e1606eb1b34ddee41486b359bd9df28d549 | 28 | 17231 | 2764 | 11 |
| go1.18.0.json | 6325742 | 86a0687c9ce129bf9cf94faa20bee250fc13a298935d3b0ca3e0dee68ef91f67 | 28 | 17960 | 2883 | 11 |
| go1.19.0.json | 6469362 | 79c93ea499226c79e234053ea886779a26d3be363e437b102c046d8b6bb98885 | 29 | 18523 | 3002 | 12 |
| go1.20.0.json | 8875175 | 6def34993dd352b01f749dc44935178bdf2dbd13f585adf631798919ad6d0a32 | 28 | 25511 | 3119 | 11 |
| go1.21.0.json | 9039469 | 7bfe8f9a0f316ba3e6258152e35181c1d1c5c6b0bb0e6e9e95355490bb447b31 | 27 | 26243 | 3257 | 10 |
| go1.22.0.json | 9203666 | c8feb28695499d1631af5ae441c8fd39c7eb75ce54dc8472673f2693e6974640 | 27 | 26712 | 3426 | 10 |
| go1.23.0.json | 9368866 | 3b1d795f2e017c17ad15119bd8083e16ccaffb66cd3d504065fe06aea0f63692 | 27 | 27192 | 3532 | 10 |
| go1.24.0.json | 10039962 | aab28c8f7fcf36224f01b883b1f3f13208412d22e4eb0d87d090a258e124c571 | 27 | 28922 | 3706 | 10 |
| go1.25.0.json | 10081618 | 54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252 | 27 | 29041 | 3741 | 10 |

Observed for all 11 base files: parse OK; 0 duplicate object keys (object_pairs_hook); 0 non-standard `Kind` values across all arch objects; `all` present in every file. `Funcs`/`Types` presence was checked on the sampled arch objects only, not exhaustively for every arch object.

Absent: `go1.26.0.json` (no 1.26 base), and no `go1.25.N.json.diff` for any N. No base for 1.14 or earlier.

Kinds observed across all arches and files: `struct` (37588), `alias` (8577), `iface` (3265), `funcdef` (2841). **`basic` never occurs** in installed data, so the `GoBasicDef`/`EnumValues` path (GoApiSnapshot.java, "TODO: work in progress") is unexercised by these files.

Position prefixes observed: `$GOROOT` (134642) and `$GOMODROOT` (47167). `Position` is present on Funcs and on some Types. No Go* deserialization class declares `Position`; Gson ignores unknown fields by default, so `Position` is inert for parsing but changes bytes (see §6).

Arch-key union across the 11 files is 29 keys: `386 all amd64 arm arm64 cgo darwin darwin-amd64 darwin-amd64-cgo darwin-arm64 darwin-arm64-cgo darwin-cgo linux linux-386 linux-386-cgo linux-amd64 linux-amd64-cgo linux-arm linux-arm-cgo linux-arm64 linux-arm64-cgo linux-cgo unix windows windows-386 windows-386-cgo windows-amd64 windows-amd64-cgo windows-cgo`. Absent by file: `cgo`, `darwin-arm64`, `darwin-arm64-cgo` absent in go1.15.0; `cgo` absent in 1.16–1.18; `darwin-cgo` absent in 1.20 and `darwin-cgo` + `windows-cgo` absent in 1.21–1.25. No arch-specific key named `linux-riscv64`, `windows-arm64`, etc. exists.

Required bootstrap struct names (from `@StructureMapping` in `rtti/*.java`): all JSON-backed names (`runtime._func`, `runtime.functab`, `runtime.iface`, `runtime.itab`/`internal/abi.ITab`, `runtime.moduledata`, `runtime.slice`, `runtime._type`/`internal/abi.Type`, and the `runtime.*type`/`internal/abi.*` alternates) are present in `all` in **all 11 files**. `string` is primitive (not in JSON `all`). `runtime.pcHeader` is in `all` for 1.25.0 and absent for 1.15.0 (the ≤1.15 artificial fallback at GoRttiMapper.getType covers that case). `GoName`, `GoVarlenString` are not JSON names (not checked further).

Patch diffs (`typeinfo/golang/patchverdiffs/go{M}.{m}.{p}.json.diff`): 123 files, contiguous from patch 1 for each minor:

| minor | files | max patch | | minor | files | max patch |
|---|---:|---:|---|---|---:|---:|
| 1.15 | 15 | 15 | | 1.21 | 13 | 13 |
| 1.16 | 15 | 15 | | 1.22 | 12 | 12 |
| 1.17 | 13 | 13 | | 1.23 | 12 | 12 |
| 1.18 | 10 | 10 | | 1.24 | 6 | 6 |
| 1.19 | 13 | 13 | | 1.25 | 0 | — |
| 1.20 | 14 | 14 | | 1.26 | 0 | — |

Byte-identical diff pairs (same SHA-256): 1.15.4=1.15.5, 1.20.8=1.20.9, 1.21.12=1.21.13, 1.22.8=1.22.9, 1.22.11=1.22.12, 1.23.5=1.23.6, 1.23.8=1.23.9. Same size but different digest: 1.15.14/1.15.15, 1.19.11/1.19.12, 1.20.6/1.20.7. Diff sizes grow with patch number (1.15.1 = 2466 bytes; 1.15.15 = 110373 bytes; 1.24.6 = 118810 bytes), which is consistent with each diff being base-relative rather than chained [INFERENCE from sizes; the applier code at GoApiSnapshot.java:134-140 applies a single diff to `go{M}.{m}.0.json`].

Diff structural check (observed, 123 files): 82,579 sections; 157,752 `+`/`-` lines (81,034 `+`, 76,718 `-`); every file's first line starts `@ `; 0 sections with zero lines; every `+` value parses as JSON (single-line); path arrays are JSON arrays whose first element is an arch name (e.g. `["all","Funcs",name,"Params",1,"Name"]`). Non-operation lines exist and are ignored by `JsonPatch`: 2538 space-led lines and 1542 unprefixed structural lines such as `]` or `[` (pretty-printing residue; `JsonPatch.readPatchSection` skips lines shorter than 3 and any line whose first character is not `+`, `-`, or `@`). `-` values were not JSON-validated here, so a `-`-led continuation line would be misread as an operation; this was not exhaustively excluded. Sample (go1.15.1.json.diff lines 1–3): `@ ["all","Funcs","net/http/fcgi.(*net/http/fcgi.response).Write","Params",1,"Name"]` / `- "data"` / `+ "p"`.

## 2. Snapshot format (from the opened sample and the parser)

Top level: JSON object whose keys are arch names. Gson reads only keys in the search chain (§3); all other keys are `skipValue`d (GoApiSnapshot.java:212-219).

Per arch object: `Funcs` (map name → GoFuncDef) and `Types` (map name → GoTypeDef). Observed shapes:
- Funcs entry: `Params` [{`Name`,`DataType`}], `Results` [{`Name`?,`DataType`}], `Flags` (int, bitmask `VarArg=1, Generic=2, Method=4, NoReturn=8, InterfaceFunc=16`), `TypeParams` (1.25.0 only; 282 entries), `Position` (`$GOROOT/...:L:C` or `$GOMODROOT/...`).
- Types entry `Kind=struct`: `Fields` [{`Name`,`DataType`}], `Position`. Example `archive/tar.Header`: Typeflag byte, Name string, Linkname string, Size int64, ...
- `Kind=alias`: `Target`. Example `any` (1.25.0).
- `Kind=iface`: no other fields observed (`archive/tar.FileInfoNames`).
- `Kind=funcdef`: `Params`, `Results`, `Position` (example `archive/tar.numberFormatter`).
- `Kind=basic` (unobserved): `DataType`, `EnumValues` (per Java class).

Deserialization (GoApiSnapshot.java:205-240, Java classes at 296-466):
- `GoTypeDefDeserializer` dispatches on `Kind`: struct/iface/basic/alias/funcdef; **any other value returns `null`** (default branch). A missing `Kind` throws NPE (`obj.get("Kind").getAsString()`). Installed files: 0 unknown kinds.
- `GsonPostFixupAdapter` replaces null `Params/Results/TypeParams/Fields` with empty lists.
- `GoArch.Funcs`/`GoArch.Types` are not null-guarded: an arch object missing either key yields NPE at `getFuncdef` (GoApiSnapshot.java:514-521) / `getTypeDef` (524-531). Not present in installed files.

## 3. Source-selection decision procedure (as coded)

Inputs: the binary's Go version string (GoBuildInfo) or the analyzer fallback option; GOOS; GOARCH.

1. Version. `GoBuildInfo.getGoVer()` = `GoVer.parse(version)` (GoBuildInfo.java:233-238). The stored version has a leading `go` stripped at GoBuildInfo.java:488-489 when it starts with `go`. `GoVer.parse` (GoVer.java:46-72) removes everything from the first character that is not `.` or a digit (`replaceAll("[^.0-9].*$","")`), splits on `.`, and requires at least major and minor. Patch missing → 0 (`parse`) or -1 (`parseWildcardPatch`).
2. Fallback. If buildinfo is null or its version is invalid, `GoBuildInfo.fromFallbackInfo` runs (GoRttiMapper.java:154-156). It uses the analyzer option `fallbackGoVer` (GolangSymbolAnalyzer.java:129-131; setter GoBuildInfo.java:188-190) and returns null unless `GoVer.parse(option)` is valid (GoBuildInfo.java:192-199).
3. Invalid version → `BootstrapInfoException("Invalid Go version string …")` (GoRttiMapper.java:166-168).
4. Range. `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")` (GoRttiMapper.java:79). Out of range → `Msg.error("Untested Go version …")` and **continues** (GoRttiMapper.java:170-172). The range is patch-wildcarded on both ends (GoVerRange.java:42-53), and `GoVer.compareTo` treats patch -1 as a wildcard (GoVer.java:143-153), so every 1.25.x is in range; 1.26.x and ≤1.14.x only log.
5. Base. `GoApiSnapshot.get` → `getApiSnapshotJsonFile` → base = `goVer.withPatch(0)` → `typeinfo/golang/go{M}.{m}.0.json` (GoApiSnapshot.java:118-125, 168-177). Missing → returns null → `get` returns `EMPTY` (GoApiSnapshot.java:115), `GoVer.INVALID`, `arches = Map.of()`.
6. Patch. `getPatchVerDiffFile(goVer)` walks `prevPatch()` (patch-1, floored at 0) until a `patchverdiffs/go{M}.{m}.{q}.json.diff` exists, only while patch > 0 (GoApiSnapshot.java:148-166). It never crosses minors. If nothing is found, the base is used unchanged.
7. Derivation. If a diff is found (for q, possibly q < p), the base is patched with that diff and the derived bytes are labeled `go{goVer}.json` (GoApiSnapshot.java:134-143). The returned `GoApiSnapshot` is constructed with `goVer` (line 239), so `getVer()` reports p even when the content came from q.
8. Chain. `archSearchOrder = [goOS-goArch, goOS, unix-if-GOOS-in-IS_GOOS_UNIX, goArch, "all"]` (GoApiSnapshot.java:108-109). `read` keeps only these keys and stores them in that order (212-237). Lookups take the first chain entry that has the name (`getFuncdef` 514-521, `getTypeDef` 524-531). `-cgo` keys and bare `cgo` are never in any chain (the chain can only produce `goOS-goArch`, `goOS`, `unix`, `goArch`, `all`), so they are dead data for this path.
9. `isInvalid()` = `arches.isEmpty()` (GoApiSnapshot.java:503-505). Because `all` is always in the chain, `isInvalid()` is false for any file that has an `all` key.
10. Struct registration. `GoRttiMapper` constructor → `initStructMappings` → `registerStructures(GOLANG_STRUCTMAPPED_CLASSES)` (GoRttiMapper.java:294-300, 330-367). An `IOException` is turned into `BootstrapInfoException("Missing Go bootstrap type info …")` **only if `apiSnapshot.isInvalid()`** (GoRttiMapper.java:356-359); otherwise it becomes `IOException("Invalid Go bootstrap struct mapping info …")`. `DataTypeMapper.registerStructure` throws `Missing struct definition …` when `getType` returns null for a non-`StructureReader` class (DataTypeMapper.java:172-180).
11. Outer handling. `getSharedGoBinary` catches `BootstrapInfoException` (warn + analyzer message, return null; GoRttiMapper.java:114-117, 125) and `IOException` ("Failed to read Go info", return null; 118-124). A malformed snapshot JSON therefore surfaces as `Failed to read Go info`, not as the missing-bootstrap message. The analyzer then logs "unable to get GoRttiMapper" and returns false (GolangSymbolAnalyzer.java:134-137).

### Predicted outcome table (source-derived, not executed)

| case | base | diff applied | predicted result |
|---|---|---|---|
| 1.25.0 | present | none (no diff) | base content; info "Using Go API snapshot for 1.25.0" |
| 1.25.3 | present | none | base 1.25.0 content; **warn "Falling back from 1.25.3 to 1.25.0"** although no diff applied (see F3) |
| 1.24.6 | present | 1.24.6 (exact) | exact diff; label matches |
| 1.24.9 | present | 1.24.6 (q=6<9) | **1.24.6 content labeled 1.24.9** (F2) |
| 1.22.13 (no such file) | present | 1.22.12 | 1.22.12 content labeled 1.22.13 |
| 1.26.x | absent | n/a | `EMPTY` → isInvalid → **"Missing Go bootstrap type info"** |
| 1.14.x | absent | n/a | `EMPTY` → same as 1.26 (range warning first) |
| malformed JSON, present base | present | — | IOException → "Failed to read Go info" (not the Missing message) |
| present file, arch chain lacks linux-*, but has `all` | present | — | `isInvalid()` false; arch-only types return null; struct mapping still succeeds for the json-backed structs in §1 (see F1) |

## 4. Findings

Severity: H = would mislead a decision record or analyzer log; M = calibration or reproducibility risk; L = limit.

**F1 (M, calibration — correction to the round-14 entry).** `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` lines 51-54 say a present file without applicable OS/arch records "can therefore reach the same invalid-snapshot branch". From source, `isInvalid()` is `arches.isEmpty()` (GoApiSnapshot.java:503-505) and `all` is hard-coded last in the chain (108-109). Every installed base file has `all`, so OS/arch exclusion alone cannot set `isInvalid()`. The decision-table row at line 77 ("Distinguish absent base file from OS/architecture exclusion") should read: missing base file, or a file with no `all` and no chain key. For installed data, the observed OS/arch effect is per-type null lookups, not the Missing message. Limit: only the 11 installed files were checked; no hand-edited snapshot was built.

**F2 (H, inventory correctness).** Patch fallback silently changes content while keeping the label. For p not in the diff set, the content of the largest lower q is applied and the derived file, the `GoApiSnapshot` version, and the "Using Go API snapshot for …" info line all report p (GoApiSnapshot.java:128-143, 239; GoRttiMapper.java:178-181). Installed effect: every 1.24.7+ binary would receive 1.24.6 content; every 1.25.N would receive 1.25.0 content. A decision record must store `requested_patch` and `selected_diff_patch` separately.

**F3 (M).** The "Falling back …" warning (GoApiSnapshot.java:158-161) prints whenever requested patch ≠ result patch, including when no diff is found and the base is used (e.g. 1.25.3). It is misleading but harmless to content.

**F4 (H for fallback users).** `fromFallbackInfo` validates the option with `GoVer.parse`, which rejects a leading `go` (GoVer.java:65 strips from the first non-digit/dot, so `go1.25.0` becomes empty and invalid). With `fallbackGoVer="go1.25.0"`, `fromFallbackInfo` returns null (GoBuildInfo.java:192-199), `getGoBinary` returns null at GoRttiMapper.java:157-163, and the analyzer reports "unable to get GoRttiMapper" with no version-format message. The option must be `1.25.0`. [Source-derived; not run.]

**F5 (L, dead data).** 10–12 keys per file (`-cgo` and bare `cgo`) are unreachable by any chain (GoApiSnapshot.java:108-109, 212-219). Inventories that count arch keys should separate reachable from unreachable keys.

**F6 (M, reproducibility).** `Position` is unused by parsing but changes with every Go patch. Sample: go1.15.1.json.diff lines 8–13 change only `Position` strings. A deterministic semantic hash should exclude `Position`; a byte hash should be recorded separately.

**F7 (M, shadowing).** Chain precedence is first-hit. Installed files are mostly disjoint across chain keys, but go1.15.0.json has 40 names that appear in ≥2 entries of the `darwin/arm64` chain (`darwin`, `unix`, `arm64`, `all`) because `darwin-arm64` is absent in 1.15.0. The 1.16+ `darwin/arm64`, `linux/amd64`, `windows/amd64` chains show 0 overlaps.

**F8 (M, unexercised paths).** No `basic` Kind is present, so `GoBasicDef`/`EnumValues` is unverified. The unknown-`Kind` default returns null, silently skipping that type (GoApiSnapshot.java `GoTypeDefDeserializer`). Neither occurs in installed data.

**F9 (M, error differential).** Malformed JSON → `Failed to read Go info` (GoRttiMapper.java:118-124); missing base → Missing message (356-359). A decision record must record `base_parse_status` separately from `base_present`.

**F10 (L, version strings).** Only a leading `go` is stripped (GoBuildInfo.java:488-489). `devel …` or other non-`go` strings become invalid → fallback → `Invalid Go version string` (GoRttiMapper.java:166-168). Pre-release suffixes are truncated by `GoVer.parse` (`1.25rc1` → `1.25.0`, GoVer.java:65), so a pre-release maps to the release base. [Source-derived; not run.]

**F11 (L, GDT).** The installed `golang_1.15…1.23_anybit_any.gdt` files are not referenced anywhere in `Base-src.zip` (grep over all `.java` members for `golang_1`, `anybit`, `typeinfo/golang`: only GoApiSnapshot.java:171 matches). They are not inputs to this RTTI path. Limit: only Features/Base sources were searched.

**F12 (L, Gson).** Duplicate object keys: 0 in installed files. In Gson's map adapter a duplicate key throws JsonSyntaxException "duplicate key" [INFERENCE from Gson source knowledge; not opened in this round, L1 should confirm against the bundled Gson jar].

**F13 (L, range log).** The 1.15–1.25 gate is informational only (GoRttiMapper.java:170-172). The round-14 entry's claim that the range does not abort is correct.

## 5. Proposed deterministic inventory fields (spec only; no tool written)

Per base snapshot (`go{M}.{m}.0.json`):
- `path` (relative to `typeinfo/golang`), `bytes`, `sha256_full`, `parse_status` (ok / error class), `duplicate_key_count`.
- `top_keys_sorted` (list) and `top_keys_sha256` (hash of canonical JSON array).
- `has_all` (bool); `arch_keys` (sorted) with `reachable` flag (key is in some chain) and `chain_membership` (which of the 5 chain slots it can fill).
- per arch: `funcs_count`, `types_count`, `kind_histogram` (struct/alias/iface/funcdef/basic/other), `has_Funcs_and_Types` (bool), `position_prefix_histogram`, `typeparams_count`.
- `bootstrap_names_present_in_all` (per class in §1: count of the 19 JSON-backed struct classes whose structure name, or any listed alternate name, is present in `all`; expected 19/19 for these files; `string` is primitive and reported separately).
- `semantic_sha256` computed over canonical JSON with `Position` removed; `full_sha256` retained.

Per patch diff:
- `path`, `target_version` (`M.m.p`), `bytes`, `sha256_full`, `section_count`, `plus_count`, `minus_count`, `first_line_is_@`, `zero_line_sections` (expect 0), `plus_values_parse` (expect all ok), `path_first_element_histogram` (arch names), `digest_duplicate_of` (other file with identical SHA-256), `gap_check` (contiguous patches from 1 for each minor).

Per decision (one record per analyzed binary):
- `raw_version_string`, `version_source` (buildinfo | fallback | none), `goos`, `goarch`, `requested_version` (`M.m.p` or invalid), `in_declared_range` (bool), `range_outcome` (in-range | untested-log-only).
- `base_file`, `base_present`, `base_sha256` (full), `base_parse_status`, `base_has_all`.
- `requested_patch`, `selected_diff_patch` (q, 0 if none), `diff_exact` (bool), `label_mismatch` (q ≠ p and q > 0), `diff_sha256`.
- `chain` (ordered list), `chain_keys_present` (ordered), `chain_keys_absent`.
- `predicted_isInvalid` = (not base_present) or (no chain key present, which implies no `all`).
- `predicted_bootstrap_outcome` ∈ {`proceed`, `Missing Go bootstrap type info`, `Failed to read Go info`, `Invalid Go version string`, `Invalid Go bootstrap struct mapping info`}.
- `struct_names_missing` (list of required names with no hit in the chain).
- `observed_analyzer_log_lines` (copied verbatim; labeled as observed only when an analyzer run was performed).

## 6. Parse caveats (consolidated)

1. Labeling: derived content can be from q ≠ p (F2); `getVer()` and logs report p (F2, F3).
2. Missing base short-circuits: diffs for a minor whose base is absent are never applied (GoApiSnapshot.java:122-125).
3. Patch search is per-minor and downward only; no upward or cross-minor fallback (148-166).
4. Fallback option must lack the `go` prefix (F4).
5. Version parse truncates everything after the first non-digit/dot (F10).
6. Only the `all` key guarantees `isInvalid()==false` (F1).
7. `-cgo`/`cgo` are never read (F5).
8. Position churn (F6).
9. `basic` Kind and unknown-Kind null path are unexercised (F8).
10. Patch applier is position-based with no context check (JsonPatchApplier.java class doc: "Does not use any context hints… should only be used against the exact original value"). Array paths use numeric indices (e.g. `Params,1,Name`), so a wrong base would corrupt silently. Installed diffs contain no context lines.
11. JsonPatchApplier.applySection indexes `lines.get(0)` without a guard; installed files have no zero-line sections, so this is latent only.

## 7. Corrections and routing

- C1 (depth/calibration): the round-14 knowledge entry needs the F1 correction (lines 51-54 and the row at line 77) and an F2 note (the 1.24.7+ label issue would matter for any future cross-patch diagnosis). Routed as an advisory to the lane; **not written here** per the contract.
- The round-14 entry's ordering claim (range warning precedes the snapshot lookup; struct registration is conditional) is confirmed by the opened code (GoRttiMapper.java:170-176, 330-367).
- The round-14 claim that patch search does not fall back to an earlier minor is confirmed (GoApiSnapshot.java:148-166).
- The round-14 claim that `GoApiSnapshot.get` returns `EMPTY` on a missing base is confirmed (115, 122-125).

## 8. Limits

- Only installed Ghidra 12.1.4 Base sources and the installed JSON/diff files were used. No upstream S004 was re-opened in this round. No Ghidra run; no derived patch was materialized and checked against any ground truth.
- No Go binary was inspected; the version → base mapping is source-derived.
- `GoName` and `GoVarlenString` structure names were not checked against JSON.
- "Installed" means the path under `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`; the byte-identity with `Base-src.zip` was not re-verified.
- Predictions in §3 are reasoning over the opened code paths and have not been executed.

## 9. Proposed L1 checks (not executed by this seat)

1. `sha256sum` each base JSON and the 123 diffs; compare with §1 and the digest pairs listed there.
2. Confirm `all` present and `Funcs`/`Types` present in every arch object across the 11 files with a one-off JSON check (non-Ghidra).
3. Confirm the Gson duplicate-key behavior against the bundled Gson jar used by Ghidra 12.1.4 (F12 [INFERENCE]).
4. Optional: one headless Ghidra run with a 1.24.9-labelled fixture to observe F2's label behavior (only if the lane permits execution).
5. Optional: one headless run with `fallbackGoVer="go1.25.0"` vs `"1.25.0"` to confirm F4.
6. Confirm the F1 correction by reading the knowledge-entry lines the correction targets (51-54, 77) against §4 F1 before editing.
7. Re-check `Base-src.zip` SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` against SOURCES row S003 before citing any anchor.

## Verdict (advisory, C1 snapshot schema)

- Inventory fields and selection record are specified (§5) and reproducible from the installed bytes listed in §1.
- Decision outcomes for missing base, patch fallback, and OS/arch applicability are source-derived (§3), with F1 and F2 changing what the prior entry should say.
- Calibration: the round-14 diagnosis overstates the OS/arch path (F1). The patch-label issue (F2) is a new, source-observed caveat. No numeric score is claimed.
