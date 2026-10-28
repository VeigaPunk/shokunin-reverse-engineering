# Draft `## Gate` rows for S138 / S139 (for `corpus/lessons/round-49.md`; not landed)

Drafted by C1ScribeSources, 2026-10-28, from independent re-opens (receipts in `receipts/`, SHA256SUMS there) and the two peer re-open reports (`../C1S138Reopen.md`, `../C1S139Reopen.md`). `opened` in the registry stays `2026-10-28`.

### Sources opened this round (2026-10-28)

| row | URL | opened | located quote (≤25 words) |
|---|---|---|---|
| S138 | https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs (tag placement); member listing https://api.github.com/repos/onekey-sec/unblob/contents/tests/integration/filesystem/squashfs/squashfs_v1/big_endian/__output__?ref=26.6.4 | listing 2026-10-28T21:09Z, HTTP 200, 1241 B, sha256 `8a59dc516ae92910c0a2c0a1a645590cfb82795567586839ea27a892022aad58` (`receipts/squashfs_v1-big_endian.json`); tree page 2026-10-28T21:11:03Z, HTTP 200, 200946 B (`../C1S138Reopen/` F1) | listing array element `[0]`: `"name": "squashfs_v1.0_be.bin_extract"` (member directory under `__output__`). Tag placement, tree page `<title>`: "unblob/tests/integration/filesystem/squashfs at 26.6.4 · onekey-sec/unblob · GitHub" |
| S139 | https://github.com/plougher/squashfs-tools/releases; release API https://api.github.com/repos/plougher/squashfs-tools/releases/tags/4.7.5; annotated tag https://api.github.com/repos/plougher/squashfs-tools/git/tags/1fdc2fe01d681438a04e2a137a9f51d829ba3358; binary `/usr/bin/unsquashfs` | release API 2026-10-28T21:08:58Z, HTTP 200, 5873 B, sha256 `979b2d89a6d3cb4a395fb46381311a07b08315f267e18cc0dc6feb22cefa3591`; tag object 2026-10-28T21:11:43Z, sha256 `68b4ba6410859943a9e525c1eb1687521d81fa3ebfee650f38b282a3568b870a`; releases page 2026-10-28T21:07:48Z, HTTP 200, 361752 B (`../C1S139Reopen.md`) | release JSON `$.name`: `"name": "Squashfs tools 4.7.5"`; tag object `$.object.sha`: `"sha": "708c59ae80853b0845017c33b42e56061cc546cd"` (peeled commit); `/usr/bin/unsquashfs -version` stdout line 1: `unsquashfs version 4.7.5 (2026/03/01)`, exit 1 |

Notes for the Gate reader (not quotes):

- The rendered pages are mutable and are not identities. S139 releases page measured at 398943 B (row, round-44 snapshot), 361752 B (2026-10-28T21:07:48Z) and the tag page at 159470 B; S138 tree page at 200946 B and 200958 B on two fetches seconds apart. The Gate cites API JSON and tag identity; a page digest appears only as a fetch-time record.
- The contents-API body hash also varies with request headers (S138 top listing: `be3180fc…` at 11007 B here, `67a0fca8…` at 9960 B in `../C1S138Reopen/` F2). Do not cite a body hash of that endpoint.
- The S138 `teaches` clause ("regression dataset, not an independent producer") is analysis, not a quote: the tree page contains no `__output__` token (`../C1S138Reopen/` F7). The pin clause is grounded by the raw LFS pointer URL in `../C1S138Reopen/` F4.
- The 22-member manifest digest check (`../C1S138Reopen/` F0, F5: manifest `06a72dd5b660c79adae943917abf40c24ab16554ec6c2f14985958799a78f5fe`, mismatch 0 of 22) is that seat's measurement; this seat did not re-run it.
