# CriticC2Confound — r17 C2 causal reading (author-side advisory critic)

Target: the go1.27 failure on shfmt. Could it come from something other than a missing base snapshot, such as a layout change, the compiler spec, or build-info parsing?
Inputs: `pilot/` (logs SHA-256-verified with `sha256sum -c pilot/SHA256SUMS`, all OK), S003 `Base-src.zip` members extracted to `/tmp/kr17-c2conf` (read-only), installed Go data dir, drafts in `w1/`.
Paths below are relative to `.ufo/waves/round-17/` unless absolute. Java anchors point into S003 members.
Read-only. No REA analyze/search/decompile, no Ghidra, no carrier execution, no installs. Carrier bytes were read with `sha256sum` and Python `open(...,'rb')` only.

## Verdict

The C2 causal reading holds. All three named confounds are excluded by lines that are present or absent in the log, and each exclusion follows from a specific source branch. The drafts do have three calibration defects:

1. **Underclaim.** The log does separate "base file absent" from "base present but no arch records", although the drafts say it cannot.
2. **Missing masking statement.** The failure happens before Ghidra reads any binary structure, so the run carries no information about the Go 1.27 layout. The drafts do not say this.
3. **Collinearity.** The supported range and the installed snapshot set coincide on this install, so the outcome alone cannot say which one caused the failure. Only the source can.

## Confound table: what each alternative would log, against what was observed

| hypothesis | log signature if true (source) | shfmt `pilot/shfmt-log/ghidra.log` | verdict |
|---|---|---|---|
| H-cspec: not marked golang | Analyzers are gated on `isGolangProgram` (`GolangSymbolAnalyzer.java:105-107`, `GoRttiMapper.java:196-198`). If the gate fails, no Go lines appear at all (log-extract `no_go_analysis`). | `:48` `x86:LE:64:default:golang`; `:82-89` Go lines present. REA profile `compiler_spec_id = auto-default` (`pilot/shfmt.json`). | excluded |
| H-reginfo: no Go register info for 1.27 | WARN `Missing Go register info…` or `…info file…` (`GoRegisterInfoManager.java:82,93`). | Absent (grep count 0). `x86-64-golang.register.info:3` `versions="1.17-"` is open-ended. | excluded |
| H-buildinfo: build info not found | `getGoBinary` returns null silently (`GoRttiMapper.java:160-163`). The analyzer error appears with no Untested or Missing line. | `:83`/`:87` `Untested Go version [1.27.0]` present. | excluded |
| H-buildinfo: version unparseable | BootstrapInfoException `Invalid Go version string [...]` (`GoRttiMapper.java:166-168`). | Absent (grep count 0). `:83` prints `GoVer.toString` (`GoVer.java:155-158`) = `1.27.0`. That requires the `go` strip (`GoBuildInfo.java:488-489`) and the suffix strip (`GoVer.java:64-65`). | excluded |
| H-fallback: version came from the fallback option | Used only if the analyzer option `fallbackGoVer` is non-empty (`GolangSymbolAnalyzer.java:129-131`, `GoBuildInfo.java:192-197`). | Not logged either way. REA preset is `ghidra-default`. INFERENCE: the version came from `fromProgram`. My stdlib byte read finds inline build info that decodes to `go1.27.0-X:nodwarf5`. The version is identical either way, so this is not causal. | not causal |
| H-layout-a: snapshot valid but struct mapping fails | IOException `Invalid Go bootstrap struct mapping info` (`GoRttiMapper.java:363-365`), then ERROR `Failed to read Go info` with a stack trace (`:118-122`). | Absent (grep count 0). `:84`/`:88` show the other branch, which needs `apiSnapshot.isInvalid()` (`:356-360`). | excluded for this run |
| H-layout-b: moduledata/pcHeader incompatible | This runs in `init()` (`:444-466`): WARN `Unknown Go pcheader magic` (`:457-458`), or a ptrSize mismatch / read error that lands at `:121`. | Absent. `init()` is never reached: it is called only on a non-null mapper (`:108-111`), and the constructor threw first (`:348`). | **untested (masked)** |
| H-arch-empty: base present, no linux/amd64/all records | `isInvalid()` is `arches.isEmpty()` (`GoApiSnapshot.java:503-505`), so it gives the same Missing line. A base being present forces INFO `Using Go API snapshot for 1.27.0` (`GoApiSnapshot.java:128` → `:162-163`, because patch 0 skips the loop at `:153`). Because `read` returns a valid `ver` (`:239`), it also forces `Using Go API snapshot for version 1.27.0` (`GoRttiMapper.java:178-180`). | Neither line is present in `:82-89`. | **excluded by the log** |
| H-missing-base | Base lookup returns null with no log line (`GoApiSnapshot.java:122-125`) → `EMPTY` (`:115`, `:242`). The Go type lookup has only one source for structs, the snapshot (`GoTypeManager.java:449`), so it returns null. No `Unable to find Go type` WARN is emitted (`GoRttiMapper.java:392-393`, observed absent). `registerStructure` then throws on the first class, `GoModuledata` (`DataTypeMapper.java:176-181`, `GoRttiMapper.java:295`), and the code takes the `:356-360` branch. | `:83-85` and `:87-89` match exactly. | supported (sufficient cause) |

The absence-based rows are valid only because the retained copy runs past the Go window: `:90-119` is the analysis summary and `:125` is stamped 10:17:56, after the `:82-89` Go lines. If a FINAL log ends before the AutoAnalysisManager summary, absence must not be used.

## Findings (defects in the drafts)

**F1. Underclaim (calibration).** `w1/draft-knowledge-r17.md:117` says "The pilot log cannot separate these two causes". `w1/DraftKnowledgeEntry.md:47` says the same. This is false: see the H-arch-empty row. A base that is present always emits the `GoApiSnapshot.java:163` INFO line, or for patch > 0 the `:160` WARN, and then the `GoRttiMapper.java:180` line. Both are absent at shfmt `:82-89`. Separately (OBSERVATION), `go1.23.0.json` and `go1.25.0.json` both contain the `all`, `linux`, `linux-amd64`, `unix` and `amd64` keys, so an empty arch set is not plausible for the installed bases.
- Smallest correction: rewrite :117 as "separated by the absent INFO pair (`GoApiSnapshot.java:163`, `GoRttiMapper.java:180`); missing-base is the only route consistent with the log." Label it OBSERVATION of absence plus INFERENCE from source, valid given log-window completeness.

**F2. Overclaim risk: masking is not stated (calibration and depth).** The constructor (`GoRttiMapper.java:329-349`) reads only the build-info version and the language before `initStructMappings` throws. No moduledata, pcHeader or type bytes are read. The observed signature is therefore invariant to Go 1.27's binary layout. Missing-base is a **sufficient** cause. Whether it is the **only** blocker is untested. `draft-knowledge-r17.md:136` ("adding a snapshot alone is not tested") is near this point but never states why: the failure point comes before any layout read. Any wording such as "only the missing snapshot blocks 1.27" would be false provenance.
- One layout facet is cheaply discriminated. OBSERVATION: the shfmt `.gopclntab` magic is `0xfffffff1` (ptrSize 8, minLC 1), which equals `GO_1_20_MAGIC` (`GoPcHeader.java:48`). The pcHeader magic was not bumped. Moduledata and type layouts remain UNKNOWN.
- Smallest correction: add one NOT-examined/INFERENCE line. Suggested text: "failure precedes any binary-structure read (`GoRttiMapper.java:348` throws before `init()` `:444`); the run carries no evidence about 1.27 moduledata/type layout; pclntab magic 0xfffffff1 = GO_1_20_MAGIC observed by byte read".

**F3. Range and snapshot collinearity (calibration).** `SUPPORTED_VERSIONS` is `1.15-1.25` (`GoRttiMapper.java:79`), and the installed bases are exactly `go1.15.0.json` through `go1.25.0.json`. On this install, no real carrier can have one condition without the other, so the outcome alone cannot attribute the failure to the range gate or to the snapshot. Only the source discriminates: `:170-172` logs and does not throw. `draft-knowledge-r17.md:32` already says the code continues after logging. The FINAL entry must keep the attribution to the snapshot via source and call `Untested` a co-symptom, never "fails because out of range".

**F4. Resolvable UNKNOWN (depth).** `draft-knowledge-r17.md:118` and `DraftKnowledgeEntry.md:20` leave the doubled block (`:82-85`, `:86-89`) UNKNOWN. Source: `TransientProgramProperties.java:107-110` returns null without caching when the supplier yields null. Each analyzer's `getSharedGoBinary` call therefore re-runs the whole route: `GolangSymbolAnalyzer.java:133` and `GolangStringAnalyzer.java:103`.

**F5. Misattribution (calibration, minor).** `w1/ScoutGoApiSnapshotLog.md:99-100` says the exception is "thrown by `init()` (356-361)". It is thrown by the constructor's `initStructMappings` (`GoRttiMapper.java:348`, `:351-367`). `init()` (`:444`) is never reached.

**F6. Unlabelled inference (calibration, minor).** `draft-knowledge-r17.md:38` states that `DataTypeMapper.java:172-181` "is the structure-lookup throw that starts the chain" as fact. The cause is dropped at `GoRttiMapper.java:356-360`: `e` is not chained, and `.formatted(goVer)` has no specifier, so the log cannot show which struct failed or where. Supporting evidence is the absent `:393` WARN, but the line should be labelled INFERENCE.

**F7. Contract classification collapses two causes (fixable, low).** `contract.md:58-59` classifies `bootstrap_missing` whenever the Missing line appears, whatever the `snapshot_labels` are. Because `compare.py` checks `snapshot_label` (`contract.md:76-78`), the discriminator is still scored. The knowledge text should say that `bootstrap_missing` with empty labels means missing-base, and with non-empty labels means arch-empty.

## Carrier-shape confound and discriminating carriers available (advisory; L1 selects)

- The pilot pair changes several variables at once. shfmt is an Arch PIE built with the external linker: segments `.interp`, `.dynsym`, `.relr.dyn`, `.gnu_debuglink` (`pilot/shfmt.json`), plus `libc.so.6` and 46 unresolved externals (log `:50-52`, `:72-75`). esbuild is a static ET_EXEC with no `.interp` or `.dynsym` (`pilot/esb.json`). By F2 this cannot affect the failure route. It does weaken the in-range success control as a matched contrast.
- Host byte scan (buildinfo magic, 16-byte aligned, inline version; ELF `e_type`) over `/usr/bin`, `~/.local/bin`, `/usr/lib/docker/cli-plugins`. OBSERVATION: no in-range ET_DYN (Arch PIE) Go carrier exists; every ET_DYN carrier is go1.26.1 or later. Discriminating candidates:
  - **Matched shape pair.** `/usr/bin/gh` (github-cli 2.102.0-1, ET_DYN, `go1.27.1-X:nodwarf5`, sha256 `fa4ea764…eb3e`) vs `/home/vgpnk/.local/bin/gh` (ET_EXEC, `go1.27.1`, sha256 `7469124f…4c9b`). Same program and version, different build shape. Predicted: an identical signature with `[1.27.1]` and no snapshot lines. A difference would falsify F2. Both have pclntab magic `0xfffffff1`.
  - **Second 1.27.0 PIE.** `/usr/bin/git-lfs` (git-lfs 3.8.0-1, `go1.27.0-X:nodwarf5`, sha256 `9ab4f28a…9fc2`).
  - **New in-range route.** `/usr/bin/aether` (aether 4.32.0-2, ET_EXEC, `go1.25.14`, sha256 `06c91f55…006e`). The base `go1.25.0.json` is present and no 1.25 patch diffs are installed (OBSERVATION: the diff maxima run 1.15.15 through 1.24.6, and none exist for 1.25 or later). Predicted: WARN `Falling back from 1.25.14 to 1.25.0` (`GoApiSnapshot.java:159-160`), then `Using Go API snapshot for version 1.25.14` (`GoRttiMapper.java:180`). This exercises the fallback branch, which neither pilot carrier reaches.
- No local carrier can split F3. The only way to split it is a Ghidra install whose snapshot set differs from its range, for example S004 upstream; that is out of scope.

## Impacted axes

- **calibration:** F1 (underconfident), F2 (overclaim guard), F3, F5, F6, F7.
- **depth:** F2 (masking mechanism plus one byte-level layout facet), F4 (closes an UNKNOWN), and the matched-pair and fallback-branch carriers.

## Searched / not done

- Searched the log sources for: `GoRttiMapper.java` 95-475, `GoApiSnapshot.java` 87-260 and 503, `GoVer.java`, `GoTypeManager.java` 81-87, 320-455 and 821, `DataTypeMapper.java` 150-300, `GoRegisterInfoManager.java` 73-100, `GolangSymbolAnalyzer.java` 100-140 and 515-564, `TransientProgramProperties.java` 95-118, and `GoPcHeader.java` magic constants.
- Grepped both pilot logs for every alternative-route string (`Missing Go register info`, `Failed to read Go info`, `Invalid Go bootstrap struct mapping`, `Unable to find Go type`, `Unknown Go pcheader`, `Falling back from`, `Invalid Go version string`): count 0 in both.
- Checked the install for any other `typeinfo/golang` dir or any `go1.2[6-9]*` file: only `Ghidra/Features/Base/data/typeinfo/golang` exists, and it has neither. Also checked `round-16/selection.py` against the base rule `go%d.%d.0.json` (`:211`, `:220`).
- Not done: Go 1.27 moduledata or type layout versus 1.25 (no Go toolchain or source installed: `go: command not found`), class identity of the loaded Ghidra jars (r14 limitation stands), and any FINAL run.
- The `ARTIFICAL_GOLANG_CONTEXT` segment (`GolangSymbolAnalyzer.java:520`, reached via `:154` after a non-null mapper) appears in `pilot/esb.json` and not in `pilot/shfmt.json`. This is a second, log-independent success marker inside the REA JSON. INFERENCE: it is absent whenever the mapper is null.
- Installs: none.
