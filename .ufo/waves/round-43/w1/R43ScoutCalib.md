# R43ScoutCalib — pre-freeze calibration of SHONEN.md / SCORECARD.md vs the repo at base 6b9e64fe

**Verdict: CONFIRMED** — every file:line range, N/N count, commit hash and selftest count asserted in
SHONEN.md (all 4 boxes) and in SCORECARD.md (`## Owned axes`, `## Capabilities`, `## Round 42`, the
`planned (round 43)` line) checks out against the repo at `6b9e64fe7e0de202d9383baad5792fbfe039a743`
(read-only git + frozen interpreter selftests + the gate run). **Zero mismatches.** The only findings
are the known append-only staleness pattern in the two `## Owned axes` rows (fresh numbers live in the
round sections; nothing false) and one method note. The round-43 landing has no calibration debt to
repair and must not grow any: all live range citations sit in files the round-43 plan does not touch.

Seat: R43ScoutCalib (scout, leaf). No tools installed/upgraded (none needed). Scratch:
`/fast/scratch/hyaku/kaidoku-r43/w1-R43ScoutCalib` (removed at exit). All evidence copied to
`.ufo/waves/round-43/w1/artifacts/R43ScoutCalib/` (cmdA.log, gate-at-base.txt, selftests-and-bytes.txt,
skill_check*.py).

## Method

- Files read at the base commit via `git show 6b9e64fe:...` (never the worktree; HEAD here is `d22686e1`,
  ahead of base; `6b9e64fe` is a descendant of `d4b4b4fb`/`eb8215ac`/`af50af81`, all ancestors verified
  with `git merge-base --is-ancestor`).
- Command A (SCORECARD `## Measurement recipes`, verbatim) run at 17 revisions.
- Every 40-hex hash in the four surfaces extracted programmatically and verified with `git cat-file -t`
  (15 unique, all commits).
- Frozen selftests run with `python3 -I -B` from scratch; the local-source gate run read-only at base.

## SHONEN.md (4 boxes; all statements with ranges/counts/hashes)

| # | location | asserted | observed | match? |
|---|---|---|---|---|
| 1 | box 1 | r42 added rule block 21 = triage v4, 13 columns, 15 rules, marker `<!-- sqfs-triage-table v4 -->`; matched evaluator 78/78 at `eb8215ac` | base SKILL.md marker line 521, table 521–539, header has 13 columns, 15 body rules; receipt `c2-at-eb8215ac.json` matched 78/78 | ✓ |
| 2 | box 1 | `SKILL.md:81-449` craft section, 20/20 resolvable rule blocks at `e1c83313f33a3d97edbd8fef402db2d06172fcdc`; block 20 (v3) at `SKILL.md:387-449` | command A @ e1c83313: 133/133, 20/20; craft heading 81, last non-blank 449, block 20 = 387–449 | ✓ |
| 3 | box 1 | 19/19 at `4d62ee5a86b4692a13f682b29ed7975e8d7e5326`; block 19 (v2) at `SKILL.md:348-375`; `tools/round-40/sqfs-triage-v2.py --selftest` 45 cases | command A: 130/130, 19/19; block 19 = 348–375; selftest `cases=45 pass=45 fail=0` | ✓ |
| 4 | box 1 | 18/18 at `52b0eb29`; block 18 (v1, 8 labels) at `SKILL.md:316-343`; `tools/round-39/sqfs-triage.py --selftest` 35 cases, reproduced by 2 wave-2 seats | command A: 128/128, 18/18; block 18 = 316–343; selftest 35/35; artifact `.ufo/waves/round-39/w2/artifacts/R39W2C2Rescore/sqfs-triage-selftest.txt` present | ✓ |
| 5 | box 2 | R42-C1 met 4/4 at `eb8215ac` (receipts `corpus/evidence/round-42/c1/`, LOG r42 entry) | receipt `c1-at-eb8215ac.json`: carriers_matched 4, exit 0, met_target, frozen_path_changed []; `corpus/evidence/round-42/c1/` present; LOG.md `## Round 42` at line 3174 | ✓ |
| 6 | box 2 | R41-C1 met 4/4 at `e9a24d07`; wave-2 repros `.ufo/waves/round-41/w2/R41W2Repro*.md` | receipt `c1-at-e9a24d07.json`: 4/4 exit 0; 3 repro files | ✓ |
| 7 | box 2 | R40 measured-not-promoted, honest stop 3/4 (R40-C1) | round-40 section + `PROVINCE.md:386-394` record 3/4 stop | ✓ |
| 8 | box 2 | r39 BE v4: 6 frozen carriers, counter 6/6 at `6fdaf4f1` | `c1-at-6fdaf4f1.json`: carriers_matched 6, met_target | ✓ |
| 9 | box 3 | v2 executed: 26/26 held-out, seed = freeze hash, indep-eval repro `.ufo/waves/round-40/w2/R40W2C2IndepEval.md` | `c2-at-42c10a58.json`: matched 26/26, exit 0; repro file present | ✓ |
| 10 | box 3 | v1 executed: 20/20; `tools/round-39/{sqfs-triage.py,c2-counter.py}` selftests 35/35 and 27/27 | `c2-at-6fdaf4f1.json`: 20/20, met; selftests reproduced 35/35 and 27/27 green | ✓ |
| 11 | box 3 | smallest 20/20 table = 8 rows / 7 cells (`.ufo/waves/round-39/w2/R39W2C2Shortcut.md`) | file present | ✓ (existence) |
| 12 | box 4 | `PROVINCE.md:97-125` Adjacent list; installer :110-115; safety refusal :116-118; tooling bullet :119-125; byte-identical at `52b0eb29` | all line probes hit at both `52b0eb29` and base; lines 97–125 byte-diff IDENTICAL between the two revisions | ✓ |
| 13 | box 4 | r39 additions at `PROVINCE.md:378-384` (row :382, note :384) | both revisions: 378 = `## Round-39 additions to Core`, 382 = `squashfs_v4_be` row, 384 = frontier note | ✓ |
| 14 | box 4 | r40 appends at `PROVINCE.md:386-394` | base: 386 = `## Round-40 measured, not promoted…`, frontier note ends 394; r41 row at 396, r42 at 410 | ✓ |

## SCORECARD.md `## Owned axes`

| location | asserted | observed | match? |
|---|---|---|---|
| coverage row | 133/133 after r41 landing (command A at `e1c83313`, missing [], dangling []) | command A @ e1c83313: mapped 133, files 133, missing [], dangling [] | ✓ |
| coverage row | 130/130 @ `4d62ee5a`; 128/128 @ r39; 126/126 @ r38; 124/124 @ r36 landing; 122/122 @ `cab59f22`; 116/116 @ `c369242f`; 109/109 @ `ebe2cb4a`; 78/78 @ `3395b6d`; 107/107 @ `7ef837a4` | command A: 130/130, 128/128 (@52b0eb29 and @6fdaf4f1), 126/126 (@0fc61133), 124/124 (@ffc81341), 122/122, 116/116, 109/109, 78/78, 107/107 — all exact | ✓ |
| coverage row | measured-after-r39 cell: command A at `52b0eb29`, missing [], dangling [] | confirmed | ✓ |
| depth row | 20/20 @ `e1c83313` (block 20 at `SKILL.md:387-449`; craft `SKILL.md:81-449`); 19/19 @ `4d62ee5a` (block 19 `SKILL.md:348-375`); 18/18 @ `52b0eb29` (`citation_resolved_rules 18`, block 18 `SKILL.md:316-343`); 17/17 @ `c369242f` and @ `ebe2cb4a`; 9/9 @ `638fb211`; 9→17 growth `58116aa1`…`4072ebb3`; r25 recount `08c7a729` | command A matches every pinned value; all six growth/recount hashes resolve | ✓ |
| depth row | evidence cell: craft section `SKILL.md:81-343` (heading 81, last non-blank 343 at `52b0eb29`); baseline `SKILL.md:77-191` at `a79945c4` | confirmed at 52b0eb29; `a79945c4` resolves | ✓ (77-191 taken as carded) |
| calibration row | 9/9 obligations; count measured at `c265db9b…` (result.json measured_revision; card once said `75af886a` until r26) | result.json measured_revision = `c265db9b…`, aligned 9/9; command B re-run: baseline 0/9 @ `66455858`, after 9/9 @ `c265db9b` | ✓ |

## SCORECARD.md `## Capabilities`

| row / note | asserted | observed | match? |
|---|---|---|---|
| BE v4 recursion row | evidence `PROVINCE.md:378-384`; counter 6/6 exit 0 at `6fdaf4f1` | PROVINCE 378–384 confirmed; receipt 6/6 | ✓ |
| triage v1 row | `SKILL.md:316-343` (block 18, marker v1); interpreter `--selftest` 35 cases; manifest H01–H20 seed `8fcda41c…`; counter 20/20 at `6fdaf4f1`; smallest table 8 rows / 7 non-`*` cells | block 18 = 316–343 at base; selftest 35/35; manifest seed + H01–H20 (n=20); receipt 20/20; shortcut note present | ✓ |
| triage v2 row | `tools/round-40/c2-counter.py --root <LANE> --rev 42c10a58… --freeze 7fce3086…` → 26/26 exit 0 (`c2-at-42c10a58.json`, repro) | receipt 26/26 exit 0; repro file present | ✓ |
| AVM-BE row | `tools/round-41/c1-counter.py` 4/4 exit 0 (`c1-at-e9a24d07.json`) | receipt 4/4 exit 0 | ✓ |
| round-32 repair note | restores 3 records; base `283aad7f` SCORECARD lines 2136, 2208, 2375; a2audit files; c2-negative receipt | @283aad7f: 2136 = curated-source-registry row, 2208 = raw-quote audit row, 2375 = Ghidra-log row; all four A2Capability*.md + `controls/c2-negative/receipt.json` present | ✓ |

## SCORECARD.md `## Round 42` + `planned` line

| item | asserted | observed | match? |
|---|---|---|---|
| header pins | base `c4a38ea2`; freeze `d1681696`; controls `b024051c`; data `d5e22b51`; landing `eb8215ac`; scores `d4b4b4fb`; lesson `corpus/lessons/round-42.md`; wave 1 = 43 seats | all hashes resolve; commit subjects match their roles; 43 top-level w1 reports; lesson present | ✓ |
| R42-C1 row | carriers_matched 4, bindings true, frozen_path_changed [], exit 0, counter_sha256 `0f5052f9…` | receipt: 4 / true / [] / 0 / `0f5052f99a97…` | ✓ |
| R42-C2 row | matched 78/78, combo_unseen_majority 19/24, observed_features_match_declared false (C02 lacks depth-limited), exit 1 | receipt: matched 78 n 78, unseen 19 of 24 vs need 12, flag false, exit 1; manifest seed = `d1681696`, C02 present | ✓ |
| owned scores | coverage 133→135 command A at `d4b4b4fb`; depth 20→21, command A resolves 21/21 after the post-scoring citation | command A @ d4b4b4fb: 135/135 (rules 20/21 there); @ base: 21/21; the citation landed in `46486e7a` ("block-21 citation (command A)") — exactly as the section narrates | ✓ |
| planned (round 43) | depth refreeze, generator refuses unobserved tuples (QUALITY 85, R42-CL1); wave 2 attacks r42 C1 landing (R42-CL2); second choice lands R41-CL3 copies (`w1/R42LocalSrc.md`); R40-CL2 open | QUALITY 85 named in `corpus/lessons/round-42.md` (3×); R42-CL1/CL2, R41-CL3, M42-* all in lessons; R40-CL2 in round-40 lesson; `R42LocalSrc.md` present; gate at base exits 1 with exactly the 18 plan-named rows (S001 S002 S003 S006 S007 S023 S035 S040 S048 S056 S066 S070 S079 S081 S082 S083 S090 S092) | ✓ |

## Findings for the L1 (debt status; the landing must not grow it)

1. **No mismatches.** Every ranged/count/hash/selftest statement above is true as pinned.
2. **Known staleness pattern, not falsehood:** the `## Owned axes` coverage row's freshest figure is
   133/133 ("count refreshed rounds 25, 26, 31, 36, 38, 39 and 40") and the depth row's is 20/20 at
   `e1c83313` ("refreshed rounds 25, 26, 39 and 40") — both lag the base truth (command A @ base =
   **135/135 files, 21/21 rule blocks**), and both refreshed-lists omit round 41. This is the accepted
   append-only pattern (round sections carry the fresh numbers; round 39's D1 lesson is the precedent);
   the round-42 section already records 135/135 and 21/21. The round-43 landing adds one knowledge entry
   + S135 + a README map row → command A at the new tip will read 136/136, 21/21. If the L1 refreshes
   these rows, use command A at the measured revision; if it appends a Round-43 section instead, the rows
   stay one round behind — same pattern, not new debt.
3. **Range movement under the round-43 plan: none.** Every live (non-pinned) range citation sits in a
   file the plan does not modify: Capabilities v1 row cites `SKILL.md:316-343` (plan keeps all SKILL
   bytes; v4 region verified byte-identical to `d1681696` already at base — region lines 521–539,
   sha256 `99cd54d7fe884748`, 13852 B, 13 cols / 15 rules); the BE row and SHONEN box 4 cite
   `PROVINCE.md:378-384` / `97-125` / `386-394` / `:157` / `:376` (C1/C2 touch neither PROVINCE nor
   SKILL; appends elsewhere don't move these). SHONEN box 1's v4 sentence ("unscored as a claim…") will
   flip to scored prose when R43-C1 lands — prose only; every ranged claim in that box is pinned at a
   historical commit and stays true.
4. **Plan preconditions already hold at base:** frozen `tools/round-42/{sqfs-triage-v4.py,
   indep-eval-v4.py,fixtures.json}` byte-identical to `d1681696` (sha prefixes `497bab67…`, `7a135dd3…`,
   `9f957663…`); S135 absent from `corpus/SOURCES.md` (frontier step opens it); S131–S134 present; gate
   before-state exit 1 / 18 rows confirmed by direct run.
5. **Method note (for wave-2 seats):** a hash that fails `git cat-file -t` mid-check may be the checker's
   own transcription, not card debt — this seat mistyped `…8d7e5326` for the real `…8d7e5326`-family hash
   once; the programmatic extraction of all 15 full hashes from the base files shows **every** carded hash
   is a real commit. Verify hashes by extraction, never by eye.

## Evidence index (all under `.ufo/waves/round-43/w1/artifacts/R43ScoutCalib/`)

- `cmdA.log` — command A output at 17 revisions (base, r42 scores/landing/spotcheck, r41 landing+measured,
  r40 stop+landing, r39 freeze-era+registry, r38/r36 measured, r36 base, r31, r26, luna-r7, luna-r3 pins).
- `selftests-and-bytes.txt` — 35/35, 45/45, 27/27 selftest tails; gate exit summary; frozen-tool byte
  identities; v4 region identity note.
- `gate-at-base.txt` — full `local-source-gate.py` run at base (exit 1, 18 FAIL rows, S126 ok line).
- `skill_check.py`, `skill_check2.py` — the read-only range/shape probes (marker→table→block extents,
  craft-section extents, region sha256).
