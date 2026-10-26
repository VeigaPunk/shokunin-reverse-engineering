# SquashFS v3 through REA: the `squashfs_v3` handler family runs plain `sasquatch` with `-le`/`-be`, never `sasquatch-v4be` (round 42, Core)

status: R42-C1 `<<L1:c1-status-line>>` — `met` at `<<L1:measured-revision>>` with `carriers_matched = <<L1:carriers-matched>>` of 4 and every binding true (`tools/round-42/c1-counter.py`, exit `<<L1:counter-exit>>`, `<<L1:score-artifact>>`), or the honest stop that replaces this line and the PROVINCE row

source: S112 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — lines 24-69 (`SquashFSExtractor`: `EXECUTABLE = "sasquatch"` :25, `V4BE_EXECUTABLE = "sasquatch-v4be"` :26, the `match endian, self.version` argv decision :39-54, the 4-token argv tail :56-64, and `get_dependencies` returning both binaries :68-69); lines 72-99 (`_SquashFSBase`: `BIG_ENDIAN_MAGIC = 0x73_71_73_68` :73, `EXTRACTOR = SquashFSExtractor(3, 0x73_71_73_68)` :75, `calculate_chunk` :77-99); lines 244-264 (`squashfs_v3`, both magics), 284-315 (the `squashfs3_super_block` C definition — no `compression` member), 318-361 (`squashfs_v3_ddwrt`, `tqsh`), 363-407 (`squashfs_v3_broadcom`, `qshs`), 409-452 (`squashfs_v3_nonstandard`, `sqlz`); v4's `compression` member at :476 for the contrast — as read 2026-10-26 from the installed unblob 26.6.4 tree (19 842 B, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`, equal to the installed copy and to the hash round 41 recorded)
source: S116 — https://unblob.org/formats/ — the producer's ten SquashFS sections (`v1`, `v2`, `v2-non-standard`, `v3`, `v3-Broadcom`, `v3-DDWRT`, `v3-non-standard`, `v4-BE`, `v4-broadcom`, `v4-LE`); the row's scope is the site's coverage statement, not an outcome
source: S121 — https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/squashfs-tools/unsquashfs.c — `read_block` swaps the block-length header only when `swap` is set (lines 664-669) and `-be` sets `swap` (lines 4389-4400); the `squashfs-v4be` build is the same tree with `-DFIX_BE` (round-40 citation, bytes unchanged; not re-read this seat)
source: S119 — rea-agents 6.5.0 package — the gap vocabulary this entry's rule reads: dependency gaps, `extractor-failure`, `depth-limited`, `unpublished-entry` in `dist/firmware/FirmwarePublication.js` (line anchors as the S119 registry row records them; not re-read this seat)
source: S118 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/extractor.py — `is_recursive_link` and `fix_symlink`: an escaping link is removed and reported, an in-tree link extracts and leaves the publication gap (anchors as the S118 registry row records them; not re-read this seat)
source: S130 (id as appended) — `<<L1:carrier-1-publisher-url>>` — `<<L1:carrier-1-publisher>>`'s own published identity of carrier 1: product, version, file name, advertised size; never the SquashFS layout of the image, never redistribution permission
source: S131 (id as appended) — `<<L1:carrier-2-publisher-url>>` — `<<L1:carrier-2-publisher>>` (same scope as S130, different document)
source: S132 (id as appended) — `<<L1:carrier-3-publisher-url>>` — `<<L1:carrier-3-publisher>>` (same scope as S130, different document)
source: S133 (id as appended) — `<<L1:carrier-4-publisher-url>>` — `<<L1:carrier-4-publisher>>` (same scope as S130, different document) (drop and renumber when two carriers share a publisher: one row per publisher, `<<L1:sources-rows-final>>`)
source: S134 — own-work, committed in the freeze — the v3 oracle premise on unblob 26.6.4's own v3 fixtures: `unsquashfs` 4.7.5 and 7-Zip 26.04 read little- and big-endian v3 to identical digests, and `unsquashfs` 4.7.5 refuses an LZMA-block v3 body (`gzip uncompress failed with error code -3`, exit 1) — text and digests at `.ufo/waves/round-42/w1/artifacts/R42C1EntryDraft/dev-evidence/dev-input-evidence.txt`
verified-at: 2026-10-26
recheck: 180d — `python3 -I -B tools/round-42/c1-counter.py --root . --rev <<L1:measured-revision>> --freeze <<L1:freeze-commit>> --pkg65 <rea-agents 6.5.0 root> --carrier-cache <DIR>` -> exit 0 with `carriers_matched 4`; the carrier pins are re-hashed from the publisher's URL by `tools/round-42/fetch-carrier.py`, and a re-fetch that lands different bytes means the entry is re-read

**What the family is, from the handler source.** unblob 26.6.4 carries four handler names whose
name starts `squashfs_v3`: `squashfs_v3` itself (S112 :244-264) and three vendor/format variants —
`squashfs_v3_ddwrt` (`tqsh`, S112 :318-323), `squashfs_v3_broadcom` (`qshs`, :363-368) and
`squashfs_v3_nonstandard` (`sqlz`, :409-414). Each declares two byte patterns over the same 28-byte
gap: the big-endian magic then `[24]` then `00 03`, and the little-endian magic then `[24]` then
`03 00`. The four magics are `sqsh`/`hsqs`, `tqsh`/`hsqt`, `qshs`/`shsq`, `sqlz`/`zlqs`. All four
inherit `_SquashFSBase.calculate_chunk` (:77-99), so the chunk end is `start + bytes_used` unless the
bytes between `bytes_used` and `round_up(bytes_used, 4096)` (then `1024`) are all zero, in which case
the padded boundary is the end. The v3 superblock is `squashfs3_super_block` (:284-315): the 32-bit
legacy fields first, then `s_major`, `s_minor`, `block_size_1`, `block_log`, `flags`, the uid/gid
counts, `mkfs_time`, `root_inode`, `block_size`, `fragments`, and the 64-bit table offsets. There is
**no compression member** — v4's struct has one at :476 and v3's does not.

**The extractor, from source and from a run.** Every SquashFS handler in 26.6.4 shares one
`SquashFSExtractor` (S112 :24-69). Its binary is `sasquatch` (:25); `sasquatch-v4be` is a *declared
dependency* (:26, :68-69) and is selected only in the `Endian.BIG, 4` branch (:40-50). A version-3
handler therefore lands in `case Endian.BIG, _:` (:51-52, append `-be`) or `case Endian.LITTLE, _:`
(:53-54, append `-le`), and the 4-token tail is `-no-exit-code -f -d {outdir} {inpath}` (:56-64). The
AVM marker branch that decides `-be` for v4 (:44-50) has no v3 path. Measured on the producer's own
fixtures (development inputs, not carriers): `command='sasquatch -le -no-exit-code -f -d …'` on
`squashfs_v3_le.bin` and `command='sasquatch -be -no-exit-code -f -d …'` on `squashfs_v3_be.bin`,
both exit 0 with 2 files published
(`dev-evidence/dev-input-evidence.txt`). So the three things round 41 had to keep apart for v4 —
marker, block-length byte order, `-be` token — collapse here: for v3 the endianness of the *whole*
structure picks `-le`/`-be` on the *plain* binary. [INFERENCE] `squashfs_v1` and `squashfs_v2` inherit
the same base extractor object (`SquashFSExtractor(3, …)`, :75) because they override only `NAME` and
`PATTERNS`; `version` is read only in the `BIG, 4` branch, so the inherited `3` changes nothing for
them. `squashfs_v2_nonstandard` overrides it to version 2 (:204) for the same reason.

**A dependency gap can name a binary the chunk does not need.** `get_dependencies` (:68-69) returns
`[sasquatch, sasquatch-v4be]` for *every* SquashFS handler, so an environment without
`sasquatch-v4be` records a dependency gap on a pure-v3 chunk even though no v3 chunk ever executes it.
The receipt's `dependencies` cell is therefore a statement about the handler's declared requirements,
not about the argv a v3 run used; the argv claim in this entry rests on S112 :39-64 plus the unblob
log lines above, never on a receipt (REA records no extractor argv on success; the round-41 entry's
Limits section states it and nothing in this round contradicts it).

**Why the oracle pair is two readers that are not sasquatch.** The producer's own extractor for this
family is sasquatch, so an oracle built on sasquatch would confirm the extractor with itself. The C1
oracle is `unsquashfs` 4.7.5 (squashfs-tools)'s own reader and 7-Zip 26.04's SquashFS handler, and the
two must agree **on every regular file** of a carrier before it freezes. The agreement cannot extend to
the non-regular rows: 7-Zip's listing reports a mode but never a link target, and its extraction rewrites
an absolute link while writing an escaping relative link out as a zero-byte file, so the symlink rows come
from `unsquashfs` alone (measured by seat `R42C1Sentinel`, `.ufo/waves/round-42/w1/R42C1Sentinel.md` §B3). Measured premise on the fixtures: both
read v3 little- and big-endian and publish identical digests for both files
(`apple.txt` `303980bc…`, `cherry.txt` `86baf352…`), and 7-Zip prints `Big-endian = +` on the BE
fixture. The pair is *not* a universal v3 oracle: `unsquashfs` 4.7.5 reads v3 blocks as gzip, and on
the producer's LZMA-block v3 fixture it fails with `gzip uncompress failed with error code -3` and
exit 1 while 7-Zip extracts both files (same evidence file). A v3 body whose blocks are LZMA therefore
has one working oracle, not two, and cannot satisfy the agreement rule as written.

**Compression is not a feature the v3 superblock declares.** Because `squashfs3_super_block` has no
compression member (S112 :284-315) and `unsquashfs -s` names no algorithm on a v3 image, a v3 carrier
cannot be classified by a superblock compression id the way the round-41 v4 carriers were (`id 1`
gzip, `id 2`/`4` xz). The observable is behavioural: the oracle's gzip read succeeds or it does not.
That is a counter-port consequence, stated in `.ufo/waves/round-42/w1/R42C1EntryDraft.md` §5 and not a
property of the images.

**The exact-path rule (carried from round 41, not re-derived).** unblob extracts chunk `X` into
`X_extract`, and rea-agents 6.5.0 stages the input as `firmware.bin`, so the `$input` chunk's extract
root is `firmware.bin_extract`. A receipt path counts as publishing an oracle row only when it equals
the row's relative path resolved against that root; no suffix matching (`2026-10-26-r41-avm-be-squashfs-core`,
R40-CL1). This entry is scored by a port of that rule, unchanged.

**Measured: four frozen carriers no extractor had touched before the freeze.** Each carrier is a
published third-party image (a distribution or vendor rootfs), its bytes are fetched from the
publisher by a pinned chain and are not committed, and its superblock is read by the non-sasquatch
readers before any REA run. `kind` is `published` for all four (the round-41 lane-built carriers have
no counterpart here: this claim is about third-party bytes).

| carrier | what | superblock read by the oracle | oracle regular files | non-regular entries | published / gaps after the freeze run | chunk |
|---|---|---|---|---|---|---|
| C1 `<<L1:carrier-1-id>>` | `<<L1:carrier-1-product>>` — `<<L1:carrier-1-url>>`, member/carve `<<L1:carrier-1-member>>` to `<<L1:carrier-1-carve-bytes>>` B, image `<<L1:carrier-1-image-sha256>>`, carrier pin `<<L1:carrier-1-carrier-sha256>>` | handler `<<L1:carrier-1-handler>>`, magic `<<L1:carrier-1-magic>>`, version `<<L1:carrier-1-major-minor>>` | `<<L1:carrier-1-oracle-regular>>` | `<<L1:carrier-1-nonregular-split>>` | `<<L1:carrier-1-published>>` files published; `<<L1:carrier-1-gaps>>` | one `<<L1:carrier-1-handler>>` chunk, not failed |
| C2 `<<L1:carrier-2-id>>` | `<<L1:carrier-2-product>>` — `<<L1:carrier-2-url>>`, member/carve `<<L1:carrier-2-member>>` to `<<L1:carrier-2-carve-bytes>>` B, image `<<L1:carrier-2-image-sha256>>`, carrier pin `<<L1:carrier-2-carrier-sha256>>` | handler `<<L1:carrier-2-handler>>`, magic `<<L1:carrier-2-magic>>`, version `<<L1:carrier-2-major-minor>>` | `<<L1:carrier-2-oracle-regular>>` | `<<L1:carrier-2-nonregular-split>>` | `<<L1:carrier-2-published>>` files published; `<<L1:carrier-2-gaps>>` | one `<<L1:carrier-2-handler>>` chunk, not failed |
| C3 `<<L1:carrier-3-id>>` | `<<L1:carrier-3-product>>` — `<<L1:carrier-3-url>>`, member/carve `<<L1:carrier-3-member>>` to `<<L1:carrier-3-carve-bytes>>` B, image `<<L1:carrier-3-image-sha256>>`, carrier pin `<<L1:carrier-3-carrier-sha256>>` | handler `<<L1:carrier-3-handler>>`, magic `<<L1:carrier-3-magic>>`, version `<<L1:carrier-3-major-minor>>` | `<<L1:carrier-3-oracle-regular>>` | `<<L1:carrier-3-nonregular-split>>` | `<<L1:carrier-3-published>>` files published; `<<L1:carrier-3-gaps>>` | one `<<L1:carrier-3-handler>>` chunk, not failed |
| C4 `<<L1:carrier-4-id>>` | `<<L1:carrier-4-product>>` — `<<L1:carrier-4-url>>`, member/carve `<<L1:carrier-4-member>>` to `<<L1:carrier-4-carve-bytes>>` B, image `<<L1:carrier-4-image-sha256>>`, carrier pin `<<L1:carrier-4-carrier-sha256>>` | handler `<<L1:carrier-4-handler>>`, magic `<<L1:carrier-4-magic>>`, version `<<L1:carrier-4-major-minor>>` | `<<L1:carrier-4-oracle-regular>>` | `<<L1:carrier-4-nonregular-split>>` | `<<L1:carrier-4-published>>` files published; `<<L1:carrier-4-gaps>>` | one `<<L1:carrier-4-handler>>` chunk, not failed |

Counter: `tools/round-42/c1-counter.py --root . --rev <<L1:measured-revision>> --freeze <<L1:freeze-commit>>
--pkg65 <rea-agents 6.5.0 root> --carrier-cache <DIR>` -> `<<L1:score-artifact>>`; result in SCORECARD
`## Round 42`. The counter re-runs each carrier's bytes at scoring time and compares the
`plus-extractor` projection, so a receipt fabricated from the oracle cannot pass (R39-CL5), and it
replays the receipt's `max_depth`; a rerun it cannot perform is `rerun_env_error` (exit 2), never met.

**The gap rule (draft of the claim's wording, as scored).** Every regular file of the frozen oracle
must be published at its exact relative path with the same sha256 and size. Every non-regular oracle
row must be accounted for: one `unpublished-entry` gap per retained symlink, or one
`MaliciousSymlinkRemoved` diagnostic per symlink the sanitiser removed (S118 :50-92 — an escaping
target is removed and reported, an in-tree target extracts and leaves the publication gap); devices,
FIFOs, sockets and directories are answered by the gap rule and need no receipt path of their own. At
most one structural `depth-limited` row is allowed, and `unknown-chunk-handler` must be absent.

**Why `--max-depth 1`.** REA's stage budget is 10 000 entries; a vendor image that contains a
second SquashFS inside its rootfs would be descended into at the default depth and can exceed it,
which returns `unreadable_output` with no chunk list (round-40 §6, unchanged for v3). Depth 1 is the
deepest setting that yields a receipt for every carrier and records at most one `depth-limited` row.
Staged entries per carrier after the freeze run: C1 `<<L1:carrier-1-staged-entries>>`, C2
`<<L1:carrier-2-staged-entries>>`, C3 `<<L1:carrier-3-staged-entries>>`, C4
`<<L1:carrier-4-staged-entries>>`.

**What the lane held before this round.** Only two statements, both producer- or table-side, and
neither an extraction outcome: the format-matrix row `2026-10-26-unblob-format-matrix`, whose README
cell reads "coverage claim only, never an extraction outcome" and whose body says "A support matrix
claims coverage, never an outcome", and the triage table v3's cause text for a chunk whose only
SquashFS handler is v1-v3 (`2026-10-26-r41-sqfs-triage-v3.md:22-24`, restated at :108-110). No REA run
on a v3 chunk existed in the corpus. This entry adds the run; it does **not** relabel any envelope and
therefore does not supersede the v3 table's cause cell — the round-42 v4 table is R42-C2's surface
(`plans/round-42-claims.md` § R42-C2) and its supersession, if it lands, is recorded there. The
supersession this entry does make is the format-matrix status for the handlers measured here, by
dated pointer in `PROVINCE.md` and `corpus/README.md` (never by editing the old row); the exact
pointer text is `.ufo/waves/round-42/w1/artifacts/R42C1EntryDraft/supersession.md`.

**Limits.** v1 and v2 images are not claimed (the handler family and the fixtures exist; no carrier
was frozen). SquashFS v4 Broadcom (`squashfs_v4_broadcom`) is not claimed. Nothing is claimed about
the *programs* the published files contain: publishing a path with a matching digest is the end of
this claim. A carrier carrying the `squashfs_v3_nonstandard` or `squashfs_v3_broadcom` magic is
covered only if it is one of the four frozen (the handler matrix above is the source reading, not a
measurement per variant); the same holds for a big-endian v3 carrier, whose `-be` leg is measured here
only on the producer's BE fixture. An LZMA-block v3 body is outside the oracle pair (measured above:
one reader refuses); the extractor is not the constraint there — unblob's `squashfs_v3` handler extracts
the producer's LZMA fixture with the same `-le` argv and 2 files published, so the hole is in the oracle,
not in sasquatch. The metadata-padding probe truncates `start_offset + bytes_used` to 32 bits
(S112 :82), so a chunk whose absolute end exceeds 4 GiB is not probed this way — irrelevant for a
carrier carved at offset 0 under 4 GiB, which is every carrier here. Vendor images are not
committed and not redistributable; the digests plus `tools/round-42/fetch-carrier.py` are the
provenance, and the publishers' licence text governs what may be re-published.
