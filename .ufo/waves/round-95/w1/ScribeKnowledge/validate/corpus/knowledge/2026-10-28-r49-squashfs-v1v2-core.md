# SquashFS v1 and v2 through REA on four frozen fixtures: `squashfs_v1` and `squashfs_v2` (round 49, R49-C1 Core, 4/4 carriers)

status: R49-C1 — the four carriers matched 4/4 at the data commit `4aabb0b4bf716fb564c8406509c40b0a67457800` (`.ufo/waves/round-49/l1/scores/c1-at-data-4aabb0b4.json`: `carriers_matched 4`, `failing []`, `frozen_path_changed []`; the six documentation bindings were false there because this entry and the PROVINCE/README rows did not yet exist). The score at the landing revision, against the single round-49 freeze `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d`, is `.ufo/waves/round-49/l1/scores/c1-final.json` (counter `tools/round-49/c1-counter.py`, sha256 `ac83715b199100774873389ea33fb4819231e1f963225416e86ad422f69d287f`); the control ledger is `.ufo/waves/round-49/controls/summary.json` (`kill_rule_fires false`). Round 44 stopped on this same claim because its frozen claim and its frozen counter named different provenance paths for the REA output directory (`corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`); round 49 states that predicate once (a prefix test on `/fast/scratch/hyaku/kaidoku-r49/`) and the counter implements that sentence. What the counter measures is REA's behaviour on the four frozen bytes, reproduced by its own rerun; it does not authenticate who wrote the committed receipt (plan, disclosed limit).

source: S138 — https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs — the unblob 26.6.4 `__output__` expected member trees for `squashfs_v1` and `squashfs_v2` in both byte orders (MIT). Re-opened 2026-10-28 (receipts `S138-tag`, `S138-members-reopen`): the tag `26.6.4` peels to commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`; all 22 member bytes fetched from the media base hash to the manifest sha256 with no mismatch (`members 22 mismatches 0`). Round-44 provenance: 10 contents-API listings HTTP 200, 2026-10-28T11:10:29Z–11:10:43Z; manifest `corpus/evidence/round-44/oracle/manifest.json`, sha256 `06a72dd5b660c79adae943917abf40c24ab16554ec6c2f14985958799a78f5fe` (receipt `manifest-sha`), `failures: []`
source: S139 — https://github.com/plougher/squashfs-tools/releases — the upstream release that grounds the second reader's identity, `/usr/bin/unsquashfs` (`unsquashfs version 4.7.5 (2026/03/01)`, sha256 `461e1fd9eac39c12e673042807459985636030d5557319343fc3a6ed4ba1677c`; receipt `unsquashfs-version`). Re-opened 2026-10-28: the release API `https://api.github.com/repos/plougher/squashfs-tools/releases/tags/4.7.5` returns `tag_name 4.7.5`, `published_at 2026-03-01T23:05:47Z` (receipt `S139-release`); the releases page returns HTTP 200 and 361757 bytes (receipt `S139-releases-page`; the round-44 row recorded 398943 bytes of the same dynamic page, so the byte count is not a stable pin)
source: S112 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — `SquashFSExtractor` :24-69 (executables :25-26, `match endian, self.version` argv decision :39-54, tail :56-64, dependencies :68-69), `_SquashFSBase` :72-99 (`BIG_ENDIAN_MAGIC` :73, `EXTRACTOR = SquashFSExtractor(3, 0x73717368)` :75), `SquashFSv1Handler` :101 (`NAME` :102, patterns :105-121, `C_DEFINITIONS` :123-136), `SquashFSv2Handler(SquashFSv1Handler)` :158 (`NAME` :159, patterns :161-178), `SquashFSv2NonStandardHandler` :199 (`NAME` :200, `BIG_ENDIAN_MAGIC` :202, `EXTRACTOR` :204), `SquashFSv3Handler` :244, `SquashFSv3BroadcomHandler` :363, `SquashFSv3NSHandler` :409 (receipt `S112-snapshot` lines). Re-opened 2026-10-28: HTTP 200, 590 lines, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` (receipts `S112-raw`, `S112-snapshot`; the snapshot is `.ufo/waves/round-49/w1/C1ScribeEntry/artifacts/squashfs-26.6.4.py`). The registry row S112 says `lines 24-70`; the file's last extractor line is 69, so this entry cites 24-69.
verified-at: 2026-10-28
recheck: 180d — re-run the frozen counter at the measured revision (`python3 -I -B tools/round-49/c1-counter.py --root . --rev <measured> --freeze <FREEZE> --pkg65 <rea-agents 6.5.0 root> --work <SCRATCH> --json-out <OUT>`) and the oracle census below (`unsquashfs -s`, `unsquashfs -lls`, extraction + member digests, the superblock decode, the 0x78da stream scan); a carrier whose sha256 differs from the pins below, a member digest that differs from the census table, or `unsquashfs -version` no longer reading 4.7.5 means this entry is re-read.

## What moved Frontier → Core

Before round 49 (2026-10-28) `PROVINCE.md` carried `SquashFS v1/v2` as still-Frontier (round-42 frontier note, line 416; receipt `province-416`: "Still Frontier: SquashFS v1/v2, `squashfs_v3_broadcom`, …"). Round 49 adds the `## Round-49 additions to Core` row `squashfs_v1` and `squashfs_v2` (SquashFS v1 and v2, gzip bodies, both byte orders) and cites this entry. Promotion outcome: moved to Core, on the four frozen carriers only, if and only if the counter is met at the landing revision (`.ufo/waves/round-49/l1/scores/c1-final.json`); the round-44 `measured, not promoted` note is superseded for v1/v2 and nothing else.

Scope of the claim, in one sentence: it is about the *handler family through REA on the four frozen carriers*, not "every SquashFS v1/v2 image on the internet". Published v1/v2 rootfs images were probed in round 44 and were not fetchable (`archive.openwrt.org/whiterussian/rc6/openwrt-brcm-2.4-squashfs.trx` returned 404 on 2026-10-28; the DD-WRT beta listing was empty), so no published carrier enters this round; the four fixtures are the whole carrier set.

## The handler family, from the handler source

unblob 26.6.4 defines the two handlers as separate classes with the same extractor (S112). `SquashFSv1Handler` (`NAME = "squashfs_v1"` :102) is matched by `73 71 73 68 [24] 00 01` (big endian) or `68 73 71 73 [24] 01 00` (little endian) (:105-121): the magic `sqsh`/`hsqs`, 24 skipped bytes, then the two bytes of the 16-bit `s_major` field, i.e. `s_major` = 1. The pattern does not constrain `s_minor`. `SquashFSv2Handler` inherits from it and only overrides the patterns (:161-178), whose `s_major` bytes are `00 02` / `02 00`, i.e. 2. Neither class overrides `EXTRACTOR`, so both use `_SquashFSBase.EXTRACTOR = SquashFSExtractor(3, 0x73717368)` (:75).

That extractor's argv decision (:37-54) branches on `endian, self.version`; only the `Endian.BIG, 4` case is special. For v1 and v2 the decision falls to `case Endian.BIG, _` → `-be` (:51-52) and `case Endian.LITTLE, _` → `-le` (:53-54), followed by the fixed tail `-no-exit-code -f -d {outdir} {inpath}` (:56-64; receipt `s112-argv`). So the command a v1/v2 chunk runs is

```
sasquatch -be| -le -no-exit-code -f -d {outdir} {inpath}
```

i.e. the same executable and the same tail as the round-42 v3 lane, and **no new REA key**: the handler name changes, the extractor does not. Endianness is the only argv difference between the four carriers. The executable `sasquatch` resolves to `/home/vgpnk/.local/bin/sasquatch`, which reports `unsquashfs version 4.5.1 (2022/03/17)` (receipts `sasquatch-where`, `sasquatch-version`; binary sha256 `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`); the counter's `FIXED_PATH` includes `~/.local/bin`, so the child process resolves the same binary.

**Binding rule — per carrier, exact equality.** The REA `extract-firmware` receipt for carrier *X* must name *X*'s frozen handler, and the name must be equal as a whole string: `squashfs_v1` for `v1le`/`v1be`, `squashfs_v2` for `v2le`/`v2be` (frozen `handler_detail`: v1, v1, v2, v2). Prefix matching is inadmissible: `squashfs_v2` is a strict prefix of `squashfs_v2_nonstandard` (S112 :200), and `squashfs_v3` is a strict prefix of `squashfs_v3_broadcom` (:363) and `squashfs_v3_nonstandard` (:409). A prefix-keyed comparator would let a v2-nonstandard receipt satisfy a v2 carrier without any byte being wrong. Exact equality also keeps a v1 receipt from satisfying a v2 carrier, which is the point of promoting two versions rather than one.

## The superblock, read from the bytes

`scripts/sb.py` (receipt `sb-decode-v2`) reads the first 32 bytes as unblob's `squashfs_super_block_t` (`char s_magic[4]`, six `uint32`, `uint16 s_major`, `uint16 s_minor`; S112 :123-137), then the v1/v2 packed tail at offset 32 (`block_size_1` u16, `block_log` u16, `flags` u8, `no_uids` u8, `no_guids` u8, `mkfs_time` u32) in the carrier's own byte order. The tail offsets are the draft layout, checked against `unsquashfs -s` (receipt `unsquashfs-s`: "Block size 32768" on the v1 pair, "Block size 65536" on the v2 pair; "Number of inodes 4/4/5/5"; "Filesystem size 177/176/201/196 bytes").

| carrier (frozen id) | magic | s_major:s_minor | order | block_size_1 | block_log | flags | no_uids/no_guids | inodes | bytes_used | mkfs_time (UTC, `sb.py`) |
|---|---|---|---|---|---|---|---|---|---|---|
| `v1be` | `sqsh` | 1:0 | be | 32768 | 15 | `0x00` | 1 / 0 | 4 | 177 | 2024-08-05T07:18:58Z |
| `v1le` | `hsqs` | 1:0 | le | 32768 | 15 | `0x00` | 1 / 0 | 4 | 176 | 2024-08-05T07:18:51Z |
| `v2be` | `sqsh` | 2:0 | be | 0 | 16 | `0x40` | 1 / 0 | 5 | 201 | 2023-03-09T17:06:30Z |
| `v2le` | `hsqs` | 2:0 | le | 0 | 16 | `0x40` | 1 / 0 | 5 | 196 | 2023-03-09T17:05:52Z |

Correction to the round-44 table: its v1 `mkfs_time` values (04:18:58Z and 04:18:51Z) are the host-local rendering that `unsquashfs -s` and `7z` print (`tz-offset`: the host offset is `-0300`), not UTC. The decoded UTC values are 07:18:58Z and 07:18:51Z (`sb-decode-v2`; `date -d @1722842338 -u` = `2024-08-05T07:18:58Z`). The v2 values were already UTC. `file(1)` prints UTC (`file-labels`: `created: Mon Aug  5 07:18:58 2024`).

Read as observations: the magic word is `sqsh` big endian and `hsqs` little endian in both versions, so the magic alone does not separate v1 from v2 — the `s_major`/`s_minor` pair does, at offset 28. `block_size_1` is 32768 on the two v1 carriers and 0 on the two v2 carriers, while `block_log` reads 15 and 16. `flags` is `0x00` on both v1 carriers and `0x40` on both v2 carriers, on both byte orders. Derived (arithmetic, not measured): 65536 does not fit the 16-bit `block_size_1` field, so the v2 value is its truncation (65536 mod 65536 = 0), and `block_log` 16 reproduces 65536, which is what `unsquashfs -s` prints.

**Compression is gzip on all four; the superblock carries no compression selector.** `unsquashfs -s` prints "Inodes are compressed" and "Data is compressed" for every carrier (v2 adds "Fragments are compressed" and "Number of fragments 1"; receipt `unsquashfs-s`). The carrier bytes carry zlib streams at `78 da`: one stream at byte offset 73 in each v1 image; offsets 63, 90 and 140 in `v2be` and 63, 90 and 138 in `v2le` (receipt `sb-decode-v2`, field `zlib_78da_offsets`). 7-Zip 26.04 reports the v1 members as compressed 6→6, 7→7, 7→7 bytes, and the four v2 members as one 25-byte compression (`apple1.txt` 7→25 and 0 for the other three; receipt `sevenzip-list`). The counter's `compression_detail` for the four carriers is `["gzip","gzip","gzip","gzip"]` and derives the class from the inode-table metadata block body plus the chain witness, not from a field (round-44 counter note, `.ufo/waves/round-44/w1/R44C1Counter.md`, "Compression is observed, not read from a field").

**The big-endian `file(1)` label is a layout artifact, not an image property.** `file` 5.48 (receipt `file-version`) prints `… version 1.0/2.0, uncompressed, 177/201 bytes …` for `v1be`/`v2be` and `… compressed, 176/196 bytes …` for `v1le`/`v2le`, and prints v1's `block_size_1` as `-32768` (receipt `file-labels`). The label flips with byte order alone: the two byte orders of a version carry the identical `flags` byte and the same member digests, and both carry zlib streams, so no field distinguishes them. A reader who takes the word as a compression statement would mark the two big-endian carriers wrong while every other reader decodes gzip.

## The oracle: `unsquashfs` is a second reader from another squashfs-tools release; 7-Zip is a third reader; the unblob `__output__` tree is same-lineage

Three readers see these four carriers. They are **not** three independent producers, and the first two are not independent implementations either:

- **`unsquashfs` 4.7.5 is the second reader** (S139): the upstream squashfs-tools release. Its `-lls` member census (receipt `unsquashfs-lls`) and its extracted member digests (receipt `unsquashfs-extract-digests`) are an outside measurement of the same bytes. Its member digests are frozen per carrier in `tools/round-49/carriers.json` and re-extracted at scoring time.
- **The first reader, sasquatch, is a patch set over the same upstream codebase.** The sasquatch README (S111, row in `corpus/SOURCES.md`) describes it as a patch set over the standard `unsquashfs`, and its build script downloads squashfs-tools v4.3, patches it and builds (`corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`). The onekey-sec package the lane installed reports `unsquashfs version 4.5.1`, and the release body of `sasquatch-v4.5.1-1` says it is rebased on squashfs-tools 4.5.1 (`corpus/knowledge/2026-10-27-sasquatch-release-matrix.md`). The two readers therefore descend from one squashfs-tools codebase through different bases and patch sets. This is the difference the entry relies on, and it is not an independent-implementation claim: the round-44 wording "independent oracle" is withdrawn in favour of "second reader from another squashfs-tools release".
- **7-Zip 26.04 is a third reader, corroboration only** (receipt `sevenzip-list`): it lists all four carriers (exit 0) with the same member names and sizes (3 files / 20 B on the v1 pair, 4 files / 28 B on the v2 pair). It corroborates the member set; the digest census is `unsquashfs`'s.
- **The unblob 26.6.4 `__output__` expected tree (S138) is same-lineage, not independent**: it is unblob's own integration expectation, produced through the sasquatch extractor under test. It checks that the lane reproduces the producer's own expected tree; it cannot corroborate the extractor, and this entry does not present it as a second producer.

All three agree on names and sizes, and `unsquashfs` and the S138 `__output__` tree agree on every regular file's sha256 (`unsquashfs-extract-digests` against `S138-members-reopen`). That agreement is one expectation checked against one reader from another release plus one third reader, not "two independent oracles".

## The carriers and their census

Frozen ids are `tools/round-49/carriers.json` (lowercase; the counter matches them case-insensitively, but this entry uses the frozen spelling). Files are under `corpus/evidence/round-42/c2/fixtures/`.

| carrier | fixture file | sha256 (receipt `fixtures-sha`) | size (bytes) | handler | endian | regular files | symlinks | device nodes | dirs |
|---|---|---|---|---|---|---|---|---|---|
| `v1be` | `v1-be--squashfs_v1.0_be.bin` | `529e10775cc152e6c5df0c6c63316811004cc73ce99f03989c86ffd396d631e6` | 4096 | `squashfs_v1` | be | 3 | 0 | 0 | root only |
| `v1le` | `v1-le--squashfs_v1.0_le.bin` | `b45925fa779eae0293635ce0e6dc8760308f25227dd88645d677ba3ffce23e71` | 4096 | `squashfs_v1` | le | 3 | 0 | 0 | root only |
| `v2be` | `v2-be--squashfs_v2.0_be.bin` | `79c0f3886291f4abcc656acd49932446cf16afaa67e6ffb0c5258e3c2e2dfcc0` | 4096 | `squashfs_v2` | be | 4 | 0 | 0 | root only |
| `v2le` | `v2-le--squashfs_v2.0_le.bin` | `7c62dbe388b972119f5d17a12836a016737d58276184f4caa2a90dafd924f124` | 4096 | `squashfs_v2` | le | 4 | 0 | 0 | root only |

Sizes: `stat -c '%n %s'` on the four fixtures (receipt `fixtures-sha`). The symlink, device and directory columns are from `unsquashfs -lls` (receipt `unsquashfs-lls`: one `d` row for `squashfs-root` and only `-` rows below it, no `l`, `c` or `b` rows).

Member census (sha256, size, relative path; receipt `unsquashfs-extract-digests`, identical for the two byte orders of a version):

| version | members |
|---|---|
| v1 | `303980bcb9e9e6cdec515230791af8b0ab1aaa244b58a8d99152673aa22197d0` 6 `apple.txt` · `5a81483d96b0bc15ad19af7f5a662e14b275729fbc05579b18513e7f550016b1` 7 `banana.txt` · `86baf3529da550a44b0681ffa031b6b676e620e9e06dc5ac1119d0cd21cbcf55` 7 `cherry.txt` |
| v2 | `6181259c6b2ca629a56920b422e9a8f212a4d0bcead923df92dbd66fbb7e1c30` 7 `apple1.txt` · `919fc82d6f1031d305dbce2fc5a74a6df5ddf2da472ee4d137c681cef28d4aff` 7 `apple2.txt` · `2d95014ed3f24e86ce5fc3a4529f057d7b2318d9b24b54f2e9476b154bd21ec6` 7 `apple3.txt` · `08d9b05b15b998f2dbc741399fef4350c7863cc85df2305d7da4e83e8c8a959d` 7 `apple4.txt` |

Each member digest above was also re-fetched from the S138 media base and matched (`S138-members-reopen`, 22 of 22). The two byte orders of each version hold the same member set with the same digests and sizes, even though the container bytes differ (`bytes_used` 177 vs 176 and 201 vs 196). The v1 image carries three data files plus the root directory (4 inodes); v2 carries four files plus the root (5 inodes). The S138 expected trees contain 22 members in total because they also hold the v2.1 outputs (`squashfs_v2.1_*`), which are not carriers and are not scored.

## What the scored receipts show

Everything in this section comes from the data run after the freeze (`corpus/evidence/round-49/c1/`, commit `4aabb0b4`) and is quoted from the committed round-49 receipts and the counter output `.ufo/waves/round-49/l1/scores/c1-at-data-4aabb0b4.json`; nothing here is carried over from round 44.

For each frozen carrier the round-49 `extract-firmware` receipt names exactly that carrier's frozen handler (`handler_detail` v1, v1, v2, v2; per-carrier `handler_ok true on all four`), publishes the census's regular files at their exact relative paths under `firmware.bin_extract/` with the oracle's sha256 and size, publishes nothing else (`extra_published []`), and reports no gap of any kind (`gap_kinds []`, coverage `complete` on all four, `gap_rule_uncovered_kinds []`):

| carrier | published files | published bytes | gaps | coverage | receipt |
|---|---|---|---|---|---|
| `v1le` | 3 | 20 | `[]` | `complete` | `corpus/evidence/round-49/c1/v1le/after.json` |
| `v1be` | 3 | 20 | `[]` | `complete` | `corpus/evidence/round-49/c1/v1be/after.json` |
| `v2le` | 4 | 28 | `[]` | `complete` | `corpus/evidence/round-49/c1/v2le/after.json` |
| `v2be` | 4 | 28 | `[]` | `complete` | `corpus/evidence/round-49/c1/v2be/after.json` |

These four carriers hold no symlink and no device node and exactly one directory level, so the symlink halves of the frozen gap rule (`unpublished-entry` per in-tree symlink, `MaliciousSymlinkRemoved` per escaping symlink) and the `depth-limited` structural gap have nothing to bind to here. A gap of any of those kinds on any of these four would be a failed carrier, not a tolerated one. The counter checks the rule either way: `per_carrier_failing []`, `gap_rule_problems []`. Each carrier's envelope id recomputes over its subject (`evidence_id_ok true on all four`), and its subject digest equals the fixture pin (`carrier_pin_ok true on all four`). The run's `parameters.output_directory` is `a path under `/fast/scratch/hyaku/kaidoku-r49/probe-R49C1Run/` (`provenance_ok` is a prefix test)`, an absolute path inside the `/kaidoku-r49/` scratch segment; the runner then copied the produced tree verbatim under `corpus/evidence/round-49/c1/<id>/` and recorded `provenance.json`. The committed evidence path is not the output directory, and that sentence is the one the counter implements.

The counter-time rerun (`projection_ok true on all four`) proves that the counter's own REA run of the same bytes has the same semantic projection as the committed receipt. It does not prove which process wrote the committed receipt (R40-CL2).

## What stays Frontier, and why

- `squashfs_v2_nonstandard` (v2ns, `sqlz`/`zlqs`): **no independent reader.** Measured 2026-10-28 on both committed v2ns fixtures: `unsquashfs` 4.7.5 exits 1 and `7z` 26.04 exits 2 (receipt `v2ns-readers`). Fact worth recording: the v2ns fixture differs from the standard v2 fixture **only inside the 4-byte magic word**, in two of its four bytes. `cmp -l` reports 2 differing bytes in each pair (receipt `v2ns-cmp`): 1-based positions 3 and 4 for the BE pair (`sqsh` → `sqlz`), 1 and 2 for the LE pair (`hsqs` → `zlqs`). So v2ns is a magic-spelling variant of a body whose extraction round 49 does measure; it is not promoted because its own magic has no second reader, not because its contents are unknown.
- `squashfs_v3_broadcom` (`shsq`/`qshs`): `unsquashfs` 4.7.5 refuses the magic (exit 1, "Can't find a valid SQUASHFS superblock"); `7z` 26.04 **does** list the committed LE broadcom fixture (exit 0, 2 files, 13 B; receipt `v3-readers`). A partial reader therefore exists, but no REA `extract-firmware` outcome was measured for this family and the C1 predicate is bound to v1/v2 carriers only; it stays Frontier.
- `squashfs_v3_nonstandard` (`sqlz`/`zlqs` at v3) and `squashfs_v3_ddwrt`'s no-pad fixture: both readers refuse (`unsquashfs` exit 1, `7z` exit 2; receipt `v3-readers`). Frontier, unchanged.
- gzip v3 bodies: a reader exists: `unsquashfs` 4.7.5 lists the committed gzip v3 fixtures (exit 0, both byte orders; receipt `v3-readers`). It stays Frontier because the round-42 Core row covers LZMA v3 bodies on published images only, and the gzip v3 fixtures have no round-49 REA receipt. For contrast, the LZMA v3 fixture `v3adapt-be--squashfs_v3_be.lzma.bin` is refused by `unsquashfs` with `gzip uncompress failed with error code -3` (exit 1; receipt `v3-readers`); round 42's v3 oracle was backhand-cli 0.25.5 plus 7-Zip.
- The promoted v1/v2 row covers gzip bodies only, because every v1/v2 carrier measured here is gzip. Nothing in round 49 measures a non-gzip v1/v2 body, so the row says nothing about one. [INFERENCE] whether a v1/v2 body with another compressor exists in the wild is not established by this entry.
- `squashfs_v4_broadcom`, LE AVM members (`hsqs`), AVM kernel images and nested sub-images below depth 1: unchanged from the round-41/42 notes; nothing was measured for them this round, and this entry says nothing new about them.

## Observation, inference, unknown

**Observed** (each with its receipt in the table below): the four carriers hash to the pins; the superblock fields in the table; every member digest and size in the census; the equality of the two byte orders' member censuses; the `unsquashfs -s` lines; the `file` labels; the `7z l` listings of all four carriers; the zlib stream offsets; the v2ns refusals from both external readers and its two-byte magic diff; the `7z` listing of the LE broadcom fixture; the S138 member re-fetch (22 of 22); the S139 release identity; the S112 handler classes, patterns, `EXTRACTOR` and the argv decision at the cited lines; the sasquatch identity; and the scored counter's fields quoted above.

**Inferred** (derived, not measured): the v2 `block_size_1` of 0 is the 16-bit truncation of 65536 (arithmetic, cross-checked against the printed block size); the `file` word is a layout artifact (it flips with byte order while the `flags` byte and every member digest stay the same); these four carriers exercise only the regular-file publication path (their census holds no symlink, device node or second directory level); the v2 fragment block holds the four 7-byte members (`unsquashfs -s` prints one fragment and 7-Zip prints a single 25-byte compression for `apple1.txt`; that the one fragment block carries the other three members as well is not measured).

**Unknown**: what bit `0x40` of the v1/v2 `flags` byte means; whether any SquashFS v1/v2 image outside these four extracts through REA at all; whether sasquatch's patches (S111) change any v1/v2 result relative to `unsquashfs` 4.7.5 beyond these four carriers; and which process wrote the committed receipts (R40-CL2).

## Limits

Four 4 KiB fixtures carrying 3–4 regular files each are a thin carrier set: the entry says the handler family works through REA on these bytes, not that every v1/v2 image extracts. No symlink, no device node, no hard link, no sparse file and no multi-block member occurs in the set, so none of those paths is exercised. The second reader is `unsquashfs` from squashfs-tools 4.7.5, and the first reader is a patch set over the same codebase (see the oracle section); the entry claims a second reader from another release, not a second implementation. The unblob `__output__` tree is same-lineage and is used only as the producer's own expectation. The counter's rerun shows the carriers extract the same way at scoring time; it cannot prove which process wrote a committed receipt (R40-CL2). Nothing is claimed about the contents of the extracted text files beyond their sha256 and size.

## Commands and receipts

Every number above is a receipt in `.ufo/waves/round-49/w1/C1ScribeEntry/receipts.tsv` (id, UTC time, exit code, stdout sha256, command). They stay in the wave directory, committed with wave 1 at `14936cb9`; no copy under `corpus/` is made.

| receipt id | UTC (2026-10-28) | exit | stdout sha256 (first 16) | command (abridged) |
|---|---|---|---|---|
| `unsquashfs-version` | 21:09:22 | 0 | 4b8162d55d32ebe2 | `unsquashfs -version`; `sha256sum /usr/bin/unsquashfs` |
| `sevenzip-version` | 21:09:22 | 0 | be8a9da1596fc88d | `7z i` |
| `file-version` | 21:09:22 | 0 | a311e6759c256049 | `file --version` |
| `sasquatch-version` | 21:09:35 | 0 | 923b821159b4a32d | `sasquatch -v`; `sha256sum $(command -v sasquatch)` |
| `manifest-sha` | 21:09:22 | 0 | 7a0dc230935791fd | `sha256sum corpus/evidence/round-44/oracle/manifest.json` |
| `fixtures-sha` | 21:09:22 | 0 | 301900a887849fa9 | `sha256sum` and `stat -c '%n %s'` on the four carriers |
| `S112-raw` | 21:09:35 | 0 | c11e3f4837efde24 | `curl` of the S112 raw file (HTTP 200) |
| `S112-snapshot` | 21:09:35 | 0 | 808bbb666351fa84 | `curl` S112 to `artifacts/squashfs-26.6.4.py`; `sha256sum`; `grep` of the handler lines |
| `S139-release` | 21:09:35 | 0 | 288b4636f6cf2507 | `curl` release API for tag 4.7.5 |
| `S139-releases-page` | 21:11:23 | 0 | beb32b9f36402c85 | `curl` releases page (HTTP 200, 361757 B) |
| `S138-tag` | 21:09:35 | 0 | 5446481ec2fb48d8 | `curl` git ref `refs/tags/26.6.4` (commit 1fcc7a0a) |
| `S138-members-reopen` | 21:11:16 | 0 | 171e34ff46dae36b | `scripts/s138.py`: 22 member bytes re-fetched and hashed (0 mismatches) |
| `unsquashfs-s` | 21:09:54 | 0 | eff74001e9ccda25 | `unsquashfs -s` on the four carriers |
| `unsquashfs-lls` | 21:09:54 | 0 | c7996f166c9cbea0 | `unsquashfs -lls` on the four carriers |
| `unsquashfs-extract-digests` | 21:09:54 | 0 | 03ccaa12ba3a8cb5 | `unsquashfs -d` into scratch; `sha256sum` of every extracted file |
| `sevenzip-list` | 21:09:54 | 0 | ae3945ea61d69b0e | `7z l -tSquashFS` on the four carriers |
| `sb-decode-v2` | 21:11:05 | 0 | 644f2b093964119e | `scripts/sb.py` on the four carriers |
| `tz-offset` | 21:11:24 | 0 | 77dca472079b9e41 | `date +%z`; `date -d @<epoch> -u` |
| `file-labels` | 21:11:39 | 0 | e52b16ea0bf33c1d | `file` on the four carriers |
| `v2ns-cmp` | 21:11:39 | 0 | 076034f818d9e751 | `cmp -l` of v2 vs v2ns; `od -c -N4` of the magic |
| `v2ns-readers` | 21:11:39 | 0 | 897ce20a26243196 | `unsquashfs -s` and `7z l` on the two v2ns fixtures |
| `v3-readers` | 21:11:39 | 0 | a921b0fec3eb8b66 | `unsquashfs -lls` and `7z l` on the v3 fixtures |
| `province-416` | 21:09:22 | 0 | 1c5c62cde04d78da | `sed -n 410,420p PROVINCE.md` |
| `province-line416` | 21:11:39 | 0 | 5ef7eb823e03877d | `grep -n 'Still Frontier: Sq' PROVINCE.md` |
| `s-rows-fieldcount` | 21:09:22 | 0 | 8d97fe9b9ee715aa | `awk` field count of the S138/S139 registry rows (11 each) |
| `counter-fixed-path` | 21:11:39 | 0 | c5bbef8c01c96553 | `sed -n 266,272p tools/round-49/c1-counter.py` (FIXED_PATH) |

The round-44 oracle command receipts (`.ufo/waves/round-44/w1/artifacts/R44EntryDraft/receipt.json`, `corpus/evidence/round-44/oracle/manifest.json`) are the earlier run of the same census and are cited for provenance only.

## Corrections after the wave-2 attack (2026-10-28)

Round-49 wave 2 (`.ufo/waves/round-49/w2/`, 40 seats) attacked this entry at `29883d4e`. Its numbers reproduce; the statements below are the repairs it forced. They supersede the sentence they name; the entry is not otherwise rewritten.

1. **Landing score.** The score at the landing revision is `.ufo/waves/round-49/l1/scores/c1-final.json` (its `revision` field names the measured commit; the file is committed one commit later, so it cannot name its own commit). The data-commit score `c1-at-data-4aabb0b4.json` has `exit_code 1` and `met_target false`: six documentation bindings were false because this entry and the PROVINCE/README rows did not yet exist; its `carriers_matched 4`, `failing []` are the carrier clauses.
2. **What the provenance clause is.** `provenance_ok` in the frozen counter is `isabs ∧ no '..' ∧ startswith('/fast/scratch/hyaku/kaidoku-r49/')`. It does not compare the output directory with the committed path, does not read `provenance.json`, and authenticates neither the writer nor the round. Where the status paragraph says the counter "implements that sentence", read this one.
3. **Limits the entry omitted (the plan discloses them).** (a) A relabelled replay — the round-44 receipts with `output_directory` rewritten under `/fast/scratch/hyaku/kaidoku-r49/` and the evidence id re-minted — scores `carriers_matched 4`, as does an envelope computed from the oracle (`.ufo/waves/round-49/w1/C1ProvCritic.md`, `C1GoldForgery.md`; reproduced in `w2/W2C1Forge.md`, `w2/W2Honesty.md`); the claim rests on the counter's own REA rerun, not on the committed receipt. (b) The six documentation bindings are presence checks: a PROVINCE/entry that asserts the opposite scores exit 0 (`w2/W2Honesty.md` H4, `w1/C1DocBindings.md`). (c) **The four carriers are the round-44 fixtures, already measured once in round 44: this is a re-run under a restated predicate, not new data.** (d) The scratch output root named in each `after.json` (`/fast/scratch/hyaku/kaidoku-r49/probe-R49C1Run/c1-run.<id>.<pid>/rea-out`, the name `probe-` is the runner's) was pruned after the verbatim copy; `provenance.json` records `copied_verbatim`.
4. **Scope.** The Core row covers the four standard **v1.0 and v2.0** fixtures (`s_major:s_minor` 1:0 and 2:0). `squashfs_v2` also matches `s_minor` 1 (the handler pattern does not constrain it) and both readers read the standard v2.1 pair, but REA never ran on a v2.1 image and no fixture of that minor is a carrier (`w2/W2Coverage.md` F1). The v3 DD-WRT no-pad and 4k-pad images named above are Frontier as well (`F2` there).
5. **REA pin.** The tool whose behaviour is measured is `rea-agents` 6.5.0 (`npx -y rea-agents@6.5.0 extract-firmware --format json --full-output`, `--max-depth` default 3, no depth-limited gap), recorded in each `run.json`; unblob 26.6.4 and sasquatch 4.5.1 are recorded in `extract-env.json` and match the live host (`w2/W2C1Rea.md`).
6. **Field names.** `handler_detail`, `per_carrier_failing`, `gap_kinds` and `provenance_ok` are the *counter's* score fields or paraphrases, not envelope keys: in the envelopes the handler is `chunks[0].handler`, emptiness is `normalized_result.extraction_gaps == []` and `unpublished_entries == []`, and the per-carrier provenance flag is `run_provenance_ok` (`w2/W2Rea.md` F2-F4). The four envelopes contain none of the typed gap strings (`missing-extractor-dependency`, `unpublished-entry`, `depth-limited`, `MaliciousSymlinkRemoved`): they witness "no gap emitted", not the type strings.
7. **S112 line citations.** The class `SquashFSv2Handler` (:158-196) also assigns `NAME = "squashfs_v2"` (:159) and a `DOC` block (:180-196); it does not assign `EXTRACTOR`. The v1 struct closes at :136 (`HEADER_STRUCT` is :137). `squashfs_v3_broadcom` is the `NAME` string at :364 (class :363) and `squashfs_v3_nonstandard` at :410 (class :409). The `match endian, self.version` argv decision starts at :39 (executable at :37). The registry row S112 says `lines 24-70`; the extractor ends at :69 and the row is append-only, so it is left (`w2/W2C1Sources.md`).
8. **Tail fields.** `block_size_1`, `block_log`, `flags`, `no_uids`/`no_guids` and `mkfs_time` are decoded from the packed layout that follows the 32-byte head; the S112 v1/v2 struct (:123-136) ends at the head, so these offsets rest on the bytes and `unsquashfs -s`, not on S112 (`w2/W2C1Entry.md` D6). `unsquashfs -s` prints `Duplicates are removed` for all four carriers, including the two v1 images whose `flags` byte reads `0x00`: the printed line is not a reading of that bit. That the tail offsets and the `78 da` offsets are exact was re-derived by an independent parser (`w2/W2C1Superblock.md`, 0 differences).
9. **Receipt paths.** `scripts/sb.py` and `scripts/s138.py` are `.ufo/waves/round-49/w1/C1ScribeEntry/scripts/sb.py` and `.../s138.py`; the receipt `counter-fixed-path` ran `sed -n 266,272p .ufo/waves/round-49/draft/tools/round-49/c1-counter.py` on the draft (the frozen counter's `FIXED_PATH` is at `tools/round-49/c1-counter.py:276`, and hard-codes the fnm node-24.21.0 path).
10. **Round-44 values.** The round-44 entry records the v1 `mkfs_time` in host-local time (-0300: 04:18:58 and 04:18:51); the UTC values are 07:18:58Z and 07:18:51Z, as in the table above. The statement that the gzip v3 fixtures are "round-42 C2 held-out inputs" is withdrawn (the round-42 entry does not say it).
