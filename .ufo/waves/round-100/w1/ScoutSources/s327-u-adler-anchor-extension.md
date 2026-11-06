# Recommendation: extend S327 anchor for the `u_adler` check (no new row)

## Finding

The `u_adler` check after decompression lives in the **same file S327 already pins**:
`src/packhead.cpp`, in `ph_decompress` itself, immediately after `upx_decompress`:

- `packhead.cpp:352` — `// verify checksum of decompressed data`
- `:353` — `if (verify_checksum) {`
- `:354-355` — `if (ft) ft->unfilter(out, ph.u_len);`
- `:356` — `unsigned adler = upx_adler32(raw_bytes(out, ph.u_len), ph.u_len, ph.saved_u_adler);`
- `:357` — `if (adler != ph.u_adler)`
- `:358` — `throwChecksumError();`

So `ph_decompress` guards both directions: c_adler over compressed bytes **before**
decompression (`:335-338`) and u_adler over decompressed bytes **after** it (`:353-358`).

## Recommendation

Do NOT open a new registry row for this (duplicate source file = the F-dup forgery
shape the C2 controls police). Instead extend S327's `anchor` cell with `352-358` and
the phrase "verify checksum of decompressed data" so the u_adler half of
`ph_decompress` is citable.

## Why the PE refusal lands on c_adler (335-338), not u_adler (353-358)

- `src/packer.h:144` — `void decompress(..., bool verify_checksum = true, ...)`.
- `src/packer.cpp:306-308` — `Packer::decompress` forwards straight to `ph_decompress(ph, in, out, verify_checksum, ft)`.
- `src/pefile.cpp:3053` — seek lands at `isection[1].rawdataptr - 64 + ph.buf_offset + ph.getPackHeaderSize()`; `:3058` reads exactly `ph.c_len` compressed bytes and calls `decompress(ibuf, obuf)`.
- Corruption of any compressed payload byte at intact length fails the c_adler compare at `:337` and throws at `:338` **before** any decompression happens; u_adler is only reachable for bytes that survive the c_adler test.

## Corroborating u_adler sites (read, not admitted; see rejection-notes.md)

- `src/p_unix.cpp:723-725` — `if (ph.c_adler != c_adler || ph.u_adler != u_adler) throwChecksumError();` (unix formats, accumulated over extents).
- `src/p_lx_elf.cpp:8085-8086` and `:9330-9331` — same comparison in ELF shlib unpack paths.
- `src/p_lx_interp.cpp:305-306` — same in interp path.
- `src/packer.cpp:266-269` — overlapping-decompression verification raises `throwInternalError("decompression failed (checksum error)")`, an internal-error variant, not the user-facing refusal.
