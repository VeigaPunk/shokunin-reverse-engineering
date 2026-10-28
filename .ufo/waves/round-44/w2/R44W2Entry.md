# R44W2Entry — sentence-level audit of `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`

Seat `R44W2Entry`, round-44 wave 2. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base `c29360e3ba5381a5ab69e372d0d9577970f85018`;
freeze `c48f8a4bfd449300c975668e59aae5b5538b6a84`; admissible measured revision
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`; lane tip at dispatch
`c86ea508188c50e2645b1f9bba65df4177cda6b1` (HEAD at audit `8bb1090af3fef64477c4337855e4347472db2701`).

Method: every factual sentence in `## What was measured`, the handler section and the source
block was mapped to committed bytes and re-derived where re-derivable — fixture sha256/size,
superblock fields parsed from the four 4096-byte blobs, member census by `/usr/bin/unsquashfs`
extraction, `unsquashfs -s` / `7z l` / `file` output, the S138 oracle manifest, the S112 handler
source (vendored 26.6.4 copy, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`),
the v2ns byte diff, the v3 reader matrix, and the frozen counter re-run at **both** candidate
revisions (`4cc1ac11`, `55bcce69`) with the frozen `rea-agents 6.5.0` package. No claim, counter,
rubric, frozen byte or production doc was edited. Scratch
`/fast/scratch/hyaku/kaidoku-r44/R44W2Entry/` was removed; the two counter reproductions are kept
under `.ufo/waves/round-44/w2/artifacts/R44W2Entry/`.

## Verdict (three asked checks)

1. **Counter result and revision cited — PARTLY WRONG (D1).** The receipt the entry cites
   (`corpus/evidence/round-44/c1/counter-at-4cc1.json`) is real and reproducible: I re-ran the
   frozen counter at `4cc1ac11` and got `exit 0`, `met_target true`, `carriers_matched 4`,
   `frozen_path_changed []`, `bindings_false []`. But `4cc1ac11` is **not** the round's admissible
   measured revision. At `55bcce69` the same frozen counter returns `exit 1`, `met_target false`,
   `carriers_matched 4`, `frozen_path_changed []`, and `bindings_false =
   [province_core_section, province_core_row, frontier_note]` — the three PROVINCE/frontier doc
   bindings, i.e. the red is caused by the honest-stop doc rewrite that commit itself landed, not
   by the output-directory provenance. `run_provenance_ok` is `true` on all four carriers at both
   revisions. The entry never cites the measured-revision receipt and attributes the stop to a
   mechanism the instrument does not report there. The **verdict** ("not promoted") is still
   correct, because the claim's controls-amendment clause (`plans/round-44-claims.md:33-36`)
   requires the receipt's `parameters.output_directory` to name a `corpus/evidence/round-44/c1/`
   path and every receipt carries only the `/kaidoku-r44/` scratch form — a clause the frozen
   counter does not implement (its `BINDINGS` tuple, `tools/round-44/c1-counter.py:334-339`,
   contains no committed-path check).
2. **`v2ns` has no independent reader — CORRECT measurement, MISSING citation (D4).** The
   measurement belongs to wave-1 seat `R44LabV2ns` (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w1/R44LabV2ns.md`,
   reader matrix r1–r8, receipts at `.../w1/R44LabV2ns/receipts/`); the entry states the two
   refusals with no pointer. I reproduced both: `unsquashfs -lls` exit 1
   `FATAL ERROR: Can't find a valid SQUASHFS superblock`; `7z l` exit 2
   `Cannot open the file as archive`, on both v2ns fixtures.
3. **"Not promoted" vs `PROVINCE.md` / `corpus/README.md` — CONSISTENT.** `PROVINCE.md:424`
   (`## Round-44 measured, not promoted (R44-C1 honest stop)`), `:428` (row text ending "no Core
   promotion is claimed") and `:430` (frontier note, "R44-C1 is not promoted") plus
   `corpus/README.md:104` (`**Measured, not promoted**`), `:224` and `:275` ("remains Frontier")
   all match the entry's status. No sentence in the entry asserts a Core promotion; the words
   "Core" at entry lines 9, 156, 163 are all negations.

**Overstatement attack — result.** The entry does not overstate a promotion. It overstates
something else: it presents claim and counter as two conflicting requirements (`while … requires
…`, entry:6-8) and then reports the counter's `exit 0` as the run's result (entry:3-6). Read
together, the status block asserts both "the instrument passed" and "the claim is not met" without
the fact that separates them — the instrument's predicate is a strict subset of the claim's. At the
round's measured revision the instrument is red for a *different* reason (doc bindings), which the
entry never says.

## Freeze defect / tip state (context, not an entry defect)

- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --oneline c48f8a4b..main -- tools/round-44/`
  → only `c86ea508` (exit 0). Both counters at the tip exit 2 with the same eight
  `frozen_path_changed` entries (`.ufo/waves/round-44/l1/c1-score-at-tip.json`,
  `c2-score-at-tip.json`). The round's account of M44-2 (measure at `55bcce69`, tip is red) is
  accurate as far as it goes.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-45/frozen-path-preflight.py`
  reproduces the pair: `--rev 55bcce69 --pathspec tools/round-44` → exit 0, `verdict clean`;
  `--rev c86ea508 --pathspec tools/round-44` → exit 1, `verdict frozen_path_changed`, the same
  eight paths. It genuinely catches M44-2.
- Honest but limited: it is a post-commit detector (it needs a revision), not a commit-time gate —
  the lesson says so ("wire it into the round's commit sequence"); it has no hook. With no
  `--pathspec` it walks the whole tree, flags **every** `A` in `FREEZE..REV` as a change, and
  skips the tree backstop (`if pathspec:` guard). The round's own invocation passes
  `--pathspec tools/round-44`, which is the only correct usage and should be written down as such.

## Sentence table

Verdict key: **OK** = recomputed/committed bytes agree; **WRONG** = committed bytes contradict;
**UNSUPPORTED** = true-looking but no committed artifact in place; **IMPRECISE** = true only under
a reading the entry does not give.

### Source block (entry:12-14, :16)

| id | line | claim | supporting committed artifact (re-derived) | verdict |
|---|---|---|---|---|
| B1 | 12 | S138 URL and the `contents` API form `<v>/<endian>/__output__?ref=26.6.4` | `corpus/evidence/round-44/oracle/manifest.json` → `source.contents_api_root`, `listings[0].api_url` = `…/contents/tests/integration/filesystem/squashfs/squashfs_v1/little_endian/__output__?ref=26.6.4` | OK |
| B2 | 12 | "10 listings, HTTP 200, 2026-10-28T11:10:29Z–11:10:43Z" | manifest `counts.listings 10`, `listings_replayed 10`; every listing `http_status 200`; `fetched_at` 11:10:29…11:10:43Z | OK |
| B3 | 12 | "22 members, HTTP 200, 11:12:37Z" | manifest `counts.files 22`, `lfs_resolved 22`, all `files[].http_status 200`, `files[].fetched_at 2026-10-28T11:12:37Z`, `failures []` | OK |
| B4 | 12 | manifest sha256 `4bc53dbba8beee0fbf912771efc0a55fd47a197cca1f56d2aaed790f817c1a13` | committed manifest sha256 = **`06a72dd5b660c79adae943917abf40c24ab16554ec6c2f14985958799a78f5fe`** at `c48f8a4b`, `4cc1ac11`, `9d3d1862`, `55bcce69` and HEAD | **WRONG (D2)** |
| B5 | 13 | S139: `unsquashfs version 4.7.5 (2026/03/01)`, sha256 `461e1fd9…`, Arch `squashfs-tools 4.7.5-1`, page HTTP 200 with `4.7.5` tag | `/usr/bin/unsquashfs` sha256 `461e1fd9eac39c12e673042807459985636030d5557319343fc3a6ed4ba1677c`, `unsquashfs -version` prints that line; `pacman -Q squashfs-tools` → `4.7.5-1`; `corpus/SOURCES.md:145` (S139) records page 200 / 398943 B / tag `4.7.5` | OK |
| B6 | 14 | S112 line numbers: class 24, executables 25-26, argv 39-54, tail 56-64, deps 69, base 72-99, `EXTRACTOR` 75, v1 101-155 / 102 / 105-121 / 123-136 / 137, v2 158-196 / 159 / 161-178, v2ns 199-241 / 200 / 202 / 204 | line-by-line against the 26.6.4 vendored copy (`…/w1/artifacts/R38W2EntryBEReview/squashfs-26.6.4.py`, sha256 `2d7b901b…`): every cited line and range matches | OK |
| N1 | 16 | recheck names `sb.py` and `bytediff.py` with no path | both exist at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w1/artifacts/R44EntryDraft/` (`sb.py`, `bytediff.py`); `receipt.json` there holds the 42 runs | OK (path should be given) |

### `## What was measured` (entry:18-29)

| id | line | claim | supporting committed artifact | verdict |
|---|---|---|---|---|
| C1 | 20-21 | Before the round `PROVINCE.md` carried `SquashFS v1/v2` as Frontier (round-42 note, line 416) | `git show c29360e3:PROVINCE.md` line 416 = "Still Frontier: SquashFS v1/v2, …" (same line at HEAD) | OK |
| C2 | 21-22 | four frozen standard fixtures measured through REA 6.5.0 `extract-firmware` + independent `unsquashfs` 4.7.5 | `corpus/evidence/round-44/c1/{v1be,v1le,v2be,v2le}/{after.json,extract-env.json,extract-tree.tsv}`; `manifest.json`; `extract-env.json` pins unblob `26.6.4`, sasquatch `4.5.1`, command `sasquatch -be -no-exit-code -f -d …`; counter `oracle_tool_detail` = the same sha256/version | OK |
| C3 | 22-24 | per-carrier 4/4, exact handler, complete publication, zero gaps; provenance mismatch prevents admission | counter receipt `carriers_matched 4`, per-carrier `handler_ok`/`oracle_hits_ok`/`gaps_ok` true; `compression_detail ["gzip"×4]`; admission judgment correct (claim clause `plans/round-44-claims.md:33-36`) | OK (framing: D6) |
| C4 | 26-29 | published v1/v2 rootfs images probed: `archive.openwrt.org/whiterussian/rc6/openwrt-brcm-2.4-squashfs.trx` 404 on 2026-10-28, DD-WRT beta listing empty | **no committed HTTP receipt**: the only occurrences outside the claim text are `w1/R44Debt.md:51` (D-02 prose) and a control-tree copy of the claim; `grep -rn whiterussian` over `corpus/evidence/round-44/**.json` and `w1/**` receipts finds no capture | **UNSUPPORTED (D5)** |

### Handler section (entry:31-65)

| id | line | claim | supporting committed artifact | verdict |
|---|---|---|---|---|
| H1 | 34-38 | v1 matched by `73 71 73 68 [24] 00 01` / `68 73 71 73 [24] 01 00`, `s_major` at offset 28, `s_minor` unconstrained | source :105-121 (both `HexString`s); four fixtures' bytes 28-31 = `00 01`/`01 00` (v1), `00 02`/`02 00` (v2) | OK |
| H2 | 39-41 | v2 inherits v1, overrides only `PATTERNS` (:161-178), `00 02`/`02 00`; neither overrides `EXTRACTOR` → `SquashFSExtractor(3, 0x73717368)` (:75) | source :158-196 (`class SquashFSv2Handler(SquashFSv1Handler)` + `PATTERNS` + `DOC` only); `EXTRACTOR` absent in both v1/v2 classes; base :75 | OK |
| H3 | 43-47 | `match endian, self.version`; only `BIG, 4` special (`sasquatch-v4be`, `-be` for standard); `BIG,_ → -be`, `LITTLE,_ → -le`; tail `-no-exit-code -f -d {outdir} {inpath}` | source :39-64 verbatim | OK |
| H4 | 47-51 | the command a v1/v2 chunk runs is `sasquatch -be\|-le -no-exit-code -f -d {outdir} {inpath}` | all four `extract-env.json` → `unblob_log.command_line` = `sasquatch -be … -no-exit-code -f -d …` (v1be/v2be`-be`, v1le/v2le`-le`); round-42 v3 lane `corpus/evidence/round-42/c1/DW-FONERA/extract-env.json:25` has the same tail | OK |
| H5 | 53-55 | "no new REA key", same binary/tail as round-42 v3; endianness the only argv difference | as H4 + the base `EXTRACTOR` unchanged; round-42 command line identical tail | OK |
| H6 | 57-65 | exact handler equality per carrier; prefix hazards `squashfs_v2`⊂`_v2_nonstandard` (:200), `squashfs_v3`⊂`_v3_broadcom` (:363)/`_v3_nonstandard` (:409) | source `NAME` strings at those lines; counter `handler_detail` = `[squashfs_v1, squashfs_v1, squashfs_v2, squashfs_v2]` | OK |

### Superblock / census / compression (entry:67-109, 131-154)

| id | line | claim | supporting committed artifact | verdict |
|---|---|---|---|---|
| S1 | 69-72 | `sb.py` reads 32 bytes per `squashfs_super_block_t` (magic + six u32 + u16 major/minor; S112 :124-137) and the packed tail at 32 (`block_size_1:u16, block_log:u16, flags:u8, no_uids:u8, no_guids:u8, mkfs_time:u32`) | source :123-137 (`C_DEFINITIONS`) matches field-for-field; 32+11 = 43 ≤ 4096 | OK |
| S2 | 76-81 | magic / major:minor / order / `block_size_1` / `block_log` / `flags` / uids / inodes / bytes_used per carrier | parsed from the four blobs: `sqsh 1:0 be 32768 15 0x00 1/0 4 177`, `hsqs 1:0 le 32768 15 0x00 1/0 4 176`, `sqsh 2:0 be 0 16 0x40 1/0 5 201`, `hsqs 2:0 le 0 16 0x40 1/0 5 196` | OK |
| S3 | 76-77 | `mkfs_time` v1be `2024-08-05T04:18:58Z`, v1le `2024-08-05T04:18:51Z` | raw field epochs 1722842338 / 1722842331 → **2024-08-05T07:18:58Z / 07:18:51Z**; `04:18` is the host-local (`TZ=-03`) rendering of the same epoch. The v2 rows (`:78-79`, 17:06:30Z / 17:05:52Z) are the UTC values | **WRONG (D3)** |
| S4 | 85-88 | v2 `block_size_1` 0 = 65536 truncated; `block_log` 16 reproduces 65536; `unsquashfs -s` prints 65536 (v2) / 32768 (v1) | arithmetic holds; `unsquashfs -s` prints `Block size 65536` (both v2) and `32768` (both v1) | OK |
| S5 | 90-100 | gzip on all four; `unsquashfs -s` inode/data compressed lines, v2 adds fragments + `Number of fragments 1`; `78 da` at 73 (both v1), 63/90/140 (v2be), 63/90/138 (v2le); 7-Zip stored bytes 6/7/7 and 25-against-apple1; counter `compression_detail` `["gzip"×4]` | all four `unsquashfs -s` runs; byte scan; `7z l` tables; counter bindings | OK |
| S6 | 102-109 | `file` 5.48: BE `uncompressed`, LE `compressed`, v1 blocksize `-32768`; flips with byte order alone while `flags` and member digests are equal | `file` 5.48 output reproduced exactly on all four; `flags` 0x00/0x40 identical within version; equal member digests (below) | OK |
| S7 | 139-142 | carrier sha256 / size 4096 / handler / endian / 3-3-4-4 regular files / 0 symlinks / 0 devices / root-only dirs | `sha256sum` matches the four pins (`529e…31e6`, `b459…3e71`, `79c0…fcc0`, `7c62…f124`); `unsquashfs -lls` shows root + 3/4 files, nothing else; `carriers.json` `nonregular []` | OK |
| S8 | 148-149 | member census digests/sizes/names | `unsquashfs -d` extraction + sha256: v1 `3039…97d0` 6 `apple.txt`, `5a81…16b1` 7 `banana.txt`, `86ba…cf55` 7 `cherry.txt`; v2 `6181…1c30`, `919f…4aff`, `2d95…1ec6`, `08d9…959d`, all 7 B — identical to the table and to `carriers.json` `oracle.members` | OK |
| S9 | 151-154 | census outputs equal across byte orders: v1 `908d3f2427a4a77e…`, v2 `df84669fe894a903…`; container bytes differ (177/176, 201/196); 4 and 5 inodes | `…/w1/artifacts/R44EntryDraft/receipt.json` runs `member-sha256-V1BE` and `-V1LE` share `stdout_sha256 908d3f24…5610b`, `V2BE`/`V2LE` share `df84669f…b03c`; inodes/bytes_used as S2 | OK |

### Oracle / receipts (entry:111-182)

| id | line | claim | supporting committed artifact | verdict |
|---|---|---|---|---|
| O1 | 113-129 | `unsquashfs` independent, 7-Zip third/corroboration, unblob `__output__` same-lineage; "never two independent oracles" | `carriers.json.oracle.independence`; `w1/R44LabV2ns.md` §Independence; source shows the extractor is sasquatch; `tools/round-42/fixtures.json` provenance | OK |
| O2 | 119-121 | 7-Zip lists all four (exit 0), 3 files/20 B (v1), 4/28 (v2); digest census is `unsquashfs`'s | `7z l` reproduced: v1 3 files/20 B, v2 4/28; receipt runs `unsquashfs-extract-V1*/V2*` + `member-sha256-*` prove the census tool | OK |
| O3 | 158-166 | counter ran at `4cc1ac1`; 4/4, all carrier clauses true, no gaps, exit 0; does not meet the frozen claim because claim wants the committed path while `run_provenance_ok` wants `/kaidoku-r44/` | receipt `corpus/evidence/round-44/c1/counter-at-4cc1.json` (reproduced by me: exit 0, met true); `after.json.parameters.output_directory` = `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/…/rea-out`; claim clause `plans/round-44-claims.md:33-36`; counter `PROV_SEGMENT` `:258`, `provenance_ok` `:1176-1182` | IMPRECISE (D1, D6) |
| O4 | 168-173 | published files `firmware.bin_extract/{…}` 20/28 B, no gaps, `complete` | each `extract-tree.tsv` (3 or 4 rows, `file`, matching sha256) and `after.json.normalized_result` (`coverage complete`, `extraction_gaps []`, `unpublished_entries []`) | OK |
| O5 | 175-181 | no symlink/device/second-level dir → gap halves unbound; control-clone `per_carrier_failing {v1be: [], v1le: [], v2be: [], v2le: []}`, `gap_rule_problems []` | `corpus/evidence/round-44/controls/pos/receipt.json` → `measured.per_carrier_failing` all `[]`; `…/pos/counter.json` → `gap_rule_problems []`; `carriers.json` `nonregular []` | OK (path not given: D7) |
| O6 | 181-182 | `evidence_id_ok` and `carrier_pin_ok` per carrier | counter receipt per-carrier clauses `evidence_id_ok true`, `carrier_pin_ok true`, `subject_sha256` = the pins | OK |

### Frontier section (entry:184-211)

| id | line | claim | supporting committed artifact | verdict |
|---|---|---|---|---|
| F1 | 186-198 | v2ns: `unsquashfs` exit 1 `FATAL ERROR: Can't find a valid SQUASHFS superblock`; `7z` exit 2 `Cannot open the file as archive`; "Measured 2026-10-28 on both committed v2ns fixtures" | reproduced on both v2ns blobs (exit 1 / exit 2, exact strings); the measurement is `w1/R44LabV2ns.md` r1/r2/r6 (receipts `w1/R44LabV2ns/receipts/`) and receipt runs `unsquashfs-lls-v2ns-{le,be}`, `7z-l-v2ns-{le,be}` — **entry names no receipt** | measurement OK, citation **UNSUPPORTED (D4)** |
| F2 | 191-195 | v2ns differs from standard v2 only in the 4-byte magic, two bytes: BE offsets 2,3 (`s`→`l`,`h`→`z`), LE offsets 0,1 (`h`→`z`,`s`→`l`); all other bytes equal | diff of `v2ns-be` vs `v2-be` → offsets `[2,3]` (`sqsh`→`sqlz`); `v2ns-le` vs `v2-le` → offsets `[0,1]` (`hsqs`→`zlqs`); lengths 4096/4096 | OK |
| F3 | 199-203 | v3 broadcom: `unsquashfs` exit 1; `7z` lists LE broadcom exit 0, 2 entries | reproduced: `unsquashfs -lls v3bc-le` exit 1; `7z l v3bc-le` exit 0, `apple.txt` + `cherry.txt` | OK |
| F4 | 204-205 | v3 nonstandard: both refuse (1, 2) | reproduced on `v3ns-le`: exit 1 / exit 2 | OK |
| F5 | 206-208 | gzip v3: `unsquashfs` lists both byte orders (exit 0); LZMA v3 refused with `gzip uncompress failed with error code -3` | reproduced: `v3-le` and `v3-be` exit 0; `v3adapt-le` exit 1 with that exact first line | OK |
| F6 | 209-211 | v4 broadcom / LE AVM / AVM kernels / nested: unchanged, nothing measured | claim text and prior-round notes; no round-44 receipt claims otherwise | OK |

### Observation / inference / unknown, Limits (entry:213-243)

| id | line | claim | supporting committed artifact | verdict |
|---|---|---|---|---|
| X1 | 218-224 | Observed list incl. "the lane counter output at revision `4cc1ac1` (`carriers_matched 4/4`, instrument `met_target true`, …)" | reproduced at `4cc1ac1`; but the entry omits the measured revision's red (D1). `gap_kinds []` is a per-carrier field, not a top-level one | IMPRECISE (D1) |
| X2 | 226-228 | Inferred: v2 truncation, `file` artifact, thin regular-file-only path | as S4, S6, O5 | OK |
| X3 | 229-232 | Unknown: meaning of `flags` bit 0x40; whether other v1/v2 images extract; which process wrote the receipts | all three genuinely unmeasured; R40-CL2 | OK |
| X4 | 234-243 | Limits: thin carrier set, no symlink/device/hardlink/sparse; one fragment block; oracle is squashfs-tools; rerun cannot attest origin; receipts in `w1/artifacts/R44EntryDraft/receipt.json`; provenance `tools/round-42/fixtures.json` (commit `1fcc7a0a…`, MIT) | `carriers.json`, `7z l` (fragment accounted to apple1), `w1/artifacts/R44EntryDraft/receipt.json` exists, `tools/round-42/fixtures.json` pins `1fcc7a0a584a70a96c31f5a276c20944d199a089` | OK |

## Numbered defects

D1 — **Entry status cites a superseded revision and a red the instrument does not report.**
Path: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:3-9`
(repeated at `:158-166` and `:224`).
Command (fresh work dir, frozen counter sha256 `9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993`):

```
python3 -I -B tools/round-44/c1-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work /fast/scratch/hyaku/kaidoku-r44/R44W2Entry/c1work55 \
  --json-out /fast/scratch/hyaku/kaidoku-r44/R44W2Entry/c1-55.json
```

Exit **1**. Observed: `met_target false`, `carriers_matched 4`, `frozen_path_changed []`,
`bindings_false ["province_core_section","province_core_row","frontier_note"]`,
`carriers.*.run_provenance_ok true` for all four. Same command at `--rev 4cc1ac11` → exit **0**,
`met_target true`, `bindings_false []`. The committed receipts agree
(`.ufo/waves/round-44/l1/c1-score-at-55bcce69.json`, `corpus/evidence/round-44/c1/counter-at-4cc1.json`).
The entry never cites the `55bcce69` receipt, and the honest-stop reason it states
(provenance) is not the binding that is false at the measured revision — the stop doc landing
itself flipped `province_core_section`/`province_core_row`/`frontier_note` to false. Action for
L1: cite the measured-revision receipt and say (a) claim clause `plans/round-44-claims.md:33-36`
fails on the receipts, (b) the instrument's `met_target true` at `4cc1ac11` is over a predicate
that omits that clause, (c) the instrument's red at `55bcce69` is a doc-conformance red produced by
the stop landing, not a provenance red.

D2 — **Wrong S138 manifest digest in the source block.**
Path: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:12`.
Command: `sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-44/oracle/manifest.json`
→ exit 0, `06a72dd5b660c79adae943917abf40c24ab16554ec6c2f14985958799a78f5fe`; the same digest is
produced by `git show <rev>:corpus/evidence/round-44/oracle/manifest.json | sha256sum` at
`c48f8a4b`, `4cc1ac11`, `9d3d1862`, `55bcce69`, `8bb1090a`. The cited
`4bc53dbb…c1a13` exists only as prose (entry `:12`, `corpus/lessons/round-44.md:24`, and the
control-tree copies of the entry); no committed file has it. Action for L1: replace with
`06a72dd5…` (and fix `corpus/lessons/round-44.md:24`, same string).

D3 — **Two `mkfs_time` cells are local time labelled UTC.**
Path: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:76-77`.
Command: parse `mkfs_time` u32 at offset 39 in the carrier's byte order, then
`datetime.fromtimestamp(e, UTC)` → `1722842338` = `2024-08-05T07:18:58+00:00`,
`1722842331` = `2024-08-05T07:18:51+00:00`; `date +%Z%z` = `-03-0300`, and `unsquashfs -s` prints
`Creation or last append time Mon Aug 5 04:18:58 2024` (local render). Observed entry values
`04:18:58Z` / `04:18:51Z` are therefore 3 h early under a `Z` label; the v2 rows on `:78-79` are
correct UTC. Action: `07:18:58Z` / `07:18:51Z`, or drop the `Z`.

D4 — **`v2ns` no-reader measurement carries no receipt pointer.**
Path: `…/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:186-190`.
Command: `/usr/bin/unsquashfs -lls corpus/evidence/round-42/c2/fixtures/v2ns-le--squashfs_v2.0_le.bin`
→ exit 1, `FATAL ERROR: Can't find a valid SQUASHFS superblock`; `/usr/bin/7z l …` → exit 2,
`Cannot open the file as archive`; same for `v2ns-be`. The measurement's home is
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w1/R44LabV2ns.md` (r1/r2/r6,
receipts under `.../w1/R44LabV2ns/receipts/`) and the R44EntryDraft receipt's
`unsquashfs-lls-v2ns-*`/`7z-l-v2ns-*` runs. Action: cite the seat or the receipt runs.

D5 — **Negative rootfs probe has no committed capture.**
Path: `…/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:26-29`.
Command: `grep -rn whiterussian /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/
--include=*.json --include=*.md --include=*.txt` → only `w1/R44Debt.md:51` (D-02 prose) and a
control-tree copy of the claim; `grep` over `corpus/evidence/round-44/**` finds nothing. The round's
own frozen-URL convention (M44-1) is "a URL is pinned only after a successful open"; a 404/empty
listing needs its dated capture too. Action: attach the 404 receipt and the DD-WRT listing capture,
or soften to "no published v1/v2 carrier was obtained".

D6 — **The claim/counter framing reads as unsatisfiability; it is under-specification of the
instrument.**
Path: `…/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:6-8`.
The claim clause (`plans/round-44-claims.md:33-36`) says `parameters.output_directory` "must name
a `corpus/evidence/round-44/c1/` path"; the predicate clause (`:137-139`) requires the
`/kaidoku-r44/` segment. One absolute path can contain both segments, so the contract is
ambiguous, not impossible; what failed is that the four receipts carry only
`/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/…/rea-out` (observed in every
`after.json.parameters.output_directory` and `provenance.json.rea_output_directory`).
`tools/round-44/c1-counter.py:334-339` has no committed-path binding at all — only
`provenance_ok` (`:1176-1182`, `PROV_SEGMENT` at `:258`). Action for L1: state "the receipts carry
only the scratch form and the frozen counter implements only that clause", not "the claim and
counter disagree", so round 45's R44-CL2 fixes the wording/outdir shape rather than assuming an
impossible contract.

D7 — **Control-clone evidence path not given, and the field is nested.**
Path: `…/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:179-181`.
`corpus/evidence/round-44/controls/pos/receipt.json` → `measured.per_carrier_failing` is the
all-empty dict quoted; the **top-level** `per_carrier_failing` key is `null` in every control
receipt and counter. A re-reader grepping the top level will think the claim unsupported. Action:
name the artifact pointer (`…/controls/pos/receipt.json` `measured.per_carrier_failing`).

## Receipts written by this seat

| seat | command | exit | stdout sha256 | wall |
|---|---|---|---|---|
| R44W2Entry | `python3 -I -B tools/round-44/c1-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work /fast/scratch/hyaku/kaidoku-r44/R44W2Entry/c1work55 --json-out /fast/scratch/hyaku/kaidoku-r44/R44W2Entry/c1-55.json` | 1 | `eea45d374bb450f15c549ca5e7c7803ac9e6c31bb982fae45d6542ee8cac9f8d` (stdout) | 7.42 s |
| R44W2Entry | same with `--rev 4cc1ac11657590c25b6565d6ab220f53372a94d3 --work …/c1work4c --json-out …/c1-4c.json` | 0 | `8742a90d9b879fbf91f77c5862273be788911ace1d2228e79cd6b9ad2d8fee6a` (stdout) | 6.93 s |

Full JSON receipts (sha256 `13218da65719b4ec8859505b19105624876dac31c3cca3a3b04f96a128b21f4e` and
`8cf462346211bb0ee8c5402d9e66c3a5a532b71c50cd3e1a31461c77dfb95621`) are archived at
`.ufo/waves/round-44/w2/artifacts/R44W2Entry/c1-at-55bcce69.json` and `c1-at-4cc1ac11.json`, with
their stdout files. stderr was empty (`e3b0c442…b855`) on both.

## Residual risk and verification gaps

- The two counter runs used the frozen `rea-agents 6.5.0` tree and reproduced the committed
  receipts' status/exit exactly; they do not re-establish *who* wrote the committed receipts
  (R40-CL2, unchanged).
- C2 (80/80, exit 0 at `55bcce69`) was read from
  `.ufo/waves/round-44/l1/c2-score-at-55bcce69.json`, not re-executed — outside this seat and not
  referenced by the entry.
- The measured-revision red has two possible readings I did not separate further: the three doc
  bindings are false because the stop landing removed the promotion section (as stated), and any
  alternative would require the counter's province parser to reject a differently-named section —
  visible in `tools/round-44/c1-counter.py:2154-2161`, `province_core_rows_seen []`.
- D3 depends on host `TZ=-03`; the error is in the label, not the arithmetic — in any timezone the
  field's UTC value is `07:18:5xZ`.
- No tool was installed or upgraded; nothing in `~/.local/bin`, `MANIFEST.json`, `.ufo/state/`,
  `.ufo/watchdog.log`, `.scratch/`, `templates/` or `scripts/` was touched. The only lane writes
  are this report and `artifacts/R44W2Entry/`.
