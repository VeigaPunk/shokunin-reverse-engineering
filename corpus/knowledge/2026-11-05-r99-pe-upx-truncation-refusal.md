# A UPX-packed PE cut inside its sections is refused by the packer's own overlay arithmetic, not answered `ok intact` (round 99, R99-C2)

source: S326 — UPX v5.2.0 `src/packer.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packer.cpp — opened 2026-11-05, 44586 bytes, sha256 `ab274d672d0985fa92d83e8c9c867d62ff30a1f31d2fb0b919e6d8826b03e040` (copy `.ufo/waves/round-99/pre/s326-packer-v5.2.0.cpp`); lines 431-433: "void Packer::checkOverlay(unsigned overlay) { if ((int) overlay < 0 || overlay > file_size_u) throw OverlayException("invalid overlay size; file is possibly corrupt");"; grounds the refusal condition.
source: S324 — UPX v5.2.0 `src/pefile.cpp` (opened round 98, re-read round 99); lines 3046-3049, `PeFile::unpack0`: "const unsigned overlay = file_size_u - ALIGN_UP(isection[iobjs - 1].rawdataptr + isection[iobjs - 1].size, ih.filealign); checkOverlay(overlay);"; lines 3042-3043: a zero `filealign` throws "unexpected value in the PE header".
verified-at: 2026-11-05 (round 99; measured revision and receipt in SCORECARD `## 2026-11-05 — round 99`)
recheck: on-release — the counting command below, re-run when UPX or a pinned carrier changes.

## The class

[observation] A UPX 5.2.0 `--best` win32/pe or win64/pep pack (exe or DLL) whose file ends before
the aligned end of its last section — `ALIGN_UP(rawdataptr + SizeOfRawData, FileAlignment)` of the
last section header — fails `upx -t` and `upx -d` with `OverlayException: invalid overlay size;
file is possibly corrupt`. On ten pinned carriers, cut one byte short of that end and at the middle
of `UPX1`'s raw data, untampered and with both round-98 tampers applied, `upx -t` failed on 40 of 40
cuts (`effective`, receipt below).

[observation] The round-98 repair (`tools/round-98/upx-pe-repair.py`) answers `ok intact`, exit 0,
on all 40 cut inputs that keep the PackHeader window (`truncated 0 of 40` at the freeze,
`.ufo/waves/round-99/pre/c2-r98-upx-pe-repair-at-freeze.json`): its exit 0 did not imply that the
packer would accept the output (round-98 closure, routed defect 4).

[observation] A file LONGER than that end carries an overlay, which UPX copies: appending 1–4096
random bytes to a pack keeps `upx -t` green and `upx -d` carries the bytes through (20 of 20 overlay
cells). The 3.3 MB `lib7-Zip-JBinding.dll` (Ghidra) ships a 2.2 MB overlay of its own; cutting into
that overlay only is not truncation.

## Rule (`tools/round-99/upx-pe-repair.py`)

1. Parse the PE section table (as round 98). Read `FileAlignment` (optional header offset 36, both
   PE32 and PE32+). `FileAlignment == 0` → refuse `filealign-zero` (the packer's own refusal).
2. `end = ALIGN_UP(last.rawdataptr + last.SizeOfRawData, FileAlignment)` over the **last section
   header in table order** (the packer's `isection[iobjs - 1]`). If the file is shorter than `end`
   → refuse `truncated: file N bytes < aligned end of last section M`, rc 2, nothing written.
3. Otherwise apply the round-98 repair rule unchanged (checksum-validated, unique PackHeader in the
   `canUnpack0` windows; `UPX0`/`UPX1` names restored).
4. CLI envelope: an unreadable `--in`, an `--out` that is a directory or whose directory is
   missing, and a failed write are typed refusals (rc 2, no traceback, no temporary left); the
   output is written through `mkstemp` in the output directory, so a stale `<out>.tmp-<pid>` cannot
   collide.

## Measured

| arm (counter `tools/round-99/pe-upx-trunc-battery.py`) | round-98 repair at freeze | round-99 repair at landing |
|---|---|---|
| recovered (10 carriers × magic/names/both) | 30 of 30 | 30 of 30 |
| decoy (checksum-invalid look-alike at the window start) | 9 of 9 | 9 of 9 |
| intact | 10 of 10 | 10 of 10 |
| overlay (runtime-random length) | 20 of 20 | 20 of 20 |
| truncated (2 cuts × untampered/both) | 0 of 40 | 40 of 40 |
| refused (not UPX) | 2 of 2 | 2 of 2 |
| cli (missing input, missing output dir, output is a dir) | 0 of 3 (rc 1 tracebacks) | 3 of 3 |
| static (no process spawning / dynamic import in the source) | 1 of 1 | 1 of 1 |

Landing receipt: `.ufo/waves/round-99/l1/scores/c2-at-01c4b79cc1cf8e6172b507edebb6a4d3125c5c6f.json`
(exit 0). Command: `python3 -I -B tools/round-99/pe-upx-trunc-battery.py --root . --repair
tools/round-99/upx-pe-repair.py --rev <rev> --work <scratch> --json-out <receipt>`.

Red fixtures scored at the freeze, each exit 1 (`.ufo/waves/round-99/pre/c2-controls-at-freeze.txt`):
identity copy; refuse-all (`intact 0`); truncation-only, no repair (`recovered 0`); fixed offset 992
(`recovered 27`: the DLL whose PackHeader sits at 517); size-keyed cache of every pinned pack
(`overlay 10`: the random overlay changes the size); lazy anchor without checksum (`decoy 0`);
over-refusal of any overlay (`overlay 0`); the packer called as the tool's own oracle (`static 0`).

## Population

Carriers (sha256-pinned in the counter): the six round-98 carriers and four DLLs —
`freeglut32.vc14.dll` (python-opengl, win32, `.rsrc`), `gle64.vc9.dll` (win64, `UPX2`),
`llio_i386.dll` (Ghidra, win32, `UPX2`), `lib7-Zip-JBinding.dll` (Ghidra, win64, `UPX2`,
FileAlignment 0x200, PackHeader at offset **517**, own overlay). Every other pack in the set has
its PackHeader at 992.

## Limits

- Only truncation is decided. A pack whose bytes are corrupted but whose length is intact is not
  detected by this rule (the round-98 co-tamper of `dd[1].RVA`, SentinelInputs, still passes
  both the repair and `upx -t`).
- One packer version (5.2.0), `--best` only; PE only (Mach-O stays Frontier).
- The decoy arm covers 9 carriers: on `lib7-Zip-JBinding.dll` the window start lies inside the
  section table, where writing a look-alike would corrupt the header.
- The static leg is a text screen for spawning and dynamic import, not a sandbox.
- The candidate was drafted and dry-run once before the freeze commit (disclosed in
  `plans/round-99-claims.md`); the landed score reads the committed bytes through `git show`.
