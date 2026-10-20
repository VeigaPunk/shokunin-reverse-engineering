# CriterionDraft — final QUALITY #17 assessment (routed defect 2)

Seat: `KaidokuR15.CriterionDraft` (leaf; no dispatch). Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Access date: 2026-10-20.
Status: L1 reports the superseding row is already integrated at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md:27`. This report assesses that final text against routed defect 2. No corpus, LOG, SKILL, lesson, gate, or fixture byte was written by this seat. This is routed defect 2 only; defect 1 (virtual-dispatch advisory) is another seat's duty. No execution of any gate, selftest, frozen run, measure, census, build, test, lint, formatter, or target/provider call. No installs or updates.

Deliverable: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/CriterionDraft.candidate.md` (drafted row plus delta against the final text).

## Axes

- **depth** — the final row retains the whole #16 obligation set (contiguous located passage, no splice or foreign locator, pinned manifest+verdict, exit 2 unevaluable) instead of replacing with a thin policy sentence. This report verifies each obligation is present, not inferred.
- **calibration** — the final row separates policy (manual-only inputs are not submitted), observation (no representation classifier; ordinary 0/1/2 rules; verdict void), and limit (green proves only pinned substring/section consistency). The only residual is that the literal finding id `quote_not_contiguous` is not named; the behavior is stated correctly.

## Final criterion: point-by-point against routed defect 2

Final row observed at `corpus/QUALITY.md:27`, 1222 characters, supersedes cell `16`, file SHA-256 `2052ed505888c5cc2e9cd78fa5eb9f76eb71c2dbbb31842107ca592849be1fb3` (mtime `2026-10-20 04:00:35 -0300`; HEAD has no row 17 and `git diff` against `9719dd232687f5ee78a4ed323b37f8810e833d10` shows exactly one added row with row 16 unchanged).

| Routed requirement | Final row | Verdict |
|---|---|---|
| representations named: code, commit, JSON, output, rendered markup-spanning | names all five and extends rendered text to character references; states raw-copied tags are not the excluded form | satisfied |
| MUST NOT be submitted as machine-gradeable | "must not be submitted as machine-gradeable" (case-insensitive marker present) | satisfied |
| manual source check | "check the appropriate source manually under #1" | satisfied |
| actual submitted rendered quote may exit 1, not an automatic exit-2 unsupported classification | "an excluded submission may receive 0/1/2 through ordinary raw/malformed/tampered rules, but that verdict is void for the manual-only claim"; "in the isolated rendered control a raw-substring miss returns 1, not an unsupported-input classification"; "no representation classifier" | satisfied in behavior; literal `quote_not_contiguous` not named (residual below) |
| supersedes #16 | text begins "Supersedes #16's manual-only ambiguity while retaining its fidelity rules"; cell `16` | satisfied |
| names the round-15 lesson | why cell cites `corpus/lessons/round-15.md`, Mistakes and Gate | satisfied |
| no gate implementation change | no gate/fixture bytes touched; row is policy only | satisfied |
| #16 obligations retained | contiguous located passage; no splice/reused locator; pinned manifest+verdict; "exit 2 is unevaluable, never clean" | satisfied |

### Residual (low severity, no change requested)

The final row never contains the literal finding id `quote_not_contiguous` (verified by substring check on the row). A reader must map "raw-substring miss returns 1" to the gate's finding. The candidate draft names `quote_not_contiguous`, `quote_location_mismatch`, and `quote_too_long`. Because the final text already states the rendered control's outcome and denies classifier status, this is a precision gap, not a defect in the policy; L1 reports the row final and this seat makes no corpus edit.

## Observed evidence (static)

- `quote-fidelity.py:35-36`: no whitespace, tag, or punctuation normalization is applied to quote or source; `:40-41` define `quote_not_contiguous` (absent from whole source) and `quote_location_mismatch` (section absent or quote outside it).
- `:78`: `CNE_FINDINGS = {"invalid_manifest", "source_tampered", "snapshot_tampered"}`; `:97-100` returns exit 2 only for those, otherwise 1 for any finding, 0 for none.
- `:250-268` (`grade_quote`): word count first (`quote_too_long`, exit 1), exact whole-source membership, then exact heading selectors and section body.
- Boundary fixture (synthetic, not executed): `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/rendered-rejected.json` quotes `Use raw bytes.` while `raw-source.md` contains `Use <em>raw</em> bytes.`; the rendered string is absent, so the code path is `quote_not_contiguous@rendered-text`, exit 1. The pinned source digest `2e80083b7567beaf119463cee31eb617a02d3ab7887bce8441baf43150118270` matches the observed `sha256sum` of `raw-source.md`. The raw-accepted manifest quotes the literal tagged form and should be exit 0. These are code derivations, not gate output.
- Lesson: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-15.md` exists (73 lines at read, uncommitted); Mistakes row at line 65 records routed defect 2, says "Superseding #17 requires excluded representations not be submitted as machine-gradeable", and defers exact exits to L1 execution.
- LOG: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/LOG.md:1855-1858` records "C2 adds QUALITY #17, preserving prior contiguous-quote requirements while making manual-only input discipline explicit", the absence of a representation classifier, and that a raw verdict on excluded input is not a valid claim verdict.

## Competing texts (record only; final is L1's)

| Obligation | Final row | FrontierScribe C1 | This draft |
|---|---|---|---|
| #16 splice/locator + manifest/verdict + "never clean" | yes | no | yes |
| manual-only classes, entities, raw-tag distinction | yes | markup only, no entity/raw-tag clause | yes |
| `must not be submitted` marker | yes | row says "are not submitted" | yes |
| 0/1/2 outcome and void verdict | yes | "exit map unchanged" only | yes, plus CNE triggers |
| literal finding ids | no | no | yes |
| supersedes cell | `16` | prose | `16` |
| cites round-15 lesson | yes | no | yes |

`FrontierScribe.md:57` does contain "must not be submitted" in its advisory prose, but its proposed row does not; a row-scoped measure would not match it. The final row satisfies the wave's measure marker (`must not be submitted`, case-insensitive) and `Supersedes #16` presence checks.

## Critic cross-check

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/AttackManualBoundary.md` attacked the earlier 03:55:10 text. Against the final row:

- **X1 false "not exit 2" guarantee:** resolved. The final row says an excluded submission "may receive 0/1/2 through ordinary raw/malformed/tampered rules", not "never exit 2".
- **X2 dropped #16 duties:** resolved. The final row carries the splice/locator, manifest/verdict, and unevaluable-exit clauses, so the bare `16` cell does not silently weaken #16.
- **X3 no disposition:** resolved. "that verdict is void for the manual-only claim" is the void-verdict clause.
- **X4 heading parser:** resolved. The final row names Markdown ATX or single-line HTML h1–h6 headings.
- **X5 entities/raw tags:** resolved. The final row includes character references and states raw-copied tags are not the excluded form.
- **X8 missing lesson:** resolved at observation; `corpus/lessons/round-15.md` now exists and is cited.
- **X7 SKILL row still reads "invalid input":** open, low. `SKILL.md:450` is outside this seat's write scope and the final row does not depend on it; L1 decides whether a same-line registry clarification is in scope.

## Limits

- Static reading only. No gate, selftest, frozen run, measure, census, or REA operation; the boundary outcomes are code-path derivations.
- `corpus/QUALITY.md`, `corpus/lessons/round-15.md`, and `LOG.md` were uncommitted at observation and may change before commit; the row digest `2052ed…` is a point-in-time value.
- The final row is L1's text; the candidate is not integrated and must not be inserted as a duplicate.
- The residual finding-id gap is a precision observation, not a claim that the final policy is wrong.
- No installs or updates were needed or performed.

## Proposed L1 checks (named; not run by this seat)

1. `git diff 9719dd232687f5ee78a4ed323b37f8810e833d10 -- corpus/QUALITY.md` shows exactly one added `| 17 |` line; the row-16 line is unchanged.
2. Final row identity: exactly one line starts `| 17 |`; last cell is `16`; the line contains `corpus/lessons/round-15.md` and matches `must not be submitted` case-insensitively.
3. `git diff 9719dd232687f5ee78a4ed323b37f8810e833d10 -- .ufo/waves/round-14/tools/quote-fidelity.py .ufo/waves/round-14/fixtures/` is empty.
4. At the committed revision, `git show <REV>:corpus/lessons/round-15.md` exists with the defect-2 Mistakes row, and `LOG.md` still carries the #17 entry; the row's why cell resolves.
5. Optional limitation control, if L1 chooses to execute it: `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --manifest .ufo/waves/round-15/boundary-fixtures/raw-accepted.json` → exit 0; the `rendered-rejected.json` run → exit 1, `quote_not_contiguous@rendered-text`. Record as "this fixture", not as a general rendered-quote detection result.
6. Regression unchanged: `--selftest` remains 28/28 and `--frozen` remains exit 0 with seven matched pins; `measure.py` at the integration revision reports the C2 wording marker.

## Files changed by this seat

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/CriterionDraft.candidate.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/CriterionDraft.md`

No other file was written; `corpus/QUALITY.md` was read, never edited.
