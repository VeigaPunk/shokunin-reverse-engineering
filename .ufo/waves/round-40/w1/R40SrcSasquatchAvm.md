# R40SrcSasquatchAvm — where sasquatch decides AVM-BE block-length endianness

**Verdict: CONFIRMED — the AVM logic lives in S121's own file (`unsquashfs.c`) at lines S121 does not cite, plus a compile-time half in `squashfs_swap.h` / `swap.c` and the `-DFIX_BE` build in `debian/rules`. No new row; draft an S121 scope/anchor amendment (old -> new below).** No patches/ directory exists at the tag; no other file hard-codes AVM.

Seat R40SrcSasquatchAvm, wave 1, 2026-10-26. Artifacts: `.ufo/waves/round-40/w1/artifacts/R40SrcSasquatchAvm/`.

## Access record

- Tag `sasquatch-v4.5.1-6` resolves (GitHub API `git/ref/tags/...` and `commits/...`) to commit `15573bf46c671c8ed23e8c0c50e6187e0c8d0b62` — equals S121's anchor.
- Tree listing (`api.github.com/repos/onekey-sec/sasquatch/git/trees/sasquatch-v4.5.1-6?recursive=1`, `truncated:false`, 447 entries): no `patches/` path, no path containing "patch"; `squashfs-tools/` is the vendored tree; `debian/rules` is the only build-variant file.
- Fetched raw (HTTP 200 each, access UTC `2026-10-26T18:18:49Z`; `curl -sL`), base `https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/`:

| file | lines | sha256 |
|---|---|---|
| `squashfs-tools/unsquashfs.c` | 4619 | `ece42b66f37ba67707c2c51b47b643c027232153705f59d238da79958a54cb40` (== S121 sha) |
| `squashfs-tools/squashfs_swap.h` | 425 | `997c221dce59067528c5867173b2927c7bb1519d55bdfe6b80bf80da16cdb0e4` |
| `squashfs-tools/swap.c` | 117 | `832143441689e7a3743a85eb5a54be26d1f3298b193c52fd585433f12da77c03` |
| `squashfs-tools/unsquash-4.c` | 836 | `c8c6a73f93489a493b126d2af3ff87ab3bd0fe54079cf00498d9fbb6966b48ce` |
| `debian/rules` | 23 | `b49d25e9f17ca3806c8ea83d52c4807509f6ad333c63b38385a2485f80f6d885` |

(Also fetched, grep-negative for `AVM|avm|fritz`: `read_fs.c`, `squashfs_fs.h`, `unsquashfs.h`, `endian_compat.h`, `Makefile`, `unsquash-1/12/123/1234/2/3/34.c`, `xz_wrapper.c`, `gzip_wrapper.c`, `compressor.c`; hashes in `sha256-all-fetched.txt`. The string "AVM" appears in no fetched file; sasquatch has no AVM-named logic, only the generic `swap` flag + `FIX_BE`.)

## Where the decision lives (file:line, located quotes <=25 words)

Two independent byte-order mechanisms; AVM layout = their *disagreement*.

1. **Compile-time (all struct fields: superblock, inodes, dirs, block lists, ids) — `squashfs-tools/squashfs_swap.h:32`**: `#if __BYTE_ORDER == __BIG_ENDIAN || defined FIX_BE` selects the real `swap_le*` macros (else `#else` at :345 makes them no-ops, e.g. `SQUASHFS_SWAP_INTS(s, d, n) memcpy(...)` :393). `swap.c:24` same guard. `unsquash-4.c:697` `SQUASHFS_INSWAP_SUPER_BLOCK(&sBlk_4);`, `:46` `SQUASHFS_INSWAP_INTS(block_list, blocks);`. So `FIX_BE` (the `sasquatch-v4be` build) makes struct fields read big-endian regardless of host/`-be`.
2. **Run-time (the 2-byte metadata-block length header only) — `unsquashfs.c:664-668`, `read_block()`**:
   - `:664` `if(swap) {` … `:667` `c_byte = (c_byte >> 8) | ((c_byte & 0xff) << 8);` — header byte-swapped only when `swap != 0`; `:668-670` else read native (LE host => little-endian header). This is the **block-length endianness decision**.
3. **Where `swap` is set** (global `int ... swap = -1` at `:58`):
   - Auto-detect, only when `swap == -1` (no `-be`/`-le`): `:2252` `if(swap == -1)`; heuristic `:2263-2265` (`s_major` out of [MIN,MAX] or `(generic.inodes & 0xFF) == 0` => "different endianess"); then `:2269-2273` `#ifdef FIX_BE swap = 0; #else swap = 1; #endif` (different) and `:2279-2283` `#ifdef FIX_BE swap = 1; #else swap = 0; #endif` (same). In the `FIX_BE` build a BE image (`s_major` reads 1024 on a LE host => "different endianess") therefore gets **`swap = 0` = little-endian headers = the AVM layout**; plain sasquatch inverts it (`swap = 1`).
   - Explicit switch, `:4389-4394`: `} else if(strcmp(argv[i], "-be") == 0) {` / `#if __BYTE_ORDER == __BIG_ENDIAN swap = 0; #else swap = 1; #endif` — on a LE host `-be` => `swap = 1` => **big-endian headers = standard BE v4**. `-le` at `:4395-4400` is the mirror.
4. **Build variant — `debian/rules:17`**: `CFLAGS=-DFIX_BE dh_auto_build` (`:15-18`: build 1 = `sasquatch`, `dh_auto_clean`, build 2 with `-DFIX_BE`, `cp ... sasquatch-v4be`).

Net (derived from the lines above; [INFERENCE] only for the unblob link, which is S112's remit): with `sasquatch-v4be` on a LE host, no `-be` => fields BE + metadata headers LE (AVM layout); `-be` => fields BE + headers BE (standard BE). This matches unblob 26.6.4 omitting `-be` when mkfs_time == bytes_used (S112 lines 44-50) and S121's existing teaches ("without the flag it misreads a standard-BE body").

Quote anchors (verified by `awk 'NR==...'` on the fetched files):
- `unsquashfs.c:667`: `c_byte = (c_byte >> 8) | ((c_byte & 0xff) << 8);` (the 16-bit header swap under `if(swap)` at :664).
- `unsquashfs.c:2269`: `#ifdef FIX_BE` followed by `swap = 0;` (:2270) in the "different endianess" branch.
- `squashfs_swap.h:32`: `#if __BYTE_ORDER == __BIG_ENDIAN || defined FIX_BE`.

## Behavioural check on development inputs (installed binaries; no frozen carrier touched)

Fresh tree (`a.txt`, `d/b.txt`, symlink `l`), `gen-squashfs.py --endian be --comp gzip` -> `be.sqfs` (sha `a10a343a…2e52`, 359 B). `artifacts/.../mkavm.py` rewrites the inode/dir/id-table metadata headers to little-endian and sets mkfs_time = bytes_used (359) -> `avm.sqfs` (sha `69eeeed3…9f37`). Installed `sasquatch-v4be` (sha `fac88740…14c6`) and `sasquatch` (sha `ad02d27a…4754`) run directly (`-d out -f`); full matrix in `behaviour-matrix.txt`:

| image | `sasquatch-v4be` (no flag) | `sasquatch-v4be -be` | `sasquatch` (either) |
|---|---|---|---|
| standard BE (`be.sqfs`) | rc=1 "failed to read id table block" | **rc=0, 3 entries, `a.txt`=hello** | rc=1 "Block size too small" |
| AVM-layout (`avm.sqfs`) | **rc=0, 3 entries, `a.txt`=hello** | rc=1 "failed to read id table block" | rc=1 "Block size too small" |

This is exactly the code-reading prediction (flag-less v4be = LE headers; `-be` = BE headers). Limits: gzip, 5-inode tree, no fragments (my `mkavm.py` asserts that); a development-image mimic of the layout, not the vendor member (not read). Earlier first attempt of `mkavm.py` double-flipped id-table blocks (dir walk overran into them) — fixed before the matrix; the shipped script is the fixed one.

## SOURCES draft — amend S121 (no duplicate row)

S121 already pins `unsquashfs.c` at this tag with the same sha; the AVM logic is in that file. Amend the **scope**, **anchor** and **teaches** cells only (columns 5, 6, 7 of the 11-column row at `corpus/SOURCES.md:127`; id, source, kind, tier, status, opened, recheck unchanged; add this round's use-by).

- **scope** old: `what `-be` does in sasquatch 4.5.1 and how the `sasquatch-v4be` build differs from plain `sasquatch`, at one tag; not unblob's argv decision, not later commits, not any carrier`
  **scope** new: `what `-be` does in sasquatch 4.5.1, how the `sasquatch-v4be` (`-DFIX_BE`) build differs from plain `sasquatch`, and which code decides the metadata-block header byte order (the AVM-BE layout: BE fields, LE headers), at one tag; not unblob's argv decision, not later commits, not any carrier`
- **anchor** old: `tag sasquatch-v4.5.1-6 = commit 15573bf4…; unsquashfs.c 4619 lines sha256 ece42b66…4cb40, lines 4389-4400 `-be` sets the swap flag; `debian/rules` lines 15-18 build the tree twice, the second as "CFLAGS=-DFIX_BE dh_auto_build" copied to sasquatch-v4be; installed binaries sha256 ad02d27a…4754 and fac88740…14c6`
  **anchor** new: keep everything and replace `lines 4389-4400 `-be` sets the swap flag;` by `lines 664-667 `read_block` swaps the 2-byte metadata header only `if(swap)` (`c_byte = (c_byte >> 8) | ((c_byte & 0xff) << 8);`), lines 2252-2283 pick `swap` when no flag (`#ifdef FIX_BE swap = 0;` for a "different endianess" image), lines 4389-4400 `-be`/`-le` set it; `squashfs_swap.h:32` and `swap.c:24` gate struct-field swapping on `defined FIX_BE`;` and, for the second file, record `debian/rules` URL `https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/debian/rules` sha256 `b49d25e9f17ca3806c8ea83d52c4807509f6ad333c63b38385a2485f80f6d885` (23 lines, `:17` `CFLAGS=-DFIX_BE dh_auto_build`) — this also closes the round-39 "loose anchor" disclosed in `round-39-verifier-spotcheck.md:135` (the quoted line lives in a second file whose URL/sha the row omitted). `squashfs_swap.h` sha `997c221d…0e4`, `swap.c` sha `83214344…7c03`.
- **teaches** old: `sasquatch-v4be reads big-endian v4 only when told `-be`; without the flag it misreads a standard-BE body`
  **teaches** new: `sasquatch-v4be with no flag reads BE fields with little-endian metadata headers (AVM layout) and with `-be` reads big-endian headers (standard BE); plain sasquatch cannot swap v4 fields at all on a LE host; the header-order choice is the single `swap` flag at `unsquashfs.c:664`.`
- **used-by**: append the round-40 claims/entry that cites it once landed (L1's call).

If the L1 prefers separate rows for the two extra files (`squashfs_swap.h`, `swap.c`, `debian/rules`), they are one coherent unit with S121 at the same tag; a duplicate row is not warranted (same tier A, same recheck trigger, same scope).

## Limits

- Read at one tag (`sasquatch-v4.5.1-6`); installed binaries' provenance beyond the S121 sha pins and the matching error-string set (`strings` shows the "different endianess" messages in both binaries; `-be` only in the v4be string table listing) is not rebuilt from source here. [INFERENCE] that the installed v4be binary is built from exactly this source, supported by the behaviour matrix.
- Compressed-data block (file data) sizes are read from inode block lists via compile-time `SQUASHFS_INSWAP_INTS` (`unsquash-4.c:46`), not from a header; the AVM-specific "little-endian block-length header" is therefore the metadata-block header read in `read_block()` (also used for fragment/id/lookup table blocks). Not separately probed for fragments/xattr/lookup tables (the dev image has none).
- No REA/unblob run, no frozen carrier read. Scratch removed on exit; nothing written outside the artifacts dir and this report.
- Tools installed: none.
