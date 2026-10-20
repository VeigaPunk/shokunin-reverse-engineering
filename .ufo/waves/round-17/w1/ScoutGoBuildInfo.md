# ScoutGoBuildInfo — Ghidra 12.1.4 Go build-info reader (C2 depth support)

Seat: KaidokuR17.ScoutGoBuildInfo-3 (author-side advisory). Read-only; no REA analyze/decompile,
no Ghidra/analyzeHeadless, no carrier execution, no installs. Byte reads of carriers and `readelf`
only.

**Anchor legend.** Short file names refer to members of
`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`:
`GoBuildInfo.java` = `ghidra/app/util/bin/format/golang/GoBuildInfo.java`;
`GoRttiMapper.java`, `GoApiSnapshot.java`, `GoVer.java`, `GoVerRange.java`, `GolangElfInfoProducer.java`
= same `.../golang/` (rtti/ for the first two); `ElfInfoItem.java`, `ElfInfoProducer.java` =
`ghidra/app/util/bin/format/elf/info/`; `ElfLoader.java`, `PeLoader.java`, `MachoLoader.java`,
`ElfProgramBuilder.java` = `ghidra/app/util/opinion/`;
`GolangSymbolAnalyzer.java`, `GolangStringAnalyzer.java` = `ghidra/app/plugin/core/analysis/`;
`DataConverter.java`, `LittleEndianDataConverter.java` = `Framework/Generic/lib/Generic-src.zip`
(`ghidra/util/`). Go reference = `go1.23.0/src/debug/buildinfo/buildinfo.go` and
`go1.23.0/src/cmd/link/internal/ld/data.go`, pinned by `curl` of raw.githubusercontent.com.

## 1. Where the reader lives and how it finds `\xff Go buildinf:`

Observed (source):
- Section names `go.buildinfo` (generic), `.go.buildinfo` (ELF), `go_buildinfo` (Mach-O):
  `GoBuildInfo.java:44-46`. Magic constant `"\u00ff Go buildinf:"`, 14 bytes, ISO-8859-1 to keep
  `0xff` intact: `GoBuildInfo.java:50-53`.
- Entry point `GoBuildInfo.fromProgram` (`:81-85`) → `findBuildInfo` (`:92-110`).
  Lookup order:
  1. `getFirstGoSection(program, SECTION_NAME, MACHO_SECTION_NAME)` (`:93-95`), resolved by
     `getGoSection` with prefixes `.` and `__` (`GoRttiMapper.java:82-83,229-237`), i.e. `.go.buildinfo`
     or `__go_buildinfo`. Read starts at section offset 0 (`readItemFromSection`, `:137-155`).
  2. Only if that returned null: memory block `data` (`getGoSection(program,"data")`, `:97-99`), then
     `findGoBuildInfoOffset(dataBP, 512)` (`:101`) and re-read at the found offset (`:103-105`).
     Comment says "common PE location" but the fallback is not PE-gated — any program with a `.data`
     block reaches it.
- `findGoBuildInfoOffset` (`:117-134`) is a **byte-by-byte** scan (`pos++` at `:131`) for the first
  14-byte magic match within `maxSearchLength`; returns -1 on miss/EOF (`:129-133`).
- Fatal parse guard: magic re-checked in `read`, else `IOException("Missing GoBuildInfo magic")`
  (`:165-168`). `readItemFromSection` converts any `IOException` into null (`:148-152`).

Observed (loader plumbing):
- ELF: `ElfLoader.detectCompilerName` sets compiler spec `golang` when any section name contains
  `gopclntab`, `go_buildinfo` or `go.buildinfo` (`ElfLoader.java:196-198`; predicate
  `GoRttiMapper.java:201-211`). `GolangElfInfoProducer` maps `.go.buildinfo` → `GoBuildInfo::read`
  (`GolangElfInfoProducer.java:46-47`) and is discovered as an `ElfInfoProducer` extension
  (`ElfProgramBuilder.java:2435-2443`; `ElfInfoProducer.java:42-48`), so build info is parsed and
  program info decorated **at load time**, independent of the compiler-spec test.
- Mach-O: same predicate, `MachoLoader.java:547-549`.
- PE: after `isGolangProgram` (`PeLoader.java:300-301`), `processGolangProperties` calls
  `GoBuildId.findBuildId` then `GoBuildInfo.findBuildInfo` and `.markupProgram`
  (`PeLoader.java:305-318`). PE's Go detection (`PeLoader.java:1146-1169`) is `GoBuildId` in `.text`
  OR `findGoBuildInfoOffset(.data, 512) != -1`, and is only reached from the `e_lfanew()==0x80`
  GCC/Clang branch (`PeLoader.java:1086-1090`) — a narrower gate than the ELF path.

Observed (bytes on this host, read-only; both carriers from the round-17 pilot set):
- `/usr/bin/shfmt`, sha256 `58f765638eed5309573967726d9f9f54c8ba16cbcc65a6a5dfe0e5285aeab459`:
  `.go.buildinfo` file offset `0x35a4c0`, size `0x600`, `sh_addralign 16`; bytes
  `ff 20 47 6f 20 62 75 69 6c 64 69 6e 66 3a | 08 | 02 | 16×00 | 13 'go1.27.0-X:nodwarf5' |
  c1 0b (uLEB=1473) | 30 77 af 0c ...` (sentinel). REA's program inventory reports the same block at
  `0x45a4c0` = section vaddr `0x35a4c0` + PIE image base `0x100000` (`pilot/shfmt.json`; shfmt is
  `ET_DYN`), whereas esbuild (`ET_EXEC`) is reported at its vaddr `0xd90000` (`pilot/esb.json`).
- esbuild 0.25.12, sha256 `bab29b2ca7a9e89b67cf720b77b2d743f9f31f5cf0d5bd74ee8c8de30ced7014`:
  `.go.buildinfo` file offset `0x990000`, size `0x330`; header identical in shape:
  `...3a | 08 | 02 | 16×00 | 09 'go1.23.12' | fa 05 (uLEB=762) | 30 77 af 0c ...`.
These bytes match the Go linker writer: 32-byte zeroed buffer, 14-byte prefix, `PtrSize` at
`data[14]`, endian bit at `data[15]`, then `|= 2` (pointer-free/inline format), varint-prefixed
version and modinfo, padded to a multiple of 16 (`data-go1.23.go:2347-2372`, align `:2353`,
`|=2` `:2364`, padding `:2367-2370`).

## 2. Header and inline vs pointer format

Observed (source, `GoBuildInfo.java`):
- Header: 14-byte magic (`:165`), `ptrSize` byte (`:169`), `flags` byte (`:170`);
  `FLAG_ENDIAN = 1<<0` (0 = little, 1 = big, `:61,171`), `FLAG_INLINE_STRING = 1<<1` (`:62,172`).
- Cross-check `if (reader.isBigEndian() && endian != Endian.BIG) throw IOException("Mixed endian-ness")`
  (`:174-176`). One-sided: a little-endian program with the big-endian flag bit set is not rejected.
- Inline (bit 1 set): seek `startOffset + 32` (`:392`), uLEB128 version length + UTF-8 bytes
  (`:394-396`), uLEB128 module length + bytes (`:398-399`); module must be framed by the 16-byte
  hex sentinels `3077af0c9274080241e1c107e6d618e6` / `f932433186182072008242104116d8f2`
  (`:56-59`, checked `:504-507`, `IOException("bad sentinel")` `:508`). A synthetic struct
  `GoBuildInfo_inline_<len>_<len>...` is built (`:400-415`).
- Pointer (bit 1 clear, pre-1.18 layout): seek `startOffset + 16` (`:418`), read two `ptrSize`
  pointers (`:419-420`) as virtual addresses in the program address space (`:422-424`), then each
  Go string header `{void* data; long len}` via `readRawGoString` (`:536-548`); `data==0 || len==0`
  yields empty bytes (`:540-542`). `versionofs`/`moduleofs` fields appended to the struct (`:434-436`).
- `parseBuildInfo` (`:442-493`): split modinfo on `\n`; `=>\t` continuation lines attach a replacement
  to the preceding module (`:449-453`); keys `path`, `mod`, `dep`, `build` (`:466-485`); a leading
  `go` is stripped from the version (`:488-490`); object constructed at `:492-493`.
- Version stored/decorated as program info `Golang go version` (`:352`; constant
  `GoVer.java:33`, writer `:101-102`), plus app path, main module, `Golang dep[N]`, and
  `Golang build[<setting>]` (`:351-374`).

Conformance to Go (observed): header offsets 14/15, inline data at +32 (`buildinfo.go:199-201`),
pointer strings at +16 and +16+ptrSize (`buildinfo.go:219-221`), and sentinel stripping
(`buildinfo.go:225-231`) all agree. Both pilot carriers are inline (`flags=0x02`), so Ghidra takes the
`:392` branch in every round-17 carrier; the pointer branch is untested by the pilot set.

## 3. What Ghidra does when build info is absent or the version is unknown

Observed (source):

| Trigger | Code path | Observable result |
|---|---|---|
| No `.go.buildinfo`, no magic in `.data` | `findBuildInfo` → null (`:92-110`); `getGoBinary` returns null, comment "probably not a Go binary" (`GoRttiMapper.java:160-163`) | `GoBuildInfo` markup silently skipped (`ElfInfoItem.java:54-61` returns when the item is null). No loader message. Each Go analyzer then logs `ERROR ... Go symbol analyzer error: unable to get GoRttiMapper` / `Go string analyzer error: ...` (`GolangSymbolAnalyzer.java:133-136`, `GolangStringAnalyzer.java:103-106`). |
| Section exists, magic/parse bad | `read` throws, `readItemFromSection` catches → null (`:148-152`); `ElfInfoItem.readItemFromSection` logs `WARN Unable to read Elf item in section: <name>` with stack (`ElfInfoItem.java:88-91`) | Warn at load; then same null-mapper path as above. |
| Version string unparseable (e.g. empty, `devel`) | `GoVer.parse` → `INVALID` (`GoVer.java:62-81`); `getGoBinary` throws `BootstrapInfoException("Invalid Go version string [%s]")` (`GoRttiMapper.java:166-169`) | Caught in `getSharedGoBinary` (`:114-116`): `WARN <message>` on the application log **and** `logAnalyzerMsg` into the analysis message log (`:128-135`). Mapper is null → analyzer errors as above. |
| Version parses but outside `SUPPORTED_VERSIONS` `1.15-1.25` (`GoRttiMapper.java:79,83`) | `Msg.error "Untested Go version [%s]"` and **continues** (`:170-172`); snapshot lookup for that version returns `EMPTY` (`GoApiSnapshot.java:102-116, 242, 503-505`); constructor's `registerStructures` fails and, because `apiSnapshot.isInvalid()`, throws `BootstrapInfoException("Missing Go bootstrap type info, unable to extract Go RTTI info.")` (`GoRttiMapper.java:351-361`) | ERROR + WARN on the application log, then analyzer errors; no RTTI, no Go types, no Go function signatures. |
| Fallback option set (`Fallback Go Version`, `GolangSymbolAnalyzer.java:1311-1312,1328,1345` → `GoBuildInfo.setFallbackVersion`, `:129-131`) | Consulted **only** when build info is null or its version is `INVALID` (`GoRttiMapper.java:153-159`); builds a metadata-free `GoBuildInfo` (`GoBuildInfo.java:188-201`: version = option, path `"unknown path"`, no module/deps/settings, `struct == null`) | Rescues obfuscated/missing build info only. **Does not** rescue an out-of-range but parseable version (`1.27.0`): the condition at `:154` is false. [Inference from the condition; consistent with the observed shfmt run that had no fallback option set.] |

Observed (pilot logs, confirming the third row):
- `pilot/shfmt-log/ghidra.log:48` `Using Language/Compiler: x86:LE:64:default:golang` (build info/section
  detection chose the Go spec), then `:82` `INFO Reading Go binary info`, `:83`
  `ERROR (GoRttiMapper) Untested Go version [1.27.0]`, `:84` `WARN ... Missing Go bootstrap type info,
  unable to extract Go RTTI info.`, `:85` `ERROR (GolangSymbolAnalyzer) ... unable to get GoRttiMapper`;
  repeated at `:86-89` for `GolangStringAnalyzer`. Failure is not cached (the
  `TransientProgramProperties` supplier returns null without storing, `GoRttiMapper.java:102-126`), so
  each analyzer re-parses the blob and re-emits the pair — two identical Error/Warn pairs per run.
- `pilot/esbuild-0.25.12-log/ghidra.log:62-64` `Reading Go binary info` →
  `INFO (GoApiSnapshot) Using Go API snapshot for 1.23.12` → `INFO (GoRttiMapper) Using Go API snapshot
  for version 1.23.12`; `:67` `INFO (GolangSymbolAnalyzer) Go version 1.23.12`. This is the exact
  success branch (`GoRttiMapper.java:174-181`, `GoApiSnapshot.java:163`).

Observation vs inference split: the messages and their order are observed in the retained logs and
match the quoted source lines; the "not cached" explanation is [INFERENCE] from `:102-126` (the
supplier returns null, and only a non-null result is stored).

## 4. Divergences from Go's own reader (calibration)

| Facet | Go (`debug/buildinfo`) | Ghidra 12.1.4 | Effect |
|---|---|---|---|
| Magic search alignment | requires `i%16==0` relative to section/segment start, advancing to the next 16-boundary after a miss (`buildinfo.go:174-187`) | plain byte scan, no alignment test (`GoBuildInfo.java:117-134`, `pos++` `:131`) | Ghidra can accept an unaligned false magic that Go rejects; for section-resident blobs both agree (offset 0, `sh_addralign 16` observed on both carriers). |
| Search extent | whole `DataStart()` section/segment, or first writable `PT_LOAD` / first RW initialized PE section / `__go_buildinfo` (`buildinfo.go:165-167,288-347,378-396`) | exact `.go.buildinfo`/`__go_buildinfo` at offset 0, else first **512 bytes** of `.data` (`GoBuildInfo.java:92-110`, `:101`) | A `.data`-placed blob beyond 512 bytes, or an ELF with section headers stripped, is invisible to Ghidra even though Go finds it. Section path dominates for normal ELF carriers. |
| `ptrSize` validation | rejects anything but 4 or 8 as `errNotGoExe` (`buildinfo.go:212-218`) | no check; byte passed to `readNextUnsignedValue(ptrSize)` (`GoBuildInfo.java:169,419-420`) → `DataConverter.getValue` → `Objects.checkIndex(size, Long.BYTES+1)` (`LittleEndianDataConverter.java:70-72`) | Pointer-format blob with `ptrSize>8` raises an unchecked `IndexOutOfBoundsException` that escapes the `IOException` catch (`GoBuildInfo.java:148-152`). [INFERENCE: Go's linker never emits this; no crafted blob tested per read-only bounds.] Inline blobs ignore `ptrSize` for reads, so this only affects pre-1.18 layouts. |
| Endianness | compares flag bit against the file's byte order for pointer reads (`buildinfo.go:203-218`) | rejects only "BE program + LE flag" (`GoBuildInfo.java:174-176`); LE program + BE flag is silently read little-endian | A mis-flagged blob yields garbage strings instead of a parse error on LE targets. |
| Empty version | `vers == ""` → `errNotGoExe` (`buildinfo.go:222-224`) | empty string → `GoVer.INVALID` → `BootstrapInfoException` (`GoRttiMapper.java:166-169`) | Same "no Go" outcome stated as a hard bootstrap error rather than "not a Go executable". |
| Version suffix | not parsed (version used as raw string) | suffix after the first non-`[.0-9]` is dropped (`GoVer.java:63-65`), so `go1.27.0-X:nodwarf5` → `1.27.0` | The `-X:nodwarf5` build tag is lost from `Golang go version`; range check sees 1.27.0. |
| Range handling | n/a | `1.15-1.25` inclusive, error-but-continue outside it (`GoRttiMapper.java:79,170-172`) | Out-of-range binaries still load, with Go analysis effectively disabled by the missing type snapshot. |

## 5. Consequence for the round-17 probe/C2 predictions

- The contract's `buildinfo-probe.py` ("16-byte aligned search as Go's debug/buildinfo does",
  `contract.md:98-105`) matches Go, not Ghidra, on alignment; that difference is **not observable**
  on the pilot carriers because both place the blob at a 16-aligned section offset 0 under
  `.go.buildinfo`. A discriminating control would need a `.data`-resident or unaligned blob.
- The probe's pointer-format branch ("report `pointer_format` and stop") is the pre-1.18 layout that
  Ghidra *does* implement (`GoBuildInfo.java:418-436`), so "pointer format" is not a Ghidra limitation
  — it is a probe decision. Only the inline branch is exercised by shfmt/esbuild.
- C2's expected shfmt trace is the four-line pattern at `pilot/shfmt-log/ghidra.log:82-85` plus the
  repeat at `:86-89`, and the absence of any `Using Go API snapshot` line. esbuild's expected trace is
  `:62-64` + `:67` with snapshot 1.23.12. These are source-derived predictions that the retained pilot
  already confirms; the prediction table can cite both the source anchors and the log lines.
- A predictor should not expect `Missing Go bootstrap type info` for unparseable versions (that row
  emits `Invalid Go version string [...]` instead), nor any message at all for a missing
  `.go.buildinfo` (silent markup, analyzer error only). This three-way discrimination is the useful
  diagnostic distinction for the C2 table.

## 6. Remaining unknowns

- No PE/Mach-O carrier was available, so the `isGolang`/`processGolangProperties` path
  (`PeLoader.java:1086-1090,1146-1169,305-318`) and the `512`-byte `.data` bound are source-only.
- `ResourceFile.getFile(true)` not-found semantics were not inspected; only the observed effect (no
  extra log line for the absent 1.27 snapshot) and the `catch → null` at `GoApiSnapshot.java:172-178`.
- Whether the unchecked `IndexOutOfBoundsException` aborts program import or is caught higher up was
  not exercised (read-only bounds; no crafted blob).
