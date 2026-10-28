# W2C1Entry — post-landing attack on `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`

Seat: W2C1Entry (leaf, read-only on the lane). Revision attacked: `29883d4ec35a31a8393c4ffb220888c44c0bb022` (lane `main`). Freeze: `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d` (ancestor of REV; `git diff --stat decc5697 29883d4e -- tools/round-49 plans/round-49-claims.md` empty). Entry bytes read from `git show 29883d4e:corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` (154 lines, sha256 `e2633e0e151ccdff972c1d7032d06b895ea481bfb33de964b6368b96e62fc0d3`). Entry sha256 at REV is the same value; no placeholder (`MEASURED`, `TODO`, `TBD`, `<…>`) remains.

## Verdict

**The entry's measured numbers reproduce; the entry does not yet meet its own citation and disclosure rules.** Not a fabrication finding. Eight items (D1–D8) need repair in non-frozen text; D9–D17 are low. D1 is a missing committed artifact that the entry's promotion verdict depends on.

- The frozen C1 counter, run by me at REV on a scratch copy of its frozen blob (sha256 `ac83715b…`), returns exit 0, `carriers_matched 4`, `failing []`, `frozen_path_changed []`, `bindings_false []`, `met_target true`. At `4aabb0b4` the same run returns `carriers_matched 4`, exit 1, with exactly the six documentation bindings false that the entry names. No counter defect found inside the entry's scope.
- All 46 receipt stdout captures recompute to the `stdout_sha256` column of `receipts.tsv`; every receipt id the entry names exists, with matching UTC, exit and 16-hex prefix.
- Carrier sha256, sizes, superblock fields, zlib offsets, unsquashfs member census (sha256, size), 7-Zip listings and the S112 line citations all reproduce from committed bytes or from the pinned external snapshot.

## Findings (ordered by weight)

| id | severity | attack | defect (exact) | evidence |
|---|---|---|---|---|
| D1 | high | Status line, promotion verdict | The entry names `.ufo/waves/round-49/l1/scores/c1-final.json` as the score "at the landing revision". That path does not exist in the worktree or at REV. `c1-at-landing.json` exists on disk but is **untracked** (`git status` `??`); no landing score is committed. The verdict the promotion depends on is not retrievable from the commit. | `git cat-file -e 29883d4e:.ufo/waves/round-49/l1/scores/c1-final.json` → absent; `…/c1-at-landing.json` → "exists on disk, but not in 29883d4e"; `ls .ufo/waves/round-49/l1/scores/` lists `c1-at-3847f393.json`, `c1-at-data-4aabb0b4.json`, `c1-at-landing.json`, `c2-*.json`. My re-run at REV (below) reproduces exit 0, so the claim holds; the artifact does not. |
| D2 | high | "What the scored receipts show"; recheck line 9 | The committed run was not a plain REA run. Every `after.json` `engine.executable_path` is `/fast/scratch/hyaku/kaidoku-r49/probe-R49C1Run/c1-run.<id>.<pid>/unblob-tee.sh` (sha256 `28956884f690402e7d1ab17cfd542e66114d7c503914adcb42b52c23111883b6`), reached through `REA_UNBLOB_COMMAND`, a logging tee that runs the real unblob 26.6.4 (`~/.local/share/uv/tools/unblob/bin/unblob`, sha256 `0ce7b624…`). The entry never mentions the wrapper, its sha, or `REA_UNBLOB_COMMAND`. `provenance.json` and `extract-env.json` record it; `run.json` `command` starts with `REA_UNBLOB_COMMAND=…`. The counter's own rerun sets `REA_UNBLOB_COMMAND` to `~/.local/bin/unblob` (counter line 1881, 1894), which resolves to the same uv binary but not through the tee. QUALITY 18 (retain producing argv/environment) and 30 (argv/env overrides retained). | `git show 29883d4e:corpus/evidence/round-49/c1/v1le/extract-env.json` (`log_tee`, `notes`); `…/v1le/after.json` `normalized_result.engine`; `…/v1le/run.json` `command`; `~/.local/bin/unblob` readlink + sha. `grep -c 'REA_UNBLOB\|unblob-tee\|log tee' entry.md` → 0. |
| D3 | medium | Entry lines 7 and 33 (receipt paths) | Two relative paths do not resolve from the lane root: `artifacts/squashfs-26.6.4.py` (line 7, "the snapshot is") and `scripts/sb.py` (line 33). Both live under `.ufo/waves/round-49/w1/C1ScribeEntry/`. Neither exists at REV (`git cat-file -e 29883d4e:scripts/sb.py` → absent). QUALITY 1. |
| D4 | medium | Receipts table row `counter-fixed-path`; line 27 ("FIXED_PATH includes `~/.local/bin`") | The receipt's command is `sed -n 266,272p .ufo/waves/round-49/draft/tools/round-49/c1-counter.py`. The entry's abridgement drops `.ufo/waves/round-49/draft/` and shows `tools/round-49/c1-counter.py`, which is the frozen file. The receipt's stdout (lines 266-272 of the draft, containing `FIXED_PATH = …`) matches no committed draft revision: at `14936cb9` and in the worktree, lines 266-272 are `PROV_BASE`/`REA_PIN`/…; `FIXED_PATH` sits at line 276. Run against the frozen counter, `sed -n 266,272p` also prints `PROV_BASE`…. The entry's sentence is still true of the frozen counter (lines 276-280 include `~/.local/bin`), but the receipt does not evidence it. | `git show decc5697:tools/round-49/c1-counter.py | sed -n 266,272p` → `PROV_BASE …`; `…grep -n 'FIXED_PATH = '` → 276; `.../w1/C1ScribeEntry/counter-fixed-path.out` first line `# lookups use one fixed PATH…`. |
| D5 | medium | Line 53-54 (unsquashfs flags); superblock table; "Duplicates" omission | `unsquashfs -s` prints `Duplicates are removed` for all four carriers, including the two v1 images whose `flags` byte the entry reads as `0x00`. The entry quotes the `unsquashfs -s` lines selectively and does not mention this, although its own unknown-section says the meaning of the flags bit is unknown. Under the v2 reading (0x40 = duplicates), v1 should not print that line; the entry therefore has an unresolved conflict between its flags column and the second reader on the v1 pair. | `grep -c 'Duplicates are removed' .ufo/waves/round-49/w1/C1ScribeEntry/unsquashfs-s.out` → 4; the two v1 blocks show flags 0x00 in `sb-decode-v2`. |
| D6 | medium | Superblock section (lines 31-44); QUALITY 5 | The tail fields (`block_size_1`, `block_log`, `flags`, `no_uids`, `no_guids`, `mkfs_time`) are decoded from a "draft layout" at offset 32, and then reported under "Read as observations". S112's v1/v2 struct (`C_DEFINITIONS` :123-136) stops at `s_minor`; the same tail exists only in S112's **v3** struct (:296-301), which the entry does not cite. Only `unsquashfs -s` block size, inode count, filesystem size and time are an external check. Layout-derived claims are inference under QUALITY 5. | `awk 'NR>=284&&NR<=302' artifacts/squashfs-26.6.4.py` (v3 struct); `NR>=123&&NR<=137` (v1 struct, no tail). Independent decode (my code) reproduces every table cell, so the values are right; the label is wrong. |
| D7 | medium | Lines 106-107 ("this round"); QUALITY 18 | Promotion scope uses the floating phrase "this round": "Nothing in this round measures a non-gzip v1/v2 body" and "nothing was measured for them this round". QUALITY 18: promotion evidence names its historical round/date instead of "this round". | `grep -n 'this round' entry.md` → lines 15, 102, 106, 107 (15/102 are "this round"-scoped too; 106-107 are the promotion-scope uses). |
| D8 | medium | Recheck line 9; Status line; QUALITY 8 | REA 6.5.0 (the tool whose behaviour the claim measures) is not pinned in the status paragraph or the body; the only occurrence in the whole entry is the recheck command (`--pkg65 <rea-agents 6.5.0 root>`). QUALITY 8 requires the pinned tool/provider version on capability claims. | `grep -c '6\.5\.0' entry.md` → 1. |
| D9 | low | Line 5-6 headline | "matched 4/4 at the data commit" is stated without the data-commit verdict (exit 1, six bindings false), which the status line does mention later in the same paragraph. The headline alone could be read as a met claim at `4aabb0b4`. QUALITY 34 (record the red result beside the green). | `c1-data.json` exit 1, `bindings_false` six names (my re-run). |
| D10 | low | Line 3 (archive of counter's own bytes); counter limit (not patched) | The counter records `counter_sha256` of its own argv path. Run from a pipe (`python3 -I -B <(git show …:tools/round-49/c1-counter.py) …`) it reports `counter: /dev/fd/63`, `counter_sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (sha256 of the empty string), `carriers_matched 4`, `bindings_false []`, exit 0. The entry quotes `ac83715b…` as the counter's identity without saying that C1 does not bind its own bytes (C2 does, exit 2 `counter_not_frozen`). This is a counter limit, reported not patched. | `.../w2/W2C1Entry/receipts.tsv` (not included; scratch-only run); re-run with the on-disk frozen copy gives `ac83715b…`, exit 0. |
| D11 | low | Line 27-28 / 102-107 receipts | Receipt `province-416` is not reproducible under this host's `cut -c`: the same `sed -n 410,420p … | cut -c1-240` at `14936cb9` yields sha `1eaa045d…`, not the receipt's `1c5c62cd…`; the `.out` differs in multi-byte `→` lines. The receipt is historically valid for its byte locale; the entry should say so or cite a byte-cut. | `git show 14936cb9:PROVINCE.md | sed -n 410,420p | cut -c1-240 | sha256sum`. |
| D12 | low | Line 33 ("tail offsets are the draft layout") | The argv-decision range is cited as `:37-54` (line 21) and `:39-54` (line 23). Line 37 is `executable = self.EXECUTABLE`; the `match` starts at 39. Harmless, but one range is wrong. | `awk 'NR>=37&&NR<=39'` on the S112 snapshot. |
| D13 | low | Line 46 (zlib streams) | "The carrier bytes carry zlib streams at `78 da`" is established only by a two-byte header scan (`sb-decode-v2` field `zlib_78da_offsets`), not by decompression. Stated as observation. QUALITY 5. | `[i for i in range(len(b)-1) if b[i:i+2]==b'\x78\xda']` reproduces the offsets; no inflate was run. |
| D14 | low | Line 96 ("the run's output_directory is a path under `…/probe-R49C1Run/`") | Correct as written (`output_directory` prefix verified on all four), but the data run's output tree is named `probe-…`, which a later reader will read as a probe. Name the run directory once in the entry. | `after.json` `parameters.output_directory`. |
| D15 | low | Line 106/107 (non-gzip, unmeasured) | "[INFERENCE]" marker present (good); the "no hard link" statement in Limits is not measured (`unsquashfs -lls` shows no `l` rows but does not report hard links; 7-Zip not checked for them). Mark as unmeasured or measure. | `unsquashfs-lls.out` has no hard-link marker; not re-tested. |
| D16 | low | Line 85-86 / S138 membership | The entry says "The S138 expected trees contain 22 members … because they also hold the v2.1 outputs" — verified (manifest: `squashfs_v2/{little,big}_endian` 8 each = v2.0 + v2.1; v1 3 each). OK. Not a defect; recorded so L1 does not re-open it. | `git show 29883d4e:corpus/evidence/round-44/oracle/manifest.json` → 22 files. |
| D17 | low | Line 71-73 (round-42 held-out claim, not in the entry's own text but in the entry's gzip-v3 bullet) | "the gzip v3 fixtures are round-42 C2 held-out inputs" — not found in `corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md` (grep `held-out|held out` → no hit); the backhand/7-Zip oracle sentence **is** there (line 36). Unverified; cite the line or drop "held-out". | `git show 29883d4e:corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md | grep -n -i 'held'`. |

## Claim-by-claim table (claim | resolves? | evidence)

Legend: YES = reproduced by me from committed bytes or the pinned snapshot; RCPT = receipt stdout hash matches, command not re-run; PART = partly true or label wrong; NO = fails.

| # | claim (entry line) | resolves? | evidence |
|---|---|---|---|
| 1 | Landing score `c1-final.json`, counter `ac83715b…` (3) | NO (path) / YES (sha) | D1; `counter_sha256` of frozen blob `ac83715b199100774873389ea33fb4819231e1f963225416e86ad422f69d287f` (`git show decc5697:tools/round-49/c1-counter.py | sha256sum`) |
| 2 | Landing verdict carriers 4/4, bindings true (re-run) | YES | `python3 -I -B c1-counter.py --root <LANE> --rev 29883d4e… --freeze decc5697… --pkg65 …/rea-agents --work <S>/cwork2 --json-out <S>/c1-landing.json` → exit 0, json sha `747a0eb1…`, stdout sha `ae830b21…` |
| 3 | Data commit `c1-at-data-4aabb0b4.json`: carriers 4, failing [], fpc [] | YES | committed file; re-run at `4aabb0b4` → carriers 4, `failing []`, `frozen_path_changed []`, exit 1 |
| 4 | Six documentation bindings false at data commit (3) | YES | re-run `bindings_false` = `province_core_section, province_core_row, frontier_note, entry_present, sourced, coverage_map_row` |
| 5 | Control ledger `controls/summary.json`, `kill_rule_fires false` (3) | YES | committed at 29883d4e; `kill_rule_fires: False`, `failures: []`, `unevaluated: []` |
| 6 | Round-44 stop reason, provenance-path mismatch (3) | YES | `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` lines 8, 24 |
| 7 | S112 sha256 `2d7b901b…`, 590 lines, HTTP 200 (7) | YES | `artifacts/…` sha and `wc -l` (artifact sits under w1, see D3); `S112-raw` receipt `c11e3f48…` |
| 8 | S112 :24-69, :25-26, :39-54 (argv), :56-64, :68-69 (7, 21) | YES, D12 | numbered snapshot: class 24, exec 25-26, match 39, `-be` 51-52, `-le` 53-54, tail 56-64, deps 68-69 |
| 9 | `_SquashFSBase` :72-99, `BIG_ENDIAN_MAGIC` :73, `EXTRACTOR` :75 (7) | YES | lines 72, 73, 75 |
| 10 | v1 class :101, NAME :102, patterns :105-121, C_DEFINITIONS :123-136, HEADER_STRUCT :137 (7, 19) | YES | lines 101, 102, 104-121, 123-136, 137 |
| 11 | v1 patterns `73 71 73 68 [24] 00 01` / `68 73 71 73 [24] 01 00` (19) | YES | lines 110, 118 |
| 12 | v2 class :158, NAME :159, patterns :161-178, s_major bytes `00 02`/`02 00` (19) | YES | lines 158-178; `[24] 00 02` at 167, `[24] 02 00` at 175 |
| 13 | v2 and v1 do not override EXTRACTOR (19) | YES | no `EXTRACTOR` in 101-198 |
| 14 | v2ns :199, NAME :200, BIG_ENDIAN_MAGIC :202, EXTRACTOR :204 (7, 29) | YES | lines 199-204 |
| 15 | v3 :244, broadcom :363, ns :409 (7, 29) | YES | lines 244, 363, 409 |
| 16 | `s_magic`, six uint32, s_major/minor = 32-byte head (33) | YES | lines 126-134 (six uint32 at 127-132) |
| 17 | Tail layout `block_size_1…mkfs_time` at offset 32 (33) | PART | not in S112 v1/v2 struct; in S112 v3 struct 296-301 (uncited). D6 |
| 18 | Superblock table: magic, s_major:minor, order, block_size_1, block_log, flags, no_uids/no_guids, inodes, bytes_used (35-40) | YES | independent decode (my code) and `sb-decode-v2` agree on every cell |
| 19 | mkfs UTC 07:18:58Z / 07:18:51Z / 17:06:30Z / 17:05:52Z (35-40) | YES | `1722842338`, `1722842331`, `1678381590`, `1678381552` decoded; `file` prints the same UTC |
| 20 | Round-44 table values were host-local (-0300), not UTC (42) | YES | `tz-offset` `-0300`; r44 entry lines 76-77 show 04:18:58Z / 04:18:51Z; 04:18 local = 07:18 UTC |
| 21 | v2 values already UTC (42) | YES | r44 entry 17:06:30Z matches |
| 22 | `block_size_1` 32768 / 0, `block_log` 15/16, flags 0x00/0x40 (44) | YES (value) / PART (flags meaning, D5) | decode + `unsquashfs -s` block sizes |
| 23 | 65536 truncated to 0 in 16-bit field (44) | YES (derived) | arithmetic; labelled as derived |
| 24 | `unsquashfs -s` lines: block size, inodes 4/4/5/5, fs size 177/176/201/196, fragments (33, 46) | YES | re-run on fixture copies; outputs match the receipt |
| 25 | "Inodes/Data are compressed" on all four; v2 "Fragments are compressed" (46) | YES | `unsquashfs-s.out` |
| 26 | zlib `78 da` offsets 73 / 63,90,140 / 63,90,138 (46) | YES (offset) / PART (stream) | header scan; D13 |
| 27 | 7-Zip member compressed sizes 6→6, 7→7, 7→7; v2 25 B for apple1 (46) | RCPT | `sevenzip-list.out`; 7z exit 0 on re-run |
| 28 | `file` 5.48 labels: "version 1.0/2.0, uncompressed/compressed, 177/201 & 176/196 bytes", blocksize -32768 (48) | YES | re-run `file` prints same labels |
| 29 | "file prints UTC" (48, 'file-labels') | YES | `created: Mon Aug 5 07:18:58 2024` |
| 30 | v2ns: 2 differing bytes, magic only; 3-4 BE, 1-2 LE (102) | RCPT | `v2ns-cmp.out` (`cmp -l` not re-run) |
| 31 | v2ns: unsquashfs exit 1, 7z exit 2 (102) | RCPT | `v2ns-readers.out` (not re-run) |
| 32 | v3 broadcom: unsquashfs exit 1 "Can't find a valid SQUASHFS superblock"; 7z exit 0 2 files 13 B (103) | RCPT | `v3-readers.out` (not re-run) |
| 33 | gzip v3 listed by unsquashfs (both orders); LZMA v3 refused with `gzip uncompress failed -3` (105) | RCPT | `v3-readers.out` (not re-run) |
| 34 | round-42 v3 oracle = backhand-cli 0.25.5 + 7-Zip (105) | YES | r42 v3 core line 36 |
| 35 | "gzip v3 fixtures are round-42 C2 held-out inputs" (105) | NO / unverified | D17 |
| 36 | Carrier sha256 ×4 and size 4096 (65-70) | YES | `sha256sum` on REV blobs `529e1077…`, `b45925fa…`, `79c0f388…`, `7c62dbe3…`; `wc -c` on the same blobs = 4096 |
| 37 | Regular files 3/3/4/4; no symlink/device; "root only" dirs (67-72) | YES | `unsquashfs -lls` re-run and receipt |
| 38 | Member census sha256/size for v1 (6, 7, 7) and v2 (7×4) (78-79) | YES | `unsquashfs -d` re-run; `find | sha256sum` equals entry text, all 7 digests |
| 39 | S138 22 of 22 re-fetched, manifest sha `06a72dd5…`, failures [] (5, 81) | YES | `manifest.json` sha256 `06a72dd5…`; `S138-members-reopen.out` tail `members 22 mismatches 0`; `failures: []` |
| 40 | S138 tag 26.6.4 → commit `1fcc7a0a…` (5) | YES | `S138-tag.out`; manifest `source.commit` |
| 41 | 10 contents-API listings, HTTP 200, 11:10:29Z–11:10:43Z (5) | YES | manifest `listings`: 10; first `fetched_at 11:10:29Z`, last `11:10:43Z` |
| 42 | S139 release `tag_name 4.7.5`, `published_at 2026-03-01T23:05:47Z` (6) | YES | `S139-release.out` |
| 43 | releases page HTTP 200, 361757 B; round-44 row 398943 B (6) | YES | `S139-releases-page.out`; SOURCES S139 row |
| 44 | `/usr/bin/unsquashfs` 4.7.5 (2026/03/01), sha `461e1fd9…` (6) | YES | `sha256sum /usr/bin/unsquashfs`; `unsquashfs -version` |
| 45 | sasquatch at `/home/vgpnk/.local/bin/sasquatch`, 4.5.1 (2022/03/17), sha `ad02d27a…` (27) | YES | `sasquatch -v`; sha256 |
| 46 | child PATH contains `~/.local/bin` (27) | YES | `extract-env.json` `path` |
| 47 | unblob 26.6.4 (provider version) (line 85-96 receipts) | YES | `after.json` `provider.version` 26.6.4 — but executed via tee: D2 |
| 48 | REA 6.5.0 `extract-firmware` (status line; recheck) | PART | pinned only in recheck (D8); `run.json` `rea-agents@6.5.0` |
| 49 | Argv `sasquatch -be|-le -no-exit-code -f -d {outdir} {inpath}` (21-25) | YES | S112 lines 51-64 |
| 50 | Frozen carriers' handler `squashfs_v1`/`squashfs_v2` per carrier (87) | YES | `after.json` `chunks[0].handler`; counter `handler_detail` |
| 51 | Published 3/3/4/4 files, 20/20/28/28 bytes; `extra_published []`; gaps `[]`; coverage complete (89-94) | YES | `after.json` `published_bytes`, `extraction_gaps []`, `unpublished_entries []`, `coverage complete` |
| 52 | `projection_ok`, `evidence_id_ok`, `carrier_pin_ok` true on all four (96-98) | YES (counter-asserted) | counter per-carrier booleans all true; evidence id recomputation not independently done |
| 53 | `output_directory` under `/fast/scratch/hyaku/kaidoku-r49/probe-R49C1Run/`, prefix test (96) | YES | `after.json` `parameters.output_directory`; D14 |
| 54 | Subject digests equal carrier pins (96) | YES | `after.json` `subject.digest.sha256` = `b45925fa…`, `529e1077…`, `7c62dbe3…`, `79c0f388…` |
| 55 | S138/S139 rows opened 2026-10-28 and list the entry in used-by (SOURCES) | YES | `used-by` column lists `2026-10-28-r49-squashfs-v1v2-core.md` for S138 and S139 |
| 56 | PROVINCE.md line 416 round-42 frontier note lists SquashFS v1/v2 (13, 'province-416') | YES | `province-line416.out` line 416; text matches entry quote |
| 57 | Round-44 probe 404 `whiterussian/rc6` and empty DD-WRT listing, 2026-10-28 (15) | YES | r44 entry lines 27-28 |
| 58 | `R44C1Counter.md` "Compression is observed, not read from a field" | YES | `.ufo/waves/round-44/w1/R44C1Counter.md` line 252 |
| 59 | `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`: sasquatch is a patch set; build downloads squashfs-tools v4.3 (55) | YES | knowledge file lines 19, 22; S111 row line 117 |
| 60 | release body of `sasquatch-v4.5.1-1` says "Rebased on … 4.5.1" (55) | YES | `corpus/knowledge/2026-10-27-sasquatch-release-matrix.md` line 55 |
| 61 | `(R40-CL2)` cited as the unknowable writer question (98, 119) | YES | exists in `corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md` and r44 entry |
| 62 | Receipt ids named in the entry exist in `w1/C1ScribeEntry/receipts.tsv` (table 127-152; text) | YES | all named ids present (`unsquashfs-version`, `sevenzip-version`, `file-version`, `sasquatch-where`, `manifest-sha`, `fixtures-sha`, `S112-raw`, `S112-snapshot`, `S139-release`, `S139-releases-page`, `S138-tag`, `S138-members-reopen`, `unsquashfs-s`, `unsquashfs-lls`, `unsquashfs-extract-digests`, `sevenzip-list`, `sb-decode-v2`, `tz-offset`, `file-labels`, `v2ns-cmp`, `v2ns-readers`, `v3-readers`, `province-416`, `province-line416`, `s-rows-fieldcount`, `counter-fixed-path`, `sasquatch-version`) |
| 63 | Receipt UTC / exit / 16-hex stdout prefix per table row (127-152) | YES | all 46 receipts re-hashed (`.out` files, committed at `14936cb9`); 46/46 match |
| 64 | Entry numbers "is a receipt in receipts.tsv" (123) | PART | `receipts.tsv` has commands in full; the table says "abridged"; `counter-fixed-path` is the wrong file (D4); `scripts/sb.py` path (D3) |
| 65 | No placeholder/TODO/`<MEASURED>` remains (QUALITY 1-12) | YES | grep on landed bytes: none |
| 66 | Limits section names unexamined surfaces (QUALITY 7) | YES | symlink/device/hard link/sparse/multi-block named; hard link unmeasured (D15) |
| 67 | "gzip only" limit with [INFERENCE] label (106) | YES | label present |

## Not run / out of seat

- C2 counter and battery: not run (other seats). C2 atoms are not in this entry's claim.
- v2ns `cmp`, `unsquashfs`/`7z` exit codes and v3 readers: receipt-only (`RCPT`), not re-executed.
- `sasquatch` extraction on the carriers: not re-run; the data-run receipts were used with the counter's own rerun.
- Hard-link, sparse and xattr absence: not measured (D15).

## Receipts and artifacts (under `.ufo/waves/round-49/w2/W2C1Entry/`)

- `receipts.tsv`: entry blob, carriers.json, frozen counter, S112 snapshot, the two counter runs, the unblob identity, the 46-receipt re-hash, the unsquashfs and superblock re-derivations. UTC is written "not captured" where I did not record it; I did not invent times.
- `c1-landing.json` (REV run, exit 0), `c1-run2.out`, `c1-run2.err`; `c1-data.json` (4aabb0b4 run, exit 1), `c1-data.out`, `c1-data.err`; `c1-run.out` (the pipe run that reported counter_sha256 e3b0…, see D10).
- `c1-counter.frozen-decc5697.py` (copy of the frozen blob; sha256 `ac83715b199100774873389ea33fb4819231e1f963225416e86ad422f69d287f`).

## Items for the L1 (non-frozen text; none patches the counter)

1. Commit the landing score (or re-point the status line) — D1 — and make `c1-final.json` exist at the path the entry names.
2. Add a paragraph naming the `REA_UNBLOB_COMMAND` tee wrapper, its sha256 `28956884…`, the real unblob sha256 `0ce7b624…`, and that the counter's rerun does not use the tee (D2). Recheck line should say which invocation it matches (QUALITY 18).
3. Repoint `scripts/sb.py` and `artifacts/squashfs-26.6.4.py` to `.ufo/waves/round-49/w1/C1ScribeEntry/…` (D3).
4. Repair the `counter-fixed-path` row: cite the real command and say it reads the draft, or re-run it against the frozen counter (D4).
5. State the `Duplicates are removed`-on-v1 observation and either explain it or label the v1 flags column as unresolved (D5). Cite S112 :296-301 for the tail and move the tail's status to inference (D6).
6. Replace "this round" at lines 106-107 with "round 49 (2026-10-28)" (D7); pin REA 6.5.0 in the status paragraph (D8).
7. Optional: D9-D17 as the L1 sees fit. D10 is a counter limit to be reported as a miss, not patched.

I did not edit, stage, commit or stash anything in the lane; no counter, plan, corpus, LOG or SCORECARD file was touched. Scratch `/fast/scratch/hyaku/kaidoku-r49/W2C1Entry/` is removed after the receipts were copied.
