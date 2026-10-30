# SOURCES append rows — round 51, wave 1 (seat ScribeSources)

Draft for the L1 to land into `corpus/SOURCES.md`. **Not applied to the lane tree.**

Two rows: **S250** (the device-node creation path that grounds the CENSUS side of the
round-51 device-accounting law) and **S251** (the producer-side padding option that
grounds the C2 no-pad discriminator). Both are `kind code`, `tier A` — source code is
CORPUS.md's own tier-A category ("primary or authoritative for that scope … source code"),
and both rows are upstream source at a named tag.

The id band: the registry ends at **S249** (156 rows); `S250`/`S251` are free. `S150`-`S242`
stay skipped (earlier lessons cite them as refused staged rows).

## The two rows

```markdown
| S250 | squashfs-tools 4.7.5 `unsquashfs.c` device-node creation path -- https://raw.githubusercontent.com/plougher/squashfs-tools/4.7.5/squashfs-tools/unsquashfs.c | code | A | the upstream extractor's char/block device-node creation path and its privilege refusal: the node is created only under `root_process`, and an unprivileged run reports "not superuser" instead of creating it, while fifo and socket nodes are attempted unconditionally and only report ERROR on failure; not REA's gap schema, not the sasquatch fork's tree, not any carrier's census | tag `4.7.5` = commit `708c59ae80853b0845017c33b42e56061cc546cd`; sha256 `6222d940c45537d597e2b36d1d46abbc90f0863e7106bab8fa7bdd97fd939341` (116,844 B); `:1296` the `mknod` call; `:1313`-`:1315` the "not superuser" refusal; `:1328`/`:1349` the fifo and socket `mknod` calls; `:4459` `root_process = geteuid() == 0;`; `unsquashfs_error.h` sha256 `6433564edbd528d12d4db9ae20a45594fdc8065884c3dcf7774858e30e44bc4a` `:44`-`:50` `EXIT_UNSQUASH_STRICT` degrades to a non-fatal `ERROR` unless `-strict-errors`; the sasquatch fork that actually ran has the same structure at `:1247`/`:1256`/`:1273`-`:1275`/`:1288`/`:1306` (sha256 `ece42b66f37ba67707c2c51b47b643c027232153705f59d238da79958a54cb40`) | A device node in a SquashFS image is absent from an unprivileged extraction by construction, not by reader failure: the extractor creates it only as root and refuses by name otherwise, so a char-device oracle entry is expected to carry no published counterpart. | queued | 2026-10-30 | on-release | corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md |
| S251 | squashfs-tools `mksquashfs.c` and `mksquashfs_help.c` padding option -- https://raw.githubusercontent.com/plougher/squashfs-tools/4.7.5/squashfs-tools/mksquashfs.c | code | A | the producer-side option that suppresses 4K padding of the produced filesystem, its upstream spelling and the padding logic it gates; the upstream spelling is `-nopad` with no hyphen at every upstream tag checked, and the option belongs to the writer, not to the reader; not any carrier's bytes, not a reader's behaviour, not REA's publication | tag `4.7.5` = commit `708c59ae80853b0845017c33b42e56061cc546cd`; `mksquashfs.c` sha256 `509241bb1aaa1a4fd144d3c7ddc96e628a9d34033573b04836672352fb4f17e2` (257,215 B) `:7113` the `-nopad` parse, `:596`/`:7491`/`:8946` the padding write it gates, `:5964` the superblock offset it chooses; `mksquashfs_help.c` sha256 `9136f6e6ac57859cb45df633128f68e615b412dc8b6abfa4da8374373f981ac2` `:467` the help line; the v3-era producer at tag `3.1` carries the same option name and help text (`mksquashfs.c` `:1914`, `:1973`, `:2248`) | A SquashFS body named "no-pad" is the producer's `-nopad` option: the filesystem is left at its unaligned length instead of being padded to a 4K multiple, and in streaming mode the superblock is placed at the unaligned write position rather than the next 4K boundary. | queued | 2026-10-30 | on-release | corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md, SKILL.md |
```

Eleven columns per row; no `|` inside any cell; longest cell 689 chars (S250 anchor) and 521
(S251 anchor) — the registry's own longest cell is 1200, so both are inside the lane's practice.
`status` is `queued` and `opened` is `2026-10-30` — the counter v2's `OPENED_DATES` is
`('2026-10-30',)` (`tools/round-51/w1/ExecCounterV2/c1-counter.py:393`), so both rows are
eligible for the `sourced` binding the moment they land.

### `used-by` routing

- **S250** -> `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md` (the C1 entry; this is the row the counter v2's `sourced` binding
  needs, since `ENTRY`/`STEM` must appear in the `used-by` cell — `c1-counter.py:2469`).
- **S251** -> `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md, SKILL.md` (the C1 entry **and** R51-C2's `SKILL.md` rule block 27).

S251 is cited by both consumers on purpose. The C1 entry's own draft says the padding row is
"included here only if the L1 lands it as a shared round-51 row whose `used-by` cell names
this entry as well as R51-C2's rule block" (`.ufo/waves/round-51/w1/ScribeEntryC1/entry.md:10`).
This row does name both, so the entry's placeholder can be filled either way. `SKILL.md` already
exists in the lane, so that half of the `used-by` resolves on disk today.

## `## Gate` quote records

For the round-51 lesson's `## Gate` (the L1 integrates these into `corpus/lessons/round-51.md`):

| row | source | accessed | located quote (<=25 words) | decision |
|---|---|---|---|---|
| S250 | https://raw.githubusercontent.com/plougher/squashfs-tools/4.7.5/squashfs-tools/unsquashfs.c (116,844 B, sha256 `6222d940c45537d597e2b36d1d46abbc90f0863e7106bab8fa7bdd97fd939341`) and https://raw.githubusercontent.com/plougher/squashfs-tools/4.7.5/squashfs-tools/unsquashfs_error.h (1,400 B, sha256 `6433564edbd528d12d4db9ae20a45594fdc8065884c3dcf7774858e30e44bc4a`) | 2026-10-30, HTTP 200, 04:58:12Z; re-fetched at master HEAD `db038ef265ed00bb17aaf695a72f9b0c3489eb20` (143,650 B, sha256 `bd2a6abd8bf6462282b5835067b79c94365a4414ad853401987ed30f4092b24f`) 04:58:13Z | `:1296` `res = mknod(pathname, chrdev ? S_IFCHR :` (7 words); `:1313`-`:1315` the assembled refusal `create_inode: could not create %s device %s, because you're not superuser!` (11 words, **composite** — three adjacent C string literals) | **admit** (tier A, `queued`): upstream `unsquashfs.c` creates a char/block device node only inside `if(root_process)` (`:1287` upstream, `:4459` sets `root_process = geteuid() == 0;`); the unprivileged branch (`:1312`-`:1316`) refuses by name and `goto failed`, which marks the inode created-but-missing (`:1373`-`:1386`). `EXIT_UNSQUASH_STRICT` (`unsquashfs_error.h:44`-`:50`) degrades to a non-fatal `ERROR` unless `-strict-errors` is passed, and `ERROR` prints without exiting while `BAD_ERROR` calls `exit(1)` (`error.h:42`-`:61`) — so the refusal is **silent** by default, and with `-no-exit-code` (`:3934`-`:3936`, which the caller's argv passes) the exit code stays 0 (`:3463`). The fifo (`:1328`) and socket (`:1349`) branches are **not** root-gated and fail with plain `ERROR`, so the two are not one mechanism. The sasquatch fork the lane actually ran has the same structure at `:1247`/`:1256`/`:1273`-`:1275`/`:1288`/`:1306` (lane copy sha256 `ece42b66f37ba67707c2c51b47b643c027232153705f59d238da79958a54cb40`). |
| S251 | https://raw.githubusercontent.com/plougher/squashfs-tools/4.7.5/squashfs-tools/mksquashfs.c (257,215 B, sha256 `509241bb1aaa1a4fd144d3c7ddc96e628a9d34033573b04836672352fb4f17e2`) and https://raw.githubusercontent.com/plougher/squashfs-tools/4.7.5/squashfs-tools/mksquashfs_help.c (56,423 B, sha256 `9136f6e6ac57859cb45df633128f68e615b412dc8b6abfa4da8374373f981ac2`) | 2026-10-30, HTTP 200, 05:03:18Z | `mksquashfs_help.c` `:467` `"-nopad\t\t\tdo not pad filesystem to a multiple of 4K\n",` (9 words); `mksquashfs.c` `:7113` `} else if(strcmp(argv[i], "-nopad") == 0)` (6 words) | **admit** (tier A, `queued`): the upstream spelling is **`-nopad`**, with no hyphen — `grep -c -- 'no-pad'` is **0** in every upstream body opened today (tags `3.1`, `4.4`, `4.5.1`, `4.6.1`, `4.7`, `4.7.4`, `4.7.5`, master, master-HEAD-pin, and the sasquatch fork). The lane's `SKILL.md` "no-pad" is the lane's own prose, not an upstream option name. The option gates three padding writes (`:596`, `:7491`, `:8946`) and the superblock offset (`:5964`). |

Both quotes were located mechanically: `python3 -I -B quote-check.py` -> `QUOTE_CHECK located=33
missing=0` (exit 0), including a negative control that must be absent (a deliberately wrong
`mknod` spelling at `unsquashfs-4.7.5.c:1296`).

## `## Search log` entry

Append as the last bullet of the `## Search log` section in `corpus/SOURCES.md` (before
`## Leads (unopened)`):

```markdown
- 2026-10-30 round 51 wave 1 (C1/C2 source opens) — Question: what upstream squashfs-tools source grounds the round-51 device-accounting law and the `-no-pad` padding claim? Where searched: the two named master raw files (`unsquashfs.c`, `mksquashfs.c`) re-fetched today, the same two files at the tagged release matching the host oracle (`4.7.5`), the same files at the current master HEAD commit, the companion `mksquashfs_help.c`/`mksquashfs_help.h`/`squashfs_fs.h`/`unsquashfs_error.h` at both refs, the upstream tags `3.1`/`4.4`/`4.5.1`/`4.6.1`/`4.7`/`4.7.4` `mksquashfs.c`, the sasquatch fork `mksquashfs.c` at tag `sasquatch-v4.5.1-6`, and `git ls-remote --tags` for the upstream tag list; every body was digested and every located quote re-checked against the served bytes (receipts under `.ufo/waves/round-51/w1/ScribeSources/`). Identified 2, screened 2, included 2 (S250, S251), excluded 0; the upstream spelling of the padding option is `-nopad` with no hyphen, so the lane's "no-pad" prose is not an upstream option name. Stop: both rows are located and anchored at a named upstream tag; no further source family was opened.
```

## Landing constraints the L1 must honour

1. **The entry file and these two rows must land in the same commit.** The census resolves every
   `mined` row's `used-by` path on disk (`scripts/sources-census.sh` `usedby_findings`, lines
   531-570). Measured on the scratch mirror: with the entry present, the `mined` variant of the
   block validates at **exit 0** (`receipts/census-mined-variant.txt`); with the entry removed,
   the same file exits **1** with exactly two `E11` lines — one per new row, both naming
   `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md`. Nothing else is red. The entry does
   not exist at the base revision, so a rows-only landing makes the registry red.

2. **With `status queued` the block is already clean at exit 0** — measured: `census exit=0`,
   `E=0`, `W04=19` (the baseline's 19, unchanged), `diff vs base: added=3 removed=0` (two rows
   plus one search-log bullet; no existing row is edited). The `queued` -> `mined` flip is the
   L1's landing step, and it is when the `E11` rule starts to bite.

3. **The C1 entry's two `source:` placeholders are filled by these two rows.**
   `.ufo/waves/round-51/w1/ScribeEntryC1/entry.md:9` is the unsquashfs device-node placeholder
   (S250) and `:10` is the `mksquashfs` `-no-pad`/padding placeholder (S251). Both placeholders
   say the row id, URL, access date, located quote and sha256 are "to be filled by the L1 at the
   freeze" — this draft supplies all five for each row. Until the entry's `source:` lines name
   the row ids, the counter v2's `sourced` binding (`c1-counter.py:2469-2472`) stays red for a
   reason no registry row can fix.

4. **`W04` is unchanged at 19** — the baseline lane registry already emits 19 `W04` lines
   (`scripts/sources-census.sh validate kaidoku-shokunin` -> exit 0, 19 findings, all `W04`).
   Neither new URL appears elsewhere in the registry (`grep -c 'raw.githubusercontent.com/plougher'
   corpus/SOURCES.md` -> 0), so the block adds no new `W04` and no `E04`.

5. **No `|` inside any cell** and eleven columns per row, asserted by `build-rows.py` before
   the census runs (it exits non-zero on any grammar violation).

## What these rows do NOT establish

- **S250 does not establish that REA emits no gap record for a device row.** It establishes the
  **producer-side** mechanism: the extractor creates the node only as root and refuses by name
  otherwise, so the node is absent from an unprivileged extraction tree. Whether REA/unblob
  emits a gap record for it is a property of REA's envelope schema (S119's territory), and the
  round-50 receipts are the measurement. The round-50 `unpublished_entries` on all four carriers
  contain **only** `symlink` entries — 636 / 636 / 567 / 612 for g7581 / g7582 / c6430 / c6490,
  with **zero** char-device entries — so the device rows are indeed absent with no disposition.
- **S250 does not cover the sasquatch fork's own tree** (S121's scope) and does not cover the
  REA gap schema (S119). It is upstream squashfs-tools source, cited as the canonical
  implementation the fork inherits the structure of.
- **S251 does not establish that the ddwrt bodies were produced with `-nopad`.** The lane's
  `squashfs_v3.be.nopad.bin` fixture (320 B, `corpus/evidence/round-42` `v3ddwrt-be`) is a
  **v3** image; upstream `mksquashfs` at tag `4.7.5` writes SquashFS v4.0
  (`squashfs_fs.h:28-29` `SQUASHFS_MAJOR 4` / `SQUASHFS_MINOR 0`), so the v3-era producer at
  tag `3.1` (`squashfs_fs.h:27-28` `SQUASHFS_MAJOR 3`) is the one that could have written it —
  and it carries the same `-nopad` name and help text (`mksquashfs.c:1914`, `:1973`, `:2248`).
  The row is scoped to the option's spelling and the padding logic it gates, not to the
  provenance of any particular body.
- **Nothing here says a fifo or a socket is omitted.** The upstream fifo and socket branches are
  *not* root-gated; they attempt `mknod` unconditionally and only report `ERROR` on failure. The
  round-50 oracle tables carry no fifo and no socket at all (kinds present: `char-device`, `dir`,
  `symlink` only), so the carriers do not exercise those branches.

## Artifact paths

| file | what it is |
|---|---|
| `.ufo/waves/round-51/w1/ScribeSources/rows.md` | this file (the draft) |
| `.ufo/waves/round-51/w1/ScribeSources/fetch-sources.sh` | the master-URL fetch driver (exact URL -> UTC -> HTTP status -> bytes -> sha256 -> curl exit) |
| `.ufo/waves/round-51/w1/ScribeSources/fetch-tags.sh` | the tag-pinned / HEAD-pin fetch driver |
| `.ufo/waves/round-51/w1/ScribeSources/quote-check.py` + `quote-check.out.txt` | the anchor locator (`QUOTE_CHECK located=33 missing=0`, exit 0) |
| `.ufo/waves/round-51/w1/ScribeSources/build-rows.py` + `build.log` | the row builder: grammar assertions, the scratch mirror, the census proof |
| `.ufo/waves/round-51/w1/ScribeSources/receipts/receipts.tsv` | the two named master-URL fetches (HTTP 200, bytes, sha256, UTC, curl exit) |
| `.ufo/waves/round-51/w1/ScribeSources/receipts/receipts-tags.tsv` | the tag/HEAD-pin/companion-file fetches (20 rows) |
| `.ufo/waves/round-51/w1/ScribeSources/receipts/receipts-sasquatch.tsv` | the sasquatch-fork fetches (2 rows) |
| `.ufo/waves/round-51/w1/ScribeSources/receipts/census-mirror.txt` | the census output on the mirror and on the untouched lane registry |
| `.ufo/waves/round-51/w1/ScribeSources/receipts/census-mined-variant.txt` | the `mined`-status variant, with and without the entry placeholder |
| `.ufo/waves/round-51/w1/ScribeSources/mirror/corpus/SOURCES.md` | the whole patched registry (base + the two rows + the search-log bullet) |

Every receipt carries the exact URL, the UTC time, the HTTP status, the byte count, the sha256 and
the curl exit code. No `Set-Cookie`/`Cookie`/`Authorization` header was saved: the fetch driver
keeps only `content-type`, `content-length`, `last-modified` and `etag` from the response
headers, and the raw header files are deleted immediately.
