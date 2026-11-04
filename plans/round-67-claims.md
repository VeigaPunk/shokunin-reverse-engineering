# Round 67 claims — kaidoku-shokunin (attempt 1)

Base: `a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92` (lane tip at round start; `jj-lane.sh state`
→ local = remote, ahead 0). Owned axes: coverage, depth, calibration — all at 10.0 on saturated
finite proxies (SCORECARD `## Saturation`). The stagnation nudge is **not** fired: the window is
N = 10 lane-rounds and a capability row entered the table in round 65; the lowest-axis obligation
is therefore live and is met by **coverage** (C1), which moves a frontier surface into Core rather
than re-scoring a proxy.

Two claims, distinct axes, causally separable (different instruments, different files, each
verifiable without the other). No fresh-start binding: of the last three closures r64 and r65 each
stopped honestly on their own predicates and r66 was admitted (both claims verified); no closure
was rejected three times in a row.

Instruments were committed **before** this file (the QUALITY #33 order) with their do-nothing
controls and pre-freeze receipts (`.ufo/waves/round-67/l1/pre/`); the carry-in LOG entry is an
ancestor of this freeze commit (QUALITY #34 and the M65-3 order check). Each clause of both
predicates is traced to the line that evaluates it (QUALITY #87), and each predicate sentence is
byte-identical in this file, `.ufo/waves/round-67/claims.json`, the instrument's `PREDICATE`
constant and every receipt (QUALITY #68; the instruments read the predicate from the claims file
and refuse on a mismatch — the r66 reviewer's routed F1 pattern).

## R67-C1 — coverage, frontier → core: LE AVM-marker SquashFS v4 under a class rule

Round 50 measured genuine AVM-marker little-endian SquashFS v4 members (`hsqs`,
`mkfs_time == bytes_used`) on four chain-pinned vendor carriers and published every oracle regular
file on all four, but the claim stopped at 2 of 4: its frozen gap rule
(`tools/round-50/gap-rule.json`) made every `char-device` oracle entry a per-row **required**
disposition, and the two FRITZ!Box carriers hold 13 char devices each (`dev/pts/0-7`,
`dev/tiatm`, `dev/led`, `dev/ttyp0-2`) for which no extractor record can exist — an extractor
that writes regular files cannot create a device node. The rule had been generalised from the
Cable carriers, where exactly one char device (`247:0`) exists.

**Surface moved:** `squashfs_v4_le` on LE AVM-marker (`hsqs`) members, Frontier → Core on the same
four pinned carriers. Unmoved at the base: `PROVINCE.md` and `corpus/README.md` list "LE AVM
members (`hsqs`)" as Frontier (`grep -n 'LE AVM' PROVINCE.md corpus/README.md`), and the four
envelopes score `gaps_ok` on 2 of 4 under the round-50 rule (`l1/pre/control-dryrun.json`).

**Predicate** (byte-identical in this file, `claims.json`, `PREDICATE` in the counter, every
receipt):

> R67-C1 is verified iff the pinned round-50 scoring engine, run under the round-67 gap rule and
> the round-67 documentation bindings, reports carriers_matched 4 of 4 with met_target true and
> exit 0 at the measured revision, while the four frozen envelopes scored under the round-50 rule
> report gaps_ok on 2 of 4.

Counter: `tools/round-67/avm-le-counter.py --score --root <lane> --rev <rev> --freeze <freeze>
--pkg65 <rea-agents 6.5.0 root> --carrier-cache <cache> --work <scratch> --out <receipt>`
(`sha256` recorded in `claims.json`). Exit 0 verified / 1 not verified (each failing clause and
binding named) / 2 could-not-evaluate.

Clause → line trace (QUALITY #87):

| clause | line that evaluates it |
|---|---|
| pinned round-50 scoring engine | `load_engine()` — `sha256_file(path) != ENGINE_PIN` raises; the receipt carries `engine {path, sha256}` |
| run under the round-67 gap rule | `patch_engine()` sets `mod.GAPRULE = RULE_V2`; the engine's `measure()` reads `plan_raw = show(root, freeze, GAPRULE)`, builds the model with `gap_rule_model(plan_raw)` and calls `disposition_check(gaps, diags, nonreg, model, root, od)` per carrier |
| round-67 documentation bindings | `patch_engine()` sets `ENTRY`, `STEM`, `CORE_HEADING`, `FRONTIER_MARK`, `OPENED_DATES`, `AFTERDIR`; the engine's bindings block computes `province_core_section`, `province_core_row`, `frontier_note`, `entry_present`, `sourced`, `coverage_map_row` |
| carriers_matched 4 of 4 | `measure()`'s `matched += bool(all(d.get(x) is True for x in CLAUSES))` over `IDS`, with `CLAUSES` patched to drop `carrier_fresh_ok` (a re-measurement of the same pinned carriers cannot be fresh; the drop is disclosed in `patches.dropped_clauses`) |
| met_target true | `measure()`'s `res['met_target'] = bool(carriers_unchanged and gap_rule_unchanged and carriers_matched == target and all(b[x] is True for x in BINDINGS))` |
| exit 0 at the measured revision | `score()`'s `"exit_code": 0 if res.get("met_target") else 1`; the receipt's `rev` names the measured revision, and the engine's `receipt_fresh` requires the receipt's first-add commit to descend from the freeze |
| 2 of 4 under the round-50 rule | `control()`'s second `disposition_check` call with `model_r50` over the same four envelopes; `gaps_ok_round50` counts them |

Kill rule: any carrier clause false under the round-67 rule, a drifted engine / rule / carrier
table, a carrier whose pinned bytes differ, a post-freeze instrument edit, or a run that needs the
predicate changed → **not verified**; the miss is reported, never narrowed.

Before-arm (do-nothing control, committed before data): `l1/pre/control-dryrun.json` — the same
four frozen envelopes and the same engine under the **round-50** rule score `gaps_ok` on **2 of 4**
(g7581 and g7582 fail on their char devices), the round-67 rule on 4 of 4, and the two red
fixtures fire: removing one symlink's `unpublished-entry` gap still fails under the round-67 rule
(`round67_rule_still_fails true`), a char-device path published as a regular file is named by the
publication check (`publication_check_names_it true`), and a junk rule that also waives symlinks
passes the first red fixture (`junk_rule_would_pass true` — the waiver must stay scoped).
After-arm: `--score` at the record, after the data runs and the documentation bindings land.

## R67-C2 — depth, gate integrity: the two round-66 mutation survivors

Round 66's mutation wave disclosed two survivors (`corpus/lessons/round-66.md` M66-5/M66-7;
`.ufo/waves/round-66/w1/MutClosure.md`, `.../MutCoverage/mutants/M2/`): M5
(`tools/round-66/closure-boundary.py` `arm()` returns `passed: True` unconditionally — the
counter's `--selftest` never calls `arm(`) and M2 (`tools/round-66/coverage-selfcheck.py`
`recipe_a_equivalence()` returns equivalent without running the block — the clause is already true
at a green revision). Round 66 routed both to the next freeze.

**Rule added:** a mutation survivor is closed by a selftest case that exercises the mutated
function on a *false* input — a false arm condition and a doctored recipe-A block — so the mutant
and the pristine counter produce different case outcomes.

**Predicate** (byte-identical in this file, `claims.json`, `PREDICATE` in the battery, every
receipt):

> R67-C2 is verified iff the round-67 selftest battery kills both round-66 mutation survivors --
> the closure counter whose arm() returns passed true unconditionally and the coverage counter
> whose recipe_a_equivalence returns equivalent without running the block -- while both pristine
> counters stay green, and the round-66 selftests alone leave both survivors alive (0 of 2).

Counter: `tools/round-67/mutation-battery.py --score --root <lane> --rev <rev> --work <scratch>
--out <receipt>` (`sha256` recorded in `claims.json`). Exit 0 verified / 1 not verified / 2
could-not-evaluate.

Clause → line trace (QUALITY #87):

| clause | line that evaluates it |
|---|---|
| the battery kills both survivors | `score()`'s `ok` requires `killed_after == len(SURVIVORS)`; each verdict's `killed_after` is `after_rc != 0 and EXPECTED_CASE[name] in failed_cases` |
| the closure survivor (`arm()` always passes) | `closure_mutant()` rewrites the single `"passed": bool(passed)` line to `"passed": True`; `selftest()`'s `check("arm-false-bound", cm.arm("ctl", False, {})["passed"], False)` fails on it |
| the coverage survivor (equivalence without running) | `coverage_mutant()` replaces the `subprocess.run`/diff span with the r66 M2 constant return; `check("equiv-doctored-bound", ...)` and `check("equiv-doctored-diffs", ...)` fail on it |
| both pristine counters stay green | `selftest()`'s `closure-selftest-green` / `coverage-selftest-green` and `score()`'s `pristine` block (both `SELFTEST CLEAN`, 30 and 26 cases) |
| the r66 selftests alone leave both alive (0 of 2) | `control()`'s `killed_before` / `survived_before` over the same two mutants |

Kill rule: a survivor that the battery does not kill, a case that passes on a mutant, a pristine
counter that is not green, a drifted or absent pinned r66 instrument, a post-freeze instrument
edit, or a run that needs the predicate changed → **not verified**, never narrowed.

Before-arm (do-nothing control, committed before data): `l1/pre/control-dryrun-c2.json` — the two
mutants scored by the round-66 selftests alone: `killed_before 0`, `survived_before 2` (both
`SELFTEST CLEAN`, 30 and 26 cases). After-arm: `--score` at the record → `survived_before 2`,
`killed_before 0`, `killed_after 2`, exit 0.

## Frontier step (not a third claim)

- `corpus/SOURCES.md`: one row opened this round (the Linux kernel SquashFS documentation's
  device-node inode text, the ground for the class rule), with the Gate block carrying this
  round's access date and a located quote of at most 25 words. The C1 knowledge entry cites that
  row (**sourced claim**).
- Census before → after with `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
  kaidoku`; both outputs and exit codes recorded.
- One mistake mined into `corpus/lessons/round-67.md` `## Mistakes` with a red demonstration.
- Assimilation: `merge/kaidoku/` — none this round (the jsc theme was adopted in round 64 and no
  remaining staged theme fits a SquashFS class rule); `considerthese/` is absent (measured by
  `ls`, exit 2).

## Round shape

One v1 wave, 12 seats (policy band 8–16): 3 executors, 1 reviewer, 1 critic, 2 mutation-testers,
1 sentinel, 1 scout, 1 connector, 2 scribes. Attack seats = reviewer + critic + 2 mutation-testers
= 4/12 = 33 % ≥ 25 %. One connector seat. The L1 holds the canonical planner seat (the validator
rejects a `planner` role). Seat outputs land under `.ufo/waves/round-67/w1/<seat>/`; the L1
integrates and lands. No residual call is planned.
