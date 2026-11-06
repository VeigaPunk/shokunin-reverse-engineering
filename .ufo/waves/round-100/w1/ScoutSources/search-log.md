# Search log — ScoutSources, 2026-11-05 (round 100, source re-grounding)

Repo revision context: lane freeze F = 8e24c29a37ca81a0bd1ff5ec73c96a949885322e; this
seat read only the frozen wave fixtures (`pre/s327-packhead-v5.2.0.cpp`) and upstream
v5.2.0 sources; no lane tree mutation. Every command below was run this seat.

## Q1. Does v5.2.0 packhead.cpp hold the c_adler test at 334-338 with throwChecksumError, and read c_adler at p+12 for format < 128?

- Files identified: raw `src/packhead.cpp` (tag v5.2.0); lane copy
  `.ufo/waves/round-100/pre/s327-packhead-v5.2.0.cpp`; release tarball copy.
- Opened: raw fetch (`curl -fsSL .../v5.2.0/src/packhead.cpp`, exit 0);
  `sha256sum` both copies → `41b4a51ba4d78429241e2c970565402287fd79360445013f955e2b4cf137f37a`,
  byte-identical; release tarball's `src/packhead.cpp` identical too.
- Read: lines 88-104 (`getPackHeaderSize`: version >= 10 non-DOS formats → 32),
  189-232 (`decodePackHeaderFromBuf`: `:219 if (format < 128) { :220 u_adler = get_le32(p + 8); :221 c_adler = get_le32(p + 12);`),
  332-360 (`ph_decompress`: c_adler test `:336-338`, u_adler test `:356-358`).
- Included: S327 re-confirmed verbatim; claim's line anchors 334-338 and p+12 are
  exact. Stop rationale: anchor byte-identical to the lane's pinned copy; nothing
  further to resolve.

## Q2. Is `upx_adler32` standard Adler-32 with seed 1?

- Files identified: `src/conf.h` (declaration), `src/compress/compress.cpp`,
  `src/compress/compress_ucl.cpp`, `src/compress/compress_zlib.cpp`,
  `src/check/dt_check.cpp`, `vendor/ucl/src/ucl_util.c` (release tarball).
- Opened: all of the above (raw fetches for conf.h and compress.cpp; tarball for the
  rest). conf.h:871 default `adler = 1`; compress.cpp:35-46 delegates `#if 1` to
  `upx_ucl_adler32`; compress_ucl.cpp:266-268 → `ucl_adler32`; ucl_util.c:135-163
  standard split/mod-65521 loop (`UCL_BASE 65521u` at :124, `UCL_NMAX 5552` at :125);
  dt_check.cpp:1152-1156 self-test constants 0x09f003f7 (seed 1) and 0x09ec03f6
  (seed 0) over bytes ff fe fd fc.
- Executed check: reference `zlib.adler32` and a hand-rolled mod-65521 loop both
  reproduce 0x09f003f7 / 0x09ec03f6 for those bytes (exit 0).
- Included: NEW row draft `draft-row-upx-adler32.md` (source cell = compress.cpp raw
  URL; ucl_util.c and dt_check cited in anchor/scope). Stop rationale: equality is
  established by UPX's own pinned self-test constants plus the located arithmetic;
  fetching the UCL submodule git history would add nothing.

## Q3. Primary source for the `u_adler` check after decompression?

- Files identified: `grep -rn "u_adler"` over v5.2.0 src (29+ hits); opened
  packhead.cpp 340-360, p_unix.cpp 715-730, p_lx_elf.cpp (hits at 8085/9330),
  p_lx_interp.cpp (305), packer.cpp (166-169, 252, 268, 306-308), pefile.cpp
  (`grep -n adler` → no matches).
- Included: packhead.cpp:352-358 is the primary source (same file as S327);
  recommended as an S327 anchor extension, NOT a new row
  (`s327-u-adler-anchor-extension.md`). Corroborators (p_unix, p_lx_elf,
  p_lx_interp, packer.cpp:268) recorded as rejections 2-5.
- Stop rationale: PE path fully traced (packer.h:144 default true → packer.cpp
  306-308 → ph_decompress); further format-specific sites cannot outrank the shared
  path already pinned by S327.

## Q4. Primary source on `--force` unpack behaviour with checksum errors?

- Files identified: `grep -rn "opt->force"` over src (25+ hits);
  `doc/upx-doc.txt` force entries; all six `throwChecksumError` call sites.
- Opened: main.cpp:368 (parse), pefile.cpp:389/465/2217/2343/2347 (pack-side
  `throwCantPack(... (try --force))` gates), doc/upx-doc.txt:776-780.
- Finding: NO `opt->force` guard exists at any of the six `throwChecksumError` call
  sites (packhead.cpp:338, :358; p_lx_elf.cpp:8086, :9331; p_lx_interp.cpp:306;
  p_unix.cpp:725). `--force` relaxes pack-time suspicious-input refusals and is
  documented as compression-side. Implication for C1: a corrupted payload is refused
  at ph_decompress regardless of `--force`; the battery's `exec`/`refused` arms need
  no force-exception carve-out.
- Included: recorded in the report and rejection notes 7-9; no row (doc text
  redundant with source; force sites teach pack-side behaviour outside C1 scope).
- Stop rationale: question answered by exhaustive call-site inspection; no web
  sources needed.

## Not opened (identified, skipped, with reason)

- UPX web docs/HTML manual, GitHub issue tracker, blog posts on UPX checksums:
  skipped — all four questions resolved from pinned v5.2.0 sources; non-pinned
  secondary sources would be weaker than what is already in hand.
- `vendor/zlib/adler32.c` (release tarball): skipped — the zlib wrapper is `#if 0`
  dead code in 5.2.0; the live path is UCL.
