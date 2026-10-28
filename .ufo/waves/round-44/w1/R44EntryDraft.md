# R44EntryDraft — R44-C1 knowledge-entry draft (SquashFS v1/v2 → Core)

Seat: `R44EntryDraft` · lane `kaidoku-shokunin` at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
· base `c29360e3ba5381a5ab69e372d0d9577970f85018` (lane main; draft claims `fc5eb54a`) ·
2026-10-28. Role: scribe/draft — author the C1 entry **in artifacts**, gather the oracle census
and superblock facts it cites, and hand it to the L1 for landing after data.

Status: draft delivered. No R44-C1 or R44-C2 value was scored here; the after-side data procedure
(`tools/round-44/c1-run.sh`) and both counters were **not** run — they belong to the L1 after the
freeze. Nothing outside my seat paths was written.

## Deliverables

| what | path | sha256 |
|---|---|---|
| entry draft (lands as `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`) | `.ufo/waves/round-44/w1/artifacts/R44EntryDraft/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` | `4d26a052d98a532762221f044628936029554abffd0c3c115a123c5613ef55c2` |
| this report | `.ufo/waves/round-44/w1/R44EntryDraft.md` | — |
| seat receipt (42 runs: argv, exit, stdout sha256, wall) | `.../artifacts/R44EntryDraft/receipt.json` | `19e5cd7109d46acc4a60df6f06ff7dc4c5f89d00b4376b00347af3c5debb6450` |
| receipt producer | `.../artifacts/R44EntryDraft/receipt.py` | `fbce27bf70bd84776decc9ea4b9539771989ad4a6820d31892d80cbb000d1aaf` |
| superblock field reader | `.../artifacts/R44EntryDraft/sb.py` | `ea4d8a17c54bbd512a7ef0275f9d0c3363b18d3374772f494606451199da6981` |
| byte-diff tool (no external comparator) | `.../artifacts/R44EntryDraft/bytediff.py` | `fb3615a2432579f1ca23459c8e7c4c936595038a1000da8cdf544106a4ab662c` |
| `cmp -l` exit-status probe | `.../artifacts/R44EntryDraft/cmpprobe.py` | `504652fc220d52ddc99d8efa28cd78aedbebfbb6ddcde0084cded3ee80c9e696` |

Scratch (disposable): `/fast/scratch/hyaku/kaidoku-r44/probe-R44EntryDraft/{rcpt,rel.html}`.

## What the entry states (all observed 2026-10-28 unless marked)

Four frozen carriers, `corpus/evidence/round-42/c2/fixtures/` (pins re-verified):
V1BE `529e1077…d631e6`, V1LE `b45925fa…3e23e71`, V2BE `79c0f388…2e2dfcc0`, V2LE
`7c62dbe3…d924f124`, all 4096 B — `squashfs_v1` (sqsh/hsqs, `s_major` 1) and `squashfs_v2`
(`s_major` 2), both byte orders.

- **Handler rule (from S112, line-cited):** the two classes share
  `_SquashFSBase.EXTRACTOR = SquashFSExtractor(3, 0x73717368)` (:75); only the `Endian.BIG, 4`
  case is special, so v1/v2 run `sasquatch -be|-le -no-exit-code -f -d {outdir} {inpath}`
  (:39-64). No new REA key. Binding must be **exact-string** per carrier, because
  `squashfs_v2` is a strict prefix of `squashfs_v2_nonstandard` (:200) and `squashfs_v3` of
  `squashfs_v3_broadcom` (:363)/`squashfs_v3_nonstandard` (:409) — a prefix comparator would let
  a v2ns or broadcom receipt satisfy a promoted carrier with no byte wrong.
- **Superblock table** (sb.py run `superblock-fields`): magic `sqsh`/`hsqs`; `s_major:s_minor`
  1:0 and 2:0; `block_size_1` 32768 (v1) / 0 (v2, 65536 truncated in the 16-bit field) with
  `block_log` 15/16; `flags` 0x00 (v1) / 0x40 (v2), equal across byte orders; `inodes` 4/5;
  `bytes_used` 177/176/201/196; mkfs times 2024-08-05T04:18:58Z, 2024-08-05T04:18:51Z,
  2023-03-09T17:06:30Z, 2023-03-09T17:05:52Z.
- **Oracle census, two independent readers agree:** `unsquashfs` 4.7.5 member digests
  (v1: apple.txt 6 B `303980bc…`, banana.txt 7 B `5a81483d…`, cherry.txt 7 B `86baf352…`;
  v2: apple1–4.txt 7 B `6181259c…`/`919fc82d…`/`2d95014e…`/`08d9b05b…`) are **byte-identical to
  the landed unblob `__output__` trees** in `corpus/evidence/round-44/oracle/`. The two byte
  orders of a version produce byte-identical census stdout (v1 `908d3f24…`, v2 `df84669f…`).
  Census holds only regular files at the root: **0 symlinks, 0 device nodes, one dir level**.
- **Frontier disclosures, measured:** v2ns — `unsquashfs` exit 1 / `7z` exit 2 (no independent
  reader), and it differs from standard v2 by **2 bytes only** (`sqsh`→`sqlz` at 0-based offsets
  2,3; `hsqs`→`zlqs` at 0,1); v3 broadcom — `unsquashfs` refuses, `7z` lists the LE fixture
  (partial reader, no REA outcome); v3 nonstandard — both refuse; gzip v3 — `unsquashfs` lists
  it (exit 0), so its Frontier status is "no C1 receipt", not "no oracle"; LZMA v3 fixture —
  `unsquashfs` refuses (`gzip uncompress failed with error code -3`). v4 broadcom / LE AVM /
  AVM kernels / nested < depth 1: unchanged, nothing measured.

## Gates and limits respected

- Did not run `tools/round-44/c1-run.sh`, `c1-counter.py`, or `c2-counter.py`; the after-side
  receipt does not exist yet, and the entry's `status:` line points at the counter's score receipt
  instead of asserting a numeric outcome.
- Read-only on the fixtures (no `chattr`, no rewrite); all extraction went to
  `/fast/scratch/hyaku/kaidoku-r44/probe-R44EntryDraft`. `git status --porcelain` shows no
  modification by this seat of any tracked file (the `D .ufo/waves/round-44/w1.ready.partial`
  line is not mine).
- No installs or upgrades; `/home/vgpnk/.omp/agent/RULES.md` read, pacman not used.
- Oracle probes only: no product code, no judge, no commit, no cross-lane surface.

## Findings for the L1 (both already messaged to `KaidokuR44`)

1. **The C1 superblock probe must not bind "compression" to `file`.** `file` 5.48 prints
   "uncompressed" for V1BE/V2BE and "compressed" for V1LE/V2LE; `unsquashfs -s` prints "Inodes
   are compressed"/"Data are compressed" for all four; the `flags` byte is 0x00 (v1) / 0x40 (v2)
   on both orders, so `file`'s word is not a function of it. Either drop the compression field or
   record the disagreement; the fixture pair is the worst case for a single-word binding.
2. **`cmp -l` exit status is unreliable at ≥ 4096 B on this host** (diffutils 3.12-2, package
   intact): `cmp -l` exits 0 on differing 4096/4097/8192-byte inputs while `cmp` and `cmp -s`
   exit 1. All four carriers are exactly 4096 B. A counter or control that reads `cmp -l`'s
   status as "equal" would green a wrong carrier. Receipt run `cmpprobe`, stdout sha256
   `d16398cb646df00b…`; use `cmp`, `cmp -s`, or digests.
3. **The exact-equality binding has a real false-accept behind it** (prefix hazard, finding 1 of
   the entry): `squashfs_v2` ⊂ `squashfs_v2_nonstandard`; `squashfs_v3` ⊂ `squashfs_v3_broadcom`
   and `_nonstandard`. A counter built with `startswith` passes a v2ns receipt for a v2 carrier.
4. **The gap rule is not exercised on this carrier set** — no symlink, no device node, one
   directory level. Any `unpublished-entry`, `MaliciousSymlinkRemoved`, `depth-limited` or
   `unknown-chunk-handler` gap on these four should be a failed carrier, so the counter must not
   tolerate them here.
5. **`squashfs_v2_nonstandard` is a magic-spelling variant**, differing from standard v2 in two
   bytes; its Frontier status is an oracle-availability statement only. If a later round obtains
   a second reader for `sqlz`/`zlqs`, the body is already measured under the v2 row.
6. Minor instrument note: `unsquashfs -version` exits 1 while printing its version string (receipt
   run `tool-unsquashfs`, exit 1) — a "tool present" check keyed on that exit would misread it.

## Landing instructions (L1, after data)

1. Copy the draft verbatim to `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`; fill
   `verified-at:` with the landing date; leave `recheck: 180d`.
2. Add SOURCES rows **S138** (unblob `__output__` dataset; the fetch manifest is
   `corpus/evidence/round-44/oracle/manifest.json`, sha256 `4bc53dbb…`) and **S139**
   (squashfs-tools releases page), each `used-by` naming this entry; the entry's `source:` lines
   already cite both by id and URL and cite S112 for handler semantics.
3. Add the `## Round-44 additions to Core` row in `PROVINCE.md` naming `squashfs_v1` and
   `squashfs_v2` and citing the entry, with a round-44 frontier note that supersedes only the
   round-42 `SquashFS v1/v2` Frontier text; add the `corpus/README.md` coverage-map row for the
   entry stem.
4. The entry asserts no counter field. If the landed `carriers.json` uses different carrier ids
   than V1BE/V1LE/V2BE/V2LE, rename them in one pass (the table and prose are the only places
   they appear).
5. If the C1 counter records a compression value, apply finding 1 before scoring; the entry's
   superblock table would otherwise disagree with the counter's field for the BE pair.

## Out of scope (not done, by contract)

After-side REA runs and receipts; counter authoring/porting; the freeze; C2's rubric and counter;
PROVINCE/README/SOURCES edits (L1 landing); any commit.
