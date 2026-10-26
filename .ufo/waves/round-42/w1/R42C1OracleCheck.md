# R42C1OracleCheck — wave 1 report

Verdict: **CONFIRMED (with two material caveats)** — the unsquashfs 4.7.5
↔ 7-Zip oracle pair agrees **file-for-file only on gzip SquashFS v3**; on
OpenWrt Kamikaze 7.09 (lzma-adaptive v3) unsquashfs 4.7.5 cannot read the
image at all, and 7-Zip's *listing* cannot supply symlink targets (its
*extraction* drops/rewrites escaping links). The hypothesis holds as
stated for gzip v3; for lzma-adaptive v3 it must be restated (see §5).

---

## 1. Scope

Seat task: test the oracle hypothesis for R42-C1 —

> on real SquashFS 3.x rootfs images, `unsquashfs` 4.7.5 and 7-Zip agree
> file-for-file (relpath, sha256, size) AND agree with a direct
> `sasquatch` extraction (cross-check only, never the oracle).

Development inputs only:
- OpenWrt Kamikaze 7.09 (designated DEVELOPMENT) — 3 images, both
  endiannesses, all lzma-adaptive (see §2);
- unblob 26.6.4 SquashFS v3 test fixtures (git LFS, MIT) — gzip LE/BE
  (base + nopad + 1kpad + 4kpad), adaptive-lzma LE/BE, Broadcom `shsq`
  magic LE;
- synthetic v3 gzip images built from the format spec (attempt, §6).

Tools (versions): unsquashfs 4.7.5 (2026/03/01); 7-Zip 26.04
(2026-10-05); sasquatch 4.5.1 (unsquashfs 4.5.1-based); unblob
26.6.4; unsquashfs-backhand 0.25.5-v3 (L1-built, final `-k` kinds).

## 2. Development corpus (with pins)

| image | sha256 | endian | compression (detected) |
|---|---|---|---|
| OpenWrt Kamikaze 7.09 `atheros-2.6/openwrt-atheros-2.6-root.squashfs` | `70d7c4c7ce6794a627bdfb38a1efae45363888a194caef260f389be5241aff58` | BE (`sqsh`) | lzma-adaptive (`sasquatch`: "Detected lzma-adaptive compression"; `7z`: Method = LZMA Spec) |
| OpenWrt Kamikaze 7.09 `brcm47xx-2.6/openwrt-brcm47xx-2.6-squashfs.trx`, carve @0xB8000 | full image `42b0259f62505bd5573ca762fae6ec5799e602e87f9e9d6ce7676aacef5bb446`; carved `brcm.squashfs` sha256 `65f94c2c17b2b0d4b52c8e0915894596a48134ead7a0b05e48a6c9b7b6ae20d` | LE (`hsqs`) | lzma-adaptive |
| OpenWrt Kamikaze 7.09 `x86-2.6/openwrt-x86-2.6-squashfs.image`, carve @0x475800 | `a0a4fcf30e0a42fa09d1f6e9577d624ef78e402590f23549389a59e250441c12`; carved `x86.squashfs` sha256 `b6c8d5a1d8aa4aad88e328d8b7b74f3a7cd0d7f47f1f37f02a68235255d5c0e` | LE | lzma-adaptive |
| unblob v3 LE gzip `squashfs_v3_le.bin` | `0161351caec8e9da6e3e5ac7b046fd11d832efb18eb09e33011e6d19d50cd1f7` | LE | gzip (7z: ZLIB / SquashFS 3.0) |
| unblob v3 BE gzip `squashfs_v3_be.bin` | `4e9493d9c6f868005dea8f11992129c3399e0bcb8f3a966c750cb925989ca97c` | BE | gzip |
| unblob v3 BE gzip `squashfs_v3.be.nopad.bin` | `c1eb3ac360e453701bf080c7a6dd7486afbf1d218bc3193944292dd8f88392f0` | BE | gzip |
| unblob v3 LE gzip `squashfs_v3.le.nopad.bin` | `314d4bbe07b83f491e9987d7db39d8560945b2ae273ed23ead7e9d92250deb3c` | LE | gzip |
| unblob v3 adaptive BE `squashfs_v3_be.lzma.bin` | `71971c7a05d2d0b44bc976bc168f7b9134af8dc9fec83553889a9b5473469495` | BE | lzma-adaptive |
| unblob v3 adaptive LE `squashfs_v3_le.lzma.bin` | `2ac15e5c993f330854497b2fd032d2e87873a288fab6da2fe72106bb40b43124` | LE | lzma-adaptive |
| unblob v3 Broadcom LE `squashfs_v3_le.bin` (magic `shsq`) | `6baad4387dd51c8010de694420a35b6709706a268f7ba9e96e6417fb969f37d3` | LE | lzma+zlib mix (7z Method = LZMA ZLIB) |

Carve commands: `dd if=brcm.trx of=brcm.squashfs bs=1 skip=753664`, `dd
if=x86.image of=x86.squashfs bs=1 skip=4677120`; start offsets found by
scanning `hsqs`/`sqsh` magic; md5 of full images match the published
`md5sums` (e7d46481…, fd7bb329…).

## 3. Findings

### 3.1 gzip v3: full file-for-file agreement (LE and BE)

On the four gzip v3 images (LE/BE × base/nopad) all three + backhand
agree on the exact set of regular files and their bytes:

| image | unsq files | 7z files | sasq files | bh files | hash mismatches (any pair) |
|---|---|---|---|---|---|
| `squashfs_v3_le.bin` | 2 | 2 | 2 | 2 | 0 |
| `squashfs_v3_be.bin` | 2 | 2 | 2 | 2 | 0 |
| `squashfs_v3.le.nopad.bin` | 4 | 4 | 4 | 4 | 0 |
| `squashfs_v3.be.nopad.bin` | 4 | 4 | 4 | 4 | 0 |

`unsquashfs -s` rc 0 on all four; extraction of every regular file gives
identical sha256 and size across unsquashfs, 7z, sasquatch and backhand.

### 3.2 lzma-adaptive v3 (all three Kamikaze images + both adaptive fixtures):
unsquashfs 4.7.5 is USELESS

- `unsquashfs -s` prints a valid superblock (`Found a valid little/big
  endian SQUASHFS 3:0`…; rc 0).
- `unsquashfs -lls` / extraction FAILS: `gzip uncompress failed with
  error code -3`, `read_block: failed to read block`, `FATAL ERROR: File
  system corruption detected`; rc 1, no listing.
- Reason: 3.x filesystems are hardwired to gzip in unsquashfs-3.c
  (`comp = lookup_compressor("gzip")`); these images store LZMA-adaptive
  blocks. 7-Zip reads them ("Method = LZMA Spec"), sasquatch and
  backhand read them.

So the draft's oracle "unsquashfs + a second non-sasquatch reader" cannot
be applied to Kamikaze 7.09 carriers.

### 3.3 lzma-adaptive: 7-Zip ≡ backhand on regular files; symlink handling
is the dividing line

| image | bh regular files | 7z regular files | 7z-only regular files | sha diffs on intersection |
|---|---|---|---|---|
| atheros (BE) | 147 | 227 | 80 (all empty) | 0 |
| brcm (LE) | 156 | 236 | 80 (all empty) | 0 |
| x86 (LE) | 137 | 217 | 80 (all empty) | 0 |

7-Zip's 80 extra regular files are 0-byte placeholders for symlinks it
refuses to create. sasquatch tree ≡ backhand tree exactly (files, links,
dirs) on all three images (atheros 147/161/43, brcm 156/162/43, x86
137/151/42).

### 3.4 The three 7-Zip symlink classes (verified on brcm/x86 and on a
targeted 4 KiB probe)

1. **Same-directory / non-escaping relative targets → created correctly**
   (e.g. `bin/ash -> busybox`).
2. **Escaping relative targets (`../…`) → dropped**: `ERROR: Dangerous
   link path was ignored : sbin/halt : ../bin/busybox` (and 79 more per
   image); a **0-byte regular file** is written in its place.
   `7z x` exits rc 2 (Sub items Errors: 80; Archives with Errors: 1).
3. **Absolute targets → rewritten inside the output tree**: in the probe
   image, `/etc/passwd` became a symlink to `<outdir>/etc/passwd`
   (Sentinel's independent probe reproduces this exactly).

Consequence: a producer that ignores 7z stderr compares a silently
different, reduced tree; the draft's "no non-regular oracle entry as a
file" cannot be verified through 7z extraction alone.

### 3.5 How each tool presents inode kinds (observed on the dev corpus)

- **Regular files**: all tools identical on gzip v3; 7z content-matches
  backhand/sasquatch on lzma-adaptive.
- **Symlinks**: unsquashfs -lls and sasquatch -lls print `<name> ->
  <target>`; 7z -slt prints `Mode = lrwxrwxrwx` but **never the target**;
  backhand -l prints plain paths (targets only visible by extraction, where
  they are preserved).
- **Empty files**: listed by all; extracted with size 0 by all (the only
  empty "files" 7z adds are the dropped-link placeholders, §3.4).
- **Hard links**: none present in any dev image (superblock nlink seen
  only on symlinks; no inode with nlink>1). Not observable in the dev
  corpus.
- **Devices / fifos / sockets**: none present in any dev image
  (Kamikaze rootfs `/dev` is empty; unblob fixtures are regular-file
  only). Not observable in the dev corpus.
- **UTF-8 names**: none present in the dev corpus (all ASCII); all
  listing tools advertise UTF-8 ("Code Page = UTF-8" in 7z).

### 3.6 Path-normalisation traps (exact, measured)

| trap | unsquashfs -lls | sasquatch -lls | 7z -slt | backhand -l |
|---|---|---|---|---|
| leading `./` | none | none | none | none |
| listing root prefix | `squashfs-root/…` on every row | `squashfs-root/…` on every row | none (bare relpath) | `/`-prefixed, root line `/` |
| trailing slash on dirs | none | none | none | none |
| extraction prefix | dest as given via `-d` | dest as given via `-dest` | no prefix | dest as given via `-d` |

The `squashfs-root/` prefix on unsquashfs/sasquatch listings must be
stripped one segment before comparing with 7z/backhand paths (freeze this
strip). 7z -slt also emits one pseudo-entry whose `Path` equals the
archive filename (archive header), which must be filtered.

### 3.7 Cross-check vs sasquatch (the extractor unblob runs)

On every image that sasquatch can read it matches unsquashfs (gzip) or
backhand (lzma-adaptive) file-for-file on regular files, and its symlink
targets match unsquashfs. `sasquatch -lls` auto-detects the superblock
endianness; forcing the wrong endian (`-be` on an LE image) fails with
rc 1 "Block size or block_log too large". `sasquatch -le` on LE lzma
works (rc 0).

### 3.8 unblob / REA relevance

`unblob 26.6.4` handler `squashfs_v3` matches magic `hsqs`/`sqsh` +
major 3; `squashfs_v3_broadcom` matches `shsq`. The Broadcom fixture is
read by 7z (Method LZMA ZLIB) and sasquatch/backhand but NOT by
unsquashfs 4.7.5 (`FATAL ERROR: Can't find a valid SQUASHFS superblock`
because of the `shsq` magic). REA 6.5.0 `extract-firmware --max-depth 1`
succeeds on the lzma-adaptive fixtures (handler `squashfs_v3`,
extraction_failed false), i.e. the *extraction* story is fine; only the
oracle-reader story is constrained.

## 4. Oracle recommendation (feeds the freeze)

- On **gzip v3 carriers**: oracle = unsquashfs 4.7.5 (`-lls` for types +
  sizes, `-d` extraction for digests) + 7-Zip (listing `-slt` for
  paths/modes/sizes; extraction for digests). Verified identical.
- On **lzma-adaptive v3 carriers** (all three Kamikaze 7.09 images):
  unsquashfs cannot participate. The L1-selected producer 1
  (`unsquashfs-backhand`, kind `*_v3_0_lzma`) agrees with 7-Zip on 156/156
  (brcm), 147/147 (atheros), 137/137 (x86) regular files — sha256 and
  path— and matches sasquatch's full tree including symlinks. This is the
  only non-sasquatch reader that can supply the non-regular table
  (symlink targets) on these carriers.
- Freeze: the one-segment `squashfs-root/` strip for unsquashfs and
  sasquatch listings; the 7z archive-header pseudo-entry filter; and the
  `-d`/`-dest` extraction roots. Record the 7z symlink divergence (drop →
  0-byte file, absolute → rewrite) as an expected-divergence rule, not a
  mismatch, for any carrier with `..`/absolute symlinks (every Kamikaze
  image has ~80 `../bin/busybox` links plus absolute `/etc/...`,
  `/tmp/...`, `/proc/...` links).
- Carrier selection implication: if carriers are to stay Kamikaze 7.09
  (or any OpenWrt-era lzma-adaptive rootfs), the oracle pair is
  **backhand + 7-Zip** (with the caveats in §3.4); unsquashfs 4.7.5 is
  usable only as a third producer on gzip v3 images (e.g. unblob-style
  fixtures, but those are C2 inputs, never C1 carriers).

## 5. Hypothesis verdict

- **gzip v3**: CONFIRMED — unsquashfs 4.7.5 ≡ 7-Zip ≡ sasquatch ≡
  backhand file-for-file.
- **lzma-adaptive v3**: PARTIALLY CONFIRMED with a restatement —
  unsquashfs cannot read the images; 7-Zip ≡ backhand (≡ sasquatch
  cross-check) on regular files; symlink targets come from backhand (or
  sasquatch), never from 7z.

## 6. Synthetic v3 writer (artifact `gen_v3.py`) — status

Built to close the presentation gaps (devices/fifo/hardlinks/UTF-8) not
present in the dev corpus:

- Exact v3.0 structural facts recovered from squashfs-tools 4.7.5 source
  (`squashfs_compat.h`, `unsquash-3.c`, `unsquash-123.c`) and from byte
 -level decoding of the unblob fixtures:
  - **packed 119-byte superblock** (no alignment pad between `no_guids`
    and `mkfs_time`; `root_inode` = `(byte_offset << 16) | offset`, no
    type bits);
  - base inode = 20 bytes (type:4 mode:12 uid:8 gid:8 bitfields + mtime
    + inode_number); reg=36, symlink=26+target, dir=36, dev=26, fifo/
    socket=24;
  - directory header = 12 bytes (`count:8` word + start_block + inode
    number), entry = 6 + name (offset:13 | type:3 | size:8 word + 16-bit
    inode number);
  - validation rules: `no_guids==0 ⇒ guid_start==0`; `uid_start <
    table_start`; `fragments==0 ⇒ fragment_table_start == uid_start`;
    `lookup_table_start == 0xFFFFFFFFFFFFFFFF` skips the exports table;
    dir-inode `start_block` is relative to the directory table, dir-entry
    `start_block` relative to the inode table.
- Current state: superblock parses cleanly in all four readers; readers
  advance to the directory scan (unsquashfs/sasquatch: "invalid
  characters in name"; backhand: empty listing); the residual defect is
  the directory-entry/header encoding (still being pinned down against
  real Kamikaze directory tables when the round ended). The writer and
  its findings are included for the L1 to finish if the synthetic
  special-file matrix is wanted at freeze time; the real dev corpus
  (§2) already covers symlink classes, empty files and gzip+lzma
  compression; it does not cover devices/hardlinks/UTF-8.

## 7. Evidence

- Artifacts: `oracle_check.py` (harness), `gen_v3.py` (v3 writer),
  `matrix_final.json` (final agreement matrix), `evidence_commands.txt`
  (exact commands, outputs and exit codes).
- Key commands (all run from `$S` = `/fast/scratch/hyaku/kaidoku-r42/R42C1OracleCheck`):
  - `unsquashfs -s|-lls <img>`; `unsquashfs -no-progress -d <dest> <img>`
  - `7z l -slt <img>`; `7z x -y -o<dest> <img>` (rc 2 on Kamikaze:
    80 sub-item errors, all "Dangerous link path was ignored")
  - `sasquatch -lls <img>`; `sasquatch -dest <dest> <img>`
  - `unsquashfs-backhand -k <kind> -l|-d <img>`
  - `python3 oracle_check.py --work work <imgs…>` (full pairwise matrix)
- Fixture downloads: `https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/<handler>/<endian>/__input__/<file>` (MIT, small; sha256 pins in §2).
- Kamikaze downloads: `https://archive.openwrt.org/kamikaze/7.09/<target>/…` (designated DEVELOPMENT; pins in §2).
- Tool installs this round: none (all readers already present; no new
  tools installed).
