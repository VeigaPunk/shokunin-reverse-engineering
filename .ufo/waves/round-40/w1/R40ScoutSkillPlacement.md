DONE — rule block 19 goes after SKILL.md line 343 (new line 344 blank, block 19 from 345); command A (SCORECARD.md:94-122, and its mirror `command_a()` in tools/round-38/c2-counter.py) still counts a block carrying a table plus `<!-- ... -->` lines, with every citation resolving (19/19), provided no column-0 `- **` line sits inside the block. Seven self-assessment spots need restating; one is a pre-existing base mismatch.

# R40ScoutSkillPlacement — placement recon for R40-C2 / SHONEN / SCORECARD pointers

Base `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f` (`git rev-parse HEAD` in the lane = that hash). Read-only over the lane; scratch fixture repo only. No tools installed.

## 1. Current values at base (observed)

Command A, verbatim body of `SCORECARD.md:93-123` run with `python3 - fa6a8a3f…` (artifact `artifacts/R40ScoutSkillPlacement/commandA-at-base.json`):
`{"citation_resolved_rules": 18, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 128, "mapped": 128, "missing": [], "rule_blocks": 18}`

Craft section (heading `## Queue-drain craft (rounds 5-12, distilled in round 13)` at `SKILL.md:81`, next `## ` at `:348` `## Config custody for live-probe rounds (SOP)`): first-to-last-non-blank range **81-343** (`heading_range` of the r38 counter; lines 344-347 are blank). Block 18 = `SKILL.md:316-343`: prose bullet `:316-331` (the `- **SquashFS extract-firmware outcome triage (round 39).**` bullet, 2-space continuation lines), blank `:332`, marker `  <!-- sqfs-triage-table v1 -->` at `:333`, table header `:334`, rows `:336-343` (8 rows, last row `clean` at `:343`). `SKILL.md` is 1354 lines.

Round-38 self-assessment counter at base (`python3 -I -B tools/round-38/c2-counter.py --root . --rev fa6a8a3f… --base fa6a8a3f… --json-out …`, exit **1**; `artifacts/R40ScoutSkillPlacement/r38-c2-counter-at-base.json`): `mismatches 1`, `guards_ok true`, `unresolved []`, the one mismatch is `R1 depth row craft range` stated `[316, 343]`, observed `[81, 343]`. Cause: the check takes the FIRST `SKILL.md:a-b` token in the SCORECARD depth row (`SCORECARD.md:24`), and that row names `SKILL.md:316-343` (`new block 18 at …`) before `SKILL.md:81-343` (craft range, later in the cell). SHONEN box 1 (`SHONEN.md:6`) lists `81-343` first, so R2 passes. This is a standing defect at base, not caused by round 40; any round-40 restatement of the depth row should put `SKILL.md:81-<end>` before any block-range token, or the same counter reads 1 mismatch again.

## 2. Recommended insertion point for rule block 19

- Insert **after `SKILL.md:343`** (`PUT >343` in the edit tool): first body line blank (keeps one blank between blocks; the existing blanks `:344-347` follow block 19), then block 19. Block 18 stays at `:316-343` byte-identical and at identical line numbers (the insert is below it), so the round-39 held-out counter's table-bytes comparison (`tools/round-39/c2-counter.py:205-206` compares SKILL at rev vs freeze) and its v1-marker lookup are untouched.
- Mirror block 18's layout: col-0 `- **<title> (round 40).**` bullet with 2-space continuation lines containing the `corpus/knowledge/<r40 entry>.md:<a>-<b>` citations; blank; 2-space-indented `  <!-- sqfs-triage-table v2 -->`; the table directly after (the v1 interpreter `tools/round-39/sqfs-triage.py:481-488` finds the marker, then the first `|` line after it, and reads until the first non-`|` line; the v2 interpreter should do the same keyed on the `v2` marker).
- Do NOT write the literal `<!-- sqfs-triage-table v1 -->` in block 19 prose (the v1 interpreter takes the first line containing it); do not write the literal v2 marker anywhere before the real one (same first-match rule). Block 18's marker is not a substring of the v2 marker and vice versa.
- Craft range after insertion = 81 to the last non-blank line of block 19 (insert size N lines + 1 leading blank → end = 343 + 1 + N where N counts block-19 lines up to its last table row). `## Config custody…` shifts from `:348` by the inserted line count.

## 3. Command A on a scratch copy with a dummy block 19 (observed)

Fixture: `git init` in `$S/fx.*`, copy of lane `SKILL.md`, `SHONEN.md`, `SCORECARD.md`, `PROVINCE.md`, `corpus/README.md`, `corpus/knowledge/` at base, one commit; one commit per variant. Driver `command-a-driver.py` imports `command_a()` + `heading_range()` from `tools/round-38/c2-counter.py` (the code is identical in logic to the SCORECARD heredoc: same split on `## Queue-drain craft `, same `(?m)^- \*\*` rule split, same citation regex; the heredoc itself was run on the real base above, the same 18/18). Dummy block generator `mk-dummy-block19.py`. Results (artifact `dummy-block19-command-a.txt`):

| variant (inserted after `:343`) | resolved/rule_blocks | craft range |
|---|---|---|
| base (no block 19) | 18/18 | 81-343 |
| **ok**: col-0 `- **…v2 (round 40).**` bullet + citation `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md:11-28`, blank, `  <!-- sqfs-triage-table v2 -->`, `  <!-- action-vocabulary: … -->`, 12-column table | **19/19** | 81-352 |
| bullets: same plus 2-space-indented `  - **action**` list items inside the block | 19/19 | 81-356 |
| marker and action comments at column 0 (still after the cited bullet) | 19/19 | 81-352 |
| badrange: citation `:11-9999` | 18/19 | 81-352 |
| nocite: block with no `corpus/knowledge/` citation | 18/19 | 81-351 |
| col0: a column-0 `- **rerun-with-dependency** …` line inside the block | 19/20 (extra uncited "rule block") | 81-354 |

Also: the v1 interpreter `python3 tools/round-39/sqfs-triage.py --skill <SKILL with v2 block> --table-only` still prints marker line 333, table line 334, 8 rules, exit 0 (checked on the base file and the variant with a v2 block).

Consequences for block 19: (a) at least one resolving `corpus/knowledge/<lowercase-stem>.md[:a-b]` citation in the bullet, range inside the cited file at the measured revision (so the r40 knowledge entry must be committed, mapped in `corpus/README.md` `## Coverage map`, which raises command A's `knowledge_files`/`mapped` from 128 — coverage stays 10 only if the new entry is mapped); (b) any list of the closed action vocabulary must be indented or inside the `<!-- -->` comment, never a column-0 `- **` line (that makes 19/20 → depth 9.5); (c) no column-0 `## ` heading inside the block (it would end the craft section); `### ` is not a stop; (d) `S###` source ids and `knowledge entry :a-b` words in table cells do not count as citations (pattern needs the `corpus/knowledge/` prefix), matching block 18's own cells.

## 4. Self-assessment lines to restate when block 19 lands (SHONEN/SCORECARD/registry)

Pointers that the round-38 counter (the only lane counter that cross-checks them: O1-O4, R1-R3) reads, plus the registry:
1. `SHONEN.md:6` (box 1 "SKILL.md contains real decision tables…"): `SKILL.md:81-343` → `81-<new end>`, `18/18 rule blocks` → `19/19`, the "rule block 18 is…" sentence gains block 19 / marker v2; keep `SKILL.md:81-…` as the first `SKILL.md:a-b` token (R2).
2. `SCORECARD.md:24` (`## Owned axes`, depth row): `18/18 queue-drain rule blocks` → `19/19` (O2 regex `(\d+)/(\d+) queue-drain rule blocks`), `citation_resolved_rules 18` → `19`, new measured-revision hash, `SKILL.md:316-343` token supplemented by block 19's range; fix the standing R1 mismatch by putting `SKILL.md:81-<end>` first in the cell.
3. `SCORECARD.md:23` (coverage row): `128/128 knowledge files mapped` → new count after the round-40 knowledge entries (O1 regex `(\d+)/(\d+) knowledge files mapped`).
4. `SCORECARD.md:629` (`## Capabilities` row "executable SquashFS `extract-firmware` outcome triage", `## Capabilities` at `:615`): keep as the round-39 row (still true for v1; keyed by first cell, which must stay unique); add a new row for the v2 table (new first cell). The round-39 row's "no domain guard" limit is superseded by R39-CL1 only through the new row.
5. `SHONEN.md:10` (box 3, `asserted: round 39's triage table is executed…`, bounded to ten generator classes, no domain guard): add the round-40 v2 sentence; do not delete the round-39 numbers (the r38 pointers guard "not fewer pointers than base").
6. SKILL round-39 instrument registry (`### Round-35/37/38/39 instrument registry`, `SKILL.md:1328`; table rows `:1332-1354`; the `tools/round-39/sqfs-triage.py` row at `:1351` states "reads only the SKILL craft triage table" and no domain guard; `heldout-gen.py :1352`, `c2-counter.py :1353`): recommended action is to leave these rows and add a new `### Round-40 instrument registry` section appended at the end of `SKILL.md` (after the last row, currently `:1354`), because the registry has no line-range self-assertion in SHONEN/SCORECARD, and appending keeps the section order. Registry rows needed for the new tools: `tools/round-40/sqfs-triage-v2.py` (gate, interpreter), the C2 held-out generator, the C2 counter, and for C1 the counter/oracle/harness (per the round-36/39 row schema: tool, gate or probe, verdict map, selftest command, pinned-value path, write scope, owner).
7. Round-39 history that cites later SKILL lines and WILL drift by +N when block 19 is inserted above them (history, not live surfaces; none is checked by command A or the r38 counter): `corpus/lessons/round-39-verifier-spotcheck.md:27` and `:153` (`SKILL.md:1346,1351,1353,1354`), `corpus/lessons/round-35.md:65-66` (`SKILL.md:1213-1219`, `:1209`), `plans/round-39-claims.md:93` (`SKILL.md:1260-1271`); in-file pointers `SKILL.md:975` (`SKILL.md:411-412` and `:894`, already pointing at the wrong lines at base: `:411-412` is Config-section prose and `:894` is a "`fafdd283`" line). Leave them, or cite `<hash>:SKILL.md:…`; do not edit lessons (lane convention).
Not needing restatement: `PROVINCE.md:97-125` / `:378-384` (C1 surface), `SCORECARD.md:3424-3426` and `SHONEN.md` history pointers `SKILL.md:316-343`/`:81-343` (round-39 historical record at the cited commit), `corpus/README.md:163` (`SKILL.md:81-195`, stale since round 13 — not checked).

Freeze-integrity note (draft C2): `tools/round-39/c2-counter.py` compares the table bytes at rev vs freeze, not the whole `SKILL.md`; the post-landing registry/SHONEN edits and a later appended `### Round-40 instrument registry` therefore do not trip a frozen-path rule as long as the v2 table lines are untouched. If the draft's freeze path for C2 is "SKILL.md" as a whole, a later registry insertion would block the score (exit 2 `frozen_path_changed`, as the freeze-integrity rule is written); the freeze should name the v2 table block (marker through last row), not the file. [INFERENCE for the draft's wording; the round-39 counter code is what was observed.]

## 5. Evidence and limits

- Commands: `git rev-parse HEAD`; `sed -n` / `grep -n` over `SKILL.md`, `SCORECARD.md`, `SHONEN.md`; command A heredoc run on the real base (exit 0); `tools/round-38/c2-counter.py` at base (exit 1, one mismatch above); fixture variants via `mk-dummy-block19.py` + `command-a-driver.py` (artifacts dir, scratch removed).
- A full r38 counter run on the fixture was not meaningful (fixture lacked tools/.ufo paths: 46 spurious unresolved pointers) and is not cited; only command A and `heading_range` were taken from the fixture.
- Not run: any REA/unblob/sasquatch, any carrier; no edits outside this report and its artifacts directory.
- Artifacts: `commandA-at-base.json`, `r38-c2-counter-at-base.json`, `dummy-block19-command-a.txt`, `command-a-driver.py`, `mk-dummy-block19.py` (under `.ufo/waves/round-40/w1/artifacts/R40ScoutSkillPlacement/`).
