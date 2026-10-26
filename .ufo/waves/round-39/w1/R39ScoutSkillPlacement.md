DONE — a table inside a `- **` list item does not break command A; append the new block as rule 18 after `SKILL.md:314` (the last non-blank craft line), indented 2 spaces, with every citation resolvable.

# R39ScoutSkillPlacement — R39-C2 insertion point and command-A behaviour

Base `a2f64e1da78afcf8cc39287106604dbcc270844c` (lane HEAD equals it; only `.ufo/waves/round-39/` and `plans/round-39-claims.md` are untracked). Read-only scout; nothing in the lane was edited.

## 1. Observed facts

**Depth count at base.** Command A is `SCORECARD.md:92-124`, run verbatim with REV = base from the lane (`python3 command-A.py a2f64e1da78afcf8cc39287106604dbcc270844c`, exit 0, copy in `artifacts/R39ScoutSkillPlacement/command-A.py`):

`{"citation_resolved_rules": 17, "rule_blocks": 17, "depth_score": 10.0, "mapped": 126, "knowledge_files": 126, "coverage_score": 10.0, "missing": [], "dangling": []}`

So depth is **17/17 rule blocks resolved**, and coverage is 126/126.

**Craft section layout at base.**
- Heading is `SKILL.md:81`; next `## ` is `:319` (`## Config custody for live-probe rounds (SOP)`).
- Lines 315-318 are blank, and the last non-blank craft line is **314**.
- The 17 `^- \*\*` rule starts are at lines 86, 108, 118, 137, 151, 162, 170, 175, 187, 196, 207, 219, 233, 240, 256, 279 and 293.
- Rule 17 (evidence-id field sensitivity) spans 293-314.
- The craft section has no tables, no fences, and no column-0 `## ` or `|` lines.

**How command A splits.**
- It takes `get('SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]`.
- It then runs `re.split(r'(?m)^- \*\*', craft)[1:]`.
- A rule counts as resolved only if it has at least one match of `corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?` and **all** matches resolve (file exists, `1 <= start <= end <= linecount`).
- Matches are found anywhere in the block text, including table cells. Bare file citations check line 1 only. `.ufo/...` citations are ignored.

**Fixture test.** I built a scratch git fixture (`git -C "$D" rev-parse --show-toplevel` equalled `$D` before the first commit) holding `corpus/README.md`, `corpus/knowledge/*.md` and `SKILL.md` copied from the lane. Each variant is a detached commit off the base fixture commit. Full matrix: `artifacts/R39ScoutSkillPlacement/variants.md`.

| variant | result (rules / resolved / depth) |
|---|---|
| base fixture | 17 / 17 / 10.0 |
| bullet + blank + 2-space-indented table, cites in cells and prose, after line 314 | 18 / 18 / 10.0 |
| column-0 table after the bullet | 18 / 18 / 10.0 |
| citations only inside table cells | 18 / 18 / 10.0 |
| one table cell cites `:40-51` on a 50-line file | 18 / **17** / 9.44 |
| table with no `corpus/knowledge/` citation | 18 / **17** / 9.44 |
| `\|` escaped pipe in a cell | 18 / 18 / 10.0 |
| block inserted mid-section before rule 17 | 18 / 18 / 10.0 |
| col-0 line `## fenced` inside the block, then a second bullet | **18 instead of 19**; section truncated at the `## ` line |
| a table continuation line starting `- **` at col 0 | **19**, 18 resolved, so the extra bullet counts as a rule |

**Rendering.** markdown-it (commonmark + table) renders the 2-space-indented table inside the `- **` item as `<ul><li><p>…</p><table>…</table><p>…</p></li>`, so it stays in the list item. A column-0 table also renders, but it closes the list; command A counts it either way.

## 2. Recommendation (exact insertion point)

1. Insert after `SKILL.md:314`: one blank line, then the new `- **…**` bullet as rule 18. Leave the existing trailing blanks and the `## Config custody` heading after it.
   - A bold lead sentence goes on the `- **` line, followed by a blank line.
   - The table follows as 2-space-indented `  | … |` rows, so it stays inside the list item.
   - Trailing prose is also 2-space-indented.
   - Put **every** citation as `corpus/knowledge/<file>.md:<a>-<b>` in a table Source cell or in the prose. Each must resolve; one bad range drops the whole block to unresolved and depth to 17/18.
   - Cite the round-36 and round-38 entries with real ranges (215 and 50 lines now) plus any round-39 entry that exists before freeze.
2. Do not use a column-0 `## ` line (including inside fences or examples), and do not start any table continuation or sub-bullet with a column-0 `- **`. Keep `|` characters escaped inside cells.
3. Why append rather than insert mid-section:
   - The citation-drift gate (`.ufo/gates/citation-drift/pointer-table.json`) pins SKILL.md lines 246, 248, 252 and 254 (rule-14/15 text), which an earlier insertion would shift.
   - `SCORECARD.md:2059` and `LOG.md:1701` cite rule 17 as `SKILL.md:293-314`.
   - Appending leaves all of these valid.
4. Expected counts after the edit: command A **18/18 rule blocks resolved**. Block length K gives the new craft range `SKILL.md:81-(315+K)` (the blank at 315 plus K lines, with the heading still at 81).

## 3. Restatements that follow if the section grows

Any growth shifts every later SKILL.md line by the block length (K+1 including the blank separator).

**SHONEN box 1** — `SHONEN.md:6`: `SKILL.md:81-314` and "17/17 rule blocks" must become `SKILL.md:81-<new last non-blank>` and "18/18".
- The gate entry `shonen-skill-range` pins SHONEN.md line 6.
- Its needle "A mitigation claim carries its natural control" must stay inside the stated range, which it will.

**SCORECARD depth row** — `SCORECARD.md:24`: `17/17 queue-drain rule blocks` and the evidence cell `SKILL.md:81-314`.
- The round-38 `tools/round-38/c2-counter.py` checks (`O2`, `O4`, `R2`) compare these strings against command A and the craft range, so the round-39 counter will likely do the same.
- Command A stays at 10.0 only if the new block resolves; any depth row shown as 10 → 10 must be rewritten as 18/18 with the revision.

**Later-line pointers in SKILL.md that shift on any growth:**
- `SKILL.md:946` states `SKILL.md:411-412` (the `analyze`/`inspect` equal-ids sentence) and "round-26 table row at `:894`". Both would need +(K+1).
- `plans/round-39-claims.md:56` cites `SKILL.md:1231-1243` (the round-36 table, currently at 1231-1243 of the 1223+ section). It will be stale after the edit. State the post-edit lines or cite by heading.
- Other bare SKILL.md line cites into `:319-:411` sit in knowledge entries or old waves (`corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md:52` `:319`; `.ufo/gates/citation-drift/pointer-table.json` quoted entries `:371`). Those are historical pins and need no change, as the pointer-table text states.

## Tooling
No tools installed or upgraded. markdown-it-py was used only via `uv run --with markdown-it-py` (ephemeral, no persistent install).

## Limits
- I did not run the citation-drift probe itself or the round-38 c2-counter on the fixture. The pointer-table conclusions come from reading entries and the probe source.
- Rendering was checked with markdown-it commonmark + table, not GitHub's renderer.
- The fixture used only `.md` knowledge files. This matches the command-A pattern, which matches `*.md` names only.
- Scratch `/fast/scratch/hyaku/kaidoku-r39/R39ScoutSkillPlacement` is removed on finish.

Artifacts: `.ufo/waves/round-39/w1/artifacts/R39ScoutSkillPlacement/command-A.py`, `variants.md`.
