# R42C1ImgVendor — vendor-firmware carriers for R42-C1 (SquashFS major 3)

**VERDICT: DONE** — four published vendor images whose rootfs is a genuine SquashFS **major 3** big-endian
filesystem, with full field data, carve rule, chunk_end and a two-producer oracle that agrees file-for-file on
every regular file of all four. Alongside it, four defects for the draft (`C1-D1..D5`, §7) — the most important
being that **all four vendor v3 rootfs are LZMA**, so `unsquashfs` 4.7.5 (the oracle's first producer at
`plans/round-42-claims.md:51`) reads *none* of them; the L1's backhand producer is what makes them usable.

Measured 2026-10-26, 21:54Z–22:10Z. No REA, no unblob, no sasquatch was run on any candidate (they were read only
with `unsquashfs`, `7z`, and the L1-built `unsquashfs-backhand`); the reserved DD-WRT / OpenWrt-8.09 candidates and
the OpenWrt 7.09 development images were not touched. Nothing installed.

## 1. Candidates (ranked)

| # | id | carrier (vendor image) | rootfs | endian | compression | sb offset | entries (f/l/d/b+c) | regular-file agreement |
|---|---|---|---|---|---|---|---|---|
| 1 | `V2-dlink-dir615c` | D-Link DIR-615 rev C, FW 3.13NA | SquashFS 3.0 | BE `sqsh` | LZMA | 0x100000 | 419/73/47/11+29 | **419/419** path+sha256 |
| 2 | `V3-dlink-dir825b` | D-Link DIR-825 rev B, FW 2.03NA | SquashFS 3.0 | BE `sqsh` | LZMA | 0x100000 | 456/77/51/14+31 | **456/456** |
| 3 | `V4-dlink-dir632` | D-Link DIR-632 rev A, FW 1.03 | SquashFS 3.0 | BE `sqsh` | LZMA | **0x1F0000** | 421/75/51/12+32 | **421/421** |
| 4 | `V1-tp-link-wr741nd` | TP-Link TL-WR741ND v1/v2, 100910 | SquashFS **3.1** | BE `qshs` | LZMA | 0x100000 | 298/55/35/9+33 | **298/298** |

All four: `f` regular, `l` symlink, `d` directory, `b`/`c` block/char device, from `7z l -slt` `Mode`;
backhand's extracted tree gives the identical shape (`oracle-*.json` in the artifacts dir).
Machine-readable records (carriers.json-ready): `.ufo/waves/round-42/w1/artifacts/R42C1ImgVendor/candidates.json`.

### 1.1 `V2-dlink-dir615c` — best carrier (top rank)

- URL `http://legacyfiles.us.dlink.com/DIR-615/REVC/FIRMWARE/DIR-615_REVC_FIRMWARE_3.13.ZIP` — official D-Link
  legacy host (Apache index; HTTP only, `https://` presents an unverifiable certificate). HTTP **200**,
  `Content-Length 3492669`, `Last-Modified Fri, 23 Oct 2020 20:24:02 GMT`. GET 2026-10-26T21:54:37Z, HEAD
  re-verify 2026-10-26T22:05:27Z.
- zip sha256 `cf3199520172803efe02b1e2418ad222762ee868d6081724f53121fc7959c8f5` (3 492 669 B).
- member `dir615_revC_FW_313NA/DIR615C1_FW313NAB09.bin`, 3 866 650 B,
  sha256 `e03750f81c91b9228fd574d4cc473577362fb04be5bc13b6e8f3896fa53be99b`.
- container chain: `uImage` magic `27 05 19 56` + `"Linux Kernel Image"` at 0 (`ih_size` 0x000ED643) → 1 MiB
  kernel partition → SquashFS superblock at **0x100000**.
- superblock (packed v3 layout, §4): magic `sqsh`, `s_major 3`, `s_minor 0`, inodes 580, block_size 65536,
  block_log 16, flags 0x40, no_uids 3, no_guids 3, mkfs_time 0x4C8F38A5, fragments 65, `bytes_used 2518754`,
  inode_table_start 0x264805, directory_table_start 0x2659F3.
- unblob 26.6.4 handler: `squashfs_v3` (PATTERN `73 71 73 68 [24] 00 03`; v1 needs `00 01`, v2 `00 02`, v4BE
  `00 04`, so the match is unambiguous).
- carve `[0x100000, 0x367000)` = 2 519 040 B (chunk_end = `round_up(bytes_used, 4096)`),
  sha256 `7e4587066558183f33d8affbbfe572f9c44c025612f8ee24d8206ad3ca33a336`.
- oracle: backhand `be_v3_0_lzma` extracts 419 regular files + 73 symlinks + 47 dirs; 7-Zip 26.04 lists the same
  types and its extraction matches **419/419** regular files on path **and sha256** (0 mismatches, 0 backhand-only).
- `unsquashfs -s` prints `Found a valid big endian SQUASHFS 3:0 superblock` (exit 0), then every listing/extraction
  fails: `gzip uncompress failed with error code -3` / `read_block: failed to read block @0x266d4a` /
  `FATAL ERROR: File system corruption detected` (exit 1) — the data is LZMA and v3 carries no compression field.
- SOURCES-quotable line (zip-internal release notes, `dir615_revC_release_notes.txt`):
  `DIR-615 Revision C Firmware Release Notes` / `Firmware: 3.13NA` / `Date: 09/30/10`.

### 1.2 `V3-dlink-dir825b`

- URL `http://legacyfiles.us.dlink.com/DIR-825/REVB/FIRMWARE/DIR-825_REVB_FIRMWARE_2.03.ZIP`; 200,
  `Content-Length 4173799`; zip sha256
  `70106e1288617614ac43acc965fb5ed0b9c1f94b2347b3cf4daa6168afb70013`; member
  `dir825_revB_fw_203NA/dir825_revB_fw_203NA.bin` 4 194 330 B, sha256
  `379836b8625f32fb3c2642656f056e9bf43f929101e2ff758bb5049c5373ef2d`.
- `uImage` at 0 (`ih_size` 0x000FFAFC); sb at 0x100000; inodes 630, bytes_used 3126468, fragments 77 (0x4D),
  mkfs_time 0x4BAC8CBB (2010-03-26T10:30:19Z), inode_table_start 0x2F894B, directory_table_start 0x2F9DCC; handler `squashfs_v3`.
- carve 3 129 344 B sha256 `cabee68272d8513b6c36579d5b0a4ee9d0638c65d6de7e33b5b994d2152df6dc`.
- oracle: backhand `be_v3_0_lzma`; **456/456** regular files agree with 7-Zip on path+sha256; 77 symlinks.
- release notes: `DIR-825 Revision B Release Notes` / `Firmware: 2.03NA` / `Date: 04/27/10`.

### 1.3 `V4-dlink-dir632` (different container offset)

- URL `http://legacyfiles.us.dlink.com/DIR-632/REVA/FIRMWARE/DIR-632_REVA_FIRMWARE_1.03.ZIP`; 200,
  `Content-Length 3643888`; zip sha256
  `f61d47c1c5cbf6ab76e67ac7282bc4eab95ed45cf0ee947f0afcafb25a424c6e`; member `DIR632_FW_103.bin` 7 667 736 B,
  sha256 `a1a4a97059772b525dd1595b0302b81d6eb6c5d7bb589a7d816cad0f68beec4f`.
- `uImage` at 0 (`ih_size` 0x00100C15), ASCII `CFE` at 3491934; sb at **0x1F0000**; inodes 592, bytes_used
  2587533, fragments 0x48=72, mkfs_time 0x4F309354 (2012-02-07T02:58:28Z); handler `squashfs_v3`.
- carve `[0x1F0000, 0x468000)` = 2 588 672 B sha256
  `0762054e07bde99c50c83d4a46c2ba5f399cd441d8259f1427df587499b257dc`.
- oracle: **421/421** regular files agree; 75 symlinks; 12 block + 32 char devices.

### 1.4 `V1-tp-link-wr741nd` (different magic family: `qshs`, SquashFS 3.1)

- URL (archive.org copy, because the vendor URL is dead — see §7 C1-D5):
  `https://archive.org/download/TP-Link_TL-WR741NDV1_100910_ce76a/ce76a7c4713f45e2c8b24704fc686494.zip`;
  HTTP 302→200, `Content-Length 2939930`; zip sha256
  `9f46170b34ba8a4effad8db627a989208e80e4e5980605d3bb3739dc60997c86`; member
  `wr741nv1_en_3_12_4_up(100910).bin` 3 932 160 B, sha256
  `f8fa728dca39040e1e42045fa625c81bb4f0506a53baf6b09249a67d7d06cadf`.
  (Archive items `TP-Link_TL-WR741NDV1_100910_ce76a` and `…V2_100910_ce76a` serve the *same* zip bytes.)
- container chain: TP-Link proprietary 0x200-byte header at 0 (`u32 1`, `"TP-LINK Technologies"`, `"ver. 1.0"`,
  CRC/region words); **no** `HDR0`/`TRX`/`CFE`; sb at 0x100000.
- superblock: magic `qshs`, `s_major 3`, `s_minor 1`, inodes 431, block_size 65536, block_log 16, flags 0xE0,
  no_uids 1, no_guids 0, mkfs_time 0x4C8D9A8B (2010-09-13T03:29:15Z), fragments 48, bytes_used **2059310**,
  inode_table_start 0x1F4CB1, directory_table_start 0x1F58BA.
- unblob handler: **`squashfs_v3_broadcom`** (PATTERN `71 73 68 73 [24] 00 03`) — the only v3 handler for this
  magic; unblob's label is "Broadcom", but the same bytes are what backhand calls `netgear_be_v3_0_lzma`
  (`be_v3_0_lzma` rejects them), so the oracle kind cannot be derived from unblob's handler name (C1-D2).
- carve 2 060 288 B sha256 `f4b10e19758f1ad55222ac2fe7c2c7637ab512ca4c80ec08b5cecdf5075f47c1`.
- oracle: backhand `netgear_be_v3_0_lzma` → **298/298** regular files agree with 7-Zip (path+sha256); 55 symlinks
  (7-Zip extracts 35, refusing all 20 whose target contains `..`), 42 device nodes.
- `unsquashfs -s` fails outright (exit 1): `FATAL ERROR: Can't find a valid SQUASHFS superblock` — the `qshs`
  magic is not in squashfs-tools' accepted set at all.

## 2. Oracle measurement (the two producers)

Producers used (both non-sasquatch, per the seat spec and the L1's 22:0xZ message):

- **A — `unsquashfs-backhand` 0.25.5** (`/home/vgpnk/.local/opt/backhand-0.25.5-v3/bin/unsquashfs-backhand`,
  features `v3, gzip, lzma, xz`), kinds `be_v3_0_lzma` / `netgear_be_v3_0_lzma`; extraction then a link-safe tree
  walk.
- **B — 7-Zip 26.04** (`7z l -slt` for the entry table and `Mode`-based types, `7z x` for contents).

| carrier | backhand kind | rc | regular (backhand) | regular (7z) | agree path+sha256 | sha mismatches | backhand-only |
|---|---|---|---|---|---|---|---|
| V2 dir615c | `be_v3_0_lzma` | 0 | 419 | 419 | **419** | 0 | 0 |
| V3 dir825b | `be_v3_0_lzma` | 0 | 456 | 456 | **456** | 0 | 0 |
| V4 dir632 | `be_v3_0_lzma` | 0 | 421 | 421 | **421** | 0 | 0 |
| V1 wr741nd | `netgear_be_v3_0_lzma` | 0 | 298 | 298 | **298** | 0 | 0 |

Type tables are identical between the two producers (`7z l -slt` `Mode` first character vs the backhand tree),
including device nodes: dir615c 11 block + 29 char, dir825b 14+31, dir632 12+32, wr741nd 9+33.

Three 7-Zip behaviours that must be encoded in any oracle built on it (each measured, files in `artifacts/`):

1. **`7z x` materialises non-regular entries as empty regular files.** dir615c: 482 files on disk = 419 regular +
   40 device nodes + 23 refused symlinks; dir825b 524 = 456+45+23; dir632 489 = 421+44+24; wr741nd 360 = 298+42+20.
   A tree walk over `7z x` output therefore *over-counts* regular files and would violate the draft's
   "no non-regular oracle entry as a file" binding. Classify with `7z l -slt` `Mode`, never with `os.walk`.
2. **`7z x` refuses every symlink whose stored target contains `..`** (`ERROR: Dangerous link path was ignored`),
   even when the normalised path stays inside the root: 23 / 23 / 24 / 20 entries. Measured: **0** symlinks in any
   carrier truly escape the root by normalisation (all `..` targets land inside), so this refusal is conservative
   and would produce false `unpublished-entry` rows.
3. **`7z`'s `-slt` listing does not print symlink targets** (only `Size` = target length), and `7z x` rewrites
   *absolute* targets into the extraction root (dir615c/dir825b/dir632 each carry 2:
   `lib/modules/2.6.15--LSDK-7.2.0.156/{build,source} -> /home/AthSDK/platform/AR7161/kernels/mips-linux-2.6.15`;
   dir632 `.../2.6.15--LSDK-7.3.0.260/... -> /home/Matrix/platform/kernel/AR7242/kernels/mips-linux-2.6.15`).
   Symlink targets for an oracle table must come from producer A (or the receipt), plus the 7-Zip `Size` as a
   length cross-check.

`unsquashfs` 4.7.5 (the draft's first producer) on the same carves: dir615c/dir825b/dir632 exit 1 with
`gzip uncompress failed with error code -3` … `FATAL ERROR: File system corruption detected`; wr741nd exit 1
`Can't find a valid SQUASHFS superblock`. Full stderr is in `artifacts/<carrier>.json` → `readers.unsquashfs_*`.

## 3. Container chains, carve rule, chunk_end

| carrier | header at 0 | sb offset | bytes_used | chunk_end (absolute) | chunk_end rule |
|---|---|---|---|---|---|
| V1 wr741nd | TP-Link 0x200-byte vendor header | 0x100000 | 2 059 310 | 3 108 864 | round_up 4096 |
| V2 dir615c | uImage (`27 05 19 56`) | 0x100000 | 2 518 754 | 3 567 616 | round_up 4096 |
| V3 dir825b | uImage | 0x100000 | 3 126 468 | 4 177 920 | round_up 4096 |
| V4 dir632 | uImage | **0x1F0000** | 2 587 533 | 4 620 288 | round_up 4096 |

`chunk_end` is unblob 26.6.4's own rule, transcribed from
`unblob/handlers/filesystem/squashfs.py` `_SquashFSBase.calculate_chunk`: `end = start + round_up(bytes_used, 4096)`
if the tail is zero padding, else 1024, else `start + bytes_used`. All four carriers pad to 4096 with zeros, so the
carve is `[sb_offset, chunk_end)` and the carve sha256 in `candidates.json` covers exactly that extent (the extra
2 178 / 286 / 2 876 / 1 139 padding bytes are the only difference from a `bytes_used`-only carve).

## 4. Superblock layout — packed, not padded (correction worth propagating)

My first pass read the v3 struct with a C pad byte after `no_guids` (mkfs_time@40) and consequently saw all 64-bit
fields as `value << 8`. That was wrong. The on-disk layout is **packed** and verified byte-for-byte against three
readers plus unblob's own parser:

```
inodes@4  s_major@28 s_minor@30 block_size_1@32 block_log@34
flags@36  no_uids@37 no_guids@38 mkfs_time@39(u32) root_inode@43(u64)
block_size@51(u32) fragments@55(u32) fragment_table_start_2@59(u32)
bytes_used@63(u64) uid_start@71 guid_start@79 inode_table_start@87
directory_table_start@95 fragment_table_start@103 lookup_table_start@111
```

- dir615c under this layout: `mkfs_time 0x4C8F38A5` → 2010-09-14 08:56:05Z = the `05:56:05` that unsquashfs prints
  in local time (UTC−3) and 7-Zip prints as `Created`; `fragments 0x41 = 65` = unsquashfs
  `Number of fragments 65`; `bytes_used 0x266EE2 = 2518754` = unsquashfs `Filesystem size 2518754` = 7-Zip
  `Physical Size 2519040` (rounded to 1 KiB).
- unblob 26.6.4 itself parses this packed layout: feeding a synthetic packed superblock through
  `StructParser(SquashFSv3Handler.C_DEFINITIONS)` returns `bytes_used 0x266ee2`, `fragments 0x41`,
  `mkfs_time 0x4c8f38a5`, `block_size 0x10000` (dissect.cstruct, no alignment padding). So `calculate_chunk`
  computes the right end on these images — REA will not produce a short or oversized v3 chunk here.
- Consequence for `tools/round-42/c1-counter.py`: read `bytes_used` at **63**, not 64, and do not divide by 256.

## 5. Ranking and recommended 4-carrier composition

Ranking axes the draft asks for (full rootfs, both endiannesses, gzip and LZMA, ≥2 publishers, quotable
product/version):

1. `V2-dlink-dir615c` — 419 regular + 73 symlinks + 40 devices, live official URL with an Apache index, release
   notes inside the zip, BE/LZMA. Best single vendor carrier.
2. `V3-dlink-dir825b` — 456 regular, richest tree; same host; BE/LZMA.
3. `V4-dlink-dir632` — 421 regular, and the only candidate whose superblock sits at a non-1 MiB offset (0x1F0000),
   which exercises the offset handling.
4. `V1-tp-link-wr741nd` — second publisher, second magic family (`qshs`, v3.**1**), second container shape
   (vendor header instead of uImage), but archive.org provenance and a switch to the `netgear_*` backhand kind.

Composition note for the L1: **every vendor major-3 image measured is big-endian and LZMA** — six distinct vendor rootfs
images across seven zip items and two publishers (§6). The endianness and gzip axes therefore have to come from the DD-WRT (`tqsh`) and
OpenWrt (`hsqs`, gzip) seats; the vendor slot should be one of the three D-Link carriers (live URL, release-note
quote, no archive dependency). If the freeze wants a gzip carrier that `unsquashfs` can also read, no vendor
candidate in this sweep can supply it.

## 6. Search log (what was probed and rejected)

Hosts probed for a live vendor index: `legacyfiles.us.dlink.com` (works, Apache index, HTTP), `fw.draytek.com.tw`
(works, index), `dl.ui.com`/`dl.ubnt.com` (200 but serves a marketing page, files gone), `dlcdnets.asus.com`
(404 on directory listing), `www.downloads.netgear.com/files/GDC/` (403 on directory *and* on files),
`static.tp-link.com` (404 for legacy paths), `ftp.zyxel.com` (DNS gone), `www.buffalo.jp` (JS only),
`sourceforge.net/projects/officiallinksysfirmware` (403), archive.org (`firmwarelibrary`/`softwarecapsules`
collections). Search engines: DDG HTML and Bing returned no usable hits, Brave worked intermittently; the winning
channel was the D-Link legacy index plus archive.org's per-file firmware items.

Rejected after measurement (reasons in `candidates.json` → `rejected`):

- D-Link DIR-130 / 330 / 450 / 451, DIR-625 / 628 / 635 / 655 rev A, DIR-825 rev A, DGL-4500 — **no SquashFS
  magic anywhere** (Ubicom/proprietary containers).
- D-Link DIR-615 rev A 1.10, rev B 2.25 — no SquashFS magic.
- D-Link **DSL-2740B rev A 1.00 and 2.06** (Broadcom 6328 ADSL) — clean SquashFS at 0x100 but **v4 Broadcom LE**
  (`shsq`, `s_major 4` → unblob `squashfs_v4_broadcom`). Useful control that the scanner/handler mapping is right;
  not a v3 carrier.
- D-Link **DIR-601 rev A 1.01** — v3 BE at 0xF0000, same LZMA family, no new axis.
- **Draytek Vigor2820** v3.3.7.9 (official `.all`, 5 784 456 B) — no SquashFS magic.
- **Linksys WRT54G v8** 8.00.8.001 (1 768 904 B) — no SquashFS magic.
- TP-Link TL-WR841ND v5 100929 — `qshs` BE v3.1 at 0x100000, i.e. the same family as `V1` (one publisher, one
  variant is enough).

## 7. Defects / draft impact

- **C1-D1 (`plans/round-42-claims.md:51`)** — the oracle names `unsquashfs` 4.7.5 as producer 1 "reads v1–v3
  gzip". A real vendor major-3 rootfs is LZMA (4/4 carriers here, LZMA-patched squashfs 3 is the embedded-vendor
  norm; unblob even ships dedicated `*_nonstandard`/`broadcom` handlers for it). unsquashfs 4.7.5 has no LZMA
  decoder and v3 has no compression field, so the vendor slot is unfillable under the draft text. Either the claim
  names backhand 0.25.5 as producer 1 and unsquashfs as an *additional* gzip-only producer (the L1's 22:0xZ
  decision), or the 4-carrier set must be gzip-only.
- **C1-D2** — handler label ≠ oracle kind. `qshs` is `squashfs_v3_broadcom` to unblob but only
  `netgear_be_v3_0_lzma` to backhand (`be_v3_0_lzma` fails on it). The per-carrier "frozen handler" and the frozen
  backhand kind are two different pins; both must be in `carriers.json`.
- **C1-D3** — 7-Zip is not a drop-in oracle: `7z x` writes device nodes and refused symlinks as empty regular files
  (+40…+45 and +20…+24 rows per carrier), refuses every `..`-containing target (0 of which actually escape), does
  not print symlink targets in `-slt`, and rewrites absolute targets. Producer 2 must take its entry table from
  `7z l -slt` `Mode` and its symlink targets from producer A; extracting with `7z` and walking the tree is wrong.
- **C1-D4** — the v3 superblock is **packed** (`bytes_used`@63, see §4); a counter using the padded C offsets reads
  `bytes_used << 8` on these very images and would carve a chunk past EOF. (My own intermediate artefacts had this
  bug; corrected before writing this report — noted so the frozen counter gets a regression check on it.)
- **C1-D5** — provenance: the TP-Link v1/v2 firmware URL is dead (legacy `static.tp-link.com` paths 404, current
  product page is JS-only), so `V1` is only an archive.org copy; D-Link's host is HTTP-only with a broken TLS
  chain, which `fetch-carrier.py` must accommodate (no `--fail`-on-TLS assumptions). The claim should say which of
  the two is acceptable rather than leaving it to the fetch script.

Also worth noting for the gap rule: `.dummy` files are real filesystem entries in the D-Link images (10 in
dir615c, one per top-level dir) — not tool artefacts; they appear in both producers and must be counted as regular
files.

## 8. Reproducibility

Scratch (removed after the run): `/fast/scratch/hyaku/kaidoku-r42/R42C1ImgVendor`. Tools used as installed, no
changes: `unsquashfs` 4.7.5, `7z` 26.04, backhand 0.25.5 (built by the L1), unblob 26.6.4 read-only (source +
`dissect.cstruct` parse of a synthetic superblock).

```sh
S=/fast/scratch/hyaku/kaidoku-r42/R42C1ImgVendor; cd "$S"
curl -sSL -o dir615c.zip http://legacyfiles.us.dlink.com/DIR-615/REVC/FIRMWARE/DIR-615_REVC_FIRMWARE_3.13.ZIP
sha256sum dir615c.zip            # cf3199520172803efe02b1e2418ad222762ee868d6081724f53121fc7959c8f5
python3 -c "import zipfile;z=zipfile.ZipFile('dir615c.zip');open('dir615c.bin','wb').write(z.read('dir615_revC_FW_313NA/DIR615C1_FW313NAB09.bin'))"
A=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C1ImgVendor
python3 $A/probe-carrier.py dir615c.bin --tag dir615c --kind be_v3_0_lzma --carve-dir probes   # sb, chunk_end, carve, 7z, unsquashfs
python3 $A/oracle-compare.py probes/dir615c.1048576.sqfs be_v3_0_lzma cmp/dir615c             # backhand vs 7z, path+sha256
curl -sSL -o wr741nd.zip https://archive.org/download/TP-Link_TL-WR741NDV1_100910_ce76a/ce76a7c4713f45e2c8b24704fc686494.zip
python3 $A/probe-carrier.py wr741nd.bin --tag wr741nd --kind netgear_be_v3_0_lzma --carve-dir probes
python3 $A/oracle-compare.py probes/wr741nd.1048576.sqfs netgear_be_v3_0_lzma cmp/wr741nd
```

Artifacts (`.ufo/waves/round-42/w1/artifacts/R42C1ImgVendor/`): `candidates.json` (carriers.json-ready records),
`probe-carrier.py` (superblock/chunk_end/carve/reader probe), `oracle-compare.py` (two-producer path+sha256
compare), `scan-sqfs.py` (magic/handler scout), `dlink-index.py` + `dlink_index.tsv` (official-index crawl,
94 firmware files over 15 models), `<carrier>.json` (probe output incl. full 7z type/path tables),
`oracle-<carrier>.json` (compare output), `7z-dir615c.txt`, `7z-x.txt`. No third-party firmware bytes are in the
lane: carves and extracts stayed in scratch; only hashes, field data and path/type tables were copied.

## 9. Limits

- No REA enumeration was possible on these candidates (forbidden this wave), so "which handler REA finally names"
  is [INFERENCE] from the unblob PATTERNS plus the fact that v1/v2/v4 patterns cannot match these headers
  (verified pattern-by-pattern from `unblob/handlers/filesystem/squashfs.py` at 1fcc7a0a).
- `unsquashfs` cannot be a producer for any of these four; the "both readers agree" result rests on backhand and
  7-Zip, as the L1 directed.
- Vendor sweep covered two publishers only; other vendors' gzip-v3 images may exist but were not reachable from a
  live official index during this wave (see §6).
- Zip-level hashes are of the downloaded bytes at the stated times; the archive.org item could re-derive (the
  `Last-Modified` recorded is 2024-04-16).
