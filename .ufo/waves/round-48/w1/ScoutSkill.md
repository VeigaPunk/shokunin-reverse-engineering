# ScoutSkill — craft block 25, house style and insertion point

Mapped `SKILL.md` `## Queue-drain craft` at freeze `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873` and re-checked at HEAD. No install. Read-only on the lane tree. Scratch `/fast/scratch/hyaku/kaidoku-r48/ScoutSkill` used to import the freeze and HEAD blobs of `tools/round-48/meanings.py`, then removed.

## Observed

`SKILL.md` blob `cb115da91fa2fd9ac87750c2b15cd4ec0a149f18` is identical at `dc73587`, at HEAD `f3a7afc42c1da2457ab0ffd1883c5bdb822f2962`, and in the worktree. Line numbers below are the freeze and the worktree.

| fact | value |
|---|---|
| section heading | line 81: `## Queue-drain craft (rounds 5-12, distilled in round 13)` |
| section span | lines 81–642 inclusive (562 lines). Next heading is line 643 `## Config custody for live-probe rounds (SOP)` |
| preamble (not a block) | lines 83–84 |
| rule blocks | **24**, counted by `tools/round-48/meanings.py` `blocks_of`: `(?m)^- \*\*` inside `craft_section` (split of `## Queue-drain craft ` up to the next `\n## `) |
| which are numbered | only the last three. Blocks 1–21 are unnumbered `- **…**` bullets (lines 86, 108, 118, 137, 151, 162, 170, 175, 187, 196, 207, 219, 233, 240, 256, 279, 293, 316, 351, 387, 457). Block 22 line 547, block 23 line 612, block 24 line 632 |
| last block today | line 632–641, title `24. An instrument's binding is an equality, not a containment, and its denominator is pinned.` |
| marker `<!-- verdict-meaning-table v1 -->` | absent (0 occurrences). Present markers in this section are `freeze-integrity-table v1` (line 583, inside block 22), `v2` (line 612, block 23 title), `exactness-table v3` (line 632, block 24 title) |

The counter does **not** require `rule_blocks == 25`. v3 requires the marker block to be the last craft block and its text after `- **` to start with `25. ` (`meanings.py` `score`, hard profile). Appending one block is what makes that true. Inserting it anywhere earlier fails `marker block is not the last craft block`. Inserting it at or after line 643 puts it outside `craft_section` and the marker counts as occurring in the file but in no craft block.

**Insertion point:** after line 641 (block 24's `  Refs:` line), before line 643. Line 642 is the blank line that already separates the section from the next heading. Keep one blank line before `## Config custody`.

## House style of blocks 23–24 (what to copy, and the one label not to copy)

Both are a single column-0 bullet, then a blank line, then a column-0 table, then a blank line, then a two-space-indented `Refs:` line. Block 23 is lines 612–630. Block 24 is lines 632–641.

Opening line, in order, all on one line:

1. `- **N. Title sentence.**` — number, period, space, sentence, period, inside the bold.
2. One space, then the marker comment, then one space, then the prose. The prose names the previous block and states the new claim in one sentence, then names the routed defects.
3. Pin sentence. Block 24 is the model (block 23 uses a bare `` `sha256:…` `` label, which the round-48 regex does **not** accept): `Interpreter pin: \`tools/round-47/exact.py\` \`interpreter_sha256:<64 hex>\`; the counter's own mutation list is pinned as \`mutations_sha256:<64 hex>\` over \`name\`, \`name\`, ….`
4. `Source S143.` at the end of block 24. The round-48 counter never reads a Source tag. Do not invent S144 — round 47's census already moved 142 → 144 (`corpus/lessons/round-47.md:98-99`). Omit the tag.

Table:

- Separator compact, no spaces in the dashes: `|---|---|---|---|` (blocks 23 and 24). Block 22's `| --- | --- |` also parses; don't use it.
- Exit cell is a bare digit. Block 24's four rows are all `1`.
- **Arm cells: copy block 24, not block 23.** Block 23 arms are prose (`presence: …`). Block 24 arms are one backticked token (`` `symbol` ``). Round 47 mistake M47-5 (`corpus/lessons/round-47.md:20`) is the first landing of block 24 failing because the arm cell carried prose. `r[2].strip("` ")` must be exactly the token.
- **Header labels: copy block 23, not block 24.** Block 23 is `| trigger | v1 hole | v2 arm | exit |`. Block 24 evolved that to `| trigger | v2 hole | v3 arm | exit |`. v3 compares the header list to exactly `["trigger", "v1 hole", "v2 arm", "exit"]` (`HEADER` in `meanings.py`). A block-24 header fails clause 2.
- Trigger cell is `ID` plus prose in the same cell (both blocks do this). The id regex is `R4[67]-CL\d+`, applied per row, and v3 requires exactly one match in that cell. Do not name the other routed id in the same trigger cell. Order of the two rows is not a clause.

Refs line: two leading spaces, each citation in backticks as `` `path:start-end` ``, gloss in parentheses after the backtick. Block 24's set is the shape. v3 (`check_refs`) requires:

- `HARD_REF` findall count ≥ 5. The pattern is `(corpus|plans|tools)/…` optional `:N` or `:N-M`.
- every cited path except `tools/round-48/meanings.py` itself has a line selector, the file exists at `--rev`, and `1 <= start <= end <= line_count`.
- path prefix is one of `corpus/lessons/`, `corpus/knowledge/`, `plans/`, `tools/round-48/`. Anything else (a URL, `QUALITY.md`, `SCORECARD.md`, `corpus/SOURCES.md`) is `unresolved`.
- the cited set includes `corpus/lessons/round-47.md` and at least one `corpus/knowledge/` entry. This is M47-6 (`corpus/lessons/round-47.md:22`): a block that cites only lessons and plans drops the depth proxy.

A `` `tools/round-48/meanings.py` `` with no `:line` is allowed (the pin line) and counts toward the findall. Do not cite any other `tools/round-48/` path without a selector. Do not start any line of the new block with `- **` — that opens another block and the marker block stops being last. Do not put a `## ` heading inside the block — `craft_section` ends at the first `\n## `.

## Pins (computed, not copied from `good_block`)

`mutations_sha256` is sha256 over each mutation's name, a newline, `inspect.getsource` of that function, and `\n---\n`, in `MUTATIONS` order (`_mut_digest`). `interpreter_sha256` is sha256 of the `tools/round-48/meanings.py` bytes at `--rev` (`score`, hard profile). No space after the colon. Lowercase hex, 64 chars. All four names must appear as substrings: `gold-meaning`, `swapped-meaning`, `duplicate-meaning`, `permuted-arm`.

| bytes | `interpreter_sha256` | `mutations_sha256` |
|---|---|---|
| freeze `dc73587` (`meanings.py` blob `c33afbad8b61604ff279202ed9b26cfa56d59d64`) | `cd4dbad884c5bd44290eb99976376920deec84b2754f5d40ad123a11b85bc70a` | `25ce025f8b2be63a5122583191cbf7588db7dc2894c869fac2ab075a84f5c1ea` |
| HEAD `f3a7afc4` (blob `2a65768ffdf26cd430298a6bf57ba91360454fc2`; worktree matches, porcelain clean) | `75fa4026cf6d7b2e580353707cbfdb97db79affab58d52ba18e6c9aae2e27079` | same `25ce025f…` |

A2 `ac02a79f` and A3 `f3a7afc4` both touch `tools/round-48/meanings.py` after `dc73587`. A3 is a one-line edit outside the four mutation bodies, so the mutation digest did not move and the interpreter digest did. Clause 6 compares the pin to the file **at `--rev`**, not at the freeze named in the prompt. A landing scored on top of current HEAD, with `tools/round-48/` left untouched, needs the HEAD interpreter pin. Recompute if another amendment lands before the `SKILL.md` edit; do not paste `cd4dbad8…` into a block that will be scored at `f3a7afc4`.

`git log --oneline dc73587..HEAD -- plans/round-48-claims.md tools/round-48/` is `f3a7afc4` (A3) then `ac02a79f` (A2). Scoring `--freeze dc73587 --rev <a rev that contains A2 or A3>` is exit 2 `frozen_path_changed` before the block is judged. That is a freeze-selection fact, not something the block text can fix.

## Template

Title is the counter's own `good_block` default. v3 only checks the `25. ` prefix; the rest is not compared. Hole sentences are that function's `GOOD_ROWS`. Exit `1` matches block 24 and `GOOD_ROWS`; v3 only checks `{0,1,2}`. Arm tokens are the frozen `EXPECTED_ARM`: `R46-CL7` → `meaning`, `R47-CL10` → `floor`. Ranges below were checked against the worktree line counts (round-47 = 120, round-46 = 102, the knowledge entry = 79, `plans/round-48-claims.md` = 180). The claims diff `dc73587..HEAD` starts at line 144, so `:44-68` and `:124-126` did not move. Re-check the ranges if those files change before landing.

```markdown
- **25. A verdict map binds meanings, and a denominator is a floor.** <!-- verdict-meaning-table v1 --> Block 24 stated what makes a check exact; this one states what makes a verdict map mean something — each row is a HIGH defect the round-47 spot-check routed, the hole that let it pass, and the arm of `tools/round-48/meanings.py` that now fails it. Interpreter pin: `tools/round-48/meanings.py` `interpreter_sha256:75fa4026cf6d7b2e580353707cbfdb97db79affab58d52ba18e6c9aae2e27079`; the counter's own mutation list is pinned as `mutations_sha256:25ce025f8b2be63a5122583191cbf7588db7dc2894c869fac2ab075a84f5c1ea` over `gold-meaning`, `swapped-meaning`, `duplicate-meaning`, `permuted-arm`.

| trigger | v1 hole | v2 arm | exit |
|---|---|---|---|
| R46-CL7 `0=banana; 1=nope; 2=whatever` scores met | the registry counter binds the digits 0/1/2, not their meanings | `meaning` | 1 |
| R47-CL10 four rows name the wrong arm and still pass | clause 5 binds membership, so the wrong arm for every routed id still passes | `floor` | 1 |

  Refs: `corpus/lessons/round-47.md:36-44` (R47-CL10 HIGH: four rows naming the wrong arm still pass), `corpus/lessons/round-47.md:103-120` (routed defects for round 48, including inherited R46-CL7), `corpus/lessons/round-46.md:89-95` (R46-CL7 HIGH: a contentless verdict map scores met), `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66` (a registered class set can hold while the surface stays shortcut-reachable), `plans/round-48-claims.md:44-68` (the R48-C1 predicate), `plans/round-48-claims.md:124-126` (the landing requirement for this block).
```

## Not checked

The registry meaning rows (clause 8) and the battery (clause 9) are outside this seat's question. This block was not inserted and the counter was not run against it. Pins were computed by importing the freeze blob and the HEAD blob; they were not produced by `meanings.py --rev`.
