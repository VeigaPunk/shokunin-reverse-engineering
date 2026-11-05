# ScribeCrossLink — cross-link audit at landing 867ed98d (round 97, wave 1)

Seat: ScribeCrossLink (scribe, leaf). Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin.
F = e859a88d78567c44bc1ecfd211afe123755ae1c7, L = 867ed98d85f45a18265441c1760386ef353b3d43, base = 2a54af07.
All checks read the lane by `git -C <lane> show L:<path>` (read-only git only; no mutating git run).
Clone: /fast/scratch/hyaku/kaidoku-r97/ScribeCrossLink/clone (`git clone --shared`, `checkout --detach L`);
`git -C $S/clone rev-parse --show-toplevel` = /fast/scratch/hyaku/kaidoku-r97/ScribeCrossLink/clone (verified).
Scratch `$HYAKU_SCRATCH/kaidoku-r97/ScribeCrossLink/` (clone, materialised copies, v7 selftest work) was removed on exit.
No REA call. No tool installed or upgraded (nothing needed). No file under tools/round-97/, .ufo/waves/round-97/,
corpus/, SKILL.md, plans/ was edited; this file is the only lane write.

## Commands run (all from the clone root, unless noted)

1. `python3 -I -B tools/round-97/craft-citation-v2.py --root . --manifest .ufo/waves/round-97/manifests/block36-after.json --block 36 --rev 867ed98d…` → rc=0, `ok exit 0` (command D, reproduced).
2. same with `…/manifests/block36-junk.json` → rc=1, 4 × `criterion-not-restated` (junk manifest refused).
3. `python3 -I -B tools/round-97/depth-blocks-v4.py --root . --rev 867ed98d… --expect-blocks 36 --shape-from 36 --expect 'blocks 36, resolved 36, required-shaped 1/1'` → rc=0, `blocks 36, resolved 36, required-shaped 1/1 … met=True exit=0` (command C, reproduced).
4. `python3 -I -B tools/round-97/stop-boundary-repair-battery-v7.py --selftest --work <scratch>` → rc=0, `SELFTEST cases=23 failures=0` (backs QUALITY 195's "selftest (23 cases)").
5. Direct import of `tools/round-96/stop-boundary-repair-battery-v6.py` at L, `verify_receipt()` on a receipt with `met_target` absent / null → `{"ok": true, "reasons": []}` (backs "accepted an absent `met_target`").
6. `git cat-file -e L:<path>` for every cited path; `git ls-tree -r L -- .ufo/waves/round-97` (41 files); `git grep -n` sweeps for N9, `byte-pin-not-bound`, `selfverify reason`.
7. sha256 of the two fetched man-page copies vs the hashes cited in SOURCES.md / the knowledge entry.

## Citation table — resolves at L

| citation (doc:line) | resolves at L | note |
|---|---|---|
| SKILL.md:810 block 36 body → `tools/round-96/stop-boundary-repair-battery-v6.py` | yes | path exists at L |
| SKILL.md:810 → `.ufo/waves/round-97/pre/c1-dirty-v6-admits.json`, `v6_dirty_exit 0` | yes | file committed; key `v6_dirty_exit`=0 present |
| SKILL.md:810 → `tools/round-97/stop-boundary-repair-battery-v7.py` | yes | exists |
| SKILL.md:810 → `git cat-file blob <revision>:<path>` | yes | v7 `pins_at_rev` uses `git cat-file blob` (v7:82-83) |
| SKILL.md:814-817 table cells → `byte-pin-not-bound`, `met-not-typed`, `uncaught exception`, `crash`, `re-read`, `--json-out` | yes | all six verbatim in the cells |
| SKILL.md:814-817 criterion cells → `QUALITY 195` / `QUALITY 196` | yes | correct row numbers; command D rc=0 |
| SKILL.md:819 Refs → `corpus/QUALITY.md rows 195-196` | yes | row 195 at QUALITY.md:335, row 196 at :337 |
| SKILL.md:819 Refs → `tools/round-97/stop-boundary-repair-battery-v7.py`, `tools/round-97/kill-rule-v3.py` | yes | both exist |
| SKILL.md:819 Refs → `corpus/knowledge/2026-11-05-r97-receipt-byte-binding.md:1` | yes | file exists; line 1 is the `source:` line |
| QUALITY.md:335 row 195 → `git cat-file blob`, `byte-pin-not-bound`, `met-not-typed` | yes | all three keywords verbatim in row 195 |
| QUALITY.md:335 row 195 → `tools/round-96/stop-boundary-repair-battery-v6.py` | yes | exists |
| QUALITY.md:335 row 195 → `.ufo/waves/round-97/pre/c1-dirty-v6-admits.json`, `v6_dirty_exit 0` | yes | committed; key/value present |
| QUALITY.md:335 row 195 → `tools/round-97/stop-boundary-repair-battery-v7.py` | yes | exists; selftest 23 cases / 0 failures measured (cmd 4) |
| QUALITY.md:335 row 195 → `.ufo/waves/round-97/l1/scores/` | worktree only | **not in commit L** (see F3) |
| QUALITY.md:335 row 195 → M96-a, M96-f | yes | corpus/lessons/round-96.md:61 and :89 |
| QUALITY.md:337 row 196 → `crash`, `uncaught exception`, `re-read`, `--json-out` | yes | all four verbatim in row 196 |
| QUALITY.md:337 row 196 → `.ufo/waves/round-96/mutants.json`, "kill class N9" | path yes / item NO | **F1** — file holds mutants M0…M10, no N9 |
| QUALITY.md:337 row 196 → `.ufo/waves/round-97/pre/c1-v2rule-at-base-crash.txt` | yes | traceback = pinned round-96 rule crashing (`KeyError: 'fresh_scored'`) on the round-97 table |
| QUALITY.md:337 row 196 → `verify_own_receipt` in `tools/round-97/kill-rule-v3.py` | yes | defined at kill-rule-v3.py:571; refuses `ownrec-met-not-typed` |
| QUALITY.md:337 row 196 → "limit 7" (round-96) | yes | corpus/lessons/round-96.md:156 — "`--json-out` is optional there"; code confirms (`kill-rule-v2.py:379`, receipt written only `if args.json_out`) |
| knowledge:1-3 source/verified-at/recheck trio | yes | first three lines are exactly `source:` / `verified-at:` / `recheck:` |
| knowledge:1 → `.ufo/waves/round-97/pre/s322-fsync2-fetch.html`, sha `f0a986d2…` | yes | committed; blob sha256 = f0a986d21500222ecb69580fc7a910f346c6b1ff1005ca515501fb05bb5d91f5 = cited hash; also in pins.sha256 |
| knowledge:1 → `tools/round-97/`, `.ufo/waves/round-97/` | yes | both trees exist at L |
| knowledge:2 → freeze `e859a88d…` | yes | `git cat-file -t` = commit |
| knowledge:3 recheck → kill-rule-v3 + depth-blocks-v4 paths, mutants.json, forgery/ | yes | all exist; command D/C reproduced (cmds 1,3) |
| knowledge:11-12 → `tools/round-96/stop-boundary-repair-battery-v6.py`, `c1-dirty-v6-admits.json`, `v6_dirty_exit 0` | yes | committed |
| knowledge:20 → `.ufo/waves/round-97/l1/scores/` (dirty-clone leg) | worktree only | **F3** — no committed receipt for the v7 refusal |
| knowledge:24-26 → fsync(2) quote | quoted text ≠ page | **F2** — second sentence is not verbatim |
| SOURCES.md:238 S322 → `fsync(2)`, copy path, sha `f0a986d2…` | yes | blob sha matches; located quote verbatim in DESCRIPTION of the fetched copy |
| SOURCES.md:239 S323 → `rename(2)`, copy path, sha `8772946a…` | yes | blob sha = 8772946a809a0db54f4854f200908f10bee758ea452e8df5efd955bc3b8e6e57 = cited; located quote verbatim; copy is **not** in pins.sha256 (added after the freeze — asymmetry, not a dangling path) |
| README.md:277 knowledge row `2026-11-05-r97-receipt-byte-binding` | yes | S322/S323, both tools, `.ufo/waves/round-97/pre/` all exist; `.ufo/waves/round-97/l1/scores/` → **F3** |
| README.md coverage map (## Coverage map, lines 13-134) | no r97 row | **F4** — map's last row is round 92 (r93-r96 absent too) |

## Findings

**F1 — QUALITY 196 cites the wrong path for kill class N9.** Row 196 says "a `KeyError` in the receipt schema check counted
as a mutant kill (`.ufo/waves/round-96/mutants.json`, kill class N9)". That file resolves at L but its mutant names are
M0…M10; `git grep -n "N9"` over the whole round-96 tree returns hits only in
`.ufo/waves/round-96/w1/MutationC1.md` and `.ufo/waves/round-96/w1/MutationC1/mutants.md` (line 42: "N9 schema check skipped
when counts is a dict" → killed via `verify-catches-unlabelled-counts` crashing with `KeyError: 'fresh_scored'`). The
substance of the claim is true, but the named path does not contain the named item. Fix: cite
`.ufo/waves/round-96/w1/MutationC1/mutants.md` (or MutationC1.md) for N9.

**F2 — the knowledge entry's fsync quotation is not verbatim.** Knowledge lines 24-26 quote "Calling fsync() does not
necessarily ensure that the entry in the directory containing the file has also reached disk. For that, fsync() on a file
descriptor for the directory is also needed." and add "(S322; located in the fetched copy.)". The fetched copy
(`.ufo/waves/round-97/pre/s322-fsync2-fetch.html`, DESCRIPTION) reads "For that **an explicit** fsync() on a file descriptor
for the directory is also needed." — the entry drops "an explicit" and rewrites "For that an" as "For that,", so the second
quoted sentence does not occur in the cited page. The SOURCES.md:238 S322 located quote is verbatim and correct; only the
knowledge entry paraphrases inside quotation marks.

**F3 — the knowledge entry's "Measured: the v7 counter refuses a dirty clone's counter pin" has no committed receipt.**
The item asks for a committed receipt path under `.ufo/waves/round-97/`: **none exists**. The committed round-97 tree holds
the before-side only — `.ufo/waves/round-97/pre/c1-dirty-v6-admits.json` (v6_dirty_exit 0, v6_admits true) whose `note`
field asserts the v7 refusal in prose but records no v7 run. The measured v7 refusal (v7 exit 1, stderr
`selfverify reason: byte-pin-not-bound:counter`) exists only in the L1 worktree receipt
`.ufo/waves/round-97/l1/scores/c1-at-867ed98d85f45a18265441c1760386ef353b3d43.json` (honest → K-bytes → dirty leg), which
is untracked (`git status` shows `?? .ufo/waves/round-97/l1/`). Same gap for the other two citations of that directory
(QUALITY 195, README.md:277): the path resolves in the worktree at L but is absent from commit L. Either commit the L1
receipts under `.ufo/waves/round-97/l1/scores/` or re-point the three citations at a committed receipt.

**F4 — README coverage map has no round-97 row.** The r97 knowledge entry was added to the "## Knowledge" index
(README.md:277) but the "## Coverage map" table (README.md:13-134) ends at round 92; rounds 93-96 are absent from the map
as well, so this is a carried-over index gap rather than a regression introduced by this landing. Recorded, not scored.

## Verified clean

- Command D reproduces at L (rc 0 after-manifest / rc 1 junk-manifest); command C reproduces at L (rc 0, expected label).
- Every manifest keyword required by `.ufo/waves/round-97/manifests/block36-after.json` occurs verbatim in its QUALITY
  row: 195 → `git cat-file blob`, `byte-pin-not-bound`, `met-not-typed`; 196 → `crash`, `uncaught exception`, `re-read`,
  `--json-out`. The four manifest row snippets are present in the block-36 table cells.
- No wrong line numbers found: SKILL.md:819's `:1` is the knowledge entry's `source:` line; rows 195/196 sit at
  QUALITY.md:335/337; S322/S323 at SOURCES.md:238/239.
- Both cited man-page copies exist at L and their sha256 match the cited prefixes (S322 is inside pins.sha256; S323 was
  fetched after the freeze and is pinned only by the SOURCES.md prefix).

## Not established / limits of this seat

- The L1 receipts under `.ufo/waves/round-97/l1/scores/` were read read-only to check the dirty-clone claim; a seat never
  overwrites them, and none was modified.
- `.ufo/waves/round-97/l1/` is untracked at L, so "resolves at L" for those three citations means "present in the worktree
  at L", not "present in commit L" — stated that way throughout the table.
- No claim in the landing was re-scored here; only citation resolution, keyword presence and the two frozen C2 commands
  were exercised.
