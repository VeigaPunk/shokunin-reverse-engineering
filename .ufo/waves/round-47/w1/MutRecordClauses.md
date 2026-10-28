# MutRecordClauses — mutation probe of `tools/round-47/record.py` (R47-C2)

Seat: `MutRecordClauses` (UFO-FSD mutation tester). Round 47, wave 1, lane `kaidoku-shokunin`.
Scope: the frozen R47-C2 counter only; `tools/round-47/exact.py` (R47-C1) was not touched.

- **Measured bytes** `tools/round-47/record.py` sha256 `abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7`,
  copied with `git show <rev>:tools/round-47/record.py` at rev `04469ee8f30b9c086000c518bc482693282dd931`.
  Re-checked at `31b092d17e77f5064c919383a9bc1e6cbfd2d1ff` and `a0753786…`: same sha256, so the probe is
  revision-stable across the A2→A5 record revisions (an earlier pass on the pre-A5 bytes `c704c3d4…` gave
  identical verdicts; A5 only moves the ghost forgery inside the corrections section).
- Scratch `S=/fast/scratch/hyaku/kaidoku-r47/MutRecordClauses`; `TMPDIR=HYAKU_SCRATCH=$S`. Lane tree read-only
  throughout; the lane's `record.py` sha256 was `abf352573…` before the first command and after the last.
- Detector = the counter's own `--selftest` (10 cases; exit 0 = all pass), plus an authored probe suite
  (`probe.py`, 12 cards) for guards the selftest cannot see. Both are copied into `receipts/`.

## Commands actually run

```sh
S=/fast/scratch/hyaku/kaidoku-r47/MutRecordClauses; export TMPDIR=$S HYAKU_SCRATCH=$S
REV=$(git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD)
git -C …/kaidoku-shokunin show "$REV:tools/round-47/record.py" > "$S/mut/tools/round-47/record.py"
git -C …/kaidoku-shokunin show "$REV:tools/round-46/gate.py" > "$S/mut/tools/round-46/gate.py"
python3 -I -B "$S/mut/tools/round-47/record.py" --root "$S/mut" --rev HEAD --selftest   # baseline, exit 0
python3 "$S/harness.py"                     # 12 mutants, one guard each, selftest per mutant
python3 "$S/probe.py" "$S/mut" mut          # 12 probes on pristine bytes
python3 "$S/probe.py" "$S/mutants/<name>" <name>   # 12 probes per mutant (10 mutants)
```

Baseline (pristine bytes): `--selftest` exit **0**, 10 cases, stdout sha256
`505afadee8e7872b2b8c3114d3a6b739db68441b31b625e866ad91847f361c20`. A baseline failure would have made every
verdict inconclusive; there was none. Each mutant is generated fresh from the pristine bytes (anchor asserted to
occur exactly once); the pristine copy's sha256 was unchanged after the whole matrix
(`pristine sha unchanged: True`, `mutations.json`).

## Mutation table (one guard deleted per mutant)

`selftest` = counter's own detector. `probe` = the authored card that flips. Bold verdict = killed.

| mutation | guard site | selftest exit | detected by (selftest case) | detected by probe | verdict |
|---|---|---|---|---|---|
| `M0-control-comment` | docstring line (control) | 0 | — | — | survived (expected) |
| `M1-classes-guard` | 379 `no atoms of class(es)` | 0 | **none** | `P1-missing-rev-class` 1→0 | survived by selftest, **killed** by probe |
| `M2-mismatches-guard` | 381 `mismatches N != 0` | 1 | `red-non-empty-window` (only) | — | **killed** |
| `M3-corrections-min-guard` | 383 `corrections N < 2` | 1 | `red-one-correction` | — | **killed** |
| `M4-corrections-bad-guard` | 385 `corrections that do not re-derive` | 1 | `red-ghost-exemption`, `red-correction-total-false`, `battery-discriminates` | `P7` 1→0, `P10` 1→0 | **killed** |
| `M5-exempt-max-guard` | 387 `exempted N > 3` | 0 | **none** | `P5-four-exemptions` 1→0 | survived by selftest, **killed** by probe |
| `M6-battery-guard` | 390–392 battery loop (both keys) | 0 | **none** | `P6` 1→0, `P6c` 1→0 | survived by selftest, **killed** by probe |
| `M6b-battery-greenonly` | 390 drops `forgeries_green` key | 0 | **none** | `P6` 1→0 | survived by selftest, **killed** by probe |
| `M6c-battery-countonly` | 390 drops `correction_forgeries` key | 0 | **none** | `P6c` 1→0 (SYNTHETIC input, see F4) | survived by selftest, **killed** by probe |
| `M7-ghost-exemption-guard` | 365 `if not historical` (ghost-exemption append) | 0 | **none** (see F5) | `P7-ghost-atom-existing-rev` 1→0 | survived by selftest, **killed** by probe |
| `M8-two-sections-guard` | 310 `len(secs) != 2 → 2` | 0 | **none** | `P8-single-round-section` 2→0 | survived by selftest, **killed** by probe |
| `M9-axes-correction-parse` | 50 `CORR` gains the `axes` alternative (fix-mutant) | 0 | **none** | `P9-false-axes-correction` 0→**1** | survived by selftest; probe shows the fix |

Guard sites: 6 `failing.append` sites (the battery loop counts once, split into three mutants), one
`corrections_bad.append` site (365), one structural `return 2` (310). **Selftest kills 3 of the 8 sites;
5 survive it.** Every survivor is load-bearing in a real call path — the probes prove it. The counter is
therefore not vacuous; its *detector* is thin.

## Probe suite: expected vs actual on pristine bytes

Fixture: one-commit-per-file git repo under `$S/fixture-*` (`git rev-parse --show-toplevel` asserted equal to
the fixture dir before the first commit), 2 dispatch files for each of rounds 8 and 9 (`counts.spawn` 1 each),
`tools/x/`, one knowledge file mapped in `corpus/README.md`. Cards are passed straight to `evaluate_text`.

| probe | pristine exit | receipt | intent |
|---|---|---|---|
| `P0-valid-control` | 0 | `failing []` | a green card is green (harness control) |
| `P1-missing-rev-class` | 1 | `no atoms of class(es) ['rev']` | clause 2, five-class coverage |
| `P5-four-exemptions` | 1 | `exempted 4 > 3`, keys `['8','8','9','9']` | clause 4 cap |
| `P6-battery-two-noop-forgeries` | 1 | `battery forgeries_green 2 != 0` (real `run_battery`) | clause 6, real forgeries |
| `P6c-battery-dial-synthetic` | 1 | `battery correction_forgeries 2 != 3` | clause 6, **SYNTHETIC** input (F4) |
| `P7-ghost-atom-existing-rev` | 1 | `corrections that do not re-derive: 1` | clause 3 existence check, isolated |
| `P8-single-round-section` | 2 | `fewer than two ## Round N sections` | clause 5 |
| `P9-false-axes-correction` | **0** | `corrections 2`, `failing []` | **HOLE** — see F2 |
| `P9b-true-axes-correction` | 0 | `corrections 2` | the axes line is invisible either way |
| `P10-false-correction-exempts` | 1 | `corrections that do not re-derive: 1`, `exempted ['9']` | see F6 |
| `P11-vacuous-corrections` | **0** | `corrections 2`, `exempted []`, `mismatches []` | see F7 |
| `P12-false-axes-atom-corrected` | 1 | `mismatches 1 != 0`, `coverage` unexempted | **HOLE** — see F2 |

## Findings

**F1 (MEDIUM, test coverage). Five of eight clause guards are invisible to `--selftest`.**
`M1`, `M5`, `M6*`, `M7`, `M8` all leave the selftest green. Cause: every selftest case asserts only the
*exit code* of `_card(...)`, and `_card` always carries all five atom classes, at most one exemption, exactly
two sections, and `battery=None`. So removing one guard is masked whenever another guard keeps the same case
red. Evidence: `M2` (mismatches) is killed by exactly one case (`red-non-empty-window`) because every other
red case is also red for a second reason; `M6*` cannot be seen at all because
`run()`'s `with_battery` parameter (line 559) is **dead** — it ignores its argument and always passes
`battery=None`, so `evaluate_text`'s battery loop is never entered from the selftest.
Action for L1: none required for the landing. If the round wants the detector to match the predicate, the
cheapest repair is one case per guard (cards are cheap: each probe above is ~6 lines).

**F2 (HIGH, unguarded clause). The `axes` correction arm of clause 3 is not implemented.**
`CORR` (line 50) parses only `seats|window|path|rev`, so `- corrects axes …` lines are never read:
`corrects()`'s axes branch (280–289) is dead code, and the duplicate at 292–299 is unreachable *and* broken
(it dereferences `atom["axis"]`, undefined in `corrects`, so it would raise if reached).
Consequences, measured:

- `P9-false-axes-correction`: a card carrying `- corrects axes coverage: 99/99` (derived `1/1`) exits **0**,
  `failing []`, `corrections 2` — a false correction is certified green. This is the exact clause-3 sentence
  "an `axes` correction must state `<resolved>/<total>`", unenforced.
- `P12-false-axes-atom-corrected`: a card whose `## Owned axes` row claims `0/1` (derived `1/1`) **cannot be
  repaired by an axes correction**: exit 1, `coverage` sits in `mismatches`, never in `exempted`.
- Under `M9` (adding `axes` to `CORR`, nothing else) `P12` becomes exit 0 with `exempted ['coverage']`,
  `corrections 3`, and `P9` becomes exit 1, `P9b` stays 0 — i.e. the one-token change realises the frozen
  sentence exactly.

**This is live at the landing, not hypothetical.** `SCORECARD.md` at `31b092d` carries two such lines (3663
section `## Record corrections — round 47`):

```
- corrects axes coverage: 138/138 — …
- corrects axes depth: 24/24 — …
```

The counter parses `[('seats','45'), ('window','46')]` only (`corrections 2`). Both axes statements happen to
be **true** at `31b092d` (measured `axis_pairs {'coverage': (138, 138), 'depth': (24, 24)}`, and both `Owned
axes` rows already state the same), so the landing is green — but the counter would be equally green if those
two numbers were wrong, and they are the two numbers R47-C2 exists to check. Do not "fix" the frozen counter;
report the divergence with clause 3 (the claims file says the arm exists; the code says it does not), and
note that these two correction lines currently contribute neither an exemption nor a check.

**F3 (MEDIUM, predicate/implementation). One correction can exempt several atoms; `EXEMPT_MAX` counts atoms.**
`exempt()` is `any(...)` per atom, so a single re-deriving `seats` correction for a round exempts both the
`Waves:` sum atom and the `Wave 1: …` pair atom of that round (`P5` shows `exempted ['8','8','9','9']` from
two correction lines). That matches the claims' wording ("may not exempt more atoms"), so it is not a
violation — recorded so the L1 does not read `exempted 4` as four corrections.

**F4 (LOW, structural). `battery.correction_forgeries == 3` is unfalsifiable from the CLI.**
`run_battery` calls `forged(...)` exactly three times unconditionally (`grep -c '^    forged(' → 3`), so the
dial can never be anything but 3; the `M6c` mutant is therefore only observable through a synthetic battery
dict (`P6c`, labelled SYNTHETIC). The other half, `forgeries_green == 0`, **is** reachable and real:
`P6` uses the tool's own `run_battery` on a card whose corrections contain no `N seats total` and no
`empty in A..B`, so two of three forgeries are no-ops → `forgeries_green 2`, exit 1 on pristine, exit 0 with
`M6`/`M6b`. (A2 fixed one no-op forgery by choosing a non-empty window; the no-op *detection* path is what
`P6` exercises.)

**F5 (MEDIUM, test design). The `red-ghost-exemption` case does not isolate the clause it is named for.**
Its forged line is `- corrects path does/not/exist.md: never`, which also fails `corrects()`'s own
path-existence re-derivation, so `M4`'s guard catches the case and deleting the existence check (`M7`) is
invisible. `P7` isolates it with `- corrects rev <base>` — a revision that resolves, an atom the card does not
contain: pristine 1 (`corrections that do not re-derive: 1`), `M7` 0. A one-line change to the selftest case
(`rev` instead of `path`) would make it discriminating.

**F6 (LOW, receipt-level divergence from the claims text). "An exemption whose correction is false keeps the
atom red" is not what the code does.** In `P10` the false `seats` atom is removed from `mismatches` and lands
in `exempted ['9']`; only `corrections_bad` (a different list) keeps the exit at 1. Exit semantics are right;
the receipt says "exempted", not "red". Consequence is not cosmetic: with `M4` deleted the same card is green
(`P10` → 0). If the L1 quotes that sentence in the landing evidence, quote it as exit-equivalent, not as
atom-level.

**F7 (MEDIUM, vacuity — contract question for L1, not a clause violation). Two corrections need not correct
anything.** `P11` is a card with **zero** mismatches and two `path` corrections naming atoms that were already
green: exit 0, `corrections 2`, `exempted []`. `CORR_MIN` counts correction *lines*, not repaired defects, so
a record with no defects satisfies "at least two re-derived corrections" with two no-ops. On the current
landing this is moot (the `seats`/`window` corrections do exempt real atoms: base had `mismatches 4`), but the
predicate text and the round's stated purpose ("every mismatch is corrected") are not the same test. Decide at
landing whether clause 3 needs "each corrected atom is otherwise red"; the code cannot express it today.

**F8 (LOW, CLI). `--selftest` still requires `--root` and `--rev`.** `python3 -I -B record.py --selftest`
exits 2 with an argparse usage error before the selftest runs; the working invocation is
`--root <any> --rev HEAD --selftest`. Anyone copying the selftest command from the docstring will read a 2
as a could-not-evaluate.

**F9 (LOW, dead code).** `exempt_keys` (line 326) is computed and never used; `run()`'s `with_battery`
parameter (559) is dead; `corrects()`'s second `axes` branch (292–299) is unreachable and would raise
`NameError` on `atom`. None changes an exit code.

## Unguarded / unreachable clauses, named

1. **Clause 3, `axes` arm — no guard at all** (`CORR` at line 50 cannot match `axes`; branch at 280–289
   unreachable). A false `- corrects axes …` statement is accepted silently (`P9`, exit 0), and a true one is
   ignored; an `axes` mismatch cannot be exempted (`P12`).
2. **Clause 2 (five-class coverage) — guard exists, detector absent** (`M1` survives the selftest; `P1`).
3. **Clause 4 (`exempted <= 3`) — guard exists, detector absent** (`M5`; `P5`).
4. **Clause 6 (`battery.forgeries_green == 0`) — guard exists, detector absent** (`M6`, `M6b`; `P6`).
   **Clause 6 (`correction_forgeries == 3`) — guard exists and cannot fire** from `run_battery` (`M6c`,
   synthetic `P6c`).
5. **Clause 3 existence check ("a correction that exempts an atom the card does not contain") — guard exists,
   detector absent** (`M7`; `P7`).
6. **Clause 5 (`sections` exactly the last two) — guard exists** (returns 2, not 1) **and no case exercises
   it** (`M8`; `P8`).

## Restoration and cleanup evidence

- Originals never written: `tools/round-47/record.py` sha256 `abf352573…` at the first command, at
  `a0753786…`, and after the last command; `git status --porcelain -- tools/ plans/` printed nothing; the only
  mutations were in `$S/mutants/<name>/` copies, regenerated from pristine bytes per mutant with the anchor
  asserted unique.
- Pristine scratch copy sha256 unchanged after the full 12-mutant matrix
  (`"pristine_sha_after" == "pristine.record_sha256"`, `pristine sha unchanged: True` in `harness.py` stdout).
- Fixture repos: `git init -q` under `$S/fixture-*` only, identity set with `git -C "$D" config` (never a
  global throwaway identity); each fixture's `rev-parse --show-toplevel` asserted equal to its directory
  before the first commit.
- No git mutation in the lane: only `rev-parse`, `show`, `cat-file`, `status --porcelain`, `log`, `diff`.
- `$S` removed after `receipts/` was copied into this seat's directory (see `receipts/ledger.json` for
  per-file sha256 and the command that produced each).

## Tooling

No installs. `python3 3.14`, `git` on PATH were sufficient. No pacman, no `uv tool`, no network.

## Receipts in this directory

`receipts/harness.py`, `receipts/probe.py` (re-runnable), `receipts/baseline.json`,
`receipts/mutations.json` (per-mutant record sha256, selftest exit, stdout sha256, failed cases),
`receipts/probe-pristine.json`, `receipts/probe-M*.json`, `receipts/probe-matrix.json`,
`receipts/harness-run.txt`, `receipts/ledger.json`.
(`probe-matrix.json` was collapsed before `P12` was added, so it covers `P0`–`P11`; the `P12` numbers in this
report come from `probe-pristine.json` and `probe-M9-axes-correction-parse.json`.)
