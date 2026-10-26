# DRAFT (not landed) — admitted entry B, rewritten

Source package file: `merge/kaidoku/knowledge/corpus/knowledge/avm-le-image-genuine-marker.md`
(staged S212–S214). Round 40 verdict: **ADMIT-AFTER-REWRITE** (`.ufo/waves/round-40/w1/R40AssimReject.md`,
row 3) with three named corrections, deferred "LE scope; admissible in an LE-AVM round after its
`:30`/`:55-56` corrections" (`corpus/lessons/round-40.md:81`).
Proposed lane path: `corpus/knowledge/2026-10-26-r42-avm-le-marker-le-squashfs.md`
Proposed lane rows: S132, S133 (own-work TSVs), S134 (613 patch), S135 (550 patch), S136 (cli.py) —
see `sources-rows.md`. Held rows reused: S108 (handler).

Bytes the lane does not hold today are imported beside this draft, under
`../imported/` (`sha256-manifest.txt`): the three 4096-byte images, both TSVs, the 613 patch, the
23-patch Freetz set, the build scripts and the build log.

**Evidence landing (proposed).** The lane's own precedent is row-keyed evidence directories —
`corpus/evidence/round-41/s126/avm-be.squashfs` (4096 B) + `lead1-avm-image.tsv` + its `.sha256`
for the round-40 row S126. Proposed: `corpus/evidence/round-42/s132/`
(`avm-le-genuine.squashfs`, `avm-le-plain550.squashfs`, `avm-le-standard-time.squashfs`,
`lead2-avm-le-genuine.tsv`, `613.patch`, `550-….patch`, `patches/`, `build-avmle*.sh`,
`build-avmle.log`) and `corpus/evidence/round-42/s133/` (`lead2-stale-build.tsv`). Total 76 KB, all
lane-built or third-party **patch text** — no third-party firmware image and nothing carved from
one, so the lane's copy prohibition does not bite.

---

source: S132 — `../imported/lead2-avm-le-genuine.tsv` (own-work, imported 2026-10-26 from `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/lead2-avm-le-genuine.tsv`, 940 B, sha256 `523637c885bb50c6d445bb096f247b9a66ab33633cae46af18be4a3d4c1b9ffa`) — rows `route`, `tarball_md5`, `image_path`, `mksquashfs_arguments`, `superblock_magic`, `superblock_compression`, `mkfs_time`, `bytes_used`, `avm_marker`, `patched_unsquashfs_stat`, `unblob_handler`, `unblob_command`, `unblob_result`, `sasquatch_v4be_direct` — as measured 2026-10-24; not a real Fritz!Box image, not unblob behaviour on the big-endian arm
source: S133 — `../imported/lead2-stale-build.tsv` (own-work, imported 2026-10-26 from the same campaign directory, 964 B, sha256 `4c962bacd24af8132f31ce78c8e8ddf03d501f221f3590ef6bd69beafb339951`) — rows `binary_sha256_before_no_clean_rebuild`, `make_output_on_changed_define`, `binary_sha256_after_no_clean_rebuild`, `conclusion`, `clean_rebuild_plain_freetz_550_define_AVM_LE`, `clean_rebuild_avm_format_as_option_without_flag`, `clean_rebuild_avm_format_as_option_with_no_mkfs_time` — as measured 2026-10-24
source: S134 — https://raw.githubusercontent.com/Freetz-NG/freetz-ng/86c23d96d76585825fa81b5cb29105e9d2ad6654/tools/make/squashfs4-host-be/patches/613-avm_format_as_option.patch — commit `86c23d96d765`, "squashfs4: enable timestamp at superblock" (2020-07-19); fetched 2026-10-26T21:52:15Z, HTTP 200, 1601 B, sha256 `9af3b3debee9f6a144c03411a439e51f4ba4f9a1bd3aaac6b8760fa9394193f8`, byte-identical to `../imported/613.patch`; the file is **absent on Freetz-NG `master` today** (HTTP 404, 2026-10-26T21:52:42Z), so the commit pin is load-bearing
source: S135 — `../imported/patches/550-mkfs_time__AVM_BE_AVM_LE.patch` — the Freetz plain-set patch that hard-wires the marker and adds the patched reader's message; byte-identical to https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/patches/550-mkfs_time__AVM_BE_AVM_LE.patch as fetched 2026-10-26T21:54:49Z (HTTP 200, 1080 B, sha256 `603c36c9e610a4f1a41548d167b7b984c8c7ac587c73fa5b19d1484d2aab15a7`); the `master` URL can move, the imported bytes cannot
source: S136 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/cli.py — tag 26.6.4, 20221 B, sha256 `fc775f1ad66f05c0f6ba77fb74c80112ea99b4baf07900d7d701b7932259f86c`, equal to the installed copy: `get_exit_code_from_reports` maps `(Severity.WARNING, 0)`; not unblob's handler choice, not sasquatch behaviour
source: S108 — unblob SquashFS handler at tag 26.6.4 (held row) — `SquashFSExtractor.extract` lines 40-54, re-read 2026-10-26: `is_avm = header.bytes_used == header.mkfs_time` sits inside `case Endian.BIG, 4:`, and `case Endian.LITTLE, _:` appends `-le` without parsing the header
verified-at: 2026-10-26
recheck: 180d — `sha256sum ../imported/avm-le-{genuine,plain550}.squashfs` → both `18d3ad0563cce852a438fe414d881909a6097fc30a38ca523372931cfcafaee4`; and `unsquashfs -s ../imported/avm-le-genuine.squashfs | sed -n '2,3p'` → `Creation or last append time Wed Dec 31 21:06:01 1969` / `Filesystem size 361 bytes` (ran 2026-10-26); a differing digest or a non-361 filesystem size means the entry is re-read
ground: `PROVINCE.md:408` — "Still Frontier: **LE AVM members (`hsqs`)** …"; wave-12 CANNOT-ANSWER item 2

# An AVM_LE image is reachable from a clean plain-Freetz build — and on unblob's little-endian arm the marker changes nothing

**Claim.** An image carrying the AVM marker (`mkfs_time == bytes_used`) **is** reachable through the
recipe the lane holds, and the round-12 finding that it was not is overturned: that finding was an
artefact of a **stale build tree**, not a property of the route.

**The recipe, and the two patches that make it.** squashfs-tools 4.3 (md5
`d92ab59aabf5173f2a59089531e30dbf`) plus Freetz's 23-patch set plus Freetz-NG's
`613-avm_format_as_option.patch` (S134), built with `-DTARGET_FORMAT=AVM_LE`.

The marker is not added by the option patch. Freetz's plain set already hard-wires it: patch
`550-mkfs_time__AVM_BE_AVM_LE.patch` (S135) writes `sBlk->mkfs_time = (int) sBlk->bytes_used;` under
`#if (TARGET_FORMAT == AVM_BE || TARGET_FORMAT == AVM_LE)` with **no further condition**. What
`613` adds is a switch around it: `int use_standard_mkfs_time = TRUE;` and the field assignment
guarded by `if (!use_standard_mkfs_time)`, with `-no-mkfs-time` setting that variable `FALSE`
(S134, hunks at patch lines 7-9, 17-19, 27-29) and help text "-no-mkfs-time … use AVM format
(length instead of timestamp)".

**Measured consequence (S133, S132).** A **clean** rebuild of the plain Freetz recipe with
`-DTARGET_FORMAT=AVM_LE` and **no** `-no-mkfs-time` produced `avm-le-plain550.squashfs`
(`mkfs_time` 361 == `bytes_used` 361) — and that file is **byte-identical** to the image the
option build produced with `-no-mkfs-time`, `avm-le-genuine.squashfs`:
`sha256 18d3ad0563cce852a438fe414d881909a6097fc30a38ca523372931cfcafaee4`, 4096 B, both. The
option build **without** the flag keeps a real timestamp (`avm-le-standard-time.squashfs`,
`6d787405…`, creation time `Sat Oct 24 16:51:00 2026`).

**What unblob does with it.** `handler=squashfs_v4_le`, argv
`sasquatch -le -no-exit-code -f -d {outdir} {inpath}`, and all four files extracted, `apple1.txt`
reading `apple` (S132; the round-40 seat reproduced the same handler and argv independently,
`.ufo/waves/round-40/w1/R40AssimReject.md`). The same image through the big-endian extractor
refuses: `sasquatch-v4be -be` exits 1 with "FATAL ERROR: Block size too small.  File system is
corrupt." and writes 0 files (re-run 2026-10-26, `../receipts/v4be-refusal.txt`).

**Why the marker is invisible *there*, and nowhere else.** The handler reads the marker only on the
big-endian v4 arm: `is_avm = header.bytes_used == header.mkfs_time` is inside `case Endian.BIG, 4:`
and decides whether `-be` is appended (S108, lines 48-50). `case Endian.LITTLE, _:` appends `-le`
without parsing the superblock at all (lines 53-54). So for a *little-endian* image the marker
changes no byte of unblob's plan — while on the big-endian arm unblob **does** recognise it and
drops `-be` (that arm is held separately: `corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md`).

**The file count is the witness, not the exit code.** unblob maps `Severity.WARNING` to exit 0
(S136, `get_exit_code_from_reports`) and `ExtractCommandFailedReport` carries
`severity: Severity.WARNING`, so a failed extraction exits 0 with zero files. Any claim about
success on this route must cite the published/extracted file count.

**Why round 12 measured it the other way.** That build re-ran `make` in an already-built tree after
changing the `-D` define. A changed `-D` is not a dependency `make` tracks: the rebuild printed
"'mksquashfs' is up to date." and the binary's sha256 was unchanged across it
(`1a7cfcf719459961ba1608185557e9c5` before and after, S133). The image that produced round 12's
"NOT AVM" reading therefore came from the inert `-DTARGET_FORMAT=AVM_BE_AVM_LE` define, which
matches neither branch of the `#if`.

**What the stock readers say.** Stock `unsquashfs` 4.7.5 renders the marker image's creation time as
`Wed Dec 31 21:06:01 1969` (-03) — epoch + 361 s, i.e. `mkfs_time` read as a timestamp — beside
`Filesystem size 361 bytes`. The "not available because of modified AVM-format (mkfs_time ==
bytes_used)" wording is the **patched** reader's, added by the same patch 550 (S135, unsquashfs
hunk); the staged entry's TSV row named `upstream_unsquashfs_stat` is relabelled
`patched_unsquashfs_stat` here.

**What this does not say.** It does not say anything about a real Fritz!Box little-endian member
(none was downloaded; `PROVINCE.md:408` keeps "LE AVM members (`hsqs`)" Frontier). It does not say
the option build is unnecessary in general — it says the marker needs the right define and a clean
build, and that `613` only makes the marker optional. One recipe, one toolchain version, one host:
the squashfs-tools 4.3 tree itself is not retained (the `patches/` set, the images, the scripts and
the build log are), so a re-run re-fetches the 4.3 tarball by md5 and re-applies the imported
patches.

---
