# C1Cherrypick — is the R25-C1 five-item calibration cherry-picked?

Seat: KaidokuR25a3.C1Cherrypick (critic, leaf). Revision under review: lane tip `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76`.
Scope: SCORECARD.md owned-axes rows (lines 19-31) and SHONEN.md. Read-only; no lane file edited except this report.

## Verdict

**Fails as an exhaustive calibration; holds as a disclosed finite five-item proxy.** At the tip, the R25-C1 instrument
reports `"items": 5, "mismatches": 0` (exit 0, 2026-10-22T10:45:05Z). The same two files still contain five more
self-assessment statements that disagree with observed repo state (E1-E5 below). The two strongest are E1 and E2:
the depth row still says 9/9 rule blocks while command A says 17/17. That gap has existed since 2026-10-18, through eight
commits. The frozen claim does not change. The L1 SHOULD disclose E1-E5 next to the 5 → 0 result, so "0 mismatches" is
not read as "the self-assessment is calibrated".

## Producing commands (all exit 0)

- Command A is extracted verbatim from `SCORECARD.md` recipe A at the tip into `<seat>/commandA.py`. It ran as
  `python3 -I -B <seat>/commandA.py <REV>` at 10:42:57Z-10:43:55Z.
- `python3 -I -B tools/round-25/a2/c1-calibration.py --root . --rev 08c7a72…` ran at 10:45:05Z.
- Command B is the SCORECARD jq recipe, run on `git show` copies of `rubric.json`/`result.json` at 10:44:50Z.
- `git show REV:FILE | grep -n '^## '` gave the section spans. `git log -S` and `git log -- SHONEN.md` gave the row history.

## Command A observations (observation)

| REV | mapped/files | rule_blocks (resolved) |
|---|---|---|
| a79945c4 (baseline) | 70/72 | 9 (9) |
| 638fb211 | 72/72 | 9 (9) |
| 3395b6d | 78/78 | 9 (9) |
| 3e99fbd6 | 92/92 | 17 (17) |
| 7ef837a4 / 9dcd11ec / 18e7eb6d | 107/107 | 17 (17) |
| 08c7a729 (tip) | 108/108 | 17 (17) |

Rule blocks grew 9 → 17 in eight commits: 58116aa1 (10, 2026-10-18), 265e1aa5 (11), 8cc81a84 (12), ba06c4dd (13),
28aa7a98 (14), 2fba56fe (15), 9c1d1fef (16) and 4072ebb3 (17, 2026-10-19).

## Extra mismatches not counted by R25-C1

**E1 — SCORECARD:24, depth row count is stale (observation, fails).** Excerpt: "9/9 queue-drain rule blocks have
resolvable file/range citations at `638fb211`". At the tip, command A gives `'citation_resolved_rules': 17, 'rule_blocks': 17`.
The same card disagrees with itself: SCORECARD:2094 says "rule blocks 16 → 17, citations 17/17", and :2927 says "citations17/17".
SHONEN:6 also says "17/17 rule blocks". The row text was last changed by 0772d548 (luna-round-3, 2026-10-16), found with
`git log -S`. Impacted axis: depth (the score 10 still holds; the stated observable does not).

**E2 — SCORECARD:24, depth row SKILL.md range is wrong at every named revision (observation, fails).** The row cites
`SKILL.md:77-191`. The `## Queue-drain craft` heading sits at line 77 at a79945c4, line 81 at 638fb211, and line 81 at the tip.
- At the baseline (a79945c4), the section is 77-192 (next heading `## Checklists` at 193; last content line 191).
- At the measured revision (638fb211), the section is 81-196 (next heading at 197).
- At the tip, the section is 81-318 (next heading `## Config custody` at 319; last content line 314).

So the range matches only the baseline, never the measured revision. At the tip, lines 77-79 are `## Error patterns`
table rows, and the range stops about 123 lines before the section ends.

**E3 — SCORECARD:24/23/25, stale measured revisions (observation, fails as the current measurement).**
- Depth is "measured `638fb211`". That revision gives 9/9; the tip gives 17/17.
- Coverage is "measured `3395b6d`". That revision gives 78/78, while the row's headline is 108/108. The 108/108 has no
  revision attached. Command A at the tip does reproduce 108/108, missing [], dangling [], so the number holds and only the
  revision attribution is stale.
- Calibration is "measured at `75af886a`". Command B outputs
  `{"stage":"after","revision":"c265db9bd3c0883fbaf4487f839559c85a736826","aligned":9,"total":9,"score":10}`, so the
  9/9 count is bound to c265db9b, not 75af886a. [INFERENCE] 75af886a is the luna-round-2 receipt reconciliation, which
  command B does not measure.

**E4 — SCORECARD:23-25, "Last-change round" column omits later moves on the same axis (inference, likely fails).**
- Depth lists "r1 measurement + luna-round-3". The eight later depth-claim commits listed above changed this row's own
  observable (9 → 17); for example, SCORECARD:2094 records the arc3-loop1-round12 depth claim.
- Calibration lists "operator-steered r1 + luna-round-2". SCORECARD headings record later calibration claims:
  - arc2-loop1-round2, round5, round8 and round10 (:704, :936, :1160, :1270);
  - arc3-loop1-round5, round7, round9 and round11 (:1636, :1759, :1872, :1977);
  - Round 24 R24-C2 (:2902), and R25-C1 itself (:3050).
- The calibration row does not mention the round-24 outside "target unmet" verdict on R24-C2 (spot-check :19). That verdict
  is recorded only at :3048.
- Coverage lists luna-round-1 and luna-round-7, so the column does list rounds that changed the observable without changing
  the score. Under that convention, depth and calibration are stale. This is inference because the column has no written definition.

**E5 — SHONEN:12, the "contested" province-version clause is stale (observation for the text, inference for full alignment).**
Excerpt: "province-version alignment is contested by the 6.5.0/207/v42 observations in `corpus/lessons/2026-10-15-round-1.md`".
- PROVINCE at the tip already states current pins `rea-agents@6.7.0` with 207/153 (PROVINCE:9, :16-18) and "Installed shared
  REA skill is v42/207 tools" (:24). It marks 6.4.0/170/127/v37 as historical (:12, :24).
- SCORECARD:56-60 says "Version drift: closed by luna-round-2 … Superseded 2026-10-18".
- The live configs, read at 10:45:05Z, all pin 6.7.0: `~/.omp/agent/mcp.json:9`, `~/.config/devin/mcp_config.json:7`
  and `~/.kimi-code/config.toml:4126`.
- 0e333eb2 rewrote this exact SHONEN line, changing only the range, and kept the stale clause (`git diff 0e333eb2^ 0e333eb2 -- SHONEN.md`).

## Statements checked that hold (observation)

- SHONEN:6 says `SKILL.md:81-314`, 17/17, at 3e99fbd6. The craft section 81-318 is byte-identical between 3e99fbd6 and the tip
  (`diff` printed IDENTICAL). Line 314 is the last non-blank line and lines 315-318 are blank.
- SHONEN:8 cites `evidence/round-1-2026-10-15/rea-bundle.json`, which exists in `ls-tree` at the tip. The lesson has
  "### Executed native smoke" at :87, and LOG:465 and :526 log the `0x117070` ENDBR64 decode.
- SCORECARD:27-30: command A at 6645585 gives 70/72 (9.72) and 9/9, and result.json `measured_revision` is c265db9b. Both hold.
- SCORECARD:23 "recount 107/107 … at 7ef837a4" holds (command A gives 107/107, missing [], dangling []).

## Instrument weakness relevant to "cherry-picked" (observation)

The I5 test accepts any SHONEN range inside PROVINCE's first `## Adjacent` section. Command A-style heading scan: that section
runs from 95 to 266 because the next `## ` heading is at 267. Lines 119-266 hold `### Round-4 additions to Core`,
`### Round-20 additions to Core`, `### Round-22 catalog dispositions` and other Core and Frontier tables. A pointer such as
`PROVINCE.md:119-131`, which covers Core tables rather than refusals, would pass I5. The current 95-116 is correct, and the
refusal list ends at 116. Impacted axis: calibration (a false-pass path in the instrument, which does not falsify the current value).

## Adjacent, outside the assigned lines (observation, not counted)

- SCORECARD:49 (C9) says "until a genuine outside verifier is identified". The lane now has non-author spot-checks
  (`corpus/lessons/round-24-verifier-spotcheck.md`; round-19 spot-check cited at SCORECARD:2575). These are round-admission
  verifiers, not promotion verifiers, so this is not counted.
- PROVINCE:17 cites OMP `mcp.json:8`. The live pin is at `:9`.

## Smallest safe correction (for L1 disclosure; no frozen claim changes)

1. Disclose E1-E5 next to the R25-C1 5 → 0 result. The result is "5 preselected items aligned", not "self-assessment calibrated".
2. In a future round, refresh the depth row:
   - change the count to 17/17;
   - change the range to `SKILL.md:81-314` at the tip;
   - change the measured revision to a current one;
   - add the 8 depth commits to the Last-change column.
3. Separately:
   - attach a revision to coverage 108/108;
   - change calibration "measured at 75af886a" to c265db9b, or split it into "count at c265db9b; receipts at 75af886a";
   - drop or re-date the SHONEN "contested" clause;
   - bound I5 at the refusal list rather than at the next `## ` heading.

## Artifacts (`<seat>` = /fast/scratch/hyaku/kaidoku-r25-a3/seats/C1Cherrypick)

- `<seat>/commandA.py` sha256 236dde1da2d78b5ee2f4827fb884901857385fe1f40bbb09bbb4b4ab4f6e9b01
- `<seat>/commandA-runs.jsonl` sha256 6c4b1ecba7cc9581a4840f144f9539c2937c30e575bd455d68b526b630d3e36e
- `<seat>/c1-at-tip.json` sha256 d6be83a566570f0abd6ad8b0dbc38bc83cea7bbd6e2c095e697426229ba91591
- `<seat>/cmdB/evidence/round-1-2026-10-15/result.json` sha256 0a03434f69a07197a426837f13cd0cca1793c66856a64c73b367695ae45e1342
- `<seat>/cmdB/evidence/round-1-2026-10-15/rubric.json` sha256 b34b7fdb2beb1b228d382ad9a3dc9861b87b6ad1de44406f00a89b1c21e746ae

Tools installed or updated: none. Web sources opened: none. REA: not invoked.
