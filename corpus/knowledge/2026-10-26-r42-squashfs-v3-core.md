# SquashFS v3 through REA: the `squashfs_v3` handler family runs plain `sasquatch` with `-le`/`-be`, and four published LZMA rootfs images publish every oracle file (round 42, Core)

status: R42-C1 — scored by `tools/round-42/c1-counter.py` against the round-42 freeze `d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b`; the score receipt and its revision are in SCORECARD `## Round 42` and `.ufo/waves/round-42/l1/scores/`

source: S112 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — `SquashFSExtractor` :24-69 (`sasquatch` :25, `sasquatch-v4be` :26, the `match endian, self.version` argv decision :39-54, argv tail :56-64), `_SquashFSBase.calculate_chunk` :77-99, `squashfs_v3` :244-264, `squashfs_v3_ddwrt` :318-323
source: S116 — https://unblob.org/formats/ — the producer's SquashFS sections incl. `v3` and `v3-DDWRT` (a coverage statement, never an outcome)
source: S118 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/extractor.py — `fix_symlink` :50-92 (escaping links removed and reported, in-tree links kept)
source: S119 — https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz — `dist/firmware/FirmwarePublication.js` `unpublished-entry` and `depth-limited` gaps (anchors as the S119 row records them)
source: S131 — https://archive.openwrt.org/kamikaze/8.09.2/atheros/ — OpenWrt's own listing and md5sums for carrier OW-A8092 (opened 2026-10-26T22:53:30Z)
source: S132 — https://archive.openwrt.org/kamikaze/8.09/x86/ — OpenWrt's own listing and md5sums for carrier OW-X86FS (opened 2026-10-26T22:53:32Z)
source: S133 — https://download1.dd-wrt.com/dd-wrtv2/downloads/v24/Broadcom/Linksys/WRT54GL_1.0/ — DD-WRT's own listing and the v24 MD5SUMS line for carrier DW-MEGA (opened 2026-10-26T22:53:34Z)
source: S134 — https://download1.dd-wrt.com/dd-wrtv2/downloads/v24/Atheros%20WiSoc/Fonera/ — DD-WRT's own listing and the v24 MD5SUMS line for carrier DW-FONERA (opened 2026-10-26T22:53:35Z)
verified-at: 2026-10-26
recheck: 180d — `python3 -I -B tools/round-42/c1-counter.py --root . --rev <measured> --freeze d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b --pkg65 <rea-agents 6.5.0 root> --carrier-cache <DIR>` -> exit 0, `carriers_matched 4`; the cache is refilled from the publishers by `tools/round-42/fetch-carrier.py --spec .ufo/waves/round-42/c1/fetch-spec.json`, and a re-fetch whose bytes differ from the pins means this entry is re-read

**The family, from the handler source.** unblob 26.6.4 has four handlers whose name starts
`squashfs_v3`: `squashfs_v3` (`hsqs`/`sqsh`, S112 :244-264), `squashfs_v3_ddwrt` (`hsqt`/`tqsh`,
:318-323), `squashfs_v3_broadcom` and `squashfs_v3_nonstandard`. All of them share one
`SquashFSExtractor`: its binary is plain `sasquatch` (:25), and `sasquatch-v4be` is chosen only in the
`Endian.BIG, 4` branch (:40-50). A v3 chunk therefore runs `sasquatch -be` (:51-52) or `sasquatch -le`
(:53-54) with the tail `-no-exit-code -f -d {outdir} {inpath}`; the AVM marker branch has no v3 path.
The chunk ends at `bytes_used` rounded up to 4096 (else 1024) when that tail is zero (:77-99), so the
REA input of each carrier is the carve of exactly that length.

**The extractor that ran, measured.** A successful REA envelope does not name its extractor, and REA
deletes unblob's log with its task directory. The round-42 run harness therefore runs unblob through a
log tee (`tools/round-42/unblob-logtee.sh`, arguments unchanged) under one fixed PATH and keeps the log
beside each receipt (`corpus/evidence/round-42/c1/<id>/unblob.log`, digests in `extract-env.json`). The
logged extract command on all four carriers is `sasquatch -be …` on the two big-endian images and
`sasquatch -le …` on the two little-endian ones; `sasquatch-v4be` appears in none.

**The oracle is two readers that are not sasquatch.** All four carriers store their blocks as LZMA:
the OpenWrt Kamikaze and DD-WRT v24 `squashfs-lzma` 3.0 writers emit raw LZMA1 streams with no props
header. squashfs-tools `unsquashfs` 4.7.5 reads v3 blocks as gzip only and refuses these images
(`gzip uncompress failed with error code -3`, round-42 `w1/R42C1DevRun.md`), so the oracle is
backhand-cli 0.25.5 built with its `v3,v3_lzma` features plus 7-Zip 26.04 (`7z l -slt` gives each
entry's mode, `7z x` the regular-file contents). The DD-WRT magics `hsqt`/`tqsh` are normalised to
`hsqs`/`sqsh` on a copy for the readers only; the pins are the published bytes. The two readers agree
on every regular file of all four carriers (`oracle-run.json` verdict `agree`), and symlink targets come
from backhand's extracted tree (7-Zip rewrites absolute links and drops escaping relative ones on
extraction, `w1/R42C1Sentinel.md` §10 A3).

**Measured on four published images no extractor touched before the freeze.**

| carrier | publisher image | magic, byte order, handler | carve [offset, length) | oracle regular / symlinks / dirs | published / gaps |
|---|---|---|---|---|---|
| OW-A8092 | OpenWrt Kamikaze 8.09.2 `atheros/openwrt-atheros-root.squashfs` (image sha256 `b3d3008e…9608967`) | `sqsh`, BE, `squashfs_v3` | [0, 1564672) | 409 / 177 / 95 | 409 files; 177 `unpublished-entry` + 1 `depth-limited` |
| OW-X86FS | OpenWrt Kamikaze 8.09 `x86/openwrt-x86-squashfs.fs` (`48d2c54d…310bef8`) | `hsqs`, LE, `squashfs_v3` | [0, 1183744) | 403 / 167 / 94 | 403 files; 167 + 1 |
| DW-MEGA | DD-WRT v24 `dd-wrt.v24_mega_generic.bin`, TRX (`abd0db4d…92a3b9`) | `hsqt`, LE, `squashfs_v3_ddwrt` | [923752, +5091328) | 447 / 207 / 58 | 447 files; 207 + 1 |
| DW-FONERA | DD-WRT v24 `Atheros WiSoc/Fonera/linux.bin` (`e9910533…40bb57`) | `tqsh`, BE, `squashfs_v3_ddwrt` | [851968, +5832704) | 569 / 178 / 72 | 569 files; 178 + 1 |

Every regular file is published at its exact path under `firmware.bin_extract/` with the oracle's
sha256 and size, and no other file is published. Every symlink — absolute targets such as
`etc/mtab -> /proc/mounts` included — stays in-tree as one `unpublished-entry` gap; no
`MaliciousSymlinkRemoved` report occurred on these four images (unblob's sanitiser rewrites an absolute
target against the extraction root before testing containment, S118 :79-91). Directories are invisible.
No carrier holds a device node, so that clause of the gap rule is not exercised here. Each image's
md5 equals the publisher's own md5sums line (S131–S134).

**What this supersedes.** Before this round the lane held SquashFS v3 only as the producer's coverage
statement (`2026-10-26-unblob-format-matrix`, "coverage claim only, never an extraction outcome") and
as the v3 triage table's cause text. For `squashfs_v3` and `squashfs_v3_ddwrt` on LZMA bodies this
entry is the outcome; the format-matrix row stays as written (a producer statement), and the dated
pointer is in `PROVINCE.md` `## Round-42 additions to Core`.

**Limits.** v1 and v2 images, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies and
SquashFS v4 Broadcom are not measured. The counter's REA rerun shows the carriers extract the same way
at scoring time; it cannot prove which process wrote a committed receipt (R40-CL2). Nothing is claimed
about the programs in the published files. The images are not committed; the URL → image sha256 →
carve → pin chain (`.ufo/waves/round-42/c1/fetch-*.json`) is the provenance.
