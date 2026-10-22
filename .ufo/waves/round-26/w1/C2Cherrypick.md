# Round 26 wave 1 — C2Cherrypick (critic): stale self-assessment outside K1-K6

Seat: KaidokuR26.C2Cherrypick. Revision read: c27f445e70cedbaf5300b2fd0a53e821d9b659a9 (Git objects only; `git show c27f445:<path>`).
Commands ran 2026-10-22T12:12Z to 12:16Z UTC. No REA calls, no tool installs, nothing written in the lane except this report.

## What this seat attacks and verdict

Target: the R26-C2 item selection (K1-K6 in `.ufo/waves/round-26/claims.json`), tested for stale self-assessment statements it leaves out.
Verdict: **holds as scoped, with disclosures required.** The claim says "Not a full audit of SCORECARD or SHONEN", so the selection is honestly partial.
Counterexample to any wider reading: 11 further statements below still disagree with repo state at c27f445, so "0 mismatches" will not mean the card is calibrated.
Smallest safe correction: list these as disclosures in the round report. Per the assignment they are not new items.
Impacted axes: calibration (directly); coverage and depth (stale frontier and count statements).

## Further mismatches (outside K1-K6)

Recipe A means SCORECARD.md `## Measurement recipes` recipe A, extracted verbatim to `recipeA.py` and run as `python3 -I -B recipeA.py <REV>` in the lane, exit 0.

1. `SCORECARD.md:12` says "calibration is the lowest axis under these heterogeneous, bounded proxies".
   Observed: the Owned axes rows at `SCORECARD.md:22-24` all score 10 (10.0, 10, 10). `SCORECARD.md:2941-2942` says "a tied-lowest owned finite proxy (coverage/depth/calibration all10)".
   Label: observation (contradiction inside the card). The statement is self-tagged `[INFERENCE]` under a 2026-10-15 heading; reading it as a current claim is my inference.
2. `SCORECARD.md:46` (C6, in `## Reconciled current state`) says "Current map is 70/72, missing r14-01 and r14-02".
   Observed: recipe A at c27f445 gives `"mapped": 108, "knowledge_files": 108, "missing": []`. Label: observation. The section is a round-1 record, but it is worded as current.
3. `SCORECARD.md:55` says "Historical 70/70 is not current 72/72". Observed: same recipe A output, 108/108. Label: observation.
4. `SCORECARD.md:78-80` (`## Open gaps`) says the jq "benign" wording "remains correction debt".
   Observed: `git show c27f445:corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md | grep -n -i benign` shows line 244 "**Safety-verdict scope (round 9):** The phrases \"Benign payload\" ... are historical wording, not a present endorsement".
   `git log -S'Safety-verdict scope (round 9)'` finds it was added by 40162fc7 "luna-round-9: ... jq-shadow safety-verdict scope qualification" (2026-10-16). The other bullets in this section carry "closed by" notes; this one has none. Label: observation.
   Side note: line 79 cites `PROVINCE.md:107-109` for the safety refusal. At c27f445 those lines are the core-supplied and source-available refusals. The safety refusal is at :114-116 (shown by `git show c27f445:PROVINCE.md | sed -n 105,117p`). At baseline a79945c4, lines 107-109 do hold the safety refusal, and the card's rule at :17-18 scopes line citations to the baseline, so this pointer holds by that rule. Label: observation.
5. `SCORECARD.md:81-83` (Domain frontier) says "real compiled EVM input, oversized cores, large PE analysis ... remain as documented".
   Observed at c27f445: `PROVINCE.md:139` says "**>90 MB PE scale wall** — CLOSED (arc2-r7". `PROVINCE.md:91-92` says "real solc-0.8.37 carriers (Core, arc3-r1/r3)". The capability row at `SCORECARD.md:622` says it "runs REA/Ghidra analyzes of 91.6MB-class PEs".
   Commands: `git show c27f445:PROVINCE.md | sed -n 73,94p` and `| grep -n -i '91\.6\|EVM'`, exit 0. Label: observation. The "oversized cores" item still matches PROVINCE:83-86.
6. `SCORECARD.md:152-154` (**planned:**) says "calibration — reconcile the still-historical province/skill surface summaries against the live version-pinned REA inventory".
   Observed: `SCORECARD.md:56` says "**Version drift:** closed by luna-round-2 (2026-10-16)". The planned field was never marked done. Label: observation (internal contradiction).
7. `SCORECARD.md:907` (arc2-loop1-round4) says citation-drift probe "+ capability row entered".
   Observed: `grep -n '^| Capability | What it can now do'` finds four capability tables (:617, :2133, :2205, :2372). Their rows (:619-622, :2135, :2207, :2374) contain no citation-drift probe row. The only match is the inline quote at :918.
   Already disclosed at `:1265-1268` ("r4's citation-drift row never entered the capabilities table"). Label: observation.
8. `SCORECARD.md:615-624` (`## Capabilities`) holds 4 rows. The card-wide count is 7: appended rows at :2135, :2207 and :2374, and `:2364` says "capability rows 6→7".
   A reader of the `## Capabilities` section alone undercounts by 3, and the section has no pointer to the appended tables. Label: the count is observation; calling it a mismatch rather than append-only design is inference.
9. `SCORECARD.md:631-632` (`## Saturation`) says "Capabilities entered the table in rounds 6-8".
   Observed: the same table lists first-working rounds arc2-loop1-round2 and arc2-loop1-round7 (:621-622). Rounds 13, 14 and 17 added rows elsewhere. Label: inference that this is stale; the sentence was declared at luna-round-10 and may be read as historical.
10. `SCORECARD.md:14` says "Numeric axis fields satisfy fleet `AXES.md:33-39`".
    Observed: `sed -n 33,39p /home/vgpnk/Projects/shokunin/AXES.md` (sha256 04ea5c9e89c91cef645536ab56863ebb014dce617e7083e54968092968a7d993) is the admission and lowest-axis rule. The "score 0–10" rule is at `AXES.md:79` (`grep -n '0–10'`).
    `git log -1 -- AXES.md` in the fleet repo (read-only) gives 84bade0 2026-10-16T15:55:20-03:00, which is after the 2026-10-15 statement. Label: observation of current content; that the pointer drifted rather than was always wrong is inference. AXES.md is not in the lane tree (`git cat-file -e c27f445:AXES.md` fails).
11. `SCORECARD.md:3061` (latest **planned:**) says "with the counting script and expected values committed before any REA run".
    Observed: `claims.json` `pre_freeze_probe` records an REA 6.5.0 `inspect-binary-layout` run at 2026-10-22T11:59:16Z, exit 0, before the freeze. At c27f445, `git cat-file -e c27f445:tools/round-26` fails (ABSENT).
    `claims.json` R26-C1 `limits` says "Any verdict value counts as complete", so no per-verb expected verdicts are committed. claims.json discloses this as "INSTRUMENT_ABSENT by design" and a non-table probe. Label: observation (the round departs from its planned order; disclosed in claims.json, not in SCORECARD).

## Checked and holding (no mismatch)

- Coverage row: baseline 9.72 is recipe A at a79945c4, 70/72 with missing r14-01 and r14-02. "recount 107/107, missing [], dangling [] at 7ef837a" holds.
  "said 78/78 from luna-round-7": `git log -S'78/78 knowledge files mapped' -- SCORECARD.md` gives 6e2ee8fa (luna-round-7) and 0e333eb2 (round 25). Holds.
- Depth row: 9/9 at 638fb211; `SKILL.md:77-191` at a79945c4 (craft heading at 77, last non-blank line 191); 17/17 at 08c7a729. All hold.
  The row's `SKILL.md:81-318` is wrong (the span is 81-314 at both 08c7a729 and c27f445), but K2 already covers that.
- Calibration row: command B on `git show c27f445:evidence/round-1-2026-10-15/{rubric,result}.json` gives baseline 0/9 and after 9/9 at c265db9b, exit 0. That revision versus the cell's `75af886a` is K5.
  The cited paths `.ufo/waves/luna-round-2/receipts/` and `rubric.json` are present.
- All capability evidence pointers at :619-622 are present at c27f445. `config-pre-pair.txt` has 6 lines and 5 hashes, which matches ":621 6-line 5-hash".
- Round-25 table (:3052-3054): `tools/round-25/a2/c1-calibration.py` gives 5 mismatches at 9dcd11ec (exit 1) and 0 at 08c7a729 (exit 0). `c2-coverage.py` gives 107 and entry_sourced 0 at 9dcd11ec, then 108 and 1 at 08c7a729. Both hold.
  Recipe A gives 108/108 and 17/17 at both 08c7a729 and dc31f9c4, so :3057 and :3059 hold. "Only the depth row was refreshed" holds within its scope (the wave-1 found items).
- Saturation and retired fields: all owned rows are at 10. The last capability entry was round 17 (:2392, :2891); round 26 is the 9th round after it, inside window 10.
  "retired: none" holds at axis level. `:1217` retires a thread, not an axis.
- SHONEN.md:6: `SKILL.md:81-314` and 17/17 at 3e99fbd6 hold (recipe A 17/17; craft span 81-314). SHONEN.md:8: `corpus/lessons/2026-10-15-round-1.md` and `evidence/round-1-2026-10-15/rea-bundle.json` are present, and LOG.md:464 records the libjq executed smoke.
  SHONEN.md:12 is K6, not re-judged here.
- `corpus/evidence/round-26/` at c27f445 holds only `before/census-start.txt`. At a0639d8 it has 0 files, consistent with the claims.json `before.basis`.

## Unknown

- Whether the Open-gaps and round-1 sections (findings 2-6) are meant as living state or a frozen record. The card mixes both: some bullets carry later "closed by" notes and others do not.

## Artifacts (/fast/scratch/hyaku/kaidoku-r26/seats/C2Cherrypick/)

- recipeA.py 236dde1da2d78b5ee2f4827fb884901857385fe1f40bbb09bbb4b4ab4f6e9b01 (recipe A body, SCORECARD.md:93-123 at c27f445)
- recipeA-runs.txt ef33dac219db5b621884d2bf8f6d07d1ca9f38a9002122c72880758678be46a5 (raw recipe A output at 7 revisions)
- SCORECARD.c27f445.md cfe8b5257c90b14b3f7cbe1349d6117a78494632096ab1fa2594e189038d977a
- SHONEN.c27f445.md 120cd2b3bb5f9e0c2bcc943bf8cf74c6c35cf887e85fe2caa660901d36ff2ddb
- rubric.json b34b7fdb2beb1b228d382ad9a3dc9861b87b6ad1de44406f00a89b1c21e746ae; result.json 0a03434f69a07197a426837f13cd0cca1793c66856a64c73b367695ae45e1342
- tools/r25-c1-calibration.py 4378af84fa8e036f62e85e81a07d21d0ed899a34b56f790a4682f0c965356eee; tools/r25-c2-coverage.py 7a7e6d6529033c5dfac6da252507ac597b30f0a3d4740522d17f87f4ee6b2c70

Tool installs: none. Sources opened: local lane Git objects and fleet AXES.md only, no web sources.
