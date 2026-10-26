# R39W2K5K6Rebuild — rebuild + independent read of carriers K5 and K6

Verdict: **CONFIRMED** for both carriers. R39-C1's K5 and K6 are reproducible byte-for-byte from their
committed source trees with the committed generator, they decode to exactly the frozen oracles under the
committed reader *and* under a reader I wrote from the on-disk layout, K6's superblock compression id is 4
with four compressed xz data blocks (each a complete `.xz` stream, CRC32, `xz --test` clean), and all six
in-image symlink classes recompute correctly under unblob 26.6.4's own `is_safe_path`. Two **DEFECTS FOUND**
exist in adjacent round-39 tooling/description, neither of which touches a carrier pin (below).

Seat scope: carriers `corpus/evidence/round-39/c1/K5` and `.../K6` only (source trees, pins, oracles,
symlink tables, receipts). No lane file outside this report and my artifacts directory was written.

## 1. Rebuild — pins reproduce exactly

Source trees copied with `cp -a` (symlinks preserved: `readlink K5src/usr/share/demo/escape` →
`../../../../etc/shadow`; `readlink K6src/outside` → `../outside`).

```
$ python3 -I -B tools/round-39/gen-squashfs.py K5src K5-rebuild.sqsh --endian be --comp gzip
wrote K5-rebuild.sqsh 26813 bytes, inodes 24                              # exit 0
$ python3 -I -B tools/round-39/gen-squashfs.py K6src K6-rebuild.sqsh --endian be --comp xz
wrote K6-rebuild.sqsh 15867 bytes, inodes 21                             # exit 0
$ sha256sum K5-rebuild.sqsh K6-rebuild.sqsh
5999eafc0fb6a8bc3cd8a363d14f4c3f0ffe00e947e155cf8f1bb3278d00b228  K5-rebuild.sqsh
00152518a3902a1a13892ec4bfd280a258f162d8fdf77260ea2b41f4f482b25b  K6-rebuild.sqsh
$ cmp corpus/.../K5/carrier.sqsh K5-rebuild.sqsh   # identical (exit 0)
$ cmp corpus/.../K6/carrier.sqsh K6-rebuild.sqsh   # identical (exit 0)
```

| carrier | frozen pin (`carriers.json`) | rebuilt sha256 | size |
|---|---|---|---|
| K5 | `5999eafc…8d00b228` | **identical** | 26813 = pin |
| K6 | `00152518…f482b25b` | **identical** | 15867 = pin |

Determinism is content-only, not environment-only: rebuilding copies whose every mtime was forced to
`2001-02-03 04:05:06`, with `chmod -R go-rwx` and `umask 077`, produced the same two hashes
(`rebuild-and-pins.txt`). The writer hardcodes `MKFS_TIME=1700000000` and modes `0o100644/0o40755/0o120777`
and sorts walks, so pins are reproducible from the tree bytes alone.

Pins are of the *committed* bytes, not a working-tree accident:
`git ls-tree 6fdaf4f1 … K5/carrier.sqsh K6/carrier.sqsh` → blobs `ed7e62c2…`/`68949843…`, equal to
`git hash-object` of the working files; `git status --porcelain` for both src trees and both carriers at
HEAD `e40a25df` is empty (`rebuild-and-pins.txt`). `carriers.json` `size_bytes`, `oracle_sha256`,
`symlinks_sha256`, `oracle_files` (10/8) and `symlinks_in_tree`/`symlinks_escaping` (2/1, 1/2) all verify
against the files on disk.

## 2. Committed reader vs oracle

```
$ python3 -I -B tools/round-39/sqfs-list.py K5-rebuild.sqsh --files K5.f.tsv --symlinks K5.s.tsv --inspect   # exit 0
$ python3 -I -B tools/round-39/sqfs-list.py K6-rebuild.sqsh --files K6.f.tsv --symlinks K6.s.tsv --inspect   # exit 0
$ diff -u corpus/.../K5/oracle.tsv   K5.f.tsv    → (identical)
$ diff -u corpus/.../K5/symlinks.tsv K5.s.tsv    → (identical)
$ diff -u corpus/.../K6/oracle.tsv   K6.f.tsv    → (identical)
$ diff -u corpus/.../K6/symlinks.tsv K6.s.tsv    → (identical)
```
Also run on the *committed* carriers: `K5c.f.tsv`/`K5c.s.tsv`, `K6c.f.tsv`/`K6c.s.tsv` are byte-identical to
the rebuild outputs (`diff -q` clean), and `--inspect` reports `regular_files` 10 / 8, `symlinks` 3 / 3,
`warnings: []`, `in_tree_symlinks`/`escaping_symlinks` 2/1 and 1/2 — the same counts as `carriers.json`.
K5's oracle rows equal the source-tree bytes directly (one apparent diff was only locale collation of
`README.txt` in my `sort`; the row set, hashes and sizes match). `K6 src == oracle` verbatim.

Edge cases the images do exercise (and both readers handle): a 0-byte regular file (K5 `empty.flag`,
inode with zero block list, start_block aliasing the next file's offset), a UTF-8 directory entry
(`アイコン.txt`, name_size counts bytes), a space in a name, a 20000-byte file (5 blocks), and K5's root
directory body ending exactly on the last byte of its metadata block (offset 380 + 112 = 492).

## 3. K6 superblock compression id 4 and compressed xz data blocks

My own superblock decode (BE, 96-byte `squashfs_super_block`) of the rebuilt images:

| carrier | magic | s_major.minor | comp id | block_size/log | frags | inodes | bytes_used | metadata |
|---|---|---|---|---|---|---|---|---|
| K5 | `sqsh` | 4.0 | **1** (gzip) | 4096/12 | 0 | 24 | 26813 | inode 1 block/846 B, dir 1 block/492 B |
| K6 | `sqsh` | 4.0 | **4** (xz) | 4096/12 | 0 | 21 | 15867 | inode 1 block/756 B, dir 1 block/402 B |

`fragment_table_start`, `xattr_id_table_start`, `lookup_table_start` are all `0xffffffffffffffff`, id table
holds one UID 1000 (`no_ids=1`), i.e. a plain no-fragment, no-xattr image.

Compressed data blocks, bit `1<<24` clear:
- K5: 2 compressed gzip blocks (`README.txt` 1, `usr/share/demo/assets/manifest.json` 1); 12 blocks stored
  raw (`zlib` level 9 output ≥ chunk, so the writer stores them raw). Decoded by `zlib.decompress`.
- K6: **4** compressed blocks, all in `var/log/repeat.log` (14400 B = 4096+4096+4096+2112, on-disk
  224/232/228/192 B); the other 10 data blocks are stored raw. Every compressed block starts with the xz
  container magic `fd377a585a00`, decompresses under `lzma.decompress` (which enforces the stream's CRC32
  check), and `xz --test` exits 0 on each extracted block (`xz -lvv` reports `Check: CRC32`, dict 8 MiB,
  `Sizes in headers: No`). The xz blocks are therefore complete `.xz` containers, not bare LZMA2 — the
  round-39 fix the generator docstring claims.

## 4. Symlink classes recomputed from the S122 rule

Rule source: unblob 26.6.4 `is_safe_path` (S122, lines 34-39) —
`basedir.joinpath(path).resolve().relative_to(basedir.resolve())`, `False` on `ValueError` — driven by
`extractor.py:50-92 fix_symlink`, which for a relative target takes `target = path.resolve()` and then tests
containment with **no clamping at the extraction root**. Two independent implementations:

1. the installed unblob function itself, run with the unblob 3.13 interpreter over `cp -a`'d trees as the
   extraction root (`symlink-classes-unblob-fn.txt`);
2. a POSIX component stack I wrote (pop on `..`, `escaping` the moment the stack would go negative) in my
   independent reader (`indep-reader.txt`).

| carrier | link | target | frozen class | recompute #1 | recompute #2 (observed behaviour in `after.json`) |
|---|---|---|---|---|---|
| K5 | `usr/share/demo/escape` | `../../../../etc/shadow` | escaping | escaping (`is_safe_path=False`, resolves to `<root>/../etc/shadow`) | `MaliciousSymlinkRemoved`, target `<…>/extracted/etc/shadow` = above `firmware.bin_extract` |
| K5 | `usr/share/demo/link-blob` | `../opt/blob.bin` | in-tree | in-tree (`True`, resolves inside) | kept as `unpublished_entries` entry |
| K5 | `usr/share/demo/link-notes` | `notes.txt` | in-tree | in-tree (`True`) | kept as `unpublished_entries` entry |
| K6 | `a/b/link-in` | `../../etc/config.ini` | in-tree | in-tree (`True`; climbs exactly to root, legal) | kept as `unpublished_entries` entry |
| K6 | `data/escape-deep` | `../../../../etc/passwd` | escaping | escaping (`False`) | `MaliciousSymlinkRemoved`, target `<…>/etc/passwd` above `firmware.bin_extract` |
| K6 | `outside` | `../outside` | escaping | escaping (`False`) | `MaliciousSymlinkRemoved`, target `<…>/extracted/outside` |

All six labels agree across the frozen table, two independent recomputations and the committed REA receipt
(diagnostics count 1 for K5, 2 for K6; unpublished-entry gaps 2 and 1). The K5 `escape` case is exactly the
no-clamping discriminator: a clamping rule would have labelled it in-tree; the fourth `..` empties the stack
and it is escaping. No symlink chains exist in either image, so class is not sensitive to resolution order.

## 5. Independent decode (not the repo reader)

`artifacts/R39W2K5K6Rebuild/indep.py` parses the superblock, both metadata streams, directory headers/entries
and regular/symlink inodes from the v6.12 layout and decompresses every data block with stdlib `zlib`/`lzma`:

```
== K5-rebuild.sqsh comp_id=1 block_size=4096 inodes=24 bytes_used=26813
   metadata blocks: inode=1 dir=1 (both uncompressed on disk)
   files: 10 (compressed data blocks total 2), symlinks: 3      RESULT: ORACLE MATCH
== K6-rebuild.sqsh comp_id=4 block_size=4096 inodes=21 bytes_used=15867
   files: 8 (compressed data blocks total 4), symlinks: 3       RESULT: ORACLE MATCH
     compressed-data-block file: var/log/repeat.log size=14400 blocks=4 compressed=4 first6=fd377a585a00
```
Inode-number↔offset map consumes the inode stream exactly (24/21 inodes), every `i_size` matches the decoded
length, and each oracle row's sha256+size matches. The committed `after.json` receipts independently carry
the same 10/8 file paths with matching sha256 and sizes (`receipt-crosscheck.txt`), so the oracle is not
merely self-consistent with a single reader.

## 6. Defects found (adjacent, not carrier-falsifying)

**D1 — `tools/round-39/gen-squashfs.py` writes metadata block *indices* where the format wants byte offsets,
so it cannot build images whose inode table exceeds 8192 bytes.** `MetaWriter.append` returns
`len(self.blocks)` as the block field of an inode/dir reference; the kernel (`SQUASHFS_INODE_BLK`, cited in
`sqfs-list.py` lines 130-136) and the repo's own reader (`sqfs-list.py:387`, `directory_table_start +
start_block`) treat that field as a byte offset inside the metadata area. Repro (301 inodes):

```
$ python3 -I -B tools/round-39/gen-squashfs.py big big.sqsh --endian be --comp gzip   # 300 files + root
wrote big.sqsh 18760 bytes, inodes 301                                                # exit 0
$ python3 -I -B tools/round-39/sqfs-list.py big.sqsh --files big.f.tsv --symlinks big.s.tsv --inspect
sqfs-list: zero-length metadata block at 3097                                         # exit 2
```
`root_ref=0x10a30` → block field `1`, offset 2608; the inode metadata blocks sit at stream byte offsets
`0` (8192 B) and `8194` (2640 B), so offset `1` lands inside block 0's data and the header there reads
`0x0000`. My independent reader rejects the same image. Impact on this round: **none** — K1, K2, K5, K6 and
every BE held-out carrier (H01/H02/H05…H10/H13…H20; H03/H04/H11/H12 are LE `hsqs`) has exactly one inode and
one directory metadata block, so the block field is always `0` and index == byte offset. Risk: any future
carrier or held-out image with roughly >220 inodes silently becomes unreadable by both readers while the
generator still exits 0. [INFERENCE] the same field is written for directory inodes, so a >8192-byte
directory table would fail the same way; not separately reproduced.

**D2 — `carriers.json` K5 description says "4 dir levels"; the image has 5.** Deepest path
`usr/share/demo/assets/icons/アイコン.txt` = 5 nested directories (6 components). Purely descriptive; the
substantive K5 description ("10 files incl 0-byte and 20000-byte, space and UTF-8 names, 2 in-tree + 1
escaping symlink") is accurate. K6's "8 files, 1 in-tree + 2 escaping" and "4 compressed xz data blocks" are
accurate.

## 7. Coverage limits of these two carriers (not defects)

- No fragments, no sparse blocks, no extended (`ldir`/`lreg`/`lsymlink`) inodes, no xattrs, no duplicate
  lookup table, metadata always stored uncompressed. Reader paths for fragments/sparse/extended inodes are
  not exercised by K5/K6.
- Compression decode is thin: K5 = 2 gzip blocks out of 14 data blocks; K6 = 4 xz blocks, all in one file,
  out of 14. The remaining blocks are raw by construction (`len(c) >= len(chunk)`) because the trees are
  small or high-entropy.
- K6's xz streams declare an 8 MiB LZMA2 dictionary (`preset 6`) with `Sizes in headers: No`. unblob/sasquatch
  and liblzma accept this, as the committed receipts and `xz --test` show; [INFERENCE] a decoder that caps
  dictionary size at the 4096-byte block size (the kernel squashfs xz wrapper's `dict_limit`) would reject
  these blocks. Not tested here; flagging only as a portability note for the "standard v4" wording.
- Symlink taxonomy covers exactly one no-clamping hop-through-root case per carrier plus one exactly-to-root
  in-tree case; no self/mutual loops, no empty targets, no absolute targets, no chained links.

## 8. Tooling and cleanup

No installs or upgrades: Python 3.14.8 (`/usr/bin/python3`), XZ Utils/liblzma 5.8.4, unblob 26.6.4 under
`~/.local/share/uv/tools/unblob` (interpreter 3.13.16) used read-only for `is_safe_path`. No pacman, no
network fetch, no REA/unblob run of my own (unblob writes `unblob.log` into cwd — not needed, receipts
already committed). All work in `S=/fast/scratch/hyaku/kaidoku-r39/R39W2K5K6Rebuild`, `TMPDIR=$S`; scratch
removed after copying evidence. No git mutation: only `log`/`ls-tree`/`hash-object`/`status`/`rev-parse`.

Artifacts: `.ufo/waves/round-39/w2/artifacts/R39W2K5K6Rebuild/`
`environment.txt`, `rebuild-and-pins.txt`, `reader-diff.txt`, `K5.f.tsv`, `K5.s.tsv`, `K6.f.tsv`, `K6.s.tsv`,
`superblock-xz.txt`, `indep.py`, `indep-reader.txt`, `symclass.py`, `symlink-classes-unblob-fn.txt`,
`probe.py`, `sb.py`, `receipt-crosscheck.txt`, `latent-multiblock-metadata.txt`, `big-reader-error.txt`.

Report: .ufo/waves/round-39/w2/R39W2K5K6Rebuild.md
