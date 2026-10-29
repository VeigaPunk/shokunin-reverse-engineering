# C2RowS138 — S138 correction row (S154) drafted, census re-derived, validated on a base-revision clone

Seat: C2RowS138 (leaf, no subagents). Base `7c678ae6d97aedb969fd253b52b3d2882ef1e186`. Lane tree, lane `corpus/SOURCES.md` and fleet repo: untouched (lane `corpus/SOURCES.md` sha256 `ae3c1e17a3c8fcfc39209b8fa2d2d4623347ced88da5b54c46e011885db54c11`, equal to the base blob; `HEAD` = `7c678ae6`).

## Verdict

**Ready to fold, not landed.** The S154 grounding row is drafted (`S154-row.md`) and passes `sources-census.sh validate --file` (exit 0) on a clone at the base revision with the row inserted after S149. The 22-member census re-derives from the tag's git tree and from the LFS media bytes (22/22, 152 B, 7 distinct sha256, sorted digest `21cb3a6a…` reproduced exactly). One of the two channels the assignment named (GitHub contents API) was rate-limited for ~6 minutes; the listings were re-fetched after reset and all 17 listing calls that matter returned HTTP 200.

## Findings (most important first)

| # | class | finding | evidence |
|---|---|---|---|
| F1 | correction (S138) | The census holds: four endian `__output__` trees (`squashfs_v1/{big,little}_endian`, `squashfs_v2/{big,little}_endian`), **22 members**, **152 B**, **7 distinct** LFS oids, sorted digest `21cb3a6ab67af507f6b4ccaff15d1990567550355a7a4c21ef4111b9efd660ca` (= the recorded value). Per endian: v1 3 files; v2.0 4 + v2.1 4. All 22 media fetches hash to their LFS oid (`media_mismatches 0`). | `receipts/census.out.txt`, `receipts/s154.json` |
| F2 | correction (S138) | One located quote per tree, each an element of a listing `name` field: v1 BE `"cherry.txt"` `$[2].name` (listing sha256 `588573…71fda`); v1 LE `"cherry.txt"` `$[2].name` (`b858d8…0ad6`); v2 BE `"apple4.txt"` `$[3].name` (`74807e…dadd`); v2 LE `"apple4.txt"` `$[3].name` (`ab0918…fdbcd`); full hashes in the S154 row and the table below. The API blob `sha` of all 22 names equals the git tree blob (`api_blob_eq_git` 22/22). | `receipts/s154.json` `quotes`, `listings` |
| F3 | channel / rate limit | Unauthenticated GitHub API quota (60/h) was exhausted on this IP: five HTTP 403 "API rate limit exceeded" responses (23:33:08Z–23:35:01Z) for the v2 little-endian `.bin_extract` listings. Core quota reset at 23:39:22Z; the two listings re-fetched at 23:39:37Z returned HTTP 200. The git-tree channel (F4) was used as a parallel independent check and needed no quota. | command log below |
| F4 | channel (new) | Git channel is a valid second source for the same census: `git clone --filter=blob:limit=2k --no-checkout --depth 1 --branch 26.6.4` gives HEAD `1fcc7a0a584a70a96c31f5a276c20944d199a089` (the S138 commit) and all 261 `squashfs` tree lines; LFS pointers (126 B) are fetched by the size filter. Recommend S154 anchors name both channels for the freeze. | `census.out.txt` |
| F5 | validator (process) | `sources-census.sh validate --file <path>` on a **bare copy** of SOURCES.md under `/fast/scratch` returns **exit 1** with E11 (`used-by` path missing on disk) on the rows citing `corpus/…`. Validated on a **clone-shaped tree** (`clone/corpus/SOURCES.md`) it returns exit 0. The freeze/landing check must run on a tree shape, not a bare file (same pitfall as the round-49 paste hazard in `W2CleanClone.md` F1). | `receipts/val-base.tsv` (exit 0, clone), bare-copy run exit 1 (not kept) |
| F6 | calibration (S138 row) | S138's `teaches` cell carries claims wider than the census: `unsquashfs` path-for-path agreement "on all six carriers" and the 7-Zip cross-check. S154's `teaches` is narrowed to the census. S138 itself is append-only and stays `mined`; S154 supersedes it for the census claim only. | `SOURCES.md` line 144 (S138) |
| F7 | warning only | S154 shares S138's URL with a different `scope`: validator emits one `W04` (warning; does not change status). `E04` (duplicate URL+scope) is not triggered by the scope difference; the `supersedes S138 —` token is present anyway. Base: 15 W04 + `ok`; S154 scratch: 16 W04 + `ok`. | `receipts/val-base.tsv`, `receipts/val-s154.tsv` |
| F8 | landing decision for L1 | The two knowledge entries that cite S138 as `source:` (`2026-10-28-r44-squashfs-v1v2-core.md`, `2026-10-28-r49-squashfs-v1v2-core.md`) are not frozen. Whether their `source:` lines also cite S154 is an L1 decision; I did not edit them. `used-by` of S154 lists both. | `corpus/knowledge/…` |
| F9 | not re-derived | S138's anchor says "10 contents-API listings". I did not re-derive that count (round-44 call history); this session made 7 root/tree listing calls, 4 `__output__` calls and 6 `.bin_extract` calls that returned 200, plus 5 rate-limit 403s. The anchor claim is left as the lane's, not checked. | command log |

## The S154 row (drafted; full text in `S154-row.md`)

- id `S154`; kind `code`; tier `A`; scope `unblob 26.6.4 upstream expected output trees`; status `mined`; opened `2026-10-28`; recheck `180d`.
- source: the unblob 26.6.4 tree URL, contents-API form, media base, commit `1fcc7a0a…`.
- anchor: the four located quotes with JSON path and listing sha256, plus the sorted digest.
- teaches: opens `supersedes S138 —`; census only (22 members, 152 B, 7 distinct sha256); not handler code, extractor behaviour, a C1 carrier, or an independent producer.
- used-by: `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`, `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`.
- Field count NF = 13 (checked by awk); no `|` inside cells.

## Command log (exact; UTC; exit; stdout sha256 where kept)

| # | command (abridged; full paths under `/fast/scratch/hyaku/kaidoku-r50/C2RowS138/`) | exit | stdout sha256 / note | time (UTC) |
|---|---|---|---|---|
| 1 | `git clone --filter=blob:limit=2k --no-checkout --depth 1 --branch 26.6.4 https://github.com/onekey-sec/unblob.git gitclone` | 0 | `rev-parse HEAD` = `1fcc7a0a584a70a96c31f5a276c20944d199a089` | 23:32 |
| 2 | `git -C gitclone ls-tree -r HEAD -- tests/integration/filesystem/squashfs` | 0 | 261 lines | 23:32 |
| 3 | `curl -sS -o <body> -w %{http_code} https://api.github.com/repos/onekey-sec/unblob/contents/tests/integration/filesystem/squashfs[/<tree>[/__output__[/<dir>]]]?ref=26.6.4` (bodies only, no headers) — root, 2 versions, 4 endian dirs, 4 `__output__`, 6 `.bin_extract` | 0 (curl) | 200 for all except 5 rate-limit 403 responses (23:33:08–23:35:01Z) | 23:32–23:35 |
| 4 | same, retried after reset for `squashfs_v2/little_endian/__output__/squashfs_v2.{0,1}_le.bin_extract` | 0 | 200, 200 | 23:39:37 |
| 5 | `python3 tools/round-50/s154-git-census.py gitclone walk_media > census.out.txt` | 0 | `bd4f32724749f88e39f2da810677a40aafcb512a3a232eb66080834634940470`; `members 22`, `bytes_total 152`, `distinct_sha256 7`, `media_mismatches 0` | 23:36 |
| 6 | `python3 -I -B tools/round-50/s154-census.py --git-census census.out.txt --listing listings > s154.json` | 0 | `d86a740f1561fb9d87545d47f8aee29d8c247cf3ce2d2d9e096a02a75d3ac508`; `failures []`, `digest_matches_recorded true` | 23:41 |
| 7 | negative: one listing `name` changed (`cherry.txt`→`cherry2.txt`) | 1 | failures: `blob mismatch …/cherry.txt`, `quote squashfs_v1/big_endian not a member name` | 23:42 |
| 8 | negative: one listing removed (`squashfs_v2.1_le`) | 1 | `missing listing` | 23:42 |
| 9 | negative: `--git-census /nonexistent` | 2 | could-not-evaluate | 23:42 |
| 10 | `git clone -q --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin clone && git -C clone checkout -q --detach 7c678ae6…` (read-only on the lane; `rev-parse --show-toplevel` = clone dir) | 0 | clone HEAD `7c678ae6…`; `corpus/SOURCES.md` sha `ae3c1e17…` = base blob | 23:33 |
| 11 | `scripts/sources-census.sh validate --file clone/corpus/SOURCES.md` (base) | 0 | `val-base.tsv`: 15 W04 + `ok`, no E-codes | 23:33 |
| 12 | same, after inserting S154 row after line 155 in the clone copy (edit only in scratch) | 0 | `receipts/val-s154.tsv` sha `3199f797…`; 16 W04 + `ok` | 23:40 |
| 13 | `scripts/sources-census.sh validate --file <bare copy>` (no lane tree around it) | 1 | E11 `used-by missing` for `corpus/…` paths (F5) | 23:33 |
| 14 | lane `sha256sum corpus/SOURCES.md`; `git rev-parse HEAD` in lane | 0 | `ae3c1e17…`; `7c678ae6…` (unchanged) | 23:41 |

Digest reproduction: `sha256` of the lines `"<LFS oid>  <path relative to tests/integration/filesystem/squashfs>\n"` sorted by path = `21cb3a6ab67af507f6b4ccaff15d1990567550355a7a4c21ef4111b9efd660ca` (matches the recorded S138 value; other orderings and formats checked and not matching).

## Receipts and artifacts (under `.ufo/waves/round-50/w1/C2RowS138/`)

- `S154-row.md` — the drafted row (sha256 `e3281886332fec0b1834d2acc0c34435463e60a9bc2a24ee1f452707880167ee`).
- `tools/round-50/s154-git-census.py` (sha256 `912b7d8e…`) — git tree + LFS pointer + media census; writes the census JSON-after-4-lines format.
- `tools/round-50/s154-census.py` (sha256 `6b47e9cb…`) — checker over the census and listing bodies; exit 0/1/2; negative controls in rows 7–9.
- `listings/*.json`: the six `.bin_extract` bodies that carry the quotes and the blob-equality check (sha256 in the table below). The outer tree and root listings (11 bodies, HTTP 200) were not copied.
- `receipts/census.out.txt` (`bd4f3272…`), `receipts/s154.json` (`d86a740f…`), `receipts/val-base.tsv` (`01fca666…`), `receipts/val-s154.tsv` (`3199f797…`), `receipts/SOURCES.s154-scratch.md` (`8c143d82…`, the clone copy with the row).

| listing file | sha256 |
|---|---|
| squashfs_v1_big_endian__squashfs_v1.0_be.bin_extract.json | 588573625c5185bd94f3c53bc9f4f92925f6e0592c26435f5bc168f37c171fda |
| squashfs_v1_little_endian__squashfs_v1.0_le.bin_extract.json | b858d860a2598a980931ef5cb86e3df106b94fd97ec3f6ff2aa3f06fdb620ad6 |
| squashfs_v2_big_endian__squashfs_v2.0_be.bin_extract.json | 74807ec11dea00f18a8b8251574cce0e474384bf22c447f102962154fe09dadd |
| squashfs_v2_big_endian__squashfs_v2.1_be.bin_extract.json | a20c4ad577cabb66c84b8d019af179f8532141e786b693d33a52d838812825de |
| squashfs_v2_little_endian__squashfs_v2.0_le.bin_extract.json | ab0918849c105b5a684efdf5518bad95b4be101496a5a7f004e744ddc33fdbcd |
| squashfs_v2_little_endian__squashfs_v2.1_le.bin_extract.json | 0d4ebb094d7b7c7988aec06cc0870befb8e222a764179d4dd19b1ee72e551d3c |

## Not run / limits

- No lane, fleet or sibling file was written. No git mutation outside the scratch clone; the clone commit was never made (validation used the edited working copy).
- Rate-limit 403 bodies were not saved (they name the workstation IP); only the count and times are recorded.
- The 22 member bytes were fetched once from the media base; no second media mirror was consulted.
- No tool was installed or upgraded.
- The census proves the listing and LFS-oid consistency at tag 26.6.4, not that unblob's extractor behaviour is correct (S154 says so).

## For the L1 freeze

1. Fold S154 as drafted (or adjust the anchor to cite both channels per F4). Insert after the S149 row; keep S138 unchanged (append-only).
2. Run `validate` on a clone-shaped tree, not on a bare file (F5).
3. Decide whether the r44/r49 knowledge `source:` lines add S154 (F8).
4. C2 atom B8 can check: S154 row has `supersedes S138 —`, kind `code`, tier `A`, NF 13, and the four quotes locate as `name` elements of the listing receipts above.
