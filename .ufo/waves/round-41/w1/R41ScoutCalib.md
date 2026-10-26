DEFECTS FOUND — calibration pre-check at `49096c7e6f226af0c750c4b003be58883cb6049f`: of ~120 checkable statements in `SHONEN.md`, `SCORECARD.md` `## Owned axes` and `## Capabilities`, every commit hash, every count, every `PROVINCE.md` range and every cited path matches; 3 statements about `SKILL.md` rule-block-18 / craft-section line ranges are stale since round 40 (verified-wrong), 3 more are inconsistent, imprecise or incomplete (low severity). No numeric count is wrong.

Seat `R41ScoutCalib` (scout, leaf). Read-only: git objects at the base plus the lane worktree (clean for `tools/`, `evidence/`, `corpus/`; only untracked `.ufo/waves/round-41/` and `plans/round-41-claims.md` differ). No REA/unblob/extractor was run; no reserved carrier touched; no tool installed or upgraded (none needed). Scratch `/fast/scratch/hyaku/kaidoku-r41/R41ScoutCalib` removed before yield.

## 1. How it was done

- Dumped `SHONEN.md` (12 lines, 4 `[~]` boxes), `SCORECARD.md` L19-32 (`## Owned axes`) and L615-635 (`## Capabilities`), plus `SKILL.md`/`PROVINCE.md` via `git show 49096c7e…:<path>` (SKILL 1405 lines, PROVINCE 394, SCORECARD 3452).
- Hash audit: `git cat-file -t` + `git merge-base --is-ancestor <h> 49096c7e` for 22 hashes (4d62ee5a, 52b0eb29, 6fdaf4f1, c369242f, ebe2cb4a, cab59f22, 3395b6d, 7ef837a4, a79945c4, 638fb211, 58116aa1, 4072ebb3, 08c7a729, c265db9b, 75af886a, 42c10a58, 7fce3086, 6645585, 283aad7f, 8fcda41c, …): all `commit`, all ancestors.
- Path audit (`artifacts/R41ScoutCalib/pathcheck.py`, brace/glob expansion, vs `git ls-tree -r` at base): 83 distinct backticked paths OK; the 8 "MISS" lines are parser artefacts (`K1..6` literal brace, `A2Capability*.md` cited by basename under `.ufo/waves/round-32/a2audit/`, `AXES.md` is the fleet file, `result.json` is relative) — all resolve by hand (`pathcheck.out`).
- Command A (SCORECARD L93-122, copied verbatim to `command-a.py`, run `python3 command-a.py <rev>` in the lane) at 15 revisions: `command-a-matrix.txt`.
- Command B (`jq` recipe at SCORECARD L132-141): baseline `6645585…` 0/9, after `c265db9b…` 9/9, score 10 — matches the calibration row.
- Selftests and counters at base (`selftests-and-counters.txt`).
- Re-runnable checker for the landing: `artifacts/R41ScoutCalib/calib-check.py` (`python3 -I -B calib-check.py --root <lane> --rev <rev> [--asserted file.json]`, 22 mechanical rows, git-object reads only; exit 1 on any mismatch). At base: `calib-check-at-49096c7e.txt` — 21 match, 1 MISMATCH (block 18 range).

## 2. Statement table

Legend: S = `SHONEN.md` line; O = SCORECARD `## Owned axes` row/line; C = SCORECARD `## Capabilities` row line.

### 2a. Mismatches / calibration debt

| # | location | asserted | observed at 49096c7e | match? |
|---|---|---|---|---|
| D1 | S:6 ("rule block 18 … marker v1, eight labels, `SKILL.md:316-343`") | block 18 = lines 316-343 (present tense "is") | block 18 = **316-346**; v1 marker at line **336** (was 333 at 52b0eb29); `git diff 52b0eb29 49096c7e -- SKILL.md` shows round 40 added a 3-line supersession note at :330-335 ("Superseded for routing by rule block 19 … mislabels mixed-link images…") | **NO** — true at 52b0eb29 only; stale since 4d62ee5a. 8 labels ✓ |
| D2 | C:629 (triage v1 row evidence `SKILL.md:316-343 (rule block 18; table after <!-- sqfs-triage-table v1 -->)`) | 316-343 | 316-346 (same cause as D1) | **NO** |
| D3 | O:24 depth row, Evidence column ("craft section `SKILL.md:81-343` (heading line 81, last non-blank line 343 at `52b0eb29`)") | craft section ends at 343 | at base the craft section is **81-375** (rule 19 added). The Score cell of the same row already says 19/19 at 4d62ee5a with block 19 at 348-375 and S:6 says 81-375, so the row contradicts itself and SHONEN | **NO (internal inconsistency)** — the "at 52b0eb29" qualifier makes it historically true but the row is the *current* evidence cell |
| D4 | O:24 depth row Last-change cell ("count refreshed rounds 25, 26, 39 and 40") vs O:23 coverage row ("25, 26, 31, 36, 38, 39 and 40") | depth refreshed 25, 26, 39, 40 | the depth row's own text cites depth measurements at round 31 (`c369242f`, 17/17) and cab59f22 (round 36 recount; command A there gives 17/17, 122/122); both rows measure the same recipe at the same commits | **imprecise** (low) |
| D5 | C:627 (LE row: "Big-endian/AVM not demonstrated") vs C:628 | big-endian not demonstrated | C:628 (same table, later round) demonstrates standard big-endian through `squashfs_v4_be`; only AVM-BE stays unpromoted | **stale sentence** (low; history row, but readable as current) |
| D6 | C:622 pointer `.ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json` for "r8 natural control (oom-kill; disable proven necessary)" | the file evidences the oom-kill | the file is an REA `error: Analysis failed / code: cancelled`, `exit_code: null`, `exit_signal: null`; the string "oom" does not occur in it. The oom-kill is attested elsewhere: `.ufo/waves/arc2-loop1-round8/R1.md:23,50,57` (`Result=oom-kill`, journal line), `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:29-30` | **partial** — pointer supports "control analysis did not complete", not "oom-kill" (low) |
| D7 | S:10 / C:630 ("26 of 26 held-out envelopes", independent evaluator) | 26/26 = depth increment | counts reproduce (see 2b); but `corpus/lessons/round-40.md` `## Wave 2` records that 18 of 26 envelopes were already decided by the v1 table and expected labels came from the same class map the table was written to (`w2/R40W2C2AxisFit.md`, `w2/R40W2C2Shortcut.md`) — neither SHONEN nor row 630 carries that bound (S:10 states the *round-39* bound only). Not recomputed here (cited from the lesson) | **omission** (this is what R41-C2/D3 repairs; the landing must state the new bound rather than grow the debt) |

### 2b. Statements that match

| location | asserted | observed | match? |
|---|---|---|---|
| S:6 | craft section `SKILL.md:81-375` at 4d62ee5a; 19/19 rule blocks | heading `## Queue-drain craft` :81, last non-blank :375, 19 `- **` blocks at both 4d62ee5a and base; command A `citation_resolved_rules 19/19` | yes |
| S:6 | rule block 19 = `SKILL.md:348-375`, v2 marker | block 19 :348-375; `<!-- sqfs-triage-table v2 -->` :361 | yes |
| S:6 | `sqfs-triage-v2.py --selftest` 45 cases | `SELFTEST cases=45 pass=45 fail=0` | yes |
| S:6, C:629 | `tools/round-39/sqfs-triage.py --selftest` 35 cases; `R39W2C2Rescore/sqfs-triage-selftest.txt` | 35/35 pass (still green against the v2-bearing SKILL: `real-skill` case ok); file exists | yes |
| S:6 | 18/18 at 52b0eb29 | command A: 18/18, 128/128 | yes |
| S:6, C:629 | "eight labels" in v1 table | 8 rows / 8 distinct labels (SKILL :337-346) | yes |
| S:8 | R40-C1 3/4 honest stop; receipts `corpus/evidence/round-40/c1/` (V1 V2 L1 L2); `R40W2Repro*.md` | `.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json`: carriers_matched 3, exit_code 1, met_target false; four receipt dirs; `R40W2ReproL/V1/V2.md` exist | yes |
| S:8, C:628 | round 39: counter 6/6 at `6fdaf4f1`; receipts K{1..6}/{after,run}.json | `tools/round-39/c1-counter.py --rev 6fdaf4f1 --freeze 8fcda41c… --pkg65 …rea-agents` → `carriers_matched 6`, `met_target true`, rc 0; all 12 receipt files in tree | yes |
| S:8 | `corpus/lessons/round-39.md`, LOG round-39 entry | exist (`LOG.md:3137` "2026-10-26 — round 39") | yes |
| S:10, C:629 | round 39: 20/20 held-out, seed = freeze `8fcda41c…`, H01–H20 | `tools/round-39/c2-counter.py --rev 6fdaf4f1` → 20/20, met_target true (also 20/20 at base); manifest seed `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b`, 20 items | yes |
| S:10, C:630 | round 40: 26/26, seed = freeze `7fce3086…`, rev `42c10a58…`, `c2-at-42c10a58.json`, exit 0 | `tools/round-40/c2-counter.py --rev 42c10a58… --freeze 7fce3086…` → matched 26 n 26 met_target true, 12 distinct decisions; also 26/26 at base; score json says 26/26 exit 0; manifest 26 items, seed = freeze | yes |
| S:10 | selftests 35/35 and 27/27 | `round-39/sqfs-triage` 35/35; `round-39/c2-counter` 27/27 (round-40 `c2-counter` 42/42, not cited) | yes |
| S:10, C:629 | "ten generator classes"; "smallest table that also scores 20/20 is 8 rows / 7 non-`*` cells" | round-39 manifest has 10 classes (fold into 8 labels); `R39W2C2Shortcut.md` :5, :17, :55-78 "8 rows, 7 non-`*` cells … proved floor" | yes |
| S:10 | `R40W2C2IndepEval.md` reproduces 26/26 | report line 1-7: CONFIRMED, 26/26 exit 0 at 42c10a58 | yes |
| S:12 | `PROVINCE.md:97-125` Adjacent; safety :116-118; tooling bullet :119-125; installer :110-115 | `## Adjacent` :97; installer bullet :110-115; "Quality/safety verdicts" :116-118; "Tooling, dated 2026-10-26" :119-125; :126 blank; next heading beyond | yes |
| S:12 | range "unchanged from round 36 and byte-identical at 52b0eb29" | sha256 of lines 97-125 identical at 52b0eb29 and base; last change `a6c433b5` "round-36: wave-2 adjacency fix" | yes |
| S:12 | round-39 additions `PROVINCE.md:378-384`, row :382, note :384 | `## Round-39 additions to Core` :378; `squashfs_v4_be` row :382; "Round-39 frontier note" :384 | yes |
| S:12 | round-40 section + note `PROVINCE.md:386-394` | heading :386; note :394; file ends :394 | yes |
| S:12 | `:157` and `:376` carry a dated round-39 pointer | :157 "[2026-10-26 … Round 39: standard BE v4 is Core …]"; :376 "Round-38 note … Round 39: superseded …" | yes |
| C:628 | `PROVINCE.md:378-384`; carriers.json; K1..K6; gzip+xz (comp_id 4) | ranges as above; `.ufo/waves/round-39/c1/carriers.json` present; counter `xz_leg_detail` K1-K5 1, K6 4; six K dirs | yes |
| O:23 | coverage 9.72 → 10.0; baseline `a79945c4` | command A at a79945c4: mapped 70 of 72, missing 2, score 9.72; at base 130/130, 10.0 | yes |
| O:23 | 130/130 at 4d62ee5a, `missing []`, `dangling []`; two entries added in round 40 | 130/130, 0/0; `7fce3086` 129, `42c10a58` 130; added files `r40-sqfs-triage-v2.md` and `r40-avm-be-squashfs-core.md` | yes |
| O:23 | 128/128 after round 39 (+ r39-sqfs-outcome-triage at 8fcda41c, r39-be-squashfs-v4-core at 6fdaf4f1); 126/126 after round 38 (+ r38-sasquatch-be…, unblob-format-matrix); 124/124 after round 36 (+ r36-sasquatch…, unblob-sasquatch-dependency) | 124 at ffc81341, 126 at 3b960fe5, 127 at 8fcda41c, 128 at 6fdaf4f1; the added file names match exactly | yes |
| O:23 | 122/122 at cab59f22; 116/116 at c369242f; 109/109 at ebe2cb4a; 108/108 (round-25 EVM entry, 08c7a729); 107/107 at 7ef837a4; 78/78 at 3395b6d | command A: 122, 116, 109, 108, 107, 78 — all with 0 missing / 0 dangling | yes |
| O:24 | 19/19 at 4d62ee5a; 18/18 at 52b0eb29; 17/17 at c369242f and ebe2cb4a; 9/9 at 638fb211 | 19/19, 18/18, 17/17, 17/17, 9/9 (638fb211 maps 72/72) | yes |
| O:24 | rule blocks grew 9 → 17 "in eight commits from 58116aa1 to 4072ebb3" (2026-10-18/19) | rule counts per SKILL-touching commit: 9 → 10 (58116aa1) → 11 (265e1aa5) → 12 (8cc81a84) → 13 (ba06c4dd) → 14 (28aa7a98) → 15 (2fba56fe) → 16 (9c1d1fef) → 17 (4072ebb3) = exactly 8 count-changing commits; dates 2026-10-18/19 | yes |
| O:24 | row kept 9/9 until round 25 recount at 08c7a729; baseline range `SKILL.md:77-191` at a79945c4 | 08c7a729 17/17; at a79945c4 heading :77, last non-blank :191, 9 blocks | yes |
| O:25 | calibration 9/9 aligned, command B, measured at `c265db9b`; row said `75af886a` until round 26 | command B → 0/9 baseline, 9/9 after at `c265db9b`; `result.json` `.measured_revision` = c265db9b; the correction commit is `46ebfd2f` "round-26: R26-C2 calibration repair"; `75af886a` is the luna-round-2 commit | yes |
| O:27, O:30 | baseline source revision `6645585…`; scores `round(10*n/d, 2)` | `rubric.json`/`result.json` `baseline_revision` = 6645585…; 70/72 → 9.72 | yes |
| C:630 | rule block 19 interpreter `tools/round-40/sqfs-triage-v2.py`; reproduced `R40W2C2Rescore.md` | exists; rescore report exists | yes |
| C:619 | "10-leg" battery, receipts `luna-round-6/receipts/` + `receipts-B/` | `leg-1..10.md` in both; report "Battery (10 legs)", "Cross-lane agreement 10/10" | yes |
| C:621 | five paths' sha256s; "zero-drift 6-line 5-hash receipt pair" | pre and post files each 6 lines (timestamp + 5 hash lines); hash lines identical across the pair | yes |
| C:622 | r7 wall-fall `ev_a4aa9b0d…`, 91.6MB PE | entry `2026-10-18-arc2-r7-pe-wall.md` carries `ev_a4aa9b0d81b0…`, "91.6MB Godot ARM64 PE" (oom half: see D6) | yes |
| C:625 | `quote-fidelity.py --selftest` | runs: `QUOTE_FIDELITY_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0` | yes |
| C:623, 626, 620, 624 | pointers (`tools/round-27/xpin-attribute.mjs`, `c2-xpin-check.py`, `BuildXpinTool.md`, `run-carriers.sh`, `corpus/SOURCES.md` …) | all present | yes |
| C:634 | "base `283aad7f` lines 2136, 2208, 2375" = three append-only records | `git show 283aad7f:SCORECARD.md` L2136 curated source registry, L2208 raw-quote regression audit, L2375 Ghidra-session log capture; `A2Capability{13,14,17,27}.md` under `.ufo/waves/round-32/a2audit/` exist | yes |
| O:23, S:8… | all remaining cited receipts/entry paths (`corpus/knowledge/2026-10-26-r40-*.md`, `R40W2DepthCount.md` — it records command A 130/130, 19/19 at 42c10a58 and 4d62ee5a, `tools/round-38/c2-counter.py`, `tools/round-36/c2-counter.py`, `corpus/README.md` `## Coverage map`) | present; `R40W2DepthCount.md` numbers equal this seat's recount | yes |

Third-party corroboration of the 130/130, 19/19, `SKILL.md:81-375` triple: `corpus/lessons/round-40-verifier-spotcheck.md:60` asserts it "at `c4895cf1`"; this seat reproduced those three values at base. That spot-check did not examine the rule-block-18 range, which is where D1/D2/D3 sit.

## 3. What the round-41 landing will move (so it does not grow the debt)

Statements that go stale the moment round 41 lands, each with the cheap repair:

1. S:6 / C:629 / O:24 SKILL ranges: rule block 20 (marker `<!-- sqfs-triage-table v3 -->`) is appended after :375, so `81-375`, "19/19", "block 19 at 348-375" must become 81-N, 20/20; the draft's prose repairs "riding the block" (R40-CL5 M1-M3, L1-L6 in `plans/round-41-claims.md`) edit blocks 18/19 in place, which will shift 316-346 and 348-375 again. Repair D1-D3 in the same edit by writing ranges only after the final SKILL.md is in the tree and run `calib-check.py` with `--asserted` set to the new numbers (the `rule_ranges` object takes any block numbers). Also: the `## Instrument registry` text after :380 and every `SKILL.md:NNN` citation below it shifts by the inserted lines.
2. Command A counts (130/130, 19/19): each new `corpus/knowledge/` entry needs a `corpus/README.md` Coverage-map row (otherwise `missing` > 0); each new rule block needs a `corpus/knowledge/…md:N-M` citation that resolves (otherwise the depth fraction drops below 20/20).
3. `PROVINCE.md:386-394` stays valid only if the new Core row is appended after :394 (the draft says "`## Round-41 additions to Core`"); if the landing edits :157 / :376 / :384 / :394 or the round-40 note ("measured, not promoted" → promoted), re-check S:12 and C:628's `:378-384`. The Adjacent block (:97-125) must stay byte-identical or S:12's "byte-identical at 52b0eb29" clause must be re-dated.
4. S:10 / C:629-630 selftest counts (45, 35, 27): any edit to `tools/round-40/*` instead of new `tools/round-41/*` changes them; a v3 interpreter will carry its own count — record the number that `--selftest` prints, not an estimate.
5. S:6 and O:24 name a single "at <hash>" for the 19/19 recount; the landing hash cannot be named inside the commit that contains it — use the round-40 pattern (measure at the parent, record in the follow-up commit) and say which.

## 4. Commands and exit codes (all read-only)

- `git -C <lane> show 49096c7e…:{SHONEN,SCORECARD,SKILL,PROVINCE}.md`; `git ls-tree -r --name-only 49096c7e…` (28693 paths); `git cat-file -t`, `git merge-base --is-ancestor` for 22 hashes: all commit / all ancestor.
- `python3 command-a.py <rev>` for 49096c7e, 4d62ee5a, 52b0eb29, 6fdaf4f1, 42c10a58, c4895cf1, c369242f, cab59f22, ebe2cb4a, 08c7a729, 4072ebb3, 638fb211, 3395b6d, 7ef837a4, a79945c4 → `command-a-matrix.txt` (all `missing 0 dangling 0` except a79945c4: 70/72, missing 2).
- `python3 -I -B tools/round-40/sqfs-triage-v2.py --selftest` → 45/45; `tools/round-39/sqfs-triage.py --selftest` → 35/35; `tools/round-39/c2-counter.py --selftest` → 27/27; `tools/round-40/c2-counter.py --selftest` → 42/42.
- `python3 -I -B tools/round-39/c1-counter.py --root <lane> --rev 6fdaf4f1 --freeze 8fcda41c… --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` → carriers_matched 6, met_target true, rc 0.
- `python3 -I -B tools/round-39/c2-counter.py … --rev 6fdaf4f1 --freeze 8fcda41c…` → 20/20 met (exit code field absent in the json; same 20/20 at base).
- `python3 -I -B tools/round-40/c2-counter.py --root <lane> --rev 42c10a58… --freeze 7fce3086…` → 26/26 met, exit 0; same at base.
- `tools/round-40/c1-counter.py … --no-rerun` → exit 2 `rerun_disabled` (it binds a fresh REA run; not run here — no REA was executed); the 3/4 exit-1 figure was checked against the stored `.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json` only (carriers_matched 3, exit_code 1), not re-run by this seat.
- Command B jq recipe → baseline 0/9 at 6645585…, after 9/9 at c265db9b…, score 10.
- `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --selftest` → 28/28 CLEAN.
- `calib-check.py --rev 49096c7e…` → 22 rows, 1 MISMATCH, exit 1.

## 5. Limits

- Not checked: statements outside the three named sections (e.g. SCORECARD `## Current assessment`, per-round sections, `## Reconciled current state`, SKILL.md rule prose); `AXES.md:33-39` (fleet file, cited at SCORECARD :14, outside scope); the C:621 "three client configs" description beyond the receipt files; semantic truth of cited reports beyond the quoted numbers.
- D7's "18 of 26 already decided by v1" is read from `corpus/lessons/round-40.md`, not recomputed.
- `pathcheck.py` reads `tree.txt` (= `git ls-tree -r --name-only 49096c7e…`, regenerate it) and the dumped section files from its cwd; `calib-check.py` is self-contained.
- Artifact dir: `.ufo/waves/round-41/w1/artifacts/R41ScoutCalib/` (calib-check.py, calib-check-at-49096c7e.txt, command-a.py, command-a-matrix.txt, pathcheck.py, pathcheck.out, selftests-and-counters.txt). All small; no vendor bytes.

Report: .ufo/waves/round-41/w1/R41ScoutCalib.md
