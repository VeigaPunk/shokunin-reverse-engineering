# R44SrcOracle — S138 opened (unblob `__output__` oracle trees), S139 drafted, draft attacked

Seat `R44SrcOracle` (source/oracle). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Claim base `c29360e3ba5381a5ab69e372d0d9577970f85018`; HEAD at seat start
`fc5eb54a2b79faee82866a27b40c8c2f1767b1eb`; the lane advanced to `9a8de923` while this seat ran
(§7). Scratch `/fast/scratch/hyaku/kaidoku-r44/probe-R44SrcOracle/`; `TMPDIR` and `HYAKU_SCRATCH` were
unset in this shell, so two captured commands also wrote regenerable temp files under `/tmp`
(`/tmp/probe-R44SrcOracle-tree.tsv`, `/tmp/r44_unblob_sqfs.json`). No fleet-root tracked file, no
`~/.local/bin`, no `tools/round-44/` path was written.

**Not done by this seat, by contract:** no `tools/round-44/c1-run.sh`, no REA 6.5.0 invocation,
no edit under `tools/round-44/`, no commit, no write outside the lane tree / my scratch / `/tmp`.

## 1. What S138 is (and what its directory names actually are)

The seat brief names the four targets `v1-little_endian`, `v1-big_endian`, `v2-little_endian`,
`v2-big_endian`. Those names do not exist. The contents API over
`tests/integration/filesystem/squashfs` at tag `26.6.4` (commit
`1fcc7a0a584a70a96c31f5a276c20944d199a089`, `git ls-remote` verified) returns:

| fixture dir | endian dirs present | `__output__` trees |
|---|---|---|
| `squashfs_v1` | `little_endian`, `big_endian` | `squashfs_v1.0_le.bin_extract`, `squashfs_v1.0_be.bin_extract` |
| `squashfs_v2` | `little_endian`, `big_endian` | `squashfs_v2.0_{le,be}.bin_extract`, **`squashfs_v2.1_{le,be}.bin_extract`** |

The four trees the brief asks for are `squashfs_v1/{little,big}_endian/__output__` and
`squashfs_v2/{little,big}_endian/__output__`; each `__output__` holds one directory per
`__input__` binary, and v2 has **two** binaries per byte order (2.0 and 2.1). Every member was
fetched, so the v2.1 trees are included.

## 2. Fetch result

| item | value |
|---|---|
| listings | 10 contents-API calls, all HTTP 200 (receipts in `R44SrcOracle/listings/`) |
| member files | **22** (v1: 3 per byte order; v2: 4 per binary × 4 binaries) |
| total bytes | **152** (v1 `apple.txt` 6 B, `banana.txt`/`cherry.txt` 7 B; v2 `apple{1..4}.txt` 7 B each) |
| distinct content sha256 | **7** |
| failures | **0** |
| destination | `corpus/evidence/round-44/oracle/<arch>/<endian>/__output__/<bin>_extract/<member>` + `manifest.json` at the tree root |
| tree digest | `21cb3a6ab67af507f6b4ccaff15d1990567550355a7a4c21ef4111b9efd660ca` over the 22 sorted `sha256  path` lines (`R44SrcOracle/oracle-tree.tsv`) |

### 2.1 Custody: the committed objects are git-LFS pointers

Every `__input__` and `__output__` object in that tree is LFS-tracked. The contents API reports
`size: 126, sha: fb25b544…` for `…/squashfs_v1.0_le.bin_extract/apple.txt`; the committed object is

```
version https://git-lfs.github.com/spec/v1
oid sha256:303980bcb9e9e6cdec515230791af8b0ab1aaa244b58a8d99152673aa22197d0
size 6
```

and `media.githubusercontent.com/media/…` serves the 6-byte `apple\n`. Verification performed for
**all 22** members, both directions:

- `pointer_git_blob_sha1 == committed_entry_sha` (the served member really is the object the
  listing points at), and
- `lfs_oid == sha256(served bytes)` and `lfs_size == len(served bytes)`.

Manifest records `path, repo_path, url, fetched_at, http_status, wall_s, bytes, sha256,
committed_entry_sha, committed_entry_size, local_path, pointer_url, pointer_bytes,
pointer_git_blob_sha1, pointer_sha256, pointer_git_blob_sha1_matches_committed_entry,
lfs_resolved, lfs_pointer_text, lfs_oid, lfs_size, lfs_oid_matches_content,
lfs_size_matches_content` per file. **The member's content address is the LFS `oid sha256`, not the
git blob sha** — S138's anchor says so for this reason.

Determinism: the tree was fetched twice independently (`fetch-run2` receipt vs the run-1 snapshot
`manifest.fetch-run1.json` + `digests.run1.tsv`); `{path, bytes, sha256}` identical for 22/22,
0 failures.

### 2.2 API budget

The unauthenticated contents API is 60 requests/hour per IP and this host is shared; the quota was
exhausted after the 10 listings. The listings were therefore **replayed** from their saved receipts
(`--from-saved-listings`) rather than re-requested — each replay record keeps its original
`fetched_at` and sets `replayed_from_saved_receipt: true`, and the 10 listing bodies are the
HTTP-200 receipts on disk. `media.githubusercontent.com` (member bytes) and
`raw.githubusercontent.com` (pointer bytes) are not quota-limited and were called live.

## 3. Second oracle vs first oracle — they agree exactly

`/usr/bin/unsquashfs` 4.7.5 extracts all six frozen carriers
(`tools/round-44/carriers.json` at `9a8de923`), and its extraction tree is path-for-path,
sha256-for-sha256 identical to the fetched `__output__` tree:

```
oracle: unsquashfs version 4.7.5 (2026/03/01) (exit 1)
carriers: 6 from tools/round-44/carriers.json
MATCH v1le squashfs_v1/le rc=0 members=3 expected_regular=3
MATCH v1be squashfs_v1/be rc=0 members=3 expected_regular=3
MATCH v2le squashfs_v2/le rc=0 members=4 expected_regular=4
MATCH v2be squashfs_v2/be rc=0 members=4 expected_regular=4
MATCH v21le squashfs_v2/le rc=0 members=4 expected_regular=4
MATCH v21be squashfs_v2/be rc=0 members=4 expected_regular=4
cross_oracle_failed_carriers=0
```

`unsquashfs -lls` census (receipt `carriers-file-and-unsquashfs-lls`), for the record:

| carrier | `file(1)` version/endian | members (`-lls`) |
|---|---|---|
| v1-le | 1.0 le | `squashfs-root/{apple 6, banana 7, cherry 7}` |
| v1-be | 1.0 be | same three names and sizes |
| v2-le | 2.0 le | `apple1..4` 7 B each |
| v2-be | 2.0 be | `apple1..4` 7 B each |

## 4. SOURCES row S138 (paste as-is)

| S138 | unblob 26.6.4 SquashFS `__output__` expected trees — https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs (member base https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/; commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`) | dataset | A | The second, cross-checking oracle for the R44-C1 carriers: unblob 26.6.4's committed expected member trees for `squashfs_v1` and `squashfs_v2`, both byte orders, as content-addressed member bytes (4 endian trees, 22 files); **not** handler code, **not** extractor behaviour, **not** a C1 carrier | `LICENSE:5-8` "Permission is hereby granted, free of charge, to any person obtaining a copy … to deal in the Software without restriction" (already fetched and quoted in S135; the fixture bytes this row grounds are the same MIT-licensed corpus); `squashfs_v1/little_endian/__output__/squashfs_v1.0_le.bin_extract/apple.txt` = 6 B `apple\n`, LFS `oid sha256 303980bcb9e9e6cdec515230791af8b0ab1aaa244b58a8d99152673aa22197d0`; 10 contents-API listings, all HTTP 200, saved as receipts; 22 members / 152 B / 7 distinct sha256; every member's pointer blob sha1 equals the listing's `sha` and every `oid sha256` equals the served bytes; sorted tree digest `21cb3a6ab67af507f6b4ccaff15d1990567550355a7a4c21ef4111b9efd660ca` (2026-10-28) | An expected tree written by the same project that writes the handler is a *second* oracle only when its member bytes are compared against a different producer: here `unsquashfs` 4.7.5 extracts all six frozen carriers to exactly this tree, so a receipt can be checked without trusting either reader alone; pin the LFS `oid sha256`, never the 126-byte pointer's blob sha | mined | 2026-10-28 | 180d | corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md |

## 5. SOURCES row S139 (draft)

| S139 | squashfs-tools 4.7.5 release — https://github.com/plougher/squashfs-tools/releases (tag https://github.com/plougher/squashfs-tools/releases/tag/4.7.5; machine-readable feed https://api.github.com/repos/plougher/squashfs-tools/releases) | docs | A | The upstream release identity of the independent oracle binary `/usr/bin/unsquashfs`: that 4.7.5 is a published squashfs-tools release (`tag_name 4.7.5`, `name "Squashfs tools 4.7.5"`, `published_at 2026-03-01T23:05:47Z`; annotated tag object `1fdc2fe01d681438a04e2a137a9f51d829ba3358`, peeled commit `708c59ae80853b0845017c33b42e56061cc546cd`) and that the installed binary reports the same version; not the source code, not any carrier, not the behaviour of any image | page HTTP 200, 398943 B, sha256 `d08749f4b9cdcf2a01cd1d4e472b77e0372a9107aa720bf683f8383b644dbd93`; tag links present and distinct: 4.5.1, 4.6, 4.6.1, 4.7, 4.7.1, 4.7.2, 4.7.3, 4.7.4, 4.7.5 (9); `/usr/bin/unsquashfs --version` → `unsquashfs version 4.7.5 (2026/03/01)` (**exits 1** while printing); page bytes are mutable (398940 B and 398943 B on two fetches), so the tag set and `published_at` are the recheck pin, not the page digest | Read an oracle's identity from the release that carries the version *and* from the binary's own version line: `unsquashfs --version` exits 1 by design, so a gate that tests the exit code rejects a correct oracle; a rendered release page carries tag names, not asset facts | mined | 2026-10-28 | on-release | corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md |

Machine-readable copy of both rows: `R44SrcOracle/sources-rows.md`.

## 6. Attack on the draft (pre-freeze findings)

### F1 — BLOCKING: the frozen `superblock_layout` is the v4 layout wearing a v1/v2 label

`tools/round-44/carriers.json` (committed `3b0fcaa9`, unchanged at `9a8de923`) freezes:

```json
"superblock_layout": {
  "compression_offset": 20, "compression_len": 2,
  "s_major_offset": 28, "s_major_len": 2,
  "s_minor_offset": 30, "s_minor_len": 2,
  "bytes_used_offset": 40, "bytes_used_len": 8,
  "note": "v1/v2 superblock field offsets per unblob squashfs.py v1/v2 classes; verify against file output"
}
```

Both offsets are the **v4** layout, and there is no v1/v2 compression field to point at:

- squashfs-tools 4.7.5 `squashfs-tools/squashfs_fs.h:294-311` (v4): `… fragments; u16 compression; u16 block_log; u16 flags; u16 no_ids; u16 s_major; u16 s_minor; u64 root_inode; s64 bytes_used; …`
  → `compression` at 20, `bytes_used` at 40. These are exactly the frozen numbers.
- unblob 26.6.4 `python/unblob/handlers/filesystem/squashfs.py:124-140` (`SquashFSv1Handler.C_DEFINITIONS`, which `SquashFSv2Handler` inherits): `char s_magic[4]; u32 inodes; u32 bytes_used; u32 uid_start; u32 guid_start; u32 inode_table_start; u32 directory_table_start; u16 s_major; u16 s_minor;`
  → **no compression member at all**, and `bytes_used` at **8** (`u32`), not 40.
- squashfs-tools 4.7.5 `squashfs-tools/squashfs_compat.h:38-64` (`struct squashfs_super_block_3`, `__attribute__((packed))`) agrees field-for-field with unblob for 0-31 and continues with `block_size_1:16, block_log:16, flags:8, no_uids:8, no_guids:8, i32 mkfs_time, root_inode`.

A probe reading the frozen offsets on the real bytes (all six carriers):

| carrier | `u16@20` (frozen "compression") | `u64@40` (frozen "bytes_used") | true `bytes_used` (`u32@8`) |
|---|---|---|---|
| v1le | 0x0047 = 71 | 862367868 | 176 |
| v1be | 0x0000 = 0 | (mkfs_time/root_inode bytes) | 177 |
| v2le | 0x0058 = 88 | — | 196 |
| v2be | 0x0000 = 0 | — | 201 |
| v2.1le | 0x0058 = 88 | — | 196 |
| v2.1be | 0x0000 = 0 | — | 201 |

So a counter that binds `compression` through the frozen offsets cannot ever see `gzip`, and its
`bytes_used` binding fails on every carrier. The frozen note tells the implementer to *"verify
against file output"* — which cannot catch this, because `file(1)` derives its own
compressed/uncompressed token from byte 20 (F2) and prints a signed 16-bit "blocksize" for v1 (F4).
**Repair before the freeze:** drop `compression` from the v1/v2 superblock binding (there is no
such field; if a compression fact is wanted it must be `flags` bit `SQUASHFS_NOD` clear, or the
presence of a `0x78da`/zlib stream), set `bytes_used` to offset 8 / len 4, and replace the note
with "verify against `unsquashfs -s`", never `file`.

Authoritative confirmed fields for a correct probe (all six carriers matched `unsquashfs -s`
field-for-field, receipt `superblock-legacy-probe`): magic `0..3`; `s_major` u16@28; `s_minor`
u16@30; `block_size_1` u16@32; `block_log` u16@34; `flags` u8@36; `no_uids` u8@37; `no_guids`
u8@38; `mkfs_time` i32@39 (packed, unaligned). `block_size` = `block_size_1` when non-zero else
`1 << block_log` — v1 has 32768/15, **v2 has `block_size_1 = 0` and `block_log = 16`**, so a plain
u16@32 blocksize read returns 0 on v2.

### F2 — the draft's "v2be is uncompressed" is false, and the error is in the oracle, not the image

Draft text: *"`v2be` is uncompressed (measured 2026-10-28: `file` reports 'version 2.0,
uncompressed'); that is an oracle property, not a counter assumption."*

`v2be`'s data is compressed:

- superblock `flags = 0x40` → `SQUASHFS_NOD` (bit 1, "uncompressed data") is **clear**; bit 6
  (`SQUASHFS_DUPLICATE`) is the only set bit (`squashfs_fs.h:64-79`);
- `/usr/bin/unsquashfs -s` on the same bytes: *"Data is compressed"*, *"Fragments are compressed"*;
- zlib streams `0x78da` are present in the image body.

`file(1)`'s token is an endianness artefact. Controlled flip on copies of `v2-be` (receipt
`file-token-flip`): changing **byte 36** (the real legacy `flags` word) does not move the token;
changing **byte 20** does (`0x00 → "uncompressed"`, `0x01 → "compressed"`). Byte 20 is the low
byte of legacy `inode_table_start` in LE images and its high (zero) byte in BE images — the slot
`file` uses for the v4 `compression` field. Hence both BE legacy carriers print "uncompressed".
**The clause must be replaced**, e.g. "`v2be` is big-endian with gzip/zlib-compressed data
(superblock flags `SQUASHFS_NOD` clear; `unsquashfs -s` reports data compressed); `file(1)` prints
'uncompressed' for both BE legacy images because its token reads byte 20 — a `file` artefact, not
an image property." The same clause is already forwarded into the wave-2 critic checklist
(`R44ScoutSEAT.md:102`, "v2be-uncompressed disclosure"), so it needs correcting in both places.

### F3 — `unsquashfs --version` exits 1

Receipt `oracle-unsquashfs-version`: `exit=1`, stdout `unsquashfs version 4.7.5 (2026/03/01)`.
An oracle-identity gate must parse the version line from output; using the exit code would reject a
correct oracle, and `2`/`1` semantics in this lane would then mis-read as "could-not-evaluate".

### F4 — `file(1)` blocksize for v1 is `-32768`

`file` prints `blocksize: -32768 bytes` for both v1 carriers (signed 16-bit widthing of 0x8000) and
`65536` for v2. Do not bind blocksize from `file`, and do not bind it from u16@32 alone (0 for v2).

### F5 — pin the LFS oid, not the git blob sha

The committed `__output__` objects are 126-byte pointers; `committed_entry_sha`
(`fb25b544…` for `apple.txt`) is the pointer's blob sha, not the member's. S138's anchor and the
counter's oracle tree must be content-addressed by `oid sha256` (`303980bc…` for `apple.txt`).

### F6 — the seat brief's directory names do not exist

`v1-little_endian`, `v1-big_endian`, `v2-little_endian`, `v2-big_endian` are not paths in the
dataset; the real ones are `squashfs_v1/{little,big}_endian` and `squashfs_v2/{little,big}_endian`
(§1). Anyone pinning the brief's spelling would 404. (Same defect class as the round-44
`stale-premise` mistake note: pin a URL only after a successful open.)

### F7 — non-blocking observations

- unblob's `squashfs_v2` pattern checks magic + `s_major` only (`… 68 73 [24] 02 00` for LE), so a
  `2.1` image (`s_minor = 1`) legitimately binds to `squashfs_v2`; `carriers.json`'s `s_minor: 1`
  rows are correct. A counter must not require `s_minor == 0` for the v2 family.
- The v2.1 `__output__` trees are byte-identical to the v2.0 ones (same 7 sha256 values), and the
  images differ from their 2.0 twins in exactly **2 bytes**: `s_minor` (offset 30 LE / 31 BE) and
  `mkfs_time` (offset 39/42). So v2.1 adds a superblock-discriminated carrier, not new member
  content; the 6-carrier set carries 4 distinct member trees.
- `expected_regular` = 3/3/4/4/4/4 matches the trees and the `-lls` census.

## 7. Lane movement during this seat

Start of seat: HEAD `fc5eb54a` (draft claims). By the end: HEAD `9a8de923`, with the L1 having
committed the oracle tree during the run — `3b0fcaa9` "frozen carriers.json + unblob `__output__`
oracle trees (S138 bytes, real LFS content)" (24 files: 22 members + `manifest.json` +
`carriers.json`) and `f18bdfb9` "add v2.1 LE/BE carriers (squashfs_v2 handler) — 6 carriers total".
The committed `manifest.json` blob equals the byte-identical file this seat wrote, so the tree in
the repo is this fetch, not a look-alike. `c29360e3` remains an ancestor of HEAD.
`corpus/SOURCES.md` has **no** S138/S139 row yet (`grep -n 'S13[89]'` empty) — §4/§5 are still
needed.

## 8. Receipts

All under `.ufo/waves/round-44/w1/R44SrcOracle/receipts/`: seat name, argv, cwd, started/finished
UTC, wall, exit, stdout bytes + sha256, stderr bytes + sha256, stdout/stderr files.

| receipt | exit | wall s | stdout sha256 (16) | note |
|---|---|---|---|---|
| `fetch-run2` | 0 | 0.568 | `ec87687d10a939e4` | second independent fetch of the 22 members (replayed listings) |
| `determinism-run1-vs-run2` | 0 | 0.014 | `a85e874118fb477b` | 22/22 identical, 0 failures |
| `oracle-tree-inventory` | 0 | 0.042 | `b953109425d97259` | 22 members, 152 B, 7 distinct, tree digest |
| `oracle-unsquashfs-version` | 1 | 0.001 | `6154c39eee941fa6` | 4.7.5 (2026/03/01); **exit 1 is the tool's** |
| `carriers-file-and-unsquashfs-lls` | 0 | 0.063 | `119c16a54ce701c2` | `file` + `-lls` census, 4 carriers |
| `cross-oracle-digests` | 0 | 0.091 | `dc0336ff2f6bec4d` | 4-carrier form (superseded) |
| `cross-oracle-digests-all6` | 0 | 0.039 | `d2f7e5db1540c4e7` | 6 carriers from `carriers.json`, 0 failed |
| `superblock-probe` | 0 | 0.008 | `456335ee2e372e47` | **negative**: v4 offsets on v1/v2 (evidence for F1) |
| `superblock-legacy-probe` | 0 | 0.008 | `36d52bcbf8448bd4` | legacy layout, 6/6 match `unsquashfs -s` |
| `file-token-flip` | 0 | 0.019 | `38a5d57726ce72d9` | byte-20 controlled flip (F2) |
| `s139-releases-page` | 0 | 0.805 | `86434136a661083f` | page 200, 398943 B, 9 tag links |
| `s139-releases-feed` | 0 | 0.491 | `8dba917cb486483b` | 9 releases, 4.7.5 @ 2026-03-01T23:05:47Z |

Listing receipts (`R44SrcOracle/listings/`, 10 files) carry API URL, `repo_path`, `fetched_at`,
HTTP status, body bytes, body sha256, wall, and the entry list (`type, name, size, sha`).
`R44SrcOracle/manifest.fetch-run1.json` + `digests.run1.tsv` are the run-1 snapshot the determinism
check compares against; `R44SrcOracle/oracle-tree.tsv` is the digest input.

## 9. Artifacts (L1 installs; nothing was written under `tools/round-44/`)

`.ufo/waves/round-44/w1/artifacts/R44SrcOracle/`

| file | sha256 | purpose |
|---|---|---|
| `fetch-oracle.py` | `513ba477e0f2be93…` | fetch driver: contents-API listing (+`--from-saved-listings` replay), media member fetch, raw pointer verification, manifest |
| `cross-oracle.py` | `c4a292889530da04…` | reads `tools/round-44/carriers.json`, extracts each carrier with `unsquashfs`, compares to its `output_tree` |
| `superblock-probe-legacy.py` | `0ededa5a0f99c36f…` | authoritative legacy 1.x/2.x read, cross-checked against `unsquashfs -s` |
| `superblock-probe-v4-layout-NEGATIVE.py` | `2fb09175d522c7c8…` | the v4-offset read, kept as the F1 counter-example |
| `determinism.py` | `4b72b3c75c02d699…` | run-1 vs run-2 member digest comparison |
| `capture-receipt.py` | `7924a4f9082bd570…` | receipt harness used for every row in §8 |

Fetched oracle tree: `corpus/evidence/round-44/oracle/` (22 members + `manifest.json`); members
live only under `<arch>/<endian>/__output__/<bin>_extract/`, so a counter walking the oracle must
scope to `*/__output__/*_extract/**` and treat `manifest.json` as metadata.

## 10. Out of scope / limits

- No REA run, no `c1-run.sh`, no C1 receipt produced: the after-side data procedure is the L1's.
- No claim about what unblob's handler *does* with these images (S138 explicitly is not handler
  behaviour); the handler-source reads in F1/F7 are defect diagnosis, not S138 scope.
- The fetch is 22 six-to-seven-byte members: it is a thin oracle, sufficient to cross-check the
  four frozen carriers' member sets, not to characterise SquashFS v1/v2.
- The core-API listings could not be re-requested after the quota ran out; the listing receipts are
  the 200 bodies from the first pass, and member bytes were fetched live from the non-quota
  endpoints. A reviewer re-running `fetch-oracle.py` without `--from-saved-listings` needs quota.
- `superblock-probe.json` (the v4-offset read) is kept intentionally as evidence for F1; it is
  superseded by `superblock-legacy-probe.json` and must not be cited as a field validation.
