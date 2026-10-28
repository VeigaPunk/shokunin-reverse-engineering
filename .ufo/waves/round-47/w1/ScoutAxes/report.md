# ScoutAxes — Owned axes at the round-47 freeze

Revision measured: `5017e1f7299c3a812e87e7950148f54313dd279e` (`plans/round-47-claims.md` + `tools/round-47/`). `SCORECARD.md` blob `1a296cdc8aec809146d0f3bd3568c448cacc3fb6`. Frozen `tools/round-47/record.py` blob `1f8e792898fd8d28ae4e63668eaebe07fa7a788d`.

The worktree copies of `SCORECARD.md` and `tools/round-47/record.py` were dirty. Nothing below reads those worktree bytes. No packages installed.

Receipts: `.ufo/waves/round-47/w1/ScoutAxes/`.

## What the current table binds

`## Owned axes` is `SCORECARD.md:19-32` at the freeze. The coverage row is line 23. The depth row is line 24. `tools/round-47/record.py` `collect_axes` keeps only the first `\d+/\d+` after the axis name (`FRAC.search` on the remainder of the row). That is the leading fraction. Later `N/N` tokens in the same cell are history and are not atoms.

Score cells are not slash-fractions: coverage `9.72 → 10.0`, depth `10 → 10`.

### Coverage row (exact)

Unicode length 2368 (UTF-8 2372 bytes). Line sha256 `81e06b81b26a7afa6cfbed1de0ca97c19a9809f41e2e9733f1244b2cc79a9287`. File-with-newline sha256 `564d266e94478e0df817b5432b6ba0908a53e0d38b4457114b9ffd6a9666a1bb` (`coverage-row.txt`).

```
| coverage | 9.72 → 10.0 | 133/133 knowledge files mapped after the round-41 landing (three entries added and mapped: `corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md`, `corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md`, `corpus/knowledge/2026-10-26-binwalk-v3-unit-of-work.md`; command A at `e1c83313`, `missing []`, `dangling []`; R41-C1 moved genuine AVM-layout BE SquashFS v4 Frontier → Core, `## Round 41` below); 130/130 knowledge files mapped after the round-40 landing (two entries added and mapped: `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`, `corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md`; command A at `4d62ee5a`, `missing []`, `dangling []`, `.ufo/waves/round-40/w2/R40W2DepthCount.md`); 128/128 after the round-39 landing (two entries added and mapped: `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md`, `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md`; 126/126 after the round-38 landing, which added `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`, `corpus/knowledge/2026-10-26-unblob-format-matrix.md`; 124/124 after the round-36 landing, which added `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`, `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`; 122/122 at `cab59f221fe19726b5692bfa4d9a9679e96b8a73`, round 36 recount with the command-A observable in `tools/round-36/c2-counter.py`; 116/116 at `c369242fee9f559f895e3f7956b1242076c7b1be`, round 31; 109/109 at `ebe2cb4a`, round 26); index integrity only, **not** fraction of the REA domain held. History: 78/78 at `3395b6d` (luna-round-7; the row kept that revision until round 26), 107/107 at `7ef837a473ae65d924b9ea34e7748f722a6cd7d5`, 108/108 after the round-25 EVM selector-naming entry | `corpus/README.md` `## Coverage map`; command A (`tools/round-38/c2-counter.py`); measured after the round-39 landing (command A at `52b0eb2907c704ed5f184c47b14c723208e5cbbc`, `missing []`, `dangling []`) and after the round-38 landing (`plans/round-38-claims.md` R38-C2) and after the round-36 landing (round 36, `plans/round-36-claims.md` R36-C2); `cab59f221fe19726b5692bfa4d9a9679e96b8a73`; earlier `c369242fee9f559f895e3f7956b1242076c7b1be` (round 31, `.ufo/waves/round-31/w1/ScribeScorecardRows.md`); baseline `a79945c4` | luna-round-1 + luna-round-7; count refreshed rounds 25, 26, 31, 36, 38, 39 and 40 |
```

Leading fraction: **133/133**. Every slash-fraction in the cell, in order:

| # | fraction | where it sits |
|---|---|---|
| 0 | 133/133 | leading; round-41 landing; command A at `e1c83313` |
| 1 | 130/130 | round-40 landing; command A at `4d62ee5a` |
| 2 | 128/128 | round-39 landing |
| 3 | 126/126 | round-38 landing |
| 4 | 124/124 | round-36 landing |
| 5 | 122/122 | `cab59f221fe19726b5692bfa4d9a9679e96b8a73`, round-36 recount |
| 6 | 116/116 | `c369242fee9f559f895e3f7956b1242076c7b1be`, round 31 |
| 7 | 109/109 | `ebe2cb4a`, round 26 |
| 8 | 78/78 | `3395b6d`, luna-round-7 |
| 9 | 107/107 | `7ef837a473ae65d924b9ea34e7748f722a6cd7d5` |
| 10 | 108/108 | after the round-25 EVM selector-naming entry |

Not in this cell: `135/135`, `137/137`, `138/138`. Those appear only in later `## Round N` prose (rounds 42–46 and the round-44 correction notes), which `collect_axes` does not read.

### Depth row (exact)

Unicode length 1613 (UTF-8 1617 bytes). Line sha256 `b99cc56d17622b1aba155bdba3f9bb4ee662d143d05329228419c3c3ee4a0692`. File-with-newline sha256 `8c4ccbf1732859cc80afcfd0b42ce14511e2a3a8c8f97954ddc20c3bfea37a5e` (`depth-row.txt`).

```
| depth | 10 → 10 | 20/20 queue-drain rule blocks have resolvable file/range citations at `e1c83313f33a3d97edbd8fef402db2d06172fcdc` (round 41, command A, new block 20 at `SKILL.md:387-449` with table v3; craft section `SKILL.md:81-449`; R41-C2 itself stopped, `## Round 41`); 19/19 queue-drain rule blocks have resolvable file/range citations at `4d62ee5a86b4692a13f682b29ed7975e8d7e5326` (round 40, command A, new block 19 at `SKILL.md:348-375` with table v2; `.ufo/waves/round-40/w2/R40W2DepthCount.md`); 18/18 at `52b0eb2907c704ed5f184c47b14c723208e5cbbc` (round 39, command A, `citation_resolved_rules 18`, new block 18 at `SKILL.md:316-343` with its citations resolving; 17/17 at `c369242fee9f559f895e3f7956b1242076c7b1be`, round 31; also 17/17 at `ebe2cb4a`, round 26). History: 9/9 at `638fb211` (luna-round-3); rule blocks grew from 9 to 17 in eight commits from `58116aa1` to `4072ebb3` (2026-10-18 and 2026-10-19), and the row kept 9/9 until round 25 added a recount at `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76`. **not** semantic correctness, generality, or fresh execution — the r3 semantic contradiction removal is measured by the contradiction census, not this proxy | craft section `SKILL.md:81-343` (heading line 81, last non-blank line 343 at `52b0eb29`; the baseline range was `SKILL.md:77-191` at `a79945c4`); command A; measured `52b0eb2907c704ed5f184c47b14c723208e5cbbc` (round 39; prior recount `c369242fee9f559f895e3f7956b1242076c7b1be`, round 31); baseline `a79945c4` | r1 measurement + luna-round-3; rule blocks added 2026-10-18 and 2026-10-19; count refreshed rounds 25, 26, 39 and 40 |
```

Leading fraction: **20/20**. Every slash-fraction in the cell, in order:

| # | fraction | where it sits |
|---|---|---|
| 0 | 20/20 | leading; `e1c83313f33a3d97edbd8fef402db2d06172fcdc`, round 41 |
| 1 | 19/19 | `4d62ee5a86b4692a13f682b29ed7975e8d7e5326`, round 40 |
| 2 | 18/18 | `52b0eb2907c704ed5f184c47b14c723208e5cbbc`, round 39 |
| 3 | 17/17 | `c369242fee9f559f895e3f7956b1242076c7b1be`, round 31 |
| 4 | 17/17 | `ebe2cb4a`, round 26 |
| 5 | 9/9 | `638fb211`, luna-round-3 |
| 6 | 9/9 | kept until the round-25 recount at `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76` |

Not in this cell: `21/21`, `22/22`, `23/23`.

## Independent observables at the freeze

Command A is the fenced recipe under `## Measurement recipes` in the freeze `SCORECARD.md`. It was run with `REV=5017e1f7299c3a812e87e7950148f54313dd279e` from the lane repo. It reads git objects only.

Coverage observable: **138/138**. `mapped=138`, `knowledge_files=138`, `missing=[]`, `dangling=[]`, `coverage_score=10.0`. The map token set is `2026-10-\d{2}-[a-z0-9-]+` inside `corpus/README.md` `## Coverage map`, intersected with stems of `corpus/knowledge/*.md`. `ls-tree` also lists `corpus/knowledge/.gitkeep`, which is not `.md` and is not in the denominator.

Command A's citation count: **23 resolved / 23 rule blocks** (`citation_resolved_rules=23`, `rule_blocks=23`, `depth_score=10.0`). That is blocks under `## Queue-drain craft ` whose every `corpus/knowledge/<slug>.md` line-selector resolves, and which have at least one such reference. It is not a raw citation tally.

The leading cells disagree with those observables: coverage **133/133 vs 138/138**, depth **20/20 vs 23/23**.

## Frozen-counter check (same numbers, dead axes repair)

`python3 -I -B` on a scratch copy of the freeze blob `record.py` (lane `gate.py` beside it), `--rev` the freeze, `--no-battery`. Exit **1**. Axes atoms it emits:

- coverage claimed `[133, 133]`, derived `[138, 138]`
- depth claimed `[20, 20]`, derived `[23, 23]`

Those derived pairs match command A. The receipt also has two non-axes mismatches (round-45 seats claimed wave2 32 vs dispatched 36; round-46 window `<tip>` unverifiable). `corrections=0`, `failing=["mismatches 4 != 0", "corrections 0 < 2"]`. Sections read: round-45, round-46. Full JSON: `record-at-freeze.json` (sha256 `7c93ef7e37dab44c5c29ae0cf99c58df97c34ef43074104f55138fae92897218`).

**The claims' axes correction line cannot clear this.** Freeze `record.py:50`:

```python
CORR = re.compile(r"^- corrects (seats|window|path|rev) (\S+):\s*(.+)$")
```

`axes` is not in the alternation. `corrections()` only keeps lines that match `CORR`, so `corrects()`'s axes branch (`record.py:280-289`, the `<resolved>/<total>` check) is unreachable. Applied to the frozen pattern (`axes-correction-parse.stdout`, sha256 `2a38a9ec28d489ee8350fe2529bf99e1b4a250649a9b229e38605593904f5210`):

| line | matched |
|---|---|
| `- corrects axes coverage: 138/138` | no |
| `- corrects axes depth: 23/23` | no |
| `- corrects seats round-45: 2 waves, 72 seats total` | yes |
| `- corrects window round-46: empty in aaaaaaa..bbbbbbb -- SCORECARD.md` | yes |

A `## Record corrections — round 47` section that only restates 138/138 and 23/23 does not exempt the atoms and does not count toward `corrections >= 2`. Clearing the axes mismatch means changing the leading fractions on lines 23 and 24. A second `if cls == "axes"` at `record.py:292-299` is also dead (the first branch returns) and names `atom`, which `corrects()` does not bind.

**Latent definition gap, not a count gap at this rev.** Command A's citation pattern is `corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?`. `depth_pair` uses `HARD_REF` (`corpus|plans|tools`, `record.py:42`) and its docstring says it reads them exactly as command A. Per block at the freeze, both resolvers accept all 23 blocks (`diverge: []`, `per-rule-command-a-vs-hardref.json`). The printed 23/23 is command A's number. A later block whose only resolvable citations sit outside `corpus/knowledge/` would split them.

## Measurement table

| measurement | value | exit | stdout sha256 | UTC | command |
|---|---|---|---|---|---|
| coverage row, leading fraction | 133/133 (11 slash-fractions in the cell; see table) | 0 | line `81e06b81b26a7afa6cfbed1de0ca97c19a9809f41e2e9733f1244b2cc79a9287` | 2026-10-28T17:49:46Z (same shell as command A; rehash 2026-10-28T17:52:50Z) | `git show 5017e1f7299c3a812e87e7950148f54313dd279e:SCORECARD.md`, row is line 23 |
| depth row, leading fraction | 20/20 (7 slash-fractions in the cell; see table) | 0 | line `b99cc56d17622b1aba155bdba3f9bb4ee662d143d05329228419c3c3ee4a0692` | 2026-10-28T17:49:46Z (rehash 2026-10-28T17:52:50Z) | same blob, line 24 |
| command A at the freeze | mapped 138 / knowledge_files 138 / missing [] / dangling []; citation_resolved_rules 23 / rule_blocks 23 | 0 | `5016a720a07e11f1a8e009e4c29b11e1cad11e38eb8a357112094bafcde27617` (`command-a.stdout`) | 2026-10-28T17:49:46Z | SCORECARD recipe A, cwd = lane, `REV=5017e1f7299c3a812e87e7950148f54313dd279e`. Body is the fenced python under `## Measurement recipes` |
| knowledge md count, map intersection | 138 `.md`, 1 non-md (`.gitkeep`), map tokens 138, intersection 138, missing [], dangling [] | 0 | `caf6a7d6da96b54f0952a60bf0180e4d7bb4a6371c6d02822040bedb3d1b29b3` | 2026-10-28T17:52:50Z | `git -C <lane> ls-tree -r --name-only 5017e1f… -- corpus/knowledge` plus the coverage-map regex; receipt `per-rule-command-a-vs-hardref.json` |
| command A vs `HARD_REF`, per craft block | 23/23 both, diverge 0 | 0 | same `caf6a7d6…` | 2026-10-28T17:52:50Z | same receipt; command A pattern vs freeze `HARD_REF` |
| frozen `record.py --no-battery` axes atoms | claimed 133/133 and 20/20; derived 138/138 and 23/23; exit 1; 4 mismatches; 0 corrections | 1 | `7c93ef7e37dab44c5c29ae0cf99c58df97c34ef43074104f55138fae92897218` | 2026-10-28T17:51:40Z | `python3 -I -B <scratch copy of freeze record.py> --root <lane> --rev 5017e1f7299c3a812e87e7950148f54313dd279e --no-battery --json-out .ufo/waves/round-47/w1/ScoutAxes/record-at-freeze.json` |
| axes correction lexer | the two `- corrects axes …` lines do not match; seats and window lines do | 0 | `2a38a9ec28d489ee8350fe2529bf99e1b4a250649a9b229e38605593904f5210` | 2026-10-28T17:52:10Z | `CORR` copied from freeze `record.py` line 50, applied to the four lines in `axes-correction-parse.stdout` |

Not run: `record.py` battery; command A at any revision other than the freeze; a fixture repo that lands an axes correction and re-scores (the lexer result already shows the line is dropped before re-derive).
