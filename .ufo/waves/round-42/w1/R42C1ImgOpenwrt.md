# R42C1ImgOpenwrt — OpenWrt Kamikaze SquashFS v3 candidate carriers (round 42, wave 1)

**Verdict: DONE — with two DEFECTS FOUND in the draft as written.** Both defects are measured, and the one
that blocks the oracle is already resolved by the L1's `backhand-cli` decision, which I have now validated on
all ten candidates (§3.3: 10/10 exact regular-file agreement between `unsquashfs-backhand 0.25.5` and
`7-Zip 26.04`). The second — `--max-depth 1` cannot reach a squashfs inside a TRX chunk — is still open and
decides which carriers are admissible.

Recon is complete for **10 candidates**, every one a genuine SquashFS **3.0** rootfs (`squashfs_v3` handler,
magic `hsqs`/`sqsh`, block 65536, LZMA). Four are ranked for a depth-1-viable C1 set; three TRX images are
marked unusable at `--max-depth 1`.

Artefacts: `.ufo/waves/round-42/w1/artifacts/R42C1ImgOpenwrt/` — `c1-openwrt-probe.py` (fetch/carve/reader
probe), `c1-backhand-crossread.py` (backhand × 7-Zip), `carriers-candidates.json` (10 records in the
fetch-carrier schema + `chunk_end`), `candidates-summary.tsv`, `chunk-and-readers.tsv`, `oracle/`,
`nonregular/`, `backhand/`, `readers/`, `dev-probes/`, `candidates-full.json`.

---

## 0. Headline findings

1. **All ten OpenWrt 8.09.x squashfs images are LZMA, not gzip** (7-Zip: `Method = LZMA Spec`; stdlib decode
   proves raw LZMA1 without a header, §3.4). `unsquashfs` 4.7.5 reads the superblock (`-s`, exit 0) but fails
   for `-lls` and `-d` on **10/10** (`gzip uncompress failed with error code -3` → `FATAL ERROR: File system
   corruption detected`, exit 1). So **OpenWrt cannot supply a gzip-v3 carrier**, and `unsquashfs` cannot be a
   producer for any OpenWrt carrier. This is the defect the L1's `backhand-cli 0.25.5` (`-k le_v3_0_lzma` /
   `be_v3_0_lzma`) decision fixes — and it works here: 10/10 carriers extract, §3.3.
2. **`--max-depth 1` cannot reach a squashfs inside a TRX chunk.** REA passes `--depth <max_depth>` straight
   to unblob (`rea-agents/dist/firmware/FirmwareProvider.js:230-231`). Measured on a development image: a TRX
   input at `-d 1` yields **only `TRX_V1`** and writes `part0/part1/part2` unexamined — no SquashFS chunk at
   all; at `-d 2` the `SQUASHFS_V3` chunk appears and is extracted. Three of the ten candidates are TRX
   (`OW-8.09-brcm24`, `OW-8.09.2-brcm47xx`, `OW-8.09.2-adm5120-be`) → **inadmissible at the frozen REA
   parameters**. Plain, offset-embedded, `W54G`-header and uImage-prefixed images are all reachable at
   `-d 1` (measured, §4.2) → the other seven are admissible.
3. **Two producers agree exactly on the real carriers**, regular files only, path + size + sha256:
   `unsquashfs-backhand 0.25.5` vs `7-Zip 26.04`, **10/10 carriers, 385–425 files each, zero differences**
   (`only_backhand = 0`, `only_7z = 0`, `content_mismatch = 0`), and the symlink path sets are identical too
   (167–178 per carrier).
4. **7-Zip is not a faithful symlink producer**, which is why the non-regular table must come from backhand.
   Per carrier `7z x` refuses 103–105 links as `Dangerous link path` (exit **2**), **materialises each refusal
   as a 0-byte regular file** (102–104 phantoms; an extraction-tree oracle would publish them as files and trip
   `P42-C1`'s "no non-regular oracle entry as a file"), and **rewrites the 6 absolute-target links** to point
   inside its extraction root (`etc/TZ → /tmp/TZ` becomes `<dest>/tmp/TZ`). Backhand extracts **all** links
   with the original targets (`/tmp/TZ`, `/proc/mounts`, `var → /tmp`, …).
5. `chunk_end` (the REA input extent) is `bytes_used` rounded up to 4096 on every candidate, tail verified to
   be exactly zero padding (119–3984 pad bytes); `chunk_end_sha256` recorded per carrier (§5).
6. **No OpenWrt-only 4-carrier set satisfies "two or more publishers"** — all ten are one publisher. Depth-1
   viability, oracle readiness and publisher diversity together require at least one non-OpenWrt carrier
   (DD-WRT `tqsh` / vendor v3), which is another seat's surface.

---

## 1. Search surface and reservation compliance

| item | value |
|---|---|
| releases walked | `https://archive.openwrt.org/kamikaze/{8.09,8.09.1,8.09.2}/` (index, per-target index, `md5sums`, `release.txt`) |
| targets inspected | brcm47xx, brcm-2.4, atheros, ar71xx, x86, ppc40x, ppc44x, rb532, adm5120/router_be, ar7, ixp4xx, rdc |
| candidates probed | 10 (§2) |
| REA / unblob / sasquatch run on a candidate | **none** |
| candidate readers used | `unsquashfs -s/-lls/-d`, `7z l/x`, `unsquashfs-backhand` (`-s/-l/-d`), pure Python byte parsing |
| extractors run on development inputs | yes, deliberately: unblob 26.6.4 + sasquatch 4.5.1 on the OpenWrt **7.09** images (designated DEVELOPMENT), on the two unblob `squashfs_v3_adaptive` fixtures, and on two synthetic files I built from the 7.09 rootfs |
| tooling installs/upgrades | none. Existing binaries only: `unblob 26.6.4` (commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`), `sasquatch`/`sasquatch-v4be` (banner `unsquashfs version 4.5.1 (2022/03/17)`), `unsquashfs 4.7.5 (2026/03/01)`, `7-Zip 26.04 (x64)`, `unsquashfs-backhand 0.25.5` (L1-built, read-only use). No pacman, no writes to `~/.local/bin` |

Scratch `/fast/scratch/hyaku/kaidoku-r42/R42C1ImgOpenwrt` is deleted at the end of this seat. No third-party
image bytes were copied into the lane; the oracle tables in `artifacts/…/oracle/` are path/size/sha256 rows.

---

## 2. Candidate inventory (all ten: SquashFS 3.0, `squashfs_v3`)

`fs_end` = SquashFS endianness; `ELF` = endianness of the first data block's busybox ELF (independent check
that the rootfs matches the target arch); `pad` = zero padding between `bytes_used` and `chunk_end`;
`d1` = reachable at REA `--max-depth 1` (§4.2).

| id | release/target | container | sb offset | magic | fs/ELF | bytes_used | chunk_end (pad) | reg | dir | lnk | dev | backhand mkfs (UTC) | d1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OW-8.09.2-atheros | 8.09.2 / atheros | plain | 0 | `sqsh` | BE/BE | 1560688 | 1564672 (3984) | 409 | 95 | 177 | 0 | 2009-12-29T14:56:30Z | ✅ |
| OW-8.09-ar71xx | 8.09 / ar71xx | plain | 0 | `sqsh` | BE/BE | 1606549 | 1609728 (3179) | 416 | 95 | 178 | 0 | 2009-02-14T21:41:30Z | ✅ |
| OW-8.09-x86-fs | 8.09 / x86 | plain | 0 | `hsqs` | LE/LE | 1182197 | 1183744 (1547) | 403 | 94 | 167 | 0 | 2009-02-15T01:46:35Z | ✅ |
| OW-8.09.2-x86-img | 8.09.2 / x86 | plain, sb at 4 677 120 (x86 boot image) | 4677120 | `hsqs` | LE/LE | 1360991 | 1363968 (2977) | 425 | 93 | 167 | 0 | 2009-12-29T17:30:19Z | ✅ |
| OW-8.09.1-ppc40x | 8.09.1 / ppc40x | uImage kernel + squashfs at 2 MiB | 2097152 | `sqsh` | BE/BE (PowerPC) | 1168293 | 1171456 (3163) | 385 | 93 | 167 | 0 | 2009-06-02T01:01:37Z | ✅ |
| OW-8.09.2-ppc44x | 8.09.2 / ppc44x | uImage kernel + squashfs at 2 MiB | 2097152 | `sqsh` | BE/BE (PowerPC) | 1168961 | 1171456 (2495) | 386 | 93 | 167 | 0 | 2009-12-29T16:45:54Z | ✅ |
| OW-8.09.1-wrt54g | 8.09.1 / brcm47xx | `W54G` 32-byte header | 775200 | `hsqs` | LE/LE | 1322493 | 1323008 (515) | 403 | 94 | 169 | 0 | 2009-06-01T23:40:40Z | ✅ |
| OW-8.09-brcm24 | 8.09 / brcm-2.4 | **TRX v1** | 503808 | `hsqs` | LE/LE | 1578187 | 1581056 (2869) | 412 | 95 | 175 | 0 | 2009-02-14T22:44:39Z | ❌ |
| OW-8.09.2-brcm47xx | 8.09.2 / brcm47xx | **TRX v1** | 775168 | `hsqs` | LE/LE | 1322889 | 1323008 (119) | 404 | 94 | 169 | 0 | 2009-12-29T15:32:54Z | ❌ |
| OW-8.09.2-adm5120-be | 8.09.2 / adm5120/router_be | **TRX v1** | 733184 | `sqsh` | BE/BE | 1299434 | 1302528 (3094) | 407 | 94 | 168 | 0 | 2009-12-29T14:12:47Z | ❌ |

Machine-readable: `artifacts/…/candidates-summary.tsv` (30 columns incl. HTTP status, access time,
`Last-Modified`, sha256, publisher md5 + match) and `chunk-and-readers.tsv` (carve offset / bytes_used /
chunk_end / pad / chunk sha256 / carve sha256 / backhand & 7-Zip counts).

All ten: `File System = SquashFS 3.0`, `block_size = 65536` (backhand `block_size: 0x010000`,
`block_log: 0x10`), `version_major.minor = 3.0` (backhand and my own parse agree), `no_uids = 1`,
`no_guids = 0`, `flags = 0x40` (DUPLICATES_REMOVED), `lookup_table_start = 0xFFFFFFFFFFFFFFFF` (v3 has none).

Container chains, with the self-consistency evidence for the carve offsets:

* **TRX** (`HDR0`, v1): `trx_len` == file size exactly; `offsets[1]` == squashfs superblock offset in all
  three (503808 / 775168 / 733184). `OW-8.09-brcm24`: `crc32=13a80633 flags=0 version=1
  offsets=[28,2308,503808]`. v1 has no lengths array.
* **uImage** (`0x27051956`, 64-byte header): ppc40x `os=5 arch=7(PowerPC) type=2 compression=1(gzip)
  data_size=1023314 name="Linux-2.6.26.8"`; ppc44x `data_size=1039637`. Payload ends at 1 023 378 < 2 MiB, so
  the squashfs is a **separate** chunk after zero padding — not nested.
* **`W54G`** (Linksys/Broadcom 32-byte header): sb at 775200 = 775168 + 32 — the TRX-era layout with the TRX
  header replaced by the device header.
* **x86 disk image**: boot sector at 0, squashfs at 4 677 120, 80 805 bytes tail after the chunk.
* **plain**: sb at 0.

Magic scan over all eight SquashFS magics (`hsqs sqsh sqlz zlqs qshs shsq tqsh hsqt`) found **exactly one**
handler-matching offset per image — no second filesystem, no vendor-magic variant anywhere.

Publisher provenance: the per-target `md5sums` file lists the filename and digest, and the computed md5 of
every download **matches** (10/10, `md5_matches = True`). `Last-Modified` also equals `mkfs_time` to the
second in 9/10 (`OW-8.09.2-atheros`: mkfs 14:56:30 vs 14:56:31).

---

## 3. Readers and the oracle

### 3.1 `unsquashfs` 4.7.5 — superblock only

```
$ unsquashfs -s OW-8.09.2-atheros.sqfs            # exit 0
Reading a different endian SQUASHFS filesystem on …
Found a valid big endian SQUASHFS 3:0 superblock on …
Filesystem size 1560688 bytes (1524.11 Kbytes / 1.49 Mbytes)
Block size 65536
Number of fragments 29 / Number of inodes 682 / Number of uids 1 / Number of gids 0

$ unsquashfs -lls OW-8.09.2-atheros.sqfs          # exit 1, 10/10 candidates
gzip uncompress failed with error code -3
read_block: failed to read block @0x17cfa2
read_fragment_table: failed to read fragment table block
FATAL ERROR: File system corruption detected
```

The same failure occurs on the unblob fixture `squashfs_v3_le.lzma.bin` (`FATAL ERROR: read_inode: failed to
read inode 132:64`, exit 1), so it is a reader limitation, not a carrier defect. `-s` never names a
compressor: v3 has **no compression-id field**; the codec has to be inferred from the block bytes (§3.4).

### 3.2 `7-Zip 26.04` — a real v3-LZMA reader with a lossy writer

```
$ 7z l -slt OW-8.09.2-atheros.sqfs                # exit 0
Type = SquashFS
Physical Size = 1560688
File System = SquashFS 3.0
Method = LZMA Spec
Cluster Size = 65536
Big-endian = +
Created = 2009-12-29 11:56:30
Characteristics = DUPLICATES_REMOVED
```

Every entry carries `Mode` (`-rwxr-xr-x` / `drwxr-xr-x` / `lrwxrwxrwx`), which is the reliable type source
(`Folder = +` also marks directories). Extraction completeness across the ten: **0 regular files missing, 0
size mismatches**.

Extraction is lossy for links, on every candidate:

```
ERROR: Dangerous link path was ignored : usr/bin/passwd : ../../bin/busybox
Sub items Errors: 102                                        # exit code 2
-rw-r--r-- 1 … 0 z-extract/usr/bin/passwd                    # 0-byte phantom regular file
```

counts: 177 typed links → 103 refused → 102 phantoms (atheros); 169 → 105 → 104 (brcm47xx); etc. And the six
absolute-target links are **rewritten** (`etc/TZ` should be `/tmp/TZ`, 7-Zip stores
`<zx-dir>/tmp/TZ`; same for `etc/fstab`, `etc/mtab`, `etc/ppp/resolv.conf`, `etc/resolv.conf`, `var`).
Consequences for C1: type the oracle from `7z l -slt` `Mode` (never from the extraction tree), and take
**symlink targets and the non-regular table from backhand**, not from 7-Zip.

### 3.3 `unsquashfs-backhand 0.25.5` × `7-Zip 26.04` on the actual carriers — 10/10 exact

`-k be_v3_0_lzma` / `le_v3_0_lzma`, `-s` for the superblock, `-d` for the tree (symlinks extract as symlinks).
Agreement computed two ways: backhand tree (lstat-typed) vs 7-Zip typed listing (path) with content from
`7z x`.

| carrier | backhand reg | 7z typed reg | path set | size+sha256 | links bh/7z | link path set | link target diffs |
|---|---|---|---|---|---|---|---|
| OW-8.09.2-atheros | 409 | 409 | identical | identical | 177 / 177 | identical | 6 (all absolute) |
| OW-8.09-ar71xx | 416 | 416 | identical | identical | 178 / 178 | identical | 6 |
| OW-8.09-x86-fs | 403 | 403 | identical | identical | 167 / 167 | identical | 6 |
| OW-8.09.2-x86-img | 425 | 425 | identical | identical | 167 / 167 | identical | 6 |
| OW-8.09.1-ppc40x | 385 | 385 | identical | identical | 167 / 167 | identical | 6 |
| OW-8.09.2-ppc44x | 386 | 386 | identical | identical | 167 / 167 | identical | 6 |
| OW-8.09.1-wrt54g | 403 | 403 | identical | identical | 169 / 169 | identical | 6 |
| OW-8.09-brcm24 | 412 | 412 | identical | identical | 175 / 175 | identical | 6 |
| OW-8.09.2-brcm47xx | 404 | 404 | identical | identical | 169 / 169 | identical | 6 |
| OW-8.09.2-adm5120-be | 407 | 407 | identical | identical | 168 / 168 | identical | 6 |

`only_backhand = 0`, `only_7z = 0`, `content_mismatch = 0` on all ten; `symlink_path_set_identical = True` on
all ten. Raw: `artifacts/…/backhand-crossread.json`, `artifacts/…/backhand/<id>.sv.tsv`.
Backhand's independent superblock dump agrees with my own parse on every field I checked
(`version_major/minor`, `block_size`, `inode_count`, `fragments`, `flags`, `bytes_used`, `mkfs_time`) — a
second, independent superblock read for `P42-C1`'s superblock binding.

### 3.4 The codec, verified (also the reason a lane reader is feasible)

v3 metadata blocks: `u16 header` (bit 15 = uncompressed, low 15 bits = stored size, filesystem endianness)
then the block; **data blocks have no header** — their lengths live in the inode block-size list. The codec is
**raw LZMA1, no 13-byte `.lzma` header, `lc=3 lp=0 pb=2`, dict ≥ 64 KiB**:

```
OW-8.09.2-atheros  inode_table @1549296   header=0x085a stored=2138  -> 8192 bytes  (eof)
                   directory_table        header=0x127a stored=4730  -> 8192 bytes  (eof)
                   data block 0 @119     (no header)               -> 65536 bytes, 7f454c4601020100
                                                                      (ELF32, MSB, MIPS)
```

True for all ten (`stdlib_reader_feasible = true`); the first data block's ELF machine matches the target:
MIPS BE (atheros, ar71xx, brcm-2.4, brcm47xx, wrt54g, adm5120-be), PowerPC BE (ppc40x, ppc44x), i386 LE
(x86-fs, x86-img). 7-Zip's label "LZMA Spec" is a naming artefact — there is no LZMA header in the stream.

---

## 4. The extractor path, measured on development inputs only

### 4.1 unblob 26.6.4 + sasquatch 4.5.1 on the OpenWrt v3-LZMA format

```
$ cd "$S" && unblob -f -d 2 -e out dev709/709-openwrt-atheros-2.6-root.squashfs      # rc=0
chunk=0x0-0xf4000 handler=squashfs_v3
command='sasquatch -be -no-exit-code -f -d …/0-999424.squashfs_v3_extract …/0-999424.squashfs_v3'
Extracted files: 148 / directories: 44 / links: 162            (309 entries in the output tree)

$ unblob -f -d 2 -e out dev709/709-openwrt-brcm47xx-2.6-squashfs.trx                  # rc=0
TRX_V1 1.82 MB → SQUASHFS_V3 1.02 MB (nested) → 326 entries
```

So sasquatch extracts the OpenWrt LZMA v3 variant with only `-be`/`-le` (no `-comp` flag), and unblob's
`squashfs_v3` handler is the matching one. `unblob --show-external-dependencies` → `7z ✓ sasquatch ✓
sasquatch-v4be ✓`.

### 4.2 The depth ladder — this is what constrains carrier choice

| input | `-d 1` | `-d 2` | `-d 3` |
|---|---|---|---|
| plain squashfs (7.09 atheros rootfs) | `SQUASHFS_V3` **extracted**, 309 entries | 309 entries | — |
| TRX (7.09 brcm47xx trx) | **`TRX_V1` only**, parts written unexamined (`part0` 2260, `part1` 751376, `part2` 1150976), **no SquashFS chunk**, 3 entries | `SQUASHFS_V3` found + extracted, 326 entries | 328 entries |
| synthetic 2 MiB prefix + squashfs (no typed container) | `SQUASHFS_V3` **extracted**, 310 entries | — | — |
| synthetic PPC uImage header + 1 MB gzip payload + zeros + squashfs at 2 MiB | `SQUASHFS_V3` **extracted**, 312 entries | — | — |

Synthetic inputs (built from the 7.09 rootfs, scratch only, never in the lane): `offset-synth = 2 MiB of 0xAA ‖
7.09 atheros root.squashfs`; `uimage-synth = 64-byte PPC uImage header (os=5 arch=7 type=2 comp=1
name="Linux-2.6.26.8") ‖ 1023314-byte gzip payload ‖ zeros to 2 MiB ‖ 7.09 root.squashfs`. They reproduce the
exact geometry of `OW-8.09.2-x86-img` and `OW-8.09.1-ppc40x`.

Rule deduced (used for the `d1` column in §2): **a chunk nested inside another chunk needs depth ≥ 2; a
squashfs merely at an offset (no enclosing handler) is found and extracted at depth 1.** unblob has **no
uImage handler** (`grep -rn '27051956|uimage|uboot'` over the whole handler tree: no hits) and no `W54G`
handler, so those headers are untyped and cost no depth level.

### 4.3 unblob fixture tree (evidence for the handler family; C2-owned, never a C1 carrier)

`tests/integration/filesystem/squashfs/` at `1fcc7a0a…` has ten handler directories; the v3 family is
`squashfs_v3{,/_adaptive/_broadcom/_ddwrt/_nonstandard}`. **`squashfs_v3_adaptive` is the LZMA-under-standard-
magic case** (`squashfs_v3_{le,be}.lzma.bin`, sha256 `2ac15e5c…`, `71971c7a…`). There is **no
`squashfs_v3_adaptive` handler class** in the installed package: those fixtures are matched by the plain
`squashfs_v3` pattern and extracted by plain `sasquatch -le/-be` — exactly the OpenWrt situation. Both fixtures
ran clean (`SQUASHFS_V3 100.00%`, 3 files, rc=0).

### 4.4 Cross-extractor agreement on a development image of this format

`artifacts/…/dev-probes/agreement/agreement-dev-709-atheros.txt` (7.09 atheros rootfs, sha256 `70d7c4c7…`):

* unblob+sasquatch regular files: **147**; 7-Zip typed regular files: **147**; identical path set, identical
  size+sha256 (147/147)
* 162 typed symlinks: 7-Zip created 81 and 80 phantoms; sasquatch's tree holds all 162 (`var` is a
  link-to-directory, which naive `os.walk` folds into `dirnames`)
* unblob logs `Ignoring special file (link, chrdev, blkdev, fifo, socket, door)` while recursing → the
  pipeline never publishes link files, so **every symlink must be accounted for by a REA gap row**

Round-41 precedent for that machinery (read-only): `corpus/evidence/round-41/c1/V3/after.json` has 85
`unpublished-entry` occurrences and one `depth-limited`; `V4` has 611 + 12 `MaliciousSymlinkRemoved` + one
`depth-limited`. ~170 symlink gaps per OpenWrt carrier is inside proven range.

---

## 5. carriers.json-ready records

Schema from `artifacts/R42C1Fetch/schema.md` §1, plus the L1's `chunk_end` addition. Per the schema,
`carve.bytes_used` stays the pin extent; `chunk_end` / `chunk_end_sha256` are record level (no unknown keys
inside `carve`). Full set of ten in `artifacts/…/carriers-candidates.json`.

**Recommended four** (all depth-1 viable; 2 BE / 2 LE; 4 distinct container shapes; 3 releases):

```json
{"id": "OW-A8092", "url": "https://archive.openwrt.org/kamikaze/8.09.2/atheros/openwrt-atheros-root.squashfs",
 "image_sha256": "b3d3008edf9cf77597457e83750d42080bffbf2f531e08624030b8d099608967",
 "carve": {"offset": 0, "bytes_used": 1560688,
           "sha256": "a50a11e05b072b62e88d989c050663887ee13a9ba5016abdbeb781184e0b3781"},
 "chunk_end": 1564672, "chunk_pad_bytes": 3984, "chunk_end_sha256":
     "35f777eb38d6597f1621e40c073933c6095951f67da19ada22a9ec882d4b4d96",
 "kind": "distribution", "handler": "squashfs_v3", "depth1_viable": true,
 "product": "OpenWrt Kamikaze 8.09.2, atheros target rootfs (Atheros AR531x/231x based routers), MIPS big-endian, plain squashfs",
 "publisher": "OpenWrt (archive.openwrt.org)",
 "oracle": "corpus/evidence/round-42/c1/OW-A8092/oracle.tsv",
 "nonregular": "corpus/evidence/round-42/c1/OW-A8092/nonregular.tsv"}

{"id": "OW-X86FS", "url": "https://archive.openwrt.org/kamikaze/8.09/x86/openwrt-x86-squashfs.fs",
 "image_sha256": "48d2c54d13370e2d7487525480071208ee911f0ecfae0ad915afc0421310bef8",
 "carve": {"offset": 0, "bytes_used": 1182197,
           "sha256": "0246e81937552775545fd3b1d287439ccafd64531b5ff9b710f2853e67e292ea"},
 "chunk_end": 1183744, "chunk_pad_bytes": 1547, "chunk_end_sha256":
     "12a2fd588e9344f178c1a33f8cc58780779dcbc2d875502bebd4ecce75433fb6",
 "kind": "distribution", "handler": "squashfs_v3", "depth1_viable": true,
 "product": "OpenWrt Kamikaze 8.09, x86 target squashfs rootfs, i386 little-endian, plain squashfs",
 "publisher": "OpenWrt (archive.openwrt.org)",
 "oracle": "corpus/evidence/round-42/c1/OW-X86FS/oracle.tsv",
 "nonregular": "corpus/evidence/round-42/c1/OW-X86FS/nonregular.tsv"}

{"id": "OW-PPC40X", "url": "https://archive.openwrt.org/kamikaze/8.09.1/ppc40x/openwrt-ppc40x-squashfs.img",
 "image_sha256": "d67bbe986581cb88728db64373bb7490e5fe6c6bfb4ac76a43bdf75d0207f788",
 "carve": {"offset": 2097152, "bytes_used": 1168293,
           "sha256": "04c3920d6882f05bc71fa40e2c43ddadcfa1ea2245044b35f8599ca0af3726d2"},
 "chunk_end": 1171456, "chunk_pad_bytes": 3163, "chunk_end_sha256":
     "a97e43ff1e3d0b1d3b0f1e8630993a35adef908973e3e4101fcb6e3fa0ce66c2",
 "kind": "distribution", "handler": "squashfs_v3", "depth1_viable": true,
 "product": "OpenWrt Kamikaze 8.09.1, ppc40x target (AMCC Taishan), PowerPC big-endian, uImage kernel + squashfs rootfs at 2 MiB",
 "publisher": "OpenWrt (archive.openwrt.org)",
 "oracle": "corpus/evidence/round-42/c1/OW-PPC40X/oracle.tsv",
 "nonregular": "corpus/evidence/round-42/c1/OW-PPC40X/nonregular.tsv"}

{"id": "OW-X86IMG", "url": "https://archive.openwrt.org/kamikaze/8.09.2/x86/openwrt-x86-squashfs.image",
 "image_sha256": "a06cace20bdc9edc7797ce3d7c08ee8c06166d7ba8becbf1315b27d33fb5ff20",
 "carve": {"offset": 4677120, "bytes_used": 1360991,
           "sha256": "69152935f9b7f56fdf69185f73317e91d84168d5c639476735c504c8d879969e"},
 "chunk_end": 1363968, "chunk_pad_bytes": 2977, "chunk_end_sha256":
     "6098225d01b4f644e66c75d4cf2b29411f59443339c8f78e6a27f0331a120687",
 "kind": "distribution", "handler": "squashfs_v3", "depth1_viable": true,
 "product": "OpenWrt Kamikaze 8.09.2, x86 target bootable squashfs disk image, i386 little-endian",
 "publisher": "OpenWrt (archive.openwrt.org)",
 "oracle": "corpus/evidence/round-42/c1/OW-X86IMG/oracle.tsv",
 "nonregular": "corpus/evidence/round-42/c1/OW-X86IMG/nonregular.tsv"}
```

Per-carrier oracle and non-regular tables are ready in `artifacts/…/{oracle,nonregular}/` (seven-carrier and
backhand symlink tables in `artifacts/…/backhand/*.sv.tsv`). Destination paths above are for the L1 to place;
I wrote nothing into `corpus/`.

### 5.1 Ranking, trade-offs named

| rank | id | endian | container | arch | reg/lnk | why |
|---|---|---|---|---|---|---|
| 1 | **OW-8.09.2-atheros** | BE | plain @0 | MIPS BE | 409/177 | newest release, cleanest carve (sb at 0), most symlinks, depth-1-proven shape |
| 2 | **OW-8.09-x86-fs** | LE | plain @0 | i386 | 403/167 | the only clean little-endian plain rootfs; pairs with #1 for endianness |
| 3 | **OW-8.09.1-ppc40x** | BE | uImage + 2 MiB gap | PowerPC BE | 385/167 | third architecture, real header chain, third release; shape verified at depth 1 with a synthetic twin |
| 4 | **OW-8.09.2-x86-img** | LE | boot image, sb @4 677 120 | i386 | 425/167 | deepest offset and largest regular-file set |
| alt-1 | OW-8.09-ar71xx | BE | plain @0 | MIPS BE | 416/178 | largest entry count; swap for #4 if arch diversity beats chain depth |
| alt-2 | OW-8.09.2-ppc44x | BE | uImage | PowerPC BE | 386/167 | newer twin of #3 |
| alt-3 | OW-8.09.1-wrt54g | LE | `W54G` header | MIPS LE | 403/169 | a third header type, depth-1 safe |
| alt-4 | OW-8.09.2-brcm47xx | LE | TRX v1 | MIPS LE | 404/169 | **only if `--max-depth` becomes 2**; genuine nested container, smallest pad (119 B) |
| alt-5 | OW-8.09-brcm24 | LE | TRX v1 | MIPS LE | 412/175 | same caveat; most links of the TRX set |
| alt-6 | OW-8.09.2-adm5120-be | BE | TRX v1 | MIPS BE | 407/168 | same caveat, BE |

Publisher weaknesses, stated plainly: no gzip-v3 image (so no `unsquashfs` producer), **zero device nodes** in
all ten (`dev/` is an empty dir — the devices preference cannot be met from OpenWrt), one publisher only, and
rootfs size 1.2–1.6 MB / 385–425 regular files.

---

## 6. Source quotes for the SOURCES rows (located)

`https://archive.openwrt.org/kamikaze/<release>/release.txt`:

* 8.09: `"The long awaited 8.09 release is finally done."`; platform list contains
  `"* Atheros AR531x/231x based routers"`, `"* Broadcom 47xx based routers (Linux 2.4 and 2.6)"`,
  `"* AMCC Taishan"`, `"* x86 based boards"`.
* 8.09.1: `"The OpenWrt team would like to announce the release of Kamikaze 8.09.1"`.
* 8.09.2: `"The OpenWrt team would like to announce the release of Kamikaze 8.09.2"` and
  `"This is the last update of the 8.09 release series"`.

`https://archive.openwrt.org/kamikaze/<release>/<target>/md5sums`, one line each (all verified against the
downloads):

```
b931dabdcf55adb7d1115ae6f1e27924  openwrt-atheros-root.squashfs      (8.09.2/atheros)
0118b7fa4992698780a4ac2e774d78b9  openwrt-x86-squashfs.fs            (8.09/x86)
0c556ac56ca32a215598b9b6fd3be8f9  openwrt-ppc40x-squashfs.img        (8.09.1/ppc40x)
086cdc1d871591dacaf98031faa71710  openwrt-x86-squashfs.image         (8.09.2/x86)
```

Product identity for the per-device `.bin` files lives in the filename only (`openwrt-wrt54g-squashfs.bin` …)
plus the release platform list — there is no per-device product page to quote, so a SOURCES row should cite
`release.txt` + the archive URL + the `md5sums` line.

---

## 7. Risks and what wave 2 must settle

1. **`--max-depth 1` vs TRX (open).** TRX images produce no SquashFS chunk at depth 1 (measured). Either keep
   them out of the frozen set (my recommended four already do), or change the frozen
   `rea_parameters.max_depth` to 2 before the freeze — that changes the frozen C1 path set.
2. **Oracle pair (resolved, with two residual conditions).** backhand × 7-Zip agree 10/10 on regular files.
   Conditions: (a) type the 7-Zip side from `Mode` in `l -slt`, never from the extraction tree — 102–104
   phantoms per carrier; (b) take symlink **targets** and the non-regular table from backhand, because 7-Zip
   rewrites the six absolute-target links (`etc/TZ → /tmp/TZ` etc.) to paths under its extraction root.
3. **Carve accounting.** `carve.bytes_used` (e.g. 1 560 688) ≠ unblob's chunk end (1 564 672); the padding is
   verified all-zero on 10/10. The counter must compare the cache entry to `bytes_used` and the REA chunk to
   `chunk_end`, or it will report a size mismatch that is not one.
4. **Symlink gap volume.** 167–178 gap rows per carrier; proven producible (round-41: 611). unblob also logs
   `Ignoring special file` for links while recursing, so nothing about links can come from the extraction tree.
5. **uImage / x86-image depth-1 reach is [INFERENCE] for the real candidates.** Measured only on synthetic
   twins of the same geometry (§4.2). If the L1 wants certainty for `OW-PPC40X`/`OW-PPC44X`/`OW-X86IMG` before
   the freeze, the first real REA run must be on them — a candidate cannot be probed without burning it.
6. **Locator longevity.** `archive.openwrt.org` answered HTTP 200 on all ten fetches on 2026-10-26T22:04Z; only
   per-target `md5sums` accompany the files (no `SHA256SUMS`, no signature), so the chain proves the fetched
   bytes plus the publisher's md5 line, not a vendor signature.
7. **Devices unavailable** from this publisher (0 nodes in 10/10), so the gap rule is exercised on directories
   and symlinks only.

Not claimed: v1/v2 images, v4 Broadcom, anything about extracted programs, and no statement about how REA's
`MaliciousSymlinkRemoved` heuristic treats a `../../bin/busybox` link — unmeasured at wave 1.

---

## 8. Reproduction

```
S=/fast/scratch/hyaku/kaidoku-r42/R42C1ImgOpenwrt; mkdir -p "$S"; cd "$S"; export TMPDIR="$S"
A=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C1ImgOpenwrt
python3 "$A/c1-openwrt-probe.py" --work "$S/probe"                     # fetch, carve, unsquashfs+7z, LZMA probe
python3 "$A/c1-backhand-crossread.py" --work "$S/xr" --carves "$S/probe/carve"   # backhand x 7-Zip
# dev-only extractor probes (7.09 is designated DEVELOPMENT; never a candidate)
curl -sS -o dev709/a.squashfs https://archive.openwrt.org/kamikaze/7.09/atheros-2.6/openwrt-atheros-2.6-root.squashfs
curl -sS -o dev709/b.trx       https://archive.openwrt.org/kamikaze/7.09/brcm47xx-2.6/openwrt-brcm47xx-2.6-squashfs.trx
unblob -f -d 1 -e out1 dev709/b.trx          # TRX_V1 only  -> the depth-1 failure mode
unblob -f -d 2 -e out2 dev709/b.trx          # TRX_V1 -> SQUASHFS_V3
unblob -f -d 1 -e out3 dev709/a.squashfs     # SQUASHFS_V3 extracted (309 entries)
```

Tools: `artifacts/…/c1-openwrt-probe.py`, `artifacts/…/c1-backhand-crossread.py` (stdlib + readers on PATH;
honour `--work`/`TMPDIR`; never invoke REA, unblob or sasquatch).
