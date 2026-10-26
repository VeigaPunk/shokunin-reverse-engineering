# R41C1VendorV4 — carrier V4 (FRITZ!Box 5491 07.31): provenance, oracle, budget decision

**Verdict: DONE.** V4 is decided as the **nested `filesystem_core.squashfs` of
`FRITZ.Box_5491-07.31.image`**, carved `[0, bytes_used)`: it is genuine AVM-BE (`sqsh` magic,
`mkfs_time == bytes_used = 32720860`, little-endian metadata block-length headers) with 7367 staging
entries against REA 6.5.0's 10000-entry budget at `--max-depth 1` (and 110,187,475 regular-file bytes
against 256 MiB). Carrier pin `ce27ebca903a1574465ddfa0626943339ce6bc8155f31f88d04049afb570087f`.
Oracle: 6349 regular files + 1017 non-regular entries, cross-checked against a direct
`sasquatch-v4be` (no `-be`) extraction with **0 mismatches**. No REA and no unblob run touched the
reserved image, the member or the carved bytes (seat rule); only `sqfs-list.py` reads and a direct
`sasquatch-v4be` listing/extraction were used, exactly as the item allows.

All paths below are lane-relative; artifacts are in
`.ufo/waves/round-41/w1/artifacts/R41C1VendorV4/`.

## 1. Chain (image sha → member sha → nested sha → carve sha)

| step | value |
|---|---|
| URL | `https://download.avm.de/fritzbox/fritzbox-5491/other/fritz.os/FRITZ.Box_5491-07.31.image` |
| image | 36,392,960 B, sha256 `a5a3a763a615c2dab226d15463bc05fbc74e844736687fa5cc87a91d2f35f661` (matches the assignment pin) |
| member | `./var/tmp/filesystem.image`, 33,361,928 B, sha256 `4cfc3016d84cccf4982d6a4c50935f1771ad350994f569496e91e42be3d92f6c` |
| nested | `filesystem_core.squashfs` (in the member's root, name confirmed by both readers), 32,722,944 B, sha256 `4d5de25c7bee7ae9206ae1882a66abe6c694ce19bcb4d568fa235fb30c7ad947` |
| carve | `[0, bytes_used) = [0, 32720860)`, 32,720,860 B, sha256 `ce27ebca903a1574465ddfa0626943339ce6bc8155f31f88d04049afb570087f` |

Commands (scratch, exit 0 each):

```
curl -sSL -o fritz5491.image https://download.avm.de/fritzbox/fritzbox-5491/other/fritz.os/FRITZ.Box_5491-07.31.image
sha256sum fritz5491.image            # a5a3a763…f35f661
tar xf fritz5491.image ./var/tmp/filesystem.image ./var/info.txt ./var/version ./var/content
sha256sum var/tmp/filesystem.image   # 4cfc3016…b3d92f6c
python3 -I -- tools/round-40/sqfs-list.py --layout avm --files member-files.tsv \
        --nonregular member-nonregular.tsv --inspect var/tmp/filesystem.image   # exit 0
#   -> filesystem_core.squashfs 4d5de25c…c7ad947 32722944
sasquatch-v4be -no-progress -d member-x var/tmp/filesystem.image               # exit 0
sha256sum member-x/filesystem_core.squashfs                                    # 4d5de25c…c7ad947
head -c 32720860 member-x/filesystem_core.squashfs > V4.carrier
sha256sum V4.carrier                                                           # ce27ebca…570087f
```

The tar member set is `./var/install`, `./var/info.txt`, `./var/tmp/kernel.image`,
`./var/tmp/filesystem.image`, `./var/version`, `./var/install-features`, `./var/content`,
`./var/chksum`, `./var/signature` (plus `./var`, `./var/tmp`). Vendor bytes are **not** copied into
the lane; the pins above are the committed form.

`carriers-V4.json` is the carriers.json fragment, with the new nested step expressed as
`external.nested: {"path": "filesystem_core.squashfs", "sha256": "4d5de25c…"}` and
`external.length: 32720860` (the carve length). `provenance.json` carries the same chain plus the
identity block.

## 2. Superblock and layout split (measured, both candidates)

Big-endian decode of the carved V4 superblock (`>[IIIIIHHHHHHQQQQQQQQ]`, offsets 0..96):

| field | value | field | value |
|---|---|---|---|
| magic | `sqsh` (0x73717368) | root_inode | 3565160933 (0xd48009e5) |
| inodes | 7367 | bytes_used | 32720860 |
| mkfs_time | **32720860** (== bytes_used) | id_table_start | 32720852 |
| block_size | 65536 (block_log 16) | xattr_id_table_start | 0xffffffffffffffff |
| fragments | 334 | inode_table_start | 32578020 |
| compression | 4 (xz) | directory_table_start | 32633150 |
| flags / no_ids | 704 / 1 | fragment_table_start | 32706630 |
| s_major / s_minor | 4 / 0 | lookup_table_start | 32720782 |

Little-endian control decode of the same 96 bytes is nonsense (`inodes` 3340500992, `block_size` 256,
`bytes_used` 15872922597311119360, marker false) — the structural half is big-endian, as claimed.
`sqfs-list.py --layout avm --inspect` reports `layout: avm`, `endian: big`,
`header_endian: little`, `block_length_signal: layout-avm`, `avm_marker: true`.

The **wrapper member** is also genuine AVM-BE: `layout avm`, marker true
(`mkfs_time == bytes_used == 33358398`), 104 inodes (9 dirs + 8 regular files + 85 symlinks + 1 char
device + root), xz, block_size 65536, 8 regular-file bytes 34,352,352.

## 3. Chain walk (LE headers threading a BE image)

`artifacts/R41C1VendorV4/chain-walk.py V4.carrier` → exit 0, `all_boundaries_close: true`,
`errors: []` (`chain-walk.json`). Every metadata boundary is closed exactly:

| chain | range | result |
|---|---|---|
| inode metadata (LE 2-byte headers) | 32578020 → 32633150 | 31 blocks, 55,068 compressed / 248,325 decompressed, **lands exactly** on `directory_table_start`; big-endian control length 26631 (> 8192, implausible) |
| directory + fragment metadata (LE headers) | 32633150 → 32706630 | 24 blocks (23 directory + 1 fragment block starting exactly at the fragment index's block pointer 32704584), 73,432 compressed, **lands exactly** on `fragment_table_start`; BE control length 19466 (implausible) |
| fragment index (BE u64) | at 32706630 → block 32704584 | LE header 2044 → 5344 B, block ends exactly at 32706630; first fragment entry **BE** `start_block=96, size=14036` plausible, LE control `size=3560308736` implausible |
| lookup index (BE u64 array) | at 32720782, 64 B (8×ceil(7367/1024)) | 8 LE-framed blocks from 32706638, 58,936 decompressed, **ends exactly** on `lookup_table_start`; first inode refs BE `0x00000000d48009c5 …` |
| id metadata + id index (BE u64) | block 32720846, index at 32720852 | block ends at `id_table_start`; id index 8 B ends at `bytes_used` (32720860) |

**Layout wording correction (measured, matters for the freeze).** The split is: structural
superblock/inode/directory/fragment/block-list fields **big-endian**, the 2-byte *metadata*
block-length header **little-endian**. The data block-length list is **not** little-endian: the
reader's data-block evidence on this carrier reads the structural (BE) field `00005428` = 21544 and
xz-decodes it to a full 65536 block, while the swapped reading `28540000` = 5,505,024 is
size-implausible; the sasquatch-v4be extraction of all 6349 files with matching sha256 confirms it
(sasquatch's `-be` flag swaps only metadata headers; S121 lines 664-669, 4390-4394). The same split is
what `tools/round-40/sqfs-list.py` documents (§3 of its docstring: "list entries are big-endian even
when the metadata headers are little-endian"). The draft's "LE metadata/data block-length headers"
should become "LE metadata block-length headers; BE inode block-list entries" before it freezes.

## 4. Oracle tables and independent cross-check

`artifacts/R41C1VendorV4/r41-oracle-run.sh V4.carrier .ufo/waves/round-41/w1/artifacts/R41C1VendorV4 work`
→ exit 0, 4.0 s. Producer 1 = `python3 -I tools/round-40/sqfs-list.py --layout avm --files oracle.tsv
--nonregular nonregular.tsv --inspect V4.carrier` (reader sha256 `1079fa9b…353cd9`, the frozen round-40
reader). Producer 2 = `sasquatch-v4be -f -no-exit-code -n -d <scratch>/root V4.carrier`
(`/home/vgpnk/.local/bin/sasquatch-v4be`, sha256 `fac88740…1b7214c6`, `unsquashfs version 4.5.1
(2022/03/17)`, exit 0; its log prints the expected "different endianess" attempt then "Successfully
decompressed with default xz decompressor").

| table | rows | bytes | sha256 |
|---|---|---|---|
| `oracle.tsv` (relpath, sha256, size) | 6349 | 719,304 | `3ab10e12320f678f556c306a1a00d540ac12d26f54b5b46f141121867f0742d6` |
| `nonregular.tsv` (relpath, kind, detail) | 1017 | 43,647 | `eea97c809a4d84d0b02d6fb943f13ea3e3afa0ed2e73db9f63974fd5cc27560d` |
| `oracle-check.tsv` (sasquatch producer) | 6349 | 719,304 | `3ab10e12…f0742d6` (identical) |

Cross-check verdict in `oracle-run.json`: `files_equal: true`, `check_files: 6349`,
`check_symlinks: 615`, `mismatch_count: 0`, `mismatches: []`. Oracle paths are **rootfs-relative**
(the nested core's extraction root is the rootfs itself: `bin/…`, `etc/…`, `usr/…`).

Kind census (non-regular): `dir` 401, `symlink` 615 (104 absolute targets, 511 relative), `char-device`
1 (`dev/led`, 247:0). The independent `sasquatch-v4be` extraction of the same bytes ends with
`created 6349 files / created 402 directories / created 615 symlinks / created 0 devices (unprivileged
cannot create the char node) / created 0 fifos / created 0 sockets / created 0 hardlinks`, so the
squashfs has no fifos, sockets or hardlinks. Regular-file bytes total **110,187,475** (105.08 MiB).
Notable members: `bin/busybox` (631,572 B, sha `936ea8fb…`), `var.tar` (30,720 B), a `wrapper/`
directory.

## 5. Collision census (R40-CL1 surface)

| set | symlink path that is a component-suffix of a regular path | regular path that is a component-suffix of a symlink path | exact path in both |
|---|---|---|---|
| V4 nested core | **0** | **0** | **0** |
| V4 wrapper member | 0 | 0 | 0 |

The census is the R40-CL1 shape (regular `usr/bin/busy` vs symlink `bin/busy`) computed on
component boundaries; a synthetic positive control returns
`[('bin/busy', 'usr/bin/busybox', ['usr/bin/busy'])]`, i.e. the check does fire on the round-40 defect
shape. **Consequence for the freeze:** V4 cannot exercise the exact-relative fix by itself; the
both-direction collisions the draft promises exist only in L3/L4, which is consistent with the draft
but should be stated in the freeze so V4 is not credited with covering R40-CL1. Symlink targets:
511 relative (56 `busybox`, 51 `../../bin/busybox`, 15 `../bin/busybox`, …), 104 absolute
(`/usr/www/cgi-bin/*`, `/var/*`, `/dev/null`); 501 targets resolve to a regular file, 114 dangle into
runtime-only paths (`/var/...`, `/tmp/log`) — normal for this rootfs.

## 6. REA 6.5.0 entry budget and the V4 decision

Budget constants (found in the installed package, version `6.5.0`):

- **`max_output_files` default 10000** (`min(1).max(100_000)`), described as the **"Staging entry
  budget, including directories and links"** —
  `dist/domain/firmware/firmwareAnalysis.js:42-46` (same default in
  `dist/cli-runtime/cutterToolContracts-TZH9EHr5.js:1763`). What it counts:
  `inventoryFirmwareOutput` (`dist/firmware/FirmwareFiles.js:121-180`) walks REA's **staging root**
  recursively without following symlinks and increments the counter once per **directory-entry name**
  (line 151-153), so regular files, symlinks, directories and special files each count once and
  directories are descended (their names counted, not their contents twice).
- **`max_output_bytes` default 256 MiB** (`268435456`) — same schema (lines 35-41); it adds
  `stat.size` for **regular files only** (lines 172-174).

| candidate | entries (chunk dir + names) | entry headroom | regular-file bytes | byte headroom | fits depth 1 | AVM-BE |
|---|---|---|---|---|---|---|
| **nested core** (chosen) | 1 + (401+6349+615+1) = **7367** | 2633 | 110,187,475 | 158,247,981 | yes | yes (marker holds) |
| wrapper member (fallback) | 1 + (9+8+85+1) = **104** | 9896 | 34,352,352 | 234,083,104 | yes | yes (marker holds) |

Decision rule as assigned: *nested core IF AVM-BE **and** its entry count fits REA's budget at
`--max-depth 1`; else the wrapper member.* Both clauses hold for the nested core (AVM-BE measured in
§2-§3; 7367 ≤ 10000 and 105.08 MiB ≤ 256 MiB), so **V4 = nested core carved to `bytes_used`**. The
wrapper fits too, but it is the fallback only; it would have published 8 regular files and carried a
depth-limited gap over the 32.7 MB core.

The count is the oracle's own name census, confirmed by the independent extraction (6349 + 615 + 401 +
1 names). It is a model in one respect only: REA contributes exactly one directory per chunk inside
its staging root (round-40 V1 receipt: chunk `input_path` `$output/firmware.bin_extract`), counted as
the single `chunk_directory` entry.

## 7. Identity for 5491 (`info_en.txt` and the image's own identity files)

`info_en.txt` is a **published sibling of the image** (not inside it); `./var/info.txt` inside the
image is only the bilingual AVM licence notice and names no product or version.

```
curl -sS -D info_en.hdr -o info_en.txt https://download.avm.de/fritzbox/fritzbox-5491/other/fritz.os/info_en.txt
# HTTP 200, content-length 53166, last-modified Mon, 18 Nov 2024 14:01:04 GMT
sha256 ec2528eb91f16d35c9245c8f7c276a57edd7fb58344a649fa1add451051970b4
```

Identity lines (lines 8-14): `Product: FRITZ!Box 5491` · `Version: FRITZ!OS 7.31` ·
`Language: English, French, German, Italian, Polish, Spanish` · `Release date: 09/04/2023`. The image's
`./var/content` agrees and adds `Product=Fritz_Box_HW243 (FRITZ!Box 5491)`, `Type=Release`,
`Releasecycle=PSQ19P2NL4`, `Version=07.31`, `Build=107858`; `./var/version` is
`FIRMWAREVERSION=171.07.31,,107858,`. Product string used in the fragments:
`FRITZ!Box 5491, FRITZ!OS 07.31`.

## 8. Risks, defects and integration work before the freeze / wave 2

1. **`carriers.json` schema gain.** The round-41 counter must accept (and the round-41 fetch tool
   must consume) `external.nested: {path, sha256}`. `tools/round-40/fetch-vendor.py` currently does
   `carve(member, length)` only; its round-41 port needs a nested step (extract
   `filesystem_core.squashfs` from the member — `sasquatch-v4be` is already a hard dependency of the
   counter's extractor pin — then carve to `length`) and must verify **member_sha256 and
   nested.sha256** before the carve (R40-CL6 chain). Without it, V4's bytes cannot be rebuilt from the
   pins and the fetch-chain binding fails.
2. **Round-41 run harness.** `tools/round-40/c1-run.sh` hardcodes the `/kaidoku-r40/` provenance
   segment and the `kaidoku-r40-c1-run-v1` schema/claim; the counter's `provenance_ok()` looks for that
   segment in `parameters.output_directory`. The round-41 after arm must be ported (segment
   `/kaidoku-r41/`, schema/claim round 41) or every receipt is rejected. My oracle-side port is
   `artifacts/R41C1VendorV4/r41-oracle-run.sh` (same frozen table grammar and validation, round-41
   provenance); the after arm has no equivalent yet.
3. **Exact-relative matching (R40-CL1) is not exercised by V4** (§5: 0 collisions both ways). V4's
   tables are admissible under either the suffix or the exact test; L3/L4 must carry the defect
   coverage, and the round-41 counter must still compute exact paths relative to the chunk extract
   root (strip the `firmware.bin_extract/` prefix recorded in the chunk `input_path`, do not
   suffix-match).
4. **Expected V4 after-receipt shape (predicted, not measured on V4).** [INFERENCE] From this layout
   plus the four round-40 receipts: handler `squashfs_v4_be`, one chunk `range = root_file_range =
   [0, 32720860)`, `extraction_failed: false`; 6349 published regular files (all oracle rows); 615
   `unpublished-entry` gaps, one per symlink; exactly 1 structural `depth-limited` gap; the char device
   `dev/led` unpublished and un-gapped (round-40 V1 behaves this way: 263/263 symlinks unpublished,
   char device neither published nor gapped). The frozen gap rule must therefore allow
   `unpublished-entry` for `symlink` (the round-40 rule does; it has no per-kind count cap for
   path-resolved gaps, so 615 is compatible) and keep `structural.depth-limited: 1`. If unblob
   published any V4 symlink, the C1 clause "publishes no non-regular entry at its exact path" would
   fail — all four round-40 carriers removed **all** symlinks (263/263, 85/85, 2/2, 2/2), so the
   precedent is strong but this is V4's main unmeasured risk.
5. **Receipt size and runtime headroom.** [INFERENCE] Round-40 V1: 697 files + 263 unpublished + 264
   gaps = 1224 entries → 383,481-byte `after.json` (313 B/entry) in 3.1 s for a 5.44 MB carrier. V4's
   6349 + 615 + 616 = 7580 entries extrapolate to ≈ 2.4 MB (< REA's 8 MiB child `--fsize` cap) and a
   proportionally longer run (32.7 MB, 7367 inodes) — comfortably inside the 120 s deadline on this
   host (the raw `sasquatch-v4be` extraction of the same bytes took 4 s end-to-end including both
   producers and hashing). No unblob/REA run was made on V4 to confirm.
6. **Reserved bytes.** The 5491 image, its `var/tmp/filesystem.image` member and the carved core were
   read only by `sqfs-list.py` and a direct `sasquatch-v4be` extraction in scratch; **no REA and no
   unblob** ran on them or on anything carved from them, before or after the freeze, per the binding
   reservation. The wave-2 after run is the first permitted extractor run.
7. **Report-field note.** `external.length` = carrier carve size (32720860), consistent with the
   round-40 `carve(member, length)` semantics now applied one level down; the nested file's own size
   (32,722,944) is recorded in `provenance.json` only, because the item fixed the nested object at
   `{path, sha256}`.

## 9. Reproduction (all commands absolute, scratch-only)

```
S=/fast/scratch/hyaku/kaidoku-r41/R41C1VendorV4          # removed before this report was finished
A=$PWD/.ufo/waves/round-41/w1/artifacts/R41C1VendorV4     # this seat's artifacts dir
bash "$A/r41-oracle-run.sh" "$S/V4.carrier" "$A" "$S/work"   # oracle.tsv/nonregular.tsv/oracle-check.tsv/oracle-run.json
python3 -I -B "$A/chain-walk.py" "$S/V4.carrier" > "$A/chain-walk.json"
```

The carrier itself is rebuilt by §1's chain (no vendor bytes are committed, AVM licence). Tool pins:
`sqfs-list.py` `1079fa9b…353cd9`; `sasquatch-v4be` `fac88740…1b7214c6` (4.5.1); `rea-agents` 6.5.0
(constants read only, never executed on V4); `unblob` 26.6.4 not executed at all this seat.

## 10. Tooling and hygiene

- **No installs or upgrades** were made (no pacman, no `uv tool`, no npm global): the only executables
  used were pre-existing `curl`, `python3`, `tar`, `sasquatch-v4be` and `jq`. Nothing was written to
  `~/.local/bin` or any PATH directory, and sasquatch/unblob were not touched.
- Scratch `/fast/scratch/hyaku/kaidoku-r41/R41C1VendorV4` (image, tar members, extracted trees,
  private work dir) was deleted after the cited tables/JSON were copied into the artifacts dir; no
  vendor bytes exist in the lane.
- Lane writes are exactly this report plus
  `.ufo/waves/round-41/w1/artifacts/R41C1VendorV4/{carriers-V4.json, provenance.json, budget.json,
  oracle.tsv, nonregular.tsv, oracle-check.tsv, oracle-run.json, chain-walk.py, chain-walk.json,
  r41-oracle-run.sh}`. No VCS mutation, no commit, no push.

## 11. Files delivered

| file | bytes | sha256 |
|---|---|---|
| `oracle.tsv` | 719,304 | `3ab10e12320f678f556c306a1a00d540ac12d26f54b5b46f141121867f0742d6` |
| `oracle-check.tsv` | 719,304 | `3ab10e12320f678f556c306a1a00d540ac12d26f54b5b46f141121867f0742d6` |
| `nonregular.tsv` | 43,647 | `eea97c809a4d84d0b02d6fb943f13ea3e3afa0ed2e73db9f63974fd5cc27560d` |
| `oracle-run.json` | 6,000 | `2d8900880653b72f14846bf1db9eb75ecd86134fc0cfae68528033ae5440bf96` |
| `chain-walk.json` | 3,134 | `245a431515d8689dbb816d30f0a5e7708ecaf5fa828c878a4a22b1cd23c44ca6` |
| `carriers-V4.json`, `provenance.json`, `budget.json`, `chain-walk.py`, `r41-oracle-run.sh` | — | present as described |
