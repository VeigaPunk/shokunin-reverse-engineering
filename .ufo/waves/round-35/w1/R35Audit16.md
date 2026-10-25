# R35Audit16 — D4 row-shape mutation tester (wave 1)

Seat: R35Audit16 (executor/mutation-tester). Item: *Mutate D4 row shape in /tmp. Read-only or private /tmp only; no lane writes.*
Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Instrument: frozen `tools/round-35/c2-calibration-counter.py` (reads immutable git objects only).
Params used: `--base aa04633a686d49756763b1feed4be6830d5bb479`, `--freeze 2323d197456f1328459d9420aff025cffbcb3e27` (first commit adding `.ufo/waves/round-35/claims-canonical.json`), `--rev` per measured commit.

## 1. Baseline (first falsifications, already recorded)

Running the frozen counter at base and tip reproduces the committed do-nothing receipt
`.ufo/waves/round-35/controls/c2-do-nothing.json` exactly (same failing set, exit 1):

- At base (`aa04633a`): `D1_census_start_missing; D2_lesson_missing; D3_source_missing; D3_verified_at_missing; D3_recheck_missing; D3_source_not_s106; D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4; D4_section_missing:### Round-34 run-6 instrument registry`.
- At tip (`3ecf4298`): same minus `D1_census_start_missing` (census now present) plus `D1_no_sources_change_after_base`; D4 identical.

D4 is therefore **not closed** at tip. Two distinct D4 failure modes are live in the real `SKILL.md`:

1. `D4_section_missing:### Round-34 run-6 instrument registry` — the counter looks for the byte-exact heading
   `### Round-34 run-6 instrument registry`, but the actual heading is
   `### Round-34 run-6 instrument registry — the shortcut-replay gate (stopped capability)` (line 1209). Exact-match on `l.rstrip() == sec`.
2. `D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4` — the "Residual witness registry" table
   (lines 1081–1084, 4 cells) sits **inside the same section span** as the round-32 registry (no intervening `##`/`###`
   heading between line 1064 and line 1086), so every `|`-starting line in that span is counted. The run-6 table
   (lines 1213–1219) is 5-cell; it is masked in the current output because section 2 is already missing.

## 2. Green baseline (D4-only) built in private scratch

`git clone` of the lane into `/tmp/r35audit16-w1` (private; source untouched). From tip `3ecf4298` a green-D4 tree `G`
(= `c0b4ca60445997f5b52de625ede926ce18c72d3e`) was built: exact run-6 heading; every `|` line in both spans padded to
8 cells (round-32 span incl. residual table; run-6 header/separator/rows). Counter at G: **no D4 failure** (exit 1 only on
D1–D3, which are outside this seat's scope). `git show G:SKILL.md` scan confirms 0 non-8-cell rows in both spans.

## 3. Mutation matrix (each a separate commit from G; counter run per rev)

| Variant | Mutation (D4 row shape) | Counter result (revision) |
|---|---|---|
| M1 | run-6 data row 1215: drop one cell (8→7) | `D4_not_eight_cells:### Round-34 run-6 instrument registry:line1215:cells=7` (`fe6beed9`) |
| M2 | round-32 data row 1068: add one cell (8→9) | `D4_not_eight_cells:### Round-32 instrument registry:line1068:cells=9` (`bca41dd6`) |
| M3 | run-6 data row 1216: merge two adjacent cells (8→7) | `D4_not_eight_cells:### Round-34 run-6 instrument registry:line1216:cells=7` (`50fca687`) |
| M4 | round-32 data row 1069: remove trailing pipe (8→7) | `D4_not_eight_cells:### Round-32 instrument registry:line1069:cells=7` (`fa5bacd3`) |
| M5 | run-6 data row 1217: wrap across two lines (first fragment 4 cells) | `D4_not_eight_cells:### Round-34 run-6 instrument registry:line1217:cells=4` (`65c552e7`) |
| M6 | negative control: blank line inserted after run-6 header | **no D4 failure** (`5a12b357`) |
| M7 | run-6 separator row 1214: shrink to 5 cells | `D4_not_eight_cells:### Round-34 run-6 instrument registry:line1214:cells=5` (`140e602e`) |

All mutations are detected with the correct section/line/cell-count ID; M6 shows non-row edits do not perturb the check.

## 4. Worktree-independence

At rev M1, with the worktree's `SKILL.md` restored to the clean G content (`git status` = `M SKILL.md`), the counter
still reports `line1215:cells=7` — it reads only the committed git object, never the worktree.

## 5. Advisory findings

- The recorded `instrument_revision` `d2729cba…` **cannot be used as `--freeze`**: `.ufo/waves/round-35/claims-canonical.json`
  does not exist at that commit (counter exits 2, "claims file absent at freeze revision"). The usable freeze is the first-add
  commit `2323d197` (same one used in the committed control receipts).
- To close D4, the data wave must (a) introduce the byte-exact heading `### Round-34 run-6 instrument registry` and
  (b) make every `|`-starting line in both spans exactly 8 cells — including the round-32 span's residual 4-cell witness table,
  which currently blocks the round-32 span regardless of the run-6 table.
- Detector nuance: a row wrapped onto a non-pipe continuation line is only partially visible (M5: continuation ignored;
  first fragment counted). No false negative observed for any pure row-shape change.

## 6. Scope enforcement

No lane production file was written. Only private /tmp scratch (`/tmp/r35audit16-w1`, receipts under `/tmp/r35audit16/`)
and this report. No VCS mutation of the lane; no `find`/`du` under `/fast/scratch`; no delegation.
