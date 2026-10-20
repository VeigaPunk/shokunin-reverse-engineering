<!-- corpus entry — kaidoku-shokunin round 1 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r1/06-pe-cross.md. Each candidate's `suggested:` field is its curation verdict; `reject` rows are retained calibration entries. -->

# 06 — PE / Cross-Format Surface (kaidoku-r1, lane probe)

Probe scope: PE binaries on a Linux host, wine presence, toolchain reach, Ghidra
viability. All commands READ-ONLY. Observed facts and inferred claims are
separated per candidate.

## Candidate: PE corpus already ships on this Linux host (413 files, no wine needed to obtain samples)
- claim: `find /usr /opt ~ -maxdepth 6 \( -name '*.exe' -o -name '*.dll' \)` returns 413 PE files on this host — a PE RE corpus exists locally without downloading anything (OBSERVED).
- source: `find /usr /opt ~ -maxdepth 6 \( -name '*.exe' -o -name '*.dll' \) 2>/dev/null | wc -l` → 413
- verify: `find /usr /opt ~ -maxdepth 6 \( -name '*.exe' -o -name '*.dll' \) 2>/dev/null | wc -l`
- verified-at: 2026-10-13
- suggested: admit — directly observed count; corpus sources identified below.

## Candidate: Native multi-arch PE samples exist locally (x86-32, x86-64, ARM64)
- claim: Godot 4.7.2 Windows export templates + setuptools launchers provide real native PE32+ binaries across three ISAs — 12 Godot exes (x86_32/x86_64/arm64 × debug/release × console/GUI) and 8 setuptools exes (cli/gui × 32/64/arm64) (OBSERVED via file(1)).
- source: `/home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/windows_release_x86_64.exe` → "PE32+ executable for MS Windows 5.02 (GUI), x86-64 (stripped to external PDB), 12 sections"; `windows_release_arm64.exe` → "PE32+ ... ARM64, 8 sections"; `~/.cache/uv/archive-v0/M1E0QXq07p7Gx3Fp/setuptools/cli-64.exe` → "PE32+ ... x86-64, 6 sections"
- verify: `file ~/.local/share/godot/export_templates/4.7.2.stable/*.exe ~/.cache/uv/archive-v0/*/setuptools/*.exe`
- verified-at: 2026-10-13
- suggested: admit — `file` output observed for all three arches; good cross-format corpus anchors (one PDB-stripped binary noted).

## Candidate: .NET managed assemblies are PE32+ with machine 0xfd1d (AnyCPU pure-IL)
- claim: `/usr/share/dotnet/shared/Microsoft.NETCore.App/9.0.19/*.dll` are PE32+ images whose COFF Machine field is 0xfd1d, reported by file(1) as "Mono/.Net assembly" — i.e., IL-only AnyCPU managed PE, a distinct sub-format from native PE (OBSERVED).
- source: `file /usr/share/dotnet/shared/Microsoft.NETCore.App/9.0.19/System.Console.dll` → "PE32+ executable for MS Windows 4.00 (DLL), Unknown processor 0xfd1d Mono/.Net assembly, 3 sections"
- verify: `file /usr/share/dotnet/shared/Microsoft.NETCore.App/9.0.19/System.Console.dll`
- verified-at: 2026-10-13
- suggested: admit — observed; 0xfd1d = ECMA pure-IL machine marker is doc-backed (ECMA-335 §II.25.2.2 — marked INFERRED-doc, not re-derived locally).

## Candidate: readelf refuses PE input (wrong-magic error, exit 1)
- claim: GNU `readelf -h` on a PE file fails with `readelf: Error: Not an ELF file - it has the wrong magic bytes at the start` and exit status 1 — readelf is ELF-only and cannot serve the PE surface (OBSERVED on both a managed .dll and a native .exe).
- source: `readelf -h /usr/share/dotnet/shared/Microsoft.NETCore.App/9.0.19/System.Console.dll` and `readelf -h ~/.local/share/godot/export_templates/4.7.2.stable/windows_release_x86_64.exe` — identical error, `EXIT:1` both times
- verify: `readelf -h /usr/share/dotnet/shared/Microsoft.NETCore.App/9.0.19/System.Console.dll; echo $?`
- verified-at: 2026-10-13
- suggested: admit — exact stderr captured; falsifiable by re-running.

## Candidate: objdump and llvm-readobj cover the PE surface without wine
- claim: installed binutils `objdump -f` parses both native (`pei-x86-64`, start address 0x140001470 for Godot) and managed PE; `llvm-readobj --file-headers` decodes COFF headers including ARM64 (`IMAGE_FILE_MACHINE_ARM64 0xAA64`) — GNU/LLVM toolchains already on PATH handle PE statically (OBSERVED).
- source: `objdump -f windows_release_x86_64.exe` → "file format pei-x86-64 / architecture: i386:x86-64 / start address 0x0000000140001470"; `llvm-readobj --file-headers cli-64.exe` → "Format: COFF-x86-64, Machine: IMAGE_FILE_MACHINE_AMD64 (0x8664), SectionCount: 6"; ARM64 template → "Format: COFF-ARM64"
- verify: `objdump -f ~/.local/share/godot/export_templates/4.7.2.stable/windows_release_x86_64.exe; llvm-readobj --file-headers ~/.cache/uv/archive-v0/*/setuptools/cli-64.exe | head -20`
- verified-at: 2026-10-13
- suggested: admit — observed output for x86-64 and ARM64; managed-dll objdump reports pei-x86-64 but with machine-agnostic start 0x0 (its IL-ness needs a CLI-aware reader — noted boundary, not a regression).

## Candidate: wine is absent — no native-PE execution path via wine on this host
- claim: wine/wine64 are not on PATH and `pacman -Q wine` reports "error: package 'wine' was not found" — no wine-based execution or wine-coupled tooling (e.g., wine-hosted disassemblers) is available (OBSERVED absence; absence of other native-PE emulators is INFERRED — qemu-user/box86/hangover not checked).
- source: `which wine wine64` → not found in PATH listing; `pacman -Q wine` → package not found
- verify: `which wine wine64; pacman -Q wine`
- verified-at: 2026-10-13
- suggested: admit — for the stated scope (wine absence). Alternative emulators unprobed → keep the wider claim out of scope.

## Candidate: Ghidra 12.1.4 is installed locally and its PE import path is wine-independent Java
- claim: Ghidra 12.1.4 PUBLIC exists at `~/.local/opt/ghidra_12.1.4_PUBLIC` with `support/analyzeHeadless` present, OpenJDK 21.0.12.1 is installed, and `ghidra/app/util/opinion/PeLoader.class` ships inside `Ghidra/Features/Base/lib/Base.jar` — the PE loader is pure-Java Ghidra code, so PE import cannot depend on wine (OBSERVED: install, loader class, JVM. INFERRED: an actual import succeeds — `analyzeHeadless` was not run because it writes project files; probe scope is READ-ONLY).
- source: `ls ~/.local/opt/ghidra_12.1.4_PUBLIC/` (ghidraRun, support/, Ghidra/); `unzip -l .../Base.jar | grep PeLoader` → `PeLoader.class` (39,640 bytes, dated 2026-09-21); `java -version` → openjdk 21.0.12.1
- verify: `ls ~/.local/opt/ghidra_12.1.4_PUBLIC/support/analyzeHeadless; unzip -l ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base.jar | grep 'opinion/PeLoader.class'; java -version`
- verified-at: 2026-10-13
- suggested: admit — every locally checkable premise is observed; only the end-to-end import run is marked inferred. Honest residual risk: Ghidra version/config quirks are possible but no mechanism for a wine dependency exists in a pure-Java loader.

## Candidate: Execution axis splits by PE subtype — managed runnable, native static-only
- claim: managed PE assemblies have a local executor (`dotnet` — runtimes Microsoft.NETCore.App 9.0.19 AND 10.0.11 installed), while native PE has none (wine absent, mono absent) — dynamic RE of native PE is unavailable; static-only (OBSERVED for presence/absence; INFERRED that `dotnet <managed.dll>` executes correctly — not exercised, and these are library assemblies without entry points).
- source: `dotnet --list-runtimes` → "Microsoft.NETCore.App 9.0.19" + "10.0.11"; `which mono` → MISSING; wine absent (above)
- verify: `dotnet --list-runtimes; which mono wine`
- verified-at: 2026-10-13
- suggested: admit — presence/absence observed; execution claim kept as inference per probe honesty.

## Candidate: PE RE tooling gaps — radare2, rizin, mono tools, pedump all absent
- claim: `rabin2`, `r2`, `radare2`, `rz-bin`, `mono`, `monodis`, `pedump`, `xxd` are all missing from PATH — the local PE toolset is binutils + LLVM + Ghidra + file/strings only (OBSERVED).
- source: `command -v` sweep over 17 tools → present: objdump, readelf, llvm-readobj, llvm-objdump, dotnet, strings, python3, java; missing: rabin2, r2, radare2, rz-bin, mono, monodis, pedump, xxd
- verify: `for t in rabin2 r2 radare2 rz-bin mono monodis pedump; do command -v $t || echo "$t MISSING"; done`
- verified-at: 2026-10-13
- suggested: admit — observed PATH sweep; a tool could exist outside PATH (unlikely for CLI RE tools; marked minor residual).

## Summary
413 PE files already on this Linux host (multi-arch native + managed .NET); wine absent so native PE is static-only, but objdump, llvm-readobj, and a local Ghidra 12.1.4 (pure-Java PeLoader, wine-independent by construction — end-to-end import inferred, not run under READ-ONLY scope) cover the surface.

## Errata (round 2)

- "Ghidra PE import inferred" is now PROVEN: `rea analyze` on
  `setuptools/cli-64.exe` (sha256 `bbb3de57…`, 14,336 B) → 8 segments,
  142 procedures, decompile of `entry` via Ghidra 12.1.4 — pure-Java PeLoader,
  wine-independent. See `2026-10-13-r2-pe-e2e-proof`. (round 2)

## Round-20 erratum (append-only; 2026-10-20)

The candidate "PE RE tooling gaps — radare2, rizin, mono tools, pedump all absent" is a 2026-10-13 observation and is now
**stale**: re-running its own sweep on 2026-10-20 (`for t in rabin2 r2 radare2 rz-bin rizin xxd; do command -v $t; done`)
resolves `rabin2`, `r2`, `radare2`, `rz-bin`, `rizin` and `xxd` under `/usr/bin` (rizin 0.8.2). REA's
`execute-rizin-command` is now held on this PE (`corpus/knowledge/2026-10-20-r20-rizin-command-observation.md`). The
original text above stays as the historical record; mono/monodis/pedump were not re-checked.
