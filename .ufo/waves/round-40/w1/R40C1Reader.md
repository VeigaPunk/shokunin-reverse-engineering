DONE — the round-40 independent reader reads genuine AVM-layout SquashFS v4 (BE fields, little-endian metadata block-length headers) with fragments, gzip/xz and every inode kind, and its regular-file list equals a direct `sasquatch-v4be -f` extraction on V1's AVM-BE member (697/697 files, 0 mismatches) and `sasquatch -f` on the LE member (4709/4709), plus round-11 and K1–K6 (0 mismatches anywhere).

Seat: executor (leaf). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; nothing written outside this report and
`.ufo/waves/round-40/w1/artifacts/R40C1Reader/`. Scratch `/fast/scratch/hyaku/kaidoku-r40/R40C1Reader` removed at exit.
No tool installed or upgraded (system `python3` 3.14.8, existing `sasquatch`/`sasquatch-v4be` 4.5.1, `curl`); no pacman
transaction. No REA and no unblob run: V1 members were read only by pure Python and direct `sasquatch`/`sasquatch-v4be`
(FROZEN-CARRIER DISCIPLINE). No C2 held-out carrier was built or read. Fixture git repos: none created.

## Deliverable

`artifacts/R40C1Reader/sqfs-list.py` (round-40; sha256 `1079fa9b36a87e62b2de8ca594cfc0820e52b3450199076d9d7cc2e870353cd9`,
1428 lines) is a copy of `tools/round-39/sqfs-list.py` (688 lines, sha256 `1808c3f5…8be7f`) extended with:

1. `--layout {auto,le,be,avm}`.
   - `le`: all fields little-endian (`hsqs`).
   - `be`: all fields big-endian (`sqsh`), including metadata headers (round-39 semantics).
   - `avm`: big-endian structural fields; **little-endian 2-byte metadata block-length headers**; data-block size
     lists, fragment index and fragment entries stay big-endian (measured, §"Layout").
   - `auto`: magic decides the structural endianness; for big-endian images the header endianness is chosen by
     `inode_table_start + 2 + len == directory_table_start` when unique, else plausibility `0 < len <= 8192` when
     unique, else by decoding both metadata chains and the whole tree (this also resolves palindromic header bytes
     such as `0x0101`). `--inspect` reports `layout`, `header_endian`, `block_length_signal`, both candidate
     lengths, and endianness evidence for the first data-block list and first fragment entry.
2. Fragments: multi-entry fragment table read with structural endianness (index pointers and 16-byte entries),
   `frag_offset` slices, and per-file block-list + tail handling. Vendor images use 112 fragments; round-11 uses one
   fragment holding all four files.
3. Compression: gzip (id 1) and xz (ids 4 and 2) — .xz container, legacy .lzma, then raw LZMA2 with
   `dict_size = block_size`; any other id exits 2. The vendor members are complete .xz containers.
4. Every inode kind: basic/extended dir, file, symlink, block/char device, fifo, socket (types 1–14), with
   `major:minor` decoded by the inverse of mksquashfs's encoding.
5. Non-regular TSV with a closed `kind` vocabulary and details (link target / `major:minor` / empty), and a 13-case
   `--selftest` whose writer is part of this file (no external tool, no sasquatch/unblob code).

CLI (confirmed to `R40C1Harness` before writing code, unchanged):

```
sqfs-list.py --layout {auto,le,be,avm} --files OUT.tsv [--nonregular OUT.tsv] [--inspect] IMAGE
sqfs-list.py --selftest
files.tsv      relpath \t sha256 \t size          (regular files only, bytewise-sorted)
nonregular.tsv relpath \t kind \t detail          (dir|symlink|block-device|char-device|fifo|socket)
```

Exit 0 success, 2 unreadable/unsupported. `--help` advertises `--layout`, `--files`, `--nonregular` (recorded in
`negative-cases.txt`).

`artifacts/R40C1Reader/compare.py` (stdlib) diffs the two oracle TSVs against an extraction tree: every regular file
by sha256+size, every directory by presence, every symlink by target, every device/fifo/socket by kind and
`major:minor`; a device node the extractor could not create as non-superuser is accepted only when the extractor log
names it.

## Validation (counts; mismatches 0 everywhere)

`artifacts/R40C1Reader/validation-matrix.tsv`; per-image JSON in `inspect/` and `compare/`.

| image | bytes | forced / auto layout | auto signal | files | dirs | links | special | extractor | compare |
|---|---|---|---|---|---|---|---|---|---|
| V1 AVM-BE member `334e56df…` | 5 443 592 | avm / avm | plausibility (le 1380, be 25605) | 697 | 117 | 263 | 1 char | `sasquatch-v4be` (no flag) | match, 697/697 |
| V1 AVM-LE member `7ea4c628…` | 28 200 968 | le / le | plausibility (le 1916, be 31751) | 4709 | 300 | 613 | 1 char | `sasquatch` (no flag) | match, 4709/4709 |
| round-11 `avm-be.squashfs` `c7f74691…` | 4096 | avm / avm | exact (le 116 = dir table) | 4 (all fragment) | 0 | 0 | 0 | `sasquatch-v4be` (no flag) | match, 4/4 |
| K1 `1cfb6c33…` | 9780 | be / be | exact | 5 | 4 | 1 | 0 | `sasquatch-v4be -be` | match, 5/5 |
| K2 `403cb0a8…` | 1606 | be / be | exact | 3 | 5 | 1 | 0 | `sasquatch-v4be -be` | match, 3/3 |
| K3 `9c7c523c…` | 4096 | be / be | exact | 4 | 0 | 0 | 0 | `sasquatch-v4be -be` | match, 4/4 |
| K4 `a29ddc15…` | 307 | be / be | exact | 4 | 0 | 0 | 0 | `sasquatch-v4be -be` | match, 4/4 |
| K5 `5999eafc…` | 26 813 | be / be | exact | 10 | 10 | 3 | 0 | `sasquatch-v4be -be` | match, 10/10 |
| K6 `00152518…` (xz) | 15 867 | be / be | exact | 8 | 9 | 3 | 0 | `sasquatch-v4be -be` | match, 8/8 |

- V1 extraction exit code is 2 only because a non-superuser cannot create `dev/led`; all regular files, directories and
  symlinks were created and compared. That one device is verified from the extractor log
  (`create_inode: could not create character device …/dev/led`). Rows `dev_logged=1` in the matrix.
- K1–K4 carrier bytes live in `corpus/evidence/round-37/c1/` (the round-39 K1–K4 directories carry only receipts);
  K5/K6 in `corpus/evidence/round-39/c1/`. Their round-37/round-39 committed `oracle.tsv` files are byte-identical to
  the new `--files` output (`oracle-tsv-identity.txt`).
- `--layout auto` produced a file list identical to the forced layout on all nine images (`cmp`, exit 0; the runner
  printed nothing on the check).
- `--selftest`: 13/13, exit 0 (`selftest.txt`): le-gzip-basic, be-gzip-basic, avm-gzip-marker, avm-xz,
  avm-raw-lzma2-id2, auto-standard-be, auto-avm, extended-inodes (ldir/lreg/lsymlink/ldev/lipc), fragments-offsets,
  escaping-links, bad-magic, unsupported-compression, truncated. The writer also emits UTF-8 names.
- Timing (with `--inspect`, so every file is hashed; three runs, wall seconds): V1 BE 0.424–0.447, V1 LE 2.577–2.613,
  round-11 0.038–0.041, K1–K6 0.039–0.043 (`timings.txt`).

## Layout measured (feeds the freeze wording)

`layout-facts.md`; `inspect/vendor-be.json`, `inspect/vendor-le.json`, `inspect/r11.json`.

- Genuine AVM layout = BE superblock/inodes/directories with **only the metadata block-length header little-endian**.
  Data-block size lists are **big-endian**, not little-endian: on V1's BE member the first block of
  `usr/sbin/FwUpstreamDocsis2_D.bin` is bytes `00 00 01 90` → BE size 400 → 65 536 bytes decoded; the swapped
  reading (size 65 536) fails xz. First fragment entry: BE `start 96, size 15332` plausible; swapped
  `start 6.9e18, size 3.8e9` implausible.
- Round-11: header LE 116 (= exact identity `121+2+116=239`), fragment entry `10 80 | …60 | 01 00 00 19` = LE header,
  BE start 96 and BE uncompressed-25 size; payload `apple\nbanana\ncherry\ndate\n`.
- The AVM marker (`mkfs_time == bytes_used`) holds on both V1 members and round-11, but it is **not** the layout test:
  the round-39 marker-only standard-BE body (`762c06a6…`) is auto-read as **be**, while the genuine AVM body with the
  marker stripped (`a23ff879…`) is auto-read as **avm** (`negative-cases.txt`). Forcing the wrong layout fails with
  exit 2 and a metadata-length out-of-bounds message (three cases recorded).

V1 provenance chain: URL → image sha256 `f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d`
(39 741 440 B) → member `./var/remote/var/tmp/filesystem.image` at tar offset **32 026 112**, 5 443 592 B, sha256
`334e56dfba6a785590bb5cdbd78fcb5be183b9af160b51fc8935a301ad3f3d4`. LE member at offset 270 848, sha256
`7ea4c628def17c25dc05f6103f8563884022dd1a5baf0c4fba38a85b546a0419`.

## Limits / risks for the L1

- **Wording risk:** if the frozen claims or the round-40 knowledge entry say AVM stores “data block-length headers”
  little-endian, that is false for V1 and round-11. Only the metadata block-length header is LE; block-size lists and
  fragment entries are BE. Cite `layout-facts.md:14-55`.
- The reader is validated only against `sasquatch`/`sasquatch-v4be`; no REA/unblob run was allowed on carriers, so the
  REA-specific gap/publish behaviour is untested here (it is C1's scoring surface, not the oracle's).
- Multi-page fragment tables (>512 entries) are not exercised by any available image (V1 has 112); the inherited
  page-index code is unchanged. Sparse blocks, ID/xattr/export tables are not exercised or parsed (not needed for
  file listing).
- `auto` uses plausibility when the inode table spans blocks; on much larger/multi-block images a decompression-valid
  wrong-endian header can theoretically be plausible, but the decode fallback then decides. V1 forced the plausibility
  branch and resolved correctly.
- Device `major:minor` follows the new-encoding formula in the pinned sasquatch source (`mksquashfs.c:1055`); it is
  exercised only by synthetic inodes (V1's single device was not created on disk) and verified by the extractor log.

## Artifact inventory (all under `artifacts/R40C1Reader/`)

```
sqfs-list.py              1079fa9b36a87e62b2de8ca594cfc0820e52b3450199076d9d7cc2e870353cd9
compare.py                ff91c7031b9929c82ea6b8b201501ef00367e2b8789284ae81c311e7bb5f1cc6
selftest.txt              13/13 passed
validation-matrix.tsv     nine images, headers and compare verdicts
inspect/{9 carriers}.json + marker-only, standard-be-fresh, avm-markerstripped
compare/{9 carriers}.json verdict=match, mismatches 0
layout-facts.md           endianness evidence (offsets, block list, fragment entry)
negative-cases.txt        --help and forced/auto discriminator runs
oracle-tsv-identity.txt   cmp against committed round-37/39 oracle.tsv
timings.txt               three runs per image
commands.txt              exact commands (download, carve, extract, oracle, compare)
checksums.txt             sha256 of every artifact file
```

`inspect/*.json` keeps the scratch `image` path as the reader received it; that path was removed at exit and is not
evidence — identify each image by the `sha256` column in `validation-matrix.tsv` (or the hashes in this report).

No changes were made to `corpus/`, `tools/`, `plans/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md` or
`LOG.md`; nothing committed; the L1 owns integration. Tool code for the freeze (`tools/round-40/sqfs-list.py`) is this
file; the L1 should copy it and re-run `--selftest` plus the nine-image loop in `commands.txt`.
