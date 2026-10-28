# W2C2Scorecard — round 49 wave 2 (post-landing) — SCORECARD attack

Lane `kaidoku-shokunin`, landing `29883d4ec35a31a8393c4ffb220888c44c0bb022`, freeze `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d`. All reads are git objects at the landing revision (`git show`, `ls-tree`, `merge-base`); the lane worktree was not used as evidence. Scratch under `/fast/scratch/hyaku/kaidoku-r49/W2C2Scorecard/` (removed at yield). Artifacts: `.ufo/waves/round-49/w2/W2C2Scorecard/`. No tools installed; no git mutation.

## Verdict

**The A9 line is exact and the C2 counter is green at the landing revision; the SCORECARD's round-48 record is only partly reconciled.** A9 equals the contract line byte-for-byte and the counter rejects every non-exact variant I tried, but A9 is forgeable by an HTML comment or code fence (the counter scores both green). Round-48 statements the closure contradicts are corrected only for calibration (by A9, beside not in place). Quality, discernment, the "75/75 seats settled" claim and the calibration numeric row are not corrected. The owned-axes calibration row still reads 10 with no reference to the round-48 `rejected-harmed` verdict, and the SCORECARD has no round-49 before→after record for either claim; the coverage row is one knowledge file stale (138 vs 139 at landing).

## Findings

| # | Severity | Attack target (file:line at landing) | Finding | Command / receipt | Exit | stdout sha256 / value |
|---|---|---|---|---|---|---|
| F1 | info (verified) | `SCORECARD.md:3753` (A9) | A9 line equals the contract text; `c2-mismatch.py` A9 check (`a9`, exactly one `- A9 ` line in `## Record corrections — round 49`, equal to the contract string) is green at landing. | `GIT_NO_REPLACE_OBJECTS=1 python3 -I -B tools/round-49/c2-mismatch.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 29883d4ec35a31a8393c4ffb220888c44c0bb022 --freeze decc5697bfd4ec1e9de4a762ad199d9bd9c4230d --battery --json-out …/c2-at-landing-battery.json` (2026-10-28T22:40:50Z) | 0 | `0cad6d5cfb525227be6af09d6cd6b6115818cee4436180a902a8d1847f490f86`; `mismatches 0`, `atoms_total 9`, `battery.failing []` |
| F2 | info (verified) | battery, `c2-mismatch.py` `mutations()` | 16 mutations each red on exactly its own atom and none a no-op; do-nothing overlay (102 changed paths restored) red on all nine. A9 has one mutation (a second contradictory line). | same command, `battery.mutations`, `battery.do_nothing_red` | 0 | as F1 |
| F3 | info (verified) | counter bytes | Worktree `tools/round-49/c2-mismatch.py` = FREEZE blob = landing blob. | `git show <rev>:tools/round-49/c2-mismatch.py \| sha256sum` at decc5697 and 29883d4e; `counter_sha256_at_freeze` in receipt | — | `9b80b3b0e3945563426510e72969a7b5fed3e66a47b567d3a8341fc1f5d8595d` (all three) |
| F4 | info (verified) | freeze | At freeze, nine atoms fail, exit 1. | `… --rev decc5697… --freeze decc5697… --json-out …/c2-at-freeze.json` | 1 | `7aa900e1f004d3f13117264e85b68a51b9116dab2590da7a00a66c584b2e37f4`; `mismatches 9`, `atoms_fail [A1..A9]` |
| F5 | **medium** | A9 predicate, `c2-mismatch.py` `a9()` line ~548 | **Forgeable: the A9 line counts when it is invisible.** A9 inside `<!-- … -->` and A9 inside a fenced code block (replacing the only visible A9 line) both score A9 green with no A9 red. The rendered SCORECARD then shows no verdict line at all while the counter reports the correction present. The battery has no mutation for this. | `python3 -I -B a9attack.py` (overlay of the landing SCORECARD, `Overlay`/`score`), artifact `a9-forgery-battery.json` | 0 (script) | `bbd4d6ce4e92af9539dd7d76d41fc43af46683f304b5a30c4b736c93643dfc3f`; cases `A9_in_html_comment` and `A9_in_code_fence`: `red []` |
| F6 | info (verified) | A9 strictness | Non-exact variants are red: line deleted; `calibration=improved`; `verdict=admitted`; trailing text; A9 moved into the round-48 section; a duplicate `## Record corrections — round 49 (draft)` heading; NBSP after the dash. | `a9attack.py` (same receipt) | 0 (script) | cases red `[A9]` with the expected message |
| F7 | **medium** | round-48 entry `SCORECARD.md:3739` (Owned scores) | States `calibration 10 → 10 (the round's record clauses now re-derive; numeric axis remains capped)`. The closure (`corpus/lessons/round-48-verifier-spotcheck.md:7,107`) records calibration **harmed** and the admission `rejected-harmed`. The contradiction is corrected only by A9 (`SCORECARD.md:3753–3755`), beside the entry, not in place. A9 checks one line; it does not check any other statement. | `git show 29883d4e:SCORECARD.md \| sed -n 3739p`; closure sha256 `a46da21f264b5c6fd23f2fe6c0ab6cadc7dad2788d5093dfc7a776131aac13e8` (identical at base `e4f2cfa5` and the lesson file) | — | prose check, not a counter |
| F8 | **medium** | round-48 `SCORECARD.md:3730, 3732` ("settled 75/75 seats"; "all 75 seats settled") | The closure's defect 7 (`closure:136`) says 72/75 seats have report artifacts, C1Meaning was blocked by `frozen_worktree_dirty`, and the report must not assert "0 dead seats" without durable settlement evidence. The registry `r48-w1-results.json` records C1Meaning as `"status": "blocked"` (files_changed `[]`) and ScribeReportNumbers as `"aborted": true`. No correction line. | `git show e4f2cfa5:.ufo/waves/round-48/r48-w1-results.json \| jq` → `results` 75; `select(output matches "status": "blocked" or "aborted": true)` → `C1Meaning`, `ScribeReportNumbers` | 0 | registry sha256 `8eec161e5e250d6747d1127b104b10dfab7469492cc62813b3651e376fd2b2c7` |
| F9 | **medium** | round-48 `SCORECARD.md:3740` (Learning trends) | `quality **improved on the instruments**` — the closure's per-axis verdict is `quality — harmed` (closure:125; S145 locator and S146 rationale are source-record errors). The round-49 prose (`:3755`) says "quality was also harmed", but the machine line A9 covers only calibration and the round-48 trend line is not corrected in place. | closure lines 107, 125 | — | prose check |
| F10 | low | round-48 `SCORECARD.md:3740` | `discernment **improved** (A1–A8 self-found instrument defects, each disclosed …)`. The closure grades discernment improved **at decision level only**; S145 locator and S146 rationale are wrong (closure:113–118). The "each disclosed" claim also sits beside a lesson header (`corpus/lessons/round-48.md:4`) that still names freeze `0f06251b` (A4) while the final declared freeze is `b6f7ca2a` (A8). No correction. | closure lines 113–118, 118; `git show 29883d4e:corpus/lessons/round-48.md \| sed -n 4p` | — | prose check |
| F11 | low | round-48 `SCORECARD.md:3736–3737` (R48-C1, R48-C2 "measured at 2e785632") | Not contradicted, but incomplete: the closure's final receipts are `c1-final-33f65a91.json` / `c2-final-33f65a91.json` at tip `8847042a`. The SCORECARD names neither `33f65a91` nor `8847042a` (`grep -n 33f65a91\|8847042a` → no lines). | `git show 29883d4e:SCORECARD.md \| grep -c '33f65a91\|8847042a'` → 0 | 1 (grep no match) | — |
| F12 | low | round-48 planned line `SCORECARD.md:3743` | `planned (round 49): … pin the gate.py helper …` is still written as planned; round 49 did not do it (`plans/round-49-claims.md` "Routed, not repaired"; A9 prose `:3755` says so). The line is not marked not-executed. | plan text; `SCORECARD.md:3755` | — | prose check |
| F13 | **medium** (owned axes, calibration) | owned-axes calibration row `SCORECARD.md:25` | The row reads `0 → 10`, numeric 10, measured by the **round-47** counter (42 atoms, "mismatches []") and points "later calibration claims" at the round sections. It carries no reference to the round-48 `rejected-harmed`/`calibration=harmed` verdict and no reference to the round-49 measure (9 mismatches at freeze, 0 at landing). The round-49 counter's nine atoms sit outside the round-47 atom set, so the round-47 "0 mismatches" did not cover round-48's record defects. The numeric 10 is therefore not a statement that calibration held through round 48. | `sed -n 25p SCORECARD.md`; F1, F4 | — | — |
| F14 | **medium** (owned axes, coverage) | owned-axes coverage row `SCORECARD.md:23` and the round-49 record | `138/138 knowledge files mapped at the round-47 landing`. At the landing, `git ls-tree -r --name-only 29883d4e corpus/knowledge \| grep -c '\.md$'` → **139** (base `e4f2cfa5` → 138). The new entry is mapped (`corpus/README.md:105`). AXES requires each claim's before→after in SCORECARD.md. Neither R49-C1 nor R49-C2 has a SCORECARD before→after row; the only round-49 SCORECARD text is the A9 line and its prose (`:3751–3755`), which says "it claims no new score". | `git ls-tree` count 139 (landing), 138 (base); `git show 29883d4e:SCORECARD.md \| grep -n 'round 49\|R49'` → only `:3751`–`:3755` | 0 | — |

## Round-48 statements the closure contradicts, with no correction (routed, not repaired)

| file:line (landing) | statement | closure contradiction | corrected? |
|---|---|---|---|
| `SCORECARD.md:3730` | "settled 75/75 seats" | defect 7: 72/75 reports; C1Meaning blocked; ScribeReportNumbers aborted | no |
| `SCORECARD.md:3732` | "all 75 seats settled" | same | no |
| `SCORECARD.md:3739` | "calibration 10 → 10 (…)" | calibration harmed; rejected-harmed | **by A9 at :3753–3755 (beside, not in place)** |
| `SCORECARD.md:3740` | "quality improved on the instruments" | quality harmed (closure:125) | prose only at :3755 |
| `SCORECARD.md:3740` | "discernment improved (… each disclosed)" | decision-level only (closure:118); lesson header freeze false (lesson:4) | no |
| `SCORECARD.md:3743` | "planned (round 49): pin gate.py …" | routed, not executed (plan) | no (not marked) |
| `SCORECARD.md:3736–3737` | "measured at 2e785632" | final receipts at 33f65a91, tip 8847042a | no (omission, not false) |

## Calibration-axis implications (owned-axes table vs closure)

- The owned-axes table reports calibration as `10` with the proxy's own limitation ("failure-selected completeness"). It says nothing about the round-48 closure verdict `rejected-harmed` (AXES.md: a round is admitted only if no axis is harmed; "report every verdict and let the operator rule"). Read as a table, calibration looks unharmed through round 48.
- The round-47 counter that produced the "0 mismatches" reading covers 42 atoms. Round-49's counter found nine record defects in round 48 at freeze (`mismatches 9`, exit 1, F4) and none at landing (F1). The round-48 defects were therefore outside the round-47 scope, not a harm of the round-47 counter's own score.
- I do not change the numeric score (AXES: the operator rules). What the table lacks: a pointer to the round-48 `rejected-harmed` verdict, and the round-49 measurement with its scope (nine atoms, A1–A9), so a reader can see that calibration is currently re-derived for those nine atoms only.
- At landing the calibration record re-derives for nine atoms (F1, F2). That is the strongest calibration claim the SCORECARD can make from this round; A9 is a single line and does not establish the owned-axes row.

## Verification gaps

- Not run: the C1 counter (not in this seat's attack surface); the full `SCORECARD.md` diff against round-47 (only the round-48 section, the correction sections and owned-axes rows were read).
- Not checked: whether the round-48 seats saw A1 bytes only (`SCORECARD.md:3730`); the closure's routed defects 1–4 and 8 (LOG pointers, dead hash) are the counter's concern (A2, A3), not re-checked here.
- The a9attack script loads the counter from the scratch copy; the frozen byte-identical copy (sha `9b80b3b0…`) is kept as `c2-mismatch.frozen-copy.py` in the artifact directory.

## Receipts (all at 2026-10-28, UTC)

| artifact | sha256 | command / exit |
|---|---|---|
| `W2C2Scorecard/c2-at-landing-battery.stdout` | `0cad6d5c…f490f86` | battery at landing, exit 0 (22:40:50Z) |
| `W2C2Scorecard/c2-at-freeze.stdout` | `7aa900e1f004d3f13117264e85b68a51b9116dab2590da7a00a66c584b2e37f4` | at freeze, exit 1; run in the same shell call as the landing run, time not captured separately (after 22:40:50Z) |
| `W2C2Scorecard/a9-forgery-battery.json` | `bbd4d6ce…dfc3f` | `a9attack.py`, exit 0 |
| `W2C2Scorecard/c2-mismatch.frozen-copy.py` | `9b80b3b0…d8595d` | = freeze blob = landing blob |
| `W2C2Scorecard/r48-closure.base.md` | `a46da21f…aac13e8` | `git show e4f2cfa5:corpus/lessons/round-48-verifier-spotcheck.md` |
| `W2C2Scorecard/r48-w1-results.json` | `8eec161e…6fd2b2c7` | `git show e4f2cfa5:.ufo/waves/round-48/r48-w1-results.json` |
| landing `SCORECARD.md` | `6896859f8ce7a00a1e039dd6372b029d63f02c6f9fbae288b436a7e5f7f6bbd2` | `git show 29883d4ec35a31a8393c4ffb220888c44c0bb022:SCORECARD.md \| sha256sum` |
