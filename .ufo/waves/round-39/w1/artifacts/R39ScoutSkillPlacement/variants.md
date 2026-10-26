# Command-A variant matrix (fixture repo; SKILL.md = lane base a2f64e1 + one inserted block after line 314)
Fixture: scratch git repo with corpus/README.md, corpus/knowledge/*.md, SKILL.md copied from the lane; every variant a detached commit off the base fixture commit; `python3 command-A.py <rev>` run with cwd = fixture. (scratch removed; this table is the record.)
ok1 = corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md:1-20 (215 lines); ok2 = ...r38-sasquatch-be-squashfs-recursion.md:1-50 (50 lines); bad = ...r38...:40-51.
| variant | block shape | rule_blocks | resolved | depth |
|---|---|---|---|---|
| base (fixture and lane a2f64e1) | none | 17 | 17 | 10.0 |
| V1 | `- **bullet**` + blank + 2-space-indented table (cites in two cells) + trailing prose, after line 314 | 18 | 18 | 10.0 |
| V2 | bullet, then column-0 table | 18 | 18 | 10.0 |
| V3 | citations only in table cells | 18 | 18 | 10.0 |
| V4 | one cell cites `:40-51` on a 50-line file | 18 | 17 | 9.44 |
| V5 | table, no `corpus/knowledge/` citation anywhere | 18 | 17 | 9.44 |
| V6 | indented fence holding `## x` at end | 18 | 18 | 10.0 |
| V6b | col-0 `## fenced` line inside block, followed by a second bullet | 18 (expected 19) | - | section truncated |
| V7 | table continuation line starting `- **` at col 0 | 19 | 18 | 9.47 |
| V8 | block inserted before rule 17 (line 292) | 18 | 18 | 10.0 |
| V9 | `\|`-escaped pipe in a cell | 18 | 18 | 10.0 |
