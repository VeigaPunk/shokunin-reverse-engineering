# Round 69 w1 — counter mutation table (seat MutSelftest)

Frozen counters attacked (copies only; originals verified unchanged after every run):

| counter | sha256 (frozen) |
|---|---|
| `tools/round-69/mutation-check.py` | `51b64c56c48899d5d2d707298431861f8465e5422e53ee7dceb903d1b56d33c2` |
| `tools/round-69/contract-probe.py` | `e609d85d0fc4604ef582ae886da38b4d335c558a1954c12344df0e468669061d` |
| `tools/round-69/controls.py` | `1f8f78c177b33196cb2a4cb6c9c4c999e70d07c4c158ddac250dae2a0196b918` |
| `tools/round-69/packed-elf.py` (C3 counter `--check-receipt`) | `4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc` |

Every mutant is a single-site replacement (the builder asserts exactly one match) of the frozen
bytes; each mutant's sha256 is in `evidence/results.json` and its source in `evidence/mutants/`.
Every row below ran the **frozen** counter and the **mutated** counter on the **same fixture**;
fixtures live in scratch git repos under `/fast/scratch/hyaku/kaidoku-r69/MutSelftest/fixtures/`
(deleted at yield; receipts copied to `evidence/`).

Legend — **FG** = mutated counter returns a green/met/ok verdict on a fixture the frozen counter
rejects (a counter-level false green); **FA** = mutated `--validate` accepts a receipt the frozen
`--validate` rejects; **flip** = a control arm's verdict flips from red to green. "Guard" names the
claim artifact that still catches the defect when the receipt is read against the frozen predicate /
kill rule / declared control (— = none, the mutant survives every frozen artifact).

## mutation-check.py (R69-C1 counter)

| # | line | mutation | fixture | frozen | mutated | outcome | guard |
|---|---|---|---|---|---|---|---|
| A1 | 69 | delete the whole `M5_control` r69 row from `PATCH_SETS` | round-69 instrument with the `arm-pack-control-false` selftest case removed (M5 would survive) | rc 1, `survivors ["M5_control"]`, `killed 4`, `ok false`, `pristine.cases 19` | rc 0, `survivors []`, `killed 4`, 4 mutant rows, `ok true` | **FG** | C1 predicate "all five mutants killed" + atom A2's five names (by name only; the counter's `ok` and `--validate` accept the 4-row receipt, rc 0) |
| A2 | 145 | kill = any non-zero rc when a case is declared (`failed` no longer required) | fixture instrument: pristine selftest green at 20 cases, every patched arm raises before printing JSON | rc 1, `killed_wrong_case` all five, `ok false` | rc 0, `killed` all five, every `failed: null`, `ok true` | **FG** | C1 predicate "each kill's `failed` list naming its declared arm-false case" and the kill rule "a syntax error is not a gate"; `--validate` accepts the receipt (rc 0) |
| A3 | 158 | `ok` ignores the `killed_wrong_case`/`unevaluable` list | same crash fixture | rc 1, `ok false` | rc 0 with `killed_wrong_case` still listing all five and `killed []`, `ok true` | **FG** | C1 predicate "all five mutants killed" (the receipt itself still shows the wrong-case rows) |
| A4 | 184 | `--validate` accepts an empty mutant list | fabricated battery receipt (no rows, `survivors []`, `pristine_ok true`) | validate rc 1, defect `"mutants absent or empty"` | validate rc 0, no defects | **FA** | declared do-nothing control `c1-constant-battery` (expects validate rc 1) and the C1 predicate (all five kills, `pristine.cases 20`) |
| A5 | — | no pristine case-count pin (not a mutant; observed coverage gap) | same 19-case instrument as A1 | `pristine_ok true` with `pristine.cases 19` | — | **gap** | C1 predicate "`pristine.cases 20`" (the battery only checks `rc == 0` and `ok is true`) |

Additional observation: the frozen `--validate` accepts receipts with `ok:false`, `rev:"deadbeef"`,
`patch_set:"r68"`, `instrument:"nope.py"`, `target_sha256:"00…"`, `expected_survivors:99`,
`survivor_count:99` (rc 0). It validates row structure plus `survivors` agreement only.

## contract-probe.py (R69-C2 counter)

| # | line | mutation | fixture | frozen | mutated | outcome | guard |
|---|---|---|---|---|---|---|---|
| B1 | 204 | A3 passes on any exit 2 (drop the `packer` / `version` substring check) | compliant-except-A3 route (refuses both bad packers, but reports the fake upx as a work problem) + a fully formed receipt | 5/6, `failed ["A3_packer_version"]`, rc 1 | 6/6, `failed []`, rc 0 | **FG** | C2 before-arm clause: the mutant scores the round-68 base instrument 1 of 6 (A3 true), so the required "0 of 6" fails |
| B2 | 114 | A5 tolerates a carrier with no `format` | compliant route + receipt whose `libz` carrier has no `format` | 5/6, `failed ["A5_carrier_record"]`, rc 1 | 6/6, `failed []`, rc 0 | **FG** | C2 kill rule "a receipt whose carrier pins/formats/modes do not equal the probe's own derivation" (textual, read from the receipt); the before-arm stays 0 of 6, so it does **not** catch this |
| B3 | 129 | A5 no longer requires carrier `ok` / arm truth | compliant route + receipt with `xxd` `ok:false` | 5/6, `failed ["A5_carrier_record"]`, rc 1 | 6/6, `failed []`, rc 0 | **FG** | C2 kill rule "a carrier arm false" (read from the receipt); before-arm 0 of 6, no catch |
| B4 | 236 | `--validate` accepts an arm with an empty `observed` dict | receipt with six arm rows, `observed {}` on each | validate rc 1, six `no observation` defects | validate rc 0, no defects | **FA** | declared do-nothing control `c2-constant-probe` (expects validate rc 1) |

Positive control (`B0`): the compliant route + fully formed receipt scores 6/6 under the frozen probe
and under both A5 mutants, so each A5 mutant's false green is caused by the injected receipt defect,
not by the fixture.

Additional observation: the frozen `--validate` accepts a six-arm receipt with `ok:false`,
`rev:"deadbeef"`, `instrument:"nope.py"`, `instrument_sha256:"00…"`, `target:99`,
`receipt:"nope"` (rc 0). It checks arm ids/booleans/observations and `arms_passed`/`failed`
agreement only.

## controls.py (the three claims' do-nothing driver)

| # | line | mutation | fixture | frozen | mutated | outcome | guard |
|---|---|---|---|---|---|---|---|
| C1 | 146 | `c3-do-nothing` is ok when `--check-receipt` returns 0 (i.e. when the do-nothing receipt is *met*) | stub root whose `packed-elf` accepts the round-68 receipt (met true, rc 0) | suite rc 1, `c3-do-nothing: false` | suite rc 0, all seven controls `true` | **flip** | C3 predicate's base clause ("the same checker over the round-68 receipt reports target 2 and no shared-object carrier") only if the claim is scored directly, not through controls |
| C2 | 150 | `c3-loose-ceiling` expects 0 (the 0.9 receipt must be met) | stub root whose `packed-elf` accepts a 0.9 ceiling | suite rc 1, `c3-loose-ceiling: false` | suite rc 0, all seven `true` | **flip** | C3 kill rule "a ceiling ratio above 0.75" / predicate (read from the receipt) |
| C3 | 103 | `c1-do-nothing` is ok when the battery reports 0 survivors | stub root whose `mutation-check` reports `survivor_count 0`, `survivors []` | suite rc 1, `c1-do-nothing: false` | suite rc 0, all seven `true` | **flip** | C1 predicate's base clause ("the same battery against round-68 … reports exactly the five survivors") only if scored directly |

The stub roots exist to isolate the controls' decision logic: each stub reports the target outcome
while doing none of the work, which is exactly what the control must reject.

## packed-elf.py `--check-receipt` (R69-C3 counter)

| # | line | mutation | fixture | frozen | mutated | outcome | guard |
|---|---|---|---|---|---|---|---|
| D1 | 285 | drop the `control_ok is True` requirement | three-carrier synthetic receipt in bounds, `control_ok:false` | `met false`, rc 1 | `met true`, rc 0 | **FG** | C3 predicate "`control_ok true`" (the checker's output does not echo `control_ok`; the receipt must be read) |
| D2 | 303 | drop the `ratio > 0.75` comparison | three-carrier synthetic receipt with `libz before_ceiling_ratio 0.9` | `met false`, rc 1 | `met true`, rc 0 | **FG** | C3 predicate "every carrier's `before_ceiling_ratio` at or below 0.75" and the kill rule "a ceiling ratio above 0.75" |

Positive control (`D0`): the in-bounds synthetic receipt is `met true` under the frozen checker and
under both mutants.

## Survivors named for the next freeze

These are counter-level defects that no frozen counter artifact detects by itself (each needs the
predicate / kill rule / a separately executed control). Any future round that changes these lines
must re-run this matrix:

1. `mutation-check.py`: no declared mutant-row inventory (a dropped row is invisible to `ok` and
   `--validate`).
2. `mutation-check.py`: a kill label is accepted on rc alone; `failed` is not compared to
   `expect_case` in either the verdict logic or `--validate`.
3. `mutation-check.py`: `ok` does not include the wrong-case/unevaluable list.
4. `mutation-check.py`: `--validate` accepts an empty mutant list and does not bind `pristine.cases`,
   `ok`, `rev`, `patch_set`, `instrument`, `target_sha256`, `expected_survivors` or `survivor_count`.
5. `contract-probe.py`: A3 accepts any exit 2.
6. `contract-probe.py`: A5 tolerates a missing `format` and a carrier that is not ok.
7. `contract-probe.py`: `--validate` accepts empty observations and binds no instrument/rev/target.
8. `packed-elf.py --check-receipt`: `control_ok` and the 0.75 ceiling relation are each one deleted
   line away from a false `met true`.
9. `controls.py`: each control's expectation is a hand-written comparison; flipping one makes the
   suite certify a do-nothing counter with all seven arms green.

## Fixture coverage notes

- The four instrument fixtures (`m5`, `crash`, `route-a3`, `route-ok`) and the three stub roots
  (`root-C1..C3`) are scratch git repos; every fixture commit was made after
  `git rev-parse --show-toplevel` printed the fixture directory.
- The round-69 instrument fixture (A1) is the committed round-69 route with only the
  `arm-pack-control-false` selftest case and its `REGISTERED_CASES` entry removed, so its pristine
  selftest is internally consistent at 19 cases (that is the point: the battery does not pin 20).
- The crash fixture (A2/A3) keeps the five r69 patch sites once each and a pristine selftest that
  prints `cases 20`, `ok true`; each patched arm raises before printing.
