# C2ScorecardDraft — SCORECARD repairs for R50-C2 (DRAFT text, pre-freeze)

Base `7c678ae6d97aedb969fd253b52b3d2882ef1e186`. Targets: `SCORECARD.md` `## Owned axes` rows `coverage` (line 23) and `calibration` (line 25), and a new `## Record corrections — round 50` section appended after the round-49 section. Blocks are paste-ready; `<N>`, `<REV>`, `<FREEZE>` and `<entry-stem>` are landing-time markers and must be filled from receipts before the row is committed. No block touches `depth` (no round-50 depth claim).

## Block 1 — coverage row, leading fraction (atom B1)

Replace the leading clause of cell 3 of the `| coverage |` row (`SCORECARD.md:23`). The old clause stays as history, after the new clause.

OLD (leading clause):

```text
138/138 knowledge files mapped at the round-47 landing (`git ls-tree -r --name-only <rev> corpus/knowledge | grep -c '\.md$'` → 138; command A `mapped 138`, `missing []`, `dangling []`, receipt `.ufo/waves/round-47/l1/scores/`)
```

NEW (leading clause):

```text
<N>/<N> knowledge files mapped at the round-50 landing (`git ls-tree -r --name-only <rev> corpus/knowledge | grep -c '\.md$'` → <N>; command A `mapped <N>`, `missing []`, `dangling []`; receipt `.ufo/waves/round-50/l1/scores/`; <N> = 139 at base `7c678ae6` plus the round-50 entry `<entry-stem>` if admitted); 139/139 at the round-49 landing `29883d4e` (the round-49 entry `2026-10-28-r49-squashfs-v1v2-core` is mapped at `corpus/README.md:105`); 138/138 knowledge files mapped at the round-47 landing (`git ls-tree -r --name-only <rev> corpus/knowledge | grep -c '\.md$'` → 138; command A `mapped 138`, `missing []`, `dangling []`; receipt `.ufo/waves/round-47/l1/scores/`)
```

Re-derivation of the base value (run by the seat, read-only): `git ls-tree -r --name-only 7c678ae6d97aedb969fd253b52b3d2882ef1e186 corpus/knowledge | grep -c '\.md$'` → 139; every stem is named in `corpus/README.md` at base (0 unnamed).

## Block 2 — calibration row, append to cell 3 (atom B2)

Append to the end of the `| calibration |` row's `Observable and limitation` cell (`SCORECARD.md:25`), after `… or mastery`. The numeric `0 → 10` cell is not changed (the operator rules on scores; this block records the verdict beside it).

```text
; **round-48 verdict:** `rejected-harmed`, calibration `harmed` (`corpus/lessons/round-48-verifier-spotcheck.md:7,107`): the round-48 lesson's declared-freeze header names `0f06251b…` while the final declared freeze was `b6f7ca2a…` (`corpus/lessons/round-48.md:4`); the numeric `10` in this row is not a statement that calibration held through round 48 (`## Record corrections — round 49`, line A9; `## Record corrections — round 50`, line B4); **round-49 measure:** `tools/round-49/c2-mismatch.py` at freeze `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d` → `mismatches 9`, exit 1; at landing `29883d4e` → `mismatches 0`, `atoms_total 9`, 16 mutations each red on its own atom, do-nothing red ×9 (`.ufo/waves/round-49/l1/scores/c2-final.json`, sha256 `544167f2a6a715954152459659faa67d031ecf9f0231f185930f02ef5de61565`); **round-50 measure:** `tools/round-50/c2-record.py --rev <REV> --freeze <FREEZE> --battery` → `atoms_total <N>`, `mismatches <N>` (`.ufo/waves/round-50/l1/scores/c2-final.json`)
```

Optional, not an atom: the `Last-change round` cell of the calibration row still reads `operator-steered r1 + luna-round-2`; the round-49 A9 line and this round's B4 line are the later calibration changes. Coverage's `Last-change round` cell likewise predates round 41 and round 49. Changing those cells is the L1's call.

## Block 3 — `## Record corrections — round 50` (atoms B3, B4, B5)

Insert **immediately before** the line `## Record corrections — round 49` (line-anchored, not the prose mention inside the round-48 `Owned scores` sentence), so the round-49 corrections section stays the last section of `SCORECARD.md`. Grammar: the round-47/48 `- corrects <class> <key>: <statement>` form for the classes those counters parse (`seats`, `path`, `rev`, `window`, `axes`, `quote`), and the round-49 `- <ID> verdict=…` form for verdicts (the only verdict form a counter exact-matches). `corrects verdict …` and `corrects receipts …` are **not** parsed by any round-47/48/49 counter (see the grammar check in `C2ScorecardDraft.md`); they would be silently dropped, so they are not used.

```text
## Record corrections — round 50

Append-only repair of round-48 statements that the round-48 and round-49 closures contradict (`corpus/lessons/round-48-verifier-spotcheck.md`, `corpus/lessons/round-49-verifier-spotcheck.md`). Each line supersedes the sentence it names; the original sentences stay where they were written. The owned-axes rows are repaired in place (coverage and calibration, Blocks 1 and 2), not by a correction line.

- corrects seats round-48: 1 wave, 75 seats total — the round-48 sentences `all 75 seats settled` and `settled 75/75 seats` overstate settlement: 72 of 75 seats have a report artifact (`w1/<seat>.md` or `w1/<seat>/`); `C1Meaning` ended `"status": "blocked"` (`frozen_worktree_dirty`, `files_changed []`), `C1Battery` has no `w1/C1Battery.md` (its receipt is the directory `w1/C1Battery-2/`), and `ScribeReportNumbers` ended `"aborted": true`. Re-derive the total with `jq '.results|length' .ufo/waves/round-48/r48-w1-results.json` → 75 and the report count with the B3 atom of `tools/round-50/c2-record.py`.
- B4 verdict=rejected-harmed source=corpus/lessons/round-48-verifier-spotcheck.md coverage=unchanged depth=improved calibration=harmed quality=harmed discernment=improved-at-decision-level-only expansion=unchanged — supersedes the round-48 `Owned scores` sentence (`calibration 10 → 10`) and the round-48 `Learning trends` sentence (`quality improved on the instruments`; `discernment improved (… each disclosed)`). Closure per-axis table `corpus/lessons/round-48-verifier-spotcheck.md:103-107`; trend verdicts `:124-127`; admission `:7`.
- corrects path .ufo/waves/round-48/l1/scores/c1-final-33f65a91.json: the R48-C1 final measure (tip `8847042a140b044dbf335210c965bf7b06b09b4f`, sha256 `6320c5d240e4822d1612c2cb929b383ca6f628953f032c7c92253e53d8ced86e`); the round-48 `measured at` cell names only the pre-landing receipt `c1-at-2e785632.json` (sha256 `a6e9f60560f7a6b9036a898a8a4d1d27cf0adf37606016b045e67b410bf6634c`).
- corrects path .ufo/waves/round-48/l1/scores/c2-final-33f65a91.json: the R48-C2 final measure (tip `8847042a140b044dbf335210c965bf7b06b09b4f`, sha256 `d1bb87d883ebfc25210d10073f00e98edf7e83c8a21417e4dc62a0bc28a23914`); the round-48 `measured at` cell names only the pre-landing receipt `c2-at-2e785632.json` (sha256 `8dcd18913a14c8d0fa7bfbf2cf17bfcef3a5d3fe5d6f2c6cbc518f59f1e794f9`).
```

Not an atom, optional for the L1: the round-48 `planned (round 49): … pin the gate.py helper …` sentence was not executed in round 49 (`W2C2Scorecard` F12, A9 prose). A line `- planned (round 49) … not executed; routed again` would mark it; the closure does not list it as contradicted, so it is not in B3–B5.

## Notes for the L1 (not paste text)

1. The B4 verdict line uses the A9 machine form because a verdict has no class in the round-47/48 grammar. If the L1 wants the requested `corrects verdict round-48:` form, the round-50 counter must add a `verdict` class to its `CORR` regex before the freeze; otherwise that line is inert.
2. `<N>/<N>` in Block 1 is not a digit fraction: the round-48 `axis_scores` regex (`\d+/\d+`) skips it until the landing fills it. The grammar check reports this at the draft stage.
3. Block 3 placement is load-bearing. The round-49 counter's A9 battery appends its mutation at **end of file** (`tools/round-49/c2-mismatch.py` `mutations()`, `sc.rstrip('\n') + '\n- A9 …'`). Placed after the round-49 corrections (fixture `84eebc28512cc30e055b7b4f9b79540548aba3e9`), that mutation lands in the round-50 section, the round-49 A9 atom stays green, and the battery reports `A9 contradictory second line appended -> red [] noop []` (exit 1). Placed before the round-49 corrections (fixture `6630ad3423849703265e4ec15f3cd178cb090254`), the round-49 counter at `--battery` is exit 0, `mismatches 0`, `battery.failing []`, `do_nothing_red` all nine. The round-48 counter (`tools/round-48/record2.py`) matches only the round-48 heading and is unaffected by either placement.
