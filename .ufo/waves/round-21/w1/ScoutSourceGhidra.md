# ScoutSourceGhidra — installed first-Go-failure semantics

## Scope and axes

- Axes in the round-21 context: **C1 calibration** and **C2 depth**. This scout addresses only the bounded source question about first Go-failure semantics; no validator, prediction, or source-row decision is made.
- Read-only source: existing S003 archive `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`. Its observed SHA-256 is `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`, matching the S003 registry row in `corpus/SOURCES.md:9`.
- No external URL was opened. No Ghidra, REA, Go toolchain, carrier, or source code was executed. The source was read directly from archive members. No LSP device was exposed in this task's tool inventory; no grep output is used as semantic proof.

## Observed source facts

1. **There are two synchronous failure boundaries, before and after the main analyzer try.** `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:102-127` shows `getSharedGoBinary` calling `getGoBinary`, then `init`; it catches an `IOException`, logs `Failed to read Go info` (`:121`), and its supplier returns `null`. `GoRttiMapper.java:444-464` orders `init` as module discovery, function data initialization, `goTypes.init`, then method-info initialization. Thus an escaping IOException in that initialization path is a bootstrap failure, before `GolangSymbolAnalyzer.added`'s main try. The caller checks `goBinary == null`, logs `Go symbol analyzer error: unable to get GoRttiMapper`, and returns false (`ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java:134-136`).

2. **Within the main pass, the first uncaught IOException aborts the remaining synchronous sequence.** `GolangSymbolAnalyzer.java:144-184` puts `recoverGhidraDataTypes`, `markupGoTypes`, module and symbol markup, function handling, and deferred-task scheduling in one sequential `try`; the `catch (IOException e)` logs `Go analysis failure` (`:181-184`) and the method returns false. An IOException escaping one stage therefore prevents later stages in that block and success-flag assignment from running. This supports “first *escaping IOException* in the synchronous pass,” not “first error of any kind.” Exact source message strings: **“Failed to read Go info”** (`GoRttiMapper.java:121`) and **“Go analysis failure”** (`GolangSymbolAnalyzer.java:182`); each quote is under 25 words.

3. **A child read failure is not necessarily an escaping failure.** `ghidra/app/util/bin/format/golang/rtti/GoTypeManager.java:639-646` shows `getTypeUnchecked` catching `IOException` and returning `null`. It follows that source does not support treating every low-level IOException as the pass's first fatal event; only one that propagates past local handling reaches the relevant outer boundary.

4. **The logged EOF shape is source-defined.** `ghidra/app/util/bin/MemoryByteProvider.java:289-313` throws `EOFException("Invalid index: …")` when the unsigned start index is outside bounds and `EOFException("Unable to read past EOF: …, …")` when the requested range exceeds bounds. These are read-failure shapes, not proof that a particular artifact encountered them.

## Interpretation and limits

- **Inference, high confidence from direct source control flow:** a synchronous log parser should distinguish the bootstrap marker (`Failed to read Go info`) from the in-pass marker (`Go analysis failure`). The first marker can pre-empt entry into the main pass; the latter identifies an IOException escaping a stage inside it. Do not equate either with all `ERROR` lines or with later background-task failures.
- **Observed lane evidence, not re-executed:** `corpus/knowledge/2026-10-20-r20-go1246-first-failure-forecast.md:33-53,60-72` records eight Go-failure matches, eleven silent-through-log-end cases, and objdump's later `execution_failure`; its stated scope is one Ghidra release, one REA version, Linux/amd64, and toolchain ELFs. `round-20/w1/ScoutLogFirstFailures.md:11-14,81-107,114-119` separately identifies deferred `AnalysisTaskWrapper` failures and limits `none up to N` to captured log prefixes. These are retained observations, not fresh checks here.
- **Unresolved:** S003 source alone does not establish which boundary a given carrier reached, that the logged exception was the only event in an incomplete log, predicted/observed error indices, Go binary layout, recovery quality, or analyzer success. Those require the separately retained, bounded log/receipt evidence; no target was run for this report.

## Checks and hand-off

- Scout checks performed: read the S003 registry row; read the relevant S003 archive members and the named round-20 lane references above; hashed the installed archive to check its registered identity. No tests, builds, extractors, batteries, REA runs, or source-row writes were performed.
- Parent-owned checks remain unexecuted: run the stable changed-path smoke and final suite once after integration, as specified for the round. This source finding does not ask for a separate Ghidra or carrier run.

Report: .ufo/waves/round-21/w1/ScoutSourceGhidra.md
