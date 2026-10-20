# Round 14 — score-contract review (C1 coverage, C2 calibration)

Seat: `KaidokuR14.ReviewScoreContract` (leaf reviewer, author-side; cannot provide non-author admission).
Access date: 2026-10-20. Repo HEAD read: `767adaf` (`git status`: only `?? .ufo/waves/round-14/`; no C1 entry, no gate, no map row exist yet).
Scope: SCORECARD.md:2090-2175 numeric treatment, C1 coverage, C2 calibration, lowest-axis obligation. No edits, no tests, no builds, no REA/target execution. Only write: this file.

## Verdict in one paragraph

The round's numeric treatment is mostly honest in intent but not yet in the claim set. All three owned proxies sit at 10.0 and are structurally incapable of rising, so neither C1 nor C2 can produce a numeric axis improvement. The claims' `before 0 → after 1` values are artifact counts, not axis scores, and must not be reported as coverage or calibration movement. Two substantive problems need L1 attention before the round can say anything about trends: (1) the planned condition for C1 ("only if a matching uncovered coverage-map question remains") has no recorded check and the coverage map already holds closely related ground; (2) the round-13 lesson states that the existing quote rule "caught both defects", which the reviewer evidence contradicts, so C2's premise must be recorded as a correction rather than silently assumed.

## Findings by severity

### F1 — High — Numeric axes cannot move; C1/C2 before→after values are not score deltas

- Owned proxies, as recorded: coverage 10.0 (index mapping completeness, "not fraction of the REA domain held"), depth 10.0 (queue-drain citation resolution), calibration 10 (9/9 frozen reconciliation obligations). `SCORECARD.md:23-25`; saturation line `SCORECARD.md:626-631`; round-12 "all owned proxies sit at 10.0" `SCORECARD.md:2096,2102-2103`.
- Coverage proxy arithmetic (recipe A, `SCORECARD.md:92-123`): score = mapped knowledge files / knowledge files. A new entry that is mapped leaves it at 10.0. An unmapped new entry gives `round(10*91/92,2) = 9.89` — a regression, i.e. harm under AXES "no axis is harmed".
- Depth proxy: `round(10*17/18,2) = 9.44` if one added SKILL rule carries an unresolved citation range.
- Calibration proxy: `rubric.json:6` `round(10 * aligned / 9, 2)`; `rubric.json:3` scopes it to "not unbiased accuracy, mastery, saturation, or promotion". The rubric is frozen; C2's gate adds no obligation to it, so the proxy cannot change.
- claims.json `:8-9`, `:22-23` express C1/C2 as `before 0 / after 1` on finite observables. Those are counts of new artifacts. claims.json `:28` ("no increase beyond saturation") is consistent with the numeric treatment; the risk is that the round entry rewrites `0→1` as a coverage/calibration score.
- Required wording for the round entry: "coverage 10.0 → 10.0 (N/N mapped); depth 10.0 → 10.0; calibration 10 → 10 (rubric frozen; gate observables are counts, not a calibration score)." C1 and C2 observables go in the capability/trend column, not the axis column.

### F2 — High — C1's uncovered-ground condition is asserted, not checked

- The plan says: "admit one source-backed knowledge entry only if a matching uncovered coverage-map question remains." `SCORECARD.md:2157-2160`. No check result is recorded in SCORECARD or the claims file. claims.json C1 is unconditional.
- Held ground the map already has:
  - `corpus/README.md:35` (Coverage map row) and `:140` cite `2026-10-13-r4-10-real-version-pair`, covering the Go 1.25→1.26 bump collapsing Ghidra symbol recovery (33,060 → 11,595 procs; pair by ELF role/address).
  - That entry states Ghidra 12.1.4's Go analyzer cannot parse the Go 1.26 layout, but the cause is "observed-not-cited" from a transient log: `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:69-73`. The new C1 entry would supply exactly the citation r4-10 lacks.
  - Go metadata entries `2026-10-16-l7-01-inspect-go-binary` and `2026-10-19-arc3-r12-go-evidence-id-domain` are on a different verb (metadata/IDs), not the recovery gate.
- Not held: the Frontier list (`corpus/README.md:170-181`) has no Go row; "Known gaps" (`:183-190`) has none. The source study path exists: `corpus/SOURCES.md:33` ("Go ≥1.26 recovery and cross-version matching").
- Measured now (read-only, my own count): 91 knowledge files, 91 mapped tokens, 0 missing, 0 unmapped tokens at `767adaf`; 17 SKILL craft rule blocks. These reproduce the SCORECARD's `command A` at `6a35398` (91/91). I did not re-run the rule-resolvability half.
- Consequence: C1 is at least as much a quality move (it supplies the missing citation for an existing r4-10 claim) as an expansion move. Whether it counts as expansion ("net new admitted entries on ground the coverage map did not hold", `LEARNING.md:33`) is a judgment L1 must record with the map rows above. Counting it as both expansion and quality would double count one artifact.
- Required: an explicit map-check line in the round entry naming the r4-10 row and deciding expansion vs quality; if expansion, the entry needs its `corpus/README.md` map token in the same commit (F1 arithmetic) and `source:`/`verified-at:`/`recheck:` fields (`LEARNING.md:69-70`).

### F3 — High — The round-13 record says the quote rule caught the defects; the evidence says the reviewer did

- `corpus/lessons/round-13.md:76`: "The existing CORPUS/SOURCES quote rule caught both defects; no extra QUALITY criterion was added."
- Contradicted by `corpus/lessons/round-13-verifier-spotcheck.md:13` (the review, not the lesson's own gate, found the defects) and by the reviewer report `.ufo/waves/kaika-w3/kaidoku-r13-review.md` §4 (DEFECT-1 S017, DEFECT-2 S018 — both found by re-opening the source, not by the lesson's own gate).
- Under `LEARNING.md:35`, a disagreement "left unlearned, or a criterion is added with no lesson behind it" counts as **harm** to discernment; the round-13 wording leaves the disagreement unlearned at the criterion level. C2 is the correct corrective path, but its premise must be recorded.
- Also, C2's "grounded QUALITY criterion" directly reverses `round-13.md:76` ("no extra QUALITY criterion was added"). Both statements cannot stand unqualified. Required: an append-only correction to round-13 (or a round-14 lesson entry that cites round-13 Mistakes #3/#4, `round-13.md:73-74`) stating that the write-time rule did not catch the defects. Do not rewrite the round-13 table.

### F4 — Medium — C2 calibration observables are small-n and not yet in the gate's input contract

- Only two real defects exist (S017, S018). Both were found by the same reviewer, so this is a selected sample. Exact Clopper–Pearson 95% interval for 2/2 detected: **[0.158, 1.000]** (computed here). A "catch rate" claim is not supportable.
- The captured inputs do not match the gate contract. The gate contract (SCORECARD/round-14 spec: "Source UTF-8 Markdown excerpt") is violated by both current captures:
  - `.ufo/waves/round-14/w1/ReviewS017-source/View8-README-ef39099b4f5076042173f9113382ebeb0630a56d.md` is HTML-rendered: `<h1>View8</h1>` (line 1), `<h2>Usage</h2>` (18), `<h3>Command-Line Arguments</h3>` (20), `<h3>Deterministic Function Names and Mapping CSV</h3>` (81).
  - `.ufo/waves/round-14/w1/s018-raw.html` is a full raw page (`<h1 class="wp-block-heading">Introduction</h1>` at 469).
  - Consequence: a manifest built on these would most likely return exit 2 (`invalid_manifest` or no section found), not the intended exit 1. That is a could-not-evaluate outcome that looks like detection if the pinned verdict is not exact. Expected verdicts must pin exit 1 plus the specific finding ID, and the fixtures must be Markdown excerpts. Fixture ownership belongs to the fixture producer; I have not touched them.
- Replay expectations (these are arithmetic over the captured text, not gate runs):
  - S017 splice quote "Use --normalize to replace address-derived function names with deterministic names based on parse order." appears verbatim nowhere: the two nearest sentences are at lines 40 and 82 (`Use <code>--normalize</code> to replace address-derived function names with deterministic identifiers.`). Expect `quote_not_contiguous` (exit 1).
  - S017 corrected quote "Replace address-derived function identifiers with deterministic names based on parse order." is at line 40, inside `Command-Line Arguments` (line 20), which ends before `Basic Usage` (line 66). Expect exit 0 with section `Command-Line Arguments` under `Usage`.
  - S018 original quote is at line 489, under `Introduction` (469) and before `Distributed payloads` (497). Original location `Decompiled output` is at line 625. Expect `quote_location_mismatch` (exit 1) for the old label and exit 0 for `Introduction`. Note the quote is a single HTML paragraph; a Markdown excerpt must reproduce it exactly.
- Gate-vs-reviewer agreement across the 22 registry rows is the only non-trivial calibration count available: the reviewer reports 20/22 verbatim-exact (`kaidoku-r13-review.md:94`). Only 2 of 22 captures exist in `w1`, so agreement is **2/22 measurable now**. Once all 22 are captured as Markdown excerpts: 20/22 reviewer-verbatim has exact 95% interval **[0.708, 0.989]** (computed). The reviewer's manual reopen is not ground truth for live web sources, and the gate covers only captured local excerpts (claims.json `limits`).

### F5 — Medium — Lowest-axis obligation: all owned axes tie; the trend furthest behind is expansion/quality, not discernment

- All owned axes sit at 10.0. `AXES.md:33-34` requires one claim on "the lane's lowest-scoring non-retired axis" unless the stagnation nudge waives it (`AXES.md:66-73`). With a tie, the obligation is satisfied by any owned axis; the nudge applies per `SCORECARD.md:2100-2105`, and it calls for a frontier/capability move. A knowledge entry is not automatically a frontier or capability move; C1 qualifies only if its ground is frontier (see F2).
- Learning trends (`LEARNING.md:26-35,88-90`): round 12 expansion unchanged; round 13 expansion unchanged after correction (`SCORECARD.md:2162-2170`), quality unchanged, discernment improved. The furthest-behind trends are expansion and quality. C1 (expansion/quality) aligns with the trend rule. C2 (calibration = discernment) does not, and is justified only by the falsifiability tie-break precedent (`SCORECARD.md:276-277`). That justification must be written, not implied.

### F6 — Medium — The round-13 "discernment improved" verdict depends on a reviewer whose non-author status is classified inconsistently

- `corpus/lessons/round-13-verifier-spotcheck.md:4`: "Both were parent-dispatched, not lane L2 seats." The same lesson's `round-13.md:55` says "dispatched L2 reviewers do not count as that outside check."
- `.ufo/waves/kaika-w3/kaidoku-r13-review.md:145` says the review "is independent of the lane." `LEARNING.md:45-46`: "A subagent the lane dispatched is still the lane." A parent-dispatched reviewer is not lane-dispatched, so it can qualify, but the artifacts disagree on the classification and this round's own spec states "dispatched seats are author-side". The round-13 discernment improvement therefore rests on a classification the record does not settle. It needs an operator or integrator ruling, recorded in the round entry.
- Sample size of the r13 spot-check: 3 decisions (2 admits S003/S008 + 1 rejection S022) plus a 22-row quote audit. Honest but small.
- For round 14: no non-author reviewer exists for the C2 gate decisions yet. Wave reviewers (`ReviewQuoteContract`, `ReviewS017`, `ReviewS018`, etc.) are dispatched and cannot count. C2's discernment trend therefore cannot be "improved" in this round without a named non-author spot-check (`LEARNING.md:42-46`). Its gate-count observables can be reported; the trend verdict cannot.

### F7 — Low — Pre-correction text in the round-13 body still reads as current

- `SCORECARD.md:2146-2155` still says calibration "No outside admit/reject spot-check yet" and "expansion improved". The append at `:2162-2175` supersedes it. The round-14 entry must not repeat the superseded wording. Calibration numeric is unchanged at 10 (`:2172-2174`).

## Measured now vs. after L1 integration

| Quantity | Measured by me at `767adaf` (read-only) | Expected after C1/C2 (not run) | Note |
|---|---|---|---|
| knowledge files / mapped / missing | 91 / 91 / 0 | 92 / 92 / 0 (C1 with map token) | 91/92 unmapped gives 9.89 |
| coverage proxy | 10.0 (derived from the above) | 10.0 | cannot rise |
| SKILL craft rule blocks | 17 (resolvability not re-run) | 17 or 18 with 100% resolvable | one unresolved gives 9.44 |
| depth proxy | 10.0 (SCORECARD `:24`, not re-measured) | 10.0 | |
| calibration proxy | 10 (`rubric.json` frozen, 9/9 per SCORECARD `:25`; result.json not re-read) | 10 | rubric must not be edited |
| gate present | no (`.ufo/waves/round-14/tools/` absent) | selftest exit codes + finding IDs, counts only | not a calibration score |
| S017/S018 replays | not run; captures are HTML | expect exit 1 (old), exit 0 (corrected) | needs Markdown fixtures first |
| gate vs reviewer on 22 rows | 2/22 captures present | agreement count with exact CI | 2/2 CI [0.158,1.000]; 20/22 CI [0.708,0.989] |
| trend verdicts | nonnumeric | expansion/quality per F2; discernment unprovable without non-author check | never numeric |

## Recommended numeric treatment (for L1 to adopt or reject)

1. Report owned axes as "10.0 → 10.0" with the counting command and measured revision. No 0→1 entries on owned axes.
2. Report C1's artifact as a count (entries +1, map tokens +1, mined source rows cited) and as a trend verdict after the F2 map check.
3. Report C2's observables as gate self-consistency counts with pinned exit codes and IDs. Do not report a "catch rate" from n=2. Report gate-vs-reviewer agreement only with its n and interval.
4. Record the lowest-axis handling explicitly: all owned axes tied at 10.0; nudge applies or does not, with reasons (F5).
5. Record the r13 classification question (F6) for an operator ruling before relying on the discernment verdict.

## Residual risk and verification gaps

- I did not run the gate, the calibration command B, or the rule-resolvability half of command A. Numbers above are either read-only recipe-A counts I computed, arithmetic, or reproduced from cited files.
- The F2 reading (held vs uncovered) is a judgment over three knowledge entries and a README map; another reader could weigh r4-10 differently. I have recorded the evidence rather than deciding it.
- The S017/S018 expectations are reasoned from captured text; no gate has evaluated them. The fixture contract mismatch (F4) is observed in the current captures only.
- I did not verify the reviewer's claim that the round-13 main-checkout `LOG.md` is dirty (`kaidoku-r13-review.md` §8.3); out of scope for this seat.
- Confidence: high for F1, F3, F4 (counts and quotes checked), medium for F2 and F5 (judgment), medium for F6 (classification ambiguity).

## Sources opened (access 2026-10-20; quotes ≤25 words)

- `SCORECARD.md:2090-2175` (round-13 and round-14 sections); `:23-25`, `:86-123` (recipe A), `:276-277`, `:626-631`. Quote: "All owned proxies sit at 10.0 and no capability row has entered" (`:2102-2103`).
- `SCORECARD.md:2157-2160` (round-14 plan): "admit one source-backed knowledge entry only if a matching uncovered coverage-map question remains".
- `.ufo/waves/round-14/claims.json:8-9,22-28`.
- `.ufo/waves/round-14/spec.json` context (C2 gate interface and "Dispatched seats are author-side").
- `evidence/round-1-2026-10-15/rubric.json:3,6`: "not unbiased accuracy, mastery, saturation, or promotion".
- `evidence/round-1-2026-10-15/baseline.json:13,18-19`.
- `corpus/README.md:11-35,140,170-190`; `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:69-73`: "Ghidra 12.1.4's Go analyzer cannot parse the Go 1.26 moduledata/pclntab layout".
- `corpus/SOURCES.md:9-12,23-24,33`: S003–S006 status `mined`; `Go ≥1.26 recovery and cross-version matching`.
- `corpus/lessons/round-13.md:76` (quoted in F3; the claim under review), `:55,67,73-74` (non-author and Mistakes context).
- `corpus/lessons/round-13-verifier-spotcheck.md:4,13`: "Both were parent-dispatched, not lane L2 seats."
- `.ufo/waves/kaika-w3/kaidoku-r13-review.md:94,145` (quote: "this review is independent of the lane"); `kaidoku-r13-critic.md:7` (expansion mislabel).
- `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:33-34,66-73` (quote: "At least one claim works the lane's lowest-scoring non-retired axis").
- `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md:26-35,42-46,88-90` (quote: "A subagent the lane dispatched is still the lane.").
- `.ufo/waves/round-14/w1/ReviewS017-source/View8-README-ef39099b4f5076042173f9113382ebeb0630a56d.md:1,18,20,40,66,81-82` (quote line 40: "Replace address-derived function identifiers with deterministic names based on parse order.").
- `.ufo/waves/round-14/w1/s018-raw.html:469,489,497,625` (quote line 489: "The goal is not perfect source recovery — V8 compilation is lossy, and the output of decompilation remains pseudocode.").

## Tools

No installs or upgrades by this seat. Computation used the Python standard library (exact binomial intervals, recipe-A counts via `git` object reads at `767adaf`). Nothing was built, tested, or linted.

## Writes

Only this file: `.ufo/waves/round-14/w1/ReviewScoreContract.md`.
