# Scout — how `x86:LE:64:default:golang` is chosen (pilot `ghidra.log:48`)

Seat: `KaidokuR17.ScoutGolangCspec-3` (advisory, read-only). Axes: calibration, depth.
Sources: installed Ghidra 12.1.4 tree `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`; Java members cited as
`Base-src.zip:<member>:<line>` (extracted with `unzip -o -q` to `/tmp`, bytes unmodified) and
`SoftwareModeling-src.zip:<member>:<line>` from `Ghidra/Framework/SoftwareModeling/lib/`;
REA 6.5.0 runtime `…/node_modules/rea-agents/dist/cli-runtime/binary-BVOr2mgE.js:<line>`;
pilot logs `.ufo/waves/round-17/pilot/{esbuild-0.25.12-log,shfmt-log}/ghidra.log`.
Labels: **OBSERVED** = read directly in file/log; **INFERENCE** = derived from source semantics, not executed.

## Answer

The compiler spec is chosen **at import time by the ELF loader**, from the ELF section-header **names** alone,
through the x86 opinion/ldefs tables; REA passes no `-processor`/`-cspec` for these carriers. It is
**independent of the Go RTTI bootstrap outcome**: the choice happens before a `Program` exists, before any
analyzer runs, and no Go code ever mutates the language. The dependency runs the *other* way — the Go
analyzers are gated on the compiler-spec *name* being `golang` (`GoRttiMapper.isGolangProgram`), so a
bootstrap failure cannot deselect the cspec, but a failed cspec selection would suppress bootstrap entirely.

## 1. Exact chain (each step anchored)

1. **No caller override.** Pilot analysis profiles carry `language_id: "auto-from-header"`,
   `compiler_spec_id: "auto-default"` and no `language_selection` key (OBSERVED,
   `pilot/esb.json`, `pilot/shfmt.json`, `analysis_profile.parameters.upstream_analysis_profile.parameters`).
   REA turns a language override into `-processor`/`-cspec` only when
   `language_selection ∈ {configured-v1, provider-pinned-v1}` (`binary-BVOr2mgE.js:7705-7714`), and passes
   `languageOverride` only when that value exists (`:8530`, `:8573`); otherwise
   `ghidraHeadlessArguments` emits no language arguments for a normal ELF (`:3866-3898`; the
   no-DOS/no-PSP/no-override/no-raw case selects the empty list `: []` at `:3898`). Pinned languages exist
   only for MIPS/PSP/RISC-V/PowerPC (`:7579`).
2. **Headless chooser.** With no language/compiler hint, `ProgramLoader.Builder.getLoadSpec` uses
   `LoadSpecChooser.CHOOSE_THE_FIRST_PREFERRED` (`ProgramLoader.java:573-580`), i.e. the first `LoadSpec`
   with `isPreferred()` (`LoadSpecChooser.java:61-68`). The chosen pair is logged as
   `"Using Language/Compiler: " + loadSpec.getLanguageCompilerSpec()` (`ProgramLoader.java:486-490`) —
   the pilot's line 48.
3. **Loader computes specs.** `ElfLoader.findSupportedLoadSpecs` (`ElfLoader.java:101-137`) reads
   `e_machine` and `e_flags` as decimal strings (`ElfHeader.java:1918-1920`, `:1926-1928`) and issues
   **two** opinion queries into one `HashSet<QueryResult>`: first, only if a compiler name was detected,
   `query(getName(), machine, compiler)` (`ElfLoader.java:109-112`); then unconditionally
   `query(getName(), machine, elf.getFlags())` (`:113`). Each result becomes a `LoadSpec` (`:132`).
   `getName()` is `"Executable and Linking Format (ELF)"` (`ElfLoader.java:42`, `:177-179`).
4. **Detection predicate is name-only.** `detectCompilerName` (`ElfLoader.java:188-200`) calls
   `elf.parseSectionHeaders()` (`:189`; `ElfHeader.java:1111-1123`), maps to `ElfSectionHeader.getNameAsString()`
   (`:190-192`), then `SwiftUtils.isSwift` (`:193-195`) and
   `GoRttiMapper.hasGolangSections` (`:196-198`), returning `GoConstants.GOLANG_CSPEC_NAME`
   (`GoConstants.java:26`, the literal `"golang"`). `hasGolangSections`
   (`GoRttiMapper.java:201-210`) matches any section name containing `gopclntab`, `go.buildinfo`
   (`GoBuildInfo.java:44`) or `go_buildinfo` (`:45`). No program bytes are read beyond the section-header
   table; no RTTI, build-info or symbol data is consulted.
5. **Opinion base table.** `x86.opinion:40-52` under `<constraint loader="Executable and Linking Format (ELF)">`:
   gcc container `:41` with leaf `primary="62" … size="64" variant="default"` at `:43`; swift leaf
   `:46`; golang container `:48` with leaf `primary="62" secondary="golang" processor="x86" endian="little"
   size="64" variant="default"` at `:49`. The `golang` id resolves to
   `x86-64-golang.cspec` via `x86.ldefs:97` inside language `id="x86:LE:64:default"` (`x86.ldefs:92`,
   `version="4.9"` `:88`).
6. **Preferred flag, not filtering.** `QueryOpinionService.addQuery` builds the DB keyed
   `[loader][primary][secondary]` (`QueryOpinionService.java:86-104`) but stores **every** pair of the broad
   query `LanguageCompilerSpecQuery(processor, endian, size, variant, null)` — i.e. the compiler-spec ID is
   dropped from the lookup — flagging each as `preferred = pair.compilerSpecID.equals(query.compilerSpecID)`
   (`:106-112`). So the "golang" entry is *the same five x86:LE:64:default pairs*
   (windows, clangwindows, gcc, golang, swift) with only `golang` marked preferred. Handler inheritance is
   `QueryOpinionServiceHandler.java:41-60`, dispatch per element at `:104-106`.
7. **Two-query union keeps the golang flag.** `query(..., "golang")` returns x86/LE/64/default pairs with
   `golang` preferred. `query(..., "0")` (e_flags 0) has no exact secondary `"0"`; masking rejects
   `"golang"`/`"swift"` as non-numeric (`QueryOpinionService.java:143-161`, masking `:192-221`, matcher
   `:223`), so it falls through to
   the `null` key — the gcc leaf — returning the same five pairs with `gcc` preferred. `QueryResult.equals`
   and `hashCode` compare **only** `pair` (`QueryResult.java:36-64`), so `results.addAll` of the gcc set
   (`ElfLoader.java:113`) is a no-op for every already-present pair: the golang-preferred entries inserted at
   `:111` survive, and exactly one preferred `LoadSpec` exists. **INFERENCE from Java `HashSet` semantics**,
   consistent with both pilot logs (below); I did not execute Ghidra to observe it.
8. **Log string format.** `LanguageCompilerSpecPair.toString()` is `languageID + ":" + compilerSpecID`
   (`SoftwareModeling-src.zip:ghidra/program/model/lang/LanguageCompilerSpecPair.java:240-242`); hence
   `x86:LE:64:default` + `:` + `golang` = log line 48 verbatim.

## 2. Independence from the RTTI bootstrap outcome

**Observed counterexample.** shfmt carrier `go1.27.0-X:nodwarf5` (subject sha256 `58f765638eed…`,
`pilot/shfmt.json`): `shfmt-log/ghidra.log:48` prints `x86:LE:64:default:golang`, and 35 lines later the
same session fails bootstrap — `:83` `Untested Go version [1.27.0]`, `:84` `Missing Go bootstrap type info,
unable to extract Go RTTI info.`, `:85` `Go symbol analyzer error: unable to get GoRttiMapper`, repeated at
`:86-89`. The language line is unchanged by the failure. Same file, esbuild carrier
(`go1.23.12`, sha256 `bab29b2ca7a9…`): `:46` ELF loader, `:48` golang cspec, then `:61` `ANALYZING all memory
and code`, `:62` `Reading Go binary info`, `:63` snapshot resolved. Import (and thus the cspec) precedes all
Go work in both logs — **OBSERVED**.

**Source direction.** cspec selection happens in `findSupportedLoadSpecs`, i.e. before any `Program` is
created and long before `GoRttiMapper.getSharedGoBinary` (`GoRttiMapper.java:102-129`) or
`getGoBinary` (`:151-188`). Bootstrap inputs (`GoBuildInfo.fromProgram`, version range
`SUPPORTED_VERSIONS = "1.15-1.25"` `:79`, snapshot `GoApiSnapshot.get` → `EMPTY` on a miss
`GoApiSnapshot.java:102-116`, `BootstrapInfoException` `:356-360`) all live downstream. Nothing in
`ghidra/app/util/bin/format/golang/**` or the two Go analyzers calls `setLanguage`/`setCompilerSpec` —
only reads (`GoRttiMapper.java:196-199`) — so no bootstrap path can revise the choice.

**The reverse coupling is real and should be carried into the round's diagnostics.** The analyzer gate is
`GoRttiMapper.isGolangProgram` = compiler-spec description name equals `"golang"`
(`GolangSymbolAnalyzer.java:105-107`, `GolangStringAnalyzer.java:94-96`, `GoRttiMapper.java:196-199`; the
description name is the ldefs `name="golang"` attribute, `BasicCompilerSpecDescription.java:22-34`,
`SleighCompilerSpecDescription.java:25-27`). Both analyzers are default-enabled
(`GolangSymbolAnalyzer.java:98-102`, `GolangStringAnalyzer.java:77-81`). So the cspec is a **precondition**
for bootstrap, not a consequence.

## 3. Boundary conditions (what would NOT yield the golang cspec)

- Predicate is section-name-only, case-sensitive `contains`. `.note.go.buildid` and `.gosymtab` do **not**
  match; `.gosymtab` size 0 (`esbuild-log/ghidra.log:56` `Skipping section [.gosymtab] with invalid size 0x0`)
  is a loader-log artifact unrelated to the cspec choice.
- An ELF whose section-header table is absent/renamed (e.g. section headers stripped, program-header-only
  rebuild) yields `compiler == null`; only the gcc-preferred query runs → `x86:LE:64:default:gcc`, and then
  `isGolangProgram` is false, so the Go analyzers never run even if `.gopclntab` bytes are mapped as a
  segment. This is the one failure mode that loses Go analysis *before* RTTI can even be attempted.
- Both pilot carriers do carry the names: `/usr/bin/shfmt` has `.gopclntab` @`0x1b3a98` (size `0x14d5c3`),
  `.go.buildinfo` @`0x35a4c0`; the esbuild build has `.gopclntab` @`0xb20ae0`, `.go.buildinfo` @`0xd90000`,
  `.gosymtab` size 0 (**OBSERVED** with `readelf -S -W`, no execution).

## 4. Calibration consequence for `log-extract.py`

`language_compiler` (line 48) and the Go bootstrap fields (lines 62-89) are **independent observables**:
neither predicts the other. A prediction tool must not treat `language_compiler == golang` as evidence of a
resolved bootstrap, nor a `missing_bootstrap` classification as evidence the cspec detection failed. The
only relation is the one-way gate described above.

## 5. Limits / what would falsify the inference

Not executed: no Ghidra/`analyzeHeadless`, no REA analyze/search/decompile, no carrier execution; sources
read from the installed `-src.zip` members and the ELF section tables. Step 7 (preferred-flag survival via
`HashSet` first-insert) is **INFERENCE**; it would be falsified by a Go ELF whose log line 48 reads
`…:gcc`, or by source evidence that `results` is not insertion-preserving (it is a `HashSet<QueryResult>`,
`ElfLoader.java:107`). No installs or upgrades were made.

Report: .ufo/waves/round-17/w1/ScoutGolangCspec.md
