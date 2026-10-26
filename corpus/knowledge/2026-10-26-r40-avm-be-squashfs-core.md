# Genuine AVM-layout big-endian SquashFS v4 extracts through REA: big-endian fields, little-endian block lengths, no `-be` (round 40)

source: S124 — https://raw.githubusercontent.com/Freetz-NG/freetz-ng/9a7236926bffaa6af16f84b3db27017cb5f02724/make/host-tools/squashfs4-be-host/patches/350-unsquashfs__AVM_BE.patch — the reader patch that swaps only the 2-byte metadata block length — opened 2026-10-26 (`.ufo/waves/round-40/w1/R40SrcFreetz.md`)
source: S125 — https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/ — `info_en.txt`: FRITZ!Box 6490 Cable, FRITZ!OS 07.57 — opened 2026-10-26 (`.ufo/waves/round-40/w1/R40SrcAvmVendor.md`)
source: S126 — /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv — the retained round-11 AVM-BE image observation, re-opened 2026-10-26 (assimilated from `merge/kaidoku` `avm-image-extraction`, `.ufo/waves/round-40/w1/R40AssimE3.md`)
source: S114 — https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt — line 8, block length little-endian; lines 13-14, the marker — re-read 2026-10-26
source: S112 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — lines 44-50, `is_avm = header.bytes_used == header.mkfs_time`; `-be` only when false — as read 2026-10-26
source: S121 — https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/squashfs-tools/unsquashfs.c — lines 664-669 (`read_block` swaps the block-length header only when `swap` is set) and 4390-4394 (`-be` sets `swap`) — as read 2026-10-26 (`.ufo/waves/round-40/w1/R40SrcSasquatchAvm.md`)
verified-at: 2026-10-26
recheck: 180d — `python3 -I -B tools/round-40/fetch-vendor.py --root . --rev main --cache <DIR>` -> exit 0 (both vendor chains still resolve to their pins)

**The layout, from sources.** AVM's SquashFS 4 variant keeps every structural field big-endian (`sqsh`
magic) but stores "the block length value at the beginning of each block" little-endian (S114 line 8);
the Freetz-NG reader patch swaps exactly the 2-byte metadata block-length header and nothing else (S124).
AVM also writes `mkfs_time == bytes_used` (S114 lines 13-14). unblob 26.6.4 picks the `squashfs_v4_be`
handler from the magic and appends `-be` to `sasquatch-v4be` only when that marker is false (S112 lines
44-50); `sasquatch-v4be` without `-be` reads the block-length header in host (little-endian) order and
with `-be` swaps it (S121 lines 664-669, 4390-4394). So the marker is the trigger and the block-length
byte order is the format: a marker on a standard-BE body (the round-39 writer's `--endian avm`) loses
`-be` and fails, and a genuine body with the marker stripped receives `-be` and fails
(`.ufo/waves/round-40/w1/R40C1MarkerBoundary.md`, H1/H2 confirmed on development images).

**The test the lane uses.** Walk the metadata headers from `inode_table_start` reading each 2-byte
length little-endian (mask `0x8000`); on an AVM body the walk lands exactly on `directory_table_start`
and the big-endian reading does not (`tools/round-40/sqfs-list.py --layout auto --inspect`, the
`layout_ok` clause of `tools/round-40/c1-counter.py`). On the four round-40 carriers and on the 7490
07.62 and 7430 07.31 development members the identity is exact (`.ufo/waves/round-40/w1/R40C1ReconGaps.md` §2).

**Core, measured (R40-C1).** REA 6.5.0 `extract-firmware --max-depth 1` (unblob 26.6.4,
`sasquatch-v4be` 4.5.1 on the child PATH) on four frozen carriers, receipts
`corpus/evidence/round-40/c1/{V1,V2,L1,L2}/after.json`:

| carrier | what | regular files published = oracle | gaps | chunk |
|---|---|---|---|---|
| V1 | FRITZ!Box 6490 Cable FRITZ!OS 07.57 (S125), member `./var/remote/var/tmp/filesystem.image` carved to `bytes_used` 5442392 | 697 | 263 `unpublished-entry` (one per symlink) + 1 `depth-limited` | one `squashfs_v4_be`, not failed |
| V2 | FRITZ!Box 6820v1 LTE FRITZ!OS 07.30, member `./var/tmp/filesystem.image` carved to 26013550 | 8 (one is the nested `filesystem_core` image) | 85 + 1 | same |
| L1 | lane-built AVM layout, xz (`tools/round-40/mk-l-carriers.py`) | 7 | 2 + 1 | same |
| L2 | lane-built AVM layout, gzip | 6 | 2 + 1 | same |

Every published file matches the independent reader's oracle by path suffix and sha256; directories and
the character device `dev/led` are invisible (no gap, no file), absolute symlinks are re-rooted and kept
as one gap each, and no symlink escapes. The counter re-runs REA on each carrier at scoring time and
compares the `plus-extractor` projection. Vendor bytes are not committed (the AVM licence forbids
redistribution): `tools/round-40/fetch-vendor.py` rebuilds them from URL → image sha256 → tar member →
carve length → carrier sha256 (`.ufo/waves/round-40/c1/carriers.json`).

**Lineage (assimilated).** The lane's rounds 9-11 lead built a 4096-byte genuine AVM-BE image and saw
unblob run `sasquatch-v4be -no-exit-code -f -d …` with no `-be` and publish its four files (S126; image
sha256 `c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32`, first header `7400` → LE 116,
`121 + 2 + 116 = 239 = directory_table_start`). That observation was re-opened this round and is now
reproduced on vendor images with lane receipts; the round-11 log carries no exit code, so it is lineage,
not a scored receipt.

**Correction.** `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md:40` ("An image whose `mkfs_time`
equals `bytes_used` loses `-be` and fails") holds only for a standard-BE body carrying the marker; a
genuine AVM-layout body with the marker extracts without `-be` (table above).

**Why `--max-depth 1`.** At REA's default depth 3 a vendor member descends into its nested
`filesystem_core` image and exceeds the 10000 staged-entry budget, so REA returns
`unreadable_output` with no chunk list; depth 1 is the deepest setting that yields a receipt for every
carrier and records one `depth-limited` gap at the carve directory (`.ufo/waves/round-40/w1/R40C1ReconGaps.md` §3, §6).

**Limits.** Two vendor images (two model families, FRITZ!OS 7.30 and 7.57) and two lane-built images;
the nested `filesystem_core` of V2 is not opened; LE AVM members (`hsqs`) and AVM kernel images are not
covered. REA records no extractor argv on success, so "no `-be`" rests on the handler source and direct
`unblob -v` logs, not on the receipt. The rerun binding shows the carriers extract through the pinned
toolchain at scoring time; it cannot prove which process wrote a committed receipt.
