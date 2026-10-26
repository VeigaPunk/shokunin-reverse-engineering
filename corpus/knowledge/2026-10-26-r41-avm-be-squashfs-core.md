# Genuine AVM-layout big-endian SquashFS v4 extracts through REA: big-endian fields, little-endian block lengths, no `-be` (round 41, Core)

status: R41-C1 `see SCORECARD `## Round 41`` — either `met` at `the commit that adds this text` with `carriers_matched = 4` and every binding true (`tools/round-41/c1-counter.py`, exit 0, ``.ufo/waves/round-41/l1/scores/``), or the honest stop that replaces this line and the PROVINCE row

source: S112 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — lines 44-50: `is_avm = header.bytes_used == header.mkfs_time`, and `-be` is appended only when it is false — as read 2026-10-26 (19 842 B, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`, equal to the installed copy)
source: S114 — https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt — lines 8-9: "the only data field stored in the little-endian format is the block length value at the beginning of each block"; lines 13-14: `mkfs_time` "contains … the same value as the super-block field `bytes_used`" — re-read 2026-10-26 (1 496 B, sha256 `c1c43f6f97d7477dcdab15203d11e43b49beb12e3a43a3b52bdd71b672a9a5d5`)
source: S124 — https://raw.githubusercontent.com/Freetz-NG/freetz-ng/9a7236926bffaa6af16f84b3db27017cb5f02724/make/host-tools/squashfs4-be-host/patches/350-unsquashfs__AVM_BE.patch (byte-identical to the Freetz master copy) — the reader patch: a new `swap_block_length` selector (patch lines 7-9), `read_block` swaps the 2-byte length header only when it is set (lines 12-25), and for `TARGET_FORMAT == AVM_BE` on a little-endian host `swap_block_length = 0` while `swap` still comes from the magic (lines 33-45) — as read 2026-10-26 (2 217 B, sha256 `7f0a1b252d4bbde747efe98d1f97b52eab28d55ee957b7307d0344cbe1e220fc`)
source: S121 — https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/squashfs-tools/unsquashfs.c — lines 664-669 (`read_block` swaps the block-length header only when `swap` is set) and 4389-4400 (`-be` sets `swap`); the `squashfs-v4be` build is the same tree with `-DFIX_BE`, so on this little-endian host it reads the AVM length header in host order — as read 2026-10-26 (round-40 citation, unchanged bytes)
source: S125 — https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/ — FRITZ!Box 6490 Cable, FRITZ!OS 07.57, the development-input vendor identity of round-40 V1 — as read 2026-10-26
source: S126 — /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv — the retained round-11 AVM-BE image observation, re-opened 2026-10-26 (lineage only; no exit code)
source: S127 — https://download.avm.de/fritzbox/fritzbox-5490/other/fritz.os/ — vendor identity of the V3 image (FRITZ!Box 5490, FRITZ!OS 07.31): listing sha256 `88c8d6485e1400cc77d8881bec189d065a045f5fe8ee285528eafaab8c4a19f4`, `info_en.txt` sha256 `e3100cdaeae9d72c8f8637119e492677ef074c468394e6d52a21fe73b7360d18`, opened 2026-10-26
source: S128 — https://download.avm.de/fritzbox/fritzbox-5491/other/fritz.os/ — vendor identity of the V4 image (FRITZ!Box 5491, FRITZ!OS 07.31): listing sha256 `badbb744ff9d916fb52b4e89d6bd613009fc1b5891f115fa93b74c73583af6f7`, `info_en.txt` sha256 `ec2528eb91f16d35c9245c8f7c276a57edd7fb58344a649fa1add451051970b4`, opened 2026-10-26
verified-at: 2026-10-26
recheck: 180d — `python3 -I -B tools/round-41/fetch-vendor.py --root . --rev main --cache <DIR>` -> exit 0 (both vendor chains resolved to their pins on 2026-10-26 (`tools/round-41/fetch-vendor.py`, exit 0)); `python3 -I -B tools/round-41/sqfs-list.py --layout avm --inspect` on each carrier still reports `layout=avm`

**The layout, from sources.** AVM's SquashFS 4 variant keeps every structural field big-endian (`sqsh`
magic, and the superblock, inode, directory, fragment-entry and lookup fields) but stores "the block
length value at the beginning of each block" little-endian (S114 lines 8-9). The reader that implements
it adds a `swap_block_length` selector beside the existing `swap`: on a little-endian host working on an
AVM body it leaves the 2-byte metadata block-length header unswapped while the rest of the superblock is
byte-swapped (S124). AVM also writes `mkfs_time == bytes_used` (S114 lines 13-14). unblob 26.6.4 picks
`squashfs_v4_be` from the magic and appends `-be` to `sasquatch-v4be` only when that marker is false
(S112 lines 44-50); `sasquatch-v4be` without `-be` reads the length header in host (little-endian) order
and with `-be` swaps it (S121 lines 664-669, 4389-4400).

So the four things are separate and must not be conflated: the marker (`mkfs_time == bytes_used`) is the
*trigger* unblob reads; the block-length byte order is the *format*; `-be` is the *argv token*; and the
`squashfs-v4be` build is the *binary*. A marker on a standard-BE body loses `-be` and fails, and a
genuine body with the marker stripped receives `-be` and fails (round-40 H1/H2,
`.ufo/waves/round-40/w1/R40C1MarkerBoundary.md`).

**The test the lane uses.** Walk the metadata headers from `inode_table_start`, reading each 2-byte length
little-endian (mask `0x8000`); on an AVM body the walk lands exactly on `directory_table_start` and the
big-endian reading does not (`tools/round-41/sqfs-list.py --layout avm --inspect`, the `layout_ok` clause
of `tools/round-41/c1-counter.py`). The counter accepts either the exact single-block identity
`inode_table_start + 2 + len == directory_table_start` or the plausibility walk; the reader `--layout avm`
and `--layout auto` must agree, and `--layout be` must refuse. Measured on V3: LE walk `30231260 + 2 + 724
== 30231986 == directory_table_start` (exact), BE first header reads 54 274 and the walk fails, and the
all-BE reader exits 2 (`.ufo/waves/round-41/w1/artifacts/R41C1VendorV3/{inode-chain-walk.txt,layout-be.log}`).
On the round-40 development carrier V1 the same identity is exact (697 regular files, 263 in-tree
symlinks, 381 non-regular rows; `.ufo/waves/round-41/w1/artifacts/R41C1Fetch/reader-real-vendor.txt`).

**The exact-path rule (R40-CL1, repaired).** Round 40's frozen counter compared a receipt path to an
oracle row with `candidate == rel or candidate.endswith('/' + rel)`. On L2 that scored the published
regular file `firmware.bin_extract/usr/bin/busy` as the symlink entry `bin/busy` and failed
`nonregular_unpublished_ok`, so the claim stopped at 3/4 (`.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json`).
A suffix is not a path. The round-41 rule resolves every receipt path against its chunk's extract root and
compares for equality: unblob extracts chunk `X` into `X_extract`, and rea-agents 6.5.0 stages every input
as `firmware.bin` (`FirmwareFiles.snapshotFirmware`), so the `$input` chunk's root is `firmware.bin_extract`;
a chunk nested under `$output/<p>` keeps the whole `<p>_extract/` prefix, which no table row can name, and
several handler chunks with no `$input` handler chunk fail closed with `extract_root` null. The prototype
(`.ufo/waves/round-40/w2/artifacts/R40W2C1Refreeze/c1-counter-exact-match.diff`, diff sha256
`8fa0a813297eb5ca4f20ed449bcac61c1d3d053ef6793664c22a15e83779c0a8`) tightened `oracle_hits_ok`,
`gaps_ok` and `nonregular_unpublished_ok` and relaxed none; its selftest went 70 -> 75 cases with 7 green /
68 red, and a suffix-matcher mutant died on three cases (a regular file is not the symlink entry, the
reverse direction, a deeper file with the oracle row's sha256 does not publish the oracle row, a gap on a
deeper file does not resolve to the entry). Re-scored on the round-40 receipts it reports 4/4 where the
frozen counter reported 3/4 (`summary.json` runs 1-3 of that directory).

**Measured: four frozen carriers, none touched by REA or unblob before the freeze.** Carriers V3 and V4
are vendor images fetched by `tools/round-41/fetch-vendor.py` (AVM licence forbids redistribution: only
digests and the rebuild command are committed); L3 and L4 are lane-built with
`tools/round-41/mk-l-carriers.py` (a copy of the round-40 writer `--endian avm-genuine`, which emits the
genuine layout: big-endian structural fields, little-endian 2-byte metadata length headers,
`mkfs_time == bytes_used`). Oracle rows and the layout facts are measured on the frozen bytes; the
published set, gaps and the REA receipt exist only after the freeze runs:

| carrier | what | oracle regular files | non-regular entries | published / gaps after the freeze run | chunk |
|---|---|---|---|---|---|
| V3 | FRITZ!Box 5490 FRITZ!OS 07.31 (S127), member `./var/tmp/filesystem.image` carved to `bytes_used` 30 233 394 — xz, 104 inodes, LE header walk exact | 8 | 95 (9 dirs, 85 symlinks, 1 char device `dev/led`) | 8 files published; gaps 85 `unpublished-entry` + 1 `depth-limited` (`corpus/evidence/round-41/c1/V3/after.json`) | one `squashfs_v4_be` chunk, not failed |
| V4 | FRITZ!Box 5491 FRITZ!OS 07.31 (S128), member `./var/tmp/filesystem.image` — the nested `filesystem_core.squashfs` carved to its own `bytes_used` (32 720 860 B); xz, 7 367 inodes | 6 349 | 1 017 (401 dirs, 615 symlinks, 1 char device) | 6349 files published; 615 symlinks accounted as 611 `unpublished-entry` gaps + 4 `MaliciousSymlinkRemoved` removals, + 1 `depth-limited` | one `squashfs_v4_be` chunk, not failed |
| L3 | lane-built AVM layout, xz, 37 inodes, 187 892 B — both-direction path collisions: regular `usr/bin/busy` / symlink `bin/busy`, symlink `usr/sbin/tool` (absolute, in-tree) / regular `sbin/tool`; relative in-tree links; empty regular file | 13 | 23 (20 dirs, 3 symlinks) | 13 files published; gaps 3 `unpublished-entry` + 1 `depth-limited` | one `squashfs_v4_be` chunk, not failed |
| L4 | lane-built AVM layout, gzip, 35 inodes, 169 545 B — the same collision shapes, gzip compression id 1 | 14 | 20 (17 dirs, 3 symlinks) | 14 files published; gaps 3 `unpublished-entry` + 1 `depth-limited` | one `squashfs_v4_be` chunk, not failed |

Counter: `tools/round-41/c1-counter.py --root . --rev <REV> --freeze d764389e9cbe61b9d1b07538ff3bff02d50bb34f --pkg65 <rea-agents 6.5.0
root> --carrier-cache <DIR>` -> `.ufo/waves/round-41/l1/scores/` (scored by `tools/round-41/c1-counter.py` after the commit that adds this text; result in SCORECARD `## Round 41`). The counter
re-runs each carrier's bytes at scoring time and compares the `plus-extractor` projection, so a receipt
fabricated from the oracle cannot pass (routed R39-CL5), and it replays the receipt's `max_depth`; a rerun
it cannot perform is `rerun_env_error` (exit 2), never met. One carrier carries gzip (L4) and the rest xz,
so both decompressor legs are bound.

**The fetch chain binds `member_sha256` (R40-CL6, repaired).** `tools/round-41/fetch-vendor.py` checks
url -> `image_sha256` -> tar member -> `member_sha256` -> (optional) nested file read out of the member
with the reader -> carve to `length` -> carrier pin, and fails closed (`link: member_sha256`) when a spec
omits the member digest. Measured on the round-40 development chain: V1 image
`f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d`, member
`334e56dfba6a785590bb5cdbd78fcb5be183b9af160b51fc8935a3015ad3f3d4`, carrier pin
`ac4098bd11a76f8ad001faac0f1a5e018708d9b03943dfebb2b18a24e0038e95`; corrupting the pinned member digest
turns the same bytes red at that link (`.ufo/waves/round-41/w1/artifacts/R41C1Fetch/vendor-chain-evidence.txt`).

**What round 40 measured and why it stopped.** Round 40 published every oracle file on four carriers
(V1 697, V2 8, L1 7, L2 6 regular files; one gap per symlink plus one `depth-limited`) and still stopped:
the counter matched 3 of 4 at `42c10a58` on the L2 suffix false positive (R40-CL1), and its PROVINCE row
was therefore recorded as **measured, not promoted** (`PROVINCE.md` `## Round-40 measured, not promoted
(R40-C1 honest stop)`). The images were faithful; the test was not. Round 41 keeps the round-40 receipts
admissible as development evidence, changes the matching rule, and re-scores on four carriers no
extractor had touched.

**Why `--max-depth 1`.** At REA's default depth 3 a vendor member descends into its nested
`filesystem_core` image and exceeds the 10 000 staged-entry budget, so REA returns `unreadable_output`
with no chunk list; depth 1 is the deepest setting that yields a receipt for every carrier and records
one `depth-limited` gap at the carve directory (round-40 §6). V3 stages 103 entries. V4 stages
7367 staged entries by the reader count (budget 10 000) — 7 367 by the oracle's own count, 73.7 % of the budget, which is why the V4
carrier choice is a fill above.

**Lineage (assimilated).** The lane's rounds 9-11 lead built a 4 096-byte genuine AVM-BE image and saw
unblob run `sasquatch-v4be -no-exit-code -f -d …` with no `-be` and publish its four files (S126; image
sha256 `c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32`, first header `7400` -> LE 116,
`121 + 2 + 116 = 239 = directory_table_start`). That log carries no exit code, so it is lineage, not a
scored receipt. The same identity is now reproduced on vendor bytes: V3's LE walk, the direct
`sasquatch-v4be` extraction without `-be` (8/8 file digests, 85/85 symlink targets, 0 mismatches,
`.ufo/waves/round-41/w1/artifacts/R41C1VendorV3/crosscheck.txt`), and the all-BE reader's refusal.

**Correction to the round-40 record.** `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md` and its
PROVINCE block recorded the layout correctly but the status `measured, not promoted`, on a counter whose
suffix test produced a false negative; both are history as of the round-41 row, not a live status. The
round-39 note's AVM sentence ("AVM-BE bodies … stay Frontier") is superseded for the genuine layout only:
an AVM body whose marker has been stripped is a standard-BE body and behaves as round 39 measured.

**Limits.** Two vendor models of one FRITZ!OS generation (5490 and 5491, 07.31) and two lane-built
images; the nested `filesystem_core` of V3 is not opened (it is one published regular file), and V4's
publication depth is whatever the V4 carrier fill allows. LE AVM members (`hsqs`), AVM kernel
images, AVM bodies with a stripped marker, fragments/xattrs on vendor images and other vendor-mangled
SquashFS variants are not covered. REA records no extractor argv on success, so "no `-be`" rests on the
installed handler source (S112) and direct `sasquatch-v4be` logs, not on the receipt. The counter's rerun
binding shows the carriers extract through the pinned toolchain at scoring time; it cannot prove which
process wrote a committed receipt. Vendor bytes are not committed and not redistributable: the digests
plus `tools/round-41/fetch-vendor.py` are the provenance [S127 licence lines 663-670 / S128 686-693 restrict
redistribution and reverse engineering; the lane publishes derived metadata only].
