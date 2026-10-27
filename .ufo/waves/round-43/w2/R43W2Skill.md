# R43W2Skill — SKILL status and region audit

## Result

No actionable discrepancy found in this scoped attack. At frozen round-43 `FREEZE` and measured `REV`, both R42-V3 status paragraphs are present immediately before their respective v3/v4 markers, the v3/v4 extracted regions are byte-identical to the round-42 anchor, and command A's rule/citation counts are unchanged between FREEZE and REV: 21/21 resolved rules, 21 rule blocks, 78 knowledge citation occurrences. The `SKILL.md` blob is identical at FREEZE and REV. At the anchor, command A was 20/21 (not 21/21); this is the expected pre-freeze state, not a post-freeze drift.

Axes: coverage (the status and table regions were checked at all three revisions), calibration (the count is recomputed from immutable Git objects using SCORECARD's exact recipe), depth (both table regions and placement are checked independently).

## Revisions and measurements

- Anchor: `d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b` (round-42 freeze).
- FREEZE: `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`.
- REV: `5856614ac4bf7f2363bbcd1956644474a82108e5` (lane tip observed during this review; descendant of FREEZE).

Extracted each region from the marker line through the line before the next heading, bold rule bullet, or sqfs table marker, trimming terminal newlines. Exact bytes and SHA-256:

| Revision | v3 region bytes / lines | v3 SHA-256 | v4 region bytes / lines | v4 SHA-256 | whole SKILL.md SHA-256 |
|---|---:|---|---:|---|---|
| Anchor | 9,659 / 16 | `56cf703d1c51130a61cbcfc1db22013575e75e6e82dcf0a61e2922e3106cfe44` | 13,856 / 19 | `92540586b8c03dcde511652c0d76ba93cbde8e5f4e79e0b94509192c19b101f2` | `28234fa95c91a9cc97f3f83e33558ec75b179bd49eab692ae9a82bf67c0a6e6f` |
| FREEZE | 9,659 / 16 | `56cf703d1c51130a61cbcfc1db22013575e75e6e82dcf0a61e2922e3106cfe44` | 13,856 / 19 | `92540586b8c03dcde511652c0d76ba93cbde8e5f4e79e0b94509192c19b101f2` | `32fb1a265da04c07c958cf04a4f4552bdec94fb527ef863cf1e08e313c03b724` |
| REV | 9,659 / 16 | `56cf703d1c51130a61cbcfc1db22013575e75e6e82dcf0a61e2922e3106cfe44` | 13,856 / 19 | `92540586b8c03dcde511652c0d76ba93cbde8e5f4e79e0b94509192c19b101f2` | `32fb1a265da04c07c958cf04a4f4552bdec94fb527ef863cf1e08e313c03b724` |

At FREEZE and REV, status prose is at lines 438 and 523, immediately preceding the markers at 440 and 525 respectively; intervening lines are indented continuation prose/blank lines, not a column-zero `- **` rule bullet. v3 says it is unscored after the R41 counter mismatch and superseded by v4; v4 says the 78/78 evaluator agreement remained unscored because R42 stopped on `observed_features_match_declared`, and identifies the round-43 rescore. At the anchor, neither status paragraph exists; both are freeze additions. This matches the frozen plan's expected marker/status placement. The full SKILL blob is equal between FREEZE and REV.

## Command A counts (SCORECARD.md recipe, evaluated against immutable revisions)

| Revision | Knowledge files | Mapped | Citation-resolved rules | Rule blocks | `corpus/knowledge/*.md` citation occurrences | Unresolved rules |
|---|---:|---:|---:|---:|---:|---|
| Anchor | 134 | 134 | 20 | 21 | 77 | none |
| FREEZE | 136 | 135 | 21 | 21 | 78 | none |
| REV | 137 | 136 | 21 | 21 | 78 | none |

Thus command A is 21/21 at FREEZE and REV, with neither rule-block count nor citation-occurrence count shifting after freeze. At anchor it is 20/21; the two new knowledge-file/map state changes between anchor and freeze mean that pre-freeze count is not the relevant post-freeze invariant. The `rule_block` implementation in `tools/round-43/c1-counter.py` starts at the marker and stops at the next heading/bold rule bullet/table marker; the status lines are outside those extracted regions. The independent command-A recipe counts all column-zero `- **` lines in the craft section, so the two indented status paragraphs do not create rule blocks.

## Evidence, commands, and limitations

Read first: frozen plan `plans/round-43-claims.md`, SHA-256 `0326dff974d48df575486256dbd5a0b36593dbc84155d0d40560b64d3c20d83e`. Also read SCORECARD command-A recipe (file SHA-256 `d7530b51b35e60d4324c2ec4742babcb378e3c1cd0910ef0bc95c4ebc5edf716`), C1 counter `tools/round-43/c1-counter.py` (`3a23e93ee95f4b0d69a2f4d03ed2592c9f0b81dbb6188cb6818a18a8f4f33c79`), committed score `.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json` (`13a495dbb6862d6cfbdd1f41e4a09460740f86bf93e8bb08e313b06d92b8a55c`), and current `SKILL.md` (`32fb1a265da04c07c958cf04a4f4552bdec94fb527ef863cf1e08e313c03b724`). Hashes above for historical revisions came from `git show <REV>:SKILL.md` bytes.

Commands/evidence:
- `git -C <lane> log --oneline -8` and `git -C <lane> rev-parse HEAD`: tip was `5856614ac4bf7f2363bbcd1956644474a82108e5`; exit 0.
- Read-only Python computation via `git show`/`git ls-tree` reproduced SCORECARD.md's command-A parsing and citation-resolution recipe at anchor/FREEZE/REV; exit 0. Output is the table above; no unresolved rule indexes at any revision.
- Read-only Python extraction/hash over immutable `git show` bytes for each marker, plus status paragraph/marker line scan; exit 0. Output is the hashes, lengths, and line positions above.
- Disk guard: `df -h /home/vgpnk/Projects/shokunin /fast/scratch` showed 590G and 370G available respectively. No scratch was created; no installation, extractor, tests, formatter, or lint run.

LSP status/tool was unavailable in this seat's mounted tools, so the required references/definition/diagnostics route could not be used; text inspection was only literal fallback and is not semantic proof. The conclusions above rely on immutable-byte extraction and the frozen command-A recipe, not grep as semantic evidence. No REA/unblob or published firmware inputs were touched. No artifacts beyond this report were needed.

Report: `.ufo/waves/round-43/w2/R43W2Skill.md`
