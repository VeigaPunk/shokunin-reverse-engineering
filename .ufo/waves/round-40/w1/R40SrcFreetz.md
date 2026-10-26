DONE — S114 URL is live and byte-identical to the round-37 copy; the "block length little-endian" sentence is located (lines 8-9). One correction to the draft: Freetz's code swaps only the 2-byte *metadata*-block headers, not data-block sizes. A new patch-code row (S123) is drafted. The S114 recheck cell should stay `180d`.

# R40SrcFreetz — Freetz AVM-BE source re-open

## 1. S114 re-fetch (access 2026-10-26T18:18:09Z)

Command: `curl -sS -D hdr.txt -o f.txt -w "%{http_code} %{size_download}" https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt`

| item | observed |
|---|---|
| HTTP status | 200 (HTTP/2), `content-type: text/plain; charset=utf-8`, etag `daa14001…5fe9` |
| size | 1496 B, 22 lines |
| sha256 | `c1c43f6f97d7477dcdab15203d11e43b49beb12e3a43a3b52bdd71b672a9a5d5` |
| vs round-37 `.ufo/waves/round-37/probes/avm.txt` | `cmp` identical, same sha256 |
| `github.com/Freetz/freetz/blob/master/...` | 200 |
| repo state | `Freetz/freetz` is not archived. master HEAD `75984884e4353db3b45b04cd37707c6e929ca0ec` (2021-05-26). The file's only commit is `3a44569c740b6373166c13ab98d5e5a7ab61711a` (2017-01-13, "rename squashfs4-host package to squashfs4-host-be"). The page is effectively dormant, not dead. |
| successor | `Freetz-NG/freetz-ng` carries the same text as `docs/wiki/60_Development/squashfs4-be.en.md`. Raw fetch 200, 1514 B, sha256 `100948f38ea0ff7258eee00a420e67b090fd9a1e7e191361d03b9a9604875fc9`. The body is the same 22 lines with a `# SquashFS 4 (BE)` heading prepended; its last commit is `f9157c387a116d6b8d6a8c99e2626c10495ed71f` (2021-02-15). |

### Located quote (the sentence asked for)

Raw file lines 8-9 (20 words):
> "the only data field stored in the little-endian format is the block length value at the beginning of each block"

Marker sentence, lines 13-14:
> "contains (instead of the filesystem creation time) the same value as the super-block field 'bytes_used'"

Other located facts from the same file:
- line 10: "compression method is hardcoded to be XZ (aka LZMA2)".
- lines 5-7: the rest of the file-system data is big-endian ("for all file system related data").
- lines 16-17: the user-id table is always stored uncompressed.

### Defect in the current S114 anchor

The anchor in `corpus/SOURCES.md` row S114 has two problems.
1. The second quoted phrase, `mkfs_time` field holds the same value as `bytes_used`, is a paraphrase and is not in the file. The real text is split across lines 13-14 (quoted above).
2. "opening line: … (called AVM-BE below)" spans raw lines 1-2. The sentence is one sentence across the line break; "(called AVM-BE below)" is raw line 2.

The row also records no HTTP status, size or sha256, and it does not carry the block-length sentence. It does not need it for its current use-by (the r38 entry), but the R40 AVM claim needs it.

### S114 recheck cell: old → new
- recheck `180d` → `180d`, unchanged. The row's `opened` is already today (2026-10-26), so this re-fetch is a same-day re-open. The next due date stays 2027-04-24 (opened + 180 d).
- Suggested edits to the row that the L1 may fold in:
  - anchor: replace the paraphrase with the verbatim lines 13-14 quote above.
  - anchor: append `HTTP 200, 1496 B, sha256 c1c43f6f…a5d5, re-opened 2026-10-26T18:18:09Z; lines 8-9 "the only data field stored in the little-endian format is the block length value at the beginning of each block"`.
  - used-by: append the round-40 AVM knowledge entry if it cites S114 for the marker.

## 2. Patch code: what is swapped (the draft needs one correction)

Freetz implements AVM-BE as patches on squashfs-tools 4.3 (`squashfs4-host-be.mk`: `SQUASHFS4_HOST_BE_VERSION:=4.3`, `EXTRA_CFLAGS="-DTARGET_FORMAT=AVM_BE"`). The sourceforge tarball md5 `d92ab59aabf5173f2a59089531e30dbf` equals Freetz's pinned `SQUASHFS4_HOST_BE_SOURCE_MD5`. The same patch files exist in Freetz-NG at `make/host-tools/squashfs4-be-host/patches/`.

Sha256 equality between Freetz/freetz and Freetz-NG:

| patch | sha256 | Freetz/freetz = Freetz-NG |
|---|---|---|
| `250-mksquashfs__AVM_BE.patch` | `f5964ad9…b908d` | yes |
| `350-unsquashfs__AVM_BE.patch` | `7f0a1b25…0220fc` | yes |
| `550-mkfs_time__AVM_BE_AVM_LE.patch` | `603c36c9…15a7` | yes |
| `101-…symbols_only.patch` | `e28b3341…c707` | yes |

Located code. Line numbers are lines of the `.patch` file.

**Reader** (`350-unsquashfs__AVM_BE.patch`):
- lines 19-22, in `read_block`: `if (read_fs_bytes(fd, start, 2, &c_byte) == FALSE)` then `if (swap_block_length)` then `c_byte = (c_byte >> 8) | ((c_byte & 0xff) << 8);`. The header is read as 2 bytes.
- line 35: `/* block length in AVM-BE format is stored in LE order */`.
- lines 36-40: `swap_block_length = 1; // do swap block length` on a big-endian host, and `swap_block_length = 0; // do NOT swap block length, already in the right order` on a little-endian host. The non-AVM branch has `swap_block_length = swap`, which is the plain BE-v4 behaviour.

**Writer** (`250-mksquashfs__AVM_BE.patch`):
- lines 7-19: the `_SQUASHFS_SWAP_SHORTS(s, d, n)` macro is `memcpy(d, s, n*sizeof(short))` on a little-endian host, which writes the 16-bit header LE.
- it is applied to `c_byte` at the inode-table, directory-table (2 sites) and `generic_write_table` sites (lines 29, 38, 47, 68, 77).
- lines 55-56: `generic_write_table(id_bytes, p, 0, NULL, TRUE); /* AVM-BE always uncompressed */`.

**Marker** (`550-mkfs_time__AVM_BE_AVM_LE.patch`):
- line 8: `sBlk->mkfs_time = (int) sBlk->bytes_used;`.
- line 25: reader test `sBlk.s.s_major == 4 && sBlk.s.mkfs_time == (int)sBlk.s.bytes_used`.

### Correction to the draft claim R40-C1
The draft says "LITTLE-endian metadata/data block-length headers". The Freetz patch code supports only the metadata half.
- Observed: `read_block` is the only function patched. Its 2-byte `c_byte` is the metadata-block header. In 4.3's `unsquashfs.c` and `read_fs.c`, `read_block` callers are the inode table, directory table, compressor-options block, and the fragment, id, lookup and xattr index tables.
- Observed: data-block sizes are read by `read_data_block(start, size, …)` (4.3 `unsquashfs.c:733`). `size` comes from the inode block list or the fragment entry (`SQUASHFS_COMPRESSED_SIZE_BLOCK(block_list[i])`, line 1025). Those are fixed-layout `file system related data`, so they are big-endian in AVM-BE. Squashfs-4 data blocks have no length header.
- [INFERENCE] The counter's "first metadata block length decodes as little-endian" check is therefore the right shape. A "data block-length header is LE" check has no basis in the Freetz source. If the freeze text says "data", reword it to "metadata block headers (inode, directory, fragment, id and lookup tables)". Whether a real AVM carrier agrees is a carrier-side measurement, which I did not make (frozen-carrier discipline).
- Freetz prose (line 8-9) says "each block". Its code swaps the 2-byte metadata header only.

## 3. Draft SOURCES row (new; 11 columns)
The URL is not dead. Add this row as a code-tier companion to S114 (S114 remains the prose note). The next free id is S123 (last is S122); the L1 renumbers if needed. The entry stem is [INFERENCE]: change it to the real round-40 AVM knowledge-entry path.

```
| S123 | Freetz-NG AVM-BE unsquashfs patch (block-length swap), commit-pinned — https://raw.githubusercontent.com/Freetz-NG/freetz-ng/9a7236926bffaa6af16f84b3db27017cb5f02724/make/host-tools/squashfs4-be-host/patches/350-unsquashfs__AVM_BE.patch (byte-identical to https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/patches/350-unsquashfs__AVM_BE.patch) | code | A | the implementation of AVM-BE's reader: which field is read little-endian, and the `swap_block_length` selector, against squashfs-tools 4.3; not a statement about any AVM image, not the sasquatch-v4be fork | Freetz-NG master `9a7236926bffaa6af16f84b3db27017cb5f02724` (2026-10-26T17:43:25Z), file last changed `a2c8410257735705a59f896b4487860b5c161913` 2022-10-16; opened 2026-10-26T18:25Z, HTTP 200, 2217 B, sha256 7f0a1b252d4bbde747efe98d1f97b52eab28d55ee957b7307d0344cbe1e220fc; patch line 35 `/* block length in AVM-BE format is stored in LE order */`, line 22 `c_byte = (c_byte >> 8) | ((c_byte & 0xff) << 8);` under `if (swap_block_length)`, line 39 `swap_block_length = 0; // do NOT swap block length, already in the right order`; companion 550-mkfs_time patch line 25 marker test `mkfs_time == (int)sBlk.s.bytes_used` | Only the 2-byte metadata-block header (read_block) is byte-order-exceptional in AVM-BE; data-block sizes come from big-endian inode/fragment fields, so a layout check targets the first metadata header, not a data header | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-r40-avm-be-squashfs-layout.md |
```

Why Freetz-NG as the pinned primary: Freetz/freetz master is frozen at 2021-05-26 while Freetz-NG is live (HEAD today). Both byte-equal, so the Freetz/freetz URL is a listed fallback.

## 4. Commands and artifacts

- `curl` of the S114 URL, header dump, `sha256sum`, `cmp` against `.ufo/waves/round-37/probes/avm.txt`.
- GitHub REST (unauthenticated): `repos/Freetz/freetz/contents/tools/make/squashfs4-host-be[/patches]`, `…/commits?path=…` and `repos/Freetz-NG/freetz-ng/git/trees/master?recursive=1` (13600 entries, `truncated=false`; AVM patches found under `make/host-tools/squashfs4-be-host/patches/`). `search/code` returned 401.
- `https://downloads.sourceforge.net/project/squashfs/squashfs/squashfs4.3/squashfs4.3.tar.gz`: md5 `d92ab59aabf5173f2a59089531e30dbf`, grepped for `read_block(` and `read_data_block`.
- `Freetz-NG/freetz-ng` `make/host-tools/…/350-…patch` at the pinned commit: 200, 2217 B, sha256 `7f0a1b25…0220fc`.

Limits: no REA, unblob or carrier run, and none was needed. The claim about 4.3's `read_block` callers is from the upstream tarball, not from a carrier. Scratch removed.

Artifacts (under `artifacts/R40SrcFreetz/`):
- `AVM-BE-format.txt.fetched-2026-10-26`
- `AVM-BE-format.txt.headers`
- `freetz-ng-wiki-squashfs4-be.en.md.fetched`
- `250-mksquashfs__AVM_BE.patch`
- `350-unsquashfs__AVM_BE.patch`
- `550-mkfs_time__AVM_BE_AVM_LE.patch`

Report: .ufo/waves/round-40/w1/R40SrcFreetz.md
