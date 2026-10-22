# Round 27 wave 1 — ReviewHygieneTargets: independent re-derivation of the 11 stale SCORECARD statements

Seat: KaidokuR27.ReviewHygieneTargets. State judged: lane main `a4f674b343d8564e21f7eb8984630a95089c82d6`
(working-tree SCORECARD.md sha256 `fbd7691c…` byte-identical to `git show HEAD:SCORECARD.md`; checked 2026-10-22T14:57Z).
Round-26 landed after the c27f445 report: owned-axes rows were refreshed (109/109 at `ebe2cb4a`) and a Round-26
section now discloses the 11 findings at `:3064-3066`. Line numbers below are current at `a4f674b3`.
Commands ran 2026-10-22T14:57Z-15:02Z UTC, read-only git/file reads in the lane. No REA calls, no tool installs,
no web sources. Nothing written in the lane except this report.

## Verdicts

| # | Line | Command (one per item) | Observed | Verdict |
|---|---|---|---|---|
| 1 | 12 | `sed -n '11,12p;22,24p;2941,2942p' SCORECARD.md` | Sentence is under `## Current assessment — 2026-10-15` and self-tagged `` `[INFERENCE]` `` at :11. Rows :22-24 read `9.72 → 10.0`, `10 → 10`, `0 → 10` (all current 10); :2941-2942 says "(coverage/depth/calibration all10)" | **inference only** — a present-tense reading contradicts the current rows, but the sentence is dated and inference-tagged; agrees with C2Width's part-inference call |
| 2 | 46 | `python3 -I -B recipeA.py a4f674b3…` (recipe A, `:94-122` verbatim, exit 0) | `{"mapped": 109, "knowledge_files": 109, "missing": [], "dangling": [], "coverage_score": 10.0, "rule_blocks": 17, "depth_score": 10.0}` | **still disagrees** — C6 says "Current map is 70/72, missing r14-01 and r14-02"; actual 109/109, missing [] |
| 3 | 55 | same recipe A run as item 2 | 109/109 at HEAD; coverage row :22 now states 109/109 at `ebe2cb4a` | **still disagrees** — "Historical 70/70 is not current 72/72" is stale twice over (not 72, and 70/70 was never current) |
| 4 | 78-80 | `grep -n 'Safety-verdict scope' corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md && sed -n '114,116p' PROVINCE.md` | Entry line 244 (present at HEAD): "Safety-verdict scope (round 9): The phrases 'Benign payload' … are historical wording, not a present endorsement". PROVINCE refusal is at :114-116; card cites :107-109 — baseline-scoped per card rule :17-18, so the pointer itself is defensible | **still disagrees** — "the old entry remains correction debt" is contradicted by the entry's own round-9 scope note qualifying exactly those phrases |
| 5 | 81-83 | `grep -n 'solc-0.8.37\|CLOSED (arc2-r7\|organic cores still exceed' PROVINCE.md && sed -n '622p' SCORECARD.md \| grep -o '91.6MB-class PEs'` | PROVINCE :91-92: "real solc-0.8.37 carriers (Core, arc3-r1/r3)"; :139: ">90 MB PE scale wall — CLOSED (arc2-r7…"; SCORECARD :622: "runs REA/Ghidra analyzes of 91.6MB-class PEs". Only PROVINCE :85-86 "the huge organic cores still exceed the cap" still matches | **still disagrees** — of the three named items, "real compiled EVM input" and "large PE analysis" are documented held/closed; "oversized cores" holds |
| 6 | 152-154 | `sed -n '56p;152,156p' SCORECARD.md` | :56: "**Version drift:** closed by luna-round-2 (2026-10-16)"; :152-154 planned field still open (no done marker, next bullet is `retired:`) | **still disagrees** — the planned reconciliation is recorded as already done at :56; the open plan is a stale internal contradiction |
| 7 | 907 | `grep -c '^| citation-drift probe \|' SCORECARD.md; sed -n '918p;1266,1268p' SCORECARD.md` | 0 capability-table rows carry that row (tables at :617, :2133, :2205, :2372; data rows :619-622, :2135, :2207, :2374). The row text appears only as the inline quote at :918. Omission is disclosed in-card at :1266-1268 ("r4's citation-drift row never entered the capabilities table") | **still disagrees** — "+ capability row entered" is false as a table fact at HEAD, but the omission is disclosed |
| 8 | 615-624 | `sed -n '617,624p;2133,2136p;2205,2208p;2372,2375p' SCORECARD.md \| grep -cE '^\| [a-z]'` and `sed -n '2364p' SCORECARD.md \| grep -o 'capability rows 6→7'` | Section table has 4 data rows; card-wide count is 7 (rows :619-622, :2135, :2207, :2374); :2364 says "capability rows 6→7". The `## Capabilities` section has no pointer to the appended tables (which are self-labeled "Capability addition (append-only)" / "(demonstrated before this row)") | **inference only** — both counts are observed; calling 4-vs-7 a mismatch rather than append-only design is interpretation, as C2Width says |
| 9 | 631-632 | `sed -n '619,622p;2135p;2207p;2374p' SCORECARD.md \| awk -F'\|' '{print $(NF-1)}'` | First-working rounds: luna-round-6, luna-round-8, arc2-loop1-round2, arc2-loop1-round7, arc3-loop1-round13, round-14, round-17 — so even the section's own table has an entry outside "rounds 6-8" | **inference only** — stale by direct observation, but the sentence was declared at luna-round-10 and may be read as historical; matches C2Width |
| 10 | 14 | `sed -n '33,39p;79p' /home/vgpnk/Projects/shokunin/AXES.md; git -C /home/vgpnk/Projects/shokunin log -1 --format='%h %cI' -- AXES.md; git cat-file -e HEAD:AXES.md` | AXES.md:33-39 is the multi-claim/lowest-axis rule ("At least one claim works the lane's lowest-scoring non-retired axis…"); the score `0–10` rule is at :79. Last AXES.md commit 84bade0 2026-10-16T15:55:20-03:00, after the 2026-10-15 statement. AXES.md absent from the lane tree (exit 128) | **still disagrees** — the cited span does not contain the numeric-field rule the sentence claims to satisfy; that this is post-hoc drift rather than always-wrong is inference |
| 11 | 3061 | `git log -1 --format='%h %cI' 81f63f36 bd0c84bc ebe2cb4a 46ebfd2f; sed -n '14p' corpus/claim-freezes.tsv; grep -n pre_freeze_probe .ufo/waves/round-26/claims.json` | Probe 11:59:16Z (pre-freeze, claims.json :7-9); C2 instrument 81f63f36 12:31:00-03:00; C1 data ebe2cb4a 12:47:57Z-3; repair 46ebfd2f 12:48:48-03:00; C1 instrument bd0c84bc 12:49:24-03:00 (after the C1 data). claim-freezes.tsv :14: "round-26 FLAGGED INSTRUMENT_ABSENT … instruments written in wave 1 and committed after"; card :3066 discloses the same | **still disagrees** — the planned order ("committed before any REA run") was not executed; the departure is now disclosed in-card (:3066) and in claim-freezes.tsv, so it is no longer undisclosed |

## Summary

Still disagrees: items 2, 3, 4, 5, 6, 7, 10, 11 (8 items; 7 and 11 with in-repo disclosures now attached).
Inference only: items 1, 8, 9 — matching C2Width's wave-2 grouping. Now agrees: none.
Item 4's `PROVINCE.md:107-109` pointer holds under the card's baseline-scoping rule :17-18; item 11's mismatch is
plan-vs-execution, disclosed at :3066 and claim-freezes.tsv :14. The hygiene scribes' drafts should be checked
against these eight observed disagreements and three inference calls, not against "11 open defects".

## Method and evidence

- HEAD = `a4f674b3` ("round-27: freeze claims…"); `git rev-parse HEAD` + sha256 comparison, 14:57Z, exit 0.
- Recipe A extracted verbatim from SCORECARD.md:94-122 (fence body) to
  `/fast/scratch/hyaku/kaidoku-r27/seats/ReviewHygieneTargets/recipeA.py`
  (sha256 `236dde1da2d78b5ee2f4827fb884901857385fe1f40bbb09bbb4b4ab4f6e9b01`); run 15:02:34Z, exit 0; raw output
  `recipeA.out` (sha256 `4f29fd60e7ef0b166cf9857bbe2d5d114187f4f15030e13f928266a423fc0c5e`). A first attempt
  extracting the fence including the heredoc wrapper (recipeA.sh) hung and was discarded; the .py body run above
  is the producing command for items 2-3.
- Labels: every table verdict row cites its producing command; exit codes: recipe A 0; `git cat-file -e HEAD:AXES.md`
  128 (expected, AXES.md is fleet-level); `grep -c` printed 0 for item 7 (no table row). All observations; the
  inference component of items 1, 8, 9, 10 and 11 is labeled in the verdict cells.
- No tool installs; no pacman/npx/uv use; no REA runs (none required); sources are local lane files and fleet
  AXES.md only; nothing outside the lane was mutated and no git/jj state was written.
