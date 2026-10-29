# ExecC1Before — C1 before receipt re-taken at the freeze (kaidoku-shokunin r50 attempt 2, wave 4 falsify)

**VERDICT: the landed C1 BEFORE receipt HOLDS — attacked and held.** A clean re-take at the freeze
(`--rev == --freeze == 435d41fd4ad9211d1579fc447936fb33d2b74467`) reproduces the landed receipt
`.ufo/waves/round-50/l1/scores/c1-before-attempt2.json` **field-for-field; the only differing key is
`/argv`** (my absolute paths vs the L1's relative ones). `exit 1`, `carriers_matched 0` of `target 4`,
**no REA reached** (2.18 s wall, `rerun_toolchain: null`, `evidence_digests: {}` — the counter's
early-exit order is correct: at the freeze no envelope exists, so no rerun and no `xpin` node call is
issued). Independently confirmed by git objects: `corpus/evidence/round-50/` holds **0** files at the
freeze, so `carriers_matched 0` is a fact, not a counter artefact.

**The landed AFTER narrative does NOT hold.** The committed prose (SCORECARD round-50 row, PROVINCE
§"Round-50 measured, not promoted") claims *"the counter's rerun reproduced every projection"* and
attributes the whole miss to the gap rule. The after receipt it cites says otherwise: **`g7581:
projection_ok = false`** with `projection_error` = `execution_failure` / `ENOENT … readlink …/usr/www.myfritz/avme/cgi-bin/luacgi` — the g7581 rerun produced **no projection at all** (2 of the 3 failing clauses are on g7581, not one). The landing discloses one cause; the receipt carries two.

## Findings table

| # | axis | finding | severity | evidence |
|---|---|---|---|---|
| F1 | calibration | Landed prose claims the counter's rerun "reproduced every projection"; the cited after receipt records `g7581:projection_ok=false` (REA `execution_failure`, ENOENT `readlink` on `usr/www.myfritz/avme/cgi-bin/luacgi`). The g7581 miss has **two** causes (gap rule + rerun crash); only the gap rule is disclosed. | high | `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` → `carriers.g7581.projection_ok=false`, `carriers.g7581.projection_error.error.code="execution_failure"`, `failing=["g7581:gaps_ok","g7581:projection_ok","g7582:gaps_ok"]`; `SCORECARD.md:3796`; `PROVINCE.md:442`; entry `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md:3,52` |
| F2 | calibration | The frozen counter converts a non-timeout REA rerun failure into a **clause failure (exit 1)**, not into "could-not-evaluate" (exit 2): only `provider_timeout` gets the `RerunEnvError`/exit-2 treatment. Since g7581's failure is an `execution_failure` of the extraction itself, the honest state of g7581's projection is UNKNOWN, not "failed" — so `carriers_matched 2 of 4` may understate and `gaps_ok`-only attribution is not supported for g7581. | high | `tools/round-50/c1-counter.py:2395-2403` (`provider_timeout` → `raise RerunEnvError`; else `d['projection_ok']=False`), `:2414` (skipped case), `CLAUSES` at `:435-441`; same receipt as F1 |
| F3 | calibration | The g7581 rerun failure looks **transient/environmental, not carrier-structural**: g7582 carries the *identical* symlink `usr/www.myfritz/avme/cgi-bin/luacgi → /usr/www/cgi-bin/luacgi` (and 15 more `luacgi` symlinks) yet its rerun reproduced its projection (`projection_ok=true`). A re-run of the g7581 leg (L1-owned, REA-invoking) would decide; until then g7581's projection is unevaluated, not failed. | high | `tools/round-50/oracle/g7581.nonregular.tsv` vs `g7582.nonregular.tsv` (rows `usr/www.myfritz/avme/cgi-bin/luacgi symlink /usr/www/cgi-bin/luacgi` in both; g7581 has 1001 nonregular rows, g7582 1001); after receipt `carriers.g7582.projection_ok=true` |
| F4 | calibration | The entry's status line says "**every documentation binding true**"; the receipt's own `bindings_false` is `["province_core_section","province_core_row"]` (the counter requires both for a promotion). The two rows are false *by design* (no Core promotion was claimed) but the sentence as written is false against the receipt it cites. | medium | after receipt `bindings_false`; `BINDINGS` at `tools/round-50/c1-counter.py:432-434`; entry line 3 |
| F5 | coverage | The landing prose's "13 `char-device` entries each … no disposition for the other twelve" is **correct**: 13 char-device rows each on g7581/g7582 (`dev/led 247:0`, `dev/pts/0..7 136:0-7`, `dev/tiatm 230:0`, `dev/ttyp0..2 3:0-2`) and 1 each on the Cable carriers; the frozen rule's only silent admission is `247:0`, so 12 per FRITZ!Box carrier are undisposed. The counter's `gaps_note` lists only 8 of them because the message truncates at `sorted(missing)[:8]`. | attacked, holds | `tools/round-50/oracle/{g7581,g7582,c6490,c6430}.nonregular.tsv`; `tools/round-50/gap-rule.json` (`removed.silent["char-device"]=["247:0"]`); counter `:1563-1564` |
| F6 | calibration (informational) | In the before receipt `carriers_unchanged`, `gap_rule_unchanged` and `frozen_path_changed []` are **vacuous**: `--rev == --freeze`, so the drift checks compare a revision with itself. They carry information only in the after run (`--rev 646d29c9` vs `--freeze 435d41fd`), where they are true. | low | before receipt keys; `c1-counter.py` drift checks; after receipt `carriers_unchanged=true`, `frozen_path_changed=[]` |
| F7 | provenance | The counter file has not drifted since the freeze: sha256 `9820811b…` is identical at `435d41fd`, in the worktree and at the tip `db61a907`. All three round-50 C1 receipts (before/after/mine) pass the counter's own `--verify-receipt` identity gate (`ok: true`). | holds | `sha256sum` of `git show 435d41fd:tools/round-50/c1-counter.py`, the worktree file, and `git show db61a907:tools/round-50/c1-counter.py`; three `--verify-receipt` runs, exit 0 |

## Commands run (exact; exit codes; sha256 of stdout)

All runs: `python3 -I -B`, `TMPDIR=/fast/scratch/hyaku/kaidoku-r50/w4-ExecC1Before`, scratch `S=/fast/scratch/hyaku/kaidoku-r50/w4-ExecC1Before`.
Lane tree read-only: `git status --porcelain` before and after the runs is **byte-identical**
(`1b75636e…`); no commit/stage/stash/jj mutation was issued in the lane or the fleet repo.

| id | command (abbreviated paths shown literally as run) | exit | wall | stdout sha256 | receipt json sha256 |
|---|---|---|---|---|---|
| R1 | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/c1-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 435d41fd4ad9211d1579fc447936fb33d2b74467 --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work /fast/scratch/hyaku/kaidoku-r50/w4-ExecC1Before/w --carrier-cache /fast/scratch/hyaku/kaidoku-r50/carrier-cache --json-out /fast/scratch/hyaku/kaidoku-r50/w4-ExecC1Before/c1-before.json` | 1 | 2.18 s (2026-10-29T21:27:32Z) | `6d7f3834…` | `be863941…` |
| R2 | same counter, `--root /fast/scratch/hyaku/kaidoku-r50/w4-ExecC1Before/clone` (clean `git clone --shared` checked out `--detach` at the freeze rev; toplevel asserted before use), `--work …/w2`, `--json-out …/c1-before-clone.json` | 1 | 4.82 s (21:28:10Z) | `6d7f3834…` (identical stdout) | `527dfdc3…` |
| R3 | `python3 -I -B tools/round-50/c1-counter.py --verify-receipt .ufo/waves/round-50/l1/scores/c1-before-attempt2.json` | 0 | — | `{"ok": true, "detail": "ok", "counter_sha256": "9820811b…"}` | — |
| R4 | `… --verify-receipt $S/c1-before.json` | 0 | — | `{"ok": true, …}` | — |
| R5 | `… --verify-receipt .ufo/waves/round-50/l1/scores/c1-after-attempt2.json` | 0 | — | `{"ok": true, …}` | — |
| R6 | `git -C $LANE ls-tree -r --name-only 435d41fd… -- corpus/evidence/round-50/ \| wc -l` → `0`; same for `corpus/knowledge/` matching `r50\|avm-le` → `0` | 0 | — | — | — |
| R7 | `sha256sum` of the counter at `435d41fd`, at the worktree, at `db61a907` → `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813` (×3) | 0 | — | — | — |
| R8 | `grep -c char-device tools/round-50/oracle/<id>.nonregular.tsv` → g7581 13, g7582 13, c6490 1, c6430 1 | 0 | — | — | — |

Machine receipt: `.ufo/waves/round-50/w4/ExecC1Before/receipt.json`; artefacts: `stdout.txt`,
`stderr.txt`, `stdout-clone.txt`, `stderr-clone.txt`, `c1-before.json`, `c1-before-clone.json`,
`diff-mine-vs-land.txt`, `lane-status-{before,after}.txt`.

## Comparison with the landed before receipt — same numbers

Structural diff of my receipt against `.ufo/waves/round-50/l1/scores/c1-before-attempt2.json`
(landed file sha256 `131b9a45…`, mine `be863941…`): **exactly one differing key, `/argv`**. Every other
key is identical, including `carriers_matched 0`, `target 4`, `exit_code 1`, `met_target false`,
`bindings` (six false: `province_core_section`, `province_core_row`, `frontier_note`, `entry_present`,
`sourced`, `coverage_map_row`), `bindings_false`, `failing` (16 clause failures × 4 carriers),
`frozen_tables_valid true`, `gap_rule_ok true`, `gap_rule_uncovered_kinds []`, `carriers_unchanged true`,
`gap_rule_unchanged true`, `frozen_path_changed []`, `tables_absent_at_freeze []`,
`carriers_spec_problems []`, `gap_rule_problems []`, `projection_profile "plus-extractor"`,
`rea_parameters {max_depth 1, max_output_bytes 536870912, max_output_files 100000}`,
`counter_sha256 9820811b…`, `prior_pins` (identical list), and the per-carrier block
(`carrier_pin_ok`, `carrier_fresh_ok`, `layout`, `carve`, `compression 4`, `oracle_files`
4556/4564/4709/3955, `oracle_derived_files` equal, `oracle_rederived_ok true`,
`nonregular_entries` 1001/1001/914/824, `nonregular_kinds ["char-device","dir","symlink"]`).

The clone-root run (R2) differs from the lane-root run in `/argv` only as well ⇒ the before measurement is
**rev-pinned, not worktree-dependent**: it is a property of the freeze revision, independent of the
lane's current tip and of sibling seats' dirty files.

**Before ↔ after cross-check (holds):** the before receipt's frozen oracle tables
(4556 / 4564 / 4709 / 3955) equal the after receipt's `oracle_files` and `published_files` on the same
four carriers, and the before `nonregular_entries` (1001 / 1001 / 914 / 824) equal the after ones — so
the landing did not move the oracle tables between the freeze and the landing, and "REA published every
frozen-oracle regular file" is supported by the stored receipts on all four carriers
(`oracle_hits_ok true`, `extra_published []`, `nonregular_unpublished_ok true`).

## What the L1 should do with F1–F4

1. Correct the two prose sentences that claim the rerun "reproduced every projection"
   (`SCORECARD.md:3796`, `PROVINCE.md:442`) — for g7581 no projection comparison happened
   (`projection_error` = `execution_failure`, ENOENT `readlink` on
   `usr/www.myfritz/avme/cgi-bin/luacgi`).
2. Disclose the g7581 rerun failure as a second, separate cause of the 2-of-4 miss, and state g7581's
   projection state as **unevaluated** (the counter scores it as a clause failure only because
   `execution_failure` is not on the exit-2 list — `c1-counter.py:2395-2403`; `provider_timeout` is).
   g7582 carries the identical symlink and its rerun succeeded, so the failure is not carrier-structural.
3. Amend the entry status line's "every documentation binding true" — the cited receipt's
   `bindings_false` is `["province_core_section","province_core_row"]` (false by design, no promotion).
4. If the L1 wants the 2-of-4 number to stand as a *measurement* rather than a *defect*, one
   counter-time REA re-run of the g7581 leg (L1-owned; the counter's full predicate command is not
   re-run by seats) decides it. If that rerun again ENOENTs on the same symlink, the gap rule is not the
   only blocker and the freeze's repair plan is incomplete.

## Scope / honesty notes

- **No REA run was performed by this seat.** The C1 counter's full predicate command (the one that
  invokes REA) was not re-run; only the at-freeze invocation (which provably does not reach REA — no
  envelope exists at the freeze) and the offline `--verify-receipt` gate were run.
- F1–F4 are read against the **landed** after receipt and the committed prose; no claim is made about
  what a fresh g7581 REA rerun would produce (not run).
- The lane tree was not modified: `git status --porcelain` identical before/after; the only writes are
  this seat's directory `.ufo/waves/round-50/w4/ExecC1Before/` and this report.
- No tool was installed or upgraded for this seat (python3 3.14.8, host-provided).
- Scratch `/fast/scratch/hyaku/kaidoku-r50/w4-ExecC1Before` removed after copying the artefacts above.
