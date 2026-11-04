# Round 66 — the two counter repairs: the closure boundary and the self-assessment atom

Base `311079d869f068bc083a8d180977e49634120fdf`; instruments and do-nothing controls `78fa9666` (ancestor of
the freeze, `git merge-base --is-ancestor 78fa9666 7b63dd5d…` exit 0); operative freeze
`7b63dd5d5199ed30bc3f213573d8594434a18eb6`; carry-in `b5b02e1f` (ancestor of the freeze, exit 0,
`.ufo/waves/round-66/l1/records/r66-order.txt`). Two claims: R66-C1 (depth, counter repair) reads 5/5 on its
after-arm receipt; R66-C2 (calibration, counter repair) is **not yet verified at the freeze** — its measured
revision is the landing, where the coverage row it repairs is written.

## Gate

Access date for the new source: 2026-11-03. The row itself is the scout's; the identifiers below are the
recorded r65 measurement, not a fresh fetch by this seat.

| candidate | locator / evidence | measured value | decision | flip condition |
|---|---|---|---|---|
| (a) CPython `sys.dont_write_bytecode` page | https://docs.python.org/3/library/sys.html, attribute at line 585; r65's recorded alternative (`corpus/lessons/round-65.md:17`): snapshot sha256 `572c354e…`, 280617 bytes, fetched 2026-11-03T23:26:03Z | the sentence r65 rejected as the *S266 anchor* is the same sentence, but the attribute is the flag `-B` sets — a different subject (the env var, not the switch) | **admit** (tier A, docs — official Python documentation for its own attribute). Row id assigned at landing; the registry's last row is S266 and `grep -cE '^\| S[0-9]+ \|' corpus/SOURCES.md` = 173, so the new row takes the next id. Scope per `claims.json` A8: the environment variable sets the flag that `-B` sets; the C1 knowledge entry cites it | reject if the committed snapshot holds no located quote of ≤25 words at the attribute's own anchor. Locator caution (QUALITY #91): r65 measured the nearest enclosing heading as the module-level `h1`, so the row's anchor must be `#sys.dont_write_bytecode` (the `<dt>` id), never a heading; an h1-only locator disqualifies the row and A8's sourced claim fails with it |
| (b) cmdline.html `-B` section, as this round's row | `corpus/SOURCES.md:183` (S266): `#cmdoption-B`, raw line 474 under h3 `Miscellaneous options` (line 451); snapshot sha256 `96f87232…`, 171073 bytes, fetched 2026-11-03T23:26:03Z | the switch's own stated effect, already carried with a 15-word quote | **reject as this round's row**: S266 already holds it; a second row for the same locator and scope would duplicate a standing row | admissible only if the new row's subject were the environment variable's flag semantics — that is (a)'s row — or if `sha256sum` of S266's snapshot disagreed with `96f87232…`; neither is measured |
| (c) the r65 instrument's `--recipe date` mode as "recipe A" | `tools/round-65/coverage-recipe.py:93`; `.ufo/waves/round-66/l1/controls/c2-do-nothing.json` condition 1 | the date mode's control value carries `knowledge_files 145`, `mapped 142`, `missing []` and the extra keys `population`, `population_dropped` (null for score/depth/revision/rule-blocks); recipe A's nine keys read `knowledge_files 145`, `mapped 142`, `missing` the three names, `coverage_score 9.79`, `depth_score 10.0`, `rule_blocks 27`, `citation_resolved_rules 27`. The two share only `mapped` | **reject**: a measured field difference, not a naming preference. The mode filters its population (`population != knowledge_files`) and emits a field recipe A never had (M65-2 pattern) | admissible as "recipe A" only if the mode emits recipe A's nine keys with equal values at the same rev. The r66 counter's `--equiv` is that test: `recipe_a_diffs {}` at both the base and the freeze (`l1/pre/dryrun-c2-selfcheck-at-base.json`, `w1/ExecCoverage/selfcheck-at-freeze.json`) |
| (d) a 30-vs-29 count fixture as evidence of the count assertion | `.ufo/waves/round-66/l1/controls/c1-do-nothing.json` a4; `.ufo/waves/round-66/w1/ExecClosure/verify.json` a4 | r65's `--manifest` on a one-entry-short copy: exit 0, `entries 29`, `ok true`, `findings []`; r66's counter on the same shape: `count_ok false`, `entries 29`, finding `count 29 != 30`, dropped entry `d8-14.7.173/d8` | **reject as a source**: a fixture demonstrates a red arm; it is not a source. The count's provenance is the frozen `CLOSURE` (30 entries) inside `tools/round-65/jsc-closure-matrix.py` plus r66's `COUNT = 30` | a fixture never becomes a SOURCES row; if a claim needs the count's provenance it cites the r65 instrument's `CLOSURE` and the r66 constant, not the fixture |

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M66-1 | stale-premise/boundary: the r65 closure check ran before the setup probe while the before-census was taken after it, so a cache written by the probe was invisible; the count was emitted, not asserted; `--skip-run` emitted a synthetic `closure.ok true` | `.ufo/waves/round-66/l1/controls/c1-do-nothing.json` a2 block: `r65_order_state {cache_present: [], entries: 5, ok: true}` against `cache_on_disk_after_probe ["__pycache__", "__pycache__/fixture_mod.cpython-315.pyc"]`; a4 block: `r65_exit 0`, `r65_manifest {entries: 29, findings: [], ok: true}`; a5 block: `r65_closure.ok true` at exit 1. Repaired: `w1/ExecClosure/verify.json` a2 `ok false`, finding `cache present after probe 2: __pycache__, __pycache__/fixture_mod.cpython-315.pyc`; a4 `count_ok false`, `count 29 != 30` | QUALITY #87 (clause → line) plus the r65 closure's routed defect 2 (M65-5) | the ordered post-probe scan folded into `closure.ok`, plus `COUNT = 30` asserted by equality, plus `skip_run_receipt` returning `closure: None, closure_claimed: False`. Shown red by the control's r65-order emulation and green by the a2/a3/a4/a5 arms (5/5, exit 0) |
| M66-2 | scope: the frozen "naming the files it hides" clause had no implementing line — `dropped = len(files) - len(population)` is an integer, and the filtered date population leaves `missing []`, so the hidden names appear nowhere | `tools/round-65/coverage-recipe.py:104-108` (`"population_dropped": dropped`, integer); `.ufo/waves/round-65/l1/c2-before-date.json`: `knowledge_files 144`, `population 142`, `mapped 142`, `missing []`, `population_dropped 2`, `mismatches 2`; new list: `recipe_a_hidden` = `2026-11-03-r65-jsc-closure-matrix`, `jsc-mapper-cli-contract`, `jsc-mapper-release-inventory` (`recipe_a_hidden_count 3`, base and freeze receipts) | QUALITY #87 — not applied at the r65 freeze; the r65 closure routed the defect (M65-4) | an emitted sorted list, tested for non-emptiness inside `selfcheck`'s `ok`. `w1/ExecCoverage/selfcheck-at-freeze.json` carries `recipe_a_hidden_count 3` and `recipe_a_hidden` is non-empty; the control's key list shows the old mode has no name key at all (`c2-do-nothing.json` condition 2: `population_dropped 3`, no names) |
| M66-3 | vacuous/control-contamination (this round's own, pre-freeze): the first C1 control run drove the a2 arm probe and the r65-order emulation through one fixture, so the pre-probe scan saw the cache the arm probe had just written and the control falsely "met" the a2 arm | `.ufo/waves/round-66/l1/controls/c1-do-nothing.py`: `# two SEPARATE fixtures: the r66 arms' fixture must not leave the cache the r65-order fixture would then scan before its own probe.` — with `fx66 = scratch / f"arm66-{arm_name}"` and `fx = scratch / f"ctl-{arm_name}"`. Corrected receipt a2 detail separates `r65_order_state.cache_present []` from `cache_on_disk_after_probe [...]`. **Stated limit: the pre-fix receipt was overwritten in place and is not retained** — `git show 78fa9666` holds only the fixed control and the 1/5 receipt | this seat, reading the control's construction and its own detail dump; the contaminated run's bytes are gone, so the class is evidenced by the fix's necessity, not by a filed receipt | one fresh fixture per arm, and a receipt whose a2 detail names both the in-order scan and the on-disk state after the probe. The corrected run scores **1/5**, which is the intended control score (only a1 is met by r65's order) |
| M66-4 | process/scope: the lane's own tool directory is not cache-free at the freeze, while the frozen toolchain is — the round's cache-free discipline is asserted only for `/home/vgpnk/.local/share/kaidoku-jsc` | `tools/round-66/__pycache__/closure-boundary.cpython-314.pyc` and `…/coverage-selfcheck.cpython-314.pyc`, mtime 2026-11-03 21:13:29 (the freeze commit is 21:13:44); `git check-ignore -v` → `.gitignore:1:__pycache__/`, so both are ignored, not tracked (`git status --porcelain --ignored tools/round-66` prints `!! tools/round-66/__pycache__/`). Contrast: `w1/ExecClosure/toolchain-cache-after.txt` is 0 bytes and `instrument-before/after.txt` both read `3c5cfb03…` / `1be9d046…` | this seat (census read); no seat reported the lane-tree cache | run any in-place import of an instrument under `-B`/`PYTHONDONTWRITEBYTECODE`, or extend the closure census to `tools/round-<N>/`. Impact on this round nil: the fixture probes run in `/fast` scratch under the venv interpreter (their cache names carry `cpython-315`, the lane's carry `cpython-314`), and the 30-entry manifest counts real files, not bytecode. The defect is that a reader of the pins cannot tell from the census that the lane tree was cache-free |

## Outcome

- **R66-C1** — verified on the executed after-arm: `w1/ExecClosure/verify.json`, 5/5 arms, `exit 0`, at the freeze
  `7b63dd5d…`, with `v1_pin 79a4dca4…` re-derived. a1 `ok true`, `cache_present []`; a2 `ok false` with
  `cache_present ["__pycache__", "__pycache__/fixture_mod.cpython-315.pyc"]` and the probe itself `ok true`
  (the cache is the probe's, not the fixture's); a3 `entries 30`, `count_ok true`; a4 `entries 29`, `count_ok false`,
  finding `count 29 != 30`, dropped entry `d8-14.7.173/d8`; a5 `closure null`, `closure_claimed false`, `verified false`,
  `runs_total 0` (`w1/ExecClosure/skiprun.json`). The pre-freeze dry run had the same 5/5 at exit 0
  (`l1/pre/dryrun-c1-verify.json`), the selftest is 30 cases clean (`l1/pre/selftest-c1.txt`), the instrument's
  sha256 is unchanged before and after the run (`3c5cfb03…`, `w1/ExecClosure/instrument-{before,after}.txt`), and the
  do-nothing control scores **1/5** (`l1/controls/c1-do-nothing.json`). Stated limit: a4's dropped entry is
  `list(CLOSURE)[0]`, so the arm demonstrates the assertion against one named truncation, not every possible one; the
  constant is 30 and the mutation is an off-by-one, not a subset test.
- **R66-C2** — **not verified on the freeze receipt.** `w1/ExecCoverage/selfcheck-at-freeze.json` (rev `7b63dd5d…`)
  reports `recipe_a_equivalent true` with `recipe_a_diffs {}` over the nine keys, `recipe_a_hidden_count 3` with the
  three names, and `mismatches 1`, `exit 1`: atom A1 `10.0` vs `10.0` is true, atom A2 is false — claimed
  `[142, 142]` against observed `[145, 145]`. That is the pre-repair state the predicate names: the row's repair is
  the round's deliverable and lands at the landing, so `--selfcheck --rev <landing>` is the only run that can score
  `mismatches 0`. The base arm is met: the same counter at `311079d8…` reports A2 false
  (`l1/pre/dryrun-c2-selfcheck-at-base.json`), and the control scores **0/3** (`l1/controls/c2-do-nothing.json`).
  The instrument's sha256 is unchanged (`1be9d046…`, `w1/ExecCoverage/instrument-{before,after}.txt`); the selftest is
  26 cases clean (`l1/pre/selftest-c2.txt`). This seat scores nothing here; it states the receipt it read and the
  revision the claim's own after-arm requires.
- **Outside closure** — still pending. The round's non-author closure has not run, and this lesson does not
  self-certify admit/reject agreement on the Gate rows or a verdict on either claim.

## Census

Round start: `l1/census-start.txt` prints `ok` for `kaidoku` and the 19 standing W04 duplicate-url warnings
(S033, S047, S054, S062, S069, S083, S090, S092, S102, S112, S117, S119, S123, S138, S142, S245, S246, S247,
S248 — unchanged names). `corpus/SOURCES.md` holds 173 rows at this read (`grep -cE '^\| S[0-9]+ \|'`), the last
being S266; the new sys row takes the next id at landing. Mined/rejected counters are not asserted here — no
census closing pass had run when this draft was written.

## QUALITY rows (drafts — the L1 lands them)

- **Row 104 (an ordered check's last step must be the one that proves no write).** In an ordered census the step
  that scans for artifacts runs after the last step that can create them, and its result folds into `ok`; a scan
  ordered before that step attests the pre-state only and is never reported as "no write". The receipt carries both
  the in-order value and the post-step scan, so a reader can see which one `ok` reads. Ground: r65's cache check ran
  before `python_probe` while the before-census was taken after it (M65-5(a)); round 66's control reproduces it —
  `.ufo/waves/round-66/l1/controls/c1-do-nothing.json` a2 reports `r65_order_state.cache_present []`, `ok true`, while
  `cache_on_disk_after_probe` holds `__pycache__/fixture_mod.cpython-315.pyc` — and the repaired counter folds the
  post-probe scan into `closure.ok` (`w1/ExecClosure/verify.json` a2: `ok false`, finding `cache present after probe 2:
  …pyc`). Fails when a receipt's `ok` is true from a scan that precedes the write-capable step. | `corpus/lessons/round-66.md` M66-1; `.ufo/waves/round-66/l1/controls/c1-do-nothing.json`; `.ufo/waves/round-66/w1/ExecClosure/verify.json` a2
- **Row 105 (a frozen count is asserted, not emitted).** A count a claim cites is a constant compared by equality and
  folded into `ok` and `findings`; `len(...) + k` emitted as a value is a description, not a check. The battery must
  include an off-by-one mutation (n−1) that turns `ok` false and prints both numbers. Ground: r65 emitted
  `entries = len(CLOSURE)+3` and asserted nothing, so a one-entry-short manifest ran `--manifest` exit 0 with
  `entries 29, ok true, findings []` (`l1/controls/c1-do-nothing.json` a4); round 66's `COUNT = 30` with `count_ok`
  inside `ok` turns the same shape red (`w1/ExecClosure/verify.json` a4: `count_ok false`, `entries 29`, finding
  `count 29 != 30`, dropped `d8-14.7.173/d8`). Fails when a count clause can be green for a count the claim declares
  wrong, or when the mutation is a no-op. | `corpus/lessons/round-66.md` M66-1; `.ufo/waves/round-66/l1/controls/c1-do-nothing.json` a3–a4; `.ufo/waves/round-66/w1/ExecClosure/verify.json` a3–a4
- **Row 106 (a control that reuses state between arms has scored nothing).** Each arm of a control or battery gets its
  own fresh fixture or work root, and the receipt names the per-arm root, or a detail key that proves the separation;
  if two arms share state, the later arm's scan reads the earlier arm's artifacts and its "met" is a statement about
  the earlier arm. Ground: round 66's first C1 control run drove the a2 arm probe and the r65-order emulation through
  one fixture, so the pre-probe scan saw the cache the arm probe had just written and the control falsely "met" the a2
  arm; the fix is in `.ufo/waves/round-66/l1/controls/c1-do-nothing.py` (`# two SEPARATE fixtures: the r66 arms'
  fixture must not leave the cache the r65-order fixture would then scan before its own probe`, with `arm66-*` and
  `ctl-*` roots per arm), and the corrected receipt's a2 detail separates `r65_order_state.cache_present []` from
  `cache_on_disk_after_probe [...]` at 1/5. Fails when two arms share a root, or when the receipt cannot show which
  root each arm's scan read. | `corpus/lessons/round-66.md` M66-3; `.ufo/waves/round-66/l1/controls/c1-do-nothing.py`; `.ufo/waves/round-66/l1/controls/c1-do-nothing.json`
