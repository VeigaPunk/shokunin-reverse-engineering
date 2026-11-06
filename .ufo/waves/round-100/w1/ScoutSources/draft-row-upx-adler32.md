# Draft NEW row: `upx_adler32` == standard Adler-32 (seed 1)

Proposed for `corpus/SOURCES.md` registry. **Scribe assigns the id** (S327 is the highest
this seat saw referenced; suggest S328 if still free). This seat did NOT edit
corpus/SOURCES.md. One row, 11 columns, no `|` inside cells; located quote is 7 words.

## Row (single line)

```
| S328 | UPX 5.2.0 `src/compress/compress.cpp` at tag `v5.2.0` (`upx_adler32`) — https://raw.githubusercontent.com/upx/upx/v5.2.0/src/compress/compress.cpp (fetched 2026-11-05; 7331 bytes; sha256 `485c0317106dc93630f08b05a396e5f21d5ce10d66df714539d261747b69022d`; byte-identical in release tarball `upx-5.2.0-src.tar.xz` sha256 `af99e526d5759de94412aea1104d5e4ca406cb725295f8633ecc9e843dc1ce1c`; copies `.ufo/waves/round-100/w1/ScoutSources/compress-v5.2.0.cpp` and `ucl_util.c`) | code | A | The seeded checksum UPX applies to PackHeader compressed and decompressed bytes, shown equal to standard zlib Adler-32 by UPX's own self-test constants; not a bespoke hash | tag `v5.2.0`; `compress.cpp:35` definition, `:40` delegate; `conf.h:871` default `adler = 1`; `dt_check.cpp:1154-1156` self-test; located quote `assert_noexcept(upx_adler32(d, 4) == 0x09f003f7);` | The PackHeader c_adler and u_adler comparisons are standard Adler-32 seeded at 1 (bundled UCL `ucl_util.c:135-163` does the split-and-mod-65521 loop, `UCL_BASE 65521u` at `:124`), so a reference implementation reproduces the refusal condition; treat recomputed Adler values as predictable, not secret. | proposed | 2026-11-05 | on-release | round-100 C1 source re-grounding (this draft) |
```

## Evidence chain (all lines read in fetched v5.2.0 sources)

1. `src/conf.h:871` — `unsigned upx_adler32(const void *buf, unsigned len, unsigned adler = 1);` (seed default 1).
2. `src/compress/compress.cpp:35-46` — definition; `#if 1` branch returns `upx_ucl_adler32(buf, len, adler)` (`:40`); zlib variant `:42` is the `#else` branch, and `upx_zlib_adler32` is `#if 0` UNUSED in `compress_zlib.cpp:231-235`.
3. `src/compress/compress_ucl.cpp:266-268` — `return ucl_adler32(adler, (const ucl_bytep) buf, len);`
4. `vendor/ucl/src/ucl_util.c:135-163` — `ucl_adler32`: `s1 = adler & 0xffff`, `s2 = (adler >> 16) & 0xffff`, `s1 += buf[i]; s2 += s1;`, per-block `s1 %= UCL_BASE; s2 %= UCL_BASE;`, returns `(s2 << 16) | s1`; `:124` `#define UCL_BASE 65521u`, `:125` `#define UCL_NMAX 5552`. Standard RFC-1950 Adler-32.
5. `src/check/dt_check.cpp:1152-1156` — `d = dd + 7` (bytes `ff fe fd fc`, pinned by the adjacent `get_be32(d) == 0xfffefdfc` static_asserts) and self-test asserts `upx_adler32(d,4) == 0x09f003f7` (seed 1) and `== 0x09ec03f6` (seed 0).

## Executed cross-check (this seat, 2026-11-05)

- Python reference: `zlib.adler32(b'\xff\xfe\xfd\xfc', 1) == 0x09f003f7` → True; `zlib.adler32(b'\xff\xfe\xfd\xfc', 0) == 0x09ec03f6` → True. Hand-rolled `s1=(s1+b)%65521; s2=(s2+s1)%65521` loop reproduces both constants. UPX's own self-test constant therefore equals the reference standard implementation for both seeds.

## Provenance

- Raw fetch `curl -fsSL https://raw.githubusercontent.com/upx/upx/v5.2.0/src/compress/compress.cpp` exit 0, sha256 `485c0317106dc93630f08b05a396e5f21d5ce10d66df714539d261747b69022d` (7331 bytes).
- Tag archive `https://github.com/upx/upx/archive/refs/tags/v5.2.0.tar.gz` and release tarball `upx-5.2.0-src.tar.xz` (sha256 `af99e526d5759de94412aea1104d5e4ca406cb725295f8633ecc9e843dc1ce1c`) both contain byte-identical `src/compress/compress.cpp` (diff -q clean); `src/packhead.cpp` in the release tarball also matches S327's pinned sha256 `41b4a51ba4d78429241e2c970565402287fd79360445013f955e2b4cf137f37a`.
- `vendor/ucl` is an empty submodule dir in the tag archive (`.gitmodules`: `upx/upx-vendor-ucl`, branch `upx-vendor`); the arithmetic quote comes from the official release tarball above (self-contained), sha256 of `vendor/ucl/src/ucl_util.c` there: `8e5db622f5a83751a5ca7c63d69c411bcdf96cc2b805bcbf3711852589d07755`.
