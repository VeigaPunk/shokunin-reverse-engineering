# SC-1 — C2 freshness receipt: Ghidra module counts

## Scope and baseline

Re-derived the installed Ghidra feature and processor directory counts as a freshness check. The comparison baseline is `PROVINCE.md:46` (34 feature modules, 39 processor modules); the inventory was reported reverified on 2026-10-18 at `PROVINCE.md:25`. The corpus's original 35-feature figure was corrected to 34 in `corpus/knowledge/2026-10-13-ghidra-install.md:66-76`.

## First-hand measurement

Read-only count of immediate child directories under the installed Ghidra tree `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra`. Command:

```sh
set -eu
root=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra
printf 'features='; find "$root/Features" -mindepth 1 -maxdepth 1 -type d -printf 'x' | wc -c
printf 'processors='; find "$root/Processors" -mindepth 1 -maxdepth 1 -type d -printf 'x' | wc -c
printf 'feature_names='; find "$root/Features" -mindepth 1 -maxdepth 1 -type d -printf '%f,' | LC_ALL=C sort | tr -d '\n'; printf '\n'
printf 'processor_names='; find "$root/Processors" -mindepth 1 -maxdepth 1 -type d -printf '%f,' | LC_ALL=C sort | tr -d '\n'; printf '\n'
```

Exact stdout:

```text
features=34
processors=39
feature_names=BSim,BSimFeatureVisualizer,Base,BytePatterns,ByteViewer,CodeCompare,DataGraph,DebugUtils,Decompiler,DecompilerDependent,FileFormats,FunctionGraph,FunctionGraphDecompilerExtension,FunctionID,GhidraGo,GhidraServer,GnuDemangler,GraphFunctionCalls,GraphServices,MicrosoftCodeAnalyzer,MicrosoftDemangler,MicrosoftDmang,PDB,ProgramDiff,ProgramGraph,PyGhidra,Recognizers,Sarif,SourceCodeLookup,SwiftDemangler,SystemEmulation,VersionTracking,VersionTrackingBSim,WildcardAssembler,
processor_names=6502,68000,8048,8051,8085,AARCH64,ARM,Atmel,BPF,CP1600,CR16,DATA,Dalvik,HCS08,HCS12,Hexagon,JVM,Loongarch,M16C,M8C,MC6800,MCS96,MIPS,NDS32,PA-RISC,PIC,PowerPC,RISCV,Sparc,SuperH,SuperH4,TI_MSP430,Toy,V850,Xtensa,Z80,eBPF,tricore,x86,
```

The receipt timestamp captured after the recount was `2026-10-19T19:22:46Z` (`date -u '+%Y-%m-%dT%H:%M:%SZ'`).

## Verdict and disposition

- Feature-module count — **VERIFIED**: measured 34 immediate child directories, matching the corrected baseline of 34; delta 0.
- Processor-module count — **VERIFIED**: measured 39 immediate child directories, matching the baseline of 39; delta 0.

No count drift was observed in this check. This measurement establishes only the current immediate-directory inventory, not module contents or runtime capability. No PROVINCE or corpus change is proposed; this is the C2 measured receipt.
