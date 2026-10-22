# NoHarmDiff — round 26 wave 2 (falsify)

Seat: KaidokuR26.NoHarmDiff. Target: is any owned axis (coverage, depth, calibration) harmed between base a0639d8e61e486e2a716ff94cddd89a73200a02c and tip c327772653badd3b19b3954e1f8713973aa3f93e.
Judged bytes: Git objects at c327772653badd3b19b3954e1f8713973aa3f93e (later L1 commits not judged). Window 2026-10-22T12:58:22Z to 13:00:13Z UTC.
Artifacts: /fast/scratch/hyaku/kaidoku-r26/seats/w2/NoHarmDiff/ (sha256 list at the end). No tools installed or upgraded. No REA calls were needed.

## Verdict: holds

No owned axis is harmed. Every deletion is an in-place restatement of a SCORECARD owned-axes row or the SHONEN cross-domain clause, which is the claimed C2 repair. Knowledge entries and lessons only gained lines.

## Diff totals (observation)

Command: `git diff --stat a0639d8e c327772653badd3b19b3954e1f8713973aa3f93e`, exit 0, 12:58:22Z. Excerpt: `47 files changed, 4252 insertions(+), 4 deletions(-)`.
Command: the same range with `--numstat`, filtered to rows with deletions greater than 0, exit 0. Output: `3	3	SCORECARD.md` and `1	1	SHONEN.md`. No other file has a deleted line.
Command: `git diff --name-status`, non-added rows only. Modified files: SCORECARD.md, SHONEN.md, SKILL.md, corpus/QUALITY.md, corpus/README.md, corpus/SOURCES.md, corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md. Every other path is an addition. No file was deleted or renamed.

## List of deletions (observation; hunks in deletion-hunks.diff)

1. SCORECARD.md line 23, the coverage row. The old row read 108/108, measured 3395b6d. The new row reads 109/109 measured at ebe2cb4a. It keeps 78/78 at 3395b6d, 107/107 at 7ef837a4 and 108/108 as history. Dropped wording: "missing [], dangling []" for 7ef837a4.
2. SCORECARD.md line 24, the depth row. The old row read 9/9 at 638fb211 and 17/17 at 08c7a729, with craft span `SKILL.md:81-318`. The new row reads 17/17 at ebe2cb4a, keeps 9/9 at 638fb211 and 08c7a729 as history, and gives span `SKILL.md:81-314` plus the baseline `SKILL.md:77-191`. Dropped wording: "found by wave-1 seat C1Cherrypick" and the 81-318 range.
3. SCORECARD.md line 25, the calibration row. The old evidence cell said "measured at `75af886a`". The new cell says "count measured at c265db9b" and keeps 75af886a, labelled as the luna-round-2 reconciliation. The 9/9 observable cell is unchanged.
4. SHONEN.md line 11. The word "contested" and the bare 6.5.0/207/v42 reference are replaced by a pointer to `PROVINCE.md:8-14` and a statement that the observations are superseded. The `PROVINCE.md:95-116` boundary text is kept verbatim.

Restated history values re-derive under command A (observation, commandA-history.txt, exit 0 each run): `3395b6d cov 78 / 78 depth 9 / 9`, `638fb211 ... depth 9 / 9`, `7ef837a4... cov 107 / 107 depth 17 / 17`, `08c7a729... cov 108 / 108 depth 17 / 17`. The craft span check (awk for the last non-blank line before line 319) gives `tip craft last nonblank 314` and the same at base, so the replaced 81-318 was not the last non-blank line at base or tip. Inference: the dropped words lose provenance detail only (C1Cherrypick is still credited in claims.json), not a measured value.

## Command A at base and tip (observation)

The recipe was extracted from SCORECARD `## Measurement recipes`. `diff` printed `recipe A identical at base and tip`. Each run was `REV=<rev> bash commandA.sh`, exit 0, at 12:58:54Z.
- a0639d8e: `"citation_resolved_rules": 17, ... "knowledge_files": 108, "mapped": 108, "missing": [], ... "rule_blocks": 17`
- 81f63f36: same as base.
- ebe2cb4a, 46ebfd2f, bd0c84bc and c3277726: `"citation_resolved_rules": 17, ... "dangling": [], ... "knowledge_files": 109, "mapped": 109, "missing": [], ... "rule_blocks": 17`
Coverage goes from 108/108 to 109/109 (10.0 to 10.0). Depth stays 17/17 (10.0). No intermediate commit dips.

## Calibration and claim instruments at tip (observation, 12:59:08Z)

- `python3 -I -B tools/round-26/c2-calibration.py --root <lane> --rev c3277726...` gave exit 0 and `mismatches 0 items 6`. The C3 commit after 46ebfd2f did not reopen any K item.
- `python3 -I -B tools/round-26/c1-id-identity.py --root <lane> --rev c3277726...` gave exit 0 and `'rows_total': 8, 'rows_complete': 8, 'entry_ok': 1`.
- Command B was run on `git show` copies of rubric.json and result.json, exit 0 at both. The output is the same at a0639d8e and the tip: `"stage":"after","revision":"c265db9bd3c0883fbaf4487f839559c85a736826","aligned":9,"total":9,"score":10`. `git diff --quiet a0639d8e <tip> -- evidence/` printed `evidence/ unchanged base..tip`.

## Append-only check on knowledge and lessons (observation)

For each commit in a0639d8e..tip, I ran `git diff --numstat` and `--name-status` on corpus/knowledge and corpus/lessons and printed any row with deletions or a status other than add. The only output was `c3277726 M corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md`, a modification with no deleted lines. Its hunk is `@@ -175,0 +176,30 @@` in a 175-line file, so it is a pure end-of-file append. The new lesson round-26.md and the r26 entry are additions. No prior lesson file changed.
Other modified files are also insert-only. `SKILL.md` has `@@ -832,0 +833,49 @@` (end-of-file, after the craft span). `QUALITY.md` has `@@ -44,0 +45 @@`. `README.md` has inserts after base lines 74, 164 and 203. `SOURCES.md` has inserts after base lines 84 and 146. The craft heading is at 81 and the next `## ` heading is at 319 at a0639d8e, ebe2cb4a, 46ebfd2f and the tip.

## Strongest counterexample tested: line-shifted pointers (round-12 lesson 9 hazard)

`git grep` at the tip found 47 pointer lines of the form README, SOURCES or QUALITY `.md:N`, and filtered them to targets past an insertion point (pointers-tip.txt). The only live one is SCORECARD.md:69, which cites `corpus/README.md:180` for the "held, not frontier" bullet. The others name an older revision.
- Observation (readme180-check.txt): at a0639d8e, README line 180 is already the `round-19` lessons row, and the bullet is at `196:`. At the tip it is at `198:`.
- Conclusion (inference): this pointer was already stale at base. Round 26's two README inserts above it move the target two lines further but do not make a correct pointer wrong. No owned-axis instrument reads it (command A, C1, C2). This is a pre-existing freshness defect, not round-26 harm.
- The lane census was run as `python3 <tree>/.ufo/gates/c1-census-v10.py --root <tree>` on `git archive` trees of base and tip, at 12:59:54Z. Both exit 1 with `VERDICT: FAIL  (stale=1 ambiguous=0 undeclared=1 unresolved=0)`. With the revision string removed, `diff` of the two outputs differs only in `SKILL.md lines=832` versus `lines=881`. The stale finding is `/home/vgpnk/.omp/agent/mcp.json:8 -> STALE`, a host file outside the lane. No regression.

## Harm verdict per axis

| Axis | Base | Tip | Harmed |
|---|---|---|---|
| coverage | command A 108/108, missing 0, dangling 0 | 109/109, missing 0, dangling 0 | no (observation) |
| depth | command A 17/17; craft span 81 to 314 | 17/17; span unchanged; C1 8 of 8, entry_ok 1 | no (observation) |
| calibration | command B 9/9; C2 5 of 6 mismatches | command B 9/9; C2 0 of 6 | no (observation) |

## Smallest safe correction (optional, not an axis defect)

SCORECARD.md:69 should re-point `corpus/README.md:180` to the "held, not frontier" bullet, which is at README line 198 at the tip. Because that section is append-only, this means appending a correction note. It was stale before round 26 and should be routed as carried debt, not counted against this round.
Unknown: commits the L1 adds after c3277726 were not judged.

## Artifacts (sha256)

e6bb76da991031b98ce51ce6e3653904ae9156db0e6cfd9f066a9d2dd48b3247 commandA.sh
50d48bc8bbf02d9425782baa25badb83a4f4700583e29b6a9197b11e040b135b commandA-runs.txt
6624ff78b9c2c31e14509e0491c77799052411b6e2b8e239fdb1628024c59673 commandA-history.txt
81ce30742690fcf930e5536669805b9e3538ccacbb3d1754544fa2de1d413c05 commandB-runs.txt
037de95a9ffb32fa398f1a3cdcf4c417e35cf9357ce8411730eb60061f6bae24 c1-at-tip.json
a977e5ec2b5c19702af171399eeb5b9a4588cba843cd8c47b94b9bec69a04345 c2-at-tip.json
53040428b1d60c8d97821bb9fa4bd913f2455e35f53f0f36ee1132fea7eb8f19 census-a0639d8e.txt
f90d34cbaa663ca9e8281a3a07fe68fc0fb5116bed08657cdce2325b911794c7 census-c3277726.txt
9a6a8009999fe6401a21d47aa74371d4b66bc6aff1dcf860417a78b8ed012ed2 deletion-hunks.diff
c563bd9e12e1d88220b1b2c17b912020522bcc8a9be4625bdb01c919ae531bad diff-stat.txt
1f716e39503628b53ed5236518b926285efb245a195e0bc865f404f82885adab numstat.txt
b7d31a84340f87a9ed49f16901a7a8ae2b81ed6de5f0f011d7324e55672cdd96 hunk-headers.txt
c539ba6cd53a3dfa1c9194df793c39d3049757b091b6a3f65e7eec2574e96746 per-commit-kl.txt
2e4a40ad027800085be36d8b1dcb5a87ab05193fcae2263150e0789e1afb82ce pointers-tip.txt
1b1667cac9eae650e934dca501fc745245420aa8b68f938bc63383a9d92983da readme180-check.txt
