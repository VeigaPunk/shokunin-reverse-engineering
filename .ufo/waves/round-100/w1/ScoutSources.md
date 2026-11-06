# ScoutSources — round 100, source re-grounding for S327 and frontier search (2026-11-05)

Seat: ScoutSources (scout). Lane: kaidoku, freeze F = 8e24c29a37ca81a0bd1ff5ec73c96a949885322e.
All commands below were run by this seat; scratch `/fast/scratch/hyaku/kaidoku-r100/ScoutSources`
(trap-deleted at end; all cited copies live in the wave dir first). No tool installs were needed;
none made. No lane files touched outside `.ufo/waves/round-100/w1/ScoutSources*`.

## Item 1 — S327 re-grounding: CONFIRMED verbatim

- `curl -fsSL https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packhead.cpp` exit 0;
  `sha256sum` → `41b4a51ba4d78429241e2c970565402287fd79360445013f955e2b4cf137f37a` — equals the
  claimed hash and equals lane copy `.ufo/waves/round-100/pre/s327-packhead-v5.2.0.cpp`
  (byte-identical; release tarball `upx-5.2.0-src.tar.xz` copy identical as well).
- Lines 332-338: `ph_decompress(...)` — `:334` comment "verify checksum of compressed data",
  `:335` `if (verify_checksum) {`, `:336` `unsigned adler = upx_adler32(raw_bytes(in, ph.c_len), ph.c_len, ph.saved_c_adler);`,
  `:337` `if (adler != ph.c_adler)`, `:338` `throwChecksumError();` — the claimed 334-338 span is exact.
- `decodePackHeaderFromBuf` (`:189`): `:219 if (format < 128) { :220 u_adler = get_le32(p + 8); :221 c_adler = get_le32(p + 12); }` — c_adler at p+12 for format < 128 confirmed.
- `getPackHeaderSize` (`:81-104`): version >= 10 non-DOS formats → 32; supports "compressed data
  starts right after the 32-byte PackHeader", with `pefile.cpp:3053` seek
  `isection[1].rawdataptr - 64 + ph.buf_offset + ph.getPackHeaderSize()` and `:3057` reading exactly `ph.c_len`.

## Item 2 — `upx_adler32` == standard Adler-32 (seed 1): ESTABLISHED, draft row written

Chain (all lines read in fetched v5.2.0 sources):
1. `src/conf.h:871` — `unsigned upx_adler32(const void *buf, unsigned len, unsigned adler = 1);` (seed default 1).
2. `src/compress/compress.cpp:35-46` — `#if 1` → `return upx_ucl_adler32(buf, len, adler);` (`:40`); zlib variant `:42`/`compress_zlib.cpp:231-235` is `#if 0` UNUSED.
3. `src/compress/compress_ucl.cpp:266-268` — `return ucl_adler32(adler, (const ucl_bytep) buf, len);`
4. `vendor/ucl/src/ucl_util.c:135-163` — `s1 = adler & 0xffff`, `s2 = (adler >> 16) & 0xffff`, `s1 += *buf++; s2 += s1;`, `s1 %= UCL_BASE; s2 %= UCL_BASE;`, return `(s2 << 16) | s1`; `:124` `#define UCL_BASE 65521u`, `:125` `#define UCL_NMAX 5552`.
5. `src/check/dt_check.cpp:1152-1156` — self-test asserts `upx_adler32(d, 4) == 0x09f003f7` (seed 1) and `0x09ec03f6` (seed 0) on `d = ff fe fd fc` (pinned by adjacent `get_be32` static_asserts).

Executed cross-check (exit 0): `zlib.adler32(b'\xff\xfe\xfd\xfc', 1) == 0x09f003f7` → True;
`zlib.adler32(b'\xff\xfe\xfd\xfc', 0) == 0x09ec03f6` → True; hand-rolled mod-65521 loop matches both.
Conclusion: the PackHeader c_adler/u_adler checksums are ordinary seeded Adler-32, not a bespoke hash.

Draft NEW row (11 columns, id S328 proposed, scribe assigns; corpus/SOURCES.md NOT edited):
`.ufo/waves/round-100/w1/ScoutSources/draft-row-upx-adler32.md`. Source cell = compress.cpp raw URL
(7331 bytes, sha256 `485c0317106dc93630f08b05a396e5f21d5ce10d66df714539d261747b69022d`, byte-identical
in release tarball sha256 `af99e526d5759de94412aea1104d5e4ca406cb725295f8633ecc9e843dc1ce1c`);
located quote `assert_noexcept(upx_adler32(d, 4) == 0x09f003f7);`; no `|` inside cells.

## Item 3 — u_adler after decompression and `--force` behaviour

u_adler primary source: `packhead.cpp:352-358` — after `upx_decompress`, `:356`
`unsigned adler = upx_adler32(raw_bytes(out, ph.u_len), ph.u_len, ph.saved_u_adler);`, `:357-358`
compare + `throwChecksumError()`. Same file S327 already pins → recommended as an S327 anchor
extension, NOT a new row (F-dup shape): `s327-u-adler-anchor-extension.md`.

Why the C1 refusal lands on c_adler first: `packer.h:144` `verify_checksum = true` default;
`packer.cpp:306-308` `Packer::decompress` forwards to `ph_decompress`; PE path reads `ph.c_len`
bytes and throws at `:338` before any decompression, so u_adler (`:358`) is unreachable for
payload corruption at intact length.

`--force`: exhaustive call-site inspection (`grep -rn "opt->force"` and all `throwChecksumError`
sites) finds NO force guard at packhead.cpp:338/:358, p_lx_elf.cpp:8086/:9331, p_lx_interp.cpp:306,
p_unix.cpp:725. All `opt->force` uses near checksums are pack-time `throwCantPack(... "(try --force)")`
gates (pefile.cpp:389/:465/:2343). Doc agrees: `doc/upx-doc.txt:776-780` — "Force compression even
when there is an unexpected value in a header field." Implication: `--force` does not bypass unpack
checksum refusal in 5.2.0; no force carve-out is needed in C1 reasoning.

## Search log and rejection notes

- `search-log.md`: four questions, files identified/opened, included/rejected, stop rationale.
- `rejection-notes.md`: ten entries — packhead.cpp (dup of S327), p_unix.cpp:723-725,
  p_lx_elf.cpp:8085/:9330, p_lx_interp.cpp:305 (format-scope corroborators), packer.cpp:266-269
  (internal-error variant), compress_zlib.cpp (dead `#if 0` wrapper), main.cpp:368 (parse only),
  pefile.cpp force sites (pack-side), doc/upx-doc.txt (redundant docs tier), ucl_util.c
  (submodule provenance; folded into the draft row instead).

## Supporting files (all under `.ufo/waves/round-100/w1/ScoutSources/`)

- `draft-row-upx-adler32.md`, `s327-u-adler-anchor-extension.md`, `rejection-notes.md`, `search-log.md`
- Pinned copies: `compress-v5.2.0.cpp` (sha256 `485c0317...b69022d`), `conf-v5.2.0.h`
  (sha256 `ffdaa719...b48962b`), `ucl_util.c` (sha256 `8e5db622...89d07755`, from release tarball).

## Verdict

S327's anchors are exact and its pinned copy byte-identical upstream; `upx_adler32` is standard
Adler-32 seeded at 1 (draft row S328 proposed); the u_adler refusal at `packhead.cpp:352-358` is
best admitted as an S327 anchor extension; `--force` never bypasses unpack checksum refusal in
v5.2.0. Findings: 6.
