# A UPX-packed PE whose compressed data was altered at intact length is refused by the packer's own Adler-32 test, not answered `ok intact` (round 100, R100-C1)

source: S327 — UPX v5.2.0 `src/packhead.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packhead.cpp — opened 2026-11-05, 13236 bytes, sha256 `41b4a51ba4d78429241e2c970565402287fd79360445013f955e2b4cf137f37a` (copy `.ufo/waves/round-100/pre/s327-packhead-v5.2.0.cpp`); lines 334-338, `ph_decompress`: "unsigned adler = upx_adler32(raw_bytes(in, ph.c_len), ph.c_len, ph.saved_c_adler); if (adler != ph.c_adler) throwChecksumError();"; lines 220-221: for formats below 128 `u_adler = get_le32(p + 8); c_adler = get_le32(p + 12);`; lines 94-101: the header is 32 bytes for version >= 10 and a non-DOS format. Grounds the refusal condition and the field offsets.
source: S324 — UPX v5.2.0 `src/pefile.cpp` (opened round 98); lines 3053-3054, `PeFile::unpack0`: "fi->seek(isection[1].rawdataptr - 64 + ph.buf_offset + ph.getPackHeaderSize(), SEEK_SET);" followed by "fi->readx(ibuf, ibufgood = ph.c_len);" — the compressed data starts right after the PackHeader and is exactly `c_len` bytes long.
source: S326 — UPX v5.2.0 `src/packer.cpp` (opened round 99); line 495: `ph.u_adler = ph.c_adler = ph.saved_u_adler = ph.saved_c_adler = upx_adler32(nullptr, 0);` and line 252: `ph.c_adler = upx_adler32(raw_bytes(o_ptr, ph.c_len), ph.c_len, ph.c_adler);` — the compressed-data checksum is Adler-32 seeded with 1, so Python's `zlib.adler32(data)` (default seed 1) computes the same number. Measured equal on all ten pinned packs, every one header version 13, `equal 10 of 10` (`.ufo/waves/round-100/l1/adler-equality.txt`; re-measured independently by this seat, seed 1 equal on 10 of 10 and seed 0 unequal on 10 of 10).
source: S328 — UPX v5.2.0 `src/check/dt_check.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/check/dt_check.cpp — opened 2026-11-05, 61985 bytes, sha256 `83f97d79d4e9f3eb11718c788addac1fcc43d943ee900e88ea7995a03f0c74fe` (copy `.ufo/waves/round-100/pre/s328-dt_check-v5.2.0.cpp`); lines 1154-1156: "assert_noexcept(upx_adler32(d, 4) == 0x09f003f7);" / "assert_noexcept(upx_adler32(d, 4, 0) == 0x09ec03f6);" / "assert_noexcept(upx_adler32(d, 4, 1) == 0x09f003f7);" over the bytes `ff fe fd fc`. Grounds that the packer's checksum is standard Adler-32 with seed 1, so a Python tool recomputes it exactly (cross-check `.ufo/waves/round-100/pre/s328-zlib-crosscheck.txt`; re-measured by this seat).
verified-at: 2026-11-05 (round 100; measured revision and receipt in SCORECARD `## 2026-11-05 — round 100`)
recheck: on-release — the counting command below, re-run when UPX or a pinned carrier changes.

[observation] The identity of UPX's `upx_adler32` with standard RFC-1950 Adler-32 is grounded by
S328: Python reproduces both of the packer's own self-test values exactly —
`zlib.adler32(bytes([0xff,0xfe,0xfd,0xfc]))` = `0x9f003f7` and with seed 0 `0x9ec03f6`
(re-measured by this seat). The measurable consequence is independent of that row: the packer's
stored `c_adler` equals Python's `zlib.adler32(data)` with the default seed 1 on 10 of 10 pinned
packs and differs from the seed-0 value on 10 of 10.

## The class

[observation] A UPX 5.2.0 `--best` win32/pe or win64/pep pack (exe or DLL) with one byte of its
compressed data changed — file length, section table, PackHeader and the PackHeader's own checksum
byte all intact — fails `upx -t` with `Exception: checksum error` and exit 1. On the ten carriers
pinned in `tools/round-100/pe-upx-corrupt-battery.py`, one byte at a run-time random offset inside
`[PackHeader + 32, PackHeader + 32 + c_len)` XORed with a random nonzero value, untampered and with
both round-98 tampers applied, two cells each: `upx -t` failed on 40 of 40 inputs (`effective`).
The refusal message is the packer's own: on the 20 untampered-base cells it reads
`Exception: checksum error`; on the 20 cells that also carry the round-98 magic/name tamper it
reads `CantUnpackException: file is modified/hacked/protected`, because the anti-unpack gate
(S324) refuses before the compressed data is ever checksummed — the two are different refusals, and
only the first is the checksum one.

[observation] The round-99 repair (`tools/round-99/upx-pe-repair.py`) answers `ok intact`, exit 0,
on such an input, and its output is byte-identical to the corrupted input (sha256 equal, this
seat's probe); `upx -t` of that output still fails rc 1. Its exit 0 did not imply that the packer
would accept the output (round-99 frontier note: "payload corruption at intact length" still
Frontier). At the freeze the round-99 repair scored `corrupt 0 of 40` against the round-100 battery
(`.ufo/waves/round-100/pre/c1-r99-upx-pe-repair-at-freeze.json`).

[observation] The PackHeader's own checksum byte (byte 31, sum of bytes 4..30 mod 251) covers the
header only; it still validates after a payload flip, which is why the round-98/99 anchor search
still finds the header and why a header-checksum test cannot see this class.

## Rule (`tools/round-100/upx-pe-repair.py`)

1. Round-99 steps unchanged: PE section table, `FileAlignment == 0` → `filealign-zero`, file shorter
   than the aligned end of the last section → `truncated`, exactly one checksum-valid PackHeader
   (version 10..14, format 9 win32/pe or 36 win64/pep) in the `canUnpack0` windows.
2. Read `c_adler` (bytes 12..15) and `c_len` (bytes 20..23), little-endian, from that header. The
   compressed data is `[ph + 32, ph + 32 + c_len)`. If it runs past the end of the file → refuse
   `truncated: compressed data ends at …`, rc 2, nothing written.
3. `zlib.adler32(compressed data) != c_adler` → refuse `checksum: adler32 of compressed data … !=
   c_adler …`, rc 2, nothing written. The tool never decompresses and never runs the packer.
4. Otherwise the round-98 repair (magic, `UPX0`/`UPX1`, third section name) as before.

The order matters for one case: a pack that is both tampered and corrupted is refused `checksum`
rather than "repaired" into a file that `upx -t` would still reject (this seat's probe on a `t32`
pack: magic + names + one flipped payload byte → rc 2, `checksum`, no `--out`).

## Measured

Counting command (frozen at `8e24c29a37ca81a0bd1ff5ec73c96a949885322e`, `plans/round-100-claims.md`):

    python3 -I -B tools/round-100/pe-upx-corrupt-battery.py --root . --repair tools/round-100/upx-pe-repair.py --rev <rev> --work <scratch> --json-out <receipt>

| repair (read at a commit) | label | exit |
|---|---|---|
| round-99 repair, at the freeze | `… truncated 40 of 40; corrupt 0 of 40; … exec 1 of 1; effective 119 of 119` | 1 |
| h0 identity copy | `recovered 0 of 30; … corrupt 0 of 40; …` | 1 |
| h1 refuse-all | `intact 0 of 10; overlay 0 of 20; … corrupt 40 of 40` | 1 |
| h2 off-by-header window | `intact 0 of 10; …` | 1 |
| h3 `u_adler` confused for `c_adler` | `intact 0 of 10; …` | 1 |
| h4 aliased-`os` `upx -t` oracle | `corrupt 20 of 40; … exec 0 of 1` | 1 |
| h5 length test without checksum | `corrupt 0 of 40` | 1 |
| h6 candidate + one harmless aliased exec | every arm full except `exec 0 of 1` | 1 |
| round-100 repair at `a610671d7a01e1d762eb7103e6ee9f8a2be287ed` | `recovered 30 of 30; decoy 9 of 9; intact 10 of 10; overlay 20 of 20; truncated 40 of 40; corrupt 40 of 40; refused 2 of 2; cli 3 of 3; static 1 of 1; exec 1 of 1; effective 119 of 119` | 0 |

Receipts: `.ufo/waves/round-100/pre/c1-*-at-freeze.json` (transcript
`.ufo/waves/round-100/pre/c1-controls-at-freeze.txt`) and
`.ufo/waves/round-100/l1/scores/c1-at-a610671d7a01e1d762eb7103e6ee9f8a2be287ed.json`.

[observation] The `exec` leg runs every candidate invocation under `strace -f -qq -e
trace=execve,execveat` and fails on any exec beyond the interpreter's own (154 invocations, 0
violations, in the L1 receipt's `exec` cell). It answers the round-99 limit that an `os` alias
evades the static text screen (CriticC2 fg/fg3): h6 passes every other arm and the static screen,
and only the exec leg refuses it.

## Population

The ten carriers, sha256-pinned in `tools/round-100/pe-upx-corrupt-battery.py` and re-hashed by this
seat at the same paths (digests equal, 10 of 10):

| slug | absolute path | sha256 of the original |
|---|---|---|
| t32 | `/home/vgpnk/.local/share/kaidoku-pwnenv/lib/python3.11/site-packages/pip/_vendor/distlib/t32.exe` | `6b4195e640a85ac32eb6f9628822a622057df1e459df7c17a12f97aeabc9415b` |
| t64 | `/home/vgpnk/.local/share/kaidoku-pwnenv/lib/python3.11/site-packages/pip/_vendor/distlib/t64.exe` | `81a618f21cb87db9076134e70388b6e9cb7c2106739011b6a51772d22cae06b7` |
| w32 | `/home/vgpnk/.local/share/kaidoku-pwnenv/lib/python3.11/site-packages/pip/_vendor/distlib/w32.exe` | `47872cc77f8e18cf642f868f23340a468e537e64521d9a3a416c8b84384d064b` |
| w64 | `/home/vgpnk/.local/share/kaidoku-pwnenv/lib/python3.11/site-packages/pip/_vendor/distlib/w64.exe` | `7a319ffaba23a017d7b1e18ba726ba6c54c53d6446db55f92af53c279894f8ad` |
| winhello | `/opt/ghidra/docs/GhidraClass/ExerciseFiles/WinhelloCPP/WinHelloCPP.exe` | `7a98a934de5f578c3a547af873221b221d037bafa87ceee71dd4f089dd228202` |
| fastlist64 | `/home/vgpnk/.local/share/fnm/node-versions/v22.20.0/installation/lib/node_modules/pnpm/dist/vendor/fastlist-0.3.0-x64.exe` | `d1a71f9ac1728082c1b276392725c3e010b98714888579b99152e401abedbf11` |
| freeglut32dll | `/usr/lib/python3.14/site-packages/OpenGL/DLLS/freeglut32.vc14.dll` | `c9c00a4ea9b9fecdcae81f6facaf27e349714d56fe7640ce9c37ed38841a0b87` |
| gle64dll | `/usr/lib/python3.14/site-packages/OpenGL/DLLS/gle64.vc9.dll` | `b427510af633a6298481e738942f3268daedf44d6c01af74620579034bede9ce` |
| llio32dll | `/opt/ghidra/GPL/DMG/data/os/win_x86_32/llio_i386.dll` | `e855478acf0d36f846befb48bfd239b7ef46e568e2408091591adec274ed0879` |
| sevenzip64dll | `/opt/ghidra/Ghidra/Features/FileFormats/data/sevenzipnativelibs/Windows-amd64/lib7-Zip-JBinding.dll` | `c769642c8a489e8fc078b8387fb9865ac5c5482ce22301a40d00145fa1304b27` |

Six exe and four DLL; every PackHeader found is version 13; nine of the ten sit at offset 992, the
DLL `lib7-Zip-JBinding.dll` at 517 (it also carries its own overlay). Host tools:
`/usr/bin/upx` (5.2.0, sha256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`),
`/usr/bin/strace` (sha256 `28ed5493ecf611b83ac0d0398cc1c4f09a228afaa7fce4737d14c8599cc796e2`).

## Limits

- [observation] A corruption that also rewrites `c_adler` to match the altered bytes (and fixes the
  PackHeader's own checksum byte) passes this rule: the candidate answers `ok intact`, exit 0,
  while `upx -t` on the same file reports `Exception: checksum error`, exit 1 (this seat's probe P3).
  [inference] The remaining failure is the packer's second checksum, `u_adler`, over the
  decompressed data (packhead.cpp 352-358): the `c_adler` test was made to pass by the forgery, and
  both refusals raise the same message, so which of the two fired is not separable from the message
  alone. That test needs the NRV/LZMA codec, which this tool does not have. Frontier.
- Header versions below 10 and DOS/big-endian formats (other field offsets and header sizes,
  packhead.cpp 85-101, 220-251) are outside the rule; the tool only accepts PE formats 9 and 36
  with versions 10..14.
- The rule decides corruption at intact length only. A pack whose compressed data runs past the end
  of the file is refused `truncated` (round-100 addition), and the round-99 aligned-end rule still
  governs a short file; a pack with an overlay is not refused.
- Measured on the ten pinned carriers by the frozen battery. Carriers outside that set are not
  covered by the battery; the round-100 wave's held-out run
  (`.ufo/waves/round-100/w1/ExecHeldOut.md`: nine held-out PE/DLL files, 54 payload flips, 54 of 54
  refused `checksum` with `upx -t` reporting `checksum error` on each input) extends the class to
  that separate population and is not part of the frozen measurement.
- The `exec` leg sees exec calls only: a candidate that reads a pre-built oracle file or a cache
  built outside the run is not caught by it. The `static` leg is a text screen for spawning and
  dynamic import, not a sandbox.
- Whether a repaired file runs on Windows is not tested.

## Not examined

- Mach-O, ELF and every non-PE format; other UPX versions than 5.2.0; other packer versions.
- PE header versions below 10, DOS formats, and the big-endian (`format >= 128`) field layout.
- The packer's second checksum (`u_adler`, over the decompressed data) and the NRV/LZMA codec: not
  exercised, and not reachable from the tool.
- Any Windows execution, loader acceptance, or runtime behaviour of a repaired file.
- The `decoy` arm's exclusion of `lib7-Zip-JBinding.dll` (its window start lies inside the section
  table) is inherited from the round-99 battery and was not re-derived here.
- The round-99 battery (`tools/round-99/pe-upx-trunc-battery.py`) was not re-scored by this seat; the
  round-100 battery was run in full at A1 and the two controls h4 and h5 were re-scored at F. The
  remaining F controls are cited from the committed transcript
  `.ufo/waves/round-100/pre/c1-controls-at-freeze.txt`, not re-run here.
