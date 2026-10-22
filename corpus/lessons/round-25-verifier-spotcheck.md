# Round 25 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)

Date: 2026-10-22. Lane-round kaidoku r25. Base `18e7eb6d9fe8842678af5f1cffbd680ead4ad473`; lane tip
judged `cce7504ac1f4e1abe703edbdfc3a8c9f55bfc13a`. Report `.ufo/reports/round-25/kaidoku.md` (fleet
commit `d0c4492f3e60966dd197d65412b1c6c0a4fa497f`). Runtime model exposed to this closure:
`anthropic/claude-opus-5-5` (session workstation context). This closure did not author any part of
the round. It dispatched no review seats; every check below was run by the closure itself.
Only committed bytes were judged; the private attempt-1 trees under `/fast/scratch/hyaku/` were not
read.

## Decision

**Admitted.** R25-C1 (calibration) and R25-C2 (coverage) both reach their frozen after-values on
committed bytes, re-measured by plain commands below. No owned axis is harmed. Status `ok`.

Session quality-bar fact (not a protocol admission criterion): only wave 1 ran, 33 seats, 8 attack
seats (reviewer 4, critic 2, mutation-tester 2) = 24.2%, one seat short of the session's 25% attack
floor (9 of 33). Wave 2 (32 attack seats, validated, `.ufo/waves/round-25/a3/w2-spec.json`) was
cut by the 2 h scope freeze after the first wave waited an hour at the seat gate. The round total
of 33 is inside the 32–100 band. The protocol admits on claims verified and no axis harmed, so the
shortfall is recorded here and in the closure notes, not used to reject.

## Driver digest (copied from `.ufo/watchdog.log`)

```
2026-10-21T20:38:06-03:00 launch kaidoku round=25 pgid=2906419 driver=hyaku-inline attempt=1
2026-10-22T04:58:59-03:00 lane-dead-no-report kaidoku round=25; retry same round (hyaku-inline attempt=1: superseded at 2026-10-22T04:56:36-03:00: stale 2026-10-21/22 author; fresh attempt)
2026-10-22T05:15:09-03:00 launch kaidoku round=25 pgid=209083 driver=hyaku-inline attempt=2
2026-10-22T05:31:57-03:00 lane-dead-no-report kaidoku round=25; retry same round (hyaku-inline attempt=2: stood down at 2026-10-22T08:30Z by Main: process job limit 100 (config says 200) left 8 lanes without seats; lanes in flight cut 8 to 4; capacity decision, not a lane fault; fresh attempt later)
2026-10-22T06:19:48-03:00 launch kaidoku round=25 pgid=1077330 driver=hyaku-inline attempt=3
2026-10-22T08:46:42-03:00 complete kaidoku round=25; hyaku-inline attempt=3
```

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git -C <fleet> log --format='%an <%ae> %H' -- .ufo/reports/round-25/kaidoku.md` | one commit, `kaidoku-shokunin <kaidoku@shokunin.local> d0c4492f…` | pass |
| SHONEN heading, one line per box | read report `## SHONEN` | 4 lines, all `[~]` with pointers | pass |
| Cited lane commits exist and are ancestors of `main` | `git rev-parse --verify <h>^{commit}` and `git merge-base --is-ancestor <h> main` for `9dcd11ec 7ef837a4 46d2613d 0e333eb2 08c7a729 dc31f9c4 1e064f9b ad73b90e cce7504a` plus `fafdd283` | all exist, all ancestors | pass |
| Lane pushed, nothing left over | `scripts/hyaku/jj-lane.sh state <lane>`; `git -C <lane> status --porcelain` | `local=remote=cce7504a… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty | pass |
| Prompt carries the template contract | `.ufo/prompts/kaidoku-round-25.md` §1–§5 plus addendum §6 | MISSION/AXES binding, 1–3 claims, frontier step, L2 floor, report path, section order, SHONEN rule, commit-then-push, push scope, L0 channel all present | pass |
| Not a marker | report names real committed work | yes | status `ok` |

Conformance defects (status-neutral):

1. Sources before→after counts from the attempt-2 freeze (`7ef837a4`, 74 rows) instead of the
   lane-round base. Over the lane-round the registry went 72 → 78 rows
   (`git show <REV>:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} \|'` at `18e7eb6d` = 72,
   `7ef837a4` = 74, `cce7504a` = 78). Attempt 1's S073 and S074 are not in the report's tally.
2. The Landed changes table omits the attempt-1 commits `62feef9c`, `a4ab912a`, `fafdd283`
   that are in this lane-round's range (all are ancestors of `main`).
3. Attempt-1 bytes in this lane-round carry run-together tokens (for example SCORECARD
   "All finite proxy scores stay10.0", "fixed34", "round25 prerequisite"; SKILL.md
   "unavailable2", "all11"). These are the session-3 degradation pattern.
4. Attempt 1 froze a different claim set (`.ufo/waves/round-25/claims.json`, first added at
   `a4ab912a`; subject landed at `fafdd283`). Attempt 2 froze new claims at `7ef837a4` with before
   receipts, after the driver superseded attempt 1, and before any after-measurement of the new
   claims (committer times: `7ef837a4` 05:21:47-03:00, first repair `0e333eb2` 06:30:53-03:00).
   The new claims are not a narrowed version of the attempt-1 target. The report and lesson say
   the attempt-1 claim was "not pursued, not as met", and `corpus/claim-freezes.tsv` row
   `round-25` is FLAGGED for both freezes. Recorded as a disclosed fact, not a narrowing.

## Claims — re-measured by the closure

Instruments are unchanged from their pins: `git diff --quiet 9dcd11ec cce7504a -- tools/round-25/a2/`
exit 0; sha256 at `cce7504a` = `4378af84…6eee` (C1) and `7a7e6d65…6c70` (C2), equal to
`.ufo/waves/round-25/a2/claims.json`. Claims and before receipts first appear at `7ef837a4`;
instruments at `9dcd11ec`. The closure did not run either lane instrument. It re-derived each item
with plain git/grep commands, and read the committed receipts as evidence.

### R25-C1 calibration — 5 fixed self-assessment items, mismatches 5 → 0

| Item | Plain command (run at each REV) | `9dcd11ec` | `cce7504a` |
|---|---|---|---|
| I1 SCORECARD records the r24 outside decision | `git show REV:SCORECARD.md \| grep -nF 'corpus/lessons/round-24-verifier-spotcheck.md' \| grep -F rejected-honest-stop` | no line | `SCORECARD.md:3048` "records round 24 as **not admitted, rejected-honest-stop**" |
| I2 LOG records the same | same on `LOG.md` | no line | `LOG.md:2954` "rules round 24 not admitted, rejected-honest-stop" |
| I3 QUALITY row cites the r24 spot-check | `git show REV:corpus/QUALITY.md \| grep -nE '^\| [0-9]+ \|' \| grep -F round-24-verifier-spotcheck.md` | no row | row 34 at `corpus/QUALITY.md:44` |
| I4 coverage row N/N equals knowledge count | `git ls-tree -r --name-only REV corpus/knowledge/ \| grep -c '\.md$'`; `grep -n '^\| coverage \|' SCORECARD.md` (first match) | stated 78/78, observed 107 | stated 108/108, observed 108 |
| I5 SHONEN pointer inside `## Adjacent` | `grep -noE 'PROVINCE\.md:[0-9]+-[0-9]+' SHONEN.md`; `grep -n '^## ' PROVINCE.md` | 88-116; Adjacent 95–266 | 95-116; Adjacent 95–266 |

Re-measured: 5 mismatches of 5 at `9dcd11ec` → 0 of 5 at `cce7504a`. Committed receipts agree
(`corpus/evidence/round-25/a2/before/c1-calibration.json` mismatches 5; `a3/after/c1-at-{0e333eb2,08c7a729,dc31f9c4,1e064f9b}.json`
mismatches 0).

Statement vs counter: **not wider.** The declared statement is the five fixed items with an
explicit limit ("not a full audit of SCORECARD or SHONEN"). The counter's disclosed false-accept
paths were checked and are not used by the landed bytes. I4 takes the first `| coverage |` row: at
`cce7504a` that row is the owned-axes row at `SCORECARD.md:23`. The counter never reads the README
map; the closure's own recount (every knowledge file stem found in `corpus/README.md`
`## Coverage map`) gives 107/107 at `9dcd11ec` and 108/108 at `cce7504a`. I1–I2 are
line co-occurrence tests; the two lines read state the r24 verdict correctly (MANIFEST r24 closure:
`verdict rejected-honest-stop`). I3 row 34 turns the r24 verdict disagreement (expected-red
receipt is not a pass; original frozen result decides) into a criterion and quotes the spot-check.
**Verdict: calibration improved.**

### R25-C2 coverage — knowledge Markdown 107 → 108, entry sourced 0 → 1

| Measure | Plain command | `9dcd11ec` | `cce7504a` |
|---|---|---|---|
| knowledge Markdown | `git ls-tree -r --name-only REV corpus/knowledge/ \| grep -c '\.md$'` | 107 | 108 |
| added knowledge files | `git diff --name-status 18e7eb6d cce7504a -- corpus/knowledge` | — | one `A`: `2026-10-22-r25-evm-selector-name-resolution.md` |
| entry `source:` rows | first line of the entry | — | S075, S076, S077, S078, S021 |
| rows mined, opened 2026-10-22, used-by names entry | `grep -nE '^\| S07[5-8] \|' corpus/SOURCES.md` | rows absent | S075–S078 all `mined`, `2026-10-22`, used-by names the entry |

Re-measured: 107 → 108 and entry sourced 0 → 1. Receipts agree (`a2/before/c2-coverage.json`
107/0; `a3/after/c2-at-1e064f9b.json` 108/1, qualifying S075–S078).

Statement vs counter: **wider than the counter.** The statement says the entry sits on PROVINCE
Frontier ground and is sourced by rows *opened* on 2026-10-22. The counter checks only file count,
row cells and the entry's existence. The closure checked the wider parts directly:

- Frontier ground: `git show 18e7eb6d:PROVINCE.md` line 93 reads "selectors stay bare hashes (no
  signature DB → no name resolution)"; the README map gains a new row "EVM selector naming
  (round 25)" (`corpus/README.md:74`).
- Actual opening: all four new rows re-opened live today (table below); quotes found verbatim.
  Live sha256 of S076 (`896d6a30…c00b`) and S077 (`fba49f82…e955`) equal the saved copies in
  `corpus/evidence/round-25/a3/sources/`. All four saved copies hash to their `SHA256SUMS` lines.
- Provenance trio present (`source:`, `verified-at:`, `recheck:`); census validate exit 0.

The entry's truth was not re-derived end to end by the closure; it rests on saved evidence and lane
seat reports (`C2IndependentTally.md`, `C2IndependentKeccak.md`, `PriorEvmEntries.md`) read as
evidence. **Verdict: coverage improved.**

### Other axes

`git diff 18e7eb6d cce7504a -- SCORECARD.md`: coverage row 78/78 → 108/108; depth row adds a
recount 17/17 (`commandA-at-1e064f9b.json`: rule_blocks 17, citation_resolved_rules 17); calibration
row unchanged; finite scores stay 10. Deletions across the whole range are only 4 lines
(`git diff --numstat 18e7eb6d cce7504a | awk '$2>0'`): PROVINCE line 93 (frontier reword),
SHONEN line 12 (pointer), SCORECARD rows 23–24. No prior knowledge entry or lesson is modified
(`git diff --name-status … -- corpus/knowledge corpus/lessons` shows only two `A`); QUALITY only
appends row 34; SOURCES only appends S073–S078.

| Axis | Verdict |
|---|---|
| calibration | improved |
| coverage | improved |
| depth | unchanged |

## Discernment spot-check

Source census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
exit 0, five W04 duplicate-URL warnings (S033, S047, S054, S062, S069), then `kaidoku ok`.

| Item | Gate decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S077 EVMole interpretation reference | admit, docs/A, mined | https://raw.githubusercontent.com/cdump/evmole/master/agent/skills/evm-bytecode-analysis/references/interpretation.md, `Evidence and inference` | agree | Quote found verbatim: "A selector is a four-byte dispatch value found by static bytecode analysis. It does not supply a verified function name." (19 words). Live sha256 equals the saved copy. Maintainer page, so tier A for this scope holds. |
| S075 4byte.directory API docs (new row, quote check) | admit, docs/A, mined | https://www.4byte.directory/docs/, Signatures > Filtering on `hex_signature` | agree | Quote found verbatim: "If the provided query is exactly 4 bytes long then results are filtered by exact match." The narrowed `teaches` ("the page says nothing about result order") holds: no "order" token in the saved page, none seen live. |
| S078 Sourcify 2025 Recap | admit, docs/A, mined | https://docs.sourcify.dev/blog/recap-2025/, `4byte.sourcify.dev` | agree | Quote found verbatim: "We implemented the exact openchain API and now Sourcify serves all signature requests to openchain.xyz as well." The seeding claim holds; the page also lists Sourcify's own verified-contract dataset, which the row omits (minor). |
| S076 Sourcify 4byte OpenAPI | admit, docs/A, mined | https://api.4byte.sourcify.dev/api-docs/swagger.json, `/signature-database/v1/lookup` `filter` | agree | `filter` description is "Whether or not to filter out junk results"; `info.version` 1.0.0; live sha256 equals the recorded one. |
| EVMole README | reject (opened, not made a row) | https://raw.githubusercontent.com/cdump/evmole/master/README.md, Foundry section | agree | The page shows `cast selectors --resolve` printing names next to selectors and states no naming rule, no ranking and no limit; it adds nothing beyond S077. |
| Sourcify API page | reject (opened, not made a row) | https://docs.sourcify.dev/docs/api/ | agree | The 4byte part is one sentence plus a link to the OpenAPI file and a Swagger loader; the citable content is the OpenAPI file, already S076. |
| S073 Git merge-base manual (attempt-1 `## Gate`) | admit, docs/A | https://git-scm.com/docs/git-merge-base, `--is-ancestor`, page 2.43.0 | agree | Quote found verbatim: "Check if the first <commit> is an ancestor of the second <commit>"; version label matches. |

Admits and rejects sampled: 5 admits, 2 rejects; 0 disagreements. The round-24 outside disagreement
on the C2 verdict became QUALITY row 34 with the spot-check cited.

## Trend verdicts

- **expansion: improved.** One new admitted entry on ground the coverage map and PROVINCE Frontier
  did not hold (EVM selector naming; PROVINCE:93 at base says "no name resolution"). Its `source:`
  cites four `mined` rows opened this round, re-opened above with quotes found. Knowledge 107 → 108.
- **quality: unchanged.** No prior knowledge entry was superseded, re-verified with a refreshed
  `verified-at`, or found false. The improvements the lane names (QUALITY row 34, self-assessment
  repair, depth recount, in-round corrections to the new entry before it landed) are discernment,
  calibration or the new entry itself, not quality changes to held knowledge. Nothing found false
  and left unmarked: `PriorEvmEntries.md` reports the eight prior EVM entries hold.
- **discernment: improved.** The outside spot-check agrees with the gate on 5 admits and 2 rejects,
  and the round-24 outside disagreement became a grounded criterion (QUALITY row 34 citing
  `corpus/lessons/round-24-verifier-spotcheck.md`).

## SHONEN

All four boxes are `[~]`. None is checked here: promotion is operator-owned. The "No cross-domain
bleed" box now points inside `## Adjacent` and looks checkable by a non-author; the operator may
review it.

## Routed defects (lane owns; fix next round)

1. `SKILL.md` section "Explicit instrument-reference custody — round 25 prospective authority" and its
   registry row `round25-custody-ruler` still say the candidate `tools/round-25/instrument-custody.py`
   "is not implemented at this phase", while `fafdd283` landed it and the claim was abandoned.
   Append a superseding note that names the abandoned claim and the landed file.
2. Self-assessment statements found stale by wave-1 seat `C1Cherrypick.md` remain open (coverage
   and calibration rows' measured-revision cells; SHONEN "province-version alignment is contested").
   They are disclosed at `SCORECARD.md` round-25 section; correct or re-measure them.
3. The two frozen instruments have disclosed false accepts (I4 first-row rule, no README read; C2
   reads the `opened` cell only). Do not reuse them as frozen counters without fixing those paths
   first, with a red-before fixture.
4. Entry wording: "one complete 4byte.directory page and one openchain `filter=false` response per
   selector" — the 138 responses are 2 per carrier-selector row (69 rows), not per distinct selector
   (43). Correct in a new commit.
5. Round-24 source disagreement (initial capinfos rejection, later S071 flip) has no QUALITY
   criterion; either add one citing the r24 spot-check or record why the flip already covers it.
6. Reports: count Sources before→after from the lane-round base, and list every lane-round commit
   (including superseded attempts) in Landed changes.
7. Attempt-1 run-together tokens in SCORECARD/SKILL/lesson text: leave filed bytes, but write new
   text with spaced tokens.
