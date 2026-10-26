# R41W2Harm — no-harm check across coverage / depth / calibration (round 41 landing)

**Verdict: DONE — no harm found.** Attacked: SCORECARD measurement recipes A and B at base `49096c7e6f226af0c750c4b003be58883cb6049f` vs tip-at-dispatch `7a24ff74736e84b1903db7ba01891c406a6e32a2`; diff of SCORECARD/SHONEN/PROVINCE for removed or weakened statements; `scripts/sources-census.sh validate` on the kaidoku lane. All checks run read-only on immutable git objects; no tool installed (nothing needed beyond git, python3, jq, and the checked-in bash script).

## Axes
- coverage (command A: mapped / missing / dangling / knowledge_files)
- depth (command A: rule_blocks / citation_resolved_rules)
- calibration (command B: aligned/total per stage)

## SCORECARD command A (copy of the recipe python verbatim; run from the lane repo, `git show`/`git ls-tree` read-only)

| metric | base 49096c7e | tip 7a24ff74 |
|---|---|---|
| revision | 49096c7e6f226af0c750c4b003be58883cb6049f | 7a24ff74736e84b1903db7ba01891c406a6e32a2 |
| knowledge_files | 130 | 132 |
| mapped | 130 | 132 |
| missing | [] | [] |
| dangling | [] | [] |
| rule_blocks | 19 | 20 |
| citation_resolved_rules | 19 | 20 |
| coverage_score | 10.0 | 10.0 |
| depth_score | 10.0 | 10.0 |

Both runs exit 0. Full JSON: artifacts `A-base.json`, `A-tip.json`. No regression: coverage stays 130/130 → 132/132 with zero missing/dangling; the two new knowledge entries are the round-41 pair (`corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md`, `corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md`, present at tip, absent at base); depth grows 19 → 20 blocks with all 20 citations resolving (block 20 carries `<!-- sqfs-triage-table v3 -->` at SKILL.md:434 and cites `2026-10-26-r41-sqfs-triage-v3.md`).

## SCORECARD command B (jq verbatim; rubric.json/result.json extracted at each rev via `git show`)

| stage | revision | aligned | total | score |
|---|---|---|---|---|
| baseline | 6645585873c4e66372b15687c47000abf8d91978 | 0 | 9 | 0 |
| after | c265db9bd3c0883fbaf4487f839559c85a736826 | 9 | 9 | 10 |

Identical at base and tip (jq exit 0 both); `evidence/round-1-2026-10-15/{rubric,result}.json` are byte-identical between the two revisions. Calibration unchanged: 0→10, no weakening.

## Diff SCORECARD / SHONEN / PROVINCE (base..tip)
- `SCORECARD.md`: byte-identical (empty diff; artifact `diff-SCORECARD.txt` sha256 e3b0c4… = empty).
- `SHONEN.md`: byte-identical (empty diff; artifact `diff-SHONEN.txt` sha256 e3b0c4… = empty).
- `PROVINCE.md`: exactly +14 insertions, 0 deletions (artifact `diff-PROVINCE.txt`). Added content only: a `## Round-41 additions to Core` row for the genuine AVM-layout big-endian SquashFS v4 and a `Round-41 frontier note`. The supersession is explicitly scoped — "for the genuine AVM layout only"; the round-40 `measured, not promoted` block is retained and its status explained as a counter suffix false negative (R40-CL1); LE AVM members (`hsqs`), AVM kernel images, nested sub-images below depth 1, other vendor-mangled images, and standard BE bodies with the AVM marker stripped stay Frontier. No statement removed or weakened.

## sources-census validate
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → **exit 0** (clean lane / warnings only). Output: one `kaidoku ok` row for `corpus/SOURCES.md`, plus 13 `W04` warnings (duplicate URL across scopes): S033 (ghidra PR 9348), S047 (go.dev dl JSON), S054 (developer.android.com NDK ABI guide), S062 (sigrok-cli man), S069 (tshark man), S083/S090/S092/S119/S123 (rea-agents 6.5.0 tgz), S102 (PE-format docs), S112 (unblob squashfs.py 26.6.4), S117 (unblob README 26.6.4). All are pre-existing W04 duplicates — none is a new E-code finding, and the lane registry validates clean.

## Conclusion
Coverage, depth, and calibration all measured identical-or-better at tip vs base; the only file-level changes in the three tracked docs are PROVINCE additions that scope the C1 promotion and keep the Frontier surface; census validates exit 0. The landing harms none of the owned axes.

Artifacts (sha256 over the artifact files, written to `artifacts/R41W2Harm/`): `A-base.json` 17742c4493868b44937a01dd177f94999523faff178b484afe3ae1eb79dff185, `A-tip.json` 9fbab717d6d81a36c72859d824b3810734458cccd5f28137c6881b1c4c543630, `B-base.json`/`B-tip.json` 98c0d09efa5a27dae3089a9a6511412a7f00ef0d3d755610d53a63db4b420958, `diff-PROVINCE.txt` 95090c64d7657e516c954288beb90e4b0feeec6011ad39cadf3b53f2bbe96801, `diff-SCORECARD.txt`/`diff-SHONEN.txt` e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, `census-validate.out` 24cd3aebd46438af0f7f6cb6cfdac33b9ee56f077b090e3d02b6766ff9e84c4f.
