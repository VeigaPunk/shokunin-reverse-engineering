# MutGate — mutation score of `tools/round-78/attack-gate.py` (round 78, w1)

Seat: MutGate (mutation tester, w1 leaf — no subagent dispatch).
Scope: score the attack gate's own detectors by mutating a scratch copy, one
single-point defect per run, and measuring which named case or fixture kills it.

## Target and snapshot provenance

- Scored file: `tools/round-78/attack-gate.py`, sha256
  `961d5a23c1d38116f5b992434fa2295b5a90643b4a52233e205837ac73bf48c0`.
- Measured rev: `c9d986eb1531c43a5b95fd0bf327d048c201e6b5` (HEAD when the matrix ran;
  `debris`: the record's own battery at that rev reports the population floor met).
- **The target advanced mid-run.** The first pass (09:18) scored `a86f6d4d…`
  (the version left by `01768ac5`). While the matrix ran, the L1 landed `8991721a`
  (plural near-miss stems), `d2ab5f3e` (population-floor record), `c9d986eb`
  (selftest-26 row), producing `961d5a23…`. The first pass produced the same
  kill/survivor pattern; **every number below is re-taken against the final
  committed version** (`961d5a23`, rev `c9d986eb`).
- Pinned round-77 instruments (working-tree copies, `git status` clean):
  `verdict-bind` `45280392…`, `prefile-receipt` `174eedb5…`.
- Restoration: the lane file's sha256 at scoring start and finish are identical;
  mutants exist only under the scratch root, which is removed after the receipts
  are copied here.

## Method

Per mutant: one exact single-point replacement in a scratch copy (asserted to
occur exactly once), then `--selftest` and `--battery --root <lane> --rev
c9d986eb --work <scratch>/<mutant>`; battery receipts are kept in this dir.
Detectors compared against the pristine baseline:

- fixture refusals lost (a fixture no longer refused);
- fixture refusals fired by a rule other than the fixture's declared rule
  (the gate's own `validate` also flags this);
- genuine-scan defects / non-zero `mismatch_count`, population floor not met;
- `validate` defects;
- each failing selftest case (26 cases at this version).

`sole` = exactly the declared fixture detector failed. `sole_rule_family` = the
same, allowing the declared rule's own red selftest cases to co-fire (i.e. no
cross-rule or record-level collateral). A `collateral_fixture_changes` field in
the receipt re-checks every other fixture's `(refused, reason-rule set, reason
count)` — all empty: no mutant perturbed any fixture outside its declared one.

## Baseline arms (pristine, measured)

- selftest: exit 0, 26 cases, 0 failures.
- battery: exit 0 — `fixtures_total 10`, `base_accepted 10`, `refused 10`,
  `genuine.mismatch_count 0`, `genuine.defects []`,
  `genuine.population_floor {cells 4, clauses 8, met true}`,
  `validate {defects [], fixtures 10}`.
- All ten base arms accepted; no run in this matrix had a base-arm failure
  (nothing inconclusive).

## Mutation results

| id | edit | verdict | killed_by | sole | sole_rule_family | detectors |
|---|---|---|---|---|---|---|
| m01 | (a) `auth_findings` returns `[]` (early return before the body) | killed | `fixture:receipt-unauth` | false | true | fixture `receipt-unauth` lost + selftest `red-receipt-auth`, `red-auth-no-instrument` |
| m02 | (b) `QUALIFIED_ATOM_RE` matches nothing | killed | `fixture:qualified-atom` | false | true | fixture `qualified-atom` lost + selftest `red-qualified-atom` |
| m03 | (c) `NEAR_MISS_RE` matches nothing | **survivor** | — | false | false | none |
| m04 | (d) `NEGATION_RE` matches nothing | killed | `fixture:negated-verdict` | false | true | fixture `negated-verdict` lost + selftest `red-negated` |
| m05 | (e) `bind_clause` atom-branch defect (`no_atoms`) returned as `(True, "bound")` | killed | `fixture:dropped-defect` | **true** | true | fixture `dropped-defect` lost |
| m06 | (f) `clean_run` no longer rejects a failed retained run (`elif False:`) | killed | `fixture:unclean-clone-run` | **true** | true | fixture `unclean-clone-run` lost |
| m07 | (g) `filing_rev` drops the `is_ancestor` check (40-hex shape kept) | killed | `fixture:stale-filing-rev` | **true** | true | fixture `stale-filing-rev` lost |
| m08 | (h) `validate_receipt` skips the refused-without-reason guard | **survivor** | — | false | false | none |

Score on this version: **8 mutants, 6 killed, 2 survivors, 0 inconclusive.**

### Per-mutant notes

- **m01** — with `auth_findings` short-circuited, `a1-forged-receipt` (whose
  receipt carries neither a 40-hex `rev` nor an instrument pin) is no longer
  refused, and the two selftest auth cases go red. The new instrument-mode auth
  check sits inside the same function and is bypassed with it; its four
  `*-mode-*` cases still pass because they call `mode_ok` directly — the
  function-level mutation is caught by the two pre-existing auth cases and the
  fixture, not by the mode cases.
- **m02** — `a2-repunctuated`'s only finding (`D24: true`) disappears; the
  fixture is accepted, so the battery loses the refusal and the selftest red
  case fires. Note the other clause (`mismatch 0`) does **not** rescue it: the
  per-fixture rule set contains only `qualified_atom`.
- **m04** — `a4-negated`'s clause `the receipt does not record D24 false`
  stops parsing as a verdict at all once the negation scan is dead; the fixture
  is accepted, red case fires.
- **m05** — `a6-dropped-defect`'s `dropped.json` has no `atoms` array, so the
  clause `D24 true` was the single `unbound_verdict` defect (reason `no_atoms`);
  flipping that return to a bound pass silently accepts the dropped defect. This
  is the only detector for it: sole kill.
- **m06** — `b1-fail-run`'s retained filing receipt is internally consistent
  (exit 1, passed false), so `check_receipt_like` passes it; only `clean_run`'s
  own exit/passed gate refuses it. Sole kill.
- **m07** — `b2-stale-filing`'s filing rev is 40 zeros: `is_hex` passes and only
  `is_ancestor` refuses it. Sole kill.
- No mutant produced cross-rule or record-level collateral
  (`collateral_fixture_changes: []` for all six kills; genuine scan and
  `validate` stayed clean throughout).

## Survivors (coverage findings — not contract changes)

### m03 — `NEAR_MISS_RE` matches nothing (survivor)

The battery verdict is **byte-identical to the pristine baseline except the
instrument self-digest** (`probes.m03_identity`: differing top-level keys ==
`["instrument"]`); selftest is 26/26 green; no fixture changes state.

Why: `a3-near-miss`'s clause `mismatch 0` **parses** as a field
(`FIELD_RE`), and its detection rides the *parsed-stem* arm
(`near["f"] not in receipt and stem(near["f"]) in NEAR_MISS_STEMS`), not
`NEAR_MISS_RE`. Likewise the plural case added mid-run (`survivors 2`) parses
as a field and rides the stem arm. `NEAR_MISS_RE`'s only exclusive coverage is
the first arm — a near-miss **spelling that does not parse** (e.g. `validate
junk`, `pristine twenty`) — and no fixture or selftest case exercises that arm.
The mutant is therefore unreachable by every detector the gate ships.
Coverage gap, reported as-is; the contract is not changed from this seat.

### m08 — `validate_receipt` skips the refused-without-reason guard (survivor)

No selftest case calls `validate_receipt` (all 26 exercise `bind_clause`,
`judge_group`, `check_receipt_like`, `auth_findings`, `mode_ok`), and the
battery can never produce the guarded shape: `refused` is assigned
`bool(reasons)` in the normal arm, and the three controls either clear reasons
with `refused false` (`base-only`) or bypass the guard (`no-fixtures`). The
guard is only reachable via `--validate` on an externally crafted or stale
receipt.

Direct probe (`probes.m08_refused_without_reason`, receipts and outputs in this
dir): a battery-shaped receipt with one fixture set `refused: true,
reasons: []` and its own instrument digest —

- pristine: `--validate` exit **1**, defects
  `["receipt-unauth: refused without a reason"]`;
- m08: `--validate` exit **0**, defects `[]`.

So the mutation is real and observable, yet no in-repo detector kills it.

## Evidence inventory (this directory)

- `mutation-receipt.json` — full matrix: target sha, baseline arms, per-mutant
  edits/detectors/`sole`/`survivor`/`collateral_fixture_changes`, probes,
  provenance, restoration.
- `driver.py` — the exact driver used (v2 constants: target `961d5a23`,
  rev `c9d986eb`).
- `pristine-attack-gate.py` — the scored snapshot, byte-for-byte.
- `pristine-v2-battery.json` — baseline battery receipt (all ten fixtures,
  base arms, genuine scan, floor, validate).
- `m01…m08-battery.json` — each mutant's battery receipt.
- `probe-refused-no-reason-{pristine,m08}.json`, `probe-validate-*.txt` — the
  m08 crafted-receipt probe.
- m03 identity evidence is inside `mutation-receipt.json` (`probes.m03_identity`)
  and derivable from `pristine-v2-battery.json` vs
  `m03-near-miss-re-dead-battery.json`.

## Bounds, security, tooling

- Mutants exist only under `/fast/scratch/hyaku/kaidoku-r78/MutGate/`; the
  scratch root is deleted after the receipts are copied here. No git/jj writes,
  no commits, no lane edit — the lane file is byte-identical before/after
  (`restoration.identical: true`).
- No environment dumps or config secret values were written; fixtures are
  synthetic committed trees and receipts.
- Tooling: none installed or upgraded (`python3`, `git` sufficed; PACMAN paused
  — no transaction attempted).
