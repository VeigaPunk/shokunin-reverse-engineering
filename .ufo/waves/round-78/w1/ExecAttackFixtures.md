# ExecAttackFixtures — R78-C1 base-arm reproduction (round 78, w1)

Seat: ExecAttackFixtures · 2026-11-04 · target: independently reproduce the base arm of
R78-C1 — run the frozen round-77 instruments on all ten committed attack fixtures with my
own wrapper, no import of `tools/round-78/attack-gate.py`.

## Method

- Own materialiser (`/fast/scratch/hyaku/kaidoku-r78/ExecAttackFixtures/matrun.py`, scratch,
  deleted after the run): copies `.ufo/waves/round-78/attacks/<fixture>/` into scratch,
  copies `tools/round-29/prefile-check.sh` in, `git init`, commits the tree, rewrites
  `@HEAD@` in every `*.json` to the first commit's hash, commits again (fixed identity
  `fixture@localhost`, fixed dates `2026-11-04T00:00:00 -0300`), asserting
  `git rev-parse --show-toplevel` equals the fixture dir before each commit and at the end.
  `TMPDIR` pointed at the scratch `tmp/` throughout; nothing under `/tmp`, nothing outside
  the lane evidence dir plus scratch.
- Instruments run per the claim's command shape: `python3 -I -B tools/round-77/verdict-bind.py
  --root <fixture-repo> --rev HEAD --json-out <r>` for a1–a6; `python3 -I -B
  tools/round-77/prefile-receipt.py --root <fixture-repo> --rev HEAD --work <w> --battery
  --json-out <r>` for b1–b4.
- Frozen-instrument verification: working-tree bytes hash-match the `claims.json`
  `loaded_by_counter` pins — verdict-bind `45280392…`, prefile-receipt `174eedb5…`,
  prefile-check.sh `9a403dc1…`, gen-fixtures.py `6ef90aa4…`.
- The ATTACKS table (id/fixture/instrument/base arm) was derived by hand from the frozen
  receipt `pre/c1-at-base.json`, not imported from the gate.

## Result — 10 of 10 reproduce, zero disagreements

| fixture | instrument | exit | base observation | frozen base | reproduced |
|---|---|---|---|---|---|
| a1-forged-receipt | verdict-bind | 0 | mismatch_count 0 | exit 0, mismatch_count 0 | yes |
| a2-repunctuated | verdict-bind | 0 | mismatch_count 0 | exit 0, mismatch_count 0 | yes |
| a3-near-miss | verdict-bind | 0 | mismatch_count 0 | exit 0, mismatch_count 0 | yes |
| a4-negated | verdict-bind | 0 | mismatch_count 0 | exit 0, mismatch_count 0 | yes |
| a5-nested-field | verdict-bind | 0 | mismatch_count 0 | exit 0, mismatch_count 0 | yes |
| a6-dropped-defect | verdict-bind | 0 | mismatch_count 0 | exit 0, mismatch_count 0 | yes |
| b1-fail-run | prefile-receipt | 1 | arm clone-run met True: rc 1, prefile: FAIL, receipt_defects [] | same, exit 1 | yes |
| b2-stale-filing | prefile-receipt | 1 | arm record-receipt met True: exit 0, defects [] | same, exit 1 | yes |
| b3-one-key-gate | prefile-receipt | 0 | arm gate-exits met True: round-78: 1 gate receipts, missing [] | same, exit 0 | yes |
| b4-stale-gate-rev | prefile-receipt | 0 | arm gate-exits met True: round-78: 1 gate receipts, missing [] | same, exit 0 | yes |

All six record fixtures (a1–a6): the frozen verdict-bind ACCEPTS each (exit 0,
mismatch_count 0) — the claimed base arm. All four receipt fixtures: the declared arm of
prefile-receipt is `met: true` and the exit matches `base_receipt_exit` exactly (b1/b2 exit 1,
b3/b4 exit 0). Per-fixture `observed` strings are byte-equal to the frozen receipt's
`base.observed` fields; every per-fixture `accepted`, `observed` and `exit` check passed
(field_checks all true in the receipt JSON).

## Independent cross-check — bit-identical materialisation

- My b2 fixture repo HEAD is `a0b040c5c9b37594c51959a943d15c001b237c28`, exactly the
  "measured" rev quoted in the frozen receipt's `filing_rev` refusal reason.
- My b4 fixture repo HEAD is `4838efc49b7402d7da21c2cab605b51c8460442b`, exactly the
  "measured" rev quoted in the frozen `gate_receipt_rev` refusal reason.
- Commit hashes depend on tree bytes, identity, dates and messages; equality means my
  materialisation is bit-identical to the gate's at declaration — the ten base acceptances
  were measured on exactly the trees I measured.

## Evidence

- Receipt JSON: `.ufo/waves/round-78/w1/ExecAttackFixtures/base-arm-reproduction.json`
  (schema `kaidoku-r78-seat-base-arm-v1`; `fixtures` with id/instrument/exit/
  mismatch_count-or-arms/reproduced; `disagreements: []`; `reproduced_all: true`).
- Raw instrument receipts (as written by the frozen instruments): `.ufo/waves/round-78/
  w1/ExecAttackFixtures/raw/<fixture>.json` — ten files.
- Console log retained in scratch until deletion; quoted above.

## Findings

- The claim's base arm holds: the frozen round-77 instruments accept all ten attack
  fixtures (10/10 `base_accepted`), with per-fixture observations byte-equal to the frozen
  receipt. No fixture fails to reproduce; nothing falsifies R78-C1's base arm.
- Note (procedural, no defect): the assignment text says "the five record fixtures
  (a1–a6)"; the committed set has six record fixtures (a1–a6) plus four receipt fixtures
  (b1–b4) = 10, matching the claim's `fixtures_total 10`. All six were run.
- Note: the lane HEAD moved during the run (`218c5aa8…` at first probe, `f9069b9b…` at
  receipt write — sibling-seat commits landing). The measurement is unaffected: the
  instruments were hash-pinned before the run and the fixture trees are committed content
  reproduced by hash.

## Bounds

No lane file edited; writes confined to
`.ufo/waves/round-78/w1/ExecAttackFixtures/` (evidence) and
`/fast/scratch/hyaku/kaidoku-r78/ExecAttackFixtures/` (scratch, deleted). Read-only git
only outside the scratch fixture repos. No environment dumps or secret material written
(no env blocks touched). No new tools installed (stdlib-only Python; nothing to record).
