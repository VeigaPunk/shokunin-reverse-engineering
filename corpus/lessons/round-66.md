# Round 66 — the two counter repairs: the closure boundary and the self-assessment atom

Base `311079d869f068bc083a8d180977e49634120fdf`; instruments and do-nothing controls `78fa9666`
(ancestor of the freeze, `git merge-base --is-ancestor 78fa9666 7b63dd5d…` exit 0); operative freeze
`7b63dd5d5199ed30bc3f213573d8594434a18eb6`; carry-in `b5b02e1f` (ancestor of the freeze, exit 0,
`.ufo/waves/round-66/l1/records/r66-order.txt`); record `5de8a1de` and the single-fraction row edit that
follows it. Two claims: R66-C1 (depth, counter repair) reads 5/5 on its after-arm; R66-C2 (calibration,
counter repair) reads `mismatches 0` at the record, after the `## Owned axes` coverage row is re-derived
in the same commit that changes the knowledge population. Both verdicts carry disclosed witness gaps
(M66-5 … M66-7), routed to the next freeze and never repaired in place.

## Gate

Access date for the new source: 2026-11-03. Fetch, locator and quote evidence:
`.ufo/waves/round-66/w1/ScoutSources/{row.md,gate.md,fetch.json}`; the row landed as S267.

| candidate | locator / evidence | measured value | decision | flip condition |
|---|---|---|---|---|
| (a) CPython `sys.dont_write_bytecode` page | https://docs.python.org/3/library/sys.html, opened this round: HTTP 200, 280617 bytes, sha256 `572c354eb01e5121f7beb3084408fc7ecbc465accf3a3335f1182c7df3648f7e`, captured 2026-11-04T00:16:22Z UTC; dt `sys.dont_write_bytecode` raw line 585, dd raw lines 587-591; nearest heading the module h1 `sys` (raw line 206), the body carries no h2; Gate quote 18 words "initially set to True or False depending on the -B command line option and the PYTHONDONTWRITEBYTECODE environment variable" | the attribute's own semantics: the attempt not to write `.pyc` files on import, an initial value set from `-B` and the variable, assignable at runtime. This is the page r65 rejected only as the *S266 switch anchor*; its subject here is the variable, not the switch | **admit** (official docs for its own attribute → tier A; scope = the flag's stated semantics only, never cache contents or an emptiness guarantee) | admissible as a different scope only if the page's own text changed; a page that stopped naming the variable would flip it |
| (b) cmdline.html `-B` section as this round's row | `corpus/SOURCES.md:183` (S266): `#cmdoption-B`, raw line 474 under h3 `Miscellaneous options` (line 451), snapshot `96f87232…` | the switch's own stated effect, already carried with a 15-word quote | **reject as this round's row**: S266 already holds that locator and scope; a second row would duplicate a standing row | admissible only if the new row's subject became the switch itself, which is S266's |
| (c) the r65 instrument's `--recipe date` mode as "recipe A" | `tools/round-65/coverage-recipe.py:93`; `.ufo/waves/round-66/l1/controls/c2-do-nothing.json` condition 1 | date mode: `knowledge_files 145`, `mapped 142`, `missing []`, plus `population`, `population_dropped 3`; recipe A: the same files, `missing` the three names, `coverage_score 9.79`, `depth_score 10.0`, `rule_blocks 27`, `citation_resolved_rules 27`. They share only `mapped` | **reject**: a measured field difference, not a naming preference (the M65-2 pattern) | admissible if the mode's emitted key set and `missing` list matched recipe A at one revision |
| (d) a 30-vs-29 count fixture as evidence of the count assertion | `.ufo/waves/round-66/l1/controls/c1-do-nothing.json` a4; `w1/ExecClosure/verify.json` a4 | r65 `--manifest` on a one-entry-short copy: exit 0, `entries 29`, `ok true`; r66 counter on the same shape: `count_ok false`, `entries 29`, `count 29 != 30` | **reject as a source**: a fixture demonstrates a red arm; the count's provenance is the frozen `CLOSURE` (30 entries = 27 keys + probe + node + interpreter) plus `COUNT = 30` | a fixture never becomes a SOURCES row |

Assimilation: none this round — the `merge/kaidoku/` jsc theme was adopted in round 64, no remaining
staged theme fits two counter repairs, and `considerthese/` is absent (`ls considerthese` exit 2,
recorded in `w1/ScoutSources/gate.md`). No row was bulk-appended.

Outside spot-check: the round's non-author closure judge supplies it; this lesson does not self-certify
admit/reject agreement.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M66-1 | stale-premise/boundary: the r65 closure check ran before the setup probe while the before-census was taken after it, so a cache written by the probe was invisible; the entry count was emitted, never asserted; `--skip-run` emitted a synthetic `closure.ok true` | `.ufo/waves/round-66/l1/controls/c1-do-nothing.json` a2 block (`r65_order_state {cache_present: [], ok: true}` against `cache_on_disk_after_probe [...]pyc`), a4 block (`r65_exit 0`, `entries 29`, `ok true`), a5 block (`r65_closure.ok true`); repaired readings in `w1/ExecClosure/verify.json` a2/a4/a5 | the r65 non-author closure routed it (M65-5); no QUALITY criterion bound it at the time — rows 104 and 105 are added this round | the ordered post-probe scan folded into `ok`, the `COUNT` assertion, and `closure: null` on `--skip-run`; shown red by the 1/5 control and by arm-mutations `COUNT 30 -> 29` (a3/a4), scan-before-probe (a2) and a synthetic closure (a5) in `w1/ExecControls/m{1,2,3}-verify.json` |
| M66-2 | scope: the frozen "naming the files it hides" clause had no implementing line — `population_dropped` was an integer and the filtered date population left `missing []` | `tools/round-65/coverage-recipe.py:104-108`; `.ufo/waves/round-65/l1/c2-before-date.json` (`population_dropped 2`, `missing []`); the new list `recipe_a_hidden` = 3 names at the base and the freeze, 4 at the record (this round's own entry joins them) | QUALITY #87, not applied at the r65 freeze; routed by the r65 closure (M65-4) | an emitted list (`recipe_a_hidden`, `recipe_a_hidden_count`) and `bool(hidden)` as one `ok` conjunct; shown red by the 0/3 control and killed in `MutCoverage` M1 |
| M66-3 | vacuous/control-contamination (this round's own, pre-freeze): the first C1 control run drove the a2 arm probe and the r65-order emulation through one fixture, so the pre-probe scan saw the cache the arm probe had just written and the control falsely "met" the a2 arm | red then green, retained fresh: `.ufo/waves/round-66/l1/records/m66-3-contamination.json` — one shared root gives `control_meets_a2_arm true`, two roots give `false`, `red_demonstrated true`; the corrected control itself is `.ufo/waves/round-66/l1/controls/c1-do-nothing.py` with `fx66 = arm66-…` and `fx = ctl-…` | the control's own detail dump (the a2 block printed `cache_present` before the probe) | every arm owns its root and the receipt separates the two states; QUALITY #106 records the rule; the pre-fix receipt was overwritten in place, so the red is re-produced by `m66-3-contamination.py` rather than retained from the first run |
| M66-4 | process/scope: the lane's own tool directory was not cache-free at the freeze while the frozen toolchain was — the round's cache-free discipline was asserted only for `/home/vgpnk/.local/share/kaidoku-jsc` | `tools/round-66/__pycache__/closure-boundary.cpython-314.pyc` and `…/coverage-selfcheck.cpython-314.pyc`, mtime 21:13:29 (freeze 21:13:44), ignored by `.gitignore:1` (`git status --porcelain --ignored` → `!! tools/round-66/__pycache__/`); contrast `w1/ExecClosure/toolchain-cache-after.txt` 0 bytes | `ScribeLesson`'s census read; no seat and no predicate covers the lane tree | removed before the landing; the limit is stated (no frozen clause samples the lane tree); routing item (a) of the round-66 `planned` field extends the closure census to `tools/round-<N>/` |
| M66-5 | boundary/witness: the a2 arm's condition binds the outcome (`ok false`, a `.pyc` named, `probe.ok true`) but not its cause, so a counter that runs the probe guarded and plants a cache scores 5/5 with a byte-identical a2 detail | `w1/CriticClaims/attacks.md` §A; `w1/CriticClaims/evidence/S_A1-verify.json`, `S_A2-verify.json`, `S_A1.diff`, `S_A2.diff` versus `evidence/frozen-verify.json` (detail dict equality `true`) | critic attack A this round; the arm condition is the line that should have caught it | routed, not repaired post-freeze: the next freeze records the probe argv/env it chose and requires `"-B" not in argv`, absent `PYTHONDONTWRITEBYTECODE`, and `cache_before == []` as arm conditions |
| M66-6 | boundary/witness: the a5 arm compares `skip_run_receipt`'s own literals in-process and never observes the CLI emission, so a counter whose `--skip-run` prints `closure.ok true` still passes a5; a1's `count_ok` clause is an identity (`len(manifest) + 3` against `len(FIXTURE_RELS) + 3`), and an empty manifest reports a green closure | `w1/CriticClaims/attacks.md` §B; `evidence/S_B-verify.json` (5/5) and `S_B-skip-run.json` (`closure.ok true` emitted) | critic attack B this round | routed: a5 must spawn `--skip-run` and parse the emitted object; a1 must compare against an external count or drop the clause. The claim's a5 clause is nonetheless observed by the CLI receipt `w1/ExecClosure/skiprun.json` (`closure null`), which is why the verdict stands with the mechanism disclosed |
| M66-7 | scope/atom strength: the row atoms read only the FIRST `<n>/<n> knowledge files` occurrence and the text after the LAST arrow, so a correct fraction prepended to a stale one (R2) and a multi-arrow score cell (R4) both report `mismatches 0` | `w1/CriticClaims/attacks.md` §D; `evidence/D-R1…R4.json` (R2 and R4 exit 0, mismatches 0; R3 and R5 caught; R6 could-not-evaluate) | critic attack D this round; F9 in `w1/ReviewerClosure/review.md` named the first-match shape as a nit | the landed row is made single-fraction and single-arrow so the frozen atom reads the only claim in it, and the next freeze requires every occurrence to equal the stem value (or exactly one occurrence) |

## Outcome

- **R66-C1 — verified.** `w1/ExecClosure/verify.json` (exit 0) and `l1/scores/c1-after-verify-at-record.json`
  (exit 0) both report `passed 5 of arms_total 5`, `ok true`, `count 30`, `v1_pin 79a4dca4…`. a1 `ok true`,
  `cache_present []`; a2 `ok false` with `cache_present ["__pycache__",
  "__pycache__/fixture_mod.cpython-315.pyc"]` and the probe itself `ok true`; a3 `entries 30`, `count_ok true`;
  a4 `entries 29`, `count_ok false`, finding `count 29 != 30`, dropped entry `d8-14.7.173/d8`; a5 `closure
  null`, `closure_claimed false` (`w1/ExecClosure/skiprun.json`, exit 1 by the mode's own contract). The
  do-nothing control scores 1 of 5 (`l1/controls/c1-do-nothing.json`); three arm-mutations each flip their
  own arm (`w1/ExecControls/`); the selftest is 30 cases clean (`l1/pre/selftest-c1.txt`); the instrument's
  sha256 is unchanged before and after every run (`3c5cfb03…`); the toolchain cache scan is 0 lines.
  **Disclosed witness gaps (routed, M66-5/M66-6):** the five arms do not by themselves prove the ordering
  fix — the a2 condition does not bind the probe's guard state, and a5 is an in-process literal; the a5
  clause's actual observation is the CLI receipt, not the arm. `MutClosure` also survives M5 (`arm()`
  returns `passed: true`), which only a controlled red (`--python /nonexistent`: pristine 2/5, M5 5/5)
  separates.
- **R66-C2 — verified at the record.** `l1/scores/c2-after-selfcheck-at-record.json` (revision `5de8a1de`):
  `recipe_a_equivalent true`, `recipe_a_diffs {}`, `recipe_a_hidden 4` (`2026-11-03-r65-jsc-closure-matrix`,
  `2026-11-03-r66-closure-boundary`, `jsc-mapper-cli-contract`, `jsc-mapper-release-inventory`), stem
  146/146 with `mismatches 0`, atoms A1 `10.0` vs `10.0` and A2 `[146, 146]` vs `[146, 146]`, `mismatches 0`,
  `ok true`, exit 0. Before-arm: `l1/pre/dryrun-c2-selfcheck-at-base.json` and
  `w1/ExecCoverage/selfcheck-at-base.json` (A2 false, `[142, 142]` vs `[145, 145]`, `mismatches 1`, exit 1);
  the freeze receipt repeats it (`w1/ExecCoverage/selfcheck-at-freeze.json`); the control scores 0 of 3.
  Recipe A is reproduced field for field against the committed SCORECARD block at the same revision
  (`--equiv`, block sha256 `1d697af1…`), and the base numbers are 145 files / 142 mapped / score 9.79 /
  depth 10.0 (27/27 rules). **Disclosed atom weakness (routed, M66-7):** the frozen atoms read the first
  fraction and the last arrow; the landed row is made single-fraction and single-arrow so the atom cannot
  read a stale one, and the strengthening of the atom itself is the next freeze's work. `MutCoverage`
  survives M2 (an equivalence arm that returns true without running the block) at a green revision; on a
  doctored block pristine `--equiv` exits 1 with three diff keys and M2 exits 0.
- **Outside closure — pending.** The round's non-author closure has not run and this lesson does not
  self-certify either verdict.

## Census

Round start: `l1/census-start.txt` → `validate --root /home/vgpnk/Projects/shokunin kaidoku` exit 0, 19
standing W04 duplicate-url warnings, 173 rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`).
Round end: 174 rows after S267, same 19 W04, `mined 165 / rejected 9`; stem recipe 146/146 at the record.
The 19 W04 stay named debt at both ends.
