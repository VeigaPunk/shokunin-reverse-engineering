# R41W2C1Docs — review of the R41-C1 landing documents at e9a24d07

**Verdict: DEFECTS FOUND — all minor; every measured number, digest, count, receipt binding and
source quotation in the four landing surfaces otherwise verifies true against the receipts,
carriers.json, the score receipts and the fetched sources. The one genuine citation defect at the
reviewed revision (entry licence-line bracket) was already repaired upstream at 74064474.**

Attacked: `corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md`, PROVINCE `## Round-41 additions
to Core` + `Round-41 frontier note`, `corpus/README.md` round-41 rows + `## Frontier`
sasquatch-v4be lines, SOURCES S127/S128 — every number against the committed receipts and
`.ufo/waves/round-41/c1/carriers.json`, every S-id + line citation against the source bytes, every
claimed limitation against what was actually measured, and the whole surface against the round-39/40
blocks. Bytes reviewed are `git show e9a24d07:…` (the measured revision), not the working tree: the
lane tip moved during this review (e1c83313 was HEAD at start; 74064474 landed mid-review with
"entry citation fix (w2 F1)"). Tooling: stock python3/curl/git only, no installs (pacman untouched).

## Findings (by severity)

**F1 — minor, citation precision (repaired upstream at 74064474).** Entry last line at e9a24d07
reads `[S127 licence lines 665-670 / 688-693 restrict redistribution and reverse engineering; …]`.
The lane's own SOURCES rows record S127 "lines 663-670 the AVM licence notice" and S128 "lines
686-693" (`corpus/SOURCES.md:133-134`). Ground truth (both files re-fetched today, digests equal to
the frozen record — see artifacts): `info_en.txt` 5490 (50 653 B, sha256 `e3100cda…7360d18`) has the
© header at line 663 and the forbid-list end at 670; 5491 (53 166 B, sha256 `ec2528eb…51970b4`) has
© at 686, end at 693. So at e9a24d07 the bracket started each range two lines late and left the
second range unattributed (it is S128's, not S127's). No material overclaim: 665/688 open inside the
same notice and the operative restriction clauses (667-670 / 690-693) lie inside both renderings.
74064474 fixed the line to "S127 licence lines 663-670 / S128 686-693", which matches SOURCES and
the live files exactly.

**F2 — minor, wording (honest but malformed).** PROVINCE Core row (`PROVINCE.md:400` at e9a24d07):
"counter `tools/round-41/c1-counter.py` `carriers_matched scored after this commit` exit see
`.ufo/waves/round-41/l1/scores/` at `the commit that adds this text`" — grammatically broken
(backticked phrase, then "exit see"). Substantively honest: it states no result, and the score
indeed happened after the landing commit (bf5286c9, `--rev e9a24d07`, 4/4, exit 0 —
`.ufo/waves/round-41/l1/scores/c1-at-e9a24d07.json`). README's parallel phrasing
(`corpus/README.md:97`, "scored by `tools/round-41/c1-counter.py` after the landing commit") is
clean and true; only the PROVINCE row reads badly.

**F3 — minor, formatting + staleness at tip.** Entry status line (`…r41-avm-be-squashfs-core.md:3`)
contains doubled backticks: "exit 0, ``.ufo/waves/round-41/l1/scores/``" (renders as a stray
backtick). And the conditional status line ("either `met` … or the honest stop that replaces this
line") was never flipped after bf5286c9 recorded met; the title ("(round 41, Core)"), the PROVINCE
row and SCORECARD `## Round 41` (`SCORECARD.md:3455`) carry the verdict, so the pointer chain
resolves — but the line's own protocol says the met branch should have replaced it.

**F4 — nano, enumeration imprecision.** Entry (exact-path rule paragraph): "a suffix-matcher mutant
died on three cases (a regular file is not the symlink entry, the reverse direction, a deeper file
with the oracle row's sha256 does not publish the oracle row, a gap on a deeper file does not
resolve to the entry)". The artifact records exactly three failures
(`.ufo/waves/round-40/w2/artifacts/R40W2C1Refreeze/selftest-suffixmut.txt`: regular≠symlink entry;
deeper-file publish; deeper-file gap resolution) — the parenthetical lists four clauses, and "the
reverse direction" has no distinct recorded case.

**F5 — nano, completeness.** README entry row (`corpus/README.md:211`) lists the entry's sources as
"S112, S114, S124, S121, S125, S127, S128", omitting S126, which the entry cites for the round-11
lineage. The SOURCES S126 row's used-by names the round-40 entry only, so the mapping is not wrong —
just incomplete relative to the entry's own citation set.

**F6 — nano, compressed pointer.** "records one `depth-limited` gap at the carve directory
(round-40 §6)" — the round-40 entry has no numbered sections; its sentence for this fact cites
`.ufo/waves/round-40/w1/R40C1ReconGaps.md` §3, §6. The shorthand resolves only if the reader knows
"§6" means that report.

**F7 — observation, evidence-artifact hazard (not doc text).**
`w1/artifacts/R41C1VendorV3/inode-chain-walk.txt` prints "LE identity
2+len+inode_table_start==directory_table_start: False" directly under the walk that ends exactly on
`directory_table_start`. The counter's identity (`tools/round-41/c1-counter.py:736`, masked
metadata length) is **True** for V3 (`le_identity: true`, 30 231 260 + 2 + 724 = 30 231 986 = dts in
the score receipt); the artifact line evidently used a different length. The entry's "(exact)" is
correct, but a reader of the raw artifact can stumble on the contradiction.

**F8 — observation, deliberate omissions worth naming.** (a) The PROVINCE Core row summarizes gaps
as "one `unpublished-entry` per retained symlink plus one `depth-limited`" and never mentions V4's
4 `MaliciousSymlinkRemoved` dispositions — accurate as written ("retained" excludes removed links),
full dispositions live in the entry table. (b) The entry reports V4's measured removal set (611
unpublished + 4 removed of 615 symlinks) without restating the claims-file caveat that the removed
set depends on directory iteration order; the counter's rerun binding pins the same four paths at
scoring time (`lib/libbroadbandcfg.so`, `lib/libbroadbandcfg.so.1`,
`usr/www/avm{,e}/cgi-bin/system_status`, all symlink rows in `V4/nonregular.tsv`), and a divergent
rerun fails `projection_ok` by design. Neither text claims more than was measured.

## Verified true (evidence ledger; extracts in `artifacts/R41W2C1Docs/`)

- **Pins & provenance** (entry table + fetch-chain paragraph vs `carriers.json`): V3 image
  `770efb4e…5ab7`, member `87cc5d6b…a0f8`, carve/`bytes_used` 30 233 394, carrier `c4f74f54…f872a`;
  V4 image `a5a3a763…f661`, member `4cfc3016…2f6c`, nested `4d5de25c…d947`, 32 720 860, carrier
  `ce27ebca…087f`; L3 `04cfb4cd…45a3` / L4 `4c0e5459…fcbc` with committed carrier.sqsh. The counter
  receipt re-verified every pin at scoring time (`carrier_pin_ok: true` ×4). fetch-vendor fail-closed
  on omitted `member_sha256` verified in code (`tools/round-41/fetch-vendor.py:199-208`, "spec omits
  member_sha256 (required since round 41)") and by the red-path evidence (all-`d` digests → exit 1,
  `link=member_sha256`; base-rev spec missing → exit 2; `w1/artifacts/R41C1Fetch/vendor-chain-evidence.txt`,
  incl. V1 image `f518ce6b…de6d` / member `334e56df…f3d4` / pin `ac4098bd…8e95` = the entry's
  development-chain numbers = `prior_pins` in the receipt).
- **Receipt numbers vs the entry table** (from `corpus/evidence/round-41/c1/*/after.json`,
  `oracle.tsv`, `nonregular.tsv`, and the score receipt): V3 8 published, 95 non-regular (9 dirs,
  85 symlinks, 1 char device `dev/led` — row 62), 86 gaps = 85 `unpublished-entry` + 1
  `depth-limited`, 0 removals, 104 inodes (103 rows + root); V4 6349 published, 1017 non-regular
  (401/615/1), 612 gaps = 611 + 1, 4 removals, 7367 inodes; L3 13/23 (20/3), gaps 3+1, 37 inodes,
  187 892 B; L4 14/20 (17/3), gaps 3+1, 35 inodes, 169 545 B; every carrier one `squashfs_v4_be`
  chunk, not failed; V3/L3/V4 xz (id 4), L4 gzip (id 1). V3 layout identity exact (30 231 260 + 2 +
  724 = 30 231 986); V4 passes via first-header plausibility (`meta_len_le` 2024 vs BE 59 399) — the
  entry's "either the exact single-block identity … or the plausibility walk" is exactly the
  V3/V4 split. `filesystem_core.squashfs` is one published regular file of V3 (oracle row 3, sha
  `cc6c1925…be43`, 29 596 696 B) — "not opened" is accurate. L3/L4 symlink shapes match the text
  (`bin/busy → ../usr/bin/busy`, `usr/sbin/tool → /sbin/tool` absolute in-tree, relative links) and
  each has the empty regular file `var/tmp/empty` (size 0).
- **Staged-entry claims**: V3 "stages 103 entries" is a measured count (root + 9 dirs + 85 symlinks
  + 8 files; `oracle-run.json` shows sasquatch created 0 char devices, so `dev/led` is not staged;
  `w1/R41C1VendorV3.md` L262). V4 "7367 staged entries by the reader count" is correctly labeled a
  reader count (no REA run existed): 1 (the `firmware.bin_extract` staging dir) + 7366 oracle rows
  (`w1/R41C1VendorV4.md` L162), against REA's 10 000 default (`max_output_files`,
  `w1/R41RevBudget.md` §1-2: root not counted, every name under the counted root is); 73.7 % =
  7367/10 000. The two numbers use different provenance and the entry labels exactly the
  reader-derived one — the assignment's flagged concern does not materialize.
- **Score receipts**: `c1-at-e9a24d07.json` `carriers_matched: 4`, exit 0, `frozen_path_changed: []`,
  `carriers_unchanged`/`gap_rule_unchanged` true, every binding true (`entry_present`,
  `province_core_row/section`, `frontier_note`, `coverage_map_row`, `gap_rule_ok`, `sourced`,
  `opened_source_rows [S127,S128]`); `c1-extra-at-e9a24d07.json` met, exit 0 (`frontier_content`,
  `oracle_rederived` ×4, `sourced_new` with S127/S128 new-at-e9a24d07 and used-by pointing at the
  entry — `git show 49096c7:corpus/SOURCES.md | grep -c "S127\|S128"` = 0).
- **Source citations** (all four files fetched fresh, digests match the entry's):
  S112 `squashfs.py` 19 842 B sha256 `2d7b901b…99287`, **byte-equal to the installed unblob 26.6.4
  copy** (`~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`),
  `is_avm = header.bytes_used == header.mkfs_time` + conditional `-be` inside lines 44-50 (line 48);
  S114 `AVM-BE-format.txt` 1 496 B sha256 `c1c43f6f…a9a5d5`, lines 8-9 and 13-14 quoted verbatim;
  S124 patch 2 217 B sha256 `7f0a1b25…220fc`, lines 7-9 (`swap_block_length` selector), 12-25
  (`read_block` conditional swap), 33-45 (`TARGET_FORMAT == AVM_BE`, LE host → 0, `swap` from magic)
  all exact; S121 `unsquashfs.c` lines 664-669 (`if(swap)` length swap) and 4389-4400 (`-be` sets
  `swap`) exact; S125 row = round-40 V1 identity (6490 Cable 07.57, image `f518ce6b…`); S126 tsv
  (read in shokuknow, read-only): 4 096 B, `sqsh`, xz id 4, `mkfs_time == bytes_used == 365`,
  handler `squashfs_v4_be`, `unblob_be_flag absent`, four files extracted, no exit status — and the
  entry's "first header `7400` → LE 116, 121 + 2 + 116 = 239" is grounded in
  `w1/R40AssimE3.md:25-26` (the tsv itself carries no table-start rows; SOURCES S126's registered
  scope covers "that image's own superblock fields").
- **Artifact pointers**: refreeze diff sha256 `8fa0a813…79c0a8` ✓; selftest 70 → 75 cases, 7 green /
  68 red ✓; mutant 3 failures ✓; summary.json runs 1-3 = patched 4/4 (exit 0), patched-reconstructed
  4/4, frozen round-40 counter 3/4 (exit 1) ✓ — "reports 4/4 where the frozen counter reported 3/4"
  exact; `crosscheck.txt` 8/8 digests, 85/85 symlink targets, 0 mismatches (and `oracle-run.json`
  `mismatch_count 0` per carrier) ✓; `layout-be.log` refusal + `sqfs-list.py` exit-2 paths
  (`:1553,:1575`) ✓; `reader-real-vendor.txt` V1 697 regular / 263 in-tree symlinks and
  `round-40/c1/V1/nonregular.tsv` = 381 rows ✓; REA stages inputs as `firmware.bin`
  (`FirmwareFiles.js:33-37` in the pinned pkg65) ✓; counter rerun semantics (replays recorded
  `max_depth`, `projection_ok` fails on a different removal set, `rerun_env_error` exit 2) match the
  code (`tools/round-41/c1-counter.py:198-246,1329-1353`) ✓; extract-root null fail-closed selftests
  present (`:2556-2733`) ✓; `.ufo/waves/round-40/w1/R40C1MarkerBoundary.md` exists ✓; SCORECARD
  `## Round 41` exists ✓.
- **"Scored after this commit" pointers**: README L97 "after the landing commit" — true (bf5286c9
  descends from 042b8769); PROVINCE row "scored after this commit" — true; entry status conditional
  — honest at e9a24d07 (no score existed in-tree at that revision).
- **Contradiction sweep vs rounds 39/40**: the round-39 note's "AVM-BE bodies … stay Frontier" and
  the round-40 `measured, not promoted` block are superseded explicitly and only for the genuine AVM
  layout ("A standard big-endian body whose AVM marker was stripped stays governed by `## Round-39
  additions to Core`" — consistent with round-40 H1/H2); the correction paragraph names the round-40
  record without rewriting it; README's dated sasquatch-v4be frontier lines chain r38 → r39 → r40 →
  r41 with each supersedes statement correct; the "Still Frontier" lists are consistent across
  PROVINCE row, note, README L256 and the entry's limits (LE AVM members `hsqs`, AVM kernels, nested
  sub-images below depth 1, vendor-mangled images); V4 being a carved nested rootfs does not
  contradict "nested filesystem_core images below depth 1 stay Frontier" (that is the in-run depth
  case, and the V4 receipt indeed records the `depth-limited` gap).

## Residual risk & verification gaps

- Vendor carrier bytes were not re-downloaded by this seat (AVM licence; size). Pin equality rests
  on the counter receipt's `carrier_pin_ok` (scored at e9a24d07 against a `--carrier-cache`), the w1
  chain evidence, and SOURCES image HEAD sizes (33 269 760 / 36 329 960 B) consistent with the
  pinned members. The entry's recheck line documents the rebuild command; I did not exercise it.
- S127/S128 *directory listing* sha256s (`88c8d648…`, `badbb744…`) are consistent between SOURCES
  and the entry but were not independently re-fetched (generated pages); the `info_en.txt` files
  were re-fetched and are byte-identical to the frozen record.
- V4's removal set is iteration-order-dependent (disclosed in the claims file, not restated in the
  entry — F8b); the committed receipt and the counter-time rerun agree on the same four paths.
- Lane tip advanced during the review (e1c83313 → 74064474); all findings are pinned to e9a24d07
  bytes via `git show`. 74064474 already resolves F1; F2-F6 are open as of that tip.
- Out of scope here: the C2 landing (SKILL block 20, triage entry, held-out data) — separate seat.

## Artifacts

`artifacts/R41W2C1Docs/`: `entry-at-e9a24d07.md`; `province-round41-block-L396-409.txt`;
`readme-round41-rows.txt`; `sources-S125-S128-rows.txt`; `score-extracts/{c1-at-e9a24d07-extract,
c1-extra-at-e9a24d07-extract,refreeze-scoring-selftest}.json`; `verification-copies/{squashfs.py,
AVM-BE-format.txt,350-unsquashfs__AVM_BE.patch,unsquashfs.c}` (fetched sources, digests in the
ledger above) and `verification-copies/info549{0,1}-licence-excerpt-*.txt` (licence-line excerpts
only; full info files not copied per the AVM no-redistribution bound — sha256s in
`verification-copies/INFO-FILES-SHA256.txt`, equal to the SOURCES records).

Report: `.ufo/waves/round-41/w2/R41W2C1Docs.md` (this file).
