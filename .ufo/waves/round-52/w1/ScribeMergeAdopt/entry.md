# AVM-LE is stock little-endian SquashFS with one superblock field changed (`mkfs_time == bytes_used`), and the marker is a writer switch, not a format flag

source: S253 — Freetz-NG `docs/make/README.md` at commit `86c23d96d76585825fa81b5cb29105e9d2ad6654`, the `squashfs4-le` package entry (lines 573-574) — 85 254 B, sha256 `1147751130102031452a39cf2736c400da277038c0807a93b34f4e09ff906b4b` — re-read 2026-10-30
source: S254 — Freetz-NG `tools/make/squashfs4-host-be/patches/613-avm_format_as_option.patch` at the same commit — 1 601 B, sha256 `9af3b3debee9f6a144c03411a439e51f4ba4f9a1bd3aaac6b8760fa9394193f8` — re-read 2026-10-30
source: S255 — Freetz-NG `tools/make/squashfs4-host-be/patches/550-mkfs_time__AVM_BE_AVM_LE.patch` at the same commit — 1 080 B, sha256 `603c36c9e610a4f1a41548d167b7b984c8c7ac587c73fa5b19d1484d2aab15a7` — re-read 2026-10-30
source: S256 — Freetz-NG `tools/make/squashfs4-host-le/squashfs4-host-le.mk` at the same commit — 2 622 B, sha256 `6d2abb494ac23d9d50dcf88d6b739b0af9eb31568ab3442cf9cb278da0f8f799` — re-read 2026-10-30
source: S260 — Freetz-NG `tools/make/squashfs4-host-be/patches/250-mksquashfs__AVM_BE.patch` at the same commit — 2 775 B, sha256 `f5964ad9bf2d24d319763e28f78bd441cd1d683d087e9b2e7bcd77d1db1b908d` — re-read 2026-10-30
source: S257 — Freetz-NG `tools/make/squashfs4-host-le/patches` at the same commit (a git symlink, target `../squashfs4-host-be/patches`) — 28 B, sha256 `6008eb3fb4b859f6ea530c0d442aaaa1c7c9f76975377d9a2d2cef1873b10479` — re-read 2026-10-30
source: S258 — `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/lead2-avm-le-genuine.tsv` (campaign-local, 940 B, sha256 `523637c885bb50c6d445bb096f247b9a66ab33633cae46af18be4a3d4c1b9ffa`) — read 2026-10-30
source: S259 — `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/lead2-stale-build.tsv` (campaign-local, 964 B, sha256 `4c962bacd24af8132f31ce78c8e8ddf03d501f221f3590ef6bd69beafb339951`) — read 2026-10-30
source: S243 — Freetz patch 101, the `AVM_LE`/`AVM_BE` symbols (lane row; the staged package's S206) — already registered
source: S245 — unblob SquashFS v4 little-endian handler at tag 26.6.4 (lane row) — already registered
verified-at: 2026-10-30
recheck: 180d — `grep -c 'the value of the mkfs_time superblock field is equal to the bytes_used field' <(curl -fsSL 'https://raw.githubusercontent.com/Freetz-NG/freetz-ng/86c23d96d76585825fa81b5cb29105e9d2ad6654/docs/make/README.md')` -> 1 (ran 2026-10-30; all seven recheck runs below were executed on 2026-10-30 — the registry rows carry the bare cadence `180d` in their `recheck` cell, because the census validator rejects prose there with E09)
ground: the round-52 LE-AVM class definition — the round-50 entry's limit 1, "No registered `corpus/SOURCES.md` row cited by this entry describes an LE AVM layout"

**Status.** Assimilated in round 52 from the shokuknow `corpus-expansion-1` package
(`merge/kaidoku/knowledge/corpus/knowledge/avm-le-image-genuine-marker.md`, staged 2026-10-24) and
re-grounded by the lane: five upstream documents re-opened on 2026-10-30 at a pinned commit, staged
ids renumbered by document (staged S220 -> S253, staged S214 -> S254; staged S206 is the lane's
already-registered S243). Six corrections were applied before admission (see `## Gate`); the staged
entry's own evidence rows are campaign-local and are registered as own-work rows (S258/S259) with
their digests, following the lane's own precedent S126.

## What upstream says the format is

[observation] Upstream describes AVM-LE as a **variant of the ordinary little-endian SquashFS**:
"The only difference of this format to the original LE format is that the value of the mkfs_time
superblock field is equal to the bytes_used field" (S253, `docs/make/README.md` lines 573-574). The
package entry is `squashfs4-le: squashfs-tools 4.3 (AVM-LE)`.

[observation] The **writer side** of that definition is upstream's own code: under
`#if (TARGET_FORMAT == AVM_BE || TARGET_FORMAT == AVM_LE)` the writer assigns
`sBlk->mkfs_time = (int) sBlk->bytes_used;` (S255, `mksquashfs.c` hunk), and the reader refuses to
read the field as a time, printing `is not available because of modified AVM-format (mkfs_time ==
bytes_used)` (S255, `unsquashfs.c` hunk). So `mkfs_time == bytes_used` is upstream's **definition**
of the marker for both AVM formats, not a lane inference from four carriers.

[observation] The **reader side** of the same package is upstream's own diagnostic, and the campaign
measurement of a built AVM-LE body saw exactly that string (S258, row
`upstream_unsquashfs_stat`).

[observation] The upstream AVM-LE toolchain is a **separate host package** from the AVM-BE one:
`squashfs4-host-le` builds `mksquashfs`/`unsquashfs` from squashfs-tools 4.3 (source md5
`d92ab59aabf5173f2a59089531e30dbf`) with `EXTRA_CFLAGS="-fcommon -DTARGET_FORMAT=AVM_LE
-DAVM_FORMAT_AS_OPTION"`, and installs them as `mksquashfs4-avm-le` / `unsquashfs4-avm-le` (S256).

[observation] The AVM-LE recipe reaches the marker patches through a **git symlink**:
`tools/make/squashfs4-host-le/patches` -> `../squashfs4-host-be/patches` (S257). The marker patches
therefore live in the AVM-BE recipe's directory and are shared by both toolchains; a citation of
S254 for an AVM-LE build that omits S257 is mis-grounded. The big-endian **layout** patches are
guarded separately (`250-mksquashfs__AVM_BE.patch` is `#if TARGET_FORMAT == AVM_BE`, S260), which is
why AVM-LE is a little-endian body with one changed field — the same split the round-41 entry states
for the BE side.

## The marker is a writer switch, not a format flag

[observation] With `AVM_FORMAT_AS_OPTION` defined, upstream makes the marker **optional**: the patch
adds `int use_standard_mkfs_time = TRUE;`, guards the assignment with `if (!use_standard_mkfs_time)`,
adds the option `-no-mkfs-time` (which sets the flag to `FALSE`) and the help line
`-no-mkfs-time\t\tuse AVM format (length instead of timestamp)` (S254). The measured campaign build
matches: its writer invocation is `-comp xz -no-mkfs-time -all-root -no-progress -no-exports
-no-sparse -b 65536` and the resulting body carries `mkfs_time` 361 == `bytes_used` 361 (S258).

[inference] The same toolchain built **without** `-no-mkfs-time` keeps the standard timestamp and
produces a body that is *not* AVM-LE, although the binary is the AVM-LE binary (S259, row
`clean_rebuild_avm_format_as_option_without_flag`: `mkfs_time` 1 792 871 460 against `bytes_used`
361). A present marker is therefore a statement about **how the body was written**, not about the
format of the tool.

## What this does not change about the carriers (held ground, cited not restated)

[observation, held] unblob 26.6.4 reads the marker **only inside its big-endian v4 branch**; every
little-endian v4 body takes `squashfs_v4_le` and the argv `sasquatch -le -no-exit-code -f -d …`,
marker or not (S245; `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`, section "The marker
is a constant of the pinned bytes, not a proof of origin"). The campaign measurement agrees: the
handler was `squashfs_v4_le`, the argv `sasquatch -le -no-exit-code -f -d {outdir} {inpath}`, and
the big-endian reader refused the same body outright with "FATAL ERROR: Block size too small. File
system is corrupt." (S258).

[observation, held] The marker is **re-stampable** and is not a proof of origin: the round-50
experiment patched `mkfs_time = bytes_used` onto stock LE bodies and REA produced identical
projections (the round-50 entry, same section).

[inference] The class "LE AVM members (`hsqs`)" is consequently defined by **one superblock
comparison** — `mkfs_time == bytes_used` — and every other property of those members (byte order,
compression, path layout) is stock little-endian SquashFS v4. The round-52 Core promotion is a
statement about the accounting of such bodies, not about a new format.

[observation] Upstream names the device class with examples only: "AVM-LE is the format used by AVM
to pack the filesystem of some cable boxes, e.g. 6490, 6590 (x86 core only)" (S253). The round-50
census found the marker on 28 LE members across **16 models**, and two of the four round-52 carriers
(7581, 7582) are **not** cable boxes. The upstream sentence is therefore evidence for the **format
definition**; the membership of the carrier class is the lane's own measurement and must not be
read off the upstream examples.

## A build lesson this round must not repeat

[observation] A changed `-D` define is **not** a make dependency. The campaign build that changed the
format define re-ran `make` in an already-built tree, was told `'mksquashfs' is up to date.
'unsquashfs' is up to date.`, and produced a **byte-identical binary**
(sha256 `1a7cfcf719459961ba1608185557e9c5` before and after) — the earlier AVM_LE measurement was
therefore taken with the stale binary of an inert define (S259, rows
`binary_sha256_before_no_clean_rebuild`, `make_output_on_changed_define`,
`binary_sha256_after_no_clean_rebuild`). A clean rebuild with the same plain recipe and
`-DTARGET_FORMAT=AVM_LE` set the marker (digest `3e72f247b4cee484bf1e9b25612758e3`).

[inference] The transferable rule for the lane: **before reading an instrument's output, assert that
the instrument's own bytes changed**. A frozen claim that re-uses a rebuilt counter, a rebuilt
extractor or a rebuilt fixture must bind the tool's digest, not trust a build's exit status.

## `## Gate` — the re-grounding record

- **c1 — the commit is pinned.** The staged row S220 cited `…/freetz-ng/master/docs/make/README.md`
  (a floating ref, the ground of several earlier refusals). The adopted row cites commit
  `86c23d96d76585825fa81b5cb29105e9d2ad6654` with sha256 `11477511…`; the paragraph moves from
  "line 674" (master) to **lines 573-574** (pinned).
- **c2 — the patch's location is stated.** The staged text reads as if `613-avm_format_as_option.patch`
  were an LE-toolchain file. It is in the AVM-BE recipe's patch directory and reaches the LE build
  only through the symlink of S257.
- **c3 — "the marker is invisible to unblob" is scoped, not asserted.** The staged entry's `:30`
  claim is replaced by the scoped, held statement in "What this does not change about the carriers"
  (source: S245; held in the round-50 entry).
- **c4 — the staged entry's `:55-56` caveats are replaced.** "Does not say unblob *recognises* the
  AVM marker" is now a source-scoped statement; "says nothing about a real Fritz!Box firmware
  image" is superseded by the round-50/51 measurements on four chain-pinned vendor members.
- **c5 — the device list is examples, not the class.** See the last paragraph above.
- **c6 — the campaign-local evidence is scoped as own-work.** S258/S259 point at files under the
  shokuknow campaign tree, which the lane does not retain; they carry the two measurements only, and
  the published claims rest on S253–S257.

**Recheck commands run on 2026-10-30** (each returned the stated count; receipts with exit codes,
digests and UTC times in the seat's `receipts/gate-receipts.txt`):

```
grep -c 'the value of the mkfs_time superblock field is equal to the bytes_used field' <(curl -fsSL 'https://raw.githubusercontent.com/Freetz-NG/freetz-ng/86c23d96d76585825fa81b5cb29105e9d2ad6654/docs/make/README.md')   # -> 1
grep -c 'use AVM format (length instead' <(curl -fsSL 'https://raw.githubusercontent.com/Freetz-NG/freetz-ng/86c23d96d76585825fa81b5cb29105e9d2ad6654/tools/make/squashfs4-host-be/patches/613-avm_format_as_option.patch')   # -> 1
grep -c 'modified AVM-format (mkfs_time == bytes_used)' <(curl -fsSL 'https://raw.githubusercontent.com/Freetz-NG/freetz-ng/86c23d96d76585825fa81b5cb29105e9d2ad6654/tools/make/squashfs4-host-be/patches/550-mkfs_time__AVM_BE_AVM_LE.patch')   # -> 1
grep -c 'DTARGET_FORMAT=AVM_LE -DAVM_FORMAT_AS_OPTION' <(curl -fsSL 'https://raw.githubusercontent.com/Freetz-NG/freetz-ng/86c23d96d76585825fa81b5cb29105e9d2ad6654/tools/make/squashfs4-host-le/squashfs4-host-le.mk')   # -> 1
grep -c 'TARGET_FORMAT == AVM_BE' <(curl -fsSL 'https://raw.githubusercontent.com/Freetz-NG/freetz-ng/86c23d96d76585825fa81b5cb29105e9d2ad6654/tools/make/squashfs4-host-be/patches/250-mksquashfs__AVM_BE.patch')   # -> 2
grep -c 'squashfs4-host-be/patches' <(curl -fsSL 'https://raw.githubusercontent.com/Freetz-NG/freetz-ng/86c23d96d76585825fa81b5cb29105e9d2ad6654/tools/make/squashfs4-host-le/patches')   # -> 1
grep -c -F 'modified AVM-format' /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/lead2-avm-le-genuine.tsv   # -> 1
grep -c -F 'up to date'         /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/lead2-stale-build.tsv   # -> 1
```

## Limits

1. This entry claims a **format definition and a writer mechanism**; it claims no extraction
   outcome, no vendor byte and no REA run. The four chain-pinned vendor members and their accounting
   are the round-50/51 entries' business.
2. It says nothing about the **device-accounting law** (the char-device / FIFO / socket boundaries of
   S250 and S251 and the round's man7 `mknod(2)` row): those are separate rows and separate claims.
3. It does not generalise the class: a stock little-endian body without the marker is **not**
   AVM-LE, and the round's Core row must be phrased over the marker-bearing bodies only.
4. The two own-work rows are campaign-local files the lane does not retain; their digests are
   recorded so a reader can confirm the bytes, but they are not lane evidence (QUALITY #1) and the
   entry's claims do not rest on them.
5. One upstream toolchain, one commit, one host: Freetz-NG at `86c23d9`. A different revision of the
   AVM toolchain may set the marker unconditionally again, which is what the plain (non-option)
   recipe does — the flag and the define are the things to re-check on any upgrade.
