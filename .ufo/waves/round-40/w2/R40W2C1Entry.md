# R40W2C1Entry — line-by-line review of the R40-C1 entry `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`

**Verdict: CONFIRMED.** I attacked every `source:` row (all six re-opened 2026-10-26, S126 included), every number in the measured table against the frozen receipts, oracles and `after.json`, the r39 correction pointer by line number, and the layout-identity paragraph with fresh runs of the frozen reader on all four carriers (both vendor carriers rebuilt from the pinned chain at the freeze). **No inaccurate or unsupported sentence found.** Three wording nits and three calibration/registry notes, listed below; none changes the entry's verdict ("measured, not promoted", honest stop at 3/4).

Evidence I generated is in `.ufo/waves/round-40/w2/artifacts/R40W2C1Entry/` (01 fetch receipt, 02 reader verification, 03 source checks, 04 receipt extracts). Vendor bytes stayed in scratch and are cited by sha256 only.

## 1. Source rows re-opened

| id | entry says | re-opened evidence (2026-10-26) | verdict |
|---|---|---|---|
| S124 | "the reader patch that swaps only the 2-byte metadata block length" | Patch fetched at the pinned Freetz-NG commit, sha256 `7f0a1b25…0220fc` (= SOURCES anchor). It patches only `read_block`: raw 2-byte read + conditional `c_byte` byte-swap under `swap_block_length`, set from `TARGET_FORMAT == AVM_BE` and host endianness; the non-AVM branch keeps `swap_block_length = swap`. Nothing else swapped. | ✓ |
| S125 | "`info_en.txt`: FRITZ!Box 6490 Cable, FRITZ!OS 07.57" | Listing sha256 `063ec39a…f7bc`, `info_en.txt` sha256 `6c601b34…70a7` — both equal the SOURCES anchor. Lines 8-14: "Product: FRITZ!Box 6490 Cable / Version: FRITZ!OS 7.57 / Release date: 04.09.2023". Nit N2: the file writes "FRITZ!OS **7.57**"; "07.57" is the image-filename and `var/content` form (`Version=07.57`). | ✓ |
| S126 | lineage: round-11 lead's 4096-byte genuine AVM-BE image, unblob ran `sasquatch-v4be -no-exit-code -f -d …` with no `-be`, four files; image sha256 `c7f74691…`, first header `7400` → LE 116, `121 + 2 + 116 = 239 = directory_table_start` | TSV re-read: `unblob_command` `sasquatch-v4be -no-exit-code -f -d {outdir} {inpath}`, `unblob_be_flag` absent, `extracted_files` apple1-4, magic `sqsh`, `image_mkfs_time 365 == image_bytes_used 365`. Image re-hashed in place: sha256 `c7f74691…d32d`, 4096 B ✓. Superblock re-parsed: `inode_table_start 121`, `directory_table_start 239`, first header `7400` → LE 116, `121+2+116=239` exact; BE 29696 fails. The sha256 lives in the SOURCES row and the arithmetic in `w1/R40AssimE3.md` §2 (not in the TSV); both re-derived here from the image bytes. | ✓ |
| S114 | "line 8, block length little-endian; lines 13-14, the marker" | Live file: the block-length sentence spans lines **8-9** (starts at 8); the marker sentence spans lines **13-14**. Nit N1: "line 8" alone truncates the sentence (the claims file shares this). | ✓ |
| S112 | "lines 44-50, `is_avm = header.bytes_used == header.mkfs_time`; `-be` only when false" | `squashfs.py` at tag 26.6.4 fetched, sha256 `2d7b901b…9287` — equals the installed unblob 26.6.4 handler digest recorded in w1. Lines 40-58: `case Endian.BIG, 4:` at 40, `is_avm` at 48, `commands_args.append("-be")` at 50. The cited span 44-50 contains the block. | ✓ |
| S121 | "lines 664-669 (`read_block` swaps the block-length header only when `swap` is set) and 4390-4394 (`-be` sets `swap`)" | `unsquashfs.c` fetched, sha256 `ece42b66…cb40` (= SOURCES pin, 4619 lines). `read_block`: `if(swap) { read; c_byte = byteswap }` at 664-668, else raw read 669-670. `-be`: `strcmp` at **4389**, `swap = 1` at **4393** (the `#if/#else/#endif` arm 4390-4394). Nit N3: substance is 664-**670** and 4389-4394; both citations land on the right code. | ✓ |

S126 scope compliance: the SOURCES row scopes S126 to the round-11 observation and the image's own fields, "nothing about vendor firmware or about the layout test" — the entry uses it only in the Lineage paragraph. ✓. S125 is cited only for V1 identity. ✓.

## 2. Measured table vs receipts and oracles

Sources: `.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json` (counter, exit 1, matched 3/4, `met_target: false`, projection `plus-extractor`), `corpus/evidence/round-40/c1/{V1,V2,L1,L2}/{after.json,run.json,oracle.tsv,nonregular.tsv}`.

| entry claim | receipt/evidence | verdict |
|---|---|---|
| V1: 697 published = oracle; gaps 263 `unpublished-entry` + 1 `depth-limited`; one `squashfs_v4_be` chunk, not failed | receipt `oracle_files 697 / oracle_hits 697 / published_files 697`; after.json gap kinds `{unpublished-entry: 263, depth-limited: 1}`; single chunk `squashfs_v4_be, extraction_failed false, range [0, 5442392)` | ✓ |
| V2: 8 (one is the nested `filesystem_core` image); 85 + 1; same chunk | oracle row `filesystem_core.squashfs` present; receipt 8/8/8; gaps `{85, 1}`; chunk `[0, 26013550)` not failed | ✓ |
| L1: 7; 2 + 1 | receipt 7/7/7; gaps `{2, 1}` | ✓ |
| L2: 6; 2 + 1 | receipt 6/6/6; gaps `{2, 1}` | ✓ |
| carve lengths: V1 member `./var/remote/var/tmp/filesystem.image` → 5442392; V2 `./var/tmp/filesystem.image` → 26013550; carrier pins | `fetch-vendor.py --rev 7fce3086…` rerun today: exit 0; image sha256s `f518ce6b…` / `3948449d…` match claims and SOURCES S125; member sha256s `334e56df…` / `cacc6461…`; carrier sha256s equal the frozen pins (`ac4098bd…8e95`, `5ccc7614…089b`) | ✓ |
| "directories and the character device `dev/led` are invisible (no gap, no file)" | V1 nonregular.tsv: `dev/led  char-device  247:0`; V1 after.json has no device gap and 697 files = oracle count; V2 has its own `dev/led` row, same invisibility | ✓ |
| "absolute symlinks are re-rooted and kept as one gap each, and no symlink escapes" | V1: 29 absolute links, e.g. `data/tam → ../var/InternerSpeicher/FRITZ/voicebox`, `dev/new_led → null`; L1 `etc/mtab → ../proc/mounts`; L2 `bin/busy → ../usr/bin/busy`; `MaliciousSymlinkRemoved` count 0 in all four after.json; every symlink yields exactly one `unpublished-entry` (kinds all `symlink`) | ✓ |
| "The counter re-runs REA on each carrier at scoring time and compares the `plus-extractor` projection" | receipt `projection_ok: true`, `projection_diff: []` for all four; `projection_profile: plus-extractor` | ✓ |
| toolchain "REA 6.5.0 (unblob 26.6.4, sasquatch-v4be 4.5.1 on the child PATH)" | run.json: rea 6.5.0, unblob 26.6.4 sha `0ce7b624…`, sasquatch_v4be 4.5.1 sha `fac88740…` | ✓ |
| "L2 failed only `nonregular_unpublished_ok` … path-suffix test reads the published regular file `usr/bin/busy` as the symlink `bin/busy` … L2's receipt publishes no symlink path" | receipt L2 `matched: false`, every other per-carrier binding true; `nonregular_published: ["firmware.bin_extract/usr/bin/busy"]`; nonregular.tsv symlink `bin/busy → /usr/bin/busy`; L2 after.json publishes 6 regular files, its 2 symlinks appear only as unpublished entries | ✓ |
| "matched 3 of 4 at `42c10a58`", honest stop, "Promotion waits for a re-frozen counter" | receipt exit 1, `carriers_matched: 3`, `met_target: false`; entry title carries "measured, not promoted" | ✓ |
| "REA records no extractor argv on success" | `grep -c sasquatch` in all four after.json = 0 (artifact 04); w1 R40C1ReconGaps §4 G10 | ✓ |
| "Vendor bytes are not committed … `fetch-vendor.py` rebuilds them from URL → image sha256 → tar member → carve length → carrier sha256" | exactly the chain the tool printed and reproduced (artifact 01) | ✓ |

## 3. The layout-identity paragraph (sharpest attack)

Entry: "Walk the metadata headers from `inode_table_start` reading each 2-byte length little-endian (mask `0x8000`); on an AVM body the walk lands exactly on `directory_table_start` and the big-endian reading does not … On the four round-40 carriers and on the 7490 07.62 and 7430 07.31 development members the identity is exact (`…/R40C1ReconGaps.md` §2)."

- **Receipt nuance (found, resolved).** The counter's `le_identity`/`be_identity` are the *single-block* identity (`its + 2 + len == dts`, c1-counter.py:564-565). Receipt: V2/L1/L2 `le_identity: true`; **V1 `le_identity: false`, `meta_signal: plausibility`** — V1's inode table is multi-block (8574 B), so the single-block identity cannot fire, and layout_ok there rests on LE-plausible/BE-implausible (1380 vs 25605 > 8192). A reader checking only the counter receipt could mistake V1 for a plausibility-only call.
- **Independent re-verification at the working tree** (tools unchanged: `git diff 42c10a58 4d62ee5a -- tools/round-40 corpus/evidence/round-40/c1` is empty): `sqfs-list.py --layout auto` resolves all four carriers to `layout: avm, header_endian: little` — signal `exact` on V2/L1/L2, `plausibility` on V1 — and each auto file list is byte-identical to the committed `oracle.tsv`. Forcing `--layout avm` (little-endian headers, no auto decision) also exits 0 on all four with file lists identical to the oracles. The reader's chain walk raises `SqfsError` unless it lands **exactly** on `directory_table_start` (sqfs-list.py `_walk_metadata_chain`), and every one of the 697/8/7/6 sha256s matched, so the little-endian walk landing exact is re-established on all four carriers. The BE reading overshoots on all six images (25605 / 16386 / 9347 / 7555 at the first header).
- **Verdict:** the sentence is **true**; the mechanism and the exactness hold. Calibration note C1: the parenthetical citation (ReconGaps §2) covers only the two development members; the committed record of four-carrier exactness is c1-extra `oracle_rederived: ok` ×4 (at 42c10a58) plus reruns like this one — the counter receipt's identity field shows `false` for V1.

## 4. r39 correction pointer

`corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md:40` contains verbatim "An image whose `mkfs_time` equals `bytes_used` loses `-be` and fails" (the entry quotes it exactly), and line 41 already carries the round-40 bracket pointing at this entry's **Correction** heading with the same standard-BE scoping the entry asserts. The narrowing matches w1 `R40C1MarkerBoundary` H1/H2 (both CONFIRMED on development images, including the `--endian avm` = marker-transform identity). ✓

## 5. Inaccurate / unsupported sentences

None material. Nits (cosmetic, do not change any claim):
- **N1** S114 "line 8" — the block-length sentence spans lines 8-9.
- **N2** S125 "FRITZ!OS 07.57" — `info_en.txt` writes "FRITZ!OS 7.57" (07.57 is the filename / `var/content` form).
- **N3** S121 ranges "664-669" / "4390-4394" — substance sits at 664-670 and 4389-4394.

## 6. Calibration / registry notes (not entry defects)

- **C1** (from §3) — V1's four-carrier "identity is exact" is not visible in the counter receipt (`le_identity: false`, `meta_signal: plausibility`); cite c1-extra `oracle_rederived` or a rerun if the sentence needs a receipt-level anchor.
- **C2** V2's identity ("FRITZ!Box 6820v1 LTE FRITZ!OS 07.30") has no SOURCES row: it rests on frozen `carriers.json` (URL, product, pins), `V2/provenance.json`, and the 6820 directory listing (re-opened: `FRITZ.Box_6820v1_LTE-07.30.image` present). S125's scope explicitly excludes "other FRITZ!OS versions". Acceptable for a measured table; not source-backed.
- **C3** The S114 SOURCES anchor still lacks the block-length quote the entry leans on (w1 `R40SrcFreetz` recommended folding it in; the row anchor names only the opening line and the marker). Related, resolved: the claims' "V1 … 117 directories" matches the reader's count including root; `nonregular.tsv` lists 116 rows because root is omitted.

## 7. Residual risk and verification gaps

- I ran no REA/unblob/sasquatch process. "No `-be`" for the four carriers therefore remains an inference from the handler source plus the measured marker/layout facts — exactly as the entry's Limits sentence discloses; committed direct `unblob -v` logs exist only for development images (w1 MarkerBoundary, ReconGaps).
- `fetch-vendor.py` was rerun at the freeze rev; the entry's recheck line names `--rev main`. Same pins either way while `carriers.json` is unchanged (frozen C1 data; tools and C1 evidence unchanged 42c10a58→4d62ee5a).
- I did not re-run `c1-counter.py`/`c1-extra.py` (L2 already adjudicated by the L1; my scope is the entry text) and did not re-check the PROVINCE/README bindings (counter receipt binds true).
- Reader rerun used the working tree at `0b15c8b2`; the empty diff above makes it byte-identical to the measured revision for the paths that matter.

## 8. Bounds and tooling compliance

No tool installed, upgraded or removed; no pacman transaction; sasquatch/sasquatch-v4be/unblob untouched. Writes confined to this report and `.ufo/waves/round-40/w2/artifacts/R40W2C1Entry/`. Scratch `/fast/scratch/hyaku/kaidoku-r40/R40W2C1Entry` (vendor cache included) removed at exit; vendor image/carrier bytes never copied into the lane — cited by sha256 only. Shokuknow read-only: one TSV read, one image hashed and header-parsed in place. Only read-only git (`diff`, `log`, `status`). No subagents, no background jobs, no `agent://all`.

Report: .ufo/waves/round-40/w2/R40W2C1Entry.md
