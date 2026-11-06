# Rejection notes — sources opened but not admitted as NEW rows (ScoutSources, 2026-11-05)

Rule applied: a NEW row needs a distinct pinned primary source teaching something the
existing registry (S324, S326, S327) does not already cover; duplicate-source rows are
an anti-pattern policed by the C2 F-dup control. Every file below was actually opened
in fetched v5.2.0 sources this seat.

1. `src/packhead.cpp` (raw fetch, sha256 `41b4a5...f37a`) — already admitted as S327.
   REJECTED as a NEW row: duplicate source. Used instead for the anchor-extension
   recommendation in `s327-u-adler-anchor-extension.md` (u_adler test at 352-358).
2. `src/p_unix.cpp:723-725` — final `c_adler`/`u_adler` comparison with
   `throwChecksumError()` after extent-wise unpack. REJECTED: unix (ELF/ps1/tos)
   formats, not the C1 PE carrier; teaches nothing S327 + packer.cpp:306-308 do not
   already cover; corroborates only.
3. `src/p_lx_elf.cpp:8085-8086`, `:9330-9331` — same comparison in ELF shlib unpack.
   REJECTED: out of C1 format scope; corroborates only.
4. `src/p_lx_interp.cpp:305-306` — same comparison in interp path. REJECTED: same
   reason as (3).
5. `src/packer.cpp:266-269` — u_adler mismatch raises
   `throwInternalError("decompression failed (checksum error)")` during overlapping
   decompression verification. REJECTED: internal-error variant on a compress-side
   verification path, not the unpack refusal the battery observes.
6. `src/compress/compress_zlib.cpp:231-235` — `upx_zlib_adler32` wraps zlib `adler32`.
   REJECTED: the wrapper is `#if 0` UNUSED; `compress.cpp:40` (`#if 1`) routes to the
   UCL variant. Admitting it would misattribute the live arithmetic.
7. `src/main.cpp:368` — `opt->force++` option parsing. REJECTED: no checksum
   semantics; evidence value nil beyond showing `--force` exists.
8. `src/pefile.cpp:389`, `:465`, `:2217`, `:2343`, `:2347` — `opt->force` gates
   pack-time suspicious-input refusals (`throwCantPack(... "(try --force)")`,
   `needForceOption()`), plus a FORCE_INTEGRITY flag removal. REJECTED as rows: these
   are compression-side gates; none touches unpack checksum refusal. Recorded as
   evidence for the `--force` question below.
9. `doc/upx-doc.txt:776-780` — `--force` documented as "Force compression even when
   there is an unexpected value in a header field." REJECTED: docs-tier restatement of
   what the source shows (no force guard at any `throwChecksumError` call site:
   packhead.cpp 338/358, p_lx_elf.cpp 8086/9331, p_lx_interp.cpp 306, p_unix.cpp 725);
   weaker tier, redundant. Corroboration only.
10. `vendor/ucl/src/ucl_util.c` — admitted INTO the `upx_adler32` draft row as the
    arithmetic (mod 65521) but REJECTED as a standalone row: it is a submodule file
    (absent from the tag archive; only present in the release tarball), and UPX's own
    `dt_check.cpp:1154-1156` self-test constants already pin the semantics from the
    UPX side with cleaner provenance.
