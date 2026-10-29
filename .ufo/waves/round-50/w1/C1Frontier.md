# C1Frontier — round 50 wave 1 (pre-freeze build)

Seat: C1Frontier-2 · 2026-10-28 · lane base `7c678ae6d97aedb969fd253b52b3d2882ef1e186` (HEAD verified, read-only).
Task: frontier read for the round-50 report — SquashFS/firmware items still Frontier AFTER the LE AVM promotion (R50-C1), each with the one cheapest next probe; verify two members of the L1's "v3 `sqsh` comp 0 avm" group by HTTP Range superblock read (≤1 KiB per request); no extractions.

## Verdict

The frontier read is **done and it changes the L1's probe table**: the five-row "v3 `sqsh` comp 0 avm" group is **not one item**. Verified by 96-byte HTTP Range reads (this seat, 2026-10-28):

- **3272** is a **genuine big-endian SquashFS v3.0** rootfs (magic `sqsh`, s_major 3 s_minor 0, `bytes_used == bytes_used_2 == 19,722,974`, inode_table_start 19,718,954, block_log 16, mkfs_time 2023-09-05T16:23:39Z, inodes 199). Its v3 `_2` legacy fields (`inode_table_start_2`, `directory_table_start_2`, `block_size_1`) are **zeroed** — AVM populates only the 64-bit fields, so any v4-offset reader misparses it.
- **7412** is **not a SquashFS at offset 0**: `sqsh` magic followed by ≥0x800 zero bytes, `0xff` fill at +0x1000, high-entropy data at +0x1000 and beyond. No version fields exist. It is an unidentified AVM container that merely begins with the SquashFS magic bytes.

Consequently the L1 scan's "comp 0" and "std"/"avm" labels on all five v3-era rows are **v4-offset artifacts**: SquashFS v3 has no compression field (grounded: plougher/squashfs-tools 4.6.1 `squashfs_compat.h`, `struct squashfs_super_block_3` — offset 20 is `inode_table_start_2`, not compression), and the L1's `mkfs_time` (offset 8) is `bytes_used_2` while its `bytes_used` (offset 40) lands in dead fields. **The plan draft's phrase "v3 `sqsh` comp 0 avm" (round-50-claims.md, probe sentence) should be reworded before the freeze** to the two split items in the frontier table below. No extraction was run; no vendor bytes were written into the lane tree (receipts = hashes, listings, parsed fields only).

## Findings

| id | finding | evidence (exact command, exit, sha256) | confidence |
|---|---|---|---|
| F1 | Group member 3272 verified: genuine BE SquashFS **v3.0**, zeroed `_2` fields, gzip-family-shaped flags (0xC0 = duplicate+export; NOI/NOD clear → compressed bodies; v3's only compressor is zlib) [INFERENCE for zlib-body] | `python3 -I -B range-probe.py > probe-run4.stdout 2>probe-run4.stderr` exit 0 (`aa8df123…`); superblock request `Range: bytes=2284032-2284127` → 206, len 96, sha256 `1b6fb1880f35e307a97b3af2fca6eec996702b2428c09bb71a2cd2a50d7697e4`, 2026-10-28T23:45:25Z | observed |
| F2 | Group member 7412 verified: `sqsh` + zeroed header, not a superblock at 0/0x80/0x100/0x200/0x400/0x800; `ff`-fill at +0x1000; data at +0x10000/+0x20000 | same command, superblock sha256 `ada1a08715ba8292fea5d940d9d7c6d0965da935f4717ff5491a3d85c7cd0717` (23:45:31Z); `python3 -I -B deep7412-probe.py` exit 0 (`8c5f8890…`): offsets 0x80–0x800 all sha256 `f5a5fd42d16a20302798ef6ed309979b43003d2320d9f0e8ea9831a92759fb4b` (= 64 zero bytes), 0x1000 `8667e718…`, 0x10000 `67c84194…`, 0x20000 `c6337802…` | observed |
| F3 | L1 scan's `comp`/`std`/`avm` columns are v4-map artifacts for all five v3-era rows; `sqfs-list.py` is v4-only (raises `unsupported SquashFS version`), so the lane has **no** v3 reader yet | `squashfs_compat.h` 4.6.1 (URL in Sources); `tools/round-41/sqfs-list.py:243-245` (v4-only assert) — read, not run | observed |
| F4 | Scan coverage hole: **26 of 70** L1 rows end `err HTTP Error 416` (the tar walk runs past EOF; `scan.py` has no end guard), 4 rows `noimage` → only **40/70** rows have any superblock read. The plan draft's "of 78 FRITZ!Box model directories, dozens publish…" should cite 40 evaluated rows | count over `.ufo/waves/round-50/l1/scan-output.txt` (70 lines): `grep -c 'err HTTP Error 416'` = 26, `grep -c noimage` = 4 — not run as a command; counted from the read file | observed |
| F5 | Nine rows read `./va` at the member data: the member named `*.image` is itself an archive (4020, 4040, 6810-lte, 6842-lte, 7312, 7360-SL, 7360-v1, 7360-v2, 7390) — concretizes "nested sub-images below depth 1" | scan-output.txt rows; walk receipts in probe-run4.stdout (both verified images have 5 prior tar members: `./var/`, `./var/chksum` (278,960/278,552 B), `./var/install`, `./var/tmp/`, `./var/tmp/kernel.image`) | observed |
| F6 | AVM kernels concretized: both verified images ship `./var/tmp/kernel.image` (3272: 1,967,624 B; 7412: 2,505,736 B); both begin `8112edfe…` (not gzip, not ELF); `5d 00 00 80 00` at +28 is LZMA-alone-shaped (props 0x5d, dict 0x00800000) but the size field does not decode plausibly → unconfirmed [INFERENCE] | `python3 -I -B kernel-probe.py` exit 0 (`a9ee6d95…`); 3272 `Range: bytes=315392-315455` sha256 `f7acc433cc17961e6b607c1008deb0a1ef41004cf11df576fe1bbf46c3b87394` (23:45:32Z); 7412 sha256 `1c5622f19e70620e47d6a074d18bb3267dd52c83a275410c061ea2a77884dfa4` (23:45:33Z) | observed + inference |
| F7 | Member-size pad: the 3272 member is 3,370 B larger than its `bytes_used` (19,726,344 vs 19,722,974) — trailing pad an oracle/counter should tolerate | probe-run4.stdout walk + F1 parse | observed |
| F8 | Honest run history: three probe-script defects before the clean run (run1: Range hits return **206**, script accepted only 200; run2: body popped before header parse; run3: parse gate re-checked `== 200`). All four run receipts retained | probe-run{,2,3,4}.stdout sha256 `2a0e3787…`, `ddf8eb16…`, `3227dc63…`, `aa8df123…`; all scripts exit 0, failures are in-band receipts | observed |

## Frontier items still Frontier AFTER the LE AVM promotion (cheapest next probe each)

Sources for the list: `PROVINCE.md:438` (round-49 frontier note) and `corpus/README.md:278` (round-49 line); the `## Frontier` section at `PROVINCE.md:73-96` carries no SquashFS item — the SquashFS frontier lives in the dated round notes. After R50-C1 promotes "LE AVM members (`hsqs`)", the SquashFS/firmware remainder is:

| # | item | cheapest next probe |
|---|---|---|
| 1 | `squashfs_v2_nonstandard` (`v2ns-*`; no independent reader) | `7z l` over the committed round-44 `v2ns-*` fixtures — zero new bytes, hunts a second reader |
| 2 | `squashfs_v3_broadcom` | free half first: read unblob 26.6.4's `squashfs_v3_broadcom` handler argv in source; then one published Broadcom v3 carrier → `unblob -l` label |
| 3 | `squashfs_v3_nonstandard` + DD-WRT no-pad/4k-pad v3 | free `sasquatch -h` knob census (what mangling can the extractor undo), then one 4k-pad DD-WRT build |
| 4 | gzip v3 bodies | F1 makes 3272 a candidate two-for-one carrier (BE v3 + compressed zlib-family body [INFERENCE]): one member fetch + `unblob -l` would also move items 2/3's family — wave-2/L1 (extraction) |
| 5 | v4 Broadcom | same shape as 2: handler source read (free), then one carrier |
| 6 | v2.1 images | free and decisive: bump s_minor 0→1 in the committed `v2le` fixture bytes (scratch copy), `unsquashfs -lls` — does the independent reader admit 2.1? |
| 7 | AVM kernel images | F6 grounds them; next: one full `kernel.image` fetch + `binwalk`/`unblob -l` region scan (extraction → wave 2/L1) |
| 8 | nested sub-images below depth 1 | F5 grounds them; next: extend the range walk into 7390's inner tar to the inner superblock — still no extraction (≤1 KiB reads) |
| 9 | **NEW — genuine BE v3.0 AVM rootfs** (3272 verified F1; 7272 same L1-read shape, unverified) | 96-byte range read on 7272 (one-line change in `range-probe.py` TARGETS), then a next-round REA claim (needs a v3-capable reader first — see F3) |
| 10 | **NEW — `sqsh`+zero-header AVM container** (7412 verified F2; 7362-SL, 6840-lte same L1-read shape, unverified) | repeat `deep7412-probe.py` offsets on 7362-SL/6840-lte (3-line change), then one full-member fetch + region scan (wave 2) |

## Receipts

- Seat dir: `.ufo/waves/round-50/w1/C1Frontier/` — `range-probe.py` (`ea8b5d1c…`), `kernel-probe.py` (`00257f5c…`), `deep7412-probe.py` (`12eff75a…`), run outputs `probe-run.stdout` (`2a0e3787…`), `probe-run2.stdout` (`ddf8eb16…`), `probe-run3.stdout` (`3227dc63…`), `probe-run4.stdout` (`aa8df123…` = receipt of record), `kernel-run1.stdout` (`a9ee6d95…`), `deep7412-run1.stdout` (`8c5f8890…`). Every HTTP receipt inside carries url, Range, status (206), Content-Range, len, body sha256, UTC. No response body was persisted anywhere; no `Set-Cookie`/auth header exists (public anonymous URLs) and none was recorded.
- Commands: all runs `python3 -I -B <script> > <out> 2> <err>` from `/fast/scratch/hyaku/kaidoku-r50/C1Frontier`, exit 0 each time; failures are in-band (F8).
- Grounding fetch: plougher/squashfs-tools tag 4.6.1 `squashfs-tools/squashfs_compat.h` (raw.githubusercontent.com, `struct squashfs_super_block_3`, packed layout + `SQUASHFS_SWAP_SUPER_BLOCK_3` bit offsets); `master` and 4.6.1 `squashfs_fs.h` were also fetched and are v4-only (that negative grounds F3's source choice).
- Tooling authorization: **nothing installed or upgraded** (stdlib python3 only); pacman untouched.
- Bounds honored: lane read-only; writes only under `.ufo/waves/round-50/w1/C1Frontier*`; scratch `/fast/scratch/hyaku/kaidoku-r50/C1Frontier` (removed at yield); no fixture git; no `--data-run`; HTTP reads per image ≤ 12 requests × ≤512 B + one 96 B + eight 64 B.

## Not run / limits

- 7272, 7362-SL, 6840-lte: **not verified by this seat** (task named two); they rest on the L1 table only — which F3 shows is mislabeled for v3-era rows, so their true layout is unknown until probed (items 9/10).
- The 0x1000-0x10000 gap of 7412 (0xff fill extent, real header location) is unresolved; data at +0x10000 is high-entropy — an encrypted/scrambled body is possible [INFERENCE, no claim made].
- No extraction, no unblob/sasquatch run on vendor bytes (task forbids); items 4/7's probes that need extraction belong to wave 2 / the L1.
- gzip-body identification for 3272 rests on the v3 spec's single compressor; the metadata-block 2-byte headers would confirm — not fetched.
