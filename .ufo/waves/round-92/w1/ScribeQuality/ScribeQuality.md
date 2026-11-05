# ScribeQuality (round 92, w1) — draft quality rows 184–187 and round-92 mistake M92-a

Seat: ScribeQuality (scribe, leaf, no subagent dispatch). Lane: `kaidoku-shokunin`, base `73a882712`, declaration `11f8606178dfd9e72001b31daf412c5463106a63`.
Status: **drafts only, nothing landed.** No lane file was edited, no lane git mutation was run, no counter was run in the lane.

## Deliverables (all in this seat directory)

| file | content |
|---|---|
| `quality-draft.md` | QUALITY rows 184, 185, 186, 187, each with an Attack paragraph naming the existing row it duplicates, sharpens or contradicts |
| `mistakes-draft.md` | `corpus/lessons/round-92.md` `## Mistakes`: M92-a (report figure ≠ receipt), with its fixture |
| `sweep-w04.sh` | the sweep command for 187 (`sweep-w04.sh <report.md> <receipt.txt>`; exit 0 agree, 1 disagree, 2 nothing checked) |
| `fixtures/` | the two report sentences and the synthetic receipt used by the fixture run (copies from scratch) |
| `receipts/sweep-w04-fixtures.log` | the fixture run, with each command, output and rc |

## Ground checks run (read-only)

- `corpus/QUALITY.md`: 309 lines, last row 183; `grep -E '^- \*\*Row 18[4-9]'` → 0 hits, so 184 is the next free number.
- Fixture run (`receipts/sweep-w04-fixtures.log`, exit codes as logged):
  - F1 real sentence `reports 7 W04` vs `.ufo/waves/round-91/l1/census-before.txt` → `DISAGREE: report 7 != receipt 29`, **rc 1** (expected 1).
  - F2 same sentence with `29` vs `census-before.txt` → `agree: report 29 == receipt 29`, **rc 0** (expected 0).
  - F1c real sentence `7` vs `census-after.txt` → `DISAGREE: report 7 != receipt 29`, **rc 1**.
  - F3 synthetic `7` vs a receipt carrying 2 W04 lines → **rc 1**. (The fixture file is named `f3-receipt-3lines.txt` but holds 2 W04 lines and 1 `ok` line; the name is wrong, the verdict is not affected.)
  - F4 synthetic `3` vs the same 2-line receipt → **rc 1**.
  - F5 report with no `N W04` figure → **rc 2** ("nothing checked").
  - F6 missing receipt → **rc 2**.
- Census receipt count: `grep -cP '\tW04\t'` = **29** on `census-before.txt`, **29** on `census-after.txt`; `census-after-counts.txt` carries no W04 line. The round-91 report line 80 states `7 W04`. The spot-check D-91-1 says the same; this seat re-derives it.
- Evidence pointers checked to exist: `.ufo/waves/round-91/w1/ReviewerFalsify.md`, `.ufo/waves/round-91/w1/CriticClaims.md`, `.ufo/waves/round-91/w1/CriticClaims/evidence/receipts/c1-cheat_typed_only.json` (the ATTACK-2 table writes `receipts/…` relative to `evidence/`), `.ufo/waves/round-91/w1/CriticClaims/evidence/cheats/`, `.ufo/waves/round-91/pre/c1-base-round90-repair.json`, `.ufo/waves/round-92/pre/controls-summary.json`, `tools/round-91/upx-stop-boundary-repair.py`, `tools/round-92/stop-boundary-battery-v2.py`, `plans/round-92-claims.md`.
- Round-92 `tools/round-92/stop-boundary-battery-v2.py` at `11f8606` (read via `git show`): `typed_refusal()` requires rc 2 and a last stdout line that parses to a JSON object with a `refused` key. Row 185 is the same predicate, written as corpus rule.
- Round-91 `tools/round-91/upx-stop-boundary-repair.py` `main`: `except Refused` prints `{"tool","class","refused"}` and returns 2. So the typed form in 185 is the form the round-91 tool already emits; the positive control (`pre/c2-positive-v2-round91.json`, `typed 10`) is consistent with it.

## Attacks (per row; full text in `quality-draft.md`)

1. **184 contradicts QUALITY 178 as written.** 178 says to refuse with rc 2 and no output unless `upx -t` on the input is green. R92-C1 repairs a red input inside ±16. The drafted row therefore supersedes 178's refusal clause for the declared window only (the Row 103 pattern) and keeps 178's refusal outside the window. Without that clause the round-92 repair breaks a standing row. Also sharpens 171 (filter vs rank key) and operationalises 182. Not a duplicate.
2. **185 is adjacent to 169 and 177, and shares a term with 26.** 169 (guards inherited, rc-2 contract) and 177 (exception coverage) are about the tool; 185 is about the counter's predicate. Row 26 uses "typed refusal" for held-verb evidence envelopes; 185 uses it for counter classes. Same word, different object; cross-reference recommended. Compatible with 155.
3. **186 is a near-duplicate of 152** (cheap-rule controls scored before freeze). The unseen-carrier clause is new. Recommended: fold into 152 as an appended clause. Adjacent to 147 and 174, not in conflict.
4. **187 duplicates 150 in substance** (record cell states a count, re-derived at the revision it names). 150's scope is registry, docstring and scorecard cells; 187 extends it to report prose. Recommended: add report prose to 150's scope and not open a number. Adjacent to 135, 105, 74.

Net recommendation to the integrator: land 184 and 185 as new rows; fold 186 into 152 and 187 into 150. That is three new numbers, not four. Final placement is the integrator's decision.

## Mistake M92-a (drafted in `mistakes-draft.md`)

- Class: report figure not equal to its receipt. Evidence: `corpus/lessons/round-91-verifier-spotcheck.md` §5 D-91-1; `.ufo/waves/round-91/l1/census-before.txt` (29 W04 lines); report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-91/kaidoku.md` line 80.
- Captured-by: `none` (QUALITY 150 does not reach report prose).
- Fix: QUALITY 187 plus `sweep-w04.sh`. Fixture where it must fail: F1 above (rc 1, `report 7 != receipt 29`); the corrected sentence passes (F2, rc 0).

## Scope limits, stated plainly

- The sweep covers only the W04 class. A sweep that claims "every number" needs one table row per class. The draft row says so.
- Row 187 cites the round-91 report, which is in the fleet root (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-91/kaidoku.md`), not the lane. The sweep reads it as given.
- The round-91 CRITIC ATTACK-2 table gives `receipts/…` paths relative to `CriticClaims/evidence/`; the drafts cite the full path.
- Rows 184 and 186 cite plans and controls that the round-92 wave is still building (the candidate `tools/round-92/upx-stop-boundary-search-repair.py` and the round-92 controls). Their evidence is the frozen claim text and the committed controls summary; this seat did not run any of those counters, so no receipt is claimed for them.

## Write-scope note

The orchestrator's `Report:` trailer names `.ufo/waves/round-92/w1/ScribeQuality.md`. The seat rules say to write only inside the seat directory, and the item says to deliver `ScribeQuality.md` into the seat directory. This report is therefore at `.ufo/waves/round-92/w1/ScribeQuality/ScribeQuality.md`. The integrator should copy or link it to the trailer path if the trailer is the one to be read.

## Host and tooling

- No install or upgrade was made. No pacman, no sysctl, no `~/.local/bin` write, no fleet-root tracked file written.
- The scratch directory `/fast/scratch/hyaku/kaidoku-r92/ScribeQuality` held only the sweep and fixtures; its copies are in this seat, and the scratch directory was removed after the copy.
- No subagent was spawned (leaf seat).

## Checks for the main agent to run once (not run by this seat)

- `bash .ufo/waves/round-92/w1/ScribeQuality/sweep-w04.sh <report> .ufo/waves/round-91/l1/census-before.txt` against any report the integrator wants checked; expect rc 1 on the round-91 report until it is corrected.
- After landing 184–187 or their folds: `grep -cE '^- \*\*Row 18[4-7]' corpus/QUALITY.md` should be 4 if all four are kept as numbers, 2 if 186 and 187 are folded (184 and 185 only).
