# ReviewControlsReceipts — R31 wave-2 falsify review of committed control receipts

Seat: `KaidokuR31.ReviewControlsReceipts` (w2, leaf). Scope: compare `controls/receipts.tsv` + `controls/receipts-detail.tsv` against the wave-1 control reports (`w1/Ctl*.md`), verify the receipts commit (7474d269) precedes the data commit (f368a101), and verify the receipts name every control required by `claims.json` `controls_required_before_data`. All paths absolute; lane read-only; sole lane write is this report.

## Method

Read-only git in the lane (`git log/show/diff/rev-parse/merge-base/cat-file`), `python3 -I -B` for the claims field, file reads of the 12 `w1/Ctl*.md` reports, the two receipts TSVs, and the two committed freeze-integrity gate outputs. No counter run, no writes to the lane or fleet, no git writes. Verification log retained at `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReviewControlsReceipts/verify-log.txt` (SHA256 `a877656569c36061001f6d6b536773d90746eb0bd4b87c51478cfef786f9d515`).

## Findings by checked item

### 1. Commit ordering — holds

`git log --no-patch` (exit 0), 2026-10-23T04:31:23Z:

- receipts `7474d26951ea03b` ct=1792729127 → 2026-10-23T04:18:47Z, "pre-data control receipts (10 frozen controls + 2 extra, none met a target), freeze-integrity gate, wave-1 reports (39 returned)"
- data `f368a101277ab9c4` ct=1792729175 → 2026-10-23T04:19:35Z, "data — 12 C1 envelopes and 23 C2 envelopes … after the control receipts (7474d269)"
- entries `0007731eec3a00c1` ct=1792729533 → 04:25:33Z; tip `1288285eed81395e6` ct=1792729627 → 04:27:07Z

`git merge-base --is-ancestor` exits: `7474d269 f368a101` → 0; `f368a101 0007731e` → 0; `0007731e 1288285e` → 0. Receipts commit precedes data commit, data precedes entries, entries precede tip.

### 2. Receipt files committed and unchanged — holds

`git diff 7474d269 -- controls/receipts.tsv controls/receipts-detail.tsv | wc -c` → 0 (working tree identical to receipts commit). Same for all 12 `w1/Ctl*.md`: `git diff 7474d269 -- w1/Ctl* | wc -c` → 0.

### 3. Row-by-row report match — holds (12/12)

Each detail row's `receipt` path resolves to the named report, whose CONTROL header, counter exit, score and construction match the receipt row (excerpts in verify-log):

| Row | Report | CONTROL line | Exit / score | Match |
|---|---|---|---|---|
| R31-C1 do-nothing | CtlC1DoNothing.md | met=no score=0/12 | 1; pass=0 entry_ok=0 province_ok=0 (both freeze & HEAD runs) | ✓ |
| R31-C1 junk-row | CtlC1JunkRow.md | met=no score=0/12 | 1; pass=0 entry_ok=1 province_ok=1 | ✓ |
| R31-C1 all-false | CtlC1AllFalse.md | met=no score=0/12 | 1; pass=0 entry_ok=1 province_ok=1, full comparison on all 12 | ✓ |
| R31-C1 no-reader | CtlC1NoReader.md | met=no score=0/12 | 1; pass=0, full comparison all 12, both doc gates passed | ✓ |
| R31-C1 shortcut keyed on ids/labels | CtlC1ShortcutIds.md | met=no score=0/12 | 1; pass=0 entry_ok=1 province_ok=1 on rotated run | ✓ |
| R31-C2 do-nothing | CtlC2DoNothing.md | met=no score=0/23 | 1; matches=0 entry_ok=0 skill_ok=0 (both runs) | ✓ |
| R31-C2 junk-row | CtlC2JunkRow.md | met=no score=0/23 | 1; matches=0 entry_ok=1 skill_ok=1 | ✓ |
| R31-C2 all-false | CtlC2AllAccept.md | met=no score=0/23 | 1; matches=0 entry_ok=1 skill_ok=1 | ✓ |
| R31-C2 no-reader | CtlC2CopiedPredictions.md | met=no score=0/23 | 1; matches=0 entry_ok=1 skill_ok=1, full comparison all 23 | ✓ |
| R31-C2 shortcut keyed on ids/labels | CtlC2ShortcutIds.md | met=no score=1/23 | 1; matches=1 — m-not-sqlite holds m-bad-pagesize's envelope, equal outside top-level meta (report: raw stdout hashes fe524e1e…/12b802db…; `"envelopes_equal_except_top_level_meta": true`) | ✓ |
| R31-C1 Core-placement shortcut (extra) | CtlC1Placement.md | met=no score=12/12 (A and B) | 1 both; pass=12 province_ok=0 both (A: row under `## Frontier`; B: prose under a Core heading) | ✓ |
| R31-C2 after-freeze amendment of predictions.tsv (extra) | CtlC2RewritePred.md | met=no score=0/23 | 1 pristine/amended/restored; counter matches=0 and did not detect the edit; prefreeze-gate.py CLEAN (missed); freeze-integrity.py FAIL exit 1 (caught) | ✓ |

The rewrite-pred gate claim is independently confirmed by output committed in the same receipts commit: `controls/freeze-integrity-ctl-rewritepred.txt` ends `freeze-integrity: FAIL pins=5 changed=1 freeze=35ba7c522dba rev=980bfa7e17d87b861889a467eb0879dc0692c7e6` / `exit=1` (predictions blob `aa4173a49916`, `commits_after_freeze=980bfa7e`); `controls/freeze-integrity-lane-at-35ba7c52.txt` ends `freeze-integrity: CLEAN` / `exit=0`.

### 4. Required controls coverage — holds

`claims.json` `controls_required_before_data` (content hash `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51`, identical to the freeze blob at 35ba7c52 — `git rev-parse 35ba7c52:…/claims.json` = b816f183a83973b74f4fde5e8a2537a981924ec8, `git cat-file blob` → same sha256) lists exactly 5 named controls. All five appear in receipts.tsv for both claims:

1. `do-nothing` → R31-C1 / R31-C2 rows ✓
2. `junk-row (entry + PROVINCE/SKILL rows without envelopes)` → junk-row rows ✓
3. `all-false (committed refusal envelopes for C1; all-accept for C2)` → all-false rows ✓
4. `no-reader (envelopes fabricated from the oracle or the predictions, never produced by REA)` → no-reader rows ✓
5. `shortcut keyed on ids/labels (another carrier's or request's envelope under the id)` → shortcut rows ✓

10 required rows, all named, all `counter_exit=1` and `met_target=no`; plus 2 rows explicitly marked "(extra)" (C1 placement, C2 rewrite-pred). Receipts commit message statement "10 frozen controls + 2 extra, none met a target" is consistent: 12 rows, all `met_target=no`.

## Verdict

- Receipts-vs-reports consistency: **holds** for all 12 rows (exit, score/met_target, construction).
- Commit ordering: **holds** (7474d269 → f368a101 → 0007731e → tip, ancestry-verified).
- Required-control naming: **holds** (all 5 × both claims present; extras allowed and labeled).

## Residual risk / verification gaps

- Re-execution gap: I did not re-run any counter; comparison is report-vs-receipt document/history consistency, not live re-measurement (the L1 measured C1 12/12 and C2 23/23 at 0007731e; the wave-1 "F2/F3" findings in CtlC1AllFalse.md — the literal target line with parentheticals and the `--write-evidence` self-certifying mode — concern scoring procedure, not the receipt rows, which record exit 1 / met=no faithfully).
- The one match in the shortcut-ids C2 control (`m-not-sqlite` ≡ `m-bad-pagesize` outside meta) is a documented coverage/identity limitation of the frozen full-envelope equivalence, not a receipt mismatch.
- Untested by this seat: whether the receipts will be enforced by the integrator gate (e.g. that data was only committed after all `met_target=no` receipts); that is an integration-policy check outside this assignment.
