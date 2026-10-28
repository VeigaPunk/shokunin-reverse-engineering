# W2CleanClone — clean-clone runnable-verbatim attack, round 49 wave 2

**Verdict: both counters reproduce exactly as the plan states in a fresh `git clone --shared` at `29883d4ec35a31a8393c4ffb220888c44c0bb022`; no counter defect found. Two paste-hazards in the lesson's commands (F1, F2) and one provenance note (F3) for the L1's report text.**

Clone: `/fast/scratch/hyaku/kaidoku-r49/W2CleanClone/clone` (`rev-parse --show-toplevel` = clone dir; detached HEAD = REV; FREEZE is an ancestor; clone `status --short` empty after all runs). All runs `GIT_NO_REPLACE_OBJECTS=1`, `TMPDIR` under scratch, cwd = clone (also repeated from the fleet root). Receipts (cmd/rc/time/out/err) in `.ufo/waves/round-49/w2/W2CleanClone/`. Scratch work dirs removed.

Common args: `--root $D --freeze decc5697bfd4ec1e9de4a762ad199d9bd9c4230d`, C1 also `--pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work $S/w* --json-out <OUT>`. Run 2026-10-28T22:41:34Z (parallel, 16 s wall).

| # | command (as the L1 pastes it) | exit | stdout sha256 | observed |
|---|---|---|---|---|
| 1 | `python3 -I -B tools/round-49/c1-counter.py … --rev 29883d4e…` | 0 (expected 0) | `ae830b21…b64657` (`c1-after.out`) | `carriers_matched 4`, `bindings_false []`, `frozen_path_changed []`, `met_target true`, `target 4`, all four carriers gzip, handlers v1/v1/v2/v2, endian le/be/le/be, entry S112/S138/S139 |
| 2 | same, `--rev decc5697…` (freeze) | 1 (expected 1) | `976af57f…acfa17c` (`c1-before.out`) | `carriers_matched 0`, false bindings exactly `coverage_map_row, entry_present, frontier_note, province_core_row, province_core_section, sourced`; `frozen_path_changed []` |
| 3 | `python3 -I -B tools/round-49/c2-mismatch.py … --rev 29883d4e… --battery` | 0 (expected 0) | `0cad6d5c…0f86` (`c2-after.out`) | `atoms_total 9`, `mismatches 0`, `battery.failing []`, 16 mutations, each `ok`, `red == [own atom]`, `noop []` (checked programmatically), `do_nothing_paths 102`, `do_nothing_red` A1–A9 |
| 4 | same, `--rev decc5697…` no `--battery` | 1 (expected 1) | `7aa900e1…37f4` (`c2-before.out`) | `atoms_total 9`, `mismatches 9` (A1–A7 "lesson line Ax absent"; A8 0 entries for r48 and r49; A9 0 sections) |
| 5 | rerun of #1 with fresh `--work`, counter from clone path, cwd = fleet root | 0 | same `ae830b21…` | stdout byte-identical; JSON differs only in `argv` |
| 6 | rerun of #3 from cwd = fleet root, counter from lane worktree path, `--root` clone | 0 | same as #3 | byte-identical (cwd-independent) |
| 7 | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` (clone at REV) | 0 | prints `149` | matches lesson "146 → 149"; base `e4f2cfa5` prints `146` |
| 8 | `git ls-tree -r --name-only <rev> corpus/knowledge \| grep -c '\.md$'` | 0 | base `e4f2cfa5` → `138`; REV → `139` | +1 as expected (same count run in the fleet lane) |
| 9 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | 0 | `065a45eb…a2ea` (`census-verbatim.out`) | 15 `W04` lines (S033 … S142) + final `kaidoku ok …/kaidoku-shokunin/corpus/SOURCES.md`; stderr empty; matches lesson's "15 W04, S033…S142" and the L1 `sources-census-end.txt` (that file additionally ends with a literal `exit=0` line) |
| 10 | `sources-census.sh validate --file $D/corpus/SOURCES.md` (clone) | 0 | (`census-clone-file.out`) | same 15 W04 + `ok`; so the registry at REV validates clean independent of the live tree |

## Findings

- **F1 (paste hazard, lesson text; not a counter defect).** Command #9 as written in `corpus/lessons/round-49.md` (`--root /home/vgpnk/Projects/shokunin kaidoku`) reads the **live lane worktree** `corpus/SOURCES.md`, not a revision. It gave the right answer here only because the lane worktree HEAD equals REV with a clean `corpus/SOURCES.md` (`git diff --stat REV -- corpus/SOURCES.md` empty at capture time). It is not a REV-pinned measurement; for a REV-pinned receipt use `--file <clone>/corpus/SOURCES.md` (#10). The L1 should say which tree each census read, or paste #10.
- **F2 (paste hazard, lesson text).** The `grep -c` (#7) is likewise a worktree read, and the `ls-tree` line (#8) needs the base and REV as two commands run with the `-C <lane>`; the lesson shows neither base/REV form for #8. Both commands print the expected values (149; 138→139), and the "+1" is only visible by running both revs. No command printed anything other than what the plan/lesson say.
- **F3 (provenance note).** `.ufo/waves/round-49/l1/scores/c1-at-landing.json` has `revision b58f9b192aba548b99d250bb896bbc42c654632c` (the parent of the landing REV), not `29883d4e…`; `c2-at-landing.json` is at `29883d4e…`. The lesson cites `.ufo/waves/round-49/l1/scores/c2-final.json` (M49-1 row) — that file does not exist in `l1/scores/` (present: `c1-at-3847f393`, `c1-at-data-4aabb0b4`, `c1-at-landing`, `c2-at-3847f393`, `c2-at-landing`). L1 must re-measure at the final revision and make the report's receipt paths exist (observed in the lane worktree; other seats may have a different view if the L1 is writing).
- No counter defect: both counters are deterministic across `--work` dirs and cwd, write nothing into the clone, and the freeze and REV numbers are exactly the plan's (9→0; 0→4).

Not run: any `c1-run.sh --data-run`; `--selftest`; mutation of counters (other seats own those).
