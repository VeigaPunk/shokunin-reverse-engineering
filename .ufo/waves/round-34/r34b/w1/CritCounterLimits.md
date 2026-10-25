# CritCounterLimits — what the R34-C2 counter cannot prove

Seat: `L1Kaidoku34-2.CritCounterLimits` (critic, limit enumeration). Round 34, run-6 re-dispatch, wave 1.
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Frozen instruments at `c79bbe7b0959132b9873ff3431cf5eb313b58b33`
(`.ufo/waves/round-34/r34b/claims.json`, claim `R34-C2`). R34-C1 (GNU version-needs) was not opened, executed or scored.
All probes ran on a copy of `tools/` under `/fast/scratch/hyaku/kaidoku-r34b/w1/CritCounterLimits/clone`; no lane file was written,
no lane VCS command was run beyond read-only `git log/diff/show/cat-file`, no ELF was executed, no network was used.
No tool was installed (nothing was needed); pacman untouched.

## 0. Reproduction and pin binding (positive findings, so the limits below are limits of *these* bytes)

| step | command | exit | UTC |
|---|---|---|---|
| repro | `/usr/bin/python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root <scratch>/clone --rev c79bbe7b…` | 0 — `GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-` | 07:20:27–07:20:29Z |
| pins | sha256 of all 26 `pins` entries vs `claims.json` | 26/26 match | 07:20Z |
| freeze drift | `git diff --stat c79bbe7b..HEAD -- tools/round-34` (empty); blobs `replay-gate.py 8fa94b23…`, `c2-shortcut-gate-counter.py 41d59703…`, configs `4483f385…`/`72b12941…` identical at freeze and working tree | empty diff | 07:23:38Z |
| controls | the five declared controls re-run through the pinned counter | `always-clean` rc=1, `no-positive-check` rc=1, `vacuous-no-floor` rc=1, `junk-clean` rc=1, `do-nothing` rc=2; all five stdout lines byte-identical to the checked-in `.txt` files | 07:23:07Z |

So the arithmetic reproduces and the instruments have not drifted. Everything below is nonetheless reachable on these exact bytes.

## 1. Strongest counterexample: an unregistered instance of a class the gate's own obligation names meets the green target

`replay-gate.py:4-8` states the obligation over "input size, input label, whole-file digest, **fixed byte slices**, the record order".
The green transform (`mini-counter.py:57-83`) reorders only the name pool and rewrites each record's `u16 name_off`; the six-byte
`(flags,value)` tail of every record array entry is byte-identical before and after.

I wrote a reader that hashes exactly those tails and returns a memorized record list, never opening the name pool, never reading `name_off`
(`/fast/scratch/hyaku/kaidoku-r34b/w1/CritCounterLimits/prefix_reader.py`, table generated from the fixtures in `mk_prefix.py`):

| probe | command | observed | UTC |
|---|---|---|---|
| A | `mini-counter.py --root <clone> --control-reader prefix_reader.py` | `matched=8 target=8 met_target=True`, exit 0 | 07:21:54–07:21:57Z |
| A2 | `naive-counter.py` with the same reader | `matched=8`, exit 0 | 07:21:54–07:21:57Z |
| B | `replay-gate.py --config cfg_prefix.json` (reader registered as class `prefix-keyed`) | `REPLAY_GATE_REFUSED … shortcuts_over_target=prefix-keyed`, exit 2 | 07:21:54–07:21:57Z |

Consequence: the gate's discriminator is *sound conditional on registration* and the frozen registration set is not faithful to the
obligation. The registered `fixed-slice` representative (`readers/fixed_slice.py`) is a printable-run scanner from offset 64 upward — it is
not a fixed-slice replay at all, and it dies because the permutation moves the strings. The class itself survives. `REPLAY_GATE_CLEAN`
therefore certifies "these seven shipped programs fail", not "no structure-blind reader of the named classes meets the target".
Zero coverage is claimed for the class space; the floor is three entries (`replay-gate.py:31,58`) and the only per-entry checks are
non-empty `path`/`class` and string-uniqueness of `class` (`:61-66`).

Corollary, measured: three class names all pointing at the same `all_false.py` clear the floor and produce
`REPLAY_GATE_CLEAN … shortcuts_below_target=3`, exit 0 (07:23:33Z). Class names are labels, not semantics.

## 2. What each layer's "receipt" actually binds

Three layers of self-report stack: reader stdout → counter receipt → gate rows → C2 clauses.

| limit | code line | probe (exit, UTC) | disclosed? |
|---|---|---|---|
| **`met_target` is trusted; `matched` and `target` are never cross-checked.** The predicate says "none meets the target"; the gate tests a boolean the counter supplies. A counter reporting `matched=8, target=8, met_target=false` for every shortcut yields `REPLAY_GATE_CLEAN` exit 0 with all seven shortcuts at 8/8. | `replay-gate.py:93-100` | D (07:22:04–07:22:11Z) exit 0; rows `[('structural',8,True), ('all-false',8,False), … ('label-memorization',8,False)]` | **not disclosed** |
| **Rows die at the gate layer.** `run_counter` returns only `matched/target/met_target/finding/exit`; per-reader `exit`, `transformed_sha256` and `input_size` are dropped. | `replay-gate.py:100` | code fact; C2 reads rows only for the green positive (`c2-…py:97-98`) | **not disclosed** |
| **A crashing reader is scored "below target".** Reader `sys.exit(7)` → counter row exit 7, matched 0 → `REPLAY_GATE_CLEAN`, `shortcuts_below_target=8`. Refuted and broken are indistinguishable. | `mini-counter.py:116-128`; gate floor at `:123` | L (07:24:04Z) exit 0 | **not disclosed** |
| **Class-label collision with the positive control suppresses refusal.** `over` excludes every row whose class equals `positive_control.class`, but `load_config` only rejects duplicate classes *among shortcuts*. An 8/8 shortcut labelled `structural` gives `REPLAY_GATE_CLEAN`. | `replay-gate.py:123` vs `:61-66` | C (07:21:57Z) exit 0, `shortcuts_below_target=6` | **not disclosed** |
| **The positive control's *identity* is never checked.** The frozen positive row is only `met_target` (`:119`) / `matched == 8` (`c2-…py:118`). Replacing the positive with the slice-keyed memorizer of §1 still yields `REPLAY_GATE_CLEAN`. | `replay-gate.py:119`; `c2-…py:118` | I (07:22:46Z) exit 0; E (07:22:04–07:22:11Z) shows the same row can be fabricated | **not disclosed** — but see §3, the *guard's presence* is covered |

## 3. The one thing the assignment asks about that IS covered: positive-guard enforcement

The question "can the counter tell a gate that enforces the positive guard from one that only reports the row" answers **yes for
enforcement, no for meaning**.

- `SELFTEST_CASES` contains `positive-below` (`replay-gate.py:161`: positive 3/4, every shortcut 0 → expect UNEVALUABLE
  `positive_control_below_target`), and `MUTANTS` contains `no-positive-check` (`:167`). A gate that merely reports the positive row and
  proceeds cannot pass that case.
- Measured: the control gate `gate-no-positive-check.py` re-run through the pinned counter gives
  `selftest_failures=2 mutants_killed=2 clauses_failed=mutants_killed,selftest_clean`, rc=1 (07:23:07Z) — the mutation is killed.

What is *not* covered is anything about what the positive row means: §2 row 5 (fabricated or memorizing positive still CLEAN), and the
positive's class name is only a string. The predicate's clause "while a registered structural reader does [meet the target]" is therefore
satisfied nominally.

## 4. The mutant score is a three-anchor presence test, not a mutation score

`MUTANTS` is a three-entry hardcoded list of literal-text replacements (`replay-gate.py:165-172`), executed against the gate's own source
read at `:175`. `mutants_killed == 3` (`c2-…py:114`) compares a count to the size of that list; a surviving *unlisted* mutant is invisible,
and an extra listed mutant would flip the clause to MISS.

Measured survivor: a copy of the gate with the counter-target binding removed (`:98` `if target != config["target"]:` → `if False:`).

| probe | command | observed | UTC |
|---|---|---|---|
| F | C2 counter `--gate <scratch>/gate_nobind_target.py` | `GATE_COUNTER_OK … mutants_killed=3 clauses_failed=-`, exit 0 | 07:22:04–07:22:11Z |
| F2 | that mutant's own `--selftest` | `{"cases": 12, "failures": 0, "mutants_killed": 3}`, exit 0 | 07:22:04–07:22:11Z |

Reason it is undetectable: every selftest config is built with `"target": scenario["target"]` (`:193`) and `SELFTEST_COUNTER` echoes
`scenario["target"]` (`:150`), so `counter_target_mismatch` is never exercised by any case. The gate that stops binding the counter's target
to the config's target passes both its own selftest and the frozen claim.

## 5. The six-clause conjunction is satisfiable by a gate that performs no evaluation

`clauses` (`c2-…py:112-119`) reads: `selftest_exit/failures` and `mutants_killed` from the gate's **stdout**, `red`/`green` verdict strings
and `positive_matched` from the gate's **JSON**, and `gate_present` from a filesystem check. A 1,979-byte mock gate
(`/fast/scratch/…/mock_gate.py`) that keys on `"naive" in config_basename`, prints the selftest summary and emits the expected verdict/rows,
returns `GATE_COUNTER_OK … clauses_failed=-`, exit 0 (probe E, 07:22:04–07:22:11Z). The claim's own control `gate-junk-clean.py` (753 bytes) is the
same shape and fails **only** `red_refused` — i.e. `selftest_clean`, `mutants_killed`, `green_clean`, `green_positive_meets_target` and
`gate_present` are all stdout/file-fed, and exactly one clause (exit 2 + the literal string `label-memorization`, `:115-116`) carries
behavioural weight.

## 6. Provenance the counter does not establish

| limit | code line | probe | disclosed? |
|---|---|---|---|
| `--rev` is echoed, never verified: no VCS call exists in the counter, and no `--root`↔revision binding. A run labelled `deadbeef…` returns exit 0 and writes that revision into the receipt. | `c2-…py:73`; `grep -E '\bgit\b|\bjj\b' ` → no match | G (07:22:11Z): `GATE_COUNTER_OK`, `measured_revision=deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` | **not disclosed** |
| The 26 `pins` are never read by either instrument; nothing verifies the counter's digest. (By hand: 26/26 match, so the *current* run is bound — the instrument does not prove it.) | no pin read anywhere in `c2-…py`/`replay-gate.py` | pin check §0 | **not disclosed** |
| `--gate` is a production-legal override — a module-global assignment at `:75`, help text says "Control only" (`:69-70`) with nothing enforcing it. A receipt produced with an override is byte-identical in verdict to a pinned run; only `gate_path` differs. | `:69-75`, `:80-81` | E/F both exit 0 | **declared, unenforced** |
| Every reader and counter is executed from paths under `--root` at whatever bytes are there (`c2-…py:46-48`, `replay-gate.py:76-83`); no digest. Composed with the unverified pins, a mutated `mini-counter.py` under a clone passes C2 unchanged. | as cited | inference from E + §0 pin non-enforcement | **not disclosed** |

## 7. What the green case is made of (evidential weight of `REPLAY_GATE_CLEAN`)

- Fixtures are author-built: 8 × exactly 512 bytes (`build.py:17`; `mini-counter.py:26,35` rejects any other size). Size-keyed is dead by
  construction ("input size cannot identify a fixture", `build.py` docstring — **disclosed**). Whole-file digest is dead because the
  permutation rewrites the pool (`digest_keyed.py` hashes the whole file). Fixed-offset string scans die because strings move.
  So of the seven registered classes, **at most one (label-memorization) is a live contest in the green case**, and the live
  fixed-slice instance lives outside the set (§1).
- The red case uses a *different counter* (`naive-counter.py`) with **zero** transform (`naive-counter.py:47` reads fixtures in place,
  docstring says so). It demonstrates refusal for identity surviving at all, not for a counter that defeats label but not slices — the case
  §1 measures and that the green CLEAN absorbs.
- `matched == TARGET` is exact (`mini-counter.py:131`, `naive-counter.py:60`), so 7/8 is "below target" and therefore "refuted": a
  near-structural reader and a pure label memorizer score the same. Not disclosed.
- One permutation per fixture under one default seed (`mini-counter.py:139`, `permute` called once per fixture at `:113-116`); no
  multiplicity, no second draw, no confidence statement. A shortcut that survives one shuffle is certified. Not disclosed.
- `green_positive_meets_target` hardcodes `== 8` (`c2-…py:118`) rather than reading the config target, while the receipt carries
  `TARGET` as a constant dict (`:28`). Two authorities for the same number; the kill rule forbids changing target, so this is latent, not live.
- `shortcuts_below_target` is computed and printed (`:109-110`, `:131`) but appears in no clause — a number in the verdict line that cannot
  fail. Cosmetic-but-misleading; not disclosed.
- The `control_plan` is prose in `claims.json`; there is no control clause in `clauses` (`:112-119`). A missing control receipt leaves
  `met_target` true. (By hand all five reproduce, §0.)
- The synthetic counter is not the production subject: the predicate is about "a finite structural-decoding counter", the scored counter is
  `mini-counter.py` on MREC bytes. **Disclosed** in `instrument_notes` (`author_built_fixtures`, `no_production_reader_run`) — this is the one
  honest scope reduction, and it bounds everything else: the gate is an admission instrument for the *method*, not evidence about the ELF reader.

## 8. Identity defect in the frozen claim (separate from the limits)

`claims.json` `predicate_identity` asserts "The same sentence is the gate config's `predicate` field, the C2 counter's PREDICATE constant and
the receipt label." Measured (07:23:38Z, string equality in Python):

```
claims_predicate == mini_config   : True
claims_predicate == naive_config  : True
claims_predicate == c2_PREDICATE  : False
claims_predicate == receipt       : False
c2_PREDICATE     == receipt       : True
```

Both configs and the claim carry "…is frozen only after registered structure-blind shortcut readers are scored under the counter's own
predicate and none meets the target, while a registered structural reader does." The counter constant (`c2-…py:23-27`) and therefore the
production receipt `.ufo/waves/round-34/r34b/after/c2-at-instruments.json` carry a different, operational sentence ("the committed replay gate
refuses the shape-only counter whose label-keyed memorization meets its target …"). Same intent, different text: the frozen claim's
identity statement is false as written. Duplicate authority for the predicate, and the receipt does not carry the frozen wording.

A related, minor collision: `readers/label_keyed.py` is pinned and shipped but registered in neither config, so a pinned shortcut program is
never scored.

## 9. Impacted axes

- **depth** (the claimed axis): the acquisition is real but narrower than the receipt reads. `REPLAY_GATE_CLEAN` is a seven-program
  statement; §1 exhibits a structure-blind 8/8 instance of a class the obligation names, outside the set.
- **calibration**: `mutants_killed`/`selftest_failures` are stdout-fed (§5) and the mutant list is a three-anchor sample (§4); a survivor was
  measured. Calibration cannot increase on this evidence.
- **coverage**: no code binds a class name to a program, and the floor is 3 (§1). Any coverage reading of "seven classes" is a reading of the
  config file, not of the gate.
- **identity**: §8 — one frozen sentence about predicate identity is false.

This is a fixable defect set, not a "judge must reject" tradeoff: every gap above is closable by a config/instrument revision that does not
touch the predicate. It is *not* closable inside the freeze, because §1 would flip the pinned green verdict and §8 changes a pinned digest.

## 10. Smallest safe corrections, ranked by axis gain per unit of change

1. **Register a faithful `fixed-slice` representative** — the (flags,value)-tail memorizer of §1 as its own class (probe B proves the gate then
   refuses it). Do this in a new instrument revision, not by editing `gate-config-mini.json`; the frozen green clause cannot survive it.
2. **Bind class → program by digest**: add `"sha256"` to each `shortcuts[]`/`positive_control` entry and verify it in `run_counter` before
   scoring; delete or register `readers/label_keyed.py`. Makes "registered set" an enumerated, pinned set (closes §1 and §6-row-2).
3. **Cross-check receipt consistency**: require `met == (matched == target)` and `0 <= matched <= target` (`replay-gate.py:93-100`) and add a
   selftest case where they disagree (closes §2-row-1, the sharpest remaining hole).
4. **Extend the duplicate-class rejection to `positive_control.class`** (`:66` vs `:123`) (closes §2-row-4).
5. **Propagate reader liveness**: keep per-row `exit`/`payload-readable` through `run_counter` and return UNEVALUABLE, not "below target", when a
   shortcut's reader did not run (closes §2-row-3).
6. **Make the mutant score a coverage statement**: derive `MUTANTS` from the branch set, assert `mutants_killed == len(MUTANTS) and
   len(MUTANTS) >= N`, and add the counter-target-binding mutant that survived probe F (closes §4).
7. **Fix the predicate identity**: make the counter's `PREDICATE` literal the frozen sentence, or record the operational sentence in a distinct
   `predicate_operational` field and have the receipt echo both (§8).
8. **Either clause `shortcuts_below_target` against the registered count, or drop it from the verdict line** (§7); same for the hardcoded `== 8`.

## Verdict

`REPLAY_GATE_CLEAN` is a true statement about the seven shipped programs and a false statement about the class space: a structure-blind
(flags,value)-tail replay of a class the gate's own obligation names reaches 8/8 under the green counter, and a gate that drops the
counter-target binding, a counter whose `met_target` contradicts `matched`, a crash-as-refutation, and a no-op mock gate all satisfy the C2
clauses. Limits §1–§7 are undisclosed by the instruments (only the synthetic-fixture scope and the status quo of "reads the counter's own
receipt fields" are disclosed), and the frozen `predicate_identity` sentence is false for the C2 constant and the production receipt.
Smallest safe path: new instrument revision adding a digest-bound, liveness-checked class set with a faithful fixed-slice representative and a
receipt-consistency clause; the frozen claim's green target cannot hold once that representative is registered.

COUNTER_LIMITS verdict: green target falsified by an unregistered fixed-slice replay (8/8); 7 undisclosed limit classes + crash-as-refutation + no-op-gate satisfiability; predicate_identity false for the C2 constant and the production receipt; C2 fixable only by a new instrument revision, not inside the freeze. utc=2026-10-25T07:24:05Z
