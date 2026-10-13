<!-- corpus entry — kaidoku-shokunin round 4 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r4/11-managed-unlock.md. -->

# kaidoku-r4 / 11 — Managed-assembly unlock retest

Re-test of the r1 managed gate (`13-managed-asm.md`, `06-pe-cross.md`): does
`inspect_managed_artifact` reject AnyCPU, and is managed-IL analysis reachable
on this host at all? Short answer: **reachable** — via pip-installed pure-Python
dnfile+dncil, and partially via rea itself (the r1 rejection claim was imprecise).

## Candidate: dnfile + dncil pip venv — full IL analysis, zero compiler needed
- claim: `python3 -m venv /tmp/dnfenv && /tmp/dnfenv/bin/pip install dnfile dncil`
  succeeds on this host (dnfile 0.18.0, dncil latest). dnfile parses full CLI
  metadata (Mono.Cecil.dll: Machine 0x14c, 343 TypeDef rows, 3019 MethodDef rows);
  dncil disassembles every method body — 2914/2914 non-empty bodies decoded on
  Mono.Cecil.dll into real CIL (`ldarg.0`, `newobj token(0x0A00002F)`, `ret`).
  The only glue is a ~15-line `CilMethodBodyReaderBase` subclass implementing
  `read/tell/seek` over `dnPE.get_data(rva, n)` (CilMethodBody takes an RVA
  reader, not bytes — `AttributeError: 'bytes' object has no attribute
  'read_uint8'` if fed raw bytes or io.BytesIO). Works on every managed dll
  including the 0xfd1d-marked ones rea refuses; parses framework assemblies,
  Pinta assemblies, anything.
- source: `/tmp/dnfenv/bin/pip install dnfile dncil` → `dnfile OK 0.18.0`;
  `/tmp/dnfenv/lib/python3.14/site-packages/dncil/cil/body/reader.py` (ABC at
  line 25, `read_uint8` used at `body/__init__.py:81`); live decode run
  `methods tried: 2914 decoded: 2914`.
- verify: `/tmp/dnfenv/bin/python -c "import dnfile,dncil"` then
  `dnfile.dnPE('<dll>').net.mdtables.MethodDef.rows` and the reader shim above.
- verified-at: 2026-10-13
- suggested: admit — this is the cheapest unlock: pure Python, no SDK/compiler/
  fetched binary, unbounded by any size budget. Recommended as the lane's
  managed-IL substrate for all further work.

## Candidate: inspect-managed-artifact gate is machine-allowlist, not AnyCPU-reject
- claim: r1's "rejects AnyCPU" is imprecise. `npx -y rea-agents@6.4.0
  inspect-managed-artifact` SUCCEEDS on machine 0x014c (i386-marked AnyCPU PE32 —
  all 36 pinta dlls incl. Mono.Cecil.dll, exit 0, full PE+CLI header evidence)
  and on 0x8664 (x64: verified by patching `/tmp/corelib-8664.dll`'s COFF
  Machine 0xfd1d→0x8664 — tool then parses PE32+ header, `cli.flags: 12`,
  runtime_version "2.5"). It rejects only the nonstandard 0xfd1d machine value
  (.NET's PE32+ pure-IL AnyCPU64 marker, `file` reports "Unknown processor
  0xfd1d"): `error code: target_unavailable / unsupported PE architecture`,
  retryable false.
- source: `npx -y rea-agents@6.4.0 inspect-managed-artifact
  /usr/lib/pinta/Mono.Cecil.dll` → evidence ev_573dc…, machine 332/0x014c;
  same on `/tmp/corelib-8664.dll` → architecture x86_64, full parse; same on
  unpatched System.Private.CoreLib.dll → typed refusal.
- verify: `npx -y rea-agents@6.4.0 inspect-managed-artifact <dll>`; to test the
  x64 path: `python3 -c "import struct; b=bytearray(open(f,'rb').read());
  struct.pack_into('<H',b,struct.unpack_from('<I',b,0x3c)[0]+4,0x8664);
  open(o,'wb').write(b)"` on a copy (patching changes sha256/evidence identity —
  triage workaround only, never on the artifact under analysis).
- verified-at: 2026-10-13
- suggested: admit — identity/PE-header inspection is usable on all 196
  i386-marked managed dlls (incl. every Pinta assembly); the 181 0xfd1d
  framework dlls need the machine-field patch on a copy or the dnfile path.

## Candidate: host managed corpus contains ZERO natively-arch'd assemblies
- claim: whole-host census (usr/share/dotnet, usr/lib/pinta, usr/lib/mono,
  /opt, ~depth-8 home scan) finds exactly two COFF Machine flavors among
  managed dlls: 196 × Intel i386 (0x14c, AnyCPU PE32) and 181 × 0xfd1d
  (AnyCPU64 PE32+, incl. System.Private.CoreLib). No 0x8664/arm64/native-arch
  managed dll exists on the box, so "find a non-AnyCPU managed dll and feed the
  gate" is impossible without byte-patching a copy.
- source: `find /usr/share/dotnet /usr/lib/pinta /usr/lib/mono /opt /home/vgpnk
  -maxdepth 8 \( -name '*.dll' -o -name '*.exe' \) | file | grep 'Mono/.Net'`
  → `196 Intel i386`, `181 Unknown processor 0xfd1d`; dnfile Machine census
  corroborates r1 `06-pe-cross.md:21`.
- verify: the find+file pipeline above.
- verified-at: 2026-10-13
- suggested: admit — bounds the rea-artifact path precisely: usable as-is on
  the i386-marked half of the corpus (all Pinta + ~half of framework).

## Candidate: inspect-managed-members works, but hits a hardcoded 64 MiB decode budget
- claim: `inspect-managed-members` and `inspect-managed-native-boundaries` are
  NOT broken — they return `metadata.status: complete` with full
  `table_row_counts` (Module/TypeRef/TypeDef/Field/MethodDef/…) on smaller
  assemblies (freetype2-2.0.dll, 13 824 B). On larger ones they emit
  `coverage.state: unavailable` with issue
  `resource-limit, metadata.representation, "Managed metadata exceeds the
  67108864 byte representation budget"`. The budget is hardcoded
  `MAX_METADATA_REPRESENTATION_BYTES = 64*1024*1024` in the shipped JS
  (`ManagedDecodeBudget.js:4`), charged at 256 B/row + ~6 B/string byte
  (`reserve`, `reserveString`, `metadataRowCursor` in
  `ManagedMetadataHeaps.js:149,88`). Pinta sweep: all 22 dlls ≤ 204 800 B pass;
  all 14 dlls ≥ 220 160 B fail (Pinta.Effects 220 160 passes, Pango-1.0 220 160
  fails — limit tracks member/heap volume, not raw bytes). No CLI flag or param
  raises it (`--help` shows only output-filter options). rea-agents 6.4.0 IS
  the latest npm version (`npm view rea-agents versions` → 6.4.0 max).
- source: 36-dll sweep `for f in /usr/lib/pinta/*.dll; do npx -y rea-agents@6.4.0
  inspect-managed-members "$f" | grep -c resource-limit; done` (results above);
  `rea-agents/dist/dotnet/ManagedDecodeBudget.js:4-18`;
  `ManagedMetadataHeaps.js:77-94,149`;
  `npx rea-agents@6.4.0 inspect-managed-native-boundaries
  /usr/lib/pinta/freetype2-2.0.dll` → `metadata.status: complete`.
- verify: rerun the sweep; `grep -n 'MAX_METADATA_REPRESENTATION_BYTES'
  ~/.npm/_npx/*/node_modules/rea-agents/dist/dotnet/ManagedDecodeBudget.js`.
- verified-at: 2026-10-13
- suggested: admit — rea managed verbs are evidence-grade for small
  assemblies (< ~205 KB); for large ones (Pinta.Core, Gtk-4.0, Roslyn,
  CoreLib) use dnfile+dncil. Treat the 64 MiB limit as fixed provider policy
  in 6.4.0; retest on version bumps.

## Candidate: Mono.Cecil under dotnet — confirmed dead end on this host
- claim: `/usr/lib/pinta/Mono.Cecil.dll` exists (with Rocks/Mdb/Pdb siblings)
  but is a library — no entry point, so `dotnet Mono.Cecil.dll` cannot run it;
  no .NET SDK is installed (`dotnet --list-sdks` empty, `dotnet tool list -g`
  → exit 155 "No .NET SDKs were found"), so no `dotnet tool install`, no
  `dotnet-script`, no `csi`; no `mono`/`monodis`/`ikdasm`/`ilasm`/`pwsh`/`csc`/
  `mcs` on PATH. Pinta also ships Microsoft.CodeAnalysis.CSharp.dll (Roslyn)
  but it too needs a host exe. The only Cecil-based unlock remains r1's
  documented move: drop in a *precompiled* reader — e.g. an ilspycmd/published
  single-file tool — which CAN run under the installed 9.0.19/10.0.11 runtimes
  via `dotnet tool.dll`. With dnfile working, that move is unnecessary.
- source: `command -v ilspycmd monodis ikdasm mono csi pwsh csc mcs` → all
  absent; `dotnet --list-sdks` → runtimes only (9.0.19, 10.0.11);
  `find / -name 'Mono.Cecil.dll'` → `/usr/lib/pinta/Mono.Cecil.dll` only;
  `file` → `PE32 … Intel i386 Mono/.Net assembly`.
- verify: commands above; r1 `13-managed-asm.md:28` corroborates.
- verified-at: 2026-10-13
- suggested: admit as non-viable — record as superseded by the dnfile unlock;
  a precompiled reader stays the fallback if a managed-side (reflection-load)
  lane ever needs it.

## Run log
- `dotnet --list-sdks` → empty; `--list-runtimes` → Microsoft.NETCore.App
  9.0.19 + 10.0.11; `dotnet tool list -g` → exit 155 no SDK.
- `command -v ilspycmd monodis ikdasm ildasm csc mcs mono pwsh csi` → none;
  only `/usr/bin/dotnet`.
- `find / -name 'Mono.Cecil.dll'` → `/usr/lib/pinta/Mono.Cecil.dll` (only hit).
- `python3 -m venv /tmp/dnfenv`; `pip install dnfile` → OK 0.18.0;
  `pip install dncil` → OK. Neither dnfile nor pefile was preinstalled.
- dnfile on Mono.Cecil.dll → Machine 0x14c, 343 TypeDefs, 3019 MethodDefs.
- dncil attempts: raw bytes → `no attribute 'tell'`; io.BytesIO →
  `no attribute 'read_uint8'`; `CilMethodBodyReaderBase` RVA shim over
  `pe.get_data` → 2914/2914 bodies decoded.
- `file`/`dnfile` machine census of all managed dlls on host → 196 × 0x14c,
  181 × 0xfd1d, zero other machine values.
- `npx -y rea-agents@6.4.0 inspect-managed-artifact` on Mono.Cecil (0x14c) →
  full evidence; on System.Private.CoreLib (0xfd1d) → `target_unavailable /
  unsupported PE architecture`; on /tmp copy patched to 0x8664 → full evidence
  as x86_64.
- 36-dll `inspect-managed-members` sweep → 22 pass (≤ 204 800 B), 14 fail
  (≥ 220 160 B) with `resource-limit metadata.representation` (64 MiB budget,
  `ManagedDecodeBudget.js:4`); `inspect-managed-native-boundaries` on
  freetype2-2.0.dll → `metadata.status: complete` + full table_row_counts.
- `npm view rea-agents versions` → 6.4.0 is latest; source greps ran against
  `~/.npm/_npx/af752b90495482d7/node_modules/rea-agents/dist/dotnet/`.
- Scratch artifacts: `/tmp/dnfenv` venv, `/tmp/corelib-8664.dll` patched copy
  (non-corpus, disposable).

## Summary
Managed-IL analysis on this host is **reachable**, cheapest path =
`pip install dnfile dncil` into a throwaway venv (already proven at
`/tmp/dnfenv`): full metadata + CIL disassembly of every managed dll,
including the 181 0xfd1d assemblies rea refuses outright and the 14 large
assemblies that overflow rea's hardcoded 64 MiB decode budget. The rea gate
itself was mis-characterized in r1: `inspect-managed-artifact` accepts
i386-AnyCPU (all Pinta dlls) and x64, rejecting only the 0xfd1d PE32+
marker — byte-patchable on a copy when header identity suffices — while
`inspect-managed-members`/`inspect-managed-native-boundaries` are fully
functional on assemblies under roughly 205 KB. The Mono.Cecil/dotnet path
remains a dead end (library without entry point, no SDK/compiler/script host)
and is now unnecessary. Verdict: managed IL = REACHABLE via dnfile+dncil;
rea managed verbs = usable-but-bounded complement, not the unlock.
