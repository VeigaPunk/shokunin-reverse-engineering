# R46W1RegA — round-46 C2 census registry rows (`reg-a`)

**Deliverable.** `.ufo/waves/round-46/w1/R46W1RegA/rows.md` — exactly three ready-to-paste
`SKILL.md` instrument-registry rows (7 cells, house schema, cell 1 = backticked path and
nothing else, verdict map binding `0=`, `1=`, `2=`, no literal `|` inside a cell, no backticks
outside cell 1). Receipts: `.ufo/waves/round-46/w1/R46W1RegA/receipt.md`,
`.ufo/waves/round-46/w1/R46W1RegA/probe.py`.

Read at the freeze `31820472784284727546808acc31b3ea1e73919b`, never from the worktree;
blob shas `57c628fe…` (round-41), `12857720…` (round-42), `e252a652…` (round-43).
No installs. Lane tree read-only; only my two report paths plus this file were written.

## 1. Why each cell says what it says

| instrument | cell 2 purpose | cell 3 verdict map | cell 4 self-test | cell 5 pinned value | cell 6 write scope |
|---|---|---|---|---|---|
| `tools/round-41/c1-counter.py` | R41-C1: four frozen AVM-layout BE SquashFS v4 carriers through REA, receipts + oracle + gap rule + fresh rerun + freeze-drift | 0 met (`met_target` and `carriers_matched` at the frozen target); 1 not met; 2 Unevaluable (`frozen_path_changed`, missing receipt/env, missing args, `--no-rerun`) | `--selftest --pkg65 <rea-agents 6.5.0 root>` → `cases 97`, `green_ok 12`, `red_ok 85`, exit 0 (ran, 2026-10-28T16:52:43Z) | `.ufo/waves/round-41/c1/{carriers.json,gap-rule.json}` (the `CARRIERS`/`GAPRULE` constants at 280–281; PRESENT at the freeze) | `--json-out` receipt, `--carrier-cache`, scratch `HYAKU_SCRATCH/kaidoku-r41` |
| `tools/round-42/c1-counter.py` | R42-C1: the v3 handler family (standard/ddwrt/broadcom, both endiannesses) through REA, receipts + oracle + gap rule + fresh rerun + stamped receipt identity | 0 met (`met_target`, or `--verify-receipt` found a matching `counter_sha256`); 1 not met (false binding, or the receipt identity does not describe the counter); 2 Unevaluable (incl. unreadable `--verify-receipt`, `--no-rerun`) | `--selftest --pkg65 <rea-agents 6.5.0 root>` → `cases 121`, `green_ok 14`, `red_ok 107`, exit 0 (ran, 2026-10-28T16:53:10Z) | `.ufo/waves/round-42/c1/{carriers.json,gap-rule.json}` (constants at 393–394; PRESENT at the freeze) | `--json-out` stamped receipt, `--work` scratch, `--carrier-cache` |
| `tools/round-43/heldout-gen-v4r43.py` | R43-C1: deterministic held-out carrier generation with the manifest FINALIZED from the measured declaration-vs-observed tuple | 0 clean (built, or tuple check/`--verify`/regeneration passed); 1 not met (REA run error, `--verify` or regeneration difference, CLI refusal); 2 `--tuple-check` found no `manifest.json` | `--selftest-tuple --scratch <dir>` → `tuple-check selftest: 17/17 passed`, exit 0 (ran, 2026-10-28T16:53:50Z) | `tools/round-42/fixtures.json` (fixture URL+sha256 pins; `tools/round-43/fixtures.json` is ABSENT, so `default_fixture_pins()` resolves there — probed) | `--out` carrier/manifest tree, `--scratch` tree + fixture cache |

Each row's claim was exercised, not inferred: `--help` (r41/r42/r43 exit 0), a `--no-rerun`
probe (both counters exit 2 with `rerun_disabled`), a missing-required-argument probe
(both exit 2), `--verify-receipt` on a non-existent file (r42 exit 2), a short-seed probe
(r43 exit 1), `--tuple-check` on a directory with no manifest (r43 exit 2), and both real
selftests plus the R43 offline tuple selftest (all exit 0).

## 2. Finding: `tools/round-43/heldout-gen-v4r43.py` takes an exit code outside {0,1,2}

`EXIT_DECLARED_TUPLE_UNOBSERVED = 3` at line 3140; returned by `finalize_manifest` (3335) and
by `run_tuple_check_dir` (3359) when a manifest's declared tuple is not the observed one,
reason `declared_tuple_unobserved`. This is by design and documented in the tool's own
`--help`. Per the seat rule it is kept **out** of the row: cell 3 binds only 0/1/2. Anything
reading exit 3 must not treat it as "not met" or as "could not evaluate" — it is a measured
refusal, and it never leaves a manifest behind.

Two consequences worth the L1's attention:

* The frozen `registry.py` `EXITMAP` is `\b([012])\s*[=:]`, so a row that also spelled
  `3=declared_tuple_unobserved` in cell 3 would still pass `strict_exit` (the `3` is not
  matched). The rows omit it anyway, per the seat rule; if the L1 wants the code recorded in
  the registry, the row is the only place that can carry it and it will not be scored.
* Nothing else in the three tools leaves {0,1,2}: both C1 counters were grepped for
  `return 3` / `exit_code: 3` / `SystemExit(3)` (no match), and their `SystemExit('<string>')`
  paths all exit 1 (measured: `r43-bad-seed`).

## 3. Calibration: my rows scored by the frozen checker, not by eye

The frozen `tools/round-46/{registry.py,census.py,gate.py,census.json}` were copied out of
the freeze and `score()` driven in-process over `rows.md` (`probe.py`; one process per mode):

* **Real frozen census (38 paths), my three rows only** — `header_ok true`, `registered` =
  the three, `thin []`, `absent_at_rev []`, `unregistered_count 35`, `failing
  ['unregistered: 35 of 38']`, exit 1. The exit 1 is the 35 census paths other seats own;
  every clause that concerns these three rows is clean.
* **Scope = exactly these three paths** — `unregistered []`, `thin []`,
  `absent_at_rev []`, `failing []`, `met_target true`, exit 0.
* **Mutants, each built from my own rows** — M1 prose-digit verdict map (`0 rows, 1 column,
  2 bytes`) → `thin` lists all three; M2 rows inside a fence → `registry_rows 0`, all three
  unregistered; M3 cell 0 a suffix (`round-41/c1-counter.py`) → exactly that path
  unregistered; M4 three-cell header → `header != house schema (7 cells)`. All four red, the
  unmutated control M0 green. The measure discriminates against the shape my rows actually
  have, which is the only calibration that matters here.
* **Census membership** — `scope_size 38`, `named_but_absent 0`, all three of my paths present
  as exact census strings, so cell 0 equality is achievable as written.

## 4. Risks the L1 should weigh before pasting

1. **Cell 5 for the two C1 counters names wave-state, not tool-adjacent, files.** Their pins
   live in `.ufo/waves/round-4{1,2}/c1/carriers.json` (+ `gap-rule.json`) and the counters read
   them **at the freeze commit** (`frozen_tables_valid`), which is why I named those paths; both
   are PRESENT at `31820472`. If the house convention is "a file beside the tool", these two
   rows are the odd ones out and should be reworded rather than reformatted.
2. **R43's pins live in round-42's tree.** `tools/round-43/fixtures.json` is ABSENT at the
   freeze and `default_fixture_pins()` falls back to `tools/round-42/fixtures.json`. A future
   edit to the round-42 pin file silently moves R43's fixture pins; that cross-round coupling is
   recorded in the row, and is worth a one-line note in the registry section preamble.
3. **Row 2's verdict map has to cover two subcommands** (`measure` and `--verify-receipt`).
   I bound each digit to one meaning that holds across both; a measure-only map would be
   thinner than the tool's real surface.
4. **`--selftest` for both C1 counters needs a `--pkg65`.** The commands in cell 4 name the
   parameter, not a path, so the row stays true if the package root moves. Both selftests did
   pass here against rea-agents 6.5.0 (already installed, nothing installed by me).

## 5. Not run (and therefore not claimed as passed)

* Full `measure()` at a revision for either C1 counter (needs the committed receipts and a live
  REA run per carrier), and `--selftest-rea` (needs a dev carrier). The rows' exit semantics
  rest on the source plus the probes above, not on a scored revision.
* `heldout-gen-v4r43.py --selftest` (needs a real seed, the image writer and the fixture pins);
  `--selftest-tuple` is the offline one and is what cell 4 names.
* The round-46 C2 forgery battery (`registry.py --selftest`, seven classes) and
  `attest.py` — the instrument-verification seats own those; I only borrowed `score()` to
  check my own output.
