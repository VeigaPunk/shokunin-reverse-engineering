<!-- corpus entry — kaidoku-shokunin round 1 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r1/07-ghidra-install.md. Each candidate's `suggested:` field is its curation verdict; `reject` rows are retained calibration entries. -->

# Ghidra Install Inventory — ~/.local/opt/ghidra_12.1.4_PUBLIC (READ ONLY)

Round-1 curation, kaidoku-shokunin lane. All evidence gathered read-only on 2026-10-13.

## Candidate: Ghidra 12.1.4 PUBLIC is installed and version-pinned
- claim: The install is Ghidra 12.1.4, PUBLIC release, built 2026-Sep-21 16:13 UTC, git revision 8b6bbb857accdfa20dc5b2f5dea471178c2e9fbc; requires Java >= 21 and supports Python 3.9–3.14.
- source: ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/application.properties (application.version=12.1.4, application.release.name=PUBLIC, application.build.date=2026-Sep-21 1613 UTC, application.java.min=21, application.python.supported=3.14, 3.13, 3.12, 3.11, 3.10, 3.9)
- verify: grep -E 'application\.(version|release\.name|build\.date|revision\.ghidra|java\.min)' ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/application.properties
- verified-at: 2026-10-13
- suggested: admit — authoritative version evidence direct from the install's own properties file; note the file lives at Ghidra/application.properties, NOT the install root.

## Candidate: Standard Ghidra distribution top-level layout
- claim: The install root contains the standard distribution layout: Ghidra/ (framework+features+processors), support/ (launchers incl. analyzeHeadless), server/ (ghidraSvr, svrAdmin, svrInstall, jaas.conf), Extensions/ (Eclipse, Ghidra, IDAPro subdirs), docs/, GPL/, licenses/, docker/, ghidraRun launcher, bom.json (157 KB SBOM), GettingStarted.{html,md}, LICENSE; total footprint ~876 MB.
- source: ls -la ~/.local/opt/ghidra_12.1.4_PUBLIC/ ; du -sh (876M)
- verify: ls ~/.local/opt/ghidra_12.1.4_PUBLIC/ && du -sh ~/.local/opt/ghidra_12.1.4_PUBLIC
- verified-at: 2026-10-13
- suggested: admit — complete, unmodified-looking distribution tree including server components and SBOM; nothing missing for headless or GUI use.

## Candidate: Headless analyzer entrypoint present at support/analyzeHeadless
- claim: support/analyzeHeadless is an executable Bourne-Again shell script (the canonical batch-mode entrypoint); it defaults MAXMEM to 2G (overridable via GHIDRA_MAXMEM / GHIDRA_HEADLESS_MAXMEM), sets -Djava.awt.headless=true with ParallelGCThreads=2 / CICompilerCount=2 for parallel headless instances, and launches in fg mode. analyzeHeadlessREADME.{html,md} ship alongside.
- source: file + head of ~/.local/opt/ghidra_12.1.4_PUBLIC/support/analyzeHeadless
- verify: file ~/.local/opt/ghidra_12.1.4_PUBLIC/support/analyzeHeadless && grep -nE 'MAXMEM_DEFAULT|LAUNCH_MODE|headless' ~/.local/opt/ghidra_12.1.4_PUBLIC/support/analyzeHeadless | head
- verified-at: 2026-10-13
- suggested: admit — the documented headless RE pipeline entrypoint exists and is tuned for many parallel instances; usage: analyzeHeadless <projdir> <projname> -import <binary> [-postScript ...].

## Candidate: 39 processor/language modules; x86, ARM, and AARCH64 all present
- claim: Ghidra/Processors contains 39 modules: 6502, 68000, 8048, 8051, 8085, AARCH64, ARM, Atmel, BPF, CP1600, CR16, Dalvik, DATA, eBPF, HCS08, HCS12, Hexagon, JVM, Loongarch, M16C, M8C, MC6800, MCS96, MIPS, NDS32, PA-RISC, PIC, PowerPC, RISCV, Sparc, SuperH, SuperH4, TI_MSP430, Toy, tricore, V850, x86, Xtensa, Z80. x86 ships compiled specs x86.sla + x86-64.sla plus .sinc sources for ISA extensions (avx, avx2, avx512, bmi1/2, sha, sgx, etc.); ARM ships ARM4–ARM8 LE/BE .sla/.slaspec; AARCH64 ships AARCH64.sla, AARCH64BE.sla, AARCH64_AppleSilicon.sla plus SVE/PAC .sinc.
- source: ls ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Processors/ (39 entries); ls of x86/, ARM/, AARCH64/ data/languages/
- verify: ls ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Processors/ | wc -l && ls ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Processors/x86/data/languages/*.sla
- verified-at: 2026-10-13
- suggested: admit — broad architecture coverage confirmed with compiled .sla language specs already built (no sleigh compile step needed for common targets).

## Candidate: Native decompiler binary is a Linux x86-64 ELF at Ghidra/Features/Decompiler/os/linux_x86_64/decompile
- claim: The decompiler's native engine is Ghidra/Features/Decompiler/os/linux_x86_64/decompile — ELF 64-bit LSB executable, x86-64, dynamically linked, not stripped, 3,434,376 bytes; a sibling sleigh binary (1,009,168 bytes) ships in the same dir; only linux_x86_64 and win_x86_64 OS dirs exist under Decompiler/os/ (no macOS arm64/x86_64 natives).
- source: file + ls -la ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Decompiler/os/linux_x86_64/ ; ls of parent os/
- verify: file ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Decompiler/os/linux_x86_64/decompile && ls ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Decompiler/os/
- verified-at: 2026-10-13
- suggested: admit — decompiler capability is native-compiled for this host's arch and directly invocable for standalone decompile/sleigh use or via the headless analyzer.

## Candidate: Host Java satisfies Ghidra's runtime requirement
- claim: /usr/bin/java is OpenJDK 21.0.12.1 (64-Bit Server VM), satisfying application.java.min=21 declared in application.properties — the install is runnable on this host without a JDK change.
- source: java -version; which java; Ghidra/application.properties
- verify: java -version 2>&1 | head -1 && grep application.java.min ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/application.properties
- verified-at: 2026-10-13
- suggested: admit — version constraint met exactly at the floor (21); no max bound declared (application.java.max empty).

## Candidate: 35 feature modules ship, including BSim, PDB, PyGhidra, FunctionID, VersionTracking
- claim: Ghidra/Features contains 35 modules: Base, BSim, BSimFeatureVisualizer, BytePatterns, ByteViewer, CodeCompare, DataGraph, DebugUtils, Decompiler, DecompilerDependent, FileFormats, FunctionGraph, FunctionGraphDecompilerExtension, FunctionID, GhidraGo, GhidraServer, GnuDemangler, GraphFunctionCalls, GraphServices, MicrosoftCodeAnalyzer, MicrosoftDemangler, MicrosoftDmang, PDB, ProgramDiff, ProgramGraph, PyGhidra, Recognizers, Sarif, SourceCodeLookup, SwiftDemangler, SystemEmulation, VersionTracking, VersionTrackingBSim, WildcardAssembler.
- source: ls ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/
- verify: ls ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/ | wc -l
- verified-at: 2026-10-13
- suggested: admit — full feature set including PyGhidra (scripting bridge) and BSim (function similarity) available for REA pipelines.

## Candidate: Auxiliary tooling in support/ extends beyond headless analysis
- claim: support/ also ships bsim/bsim_ctl (similarity DB), GhidraGo (Go-based launch helper), pyghidraRun, jshellRun, sleigh (standalone SLEIGH compiler CLI), convertStorage, ghidraClean, ghidraDebug, buildGhidraJar, and launch.sh/LaunchSupport.jar — a complete CLI toolchain alongside the GUI ghidraRun.
- source: ls ~/.local/opt/ghidra_12.1.4_PUBLIC/support/
- verify: ls ~/.local/opt/ghidra_12.1.4_PUBLIC/support/
- verified-at: 2026-10-13
- suggested: admit — pyghidraRun + sleigh CLI give scriptable RE paths that bypass the Java-heavy analyzer when needed.

## Summary
Ghidra 12.1.4 PUBLIC (build 2026-09-21, rev 8b6bbb85) is fully installed at ~/.local/opt/ghidra_12.1.4_PUBLIC (876M): headless entrypoint support/analyzeHeadless ready, 39 processor modules with compiled x86/ARM/AARCH64 specs, native Linux x86-64 decompiler+sleigh binaries, 35 features incl. PyGhidra/BSim, and host OpenJDK 21 satisfies the Java>=21 floor — all candidates recommended admit.

## Errata (round 2)

- Feature module count is **34, not 35** (audit-B re-ran `ls Ghidra/Features | wc -l`;
  the enumerated list in the claim is complete — the count digit was off by one).
