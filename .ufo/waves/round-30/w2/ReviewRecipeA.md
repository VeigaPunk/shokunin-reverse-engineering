# ReviewRecipeA — round 30, wave 2

Seat: `KaidokuR30.ReviewRecipeA` (reviewer). Attacked: SCORECARD recipe A (coverage map and depth proxy) at the lane base and the measured revision, and the lane statement at `SCORECARD.md:3215` (HEAD `3502b94c`): "Knowledge files 114 → 116 (recipe A at `92b1dd2d`: mapped 116/116, depth 17/17 rule blocks), both new entries in the coverage map and knowledge index."

**Verdict: holds.** At the measured revision 116/116 knowledge files are mapped and 17/17 rule blocks resolve their citations. At the base the numbers are 114/114 and 17/17. Nothing is missing and nothing dangles at either revision. (observation)

## Method

I took recipe A from `SCORECARD.md` `## Measurement recipes` **A** and extracted it unchanged from the worktree with awk, saving it as a scratch script. It reads only Git objects (`git ls-tree`, `git show`). I ran it from the lane root with `REV=<rev> timeout 300 bash recipeA.sh`. Nothing in the lane was mutated, no REA run was made, and no carrier or mutant was touched.

## Outputs

Base `d210fb8f`. Run at 2026-10-23T03:12:21Z, exit 0, stderr empty:

```json
{"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 114, "mapped": 114, "missing": [], "revision": "d210fb8f", "rule_blocks": 17}
```

Measured revision `92b1dd2ddc119fda89a611ba515bdf6cfe906f76`. Run at 2026-10-23T03:12:21Z, exit 0, stderr empty:

```json
{"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 116, "mapped": 116, "missing": [], "revision": "92b1dd2ddc119fda89a611ba515bdf6cfe906f76", "rule_blocks": 17}
```

Extra check at HEAD `3502b94c5b93d86c5d67866035fd150899456295`, the commit that carries the round-30 SCORECARD section. Run at 2026-10-23T03:13:10Z, exit 0. The output matches the measured revision (116/116, 17/17, missing `[]`, dangling `[]`). Running `git diff --stat 92b1dd2d HEAD -- corpus/knowledge corpus/README.md SKILL.md` prints nothing, so the inputs recipe A reads did not change between the two commits. (observation)

## Supporting checks

- **The +2 knowledge files are exactly the two round-30 entries** (observation). `git diff --name-status d210fb8f 92b1dd2d -- corpus/knowledge corpus/README.md SKILL.md` shows:
  - added: `corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` and `…-r30-rust-auditable-refusals.md`
  - modified: `corpus/README.md`, `SKILL.md`, `2026-10-16-l7-02-inspect-rust-binary.md` and `2026-10-22-r29-evm-fresh-selector-naming.md`
- **Both new entries are in the coverage map** (observation). At `92b1dd2d`, `corpus/README.md` has `## Coverage map` at line 11 and `## Knowledge` at line 84. Coverage-map rows 81–82 hold `` `2026-10-23-r30-rust-auditable-positive` `` and `` `2026-10-23-r30-rust-auditable-refusals` ``. Recipe A's map section is bounded by the next `\n## `, so it stops at line 84.
- **Both new entries are in the knowledge index** (observation). They appear at `corpus/README.md:179-180` (`## Knowledge`, which runs from line 84 to `## Lessons` at line 182). This confirms the "coverage map and knowledge index" clause in `SCORECARD.md:3215`.
- **The SCORECARD statement is not in the measured revision itself** (observation). `git show 92b1dd2d:SCORECARD.md | wc -l` gives 3203, and that revision has no round-30 section. The statement `SCORECARD.md:3215` first lands in `3502b94c`, which is the only commit in `92b1dd2d..HEAD`. The statement cites recipe A *at* `92b1dd2d`, and that is what I recounted, so this is not a defect.

## Residual risk

1. **The depth proxy does not cover round 30's new SKILL content** (observation, with an inference about scope). Recipe A counts `- **` blocks only inside `## Queue-drain craft ` (`SKILL.md:81-318` at `92b1dd2d`). The round-30 SKILL addition is a separate section, `## Rust dependency metadata (\`inspect-rust-binary\`) — round 30` at `SKILL.md:966`. It came in as one diff hunk, `@@ -964,0 +965,41 @@`. So the 17/17 is unchanged from the base by construction, and it says nothing about whether the new decision table cites anything correctly. [INFERENCE] Read 17/17 as "the old craft rules still resolve", not as depth evidence for round 30.
2. **"Mapped" is a token test** (observation from the recipe code). It means a `2026-10-\d{2}-[a-z0-9-]+` token appears in the coverage-map section. It does not check that the row's verdict text is correct. The text of rows 81–82 is the subject of other seats' reviews, not this recount.
3. **Citation checks stop at line ranges** (observation from the recipe code). A citation counts as resolved if the cited file exists and the line range lies inside it. The recipe does not check that the cited lines support the rule.

## Verification gaps

None in scope. Both requested revisions were recounted live. No tool was installed or updated.

## Artifacts

All under `/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReviewRecipeA/`:

| file | sha256 |
|---|---|
| `recipeA.sh` (recipe A, extracted unchanged) | `e6bb76da991031b98ce51ce6e3653904ae9156db0e6cfd9f066a9d2dd48b3247` |
| `out-d210fb8f.json` | `4d0e64dbef49684d8b0721d06e29f29821010269eebb29196e57c2371690a852` |
| `out-92b1dd2ddc119fda89a611ba515bdf6cfe906f76.json` | `afc5e1ad5b227108cb5b0322528229171dde466b903d3e8bc7a9811a6827e790` |
| `out-3502b94c.json` | `cf3b2d94cc9a7521bec19353c837222f63c404dd66639058cb1cf8741057764c` |
| `err-d210fb8f.txt`, `err-92b1dd2d….txt` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
