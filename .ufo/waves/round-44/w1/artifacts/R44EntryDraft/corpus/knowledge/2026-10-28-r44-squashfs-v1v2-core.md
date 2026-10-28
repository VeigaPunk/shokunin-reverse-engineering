# SquashFS v1 and v2 through REA: `squashfs_v1` and `squashfs_v2` run plain `sasquatch -be`/`-le`, and their four frozen fixtures extract to byte-identical member sets in both byte orders (round 44, Core)

status: R44-C1 — scored by `tools/round-44/c1-counter.py` against the round-44 freeze at the
landing revision; the counter's score receipt and the revision it measured are in
`.ufo/waves/round-44/l1/scores/` and SCORECARD `## Round 44`.

source: S138 — https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs — the unblob 26.6.4 `__output__` expected member trees for `squashfs_v1` and `squashfs_v2` in both byte orders (MIT; the round-44 listings were fetched through `https://api.github.com/repos/onekey-sec/unblob/contents/tests/integration/filesystem/squashfs/<v>/<endian>/__output__?ref=26.6.4` — 10 listings, HTTP 200, 2026-10-28T11:10:29Z–11:10:43Z — and 22 members, HTTP 200, 2026-10-28T11:12:37Z; manifest `corpus/evidence/round-44/oracle/manifest.json`, sha256 `4bc53dbba8beee0fbf912771efc0a55fd47a197cca1f56d2aaed790f817c1a13`, `failures: []`)
source: S139 — https://github.com/plougher/squashfs-tools/releases — the upstream release page that grounds the independent reader's identity, `/usr/bin/unsquashfs` (`unsquashfs version 4.7.5 (2026/03/01)`; Arch package `squashfs-tools 4.7.5-1`); page opened 2026-10-28, HTTP 200, `4.7.5` tag present
source: S112 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — `SquashFSExtractor` :24-69 (executables :25-26, `match endian, self.version` argv decision :39-54, tail :56-64, dependencies :69), `_SquashFSBase` :72-99 (`BIG_ENDIAN_MAGIC` :73, `EXTRACTOR = SquashFSExtractor(3, 0x73717368)` :75, chunk end :77-99), `SquashFSv1Handler` :101-155 (`NAME` :102, patterns :105-121, `C_DEFINITIONS` :123-136, `HEADER_STRUCT` :137), `SquashFSv2Handler` :158-196 (`NAME` :159, patterns :161-178), `SquashFSv2NonStandardHandler` :199-241 (`NAME` :200, `BIG_ENDIAN_MAGIC` :202, `EXTRACTOR` :204)
verified-at: (filled at landing)
recheck: 180d — re-run the oracle census recorded below (`unsquashfs -lls`, `unsquashfs -s`, extraction + member digests, the superblock read) at the measured revision; any carrier whose sha256 differs from the pins below, or any member digest that differs from the census table, means this entry is re-read. `unsquashfs -version` at that time must still identify the oracle.

**Observation discipline.** Everything in the tables below was read from committed bytes on
2026-10-28 (oracle census) or from the pinned handler source; the only unobserved item is the
after-side REA receipt, which the counter scores at the landing revision. Observation, inference
and unknown are separated at the end; a value named in a table is always an observation.

## What moved Frontier → Core

Before this round `PROVINCE.md` carried `SquashFS v1/v2` as still-Frontier (round-42 frontier
note, line 416: "Still Frontier: SquashFS v1/v2, …"). Round 44 adds a
`## Round-44 additions to Core` row naming `squashfs_v1` and `squashfs_v2`, and this entry is its
evidence: the two handler families, **in both byte orders**, through REA 6.5.0
`extract-firmware` (unblob 26.6.4, child PATH carrying sasquatch 4.5.1), on four frozen MIT
fixtures.

Scope of the promotion, in one sentence: it promotes the *handler family through REA on the four
frozen carriers*, not "every SquashFS v1/v2 image on the internet". Published v1/v2 rootfs
images were probed and were not fetchable (`archive.openwrt.org/whiterussian/rc6/openwrt-brcm-2.4-squashfs.trx`
404 on 2026-10-28; the DD-WRT beta listing was empty), so no published carrier enters this
round; the fixtures are the whole carrier set.

## The handler family, from the handler source

unblob 26.6.4 defines the two handlers as separate classes with the same extractor:
`SquashFSv1Handler` (S112 :101, `NAME = "squashfs_v1"` :102) is matched by
`73 71 73 68 [24] 00 01` (big endian) or `68 73 71 73 [24] 01 00` (little endian)
(:105-121): the magic `sqsh`/`hsqs`, 24 skipped bytes, then the two bytes of the 16-bit
`s_major` field, big-endian `00 01` or little-endian `01 00`, i.e. `s_major` = 1. The pattern
does not constrain `s_minor` (the next two bytes are not in the match string).
`SquashFSv2Handler` (S112 :158) inherits it and only overrides the patterns (:161-178), whose
`s_major` bytes are `00 02` / `02 00`, i.e. 2. Neither class overrides `EXTRACTOR`, so both use
`_SquashFSBase.EXTRACTOR = SquashFSExtractor(3, 0x73717368)` (:75).

That extractor's argv decision (:39-54) branches on `endian, self.version`; only the
`Endian.BIG, 4` case is special (it selects `sasquatch-v4be` and, for a standard body, appends
`-be`). For v1 and v2 the decision falls to `case Endian.BIG, _` → `-be` and
`case Endian.LITTLE, _` → `-le` (:48-54), followed by the fixed tail
`-no-exit-code -f -d {outdir} {inpath}` (:56-64). So the command a v1/v2 chunk runs is

```
sasquatch -be| -le -no-exit-code -f -d {outdir} {inpath}
```

i.e. the same binary and the same tail as the round-42 v3 lane, and **no new REA key**: the
handler name changes, the extractor does not. The endianness is the only argv difference between
the four carriers.

**Binding rule — per carrier, exact equality.** The after-side receipt for carrier *X* must name
*X*'s frozen handler, and the name must be equal as a whole string: `squashfs_v1` for V1BE/V1LE,
`squashfs_v2` for V2BE/V2LE. Prefix matching is inadmissible, and this is not pedantry:
`squashfs_v2` is a strict prefix of `squashfs_v2_nonstandard` (S112 :200), and `squashfs_v3` is a
strict prefix of `squashfs_v3_broadcom` (:363) and `squashfs_v3_nonstandard` (:409). A
prefix-keyed comparator would let a v2-nonstandard receipt satisfy a v2 carrier, or a broadcom
receipt satisfy a v3 carrier, without any byte being wrong. Exact equality also keeps a v1
receipt from satisfying a v2 carrier and vice versa, which is the whole point of promoting two
versions rather than one.

## The superblock, read from the bytes

`sb.py` (receipt run `superblock-fields`) reads the first 32 bytes as unblob's
`squashfs_super_block_t` (`char s_magic[4]`, six `uint32`, `uint16 s_major`, `uint16 s_minor`;
S112 :124-137) and the v1/v2 packed tail at offset 32 (`block_size_1:uint16`,
`block_log:uint16`, `flags:uint8`, `no_uids:uint8`, `no_guids:uint8`, `mkfs_time:uint32`) in the
carrier's own byte order.

| carrier | magic | s_major:s_minor | order | block_size_1 | block_log | flags | no_uids/no_guids | inodes | bytes_used | mkfs_time (UTC) |
|---|---|---|---|---|---|---|---|---|---|---|
| V1BE | `sqsh` | 1:0 | be | 32768 | 15 | `0x00` | 1 / 0 | 4 | 177 | 2024-08-05T04:18:58Z |
| V1LE | `hsqs` | 1:0 | le | 32768 | 15 | `0x00` | 1 / 0 | 4 | 176 | 2024-08-05T04:18:51Z |
| V2BE | `sqsh` | 2:0 | be | 0 | 16 | `0x40` | 1 / 0 | 5 | 201 | 2023-03-09T17:06:30Z |
| V2LE | `hsqs` | 2:0 | le | 0 | 16 | `0x40` | 1 / 0 | 5 | 196 | 2023-03-09T17:05:52Z |

Read as observations: the magic word is `sqsh` big endian and `hsqs` little endian in both
versions, so the magic alone does not separate v1 from v2 — the `s_major`/`s_minor` pair does, at
offset 28; `block_size_1` is 32768 on the two v1 carriers and 0 on the two v2 carriers, while
`block_log` reads 15 and 16; `flags` is `0x00` on both v1 carriers and `0x40` on both v2
carriers, on both byte orders. Derived (arithmetic, not measured): 65536 does not fit the 16-bit
`block_size_1` field, so the v2 value is its truncation (65536 mod 65536 = 0), and `block_log` 16
reproduces 65536 — which is exactly what `unsquashfs -s` prints ("Block size 65536"); the reader
prints "Block size 32768" for the v1 pair.

**Two observers disagree on the word "compressed" for the big-endian pair.** Recorded verbatim,
not resolved:

- `file` 5.48: V1BE and V2BE "… version 1.0/2.0, **uncompressed**, 177/201 bytes …"; V1LE and
  V2LE "… version 1.0/2.0, **compressed**, 176/196 bytes …".
- `unsquashfs -s` 4.7.5: all four carriers print "Inodes are compressed" and
  "Data are compressed" (v2 additionally "Fragments are compressed", "Number of fragments 1").
- The `flags` byte is the same per version across byte orders (`0x00`/`0x40`), so the `file` word
  is not a function of that byte, and `file` also prints v1's `block_size_1` as "−32768" (it
  reads the 16-bit field signed) where the reader prints 32768.

This entry prefers neither word: it records that the big-endian pair is labelled "uncompressed"
by `file` and "compressed" by `unsquashfs`, and it does not assign a meaning to `flags` bit
`0x40` in v1/v2. Whether a given block is stored raw is not decided here.

## The oracle census

Two independent readers, neither of them sasquatch: `unsquashfs` 4.7.5 (squashfs-tools; S139) and
the unblob 26.6.4 `__output__` expected tree (S138). They agree on every regular file of all four
carriers — the extraction census below (receipt runs `member-sha256-*`) is byte-identical to the
members landed under `corpus/evidence/round-44/oracle/`.

| carrier | fixture file (under `corpus/evidence/round-42/c2/fixtures/`) | sha256 | size | handler | endian | regular files | symlinks | device nodes | dirs |
|---|---|---|---|---|---|---|---|---|---|
| V1BE | `v1-be--squashfs_v1.0_be.bin` | `529e10775cc152e6c5df0c6c63316811004cc73ce99f03989c86ffd396d631e6` | 4096 | `squashfs_v1` | be | 3 | 0 | 0 | root only |
| V1LE | `v1-le--squashfs_v1.0_le.bin` | `b45925fa779eae0293635ce0e6dc8760308f25227dd88645d677ba3ffce23e71` | 4096 | `squashfs_v1` | le | 3 | 0 | 0 | root only |
| V2BE | `v2-be--squashfs_v2.0_be.bin` | `79c0f3886291f4abcc656acd49932446cf16afaa67e6ffb0c5258e3c2e2dfcc0` | 4096 | `squashfs_v2` | be | 4 | 0 | 0 | root only |
| V2LE | `v2-le--squashfs_v2.0_le.bin` | `7c62dbe388b972119f5d17a12836a016737d58276184f4caa2a90dafd924f124` | 4096 | `squashfs_v2` | le | 4 | 0 | 0 | root only |

Member census (sha256, size, relative path), identical for the two byte orders of a version:

| version | members |
|---|---|
| v1 | `303980bcb9e9e6cdec515230791af8b0ab1aaa244b58a8d99152673aa22197d0` 6 `apple.txt` · `5a81483d96b0bc15ad19af7f5a662e14b275729fbc05579b18513e7f550016b1` 7 `banana.txt` · `86baf3529da550a44b0681ffa031b6b676e620e9e06dc5ac1119d0cd21cbcf55` 7 `cherry.txt` |
| v2 | `6181259c6b2ca629a56920b422e9a8f212a4d0bcead923df92dbd66fbb7e1c30` 7 `apple1.txt` · `919fc82d6f1031d305dbce2fc5a74a6df5ddf2da472ee4d137c681cef28d4aff` 7 `apple2.txt` · `2d95014ed3f24e86ce5fc3a4529f057d7b2318d9b24b54f2e9476b154bd21ec6` 7 `apple3.txt` · `08d9b05b15b998f2dbc741399fef4350c7863cc85df2305d7da4e83e8c8a959d` 7 `apple4.txt` |

The two byte orders of each version therefore hold the same member set with the same digests and
sizes (the census outputs are equal: v1 `908d3f2427a4a77e…`, v2 `df84669fe894a903…`), even though
the container bytes differ (`bytes_used` 177 vs 176 and 201 vs 196). The v1 image carries three
data files plus the root directory — its superblock counts 4 inodes; v2 carries four files plus
the root — 5 inodes.

**What the after-side receipt must show.** For each frozen carrier, the committed round-44
`extract-firmware` receipt must name that carrier's frozen handler (exact string), publish every
regular file above at its exact relative path under the chunk extract root with the same sha256
and size, publish no other file, and account for every non-regular oracle row by the frozen gap
rule. These four carriers hold **no symlink and no device node** and exactly one directory level,
so the symlink halves of the gap rule (`unpublished-entry` per in-tree symlink,
`MaliciousSymlinkRemoved` per escaping symlink) and the `depth-limited` structural gap have
nothing to bind to on this carrier set: an `unpublished-entry`, `MaliciousSymlinkRemoved`,
`depth-limited` or `unknown-chunk-handler` gap on any of these four is a failed carrier, not a
tolerated one. The counter checks the rule either way.

## What stays Frontier, and why

- `squashfs_v2_nonstandard` (v2ns, `sqlz`/`zlqs`): **no independent reader.** Measured
  2026-10-28 on both committed v2ns fixtures: `unsquashfs` 4.7.5 exits 1 with
  `FATAL ERROR: Can't find a valid SQUASHFS superblock`; `7z` 26.04 exits 2 with
  `Cannot open the file as archive`. The standard v2 oracle is unavailable for these bodies, and
  a same-tool oracle (unblob/sasquatch reading what unblob/sasquatch wrote) is not an oracle.
  Fact worth recording: the v2ns fixture differs from the standard v2 fixture **only inside the
  4-byte magic word**, and only in two of its four bytes. `bytediff.py` (receipt runs
  `bytediff-v2be-v2nsbe`, `bytediff-v2le-v2nsle`) reports `diff_bytes=2` over two 4096-byte files
  in each pair: 0-based offsets 2 and 3 (`s`→`l`, `h`→`z`, i.e. `sqsh`→`sqlz`) for the BE pair,
  offsets 0 and 1 (`h`→`z`, `s`→`l`, i.e. `hsqs`→`zlqs`) for the LE pair. Every other byte of
  both images, the whole superblock tail and both data sets included, is equal. So v2ns is a
  magic-spelling variant of a body whose extraction this round does measure; it is not promoted
  because its own magic has no second reader, not because its contents are unknown.
- `squashfs_v3_broadcom` (`shsq`/`qshs`): `unsquashfs` 4.7.5 refuses the magic (exit 1, same
  superblock error); `7z` 26.04 **does** list the committed LE broadcom fixture (exit 0, 2
  entries). A partial reader therefore exists, but no REA `extract-firmware` outcome was measured
  for this family this round and the C1 predicate is bound to v1/v2 carriers only; it stays
  Frontier until a carrier is frozen and run.
- `squashfs_v3_nonstandard` (`sqlz`/`zlqs` at v3): both readers refuse (`unsquashfs` exit 1,
  `7z` exit 2). Frontier, unchanged.
- gzip v3 bodies: **a reader exists** — `unsquashfs` 4.7.5 lists the committed gzip v3 fixtures
  (exit 0, both byte orders) — which is why this family is not in the "no reader" class. It stays
  Frontier because the round-42 Core row covers LZMA v3 bodies on published images only, and the
  gzip v3 fixtures are round-42 C2 held-out *inputs* with no C1 after-receipt. (For contrast the
  LZMA v3 fixture is refused by `unsquashfs`: `gzip uncompress failed with error code -3` —
  round-42's v3 oracle was backhand-cli 0.25.5 plus 7-Zip.)
- `squashfs_v4_broadcom`, LE AVM members (`hsqs`), AVM kernel images and nested sub-images below
  depth 1: unchanged from the round-41/42 notes; nothing was measured for them this round, and
  this entry says nothing new about them.

## Observation, inference, unknown

**Observed** (2026-10-28, on the committed fixtures, or read from the pinned handler source):
the four carriers hash to the pins above; the superblock fields in the table; every member digest
and size in the census; the equality of the two byte orders' member censuses; the `unsquashfs -s`
lines and the `file` labels quoted verbatim; the v2ns refusals from both external readers; the
`cmp -l` byte diffs; the `7z` listing of the LE broadcom fixture; the handler classes, patterns,
`EXTRACTOR` and the argv decision at the cited lines.

**Inferred** (derived, not measured): the v2 `block_size_1` of 0 is the 16-bit truncation of
65536 (arithmetic, cross-checked against the reader's printed block size); the `file` compression
word does not follow the `flags` byte (that byte is equal within a version and the word differs
across byte orders); these four carriers exercise only the regular-file publication path (their
census holds no symlink, device node or second directory level).

**Unknown**: which of the two compression words is right for the big-endian pair, and what bit
`0x40` of the v1/v2 `flags` byte means; whether any SquashFS v1/v2 image outside these four
extracts through REA at all; and the after-side REA outcome itself, which the counter scores at
the landing revision and which this draft does not assert.

## Limits

Four 4 KiB fixtures carrying 3–4 regular files each are a thin carrier set: the entry says the
handler family works through REA on these bytes, not that every v1/v2 image extracts. No symlink,
no device node, no hard link, no sparse file and no fragment-bearing large file occurs in the set,
so none of those paths is exercised. The v1 fixtures are uncompressed at the `file` layer and
flagged compressed by the reader as recorded above; no carrier exercises the "uncompressed
blocks" bit of v1/v2 either way. The counter's REA rerun shows the carriers extract the same way
at scoring time; it cannot prove which process wrote a committed receipt (R40-CL2). Nothing is
claimed about the contents of the extracted text files. The extraction commands, their exit
codes and their stdout digests are in the seat receipt
`.ufo/waves/round-44/w1/artifacts/R44EntryDraft/receipt.json`; the byte-level provenance of the
fixtures is `tools/round-42/fixtures.json` (unblob 26.6.4, commit `1fcc7a0a…`, MIT).
