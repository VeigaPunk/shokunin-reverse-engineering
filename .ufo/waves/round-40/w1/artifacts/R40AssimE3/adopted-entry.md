# A real AVM-layout big-endian SquashFS image builds and extracts — and the marker is a timestamp proxy, the block-length endianness is the layout

source: S123 — /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv (sha256 `f205807de8016ead8732d77f14acf5e99e6527e02d6281566f6070b7c8539eb0`) — rows `image_path`, `image_magic`, `image_mkfs_time`, `image_bytes_used`, `image_is_avm`, `unblob_handler`, `unblob_command_verbatim`, `unblob_be_flag`, `extracted_files` — re-opened 2026-10-26
source: S124 — /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/freetz-squashfs4-host-be.mk (sha256 `48fb043d8fb2e9b1ea916abb06316bb99a3c3d2232d8694e6f6f651a0393a3d5`) — lines 1-4, the pinned source, md5 and site — re-opened 2026-10-26
source: S125 — https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt (1496 B, sha256 `c1c43f6f97d7477dcdab15203d11e43b49beb12e3a43a3b52bdd71b672a9a5d5`) — lines 5, 8 and 13-14, the layout and marker bullets — as read 2026-10-26
source: S108 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — `SquashFSExtractor` lines 40-52, the AVM branch — as read 2026-10-26
source: S107 — https://github.com/onekey-sec/sasquatch/releases/tag/sasquatch-v4.5.1-6 — the amd64 `usr/bin/sasquatch-v4be` digest `fac88740…` — as read 2026-10-26
source: S121 — https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/squashfs-tools/unsquashfs.c (sha256 `ece42b66…cb40`) — lines 664-669, the block-length swap in `read_block`, and lines 4390-4394, `-be` setting `swap` — as read 2026-10-26
verified-at: 2026-10-26
recheck: 180d — `sha256sum /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/avm-be.squashfs` -> `c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32` (ran 2026-10-26)
ground: the lane's open lead from rounds 9-11 — does a genuine AVM-BE image extract through unblob, and what in its bytes makes it AVM-BE rather than standard big-endian v4

**Claim (falsifiable).** The 4 096-byte image at the absolute path above, sha256
`c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32`, is a genuine AVM-layout
big-endian SquashFS v4 (`magic` `sqsh`, compression id 4 = xz, `mkfs_time` 365 == `bytes_used` 365,
metadata block-length headers little-endian), and it extracts through unblob 26.6.4, which builds
`sasquatch-v4be -no-exit-code -f -d {outdir} {inpath}` with **no `-be`**, publishing all four files
with their exact contents. Re-running the hashes and the retained log either reproduces that or the
entry is wrong.

**The layout, from sources, before any measurement.** Freetz's own description of the format
(S125, lines 5-8): AVM-BE replaces "the little-endian data layout" of stock SquashFS-4 with a
big-endian one, and — the load-bearing bullet — "the only data field stored in the little-endian
format is the block length value at the beginning of each block"; its super-block field `mkfs_time`
"contains … the same value as the super-block field `bytes_used`" (lines 13-14). So an AVM-layout
image is **big-endian superblock + little-endian 2-byte metadata block-length headers**; the marker
is a separate, timestamp-shaped property.

**The producer branch that makes this matter.** unblob 26.6.4, installed handler at
`/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`,
sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` — byte-identical to tag
26.6.4 (S108). Lines 40-52 parse the superblock **big-endian**, then:

```python
is_avm = header.bytes_used == header.mkfs_time      # :48
if not is_avm:                                     # :49
    commands_args.append("-be")                    # :50
```

The source comment on those lines cites exactly S125's document. So unblob's *extractor-argument*
choice keys on `mkfs_time == bytes_used`; its *handler* choice never does (magic plus endianness
only). On the extractor side the flag reaches the field that matters: `read_block` byte-swaps the
2-byte block-length header if and only if `swap` is set (`unsquashfs.c:664-669`, S121), `-be` sets
`swap` to 1 on a little-endian host (`:4390-4394`), and `sasquatch-v4be` is the `-DFIX_BE` build of
sasquatch 4.5.1. Without `-be`, that header is therefore read in host (little-endian) order — the
AVM layout — while `-be` would force big-endian and misread an AVM body.

**The image itself (observation, re-measured 2026-10-26).** Superblock read big-endian, both
readings of the first metadata header at `inode_table_start` taken:

| field | value |
|---|---|
| magic | `sqsh` (big-endian) |
| mkfs_time / bytes_used | 365 / 365 — marker **true** |
| compression id | 4 (xz) |
| inode_table_start / directory_table_start | 121 / 239 |
| first metadata header bytes | `7400` |
| length decoded little-endian | **116** — and 121 + 2 + 116 = 239 = `directory_table_start` |
| length decoded big-endian | 29 696 — the identity fails |

Two independent signals agree that the block-length field is little-endian, i.e. the body is the
AVM layout, not standard BE. Command:
`python3 -I -B .ufo/waves/round-40/w1/artifacts/R40AssimE3/probe-avm-layout.py <image>` from the lane
root, output `probe-output.tsv` beside it.

**The extraction (observation, from the retained log, not re-run).** The round-11 run retained
`unblob.log` (sha256 `352e0d794143df9cc4fa6113d72ee5a620ea0aa201a930e00e91590518aed5d7`): a
`Found valid chunk chunk=0x0-0x1000 handler=squashfs_v4_be`, then
`Running extract command command='sasquatch-v4be -no-exit-code -f -d /tmp/r11-avm3/avm-be.squashfs_extract …'`
— no `-be` — then four `Processing file` lines for `apple1.txt`-`apple4.txt` (6, 7, 5 and 7 bytes).
The TSV records the contents (`apple` … `date`). An earlier retained run in the same directory
(`avm-final.log`, 2026-10-24 09:01) ended in `Can't run extract command` with
`dependencies=['sasquatch-v4be']`; the successful record is the 12:01:54 log, whose working
directory and output path are `/tmp/r11-avm3`, not the `-e /tmp/r11-avm` of the earlier attempt.
**Limit:** the retained log carries no exit status and no version banner, so "exit 0" and
"unblob 26.6.4" are not in that file — the version is pinned by the installed handler digest above,
and a receipt with a recorded exit code is what a scored claim needs (QUALITY #18).

**The marker is a timestamp proxy; the layout is the block-length byte order.** Four images from
this seat's own bytes (2026-10-26), classed by the identity test, none of them run through
unblob/sasquatch here:

| image | marker | block lengths | class |
|---|---|---|---|
| the retained AVM image (S123) | true | LE (116 fits) | AVM layout |
| `control-avm-markerstripped.sqsh` — same bytes, `mkfs_time` 365 → 1 | false | LE (116 fits) | **AVM layout** |
| `control-standard-be.sqsh` — `gen-squashfs.py --endian be` | false | BE (168 fits) | standard BE |
| `control-avm-mode.sqsh` — `--endian avm`, i.e. the same bytes with the marker written in | true | BE (168 fits) | **standard BE** |

The two generator controls are 373 B each and differ **only** in bytes 8-12: patching
`control-standard-be.sqsh`'s `mkfs_time` to its `bytes_used` reproduces `--endian avm` byte for byte
(0 differing bytes, sha256 `e68f6a53…`). So the marker mispredicts the layout in both directions,
and `gen-squashfs.py --endian avm` is a marker transform, not an AVM-layout writer — it cannot emit
little-endian block lengths.

**What this corrects.** (1) `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md:40` — "An image
whose `mkfs_time` equals `bytes_used` loses `-be` and fails" — holds only for a **standard-BE** body
carrying the marker; a genuine AVM-layout body with the marker extracts successfully without `-be`
(the retained run above), and with the marker stripped it keeps its AVM layout. The sentence is
narrowed here, not withdrawn. (2) `SKILL.md:339`'s `avm-marker-be-dropped` row keys the outcome on
`mkfs_time equals bytes_used`; on this evidence the row's discriminator must be the **block-length
endianness**, or a genuine AVM-layout image is mislabelled as broken. That table is R40-C2's
surface and is named here only as the consequence. (3) The `-be`-chosen failure direction
(standard BE with the marker → 0 files, exit 1) is round-39's measurement
(`.ufo/waves/round-39/w1/R39AssimAvmCritic.md`), not this entry's.

**Not examined.** One directory with four small files: this is a format-conformance carrier, not a
firmware tree. No vendor AVM member was opened or extracted here; nothing is claimed about AVM's
own images, about their wrappers, or about the extracted programs. The extraction was not re-run in
round 40 and no REA call was made; the `unblob` argv decision is read from the pinned source, and
the round-11 outcome is read from the retained log. Fragment handling, xattrs, sparse files and
payloads larger than one metadata block are untested here. `sasquatch`/`sasquatch-v4be` 4.5.1's own
layout detection was not re-derived from source, only exercised.

---

Target path: `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`
Stem (for `corpus/README.md` mapping and PROVINCE's Core row): `2026-10-26-r40-avm-be-squashfs-core`
