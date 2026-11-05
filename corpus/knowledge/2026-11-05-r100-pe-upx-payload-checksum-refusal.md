# A UPX-packed PE whose compressed data was altered at intact length is refused by the packer's own Adler-32 test, not answered `ok intact` (round 100, R100-C1)

source: S327 — UPX v5.2.0 `src/packhead.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packhead.cpp — opened 2026-11-05, 13236 bytes, sha256 `41b4a51ba4d78429241e2c970565402287fd79360445013f955e2b4cf137f37a` (copy `.ufo/waves/round-100/pre/s327-packhead-v5.2.0.cpp`); lines 334-338, `ph_decompress`: "unsigned adler = upx_adler32(raw_bytes(in, ph.c_len), ph.c_len, ph.saved_c_adler); if (adler != ph.c_adler) throwChecksumError();"; lines 220-221: for formats below 128 `u_adler = get_le32(p + 8); c_adler = get_le32(p + 12);`; lines 94-101: the header is 32 bytes for version >= 10 and a non-DOS format. Grounds the refusal condition and the field offsets.
source: S324 — UPX v5.2.0 `src/pefile.cpp` (opened round 98); line 3053, `PeFile::unpack0`: "fi->seek(isection[1].rawdataptr - 64 + ph.buf_offset + ph.getPackHeaderSize(), SEEK_SET);" then `readx(ibuf, ph.c_len)` and `decompress(ibuf, obuf)` — the compressed data starts right after the PackHeader.
source: S326 — UPX v5.2.0 `src/packer.cpp` (opened round 99); line 495: `ph.u_adler = ph.c_adler = ph.saved_u_adler = ph.saved_c_adler = upx_adler32(nullptr, 0);` — the checksum seed is the Adler-32 initial value, so Python's `zlib.adler32(data)` computes the same number (measured equal on all ten pinned packs, every one header version 13: `.ufo/waves/round-100/l1/adler-equality.txt`, `equal 10 of 10`).
verified-at: 2026-11-05 (round 100; measured revision and receipt in SCORECARD `## 2026-11-05 — round 100`)
recheck: on-release — the counting command below, re-run when UPX or a pinned carrier changes.

## The class

[observation] A UPX 5.2.0 `--best` win32/pe or win64/pep pack (exe or DLL) with one byte of its
compressed data changed — file length, section table, PackHeader and its own checksum byte all
intact — fails `upx -t` with `Exception: checksum error`. On the ten carriers pinned in
`tools/round-100/pe-upx-corrupt-battery.py`, one byte at a run-time random offset inside
`[PackHeader + 32, PackHeader + 32 + c_len)` XORed with a random nonzero value, untampered and with
both round-98 tampers applied, two cells each: `upx -t` failed on 40 of 40 inputs.

[observation] The round-99 repair (`tools/round-99/upx-pe-repair.py`) answers `ok intact`, exit 0,
on every such untampered input and "repairs" every tampered one (`corrupt 0 of 40` at the freeze,
`.ufo/waves/round-100/pre/c1-r99-upx-pe-repair-at-freeze.json`); at round start four random flips
in a `t32.exe` pack gave `ok intact` rc 0 four times against `upx -t` rc 1. Its exit 0 did not imply
that the packer would decompress the output (round-99 frontier note: "payload corruption at intact
length" still Frontier).

[observation] The PackHeader's own checksum byte (byte 31, sum of bytes 4..30 mod 251) covers the
header only; it validates after a payload flip, which is why the round-98/99 anchor search still
finds the header and why a header-checksum test cannot see this class.

## Rule (`tools/round-100/upx-pe-repair.py`)

1. Round-99 steps unchanged: PE section table, `FileAlignment == 0` → `filealign-zero`, file shorter
   than the aligned end of the last section → `truncated`, exactly one checksum-valid PackHeader
   (version 10..14, format 9 or 36) in the `canUnpack0` windows.
2. Read `c_adler` (bytes 12..15) and `c_len` (bytes 20..23), little-endian, from that header. The
   compressed data is `[ph + 32, ph + 32 + c_len)`. If it runs past the end of the file → refuse
   `truncated: compressed data ends at …`.
3. `zlib.adler32(compressed data) != c_adler` → refuse `checksum: adler32 of compressed data … !=
   c_adler …`, rc 2, nothing written. The tool never decompresses and never runs the packer.
4. Otherwise the round-98 repair (magic, `UPX0`/`UPX1`, third section name) as before.

The order matters for one case: a pack that is both tampered and corrupted is refused `checksum`
rather than "repaired" into a file that `upx -t` would still reject.

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

The `exec` leg runs every candidate invocation under `strace -f -qq -e trace=execve,execveat` and
fails on any exec beyond the interpreter's own. It answers the round-99 limit that an `os` alias
evades the static text screen (CriticC2 fg/fg3): h6 passes every other arm and the static screen,
and only the exec leg refuses it.

## Limits

- A corruption that also rewrites `c_adler` to match the altered bytes (and fixes the header's own
  checksum byte) passes this rule; UPX then fails later on `u_adler` after decompression, which this
  tool cannot compute without the NRV/LZMA codec. Frontier.
- Header versions below 10 and DOS/big-endian formats (other field offsets and header sizes,
  packhead.cpp 85-101, 220-251) are outside the rule; the tool only accepts PE formats 9 and 36 with
  versions 10..14.
- Measured on the ten pinned carriers; carriers outside that set rest on the round-100 wave's
  held-out run (`corpus/lessons/round-100.md`), not on the frozen battery.
- The `exec` leg sees exec calls only: a candidate that reads a pre-built oracle file or a cache
  built outside the run is not caught by it.
