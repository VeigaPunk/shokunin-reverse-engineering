# R42C1ImgDdwrt — DD-WRT C1 candidate carriers (round 42, wave 1)

**Verdict: DEFECTS FOUND** — six DD-WRT v24 images were fetched, digested and fully measured, and **not one
can satisfy the R42-C1 oracle as the draft writes it**: DD-WRT's `hsqt`/`tqsh` rootfs are SquashFS 3.0 with
**LZMA** blocks, and all three readers I could line up reject the published magic (unsquashfs 4.7.5, 7-Zip
26.04, and — measured after the L1's oracle decision — `unsquashfs-backhand` 0.25.5 with all 13 of its kinds),
while unsquashfs additionally cannot decode the LZMA blocks at all. The unblob 26.6.4 `squashfs_v3_ddwrt`
handler and sasquatch 4.5.1 *do* handle the same magic + codec combination (proved on fixture-derived
development copies), so the extraction half of C1 is sound. **On a frozen 4-byte magic-normalised copy the
L1's oracle pair works exactly**: backhand and 7-Zip agree on the complete path set for all six carriers and
on 296/296 sha256 for the sampled one (§13). Everything below is measured; nothing is inferred except where
marked `[INFERENCE]`.

Seat: `R42C1ImgDdwrt`. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Scratch
`S=/fast/scratch/hyaku/kaidoku-r42/R42C1ImgDdwrt` (removed at the end). Artifacts:
`.ufo/waves/round-42/w1/artifacts/R42C1ImgDdwrt/`.

## 1. Scope and what was / was not run

Run: HTTP GET + digest on the published images; byte-level superblock parsing; handler `PATTERNS` matching
taken mechanically from the installed unblob source; `unsquashfs` (`-s`, `-lls`), `7z` (`l -slt`, `x`) and
`bsdtar -tf` **on the carriers** (permitted reader-only access); `sasquatch` and `unblob` **only on
fixture-derived development copies** in scratch (unblob 26.6.4 fixtures are development inputs).

Not run, deliberately: no REA, no unblob and no sasquatch on any published candidate or anything carved from
one; no VCS mutation; no package installs (nothing needed — `curl`, `python3` 3.14.8, `unsquashfs` 4.7.5,
`7z` 26.04, `bsdtar` 3.8.10, `unblob`, `sasquatch` 4.5.1 were already present); no build/lint/test gates
(the L1 owns post-integration gates). No writes outside this report and this seat's artifacts directory.

Magic-normalised copies (bytes 0..3 swapped to `hsqs`/`sqsh`) exist **only as a diagnostic** in scratch; the
carrier pins below are the published, unpatched bytes, as `R42C1Fetch` requires.

## 2. Candidate table (all measured)

Publisher for all six is the DD-WRT project's own download tree (`download1.dd-wrt.com`); the per-product
directories name the device vendors. MD5 of every download was checked against the publisher's
`MD5SUMS` for `v24/` (`https://download1.dd-wrt.com/dd-wrtv2/downloads/v24/MD5SUMS`, 11 871 B, 132 lines,
sha256 `6054cca0dc3cd798bc9fb6b5d39f0372bb3d998bebe1504f05f9ad8cb51a508d`);
all six **MATCH** — reproducible with `artifacts/.../md5-vs-published.py` (output `md5-verify.log`).

| id | product | HTTP | accessed (UTC) | bytes | image sha256 | published md5 | rootfs offset | bytes_used | carve sha256 (pin) |
|---|---|---|---|---|---|---|---|---|---|
| DDWRT-FONERA | DD-WRT v24 `linux.bin`, Fonera | 200 | 2026-10-26T21:56:58Z | 6 684 672 | `e9910533…bb57` | `3ccdd6b6…` ✓ | 851968 | 5 829 314 | `a4a454a9d0b06c3f3420033857c00b85e62fc3184822fbd92f21db97231df10f` |
| DDWRT-BCM-MEGA | DD-WRT v24 mega, Broadcom generic | 200 | 2026-10-26T21:56:50Z | 6 017 024 | `abd0db4d…a3b9` | `bed653f2…` ✓ | 923752 | 5 090 570 | `f86ea69c60fb030c672f093a375f1d3b2dd20332bb7eb71db9610a276646e404` |
| DDWRT-UBNT-LS2 | DD-WRT v24 for Ubiquiti LiteStation 2 | 200 | 2026-10-26T21:56:53Z | 3 645 784 | `ad32b8b2…bbd5` | `af15e394…` ✓ | 852292 | 2 792 577 | `3b130a5afbe6201f2f490545f26c8d39dc9469a2a5f1c00eb92f7409b2b4ac82` |
| DDWRT-BUFFALO-ROOTFS | DD-WRT v24 `root.fs`, BUFFALO WHR-HP-AG108 | 200 | 2026-10-26T21:56:55Z | 2 605 056 | `7cb5eec5…bc16` | `dc06a47e…` ✓ | 0 | 2 602 977 | `3b4e852f508a1839d395e424afa48f66be10ab887c1445e560e020cce8bdac63` |
| DDWRT-AR430W | DD-WRT v24 `linux.bin`, Airlink 101 AR430W | 200 | 2026-10-26T21:57:01Z | 3 731 456 | `35eff8e3…3bd1` | `b83fc046…` ✓ | 851968 | 2 876 746 | `9b3b9cc48fb3823428620f64dd04b48c4f3170467e534962c9eadd2d274cd441` |
| DDWRT-BCM-MINI | DD-WRT v24 mini, Broadcom generic | 200 | 2026-10-26T21:56:45Z | 2 920 448 | `ee9e9e1b…b521` | `cee30faa…` ✓ | 923872 | 1 992 951 | `e34b6446dee4f4d5fbb41281522c868bc72631546935957482daac99e63f54bc` |
| ~~DD-WRT v23 std~~ *(rejected: v2.1, not v3)* | `dd-wrt.v23_generic.bin` in `stable/dd-wrt.v23/dd-wrt.v23.std.zip` | 200 | 2026-10-26T21:53:18Z | zip 17 597 927 (member 3 522 560) | zip `2f9a64e8…b75e`, member `b2248f4a…6ea6` | — | 604396 | (v2 superblock) | magic `hsqs`, **major 2 minor 1** |

Full URLs (all fetched with plain `curl -sS -o`, `%{http_code}` recorded per file in `fetch.log`):

- `https://download1.dd-wrt.com/dd-wrtv2/downloads/v24/Broadcom/Linksys/WRT54GL_1.0/dd-wrt.v24_mini_generic.bin`
- `https://download1.dd-wrt.com/dd-wrtv2/downloads/v24/Broadcom/Linksys/WRT54GL_1.0/dd-wrt.v24_mega_generic.bin`
- `https://download1.dd-wrt.com/dd-wrtv2/downloads/v24/Atheros%20WiSoc/Ubiquiti%20Litestation%202/LS2.dd-wrt.bin`
- `https://download1.dd-wrt.com/dd-wrtv2/downloads/v24/Atheros%20WiSoc/BUFFALO%20WHR-HP-AG108/root.fs`
- `https://download1.dd-wrt.com/dd-wrtv2/downloads/v24/Atheros%20WiSoc/Fonera/linux.bin`
- `https://download1.dd-wrt.com/dd-wrtv2/downloads/v24/Atheros%20WiSoc/Airlink%20101%20AR430W/linux.bin`

The two Broadcom files were fetched from the `Linksys/WRT54GL_1.0` product directory and are **byte-identical**
(md5-equal) to the publisher's canonical `./Broadcom/Broadcom Generic/dd-wrt.v24_{mini,mega}_generic.bin`
entries — so the product directory and the canonical build are the same published bytes.

`carve.offset + bytes_used <= image bytes` holds for all six (tail padding after the rootfs: 3625, 2702,
915, 2079, 3390, 2742 bytes respectively), which is what `fetch-carrier.py` enforces.

## 3. Container chain to the SquashFS, and how to carve

| id | container | evidence in the published bytes |
|---|---|---|
| DDWRT-BCM-MINI | TRX (`HDR0`) at 0, then a gzip kernel, then the rootfs | `HDR0` at 0; length field `0x002c9000` **little-endian** = 2 920 448 = file size; header offsets loader=28, kernel=2288, **rootfs=923872** (declared offset == carve) |
| DDWRT-BCM-MEGA | same TRX layout | length `0x005bd000` LE = 6 017 024 = file size; offsets 28 / 2288 / **rootfs=923752** |
| DDWRT-UBNT-LS2 | vendor ASCII header | `OPENLS2.ar2316.DD-WRT\0…` at 0, zero-filled to the rootfs |
| DDWRT-BUFFALO-ROOTFS | none | superblock at offset 0 (bare rootfs — the simplest carve of the set) |
| DDWRT-FONERA | vendor boot header `6d 00 00 80 00 38 fc 28 …`, kernel, rootfs | rootfs at `0xD0000` |
| DDWRT-AR430W | same vendor boot header (identical first 32 bytes to Fonera), rootfs at `0xD0000` | rootfs at `0xD0000` |

Carve = `dd if=<image> of=<pin>.bin bs=1 skip=<offset> count=<bytes_used>` (or the `fetch-carrier.py` window);
the resulting bytes hash to the pin column above.

## 4. Superblock fields (v1-compat and 64-bit fields all read)

All six read `s_major = 3`, `s_minor = 0`, block size 65536 (`block_log` 16), `flags` 0x40, fragments 23–79,
`lookup_table_start = 0xFFFF…FF` (absent). Magic and byte order split by platform: Broadcom builds use
`hsqt` (fields little-endian), Atheros builds use `tqsh` (fields big-endian). Full field dump in
`artifacts/.../superblocks.tsv`; per-carrier file-system creation times are 2008-05-24 (Broadcom) and
2008-05-19/20 (Atheros), consistent with the publisher's `Last-Modified` headers (May 2008).

`mkfs_time` values: BCM-MINI 1211628861, BCM-MEGA 1211633333, UBNT-LS2 1211252161, BUFFALO 1211251697,
FONERA 1211247432, AR430W 1211249842. Inodes: 530 / 713 / 591 / 576 / 820 / 574.

There is **no compression id field in a v3 superblock** (the v4 `compression` field does not exist here); the
codec is established by decoding (see §5.2) — 7-Zip reports `Method = LZMA Spec` for every one of the six.

## 5. Handler `PATTERNS` match, and the oracle result

### 5.1 Pattern match (mechanical, no retyping)

`sqfs-handler-match.py` extracts every `PATTERNS` `HexString` body from the installed handler source and
compiles `[N]` to N wildcard bytes. Parsed 10 handlers / 18 patterns from
`…/unblob-…/unblob/handlers/filesystem/squashfs.py`; result over all six images: **exactly one match each —
`squashfs_v3_ddwrt`** at the carve offset, nothing else (`squashfs_v3` requires `hsqs`/`sqsh`,
`squashfs_v3_broadcom` requires `shsq`/`qshs`, `squashfs_v3_nonstandard` requires `sqlz`/`zlqs`). Raw log:
`artifacts/.../handler-match.log`.

The extractor's flag choice is then correct for both magics: `get_endian()` reads the 4 magic bytes as a
**big-endian** int and compares to `BIG_ENDIAN_MAGIC = 0x74717368` (`squashfs.py:318-352`,
`file_utils.py:350-361`). `tqsh` → BE int `0x74717368` → equal → `sasquatch -be`; `hsqt` → `0x68737174` →
not equal → `sasquatch -le`. §6 proves both choices are the right ones.

### 5.2 Oracle: no admissible oracle exists for these carriers

Every carrier, as published:

| reader | on the published `hsqt`/`tqsh` bytes | on a diagnostic `hsqs`/`sqsh` copy of the same bytes |
|---|---|---|
| `unsquashfs 4.7.5` `-s` | rc **1**, `FATAL ERROR: Can't find a valid SQUASHFS superblock` (all six) | rc 0, `Found a valid {little,big} endian SQUASHFS 3:0 superblock` |
| `unsquashfs 4.7.5` `-lls` | rc **1**, same fatal error, 0 entries | rc **1**, `gzip uncompress failed with error code -3` → `read_block: failed to read block @0x…` → `FATAL ERROR: File system corruption detected`, 0 entries |
| `7z 26.04` `l -slt` | rc **2**, `ERROR: … Cannot open the file as archive`, 0 entries | rc **0**, full listing; `Method = LZMA Spec`; entries 819 / 712 / 590 / 575 / 573 / 529 |
| `unsquashfs-backhand 0.25.5` `-l` (L1's chosen producer 1; `-k le_v3_0_lzma` / `be_v3_0_lzma`) | rc **1 with every one of its 13 kinds** (auto-detect fails all 13 on both magics) | rc **0**, full path list; paths identical to the 7-Zip listing for all six carriers (§13) |
| `bsdtar 3.8.10` `-tf` (libarchive) | — | rc **1**, `Error opening archive: Unrecognized archive format` (libarchive 3.8.10 has no SquashFS v3 reader at all; the same on a gzip v3 fixture) |

So the two readers **cannot agree on anything**: unsquashfs produces no path set for any candidate, and 7-Zip
never accepts the published magic. Two independent causes, either one fatal to the draft predicate:

- **D-1 magic gate.** Neither `unsquashfs` nor `7z` recognises `hsqt`/`tqsh`; they only accept `hsqs`/`sqsh`
  (and the Broadcom/`sqlz` variants are likewise unrecognised). This is the *published* bytes of every DD-WRT
  v24 rootfs.
- **D-2 codec gate.** After normalising the magic (diagnostic only), unsquashfs parses the superblock and then
  fails on the first compressed block with `gzip uncompress failed with error code -3` while 7-Zip decodes the
  same image completely. The measured v3 path of squashfs-tools 4.7.5 only ever invokes the gzip decompressor
  (the failure text names gzip alone, with no lzo/lz4/xz/zstd attempt as sasquatch shows), so the `lzma` entry
  in `unsquashfs -help-all` is `[INFERENCE]` the v4 LZMA compression id and is not reachable for v3. The DD-WRT
  v24 rootfs are **SquashFS 3.0 + LZMA**.

D-2 is not a DD-WRT quirk. The same measurement on every OpenWrt Kamikaze release I could sample, plus
DD-WRT v23, gives `hsqs` (standard magic) or `hsqt`, always `Method = LZMA Spec`, always `unsquashfs -lls`
rc = 1 (`artifacts/.../alt-family.tsv`):

| image | magic | version | codec | `unsquashfs -lls` | `7z l` entries |
|---|---|---|---|---|---|
| DD-WRT v23 std generic (from `stable/dd-wrt.v23/dd-wrt.v23.std.zip`) | hsqs | 2.1 | LZMA | rc 1 | 793 |
| OpenWrt Kamikaze 7.06 brcm-2.4 | hsqs | 3.0 | LZMA | rc 1 | 359 |
| OpenWrt Kamikaze 7.07 brcm-2.4 | hsqs | 3.0 | LZMA | rc 1 | 364 |
| OpenWrt Kamikaze 7.09 brcm-2.4 (DEVELOPMENT, never a C1 carrier) | hsqs | 3.0 | LZMA | rc 1 | 364 |
| OpenWrt Kamikaze 8.09 brcm-2.4 | hsqs | 3.0 | LZMA | rc 1 | 683 |
| OpenWrt Kamikaze 8.09 brcm47xx | hsqs | 3.0 | LZMA | rc 1 | 740 |
| OpenWrt Kamikaze 8.09 x86 `openwrt-x86-squashfs.fs` | hsqs | 3.0 | LZMA | rc 1 | 665 |

Consequence for the draft: its two named example carriers ("DD-WRT v24 `tqsh`", "OpenWrt Kamikaze 8.09
squashfs-3.0") **both** fail the draft's own oracle sentence "`unsquashfs` 4.7.5 (reads v1–v3 gzip)": the
parenthetical is the whole problem — the 2007–2009 v3 population that these vendors shipped is LZMA, so even a
standard-magic gzip requirement would not rescue them.

Corroboration, independently reached: seat `R42C1DevRun` (`R42C1DevRun.md:37-51,150-151,173-177`) measured the
same unsquashfs LZMA failure on the designated *development* OpenWrt images and calls the draft premise
falsified. What this seat adds on top is the **second, independent gate that only the DD-WRT family has**: the
published `hsqt`/`tqsh` magic is rejected by both named readers before any codec question arises, so no
diagnostic magic-normalisation-free oracle is possible for these carriers at all. Practical consequence for
carving: on DD-WRT images `unsquashfs -s` cannot supply the filesystem size; take `bytes_used` from the v3
superblock (offset 63 in the header struct) as this seat did.

### 5.3 7-Zip as an oracle producer: use the listing, never `7z x`

On a diagnostic standard-magic copy of DDWRT-BCM-MINI, `7z x` exits 2 with 74 sub-item errors, all of the form
`ERROR: Dangerous link path was ignored : sbin/adjtimex : ../bin/busybox` (72 symlinks) plus `../tmp`,
`../tmp/www`; the extracted tree holds 113 of the 187 listed symlinks and 370 regular files against 296 listed
(7-Zip materialises hard-linked busybox entries). An oracle built from `7z x` path sets would therefore
disagree with any other producer on ~one third of the symlinks. The listing (`7z l -slt`) is faithful:
`Path`, `Size`, `Mode` (`-rwxr-xr-x` / `drwxr-xr-x` / `lrwxrwxrwx`) per entry — that is the shape a v3 oracle
should compare.

## 6. The extraction half of C1 is sound (positive result, dev inputs only)

No REA, unblob or sasquatch was pointed at the carriers. Instead I built three development copies from
MIT-licensed unblob fixtures (4096-byte images) by rewriting the first four bytes to the DD-WRT magics, then
ran the frozen extractor path:

| input | tool | result |
|---|---|---|
| fixture `squashfs_v3_ddwrt/…/squashfs_v3_le.bin` (gzip) + magic→`hsqt` | `sasquatch -le -no-exit-code -f -d …` | rc 0, 2 files, `Non-standard SquashFS Magic: 'hsqt'` |
| same | `sasquatch -be` | rc 1, `FATAL ERROR: Block size or block_log too large` |
| fixture `squashfs_v3_adaptive/…/squashfs_v3_le.lzma.bin` (LZMA) + magic→`hsqt` | `sasquatch -le` | rc 0, 2 files |
| same | `sasquatch -be` | rc 1, same fatal error |
| fixture `…/squashfs_v3_be.lzma.bin` (LZMA) + magic→`tqsh` | `sasquatch -be` | rc 0, 2 files, `Non-standard SquashFS Magic: 'tqsh'` |
| same | `sasquatch -le` | rc 1, `Block size or block_log too large` |
| `hsqt` + LZMA copy | `unblob -d 2` (26.6.4) | rc 0, chunk `0x0-0x1000`, **`handler=squashfs_v3_ddwrt`**, 2 files |
| `tqsh` + LZMA copy | `unblob -d 2` | rc 0, chunk `0x0-0x1000`, **`handler=squashfs_v3_ddwrt`**, 2 files |

Table verbatim in `artifacts/.../dev-input-extraction.tsv`. So: the handler matches both DD-WRT magics, the
extractor picks the correct `-be`/`-le` per magic, sasquatch 4.5.1 decodes LZMA v3, and unblob reports no
failed chunk — the predicate's "names a `squashfs_v3*` handler with no failed chunk" half is achievable. Only
the oracle half is not.

Secondary observation for the C2 seat (not my axis, flagging only): the upstream `squashfs_v3_ddwrt` fixture
`little_endian/__input__/squashfs_v3_le.bin` (4096 B, sha256 `0161351caec8e9da…`) carries magic `hsqs` and
therefore matches handler **`squashfs_v3`**, not `squashfs_v3_ddwrt`; the `big_endian` fixture under that path
404s on the `26.6.4` media URL. The DD-WRT magic branch has no upstream fixture exercising it — which is why
the synthetic copies above were needed.

## 7. Ranking and a 4-carrier proposal (conditional on fixing the oracle)

Ranked for the C1 set by "full rootfs, both endiannesses, two or more product stories, simplest carve":

1. **DDWRT-FONERA** — richest rootfs (820 inodes; 569 files, 72 dirs, 178 symlinks), BE `tqsh`, rootfs at
   `0xD0000` after a vendor boot header.
2. **DDWRT-BCM-MEGA** — richest LE rootfs (713 inodes; 447 files, 58 dirs, 207 symlinks), TRX header declares
   the rootfs offset, so the container chain is self-evidencing.
3. **DDWRT-UBNT-LS2** — 591 inodes (362/61/167), BE `tqsh`, vendor ASCII header, and the **only candidate with
   a located product/version quote** (see §8).
4. **DDWRT-BUFFALO-ROOTFS** — 576 inodes (352/58/165), BE `tqsh`, **bare rootfs at offset 0** (simplest carve,
   no container parsing in the counter).
   Alternative for a 2-LE / 2-BE set: swap #4 for **DDWRT-BCM-MINI** (530 inodes, LE `hsqt`, 187 symlinks).

Composition caveats the L1 must weigh: (a) **all four would be published by the DD-WRT project** — the
"two or more publishers" preference is only met if per-device directories count as publisher diversity (I do
not think they do); (b) **no carrier contains device nodes** — `7z -slt` shows zero block/character devices in
all six, so the "devices" preference is unmeetable from this family; (c) symlink density is high (165–207 per
image), so the gap rule and the symlink mapping will dominate the score.

## 8. SOURCES-row material (located quotes)

- Ubiquiti LiteStation 2 — `https://download1.dd-wrt.com/dd-wrtv2/downloads/v24/Atheros%20WiSoc/Ubiquiti%20Litestation%202/LS2.dd-wrt-flashing.txt`
  (200, 1 072 B), line 1: **"Upgrading Ubiquiti LS2 to DD-WRT v24"**, and later **"LiteStation firmware file
  (e.g. LS2.dd-wrt.bin for LiteStation2)"**. This ties product, version and file name in one publisher text.
- All others: located quote is the publisher's directory index
  `https://download1.dd-wrt.com/dd-wrtv2/downloads/v24/` (200, 749 B) — `Index of /dd-wrtv2/downloads/v24/`
  listing `Atheros WiSoc/ 30-Jun-2008 13:14`, `Broadcom/ 18-May-2008 07:54`, `X86/`, `XScale/`, plus the
  per-product directories named in the URLs, plus the publisher's `v24/MD5SUMS` rows. `wiki.dd-wrt.com`
  version-history pages returned 301→404 at recon time, so **no wiki-level version quote exists for the
  Broadcom generic builds** — that gap must be accepted or filled by another seat.

## 9. carriers.json-ready records (schema of `R42C1Fetch/schema.md`)

Machine-readable set in `artifacts/.../carriers-ddwrt.json`: one record per candidate with
`id, claim, url, image_sha256, carve{offset,bytes_used,sha256}, kind, product, publisher, container_note,
handler, superblock{…}, oracle, nonregular, oracle_status, freezable` and **`freezable: false` on every one**.
Shape of one record:

```json
{"id":"DDWRT-BUFFALO-ROOTFS","claim":"R42-C1",
 "url":"https://download1.dd-wrt.com/dd-wrtv2/downloads/v24/Atheros%20WiSoc/BUFFALO%20WHR-HP-AG108/root.fs",
 "image_sha256":"7cb5eec56b1a2d88a0d286eb2dd11666ddbd08cacfcb4361d1ccbf1fcc66bc16",
 "carve":{"offset":0,"bytes_used":2602977,
          "sha256":"3b4e852f508a1839d395e424afa48f66be10ab887c1445e560e020cce8bdac63"},
 "kind":"vendor","product":"DD-WRT v24 root.fs for BUFFALO WHR-HP-AG108",
 "publisher":"DD-WRT project (download1.dd-wrt.com)","handler":"squashfs_v3_ddwrt",
 "oracle":null,"nonregular":null,"freezable":false}
```

No `container` object is emitted: for these images the firmware header is *inside* the downloaded file, so
`carve.offset` is relative to the image (the tool's `carve.offset + bytes_used <= len(image)` check holds —
§2). Note for `R42C1Fetch`: the schema's note that "round-42 carriers are already carved to the superblock
start" fits these records, but for DD-WRT the first four bytes are `hsqt`/`tqsh`, **not** `hsqs`.

## 10. Recommendations to the planner (pick one; the draft as written cannot pass)

- **A (recommended, and now measured): repair the oracle, keep the carriers.** Frozen oracle = `unsquashfs-backhand`
  0.25.5 (`-k le_v3_0_lzma` / `-k be_v3_0_lzma`, `-l` for paths, `-d` for extraction with links as links) **plus**
  `7z l -slt` / `7z x`, both on a copy of the pinned bytes normalised by a frozen 4-byte magic mapping
  (`hsqt→hsqs`, `tqsh→sqsh`). Measured on all six carriers: identical path sets (819/712/590/575/573/529), and on
  the sampled carrier 296/296 regular files agree on sha256 while backhand restores all 187 symlinks as symlinks
  (§13). The 4-byte mapping is deterministic and belongs to the oracle, never to the pin.
- **B: change the carrier family to gzip v3.** Then unchanged `unsquashfs` works. Status: **no such publisher
  found** — DD-WRT v23/v24 and OpenWrt Kamikaze 7.06–8.09 (brcm-2.4, brcm47xx, x86) are all LZMA (§5.2).
  Finding one costs another recon wave with no guarantee, and a gzip-only v3 population may be a narrow
  slice of what REA actually meets in the field.
- **C: keep one producer for this family** and record the codec/magic deviation in the counter (weakest: it
  retires the "two independent producers" property that R42-C1 is scored on). Not recommended.

## 11. Risks, limits, and open items

- Sampling limit: seven distinct DD-WRT images were measured (six v24 builds above plus the v23 build).
  `v24-sp1/Consumer/Broadcom Generic/` lists the same file names as `v24/Broadcom Generic/`, and the two
  Broadcom files I fetched from the `v24` tree are byte-identical to the `v24/MD5SUMS` entries for those
  names; SP1's own `MD5SUMS` was not compared. If a gzip-v3 DD-WRT build exists outside these, it was not
  found.
- Codec identification rests on 7-Zip's `Method = LZMA Spec` plus unsquashfs's gzip rejection; the DD-WRT
  squashfs-lzma variant is not the v4 LZMA id. Two independent tools agree on the observed behaviour.
- `7z` version sensitivity: 26.04; a different 7-Zip build could conceivably gate differently on the magic,
  so the frozen receipt must record the version (`7z` prints `26.04 (x64)`).
- No device nodes in any of the six rootfs; if the C1 set needs them, a different publisher is required.
- Publisher diversity: all six are DD-WRT-project builds (§7); with openwrt/kamikaze excluded (7.09
  development) or unusable (8.09 LZMA), a fourth-carrier "two or more publishers" row is still open.
- The round-41 evidence under `corpus/evidence/round-41/c1/` was not read for this seat (not needed for DD-WRT
  recon) and no round-41 path was touched.
- All inference is marked; every number above was printed by a command listed in `artifacts/.../` (fetch.log,
  handler-match.log, probe-matrix.json, superblocks.tsv, reader-oracle.txt, dev-input-extraction.tsv,
  alt-family.tsv).

## 12. Artifacts index (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C1ImgDdwrt/`)

| file | what it is |
|---|---|
| `sqfs3-probe.py` | v3 superblock parser (bytes only); prints fields, carve range, in-place carve sha256 |
| `sqfs-handler-match.py` | parses unblob 26.6.4 handler source, compiles every `PATTERNS` entry, matches raw images |
| `c1-img-probe.py` | per-candidate driver: superblock → carve → `unsquashfs -s/-lls` + `7z l -slt` → diagnostic standard-magic copy → repeat; JSON |
| `probe-matrix.json` | the six candidates' full reader matrix (rc, stderr, entry counts) |
| `handler-match.log` | pattern-match output (10 handlers / 19 patterns; only `squashfs_v3_ddwrt` matches) |
| `fetch.log` | per-URL `GET`, HTTP status, UTC access time, bytes, sha256, md5 |
| `superblocks.tsv` | every v3 superblock field per candidate |
| `oracle-matrix.tsv` | ranked candidate table incl. 7-Zip entry composition |
| `reader-oracle.txt` | human-readable reader matrix per candidate (published vs diagnostic copy) |
| `alt-family.tsv` | DD-WRT v23 + Kamikaze 7.06/7.07/7.09/8.09 measurements (magic, codec, readers) |
| `dev-input-extraction.tsv` | sasquatch flag matrix and unblob runs on fixture-derived `hsqt`/`tqsh` copies |
| `md5-vs-published.py`, `md5-verify.log` | MD5 of each downloaded image vs the publisher's `v24/MD5SUMS` (all MATCH) |
| `oracle-agreement.py`, `norm-matrix.json`, `norm-full-mini.json` | backhand + 7-Zip agreement on the normalised copy: path sets for all six, full sha256/type check on DDWRT-BCM-MINI |
| `chunk-end.tsv` | `bytes_used`, unblob `calculate_chunk` padding rule and `chunk_end` per carrier (all take the 4096 rule) |
| `carriers-ddwrt.json` | fetch-schema records incl. `chunk_end` and the measured oracle plan, all `freezable:false` |

No third-party firmware image and nothing extracted from one was copied into the lane; scratch
`/fast/scratch/hyaku/kaidoku-r42/R42C1ImgDdwrt` was removed.

## 13. Addendum — the L1's oracle pair measured on these carriers (backhand 0.25.5 + 7-Zip 26.04)

Written after the first yield, on the L1's decision that producer 1 is `unsquashfs-backhand` 0.25.5
(`/home/vgpnk/.local/opt/backhand-0.25.5-v3/bin/unsquashfs-backhand`, features v3/v3_lzma/gzip/xz) and producer
2 is 7-Zip. The six published images were re-fetched and re-digested: all six sha256 values are **identical**
to §2, so the measurements below are on the same bytes.

### 13.1 Backhand cannot read the published DD-WRT magic either

- `unsquashfs-backhand -l <carve>` (auto-detect): rc **1**; stderr enumerates `Failed le_v4_0:`, `Failed
  be_v4_0:`, `Failed le_v3_0:`, …, `Failed avm_be_v4_0:` — **all 13 kinds** fail.
- Explicit `-l -k <kind>` for each of the 13 kinds (`le_v4_0 be_v4_0 le_v3_0 be_v3_0 le_v3_0_lzma be_v3_0_lzma
  netgear_be_v3_0_lzma_standard netgear_be_v3_0_lzma le_v3_0_lzma_swap_standard be_v3_0_lzma_swap_standard
  le_v3_1_lzma_swap be_v3_1_lzma_swap avm_be_v4_0`) on an `hsqt` carve (BCM-MINI) and a `tqsh` carve (FONERA):
  rc **1**, 0 entries, every kind.
- Control on a development image: `openwrt-x86-squashfs.fs` (Kamikaze 8.09, `hsqs` + LZMA) — auto-detect rc 0,
  **665** entries; `-k le_v3_0_lzma` also 665. So the binary and its LZMA path work; the failure is the magic.
- Why no kind covers it: DD-WRT's `hsqt` is `hsqs` with one byte incremented (0x73→0x74), and `tqsh` likewise
  versus `sqsh` — not a byte swap, so the `*_lzma_swap_standard` kinds are not the same transform `[INFERENCE:
  inferred from the magic bytes and kind names; no backhand source read]`.

### 13.2 On a frozen 4-byte normalised copy the pair agrees exactly

Copy = pinned carve with bytes 0..3 set to the standard v3 magic for that byte order (`hsqt→hsqs`,
`tqsh→sqsh`); nothing else changes. Backhand kind follows the byte order.

| carrier | magic → norm | backhand kind | backhand `-l` paths | 7-Zip `l -slt` paths | files / dirs / symlinks (7-Zip) | path sets equal |
|---|---|---|---|---|---|---|
| DDWRT-FONERA | tqsh → sqsh | be_v3_0_lzma | 819 | 819 | 569 / 72 / 178 | **yes** |
| DDWRT-BCM-MEGA | hsqt → hsqs | le_v3_0_lzma | 712 | 712 | 447 / 58 / 207 | **yes** |
| DDWRT-UBNT-LS2 | tqsh → sqsh | be_v3_0_lzma | 590 | 590 | 362 / 61 / 167 | **yes** |
| DDWRT-BUFFALO-ROOTFS | tqsh → sqsh | be_v3_0_lzma | 575 | 575 | 352 / 58 / 165 | **yes** |
| DDWRT-AR430W | tqsh → sqsh | be_v3_0_lzma | 573 | 573 | 349 / 60 / 164 | **yes** |
| DDWRT-BCM-MINI | hsqt → hsqs | le_v3_0_lzma | 529 | 529 | 296 / 46 / 187 | **yes** |

(Driven by `oracle-agreement.py`; raw output `norm-matrix.json`.)

### 13.3 Content and type agreement, full check on DDWRT-BCM-MINI

| producer | regular files | symlinks | rc | note |
|---|---|---|---|---|
| backhand `-d` | 296 | **187** | 0 | every link restored as a link (`usr/tmp -> ../tmp` included) |
| `7z x` | 370 | 113 | 2 | 74 sub-item errors: 72 `Dangerous link path was ignored : sbin/* : ../bin/busybox`, plus `../tmp`, `../tmp/www`; the 72 link rows are materialised as files |

Common regular files 296; **sha256 agrees 296/296**; the only rows 7-Zip has that backhand does not are exactly
the 72 `../bin/busybox` link rows. So the pair is complete for regular content and backhand is the producer that
preserves symlinks; 7-Zip must not be used as the symlink authority (`7z x`), only as the path/size/mode
authority (`7z l -slt`) plus a content cross-check for the files it does write.

### 13.4 `chunk_end` (the REA input length the L1 asked for)

Unblob's `calculate_chunk` (`squashfs.py:77-100`, `PAD_SIZES = [4096, 1024]` at line 21) rounds `bytes_used` up to 4096, then 1024, when the tail is
zero padding. All six take the **4096** rule:

| carrier | offset | bytes_used | chunk_end | pad rule | bytes after chunk_end in the image | carve sha256 |
|---|---|---|---|---|---|---|
| DDWRT-BCM-MINI | 923872 | 1 992 951 | 2 918 624 | 4096 | 1824 | `e34b6446…54bc` |
| DDWRT-BCM-MEGA | 923752 | 5 090 570 | 6 015 080 | 4096 | 1944 | `f86ea69c…e404` |
| DDWRT-UBNT-LS2 | 852292 | 2 792 577 | 3 645 764 | 4096 | 20 | `3b130a5a…ac82` |
| DDWRT-BUFFALO-ROOTFS | 0 | 2 602 977 | 2 605 056 | 4096 | 0 | `3b4e852f…ac63` |
| DDWRT-FONERA | 851968 | 5 829 314 | 6 684 672 | 4096 | 0 | `a4a454a9…f10f` |
| DDWRT-AR430W | 851968 | 2 876 746 | 3 731 456 | 4096 | 0 | `9b3b9cc4…d441` |

`chunk-end.tsv` carries the same table; `carriers-ddwrt.json` now also records `chunk_end`,
`chunk_end_pad_rule` and the per-carrier oracle plan (`backhand -k …` + 7z, requiring the frozen
normalisation). `freezable` stays `false` in that file until the predicate text admits the normalisation.

### 13.5 Consequence for the freeze

The oracle rule must say, in as many words, that the 4-byte magic normalisation is part of the **oracle** and is
applied to a copy (the pin stays the published bytes), and that backhand's kind is derived from the carrier's
magic. If instead the rule requires both producers to read the published bytes verbatim, **no DD-WRT carrier can
freeze** and only option B (a gzip-v3 family, not yet found) remains.
