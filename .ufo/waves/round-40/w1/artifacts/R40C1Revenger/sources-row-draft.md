# Draft SOURCES row — sasquatch FIX_BE build machinery

Status: DRAFT for the L1 (not appended to `corpus/SOURCES.md`; wave-1 seat may not edit it).

## Is the location already a lane row?

Yes, partly. **S121** (`corpus/SOURCES.md:127`) already pins
`onekey-sec/sasquatch` at tag `sasquatch-v4.5.1-6` and anchors `squashfs-tools/unsquashfs.c`
(sha256 `ece42b66…4cb40`) plus `debian/rules:16-18`. It does **not** anchor the files where the
`FIX_BE` byte-order machinery actually lives: `squashfs_swap.h:32`
(`#if __BYTE_ORDER == __BIG_ENDIAN || defined FIX_BE`) and `swap.c:24`, nor the object split in
`Makefile:181-185,409` that keeps `read_fs.o` (and its compile-time `read_block`) out of the
unsquashfs binary.

So this is **not a new location** but a **file-level split of S121**. The L1 should either
(a) extend S121's `anchor` cell with the five hashes and line anchors below, or (b) admit the
companion row below if the lane prefers one row per file (as with S108/S112).

## Draft row (11 columns, table order `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`)

| S123 | onekey-sec/sasquatch FIX_BE build machinery at tag sasquatch-v4.5.1-6 — https://github.com/onekey-sec/sasquatch/tree/sasquatch-v4.5.1-6/squashfs-tools | code | A | How the `sasquatch-v4be` build reads a big-endian superblock while treating the 2-byte block-length headers as little-endian: the `FIX_BE` compile-time swap switch, the runtime `swap` flag that `-be` sets, and the two-build recipe; not unblob's argv choice, not any carrier | tag `sasquatch-v4.5.1-6` = commit `15573bf46c671c8ed23e8c0c50e6187e0c8d0b62`; `squashfs_swap.h` sha256 `997c221dce59067528c5867173b2927c7bb1519d55bdfe6b80bf80da16cdb0e4`, `:32` `#if __BYTE_ORDER == __BIG_ENDIAN \|\| defined FIX_BE`, `:294-296` `SQUASHFS_INSWAP_SUPER_BLOCK` unconditional swap, `:342` `SQUASHFS_INSWAP_SHORTS` = `inswap_le16_num`; `swap.c` sha256 `832143441689e7a3743a85eb5a54be26d1f3298b193c52fd585433f12da77c03`, `:24` same guard, `:63-67` `inswap_le16`, `:106-116` `inswap_le16_num`; `unsquashfs.c` `:653-670` `read_block` byte-swaps the 2-byte length only `if(swap)`, `:2252-2286` the endian heuristic with `FIX_BE` inverting both arms (`swap = 0` when the image "suggests … a different endianess"), `:4389-4400` `-be` sets `swap = 1` on an LE host; `Makefile` sha256 `207c722978c1f9105e9f93efad0d11e48583c08708a3d6ccf969f92682757126`, `:181-185` `read_fs.o` is `MKSQUASHFS_OBJS`-only, `:409` `sasquatch: $(UNSQUASHFS_OBJS)`; `debian/rules` sha256 `b49d25e9f17ca3806c8ea83d52c4807509f6ad333c63b38385a2485f80f6d885`, `:12-18` builds the tree twice, the second `CFLAGS=-DFIX_BE`, copied to `sasquatch-v4be` | Read a successful `sasquatch-v4be` run as (all fs structs BE) + (block lengths LE unless `-be`), and never claim a successful REA receipt records the sasquatch argv | mined | 2026-10-26 | 180d | corpus/knowledge/<round-40 AVM-layout entry> (pending L1) |

## Anchor hashes (recomputable)

```
sha256sum squashfs-tools/{squashfs_swap.h,swap.c,unsquashfs.c,Makefile,read_fs.c,unsquash-4.c} debian/rules
997c221dce59067528c5867173b2927c7bb1519d55bdfe6b80bf80da16cdb0e4  squashfs_swap.h
832143441689e7a3743a85eb5a54be26d1f3298b193c52fd585433f12da77c03  swap.c
ece42b66f37ba67707c2c51b47b643c027232153705f59d238da79958a54cb40  unsquashfs.c
207c722978c1f9105e9f93efad0d11e48583c08708a3d6ccf969f92682757126  Makefile
2391d75f71a80092fd2fc3ca2ffabe5f251dbf051e36cd8297d1462a79dd7e33  read_fs.c
c8c6a73f93489a493b126d2af3ff87ab3bd0fe54079cf00498d9fbb6966b48ce  unsquash-4.c
b49d25e9f17ca3806c8ea83d52c4807509f6ad333c63b38385a2485f80f6d885  debian/rules
```

Fetch: `https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/squashfs-tools/<file>`
and `…/debian/rules`. All seven were fetched this seat and hashed locally (see
`source-anchors.txt`).

## Why it earns a row (or an S121 extension)

- `S121`'s scope sentence is "what `-be` does … and how the `sasquatch-v4be` build differs from
  plain `sasquatch`". The mechanism the AVM claim depends on is exactly that difference, and it is
  not in `unsquashfs.c` alone: `FIX_BE` is a *compile-time* substitution of the whole
  `squashfs_swap.h` branch (`:32`), while `swap` is a *runtime* flag read only by `read_block`
  (`:664`). Without both anchors a reader can conclude that `-be` swaps the superblock, which is
  false.
- The lane's S112/S114 pair already splits one upstream file into two rows by scope, so a
  file-level split is inside the existing convention.
