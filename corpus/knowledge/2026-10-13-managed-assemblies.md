<!-- corpus entry — kaidoku-shokunin round 1 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r1/13-managed-asm.md. Each candidate's `suggested:` field is its curation verdict; `reject` rows are retained calibration entries. -->

# kaidoku-r1 / 13 — Managed assemblies surface (.NET / Mono)

Round-1 read-only survey of managed (CLR / PE-CIL) artifacts and managed-code
tooling on this Linux host.

## Candidate: .NET host + two shared runtimes installed; no SDK, no Mono
- claim: `/usr/bin/dotnet` (symlink → `/usr/share/dotnet/dotnet`) is a working .NET host v10.0.11 (RID `arch-x64`) with shared runtimes Microsoft.NETCore.App 9.0.19 and 10.0.11 installed via pacman (`dotnet-host`, `dotnet-runtime-9.0`, `dotnet-runtime-10.0`); `dotnet --list-sdks` returns none and `dotnet tool` fails with "No .NET SDKs were found"; no `mono`, `monodis`, `pedump`, `ilasm`, `csc`, `mcs`, or `pwsh` exists on PATH and `/usr/lib/mono` does not exist.
- source: `which dotnet mono ilspycmd ilasm monodis ildasm csc mcs pwsh`; `dotnet --info`; `dotnet --list-sdks`; `pacman -Q | grep -iE 'dotnet|mono'`; `ls /usr/lib/mono`
- verify: `dotnet --info && dotnet --list-sdks; which mono monodis ilspycmd ildasm csc mcs pwsh; ls /usr/lib/mono 2>&1`
- verified-at: 2026-10-13
- suggested: admit — runtime present means managed apps execute and can be exercised dynamically, but the absence of SDK/compiler/Mono means the classical .NET RE toolchain path is partially blocked.

## Candidate: ~341 managed framework DLLs under /usr/share/dotnet/shared
- claim: `Microsoft.NETCore.App/10.0.11` contains 172 `*.dll` and `9.0.19` contains 169 `*.dll` — the canonical framework assemblies (System.*, Microsoft.*, netstandard, mscorlib facade); all are managed reference assemblies, deterministic-versioned RE targets with public documentation.
- source: `find /usr/share/dotnet/shared/Microsoft.NETCore.App/{10.0.11,9.0.19} -name '*.dll' | wc -l` → 172 / 169
- verify: `find /usr/share/dotnet/shared -name '*.dll' | wc -l; file /usr/share/dotnet/shared/Microsoft.NETCore.App/10.0.11/System.Private.CoreLib.dll`
- verified-at: 2026-10-13
- suggested: admit — large, stable managed corpus; framework IL is also the baseline for validating any future decompiler brought to the box.

## Candidate: Pinta 3.1.2 — 36 verified managed DLLs at /usr/lib/pinta
- claim: every one of the 36 `*.dll` files under `/usr/lib/pinta` is `file`-verified as "PE32 executable … Mono/.Net assembly"; the app is framework-dependent on `net10.0` (`Pinta.runtimeconfig.json` TFM `net10.0`, `Pinta.deps.json` runtimeTarget `.NETCoreApp,Version=v10.0`), installed via pacman `pinta 3.1.2-2`; corpus spans app assemblies (Pinta.Core/Effects/Tools/Gui.*), GirCore Gtk4 bindings (Gtk-4.0, Adw-1, Gsk-4.0 …), Mono.Addins plugin framework, Microsoft.CodeAnalysis (Roslyn), ICSharpCode.SharpZipLib, NGettext, System.CommandLine, Tmds.DBus.
- source: `for dll in /usr/lib/pinta/*.dll; do file "$dll" | grep 'Mono/.Net assembly'; done` → 36 hits; `pacman -Qo /usr/lib/pinta/Pinta.dll`; `/usr/lib/pinta/Pinta.{runtimeconfig,deps}.json`
- verify: `file /usr/lib/pinta/Pinta.dll; find /usr/lib/pinta -name '*.dll' | wc -l; cat /usr/lib/pinta/Pinta.runtimeconfig.json`
- verified-at: 2026-10-13
- suggested: admit — the only third-party managed application on the host; an ideal real-world RE target with mixed app-code + binding-layer + plugin architecture.

## Candidate: Mono.Cecil.dll on disk — an assembly-reading substrate without a decompiler
- claim: `/usr/lib/pinta/Mono.Cecil.dll` (plus `Mono.Cecil.Rocks/Mdb/Pdb`) is present as a Pinta dependency; Cecil is the same library ilspy/monodis-class tools use for metadata+IL access, so a managed-assembly introspection capability technically exists on the box — but with no SDK, no `csc`, no `dotnet-script`/`csi`, nothing on the host can compile a Cecil harness (a precompiled one could still run via `dotnet <tool>.dll` against the 10.0 runtime).
- source: `ls /usr/lib/pinta/Mono.Cecil*`; `dotnet tool list --global` → SDK-required error; `which csi dotnet-script` → absent
- verify: `file /usr/lib/pinta/Mono.Cecil.dll; dotnet tool list --global 2>&1 | grep 'No .NET SDKs'`
- verified-at: 2026-10-13
- suggested: admit — honest tooling-gap record: reader library present, compiler absent; defines the cheapest future enablement move (drop in a precompiled Cecil/ilspy binary, no SDK needed).

## Candidate: No dedicated decompiler/disassembler tooling installed
- claim: neither `ilspycmd`, `ildasm`/`ilasm`, `monodis`, `dnSpy`, `avalonia-ilspy`, nor any `dotnet tool` is installed; `~/.dotnet/tools` and `~/.nuget/packages` do not exist; managed-assembly analysis is limited to `file`/`strings` triage plus runtime reflection (`dotnet` executing a managed binary, e.g. `dotnet /usr/lib/pinta/Pinta.dll`, is possible since runtimes exist).
- source: `which ilspycmd ildasm ilasm monodis`; `ls ~/.dotnet/tools ~/.nuget/packages` → absent; `dotnet tool list --global` → "No .NET SDKs were found"
- verify: `which ilspycmd ildasm ilasm monodis dnSpy; ls -d ~/.dotnet/tools ~/.nuget/packages 2>&1`
- verified-at: 2026-10-13
- suggested: admit — tooling-absent frontier record; constrains managed RE to triage + execution + a future precompiled-reader lane.

## Candidate: All other *.exe / *.dll on the host are native PE — not managed
- claim: of 21 `*.exe` under `~/ /opt /usr/lib` (depth ≤6) and 51 `*.dll` under `/usr/lib /opt` (depth ≤5), every non-pinta, non-dotnet-shared artifact is native: `DBZMON.exe` and Godot 4.7.2 export templates are stripped PE32+ native; setuptools `cli/gui*.exe` (uv cache) are PE32 native launchers; `/usr/lib/nvidia/wine/nvngx.dll` and PyOpenGL `freeglut*.dll` are native Windows DLLs; `/opt` (1Password, claude-code, containerd, intel, spotify) contains zero `*.dll`/`*.exe` at depth ≤8; no flatpak .NET apps found.
- source: `find ~ /opt /usr/lib -maxdepth 6 -name '*.exe'` → 21; `find /usr/lib /opt -maxdepth 5 -name '*.dll'` → 51; `file` on representative artifacts; `find /opt -maxdepth 8 -name '*.dll'` → 0; `flatpak list --app` → none
- verify: `file /home/vgpnk/Projects/gamez/dbzmon/builds/windows/DBZMON.exe; find /opt -maxdepth 8 -name '*.dll' -o -name '*.exe' | wc -l`
- verified-at: 2026-10-13
- suggested: admit — bounds the managed surface precisely: managed corpus = Pinta (36) + framework shared runtimes (~341) and nothing else; all executable/game artifacts belong to the native-PE lane.

## Summary
Managed surface is real but narrow: a working `dotnet` host (runtimes 9.0.19 + 10.0.11, no SDK), ~341 framework DLLs, and exactly one managed application (Pinta 3.1.2, 36 Cecil-readable assemblies, incl. Mono.Cecil itself); no Mono, no decompiler, no NuGet cache — all remaining PE artifacts are native, so managed RE here means triage + runtime execution + a future precompiled-reader path.
