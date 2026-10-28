# W2C1Superblock — superblock table and carriers.json pins, own parser (landing 29883d4e)

**Verdict: no numeric value differs.** Every value in the entry's superblock table and every superblock pin in `tools/round-49/carriers.json` equals my independent decode of the four committed carriers (0 DIFF over 4 carriers × 16 compared fields). The offsets of the `78 da` streams the entry cites are exact. I found four text-level defects, none of which touches a counter predicate; all are in frozen or landed prose, not in a measured number. Nothing in the lane was edited.

Read at `29883d4ec35a31a8393c4ffb220888c44c0bb022`, carriers from git objects. Run 2026-10-28T22:3xZ, `GIT_NO_REPLACE_OBJECTS=1`. Scratch removed; artifacts in `.ufo/waves/round-49/w2/W2C1Superblock/`.

## Method
- `parse_sb.py` (own, ~35 lines, `python3 -I -B`, exit 0, no repo code): magic → byte order; `struct.unpack` of inodes, bytes_used, uid_start, guid_start, inode_table_start, directory_table_start (offsets 4..27), s_major/s_minor (28/30), block_size_1/block_log (32/34), flags/no_uids/no_guids (36..38), mkfs_time (39). It also scans for `78 da`, inflates each stream, and reads the metadata-block u16 at the inode/dir table start. Output `parse_out.json` sha256 `24c77ce8…a11f3`; `parse_sb.py` sha256 `b27bc015…5266`.
- The four carrier files were extracted with `git show 29883d4e:corpus/evidence/round-42/c2/fixtures/<f>`. sha256 and size equal `carriers.json` and the entry table (4096 bytes each; `529e1077…`, `b45925fa…`, `79c0f388…`, `7c62dbe3…`).
- I compared the result with `carriers.json` `carriers[].{sha256,size,s_major,s_minor,endian}` and `oracle.superblock_info.probe_v1v2.{bytes_used,directory_table_start,guid_start,inode_table_start,inodes,uid_start,magic,major,minor,endianness,meta_len}`: `compare_carriers_json.txt` sha256 `66f4a1ab…735266`... (full: `66f4a1ab1a207f9d3a990769298e8b409ebeace4d4bb82cbc5ee67ccba27735f`), final line `DIFFS 0`.
- Entry table vs mine, all equal:

| carrier | magic | maj:min | block_size_1 | block_log | flags | uids/gids | inodes | bytes_used | mkfs_time UTC | mkfs epoch |
|---|---|---|---|---|---|---|---|---|---|---|
| v1be | sqsh | 1:0 | 32768 | 15 | 0x00 | 1/0 | 4 | 177 | 2024-08-05T07:18:58Z | 1722842338 |
| v1le | hsqs | 1:0 | 32768 | 15 | 0x00 | 1/0 | 4 | 176 | 2024-08-05T07:18:51Z | 1722842331 |
| v2be | sqsh | 2:0 | 0 | 16 | 0x40 | 1/0 | 5 | 201 | 2023-03-09T17:06:30Z | 1678381590 |
| v2le | hsqs | 2:0 | 0 | 16 | 0x40 | 1/0 | 5 | 196 | 2023-03-09T17:05:52Z | 1678381552 |

- `78 da` offsets (inflate-verified): v1be/v1le `[73]`; v2be `[63, 90, 140]`; v2le `[63, 90, 138]`. Equal to the entry text and to the round-49 scribe's `scripts/sb.py` (sha256 `f1614b79…a0b8`, run on the same bytes, same output). `78 xx` scan finds no other zlib header.
- Host-local vs UTC correction is right: `TZ=UTC unsquashfs -s`/`7z l` print 07:18:58/07:18:51; `date +%z` = `-0300`; `TZ=America/Sao_Paulo date -d @1722842338` = 04:18:58. (`readers_utc.txt`, sha256 `e84d0325…94228`.)
- Reader outputs match the entry: unsquashfs 4.7.5 inodes/size/block size/fragments/uids, 7z member sizes (6→6, 7→7, 7→7; 7→25 + 0,0,0), `file` 5.48 labels incl. `-32768`.
- Installed unblob 26.6.4 `squashfs.py`: struct is `char s_magic[4]`, six `uint32`, two `uint16`; v1 patterns `73 71 73 68 [24] 00 01` / `68 73 71 73 [24] 01 00`, v2 `… 00 02` / `02 00`. Matches the entry.

## Findings (all non-numeric; none moves a counter)

| # | severity | what | evidence (exact) |
|---|---|---|---|
| F1 | medium (frozen prose, calibration) | `carriers.json` `superblock_layout.note` says "SquashFS v1/v2 superblock is 32 bytes (packed)" and every `probe_v1v2.superblock_size` is `32`. 32 is only unblob's `squashfs_super_block_t` header struct. The packed superblock continues: block_size_1/block_log/flags/uids/gids/mkfs_time to offset 43, `root_inode` u64 at 43, and in v2 `block_size` u32@51, `fragments` u32@55, `fragment_table_start` u32@59 → v2 header is 63 bytes. Proof from the bytes: v1 raw data `apple\nbanana\ncherry\n` starts at 51; v2 first zlib stream starts at 63. `extended_header.txt` (sha256 `6fe3ebe8…68df2`): v1 root_inode 0x33 both orders; v2 root_inode 0x60, block_size 65536, fragments 1, fragment_table_start 193 (be) / 188 (le). The entry itself does not claim 32 bytes total (it says "first 32 bytes … then the packed tail"), so the entry is fine; the frozen note and the probe field name are not. | `python3 -I -B` over the four carriers, offsets as stated |
| F2 | low-medium (entry, calibration) | The entry labels 65536 as *derived* ("arithmetic, not measured … truncation") and `block_size_1 = 0` as an observation. 65536 is directly measurable: the v2 header's `block_size` u32 at offset 51 reads 65536 on both byte orders (`extended_header.txt`). The "derived" label understates the evidence; the claim is true. | `extended_header.txt` lines v2 `>` and `<` |
| F3 | low-medium (entry + carriers.json) | "Compression is gzip on all four" is evidenced for v1 only by the *inode-table* metadata block. In both v1 carriers the single `78 da` stream (offset 73) is the inode table (meta header `0x38`/`0x37` at 71, inflates to 65 bytes, ends exactly at directory_table_start); the v1 directory table header is `0x802a` (uncompressed bit set); the data blocks are stored raw (`apple\nbanana\ncherry\n` at 51; 7z 6→6). The entry prints "Data is compressed" (a flag read) and the 7z 6→6 figures next to "gzip on all four" without saying v1 data is stored. Also `carriers.json` `compression_evidence` for v1le/v1be says "inodes/data/fragments compressed" but `unsquashfs -s` prints no Fragments line for v1 (readers_utc.txt). The `probe_v1v2.compression: gzip` is an inode-table-header inference, which the entry's own "no selector" sentence allows; a reader would still likely infer gzip data blocks in v1. v2: streams 63 (28-byte fragment), 90 (inode table), 138/140 (dir table) are all deflate. | `parse_out.json` fields `inode_meta_hdr`, `dir_meta_hdr`, `inflate` |
| F4 | low (citation) | `carriers.json` `superblock_layout.note` cites the unblob struct as "(S119)"; S119 is the rea-agents package row, S112 is the unblob handler row (`corpus/SOURCES.md` lines 118/125 at the landing rev). The entry cites S112 correctly. Within the entry, S112 range is `:123-136` in the header line and `:123-137` in the superblock section (struct closes at 135, `HEADER_STRUCT` at 137 in the installed 26.6.4 file). `scripts/sb.py` exists only at `.ufo/waves/round-49/w1/C1ScribeEntry/scripts/sb.py` (disclosed at entry line 123 as staying in the wave directory; the path `scripts/sb.py` is relative to it). | `git show 29883d4e:corpus/SOURCES.md`; `git ls-tree` |

## Side check (file(1) explanation, supports the entry)
The entry's "layout artifact" explanation for the BE `uncompressed` label holds, and the mechanism can be named: `file` reads the u16 at offset 20 (the v4 compression field) — high half of the 32-bit `inode_table_start` in BE (0 → "uncompressed"), low half in LE (71/88 → "compressed"). Scratch mutation: BE with bytes 20-21 set to `00 01` → "zlib compressed"; LE with bytes 20-21 zeroed → "uncompressed"; flags^3 changes nothing. The entry's sentence "no field distinguishes them" is slightly loose: no *compression* field does, but `inode_table_start`/`bytes_used`/`dir_table_start`/`mkfs_time` differ between the byte orders (the entry elsewhere lists bytes_used 177 vs 176). `carriers.json` names offset 20; the entry does not.

## Not run
`c1-counter.py` and `c2-mismatch.py` themselves (out of scope for this seat). No check of S138/S139 live pages. No v2ns/v3 decode.

## Receipts
All commands above exited 0 (git show, parse_sb.py, compare, unsquashfs/7z/file reads, mutation probe). Hashes of artifacts: `parse_sb.py` b27bc015…, `parse_out.json` 24c77ce8…, `compare_carriers_json.txt` 66f4a1ab…, `extended_header.txt` 6fe3ebe8…, `readers_utc.txt` e84d0325…. `carriers.json` at landing rev blob content sha256 `829e3392…56b3` (unchanged since the freeze: empty `git diff --stat decc5697..29883d4e -- tools/round-49/carriers.json`).
