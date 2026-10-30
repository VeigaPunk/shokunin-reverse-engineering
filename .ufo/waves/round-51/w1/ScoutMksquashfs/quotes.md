# Quotes — mksquashfs padding source (R51-C2 grounding)

Every quote is ≤25 words. Line numbers are into the fetched file
`https://raw.githubusercontent.com/plougher/squashfs-tools/master/squashfs-tools/mksquashfs.c`
sha256 `205f58e6394844317b58266ca351966e222a2cc49657c7cc68365030d4a2bc5c`, 266,790 B,
HTTP 200 2026-10-30, upstream master head `db038ef265ed00bb17aaf695a72f9b0c3489eb20`.
Local tool: `mksquashfs version 4.7.5 (2026/03/01)` (pacman `squashfs-tools 4.7.5-1`).

## Q1 — the option is `-nopad`, one token, no hyphen

> `:8501` `} else if(strcmp(argv[i], "-nopad") == 0)`

- ref: fetched `mksquashfs.c:8501` (mksquashfs option loop); same flag at `:7362` (sqfstar loop)
- sha256 of the fetched file: `205f58e6…d4a2bc5c`

> `:8502` `nopad = TRUE;`

- ref: fetched `mksquashfs.c:8502`

## Q2 — the flag's own one-line declaration comment

> `:204` `/* Will Mksquashfs pad the filesystem to a multiple of 4 Kbytes? */`

- ref: fetched `mksquashfs.c:204`

## Q3 — where the padding is actually written (the skipped work)

> `:588` `if(!nopad && tail) {`

- ref: fetched `mksquashfs.c:588`, inside `prep_destination()`

> `:590` `write_destination(fd, get_dpos(), 4096 - tail, temp);`

- ref: fetched `mksquashfs.c:590` — writes `4096 - tail` zero bytes at the current position

## Q4 — the tail computation: pad up to a 4096-byte (4 KiB) multiple

> `:577` `int tail = end & (4096 - 1);`

- ref: fetched `mksquashfs.c:577`

## Q5 — the function's own summary comment

> `:571-573` `/* If necessary: truncate output destination to filesystem end / pad to 4Kbyte multiple */`

- ref: fetched `mksquashfs.c:571-573` (comment head of `prep_destination()`)

## Q6 — the streaming-mode second effect of the same flag

> `:6262` `block = nopad ? get_dpos() : (get_dpos() + 4095) & ~4095;`

- ref: fetched `mksquashfs.c:6262`, in `write_superblock()` — superblock offset 4 KiB-aligned unless `nopad`

## Q7 — upstream master keeps the option strings in a separate header

> `:77` `#include "mksquashfs_help.h"`

- ref: fetched `mksquashfs.c:77` — the usage strings are NOT in `mksquashfs.c` on master

## Q8 — the usage string, from the installed 4.7.5 tool

> `-nopad			do not pad filesystem to a multiple of 4K`

- ref: `mksquashfs -help-option pad` (exit 0), squashfs-tools 4.7.5-1

## Q9 — the only "why" in the shipped toolchain (installed man page, not the fetched file)

> `:1431` `The -nopad option informs Mksquashfs to not pad the filesystem to a 4K multiple.`

- ref: `/usr/share/doc/squashfs-tools/USAGE-MKSQUASHFS:1431`, sha256 `b047ffbb…aa26b12e7f`

> `:1432-1433` `This is performed by default to enable the output filesystem file to be mounted / by loopback, which requires files to be a 4K multiple.`

- ref: `/usr/share/doc/squashfs-tools/USAGE-MKSQUASHFS:1432-1433`

> `:1434-1435` `If the filesystem is being written to a block device, or is to be stored in a bootimage, the extra / pad bytes are not needed.`

- ref: `/usr/share/doc/squashfs-tools/USAGE-MKSQUASHFS:1434-1435`

## Q10 — the negative: upstream master's `mksquashfs.c` carries NO rationale comment

- observation, not a quote: grepping the fetched 266,790-byte file for `loopback`, `bootimage`,
  `pad to a multiple`, `multiple of 4K` returns only `:204`, `:573` and the code sites above.
  The "why" exists only in the shipped man page (Q9), which is a different artifact at a
  different version (4.7.5 installed vs master HEAD).
- ref: fetched `mksquashfs.c` (sha256 `205f58e6…d4a2bc5c`), full-file grep

## Q11 — the rejected spelling, measured

> `mksquashfs: -no-pad is an invalid option`

- ref: measured, `mksquashfs rej rej.sqfs -noappend -no-progress -all-root -no-pad`, exit 1
- ref (mirror): `mksquashfs -help-option no-pad` → `mksquashfs: -help-option no-pad does not match any mksquashfs option`

## Q12 — the ddwrt refusal is magic-driven, not pad-driven (measured)

> `Non-standard SquashFS Magic: 'tqsh'`

- ref: measured, `sasquatch -be …/squashfs_v3.be.nopad.bin`, exit 0, stderr
- corroborating lane bytes: the same string appears verbatim in the committed round-42
  envelope `dmg_Z3_v3ddwrt_inode_table/envelope.json` (base64 stderr field,
  `sha256 839c17a8…`) — the lane's own failed-body receipt.
