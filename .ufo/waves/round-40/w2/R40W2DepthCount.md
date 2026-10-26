DEFECTS FOUND — command A is green at the landing (coverage 130/130 mapped, depth 19/19 rule blocks resolved, 0 missing, 0 dangling at `42c10a58` and `4d62ee5a`), but the landing leaves the lane's own axis records one round behind (rows still read 128/128 and 18/18), the wave-1 `axis-record-gate` is red at `42c10a58` and at the tip, and no round-40 instrument runs it.

Seat `R40W2DepthCount`. Attacked: the coverage/depth counting recipes at `fa6a8a3f`, `42c10a58`, `4d62ee5a` (plus the freeze `7fce3086`, the round-39 anchor `52b0eb29`, `45e89864`, `73c7bf9c`, `8b9634ed`), the accuracy of the numbers the landing's self-assessment surfaces state, and the sensitivity of the counter itself. Nothing outside `.ufo/waves/round-40/w2/R40W2DepthCount.md` and `.ufo/waves/round-40/w2/artifacts/R40W2DepthCount/` was written; no VCS mutation; no tool installed.

## 1. Recipe and how it was run

`command_a()` is **imported verbatim** from `tools/round-38/c2-counter.py` (the lane's executable mirror of SCORECARD.md command A) by file path — no re-typed copy — in `artifacts/R40W2DepthCount/depthcount.py`, with a detail pass using the same split (`## Queue-drain craft ` → next `## `), the same rule split (`(?m)^- \*\*`), the same citation pattern (`corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?`) and the same range test (`1 <= first <= last <= len(lines)`), plus the lists command A only aggregates. Independent cross-check: my base result is identical to `w1/artifacts/R40ScoutSkillPlacement/commandA-at-base.json` (`citation_resolved_rules 18, knowledge_files 128, mapped 128, rule_blocks 18`), which was produced by a heredoc copy of the SCORECARD recipe rather than by the counter.

Full command lines and raw stdout: `artifacts/R40W2DepthCount/commands.txt` §A.

## 2. Measured (command A, verbatim outputs)

| revision | rule blocks | resolved rules | citations (resolved) | knowledge files | mapped | missing | dangling |
|---|---|---|---|---|---|---|---|
| `fa6a8a3f` base | 18 | 18 | 70 (70) | 128 | 128 | 0 | 0 |
| `8b9634ed` r39 tip | 18 | 18 | — | 128 | 128 | 0 | 0 |
| `52b0eb29` r39 measured anchor | 18 | 18 | — | 128 | 128 | 0 | 0 |
| `45e89864` control receipts | 19 | 19 | — | 129 | 129 | 0 | 0 |
| `7fce3086` freeze | 19 | 19 | — | 129 | 129 | 0 | 0 |
| `73c7bf9c` C1 receipts | 19 | 19 | — | 129 | 129 | 0 | 0 |
| **`42c10a58` measured (landing)** | **19** | **19** | **76 (76)** | **130** | **130** | **0** | **0** |
| **`4d62ee5a` tip (demotion)** | **19** | **19** | **76 (76)** | **130** | **130** | **0** | **0** |

Raw:
```
{"command_a": {"knowledge_files": 128, "mapped": 128, "resolved_rules": 18, "rule_blocks": 18}, "dangling_map": 0, "mapped": 128, "missing_map": 0, "rev": "fa6a8a3f", "total": 128, "unresolved_refs": 0, "zero_citation_rules": 0}
{"command_a": {"knowledge_files": 130, "mapped": 130, "resolved_rules": 19, "rule_blocks": 19}, "dangling_map": 0, "mapped": 130, "missing_map": 0, "rev": "42c10a58", "total": 130, "unresolved_refs": 0, "zero_citation_rules": 0}
{"command_a": {"knowledge_files": 130, "mapped": 130, "resolved_rules": 19, "rule_blocks": 19}, "dangling_map": 0, "mapped": 130, "missing_map": 0, "rev": "4d62ee5a", "total": 130, "unresolved_refs": 0, "zero_citation_rules": 0}
EXIT=0
```

- **Rule blocks:** 18 at the base, 19 from the freeze onward. The delta is block 19 (`SKILL.md:348-375`, `<!-- sqfs-triage-table v2 -->` at `:361`); block 18 (`:316-346`) gained only the 3-line supersession sentence and keeps the v1 table bytes (`diff -u` of `:316-343`@`52b0eb29` vs `:316-346`@tip: one replaced line, 3 added, table rows identical).
- **Resolved citations:** every rule block has ≥1 `corpus/knowledge/` citation and every citation resolves; totals 70 → 76 (+5 in block 19, +1 in block 18's supersession sentence). `zero_citation_rules []`, `unresolved_refs []`.
- **Coverage:** missing list `[]`, dangling list `[]` at all eight revisions. Both are empty *by construction* in the honest direction: `mapped` is a set intersection with the on-disk stems, so a knowledge file without a map row shows up as *missing* (verified live, probe T1), and a map stem without a file shows up as *dangling*.
- **Credit is structural, not incidental:** of the 130 stems in the `## Coverage map` section at `42c10a58`, 84 appear in the `entries` column, 43 as the `knowledge/<stem>` subject cell, 2 in both, and 1 (`2026-10-26-r36-sasquatch-squashfs-recursion`) in the `entries` column and a state cell. No stem is credited by prose alone.

## 3. The defect: the landing did not move the axis records it lands on

The two numbers the lane scores (coverage `mapped/files`, depth `resolved/rules`) both moved at the freeze and again at the landing, and neither row was refreshed:

- `git log --oneline 7fce3086..4d62ee5a -- SCORECARD.md SHONEN.md` → **no output**. `git diff --stat fa6a8a3f 42c10a58 -- SCORECARD.md` → **no output**. Round 40 changed PROVINCE.md, corpus/README.md, one entry and the score files; never the axis records.
- At the tip, `SCORECARD.md` still reads `128/128 knowledge files mapped` and `18/18 queue-drain rule blocks … at 52b0eb29`; the tree measures **130/130** and **19/19**. `SHONEN.md:6` still asserts `SKILL.md:81-343` and `18/18`; the craft section is **81-375** and holds **19** blocks.

Instrument readings (all four revisions, `artifacts/R40W2DepthCount/c2r38-*.json`):

| rev | round-38 counter | wave-1 `axis-record-gate.py` (independent, same recipe) |
|---|---|---|
| `fa6a8a3f` base | 1 mismatch, exit 1 — `R1` only (`stated [316,343]`, `observed [81,343]`, pre-existing) | `findings=0`, exit 0 |
| `7fce3086` freeze | 5 mismatches, exit 1 | `findings=2`, exit 1 |
| `42c10a58` measured | 5 mismatches, exit 1 | `findings=2`, exit 1 |
| `4d62ee5a` tip | 5 mismatches, exit 1 | `findings=2`, exit 1 |

New at the freeze/landing (`O1` coverage `128` vs `129`/`130`, `O2` depth `18` vs `19`, `O4` SHONEN box1 `18` vs `19`, `R2` SHONEN box1 range `81-343` vs `81-375`); `R1` is inherited from the base (the depth row's first `SKILL.md:a-b` token is a block pointer, not the section range).

Calibration of the claim against this: the rows are **stale, not false**. The depth row is explicitly anchored to `52b0eb29`, where command A returns exactly `18/18`; the `128/128` coverage sentence is true at `52b0eb29` and at `8b9634ed`; `SHONEN.md:6` anchors its count to `52b0eb29` as well. So nothing here contradicts R40-C1 or R40-C2's predicates — R40-C2's `26/26` is about the v2 table, which command A only counts as one block. What is falsified is the landing's **coherence with its own measurement surface**: round 40 added the depth block and both entries, and the two living rows that the lane scores still describe round 39. This is the same class of defect round 39's wave 2 found (`w1/R40MistakeHunt.md` MH-11) and for which wave 1 built `w1/artifacts/R40MistakeHunt/axis-record-gate.py` — the gate exists, is green at the base and red at the landing and at the tip, and **no round-40 frozen instrument calls it** (`tools/round-40/c2-counter.py` and `c1-extra.py` contain zero references to `SCORECARD`/`Coverage map`/`corpus/README`; `c1-counter.py` reads `## Coverage map` only to confirm the C1 entry stem is mapped).

Wave 1 had already enumerated the exact restatements in `w1/R40ScoutSkillPlacement.md` §4 items 1-3 (SHONEN box1 → `19/19` and `81-<new end>`; depth row → `19/19`, new anchor, `citation_resolved_rules 19`; coverage row → the post-round-40 count). None of the three was made. Suggested closure edits, derived from the measurement (for the closure owner; I hold no write access to these files):
1. `SCORECARD.md` coverage row: first `N/N` → `130/130` (was true at `52b0eb29` as 128/128; state the new anchor).
2. `SCORECARD.md` depth row: `18/18` → `19/19`, `citation_resolved_rules 18` → `19`, new anchor `42c10a58`/`4d62ee5a`, and put `SKILL.md:81-375` **first** in the cell to clear the inherited `R1`, with block 18 restated as `316-346` and block 19 as `348-375` (the old `316-343` now stops 3 lines short of block 18's end).
3. `SHONEN.md:6`: `18/18` → `19/19`, `SKILL.md:81-343` → `81-375`, and name block 19 / marker v2 in the "rule block 18 is …" sentence.

## 4. Counter sensitivity (sandbox clone, fixture identity inside it only)

`artifacts/R40W2DepthCount/probe.py` on `$S/fx.*/lane` (toplevel asserted equal to the fixture dir; clone of lane HEAD `0b15c8b2`, which reproduces the tip's 130/130 and 19/19):

| probe | result | verdict |
|---|---|---|
| T0 control | 130/130, 19/19 | matches the lane tip |
| T1 delete one coverage-map row | 129/130 | map completeness is load-bearing |
| T2 strip all five line ranges in block 19 (bare filenames) | **19/19 unchanged** | **blind spot: range precision is unscored**; absent range becomes `1-1` |
| T3 range past EOF (`:46-57` of a 56-line entry) | 18/19 | out-of-file ranges caught |
| T4 append a citation-free `- **…**` block | 19/20 | uncited blocks caught |
| T5 cite a nonexistent knowledge file | 18/19 | missing files caught |

So `19/19` in §2 certifies *citation existence and in-file ranges*, not that a citation points at the passage it is used for. Block 19's five citations tile the entry body exhaustively (`11-18`, `19-26`, `27-36`, `37-45`, `46-56` of a 56-line entry whose body starts at line 9) — a specificity-free pattern that this metric can never penalise. The depth *score* also cannot move: `10 * 19/19 = 10.0`, the same as base (consistent with `w1/R40MistakeHunt.md` MH-4); the round-40 depth move is the block count and the v2 table's content, which `tools/round-40/c2-counter.py` measures separately.

## 5. Risks and limits

- Staleness is defensible as the lane's refresh-at-closure convention (at `52b0eb29` the rows also read one round behind — 126/126 and 17/17 — and were refreshed by the round-39 closure). The risk is that the refresh is *unowned* in round 40: neither frozen claim names it, the R38 calibration instrument and the wave-1 axis gate both go red at the landing, and wave 2 cannot perform the edit under the seat bounds.
- `SHONEN.md:6`'s `SKILL.md:81-343` is the one record that no longer describes the tree it ships with (the craft section ends at 375); it is anchored to `52b0eb29`, so it is stale rather than false. Any reader of the tip alone is misled about the section.
- The coverage recipe only counts stems matching `2026-10-\d{2}-[a-z0-9-]+`; an entry named outside that shape would surface as *missing* (visible), not as silent credit — no live occurrence at any of the eight revisions (missing `[]` everywhere).
- Not measured here: R40-C1's C1 counter, R40-C2's 26/26 triage score, REA/unblob/sasquatch (never run by this seat), SCORECARD `## Capabilities` rows 4-7 of the scout's list.

## 6. Tooling and housekeeping

No tool installed, upgraded or moved (nothing was needed; pacman is paused host-wide). Scratch `S=/fast/scratch/hyaku/kaidoku-r40/R40W2DepthCount` (including the sandbox clone) removed after copying the cited files.

## Artifacts (`.ufo/waves/round-40/w2/artifacts/R40W2DepthCount/`)

`commands.txt` (every command line and raw output), `depthcount.py` (driver importing the lane's `command_a`), `depth-3revs.json`, `anchors.json`, `52b0eb29.json`, `c2r38-base.json`, `c2r38-r39.json`, `c2r38-freeze.json`, `c2r38-measured.json`, `c2r38-at-tip.json`, `probe.py`, `probe.json`, `coverage-stem-columns.json`.
