# R39C1IndepReader — independent SquashFS 4.0 oracle reader (round 39, wave 1)

**Verdict: DONE.** `sqfs-list.py` (pure stdlib, no unblob/REA/sasquatch code) reads
SquashFS 4.0 of either endianness with gzip/LZMA/XZ, fragments and sparse blocks, and
its regular-file table is byte-identical (after a C-locale sort) to all four committed
round-37 `oracle.tsv` files (K1–K4) and to their source trees/extractor output; the
symlink tables for K1–K4 are in §4. Four measured limits of the lane generator (§7,
P1–P4) and one symlink-classification correction (§6, loops) change what the freeze can
safely ask K5/K6 to be.

Artifacts: `.ufo/waves/round-39/w1/artifacts/R39C1IndepReader/`.
Reader sha256 `1808c3f54205448761e27ffe8a82de59fe87300eb4c49ec406324800d148be7f`.
No REA run, no held-out carrier, no VCS mutation; scratch removed (§10).

## 1. Deliverable and contract

`artifacts/R39C1IndepReader/sqfs-list.py` — 688 lines, stdlib only (`argparse`,
`hashlib`, `json`, `lzma`, `struct`, `sys`, `zlib`).

    python3 -I -B sqfs-list.py IMAGE --files OUT.tsv --symlinks OUT.tsv [--inspect]
    exit 0 ok | exit 2 unreadable or unsupported (reason on stderr)

| table | columns |
|---|---|
| `--files` | `<image-root-relative path>\t<sha256>\t<size>` |
| `--symlinks` | `<image-root-relative path>\t<raw on-disk target>\t<in-tree\|escaping>` |

Rows are sorted by the UTF-8 bytes of the path, `\n` terminated, no header — the
committed `oracle.tsv` shape. Paths are POSIX, image-root relative, no `./` prefix, so
they are exactly the "relative-path suffix" the C1 predicate matches against
`firmware.bin_extract/…` published paths.

`--inspect` prints a JSON summary to stdout: endianness, every superblock field, counts,
`symlink_reasons`, and `decode_paths` (`compressed_metadata_blocks`, `raw_metadata_blocks`,
`compressed_data_blocks`, `raw_data_blocks`, `sparse_blocks`, `fragment_slices`) — the
evidence in §5 that a given run really decoded what it claims to decode.

Refusals (all exit 2, message names the fault): bad magic; `s_major/s_minor` ≠ 4.0;
`block_size` outside 4096…1 MiB or not a power of two (a disagreeing `block_log` is a
warning, `block_size` wins); `bytes_used` past end of file (truncated); table starts
outside `[96, bytes_used)`; compression id other than 1/2/4; any decompression failure;
metadata block that inflates past 8192; a directory body that overruns or underruns its
declared length; dir entry name > 256 bytes; name with NUL/TAB/CR/LF (cannot be written
as TSV); duplicate name in a directory; a directory inode reachable twice; a data block
whose size field has bits above bit 24 set (kernel `squashfs_block_size` returns `-EIO`
for that); a missing/out-of-range fragment; a file whose inode size disagrees with the
bytes actually assembled.

Implemented paths: superblock (96 bytes), base/reg/lreg/dir/ldir/symlink/lsymlink inodes,
uncompressed **and** compressed metadata blocks, directory bodies spanning metadata
blocks, data blocks (compressed, stored-uncompressed via bit 24, sparse via a zero
entry), fragments (index table → metadata page → entry, compressed fragment pages),
in-tree/escaping/loop/empty symlink classification. Special inodes (device/fifo/socket)
are counted, not published.

## 2. Layout source (pinned)

Linux v6.12, fetched 2026-10-26 (kept as `sources/squashfs_fs.h.v6.12`, sha256
`ae0303d382a655c942f6401de3591c8d3bf626220062f32af57c87a3691320b7`):

* base: `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/squashfs/`
* `squashfs_fs.h?h=v6.12` — `:19` metadata size 8192 · `:33` name max 256 · `:36` dir
  count 256 · `:38` invalid fragment `0xffffffff` · `:78-92` inode type ids (DIR 1,
  REG 2, SYMLINK 3, LDIR 8, LREG 9, LSYMLINK 10, LSOCKET 14) · `:106-118` compressed
  bits (`1<<15` metadata, `1<<24` data) · `:130-136` inode ref = `blk << 16 | offset`
  where `blk` is a **byte** offset from the table start · `:233-238` compression ids
  (ZLIB 1, LZMA 2, LZO 3, XZ 4, LZ4 5, ZSTD 6) · `:240-260` `squashfs_super_block`
  (96 bytes, field order used verbatim) · `:269-276` base inode · `:322-332` symlink
  inode · `:334-346` reg inode · `:348-363` lreg inode (`start_block` is `__le64`,
  then `file_size`, `sparse`, `nlink`, `fragment`, `offset`, `xattr`) · `:365-377` dir
  inode (`start_block`, `nlink`, `file_size` u16, `offset` u16, `parent_inode`) ·
  `:379-394` ldir inode · `:409-415` dir entry · `:417-421` dir header · `:423-427`
  fragment entry (`__le64 start`, `__le32 size`, `__le32 unused`).
* `dir.c?h=v6.12` `:52,118` the 3 invented bytes for `.`/`..` · `:150-195` the readdir
  body (`length = i_size`, `count+1` entries, per-entry ref `start_block << 16 | offset`,
  signed inode-number delta).
* `inode.c?h=v6.12` `:175-199` lreg + `squashfs_frag_lookup` · `:273-302` symlink and
  lsymlink (lsymlink stores an extra `__le32 xattr` **after** the target bytes — the
  reader consumes it).
* `file.c?h=v6.12` `:440` `squashfs_readpage_sparse` · `:616` `if (bsize == 0)` — a zero
  block-list entry is a sparse block.
* `fragment.c?h=v6.12` `:38-60` fragment lookup: u64 index entry → metadata page →
  `{start_block, size, unused}`, page offset `(i*16) % 8192`.
* `block.c?h=v6.12` `:271-280` data block: `1<<24` = stored uncompressed, rest = on-disk
  size.
* Symlink disposition (not a kernel source): unblob 26.6.4
  `lib/python3.13/site-packages/unblob/extractor.py:50-95` `fix_symlink` +
  `:34-39` `is_safe_path` — absolute target `lstrip('/')` and re-rooted at the extraction
  root; a target outside the root is unlinked and reported `MaliciousSymlinkRemoved`; an
  empty target is unlinked with **no** report (`:68-72`).

## 3. Validation on K1–K4 (committed oracles)

Measured at base `a2f64e1da78afcf8cc39287106604dbcc270844c` (lane `main`), with the four
carriers hashing exactly to the round-38 pins: K1 `1cfb6c33…`, K2 `403cb0a8…`,
K3 `9c7c523c…`, K4 `a29ddc15…` (`sha256sum` on the committed bytes, 2026-10-26). If a
later wave changes any K1–K4 byte, every table in §3/§4 must be re-derived — the classes
are carrier-specific, not a property of the tree the carrier was built from.

    python3 -I -B artifacts/R39C1IndepReader/check-oracles.py \
        --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
        --artifacts artifacts/R39C1IndepReader        # exit 0

Result (`oracle-check.txt`), comparing each `K*.files.tsv` with the committed
`corpus/evidence/round-37/c1/K*/oracle.tsv` after a C-locale sort of both:

| carrier | endian | compression | block_size | inodes | fragments | bytes_used | rows | files table |
|---|---|---|---|---|---|---|---|---|
| K1 `carrier.sqsh` | big | gzip | 4096 | 11 | 0 | 9780 | 5 | **IDENTICAL** (sha256 `0c993e7421338a8c…`) |
| K2 `carrier.sqsh` | big | gzip | 4096 | 10 | 0 | 1606 | 3 | **IDENTICAL** (`6567cc50d9a1dea2…`) |
| K3 `carrier.bin` | big | gzip | 131072 | 5 | 1 | 307 | 4 | **IDENTICAL** (`638a6f75579ae1ff…`) |
| K4 `carrier.bin` | big | gzip | 131072 | 5 | 1 | 307 | 4 | **IDENTICAL** (`638a6f75579ae1ff…`) |

(the quoted hash is sha256 over the sorted table, first 16 hex digits as recorded in
`oracle-check.txt`; K3 and K4 hold the same four files, K4 is the same image without the
4096-byte padding — 307 bytes on disk).

Independent extractor agreement, same carrier bytes, read-only (`extractor-probes.txt`):

* `unblob` 26.6.4 on K1–K4: extracted regular files identical to the reader's table
  (5/3/4/4 rows, path + sha256 + size), and its symlink disposition equals the reader's
  class for every link (K1 `link-to-hello` reported `MaliciousSymlinkRemoved`, K2
  `var/lib/run-link` kept).
* `sasquatch-v4be` 4.5.1 (`-be`) on K1: 5 files identical, and it keeps the raw
  `../hello.txt` symlink that unblob later removes — the reader reports the raw target,
  which is what REA's `unpublished_entries[].link_target` carries (K2 `after.json`
  `../../a/run.sh`).

## 4. Symlink tables for K1–K4 (deliverable)

    K1  link-to-hello      ../hello.txt      escaping
    K2  var/lib/run-link   ../../a/run.sh    in-tree
    K3  (none)
    K4  (none)

Cross-check, measured:

* K1 `link-to-hello` sits in the image root, so `../hello.txt` leaves the root. unblob
  logs `Path traversal attempt through symlink, removing target=hello.txt` and the JSON
  report carries `MaliciousSymlinkRemoved {link: …/link-to-hello, target: …/hello.txt}`
  (note: for a relative link unblob reports the **resolved absolute** target). REA's
  round-38 K1 `after.json` has 0 gaps — consistent.
* K2 `var/lib/run-link` → `../../a/run.sh` resolves to `a/run.sh` inside the root: unblob
  keeps the link, and round-38 K2 `after.json` carries exactly one
  `unpublished-entry` gap with `link_target` `../../a/run.sh` — consistent.
* K3/K4: the two unblob fixtures contain no symlinks at all, so `K3.symlinks.tsv` and
  `K4.symlinks.tsv` are empty files (0 bytes), not absent.

Reader `--inspect` reasons for the same runs: K1 `{above-root: 1}`, K2 `{inside: 1}`,
K3/K4 `{}`.

## 5. Two required LE images (plus fixtures that cover the paths K1–K4 miss)

    python3 -I -B artifacts/R39C1IndepReader/build-and-check.py \
        --work $S/work --artifacts artifacts/R39C1IndepReader \
        --gen <LANE>/tools/round-37/gen-squashfs.py         # exit 0, "ALL EXPECTED"

Trees are written deterministically by the harness (`trees/A`, `trees/B`, …); every
expected file table is computed from the tree with an independent `os.walk` + sha256 and
every symlink class is stated by hand in `LINK_CASES`. `build-and-check.txt` records the
reader sha256 it scored.

| fixture | built by | bytes | endian/comp | files | symlinks (in-tree/escaping) | check |
|---|---|---|---|---|---|---|
| **A-le-gzip** | lane generator | 1217 | LE gzip | 6 | 3 / 1 | files == tree; symlinks == expected; `unsquashfs` 4.7.5 extracts 6 files identical |
| **B-le-xz** | lane generator | 665 | LE **lzma (id 2!)** | 2 | 2 / 1 | files == tree; symlinks == expected; `unsquashfs` **fails** (see §7 P0) |
| B-be-gzip | lane generator | 668 | BE gzip | 2 | 2 / 1 | files == tree; `sasquatch-v4be` + `unblob` agree |
| B-be-xz | lane generator | 665 | BE **id 2** | 2 | 2 / 1 | files == tree; `sasquatch-v4be` **fails** (§7 P0) |
| C-le-gzip | lane generator | 285 | LE gzip | — | — | non-ASCII filename probe → reader exit 2 (§7 P1) |
| L-le-gzip | lane generator | 14860 | LE gzip | — | — | 300-file probe → reader exit 2 (§7 P2) |
| D-le-mksq-gzip | mksquashfs 4.7.5 | 1516 | LE gzip | 6 | 3 / 1 | files == tree; `unsquashfs`/`unblob` identical |
| D-le-mksq-xz | mksquashfs 4.7.5 | 1386 | LE **xz id 4** | 6 | 3 / 1 | files == tree; `unsquashfs`/`unblob` identical |
| S-le-mksq-gzip | mksquashfs 4.7.5 | 520 | LE gzip | 1 | 0 / 0 | files == tree; one sparse block decoded; `unsquashfs` identical |

A's contents: four data-block shapes (14000 B over four 4096 B blocks, exactly 4096 B,
4097 B, empty), a zero-length file, an empty directory, a space in a name, non-ASCII
**content** under an ASCII name, and four symlinks (`a/exact.bin` in-tree, a chain
`link-chain → link-same → a/exact.bin`, an absolute `/a/exact.bin`, and `../outside.txt`
escaping). B adds an absolute target, a self-loop, an escaping `../../etc/passwd`, and a
symlink to a directory that the generator drops (§7 P3).

What each carrier/fixture actually decodes (`--inspect` `decode_paths`), i.e. which code
paths have real evidence:

| image | compressed metadata | compressed data | sparse | fragment slices | xz-container |
|---|---|---|---|---|---|
| K1, K2 (BE) | 0 | 1 / 3 | 0 | 0 | – |
| **K3, K4 (BE)** | **2 each** | 0 | 0 | **4 each** | – |
| A, B/B-be (generator) | 0 | 6 / 3 | 0 | 0 | B uses raw LZMA2, not an XZ container |
| D (mksquashfs) | 2 | 4 | 0 | 3 | D-xz yes (id 4) |
| S (mksquashfs) | 2 | 2 | **1** | 0 | – |

So: **BE + compressed metadata + fragments are validated by K3/K4 themselves** (each
7-byte `apple*.txt` is a zero-block file whose bytes live in fragment 0: entry
`{start_block: 96, size: 25}` → 28 decompressed bytes, offsets 0/7/14/21), and the
committed oracle is what cross-checks my fragment reader. That also corrects the C1 draft's
"the lane generator writes none, but the unblob fixtures K3/K4 **may** use them": K3/K4 do
use fragments (`superblock.fragments == 1`).

## 6. Correction: symlink loops are *kept*, not removed

The draft's symlink rule is two-sided (resolves inside → kept, escapes → removed). A
third case exists and behaves like the kept side (under the runtime measured here, and
see the version pin below):

* measured: `unblob` 26.6.4's bundled interpreter is Python 3.13.16
  (`~/.local/share/uv/tools/unblob/bin/python3`); on a self-loop (`loop -> loop`) and a
  mutual loop (`a -> b`, `b -> a`) `Path.resolve()` returns the unresolved path instead
  of raising `RuntimeError` (checked with both the host 3.14.8 and the unblob venv
  3.13.16). `is_recursive_link` (`extractor.py:44-48`) therefore never fires,
  `is_safe_path` sees an inside path, and the link is kept.
  **This is an interpreter-version dependency, not a SquashFS rule**: on an interpreter
  whose `Path.resolve()` raises (pre-3.13 behaviour) `is_recursive_link` returns true and
  `fix_symlink` removes the link as `MaliciousSymlinkRemoved`, flipping the receipt from
  in-tree/gap to escaping/no-gap. The freeze should pin `unblob` 26.6.4 with its
  Python 3.13.16 runtime, or keep cycles out of the frozen six — the same carrier
  classified either way is otherwise an honest-looking evidence flip.
* measured end to end: `extractor-probes.txt` — unblob keeps `loop` in D-le-mksq-gzip and
  `self` in B-be-gzip, with **no** `MaliciousSymlinkRemoved` entry. A kept symlink is
  published as metadata only, so REA records an `unpublished-entry` gap for it, exactly
  as for an in-tree link.
* consequence for the oracle: `sqfs-list.py` classifies a loop as **in-tree** (kept,
  gap) and reports `symlink_reasons: {loop: n}` in `--inspect`. An empty target stays
  **escaping** (unblob unlinks it silently at `extractor.py:68-72`, so no gap) — that one
  is source-read only, because no writer on this host can create it.

The C1 oracle format stays two-column, but the claim sentence "a symlink whose target
resolves inside the extraction root is kept … a symlink that escapes is removed" is
incomplete for loops: either add "a symlink loop is kept (Python ≥3.13 no longer raises
in `Path.resolve()`)" or forbid loops in the frozen six (the lane generator *can* write
one — `os.symlink('self','self')` — so K5/K6 construction must exclude it deliberately).

### 6.1 Chains and cycles: what the reader's class means (independently confirmed)

A sibling seat (`R39C1SymlinkK1K4`) measured, on its own development BE carriers, that
unblob's class depends on the whole chain, not one lexical step, and that `fix_symlink`
rewrites kept targets. I reproduced all four outcomes on an image built here
(`extractor-probes.txt`, fixture `chains-le-gzip.sqsh`: `mksquashfs` 4.7.5, LE gzip, 7
symlinks + `hello.txt`):

| link (on-disk target) | reader class | unblob 26.6.4 outcome | leading target after rewrite |
|---|---|---|---|
| `x -> y`, `y -> ../outside.txt` | x escaping, y escaping | **both** removed, 2 `MaliciousSymlinkRemoved`, no gap for x | – |
| `p -> q`, `q -> hello.txt` | p in-tree, q in-tree | both kept, 2 gaps | `p -> hello.txt`, `q -> hello.txt` |
| `a -> b`, `b -> a` | a in-tree (loop), b in-tree (loop) | both kept, 2 gaps | `a -> a`, `b -> a` |
| `self -> self` | in-tree (loop) | kept, gap | `self -> self` |

The reader's resolver follows chains (it splices each link's target and re-resolves, up to
40 hops), so it agrees with unblob on all four rows — a one-step lexical classifier would
call `x` in-tree and be wrong.

**Target column caveat.** `symlinks.tsv` carries the **raw on-disk target**. `fix_symlink`
writes kept links back as `os.path.relpath(outdir.joinpath(target), start=path.parent)`,
so a kept chain is flattened (`p -> hello.txt`) and a kept cycle can become a self-loop
(`a -> a`), and even a plain target changes string if it is not already normalized
(`./hello.txt` → `hello.txt`). REA's `unpublished_entries[].link_target` is the
post-rewrite string. K1/K2 are stable (`../hello.txt` removed; `../../a/run.sh` rewritten
to the same string, which is what round-38 K2 `after.json` shows), but for a frozen
carrier containing a chain, a cycle or a non-normalized target the raw and rewritten
strings differ. The C1 predicate as drafted compares gaps and paths, not link targets, so
this is a documentation caveat rather than a predicate risk — and the cleanest freeze
rule is the one the sibling adopted: keep K5/K6 chain-free and cycle-free.

## 7. Freeze-facing findings: measured limits of `tools/round-37/gen-squashfs.py`

`generator-probes.py` / `generator-probes.txt`, all recomputed from the fixture images.

**P0 — `--comp xz` produces an image no stock extractor can read.** The writer maps
`COMP = {'gzip': 1, 'xz': 2}` (`gen-squashfs.py:8`) but compresses with a **raw LZMA2**
stream (`:22-29`, `lzma.FORMAT_RAW`, `dict_size = block_size`). On-disk id 2 means legacy
LZMA. Measured: `unsquashfs` 4.7.5 → `lzma uncompress failed with error code 7`,
`FATAL ERROR: writer: failed to read/uncompress file …/x/two.bin`, exit 1 (and it leaves a
0-byte `x/two.bin` behind); `sasquatch-v4be` 4.5.1 → tries every decompressor, then
`FATAL ERROR: writer: failed to read/uncompress file …/x/two.bin`, exit 1. My reader
decodes such images on purpose (FORMAT_AUTO → FORMAT_ALONE → raw LZMA2 with
`dict_size = block_size`), which is a superset of SquashFS 4.0 and is why B-le-xz passes
here while both real extractors fail. **A BE xz K5/K6 built with this generator would
fail the C1 after-run for handler reasons, not coverage reasons.** Use gzip for K5/K6, or
fix the generator (id 4 + XZ container) before the freeze.

**P1 — a non-ASCII *filename* writes a malformed image.** The dir entry size field is
`len(name) - 1` over `str` (`:146-148`) while the bytes appended are `name.encode()`.
Measured on `C-le-gzip` (tree: `plain.txt`, `é-name.txt`): directory body hex
`…0200000002000800706c61696e2e7478742400010002000900c3a92d6e616d652e747874` — the second
entry declares `size=9` (10 name bytes) but `é-name.txt` is 11 bytes, so the stream is one
byte out of step; the reader refuses with exit 2 (`metadata body out of bounds`) and
`unsquashfs` exits 1. Frozen K5/K6 and any held-out C2 carrier must use ASCII names (or
the generator must use `len(name.encode())`). K2's "unicode name" is safe because the
unicode is file **content**: `space name.txt` holds `unicode-é中.txt\n` (21 bytes,
`xxd` in §3 run), not a name.

**P2 — inode/dir refs break as soon as a table needs a second metadata block.**
`MetaWriter.append` returns `(len(self.blocks), offset)` (`:41-48`) and that block
**count** is stored as the ref's block field (`:109,116,145,159,161`), but
`squashfs_fs.h:130-136` defines the field as a **byte** offset from the table start.
Measured on `L-le-gzip` (300 one-byte files): inode table 10836 bytes = two 8192-byte
blocks; stored `root_inode = 0x0000000000010a30` (block field 1, offset 2608) where the
correct ref is `0x0000000020020a30` (byte offset 8194); the reader exits 2
(`metadata block at 397: decompression failed`) and `unsquashfs` exits 1
(`FATAL ERROR: read_inode: failed to read inode 397:2608`). The same convention is used
for `dir_header.start_block`, which the generator always writes as 0 (`:139-141`), so a
directory table over 8192 bytes is broken the same way. K1/K2 are unaffected (their
inode/directory tables are 382/212 and 348/185 bytes). **Constraint for the freeze: a K5/K6 tree built
with this generator must keep both the inode table and the directory table under 8192
bytes**, or the generator must be fixed first. Sizing notes: a file inode is 32 + 4 per
data block, a symlink 24 + target bytes, a dir inode 32; 300 one-byte files already
overflow, ~250 do not.

**P3 — symlinks whose target is a directory silently disappear.** `os.walk` lists them
in `dirnames`, while the writer only reads `fnames` (`:58-70`), so they never reach the
image. Measured: tree B has `abs, dot, self, up`; the image has `abs, self, up`
(`dot → .` dropped). If a K5/K6 tree is described as "symlink + …", a symlink to a
directory would silently make the carrier and its oracle disagree with the tree.

**P4 — metadata is never compressed by the generator** (`meta_header` always sets
`0x8000`, `:38-39,46,52`). Every generator image reports
`compressed_metadata_blocks: 0`. K5/K6 built with it add no compressed-metadata coverage;
that coverage only exists in K3/K4 (and in the mksquashfs fixtures).

## 8. Risks to the C1 freeze as drafted

1. `squashfs_v4_be` handler evidence for K5/K6 needs extractable images: **gzip, not
   `--comp xz`** (P0), unless the generator is fixed in the same freeze.
2. Both new carriers must stay under the 8192-byte inode/dir table limit (P2), and must
   avoid non-ASCII filenames (P1) and symlinks-to-directories (P3) — otherwise the frozen
   carrier is malformed and no honest after-receipt can exist.
3. The oracle (`oracle.tsv` + `symlinks.tsv`) should be produced **by this reader** (or
   cross-checked against it) rather than from the source tree alone, because the tree is
   not what the generator wrote in P1/P3 cases. For K1–K4 the reader and the tree agree
   exactly, so no frozen K1–K4 byte changes.
4. The symlink rule needs the loop sentence (§6), or a stated prohibition on loops in the
   frozen six. An empty-target link is removed without a report; if the frozen six may
   contain one, the rule needs that sentence too.
5. Symlink *chains* are classified by full resolution here and agree with unblob (§6.1),
   but the oracle's target column is the raw on-disk target while REA reports the
   rewritten one: chains, cycles and non-normalized targets make those strings differ.
   Chain-free, cycle-free, already-normalized symlinks keep the two columns identical
   (as in K2), which is the cheapest freeze rule.

6. Low priority, for the record: `carriers.json` describes K2 as "tree with symlink +
   unicode name"; the unicode is file content and the tree has no non-ASCII name. If a
   later revision regenerates K2 from a *new* tree, the phrase invites the P1 trap.
7. The C1 predicate's gap expectation (exactly the in-tree symlinks) is exactly what §3
   and §6 measured unblob to do on K1/K2, including the loop case; nothing else in the
   four carriers produces `unpublished-entry` gaps.

## 9. Limits (disclosed)

* **BE + sparse blocks is not exercised.** The only sparse-block image here is
  `S-le-mksq-gzip` (LE). The sparse path is endian-independent (the block-list entry is
  read with the same endian-prefixed `u32` as everything else), but the combination is
  `[INFERENCE]`, not measured; `mksquashfs` cannot write BE and the lane generator writes
  no sparse files.
* **Loop classification is environment-pinned**: measured against unblob 26.6.4 on its
  bundled Python 3.13.16 (§6). Under an interpreter that raises from
  `Path.resolve()` on a loop, `is_recursive_link` fires and the same link becomes
  `escaping`. Both directions are `[INFERENCE]` for other interpreter versions.
* **Empty symlink target** is classified `escaping` from source reading
  (`extractor.py:68-72`, removed with no report) and `[INFERENCE]` from source only: no
  writer here can create such an entry.
* **Compression ids 3 (lzo), 5 (lz4), 6 (zstd)** are refused with exit 2 by design; a
  carrier using them is out of scope for this reader and for the C1 claim.
* **Id 2 legacy LZMA** is accepted through FORMAT_AUTO/FORMAT_ALONE as well as the
  generator's raw LZMA2; the reader therefore accepts strictly more than the kernel.
* **Symlink chains inside images**: the reader resolves chains (up to 40 hops, `loop`
  at the limit) against the in-image tree, not against a materialised extraction. That
  matches unblob's `Path.resolve()` on a real extraction for everything measured here
  (K1, K2, A, B-be, D, and the chain/cycle fixture of §6.1); a chain through an omitted
  special file is untested.
* **Target strings are raw**: see §6.1 — unblob rewrites kept targets, so raw and
  rewritten strings differ for chains, cycles and non-normalized targets.
* **`--inspect` values are per run**: `decode_paths` counts what was actually decoded by
  that walk (a file inode is only read when its path is reachable from the root).
* No REA envelope was produced or read for this item; §3's REA-side statements cite the
  committed round-38 receipts only (K1 `after.json` 0 gaps, K2 `after.json` one
  `unpublished-entry` with `link_target`).

## 10. What I wrote, and what I did not touch

Wrote (all under `.ufo/waves/round-39/w1/`): `R39C1IndepReader.md` and everything under
`artifacts/R39C1IndepReader/` — `sqfs-list.py`, `check-oracles.py`,
`build-and-check.py`, `extractor-probes.py`, `generator-probes.py`, `README.md`, the four
transcripts (`oracle-check.txt`, `build-and-check.txt`, `extractor-probes.txt`,
`generator-probes.txt`), 14 carrier/fixture prefixes × four outputs (`files.tsv`, `symlinks.tsv`, `inspect.json`, `stderr.txt`), `images/`
(ten fixture images, the chain/cycle fixture included), `sources/squashfs_fs.h.v6.12`, `sha256sums.txt`.

Did not touch: `corpus/`, `tools/`, `plans/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`,
`SKILL.md`, `LOG.md`, the fleet repo, sibling lanes, `/home/vgpnk/Projects/shokuknow`.
No VCS command that mutates state was run; no file outside the lane was written. Scratch
(`/fast/scratch/hyaku/kaidoku-r39/R39C1IndepReader`) is removed.

No tool was installed or upgraded for this item (nothing was missing: `unsquashfs` 4.7.5,
`sasquatch-v4be` 4.5.1 (based on unsquashfs 4.5.1), `unblob` 26.6.4, `mksquashfs` 4.7.5,
Python 3.14.8 were already present).

Report: `.ufo/waves/round-39/w1/R39C1IndepReader.md`
