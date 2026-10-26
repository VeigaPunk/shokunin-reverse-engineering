# R40C1VendorV1 — C1 carrier V1 provenance, superblock and AVM-layout byte proof

**Verdict: DONE** — the V1 chain closes at every link on measured bytes (URL → HTTP 200 → image
sha256 = the pin → tar member path/offset/sha256 → byte range → carrier sha256); the member is a
big-endian SquashFS v4 superblock (`sqsh`, v4.0, xz, 64 KiB blocks, marker
`mkfs_time == bytes_used = 5442392` hold) whose metadata block-length headers are **little-endian**,
proved twice (inode-table and directory-table header chains land exactly on the next table start only
under LE; the BE reading overshoots every table); the carrier bytes are recommended as
`member[0:bytes_used)` (5442392 B, sha256 `ac4098bd…8e95`) because the whole member injects an
8-byte `UnknownChunkReport` into every unblob/REA run (measured on a dev fixture of identical shape,
never on the carrier); `sasquatch-v4be -ll` extracts the carve with exit 0 / 1079 entries while
`sasquatch-v4be -be -ll` fails with exit 1 / 0 entries.

Seat: leaf. **No REA and no unblob run was made on V1, on the vendor image, or on any C1 carrier.**
All unblob runs below were on fresh dev fixtures / a fresh `gen-squashfs.py` tree. Read-only git only;
no VCS mutation; nothing installed (no pacman transaction, `sasquatch*`/`unblob` untouched).
Scratch `/fast/scratch/hyaku/kaidoku-r40/R40C1VendorV1` removed at exit; everything cited is copied
into `.ufo/waves/round-40/w1/artifacts/R40C1VendorV1/` (5.5 MB, incl. the 5 442 392 B carrier).

Item boundaries honoured: superblock parse, first metadata header both ways, tail analysis, carrier
recommendation, `sasquatch-v4be -ll` and `-be -ll` on the carved bytes. No oracle, no REA receipt, no
held-out data.

---

## 1. Provenance chain (every link, with digests)

| # | link | measured |
|---|---|---|
| 1 | URL | `https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/FRITZ.Box_6490_Cable-07.57.image` |
| 1 | HTTP | **200**, `Content-Length: 39741440`, `Server: nginx`, `Last-Modified: Mon, 04 Sep 2023 17:08:03 GMT`, `ETag: "64f60ef3-25e680e"`, `Accept-Ranges: bytes` (`curl -sS -D headers.txt`, exit 0, 4.63 s) |
| 2 | image | 39 741 440 B, sha256 **`f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d`** — **equals the pinned digest** |
| 2 | container | plain POSIX tar, 21 entries, no compression, tar stream ends at 39 732 224 B |
| 3 | tar member | `./var/remote/var/tmp/filesystem.image`, size 5 443 592, tar header @ 32 025 600, **data @ 32 026 112 … 37 469 704**, sha256 **`334e56dfba6a785590bb5cdbd78fcb5be183b9af160b51fc8935a3015ad3f3d4`**; `image[32026112:37469704]` byte-equal to the extracted member |
| 4 | byte range | `[0, 5442392)` = the superblock's `bytes_used` (BE u64 at superblock offset 40..48) |
| 5 | carrier | `carrier-v1-be.sqsh`, 5 442 392 B, sha256 **`ac4098bd11a76f8ad001faac0f1a5e018708d9b03943dfebb2b18a24e0038e95`**, byte-equal to `member[:5442392]` |

Supporting identity (not part of the carrier, recorded for the freeze's provenance note):
`./var/version` = `FIRMWAREVERSION=141.07.57,,107830,120308002013` (47 B, sha256
`288451fe…bdb3`); `./var/info.txt` 2807 B, sha256 `b0360d88…e39b`. The LE sibling member
`./var/remote/var/tmp/x86/filesystem.image` is 28 200 968 B, sha256 `7ea4c628…0419` — recorded,
**not** a C1 carrier.

Machine-readable: `provenance.json` (`chain.1_url` … `chain.5_carrier`, plus `member_shape` and the
`carrier_choice` rationale).

## 2. Superblock (BE; `superblock.json`, emitted by `sb-parse.py`)

| field | value |
|---|---|
| magic | `sqsh` (`73 71 73 68`) → **big-endian** |
| s_major / s_minor | **4 / 0** |
| compression | id **4 = xz**; `block_log` 16 ↔ `block_size` **65 536** (consistent) |
| inode_count | **1079** |
| fragment_count | 112 |
| bytes_used | **5 442 392** |
| mkfs_time | **5 442 392** → **AVM marker `mkfs_time == bytes_used` holds** |
| mkfs_time as date | 1970-03-04T23:46:32Z (a byte-count proxy, not a timestamp — same trap as R39's 1970-date fingerprint) |
| root_inode_ref | `0x1c48130a` → block 7240, offset 4874 (inside the inode-table span) |
| flags | 0x02c0 = duplicates \| exportable \| no-xattrs, **no** compressor-options block |
| id_count | 1 |
| xattr_id_table_start | `0xFFFF…FFFF` (absent) |
| inode_table_start | 5 421 468 |
| directory_table_start | 5 430 042 |
| fragment_table_start | 5 440 850 |
| lookup_table_start | 5 442 362 |
| id_table_start | 5 442 384 |

Table ladder strictly increasing `inode < dir < frag < lookup < id < bytes_used`, so every structure is
inside the carved extent. The id table is the last 8 bytes (`00 00 00 00 00 53 0b 4a`, one u64 pointer).

## 3. Metadata block-length endianness — the load-bearing test

First header at `inode_table_start = 5 421 468`, bytes `64 05`:

- **little-endian → 1380** (flag clear, compressed): `5 421 468 + 2 + 1380 = 5 422 850 ≤ 5 430 042`
- **big-endian → 25 605**: `5 421 468 + 2 + 25 605 = 5 447 075`, **past `directory_table_start` and past
  `bytes_used`** → impossible.

Plausibility alone is a heuristic, so the decisive test is the whole-chain landing (`sb-walk.py`,
`metadata-chain.json`):

| table | LE chain | BE chain |
|---|---|---|
| inode table → `directory_table_start` (span 8574) | **5 headers** `[1380, 1872, 2204, 1776, 1332]` (= sum 8574 + 5·2) — **lands exactly** on 5 430 042 | 1 header `[25605]` — overshoots to 5 447 075 |
| directory table → `fragment_table_start` (span 10 808) | **4 headers** `[3216, 3612, 3316, 656]` — **lands exactly** on 5 440 850 | 3 headers `[4108, 5912, 10784]` — ends at 5 450 852 |

Control on a **standard** BE body (fresh `gen-squashfs.py --endian be --comp gzip`, 3526 B, sha256
`240375b9…b25df1`): the inverse holds — BE lands exactly (`265 + 2 + 3106 = 3373 =
directory_table_start`), LE does not. So the test discriminates in both directions and is not a
constant.

Same test on the LE sibling member: LE chain of 24 headers lands exactly, BE chain of 3 does not.

**Caveat that the round-40 oracle must not be built on** (measured): xz-decompressing the first
metadata block with the **over-long BE length 25 605 still yields a valid 8192-byte metadata block**,
because the decoder stops at the end of the xz stream and ignores trailing bytes. Length-vs-§
"decompression succeeded" therefore cannot separate LE from BE when the wrong length is *longer*; only
the chain-landing (or a checksummed full-table walk) can. Conversely the wrong length is detectable
when it is *shorter*.

## 4. What is past `bytes_used` (member 5 443 592 B; R39 saw chunk `0-5443584`)

| range | bytes | content |
|---|---|---|
| `[0, 5 442 392)` | 5 442 392 | the filesystem |
| `[5 442 392, 5 443 584)` | **1192** | **all `0x00`** — page padding |
| `[5 443 584, 5 443 592)` | **8** | vendor trailer `23 de 53 c4 2a 99 c5 51` (not a match for crc32/adler32 of either prefix; meaning unknown, not needed by the claim) |

Why R39 saw chunk end 5 443 584: `unblob` 26.6.4 `_SquashFSBase.calculate_chunk`
(`…/unblob/handlers/filesystem/squashfs.py:77-98`, handler sha256 `2d7b901b…9287`) rounds
`bytes_used` up to a `PAD_SIZES` value ([4096, 1024], line 21) **only if the bytes read at
`bytes_used` are that many zeros** (line 92). `round_up(5442392, 4096) = 5443584`, and those 1192
bytes are zero, so the chunk stops at 5 443 584 and the 8-byte trailer is left outside it.

The **same shape** repeats in the LE member: 28 200 968 B, `bytes_used` 28 200 029, 931 zero bytes to
28 200 960, then the **same 8-byte trailer**. So pad+trailer is an AVM firmware convention, not part
of either SquashFS.

## 5. Carrier bytes: recommendation and the measurement behind it

Measured chunk behaviour on three dev fixtures of identical shape (`gen-squashfs.py --endian be`,
`bytes_used` 3526; `chunk-arithmetic.txt`, `rep-A/B/C.json`) — **dev inputs, never the carrier**:

| fixture | shape | unblob 26.6.4 report |
|---|---|---|
| A exact `bytes_used` | 3526 B | `ChunkReport 0→3526 squashfs_v4_be`; **no unknown chunk**; 4 files; identification 100.00 % |
| B + zeros to 4096 | 4096 B | `ChunkReport 0→4096`; no unknown chunk |
| C B + 8-byte trailer (**= V1's shape**) | 4104 B | `ChunkReport 0→4096` **+ `UnknownChunkReport 4096→4104 size=8`** |

**Recommendation: carrier = `member[0:bytes_used)` = 5 442 392 B, sha256 `ac4098bd…8e95`.**

- Whole member (5 443 592 B): chunk `0→5 443 584` **plus an 8-byte unknown chunk**, i.e. unknown-chunk
  noise inside the C1 subject that the frozen projection would have to carry or explain. Rejected.
- `[0, bytes_used)` : the padding test reads EOF, fails, and the fallback returns `0→5442392` = the
  whole file — one chunk, next to no noise, and it adds the invariant **carrier size == its own
  `bytes_used`** (a cheap extra binding for P40-C1). Chosen.
- `[0, 5 443 584)` (pad to 4096): also one clean chunk, but ships 1192 vendor zero bytes that belong to
  no filesystem and destroys that invariant. Fallback only if some tool insists on a 4 KiB multiple —
  nothing measured here does.

Exact reproduce command, in `CARVE.md` (download → sha256 check → `tar -x` → `BU=$(python3 …)` →
`head -c "$BU"`). It yields `BU=5442392` and the sha256 above, `stat -c %s` = 5442392.

## 6. Direct `sasquatch-v4be` reads of the carved bytes (allowed)

`sasquatch-v4be` 4.5.1 (2022/03/17), binary sha256
`fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`.

```
$ sasquatch-v4be -ll carrier-v1-be.sqsh          # no -be
exit=0   1079 lines
  squashfs-root                         (dir)
  squashfs-root/bin                     (dir)
  squashfs-root/bin/aicmd               -rwxrwxrwx 8888
  squashfs-root/bin/ash -> busybox
  …
stderr (3 lines):
  SquashFS version [1024.0] / inode count [923009024] suggests a SquashFS image of a different endianess
  Trying to decompress using default xz decompressor...
  Successfully decompressed with default xz decompressor

$ sasquatch-v4be -be -ll carrier-v1-be.sqsh
exit=1   0 lines
stderr:
  Reading a different endian SQUASHFS filesystem on carrier-v1-be.sqsh
  read_id_table: failed to read id table block
  FATAL ERROR: File system corruption detected
```

That is exactly the marker-driven split: the same bytes list completely **without** `-be` and die
**with** it. Note also that the "different endianess" stderr sentence appears on the *successful* run —
it is not a failure signal (matches R39's warning not to key on it).

Entry census from that listing (`listing-summary.txt`): **118 dirs, 697 regular files, 263 symlinks,
1 char device** (`dev/led`, `247,0`) = 1079 entries.

## 7. Two freeze-critical consequences I measured (not in the draft yet)

**(a) The frozen gap rule must be sized for 264 non-regular entries on V1.** Of the 263 symlinks,
**234 are in-tree** and **29 have absolute targets** (`/var/tmp/passwd`, `/etc/default.049`,
`/usr/sbin/upgradebox`, `/dev/null`, `/./lib/libled2.so.2.2.0`, …). Under the R39-measured
unblob/REA behaviour, in-tree links become one `unpublished-entry` gap each and absolute links are
removed/rewritten with `MaliciousSymlinkRemoved`; the char device is never published. A rule derived
from development recon that allows, say, "≤2 gaps" would fail V1 even with a perfect extraction. The
draft's phrasing ("only the extraction gaps the frozen gap rule allows") is fine only if the rule is
stated in terms of entry classes, not a magic count. **The exact split (234 / 29 / 1) is in
`listing-summary.txt`** and the full per-link list can be regenerated from `sq-list-noflag.txt`.

**(b) The round-39 oracle cannot read this carrier, so the round-40 `--avm` mode is load-bearing.**
`python3 -I -B tools/round-39/sqfs-list.py carrier-v1-be.sqsh --files … --symlinks … --inspect`
→ **exit 2**, stderr `sqfs-list: metadata body out of bounds: offset 5436876 length 29708, image
5442392 bytes`. The R39 reader decodes standard-BE block lengths, desynchronises in the AVM layout, and
refuses. So (i) there is **no independent file census for V1 yet** — my 697-file count is
sasquatch-derived, and the "same relative-path suffix + same sha256 for every regular file" binding
has nothing independent to check it against until the AVM-mode oracle lands; (ii) the oracle's AVM mode
must key on **LE block lengths** and should validate itself by the chain-landing test in §3, not by
"decompression succeeded".

## 8. Limits, open questions, inference

- `[INFERENCE]` The data-block size arrays inside inode headers were **not** examined by this seat
  (that is the oracle's parse). If the AVM variant leaves those big-endian while metadata lengths are
  LE, the oracle will fail its sha256 comparison and the failure will be visible; `sasquatch-v4be`
  without `-be` reading all 1079 entries suggests it does not, but I did not prove it.
- `[INFERENCE]` The 8-byte trailer's meaning is unknown; I checked crc32 and adler32 of both plausible
  prefixes and neither matches, so I make no claim about it. It is excluded by the recommended carve.
- The `sqsh` magic at `0x0` plus `mkfs_time == bytes_used` is the marker **proxy**; the format test is
  the block-length endianness (§3). Both hold here.
- The 1079-entry census is sasquatch-derived (§7b), so it is evidence for the freeze's expectations,
  not an independent oracle.
- No claim is made about the LE sibling member beyond its shape and that it carries the marker.
- Not examined: anything inside the extracted tree (programs, kernel images, `var.tar`), AVM wrapper
  layers above the member, V2 selection (a second vendor image — not chosen here).

## 9. Evidence index (all under `.ufo/waves/round-40/w1/artifacts/R40C1VendorV1/`)

| file | what |
|---|---|
| `carrier-v1-be.sqsh` | the recommended carrier, 5 442 392 B, sha256 `ac4098bd…8e95` |
| `provenance.json` | the whole chain, `member_shape`, `carrier_choice` (+ rejected alternatives and why) |
| `superblock.json` | every superblock field, marker, ladder, flags, first header both ways |
| `metadata-chain.json` | inode/directory chain walks LE vs BE for carrier + LE member + dev control |
| `CARVE.md` | exact carve command, byte-shape table, why not the whole member, what may not run |
| `chunk-arithmetic.txt`, `rep-A/B/C.json` | unblob chunk/unknown-chunk records for the three dev shapes |
| `sq-list-noflag.txt`, `sq-list-noflag.err` | `sasquatch-v4be -ll` full listing + stderr |
| `sq-list-be.err`, `sq-list-be.txt.empty-because-be-failed` | `-be -ll` failure (exit 1, zero lines) |
| `listing-summary.txt` | entry census, 234 in-tree / 29 absolute links, top-level entries, char device |
| `headers.txt`, `tar-listing.txt`, `info.txt`, `version` | HTTP headers, tar inventory, vendor metadata |
| `sb-parse.py`, `sb-walk.py`, `emit.py`, `chunkdump.py` | the tools used (stdlib only; `emit.py` regenerates the three JSONs) |
| `SHA256SUMS.txt` | sha256 of every artifact file |

Reproduce the JSONs: `python3 emit.py <scratch-with-files> <artifacts-dir>`.

Exact commands and exit codes are quoted inline in §1–§6; every number above is read from those files.

## 10. Hand-over to the freeze (concrete claim edits)

1. Pin the carrier as **`carrier-v1-be.sqsh` = `member[0:bytes_used)`**, sha256
   `ac4098bd11a76f8ad001faac0f1a5e018708d9b03943dfebb2b18a24e0038e95`, 5 442 392 B, and add
   "carrier size == its own `bytes_used`" as a cheap superblock binding. Provenance must name the tar
   data range `[32026112, 37469704)` as well as the member path.
2. Keep "first metadata block length decodes as little-endian" but strengthen it to the **chain
   landing test** for both the inode and the directory table (a one-header check is satisfiable by a
   standard-BE body with a lucky first header; the chain is not).
3. State the gap rule by **entry class** (in-tree link, absolute/escaping link, char device, hard
   link) — V1 alone carries 234 + 29 + 1.
4. Require the round-40 oracle to reproduce **697 regular files** and to print an independent entry
   census; the round-39 reader exits 2 on this carrier (§7b), so the census currently has no
   independent source.
5. Do not key any table row or control on the "different endianess" stderr sentence (§6).
