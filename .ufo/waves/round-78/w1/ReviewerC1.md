# ReviewerC1 — independent re-derivation of R78-C1 at the freeze

Seat: `ReviewerC1` · lane `kaidoku-shokunin` · measured rev `ffcb47d13f0340f88397af6c8d2707a9554abab3` (the freeze)
Verdict: **R78-C1's measured counters re-derive independently. No fixture is refused by a rule other than its declared one. No over-tightening found.** One low-severity observation (near-miss stem list) and one semantics note (exit 1 at the freeze is the declared pre-landing state) below.

Evidence dir: `.ufo/waves/round-78/w1/ReviewerC1/` (receipt.json is the machine-readable summary of this report).

## 1. The counting command, run by this seat

```
python3 -I -B tools/round-78/attack-gate.py --root . --rev ffcb47d13f0340f88397af6c8d2707a9554abab3 \
  --work /fast/scratch/hyaku/kaidoku-r78/ReviewerC1 --battery --json-out battery-receipt.json
```

Pasted from the receipt (`battery-receipt.json`):

| field | value |
|---|---|
| `fixtures_total` | 10 |
| `base_accepted` | 10 |
| `refused` | 10 |
| `validate` | `{"defects": [], "fixtures": 10}` |
| `genuine.mismatch_count` | 0 |
| `genuine.defects` | 4 items, all "no filing receipt" / "no gate receipt in the round dir" for `clean_run`, `filing_rev`, `gate_receipt_schema`, `gate_receipt_rev` |
| `exit` / `ok` | 1 / false |
| `instrument.sha256` | `780089e3…d173` — equal to the pin in `.ufo/waves/round-78/claims.json` |

Semantics note (not a defect): `exit 1` at the freeze is the declared pre-landing state. The four `genuine.defects` name the wave's own `.ufo/waves/round-78/l1/scores/` receipts that do not exist until the wave lands; the frozen predicate's `after` clause is the landing state (`exit 0`, `genuine.defects []`). At the freeze the committed SCORECARD carries no round ≥ 78 capabilities rows (`genuine.record.in_scope_cells 0`), so the record arm has nothing else to judge. Every measured counter matches the frozen predicate's measured values (`base_accepted 10 of 10`, `refused 10`, `genuine.mismatch_count 0`, defect-free `validate`).

Cross-check: this seat's per-fixture results (id, fixture dir, declared rule, `base.accepted`, `base.observed`, `refused`, full `reasons`) are **byte-equal** to the committed `.ufo/waves/round-78/pre/c1-at-base.json` at the freeze (10 of 10 compared, 0 diffs), and the stdout summary is identical to the committed `pre/c1-battery-run.json` wrapper. The do-nothing control was also re-run by this seat: `--control base-only` reports `refused 0` of 10 (`ctl-base-only.json`), as the predicate requires.

## 2. Per-fixture refusal, re-derived from the fixture bytes

Each fixture was refused by exactly its declared rule. Triggers verified by `grep -n` on the committed fixture bytes (worktree copies are unmodified):

| id | fixture | declared rule | trigger (file:line — substring) |
|---|---|---|---|
| receipt-unauth | a1-forged-receipt | receipt_auth | `green-forged.json:1-9` — the receipt has only `atoms` (line 2) and `mismatch_count` (line 8); no `rev`, no `instrument` → "no 40-hex rev" |
| qualified-atom | a2-repunctuated | qualified_atom | `PROVINCE.md:5` — `(D24: true, mismatch 0, D24 true)`; clause `D24: true` is an atom id with a qualifier |
| near-miss-field | a3-near-miss | near_miss_field | `PROVINCE.md:5` — `(mismatch 0, D24 true)`; `mismatch 0` is stem-first, and the receipt `green-authed.json:12` has only `mismatch_count`, never `mismatch` |
| negated-verdict | a4-negated | negated_verdict | `PROVINCE.md:5` — `(the receipt does not record D24 false, D24 true)`; `NEGATION_RE` matches "not" |
| nested-hidden-mismatch | a5-nested-field | value_mismatch | `PROVINCE.md:5` claims `(forged_detected true, D24 true)`; `nested.json:7` has `"forged_detected": false` at `/arms[0]/observed/verdict/forged_detected` |
| dropped-defect | a6-dropped-defect | unbound_verdict | `PROVINCE.md:5` claims `(D24 true, mismatch_count 0)`; `dropped.json:1-9` has `instrument`/`mismatch_count`/`rev`/`schema` only — no `atoms` array, so the `D24` atom clause cannot bind ("no_atoms") |
| unclean-clone-run | b1-fail-run | clean_run | `.ufo/waves/round-78/l1/scores/prefile-at-filing.json:13,15` — `"exit": 1`, `"passed": false`, verdict line `prefile: FAIL` |
| stale-filing-rev | b2-stale-filing | filing_rev | `.ufo/waves/round-78/l1/scores/prefile-at-filing.json:17` — `"rev": "0000…0000"`, 40-hex but not an ancestor of the fixture's measured rev |
| gate-receipt-schema | b3-one-key-gate | gate_receipt_schema | `.ufo/waves/round-78/l1/scores/gate-at-tip.json:1-3` — the whole receipt is `{"exit": 0}`; missing `rev`, `argv`, `passed`, `prefile_line`, `stdout`, `stdout_sha256`, `env_keys` |
| gate-receipt-stale-rev | b4-stale-gate-rev | gate_receipt_rev | `.ufo/waves/round-78/l1/scores/gate-at-tip.json:17` — `"rev": "0000…0000"`, not an ancestor of the measured rev |

No fixture was refused by a rule other than its declared one (the gate applies exactly one rule per fixture, and `validate` checks `reason.rule == fixture.rule` for every reason — `validate.defects` is empty).

## 3. Base arm, checked by this seat (5 fixtures, both instruments)

The frozen round-77 instruments were re-run by this seat on the battery-materialised fixture repos (scratch), not just read from the battery receipt:

| fixture | instrument | accepted field | observed |
|---|---|---|---|
| a1-forged-receipt | `tools/round-77/verdict-bind.py` | `record_clean` = exit 0 and `receipt.mismatch_count == 0` | exit 0, `mismatch_count 0` (`basecheck-a1-forged-receipt.json`) |
| a2-repunctuated | `tools/round-77/verdict-bind.py` | `record_clean` as above | exit 0, `mismatch_count 0` (`basecheck-a2-repunctuated.json`) |
| b1-fail-run | `tools/round-77/prefile-receipt.py --battery` | `arms[clone-run].met` | met True — "rc 1, prefile: FAIL, receipt_defects []" (`basecheck-b1-fail-run.json`) |
| b2-stale-filing | `tools/round-77/prefile-receipt.py --battery` | `arms[record-receipt].met` | met True — "exit 0, defects []" (arms_ok 5 of 6; the false `gate-exits` arm is this fixture's planted defect and is not the accepted field) (`basecheck-b2-stale-filing.json`) |
| b3-one-key-gate | `tools/round-77/prefile-receipt.py --battery` | `arms[gate-exits].met` | met True — "round-78: 1 gate receipts, missing []" (arms_ok 6 of 6) (`basecheck-b3-one-key-gate.json`) |

All five accepted fields read true — the frozen round-77 instruments do accept each fixture tree, which is precisely the over-set premise R78-C1 calibrates.

## 4. Over-tightening probe (`scan_record`)

Arms run by this seat in a scratch git record against the gate's own `scan_record` (`probe.py`, `probe-output.txt`):

- **P — minimal correct cell, authenticated receipt → `findings []`, 2 bound clauses, 0 mismatches.** What had to be included: a `## Capabilities` row with round ≥ 78 in the 4th cell; a parenthesised group whose clauses are in the gate's grammar with its word order (`0 mismatches`, `D24 true`); a `.json` receipt path earlier in the same cell; receipt JSON whose 40-hex `rev` names a commit carrying the pinned instrument blob, with `instrument.path` + `instrument.sha256` re-deriving against that blob (`receipt_auth`); and receipt fields the clauses bind to with typed-equal values.
- **S1 — grammar-legal `pristine 0, validate defect-free` under the genuine rule set → `findings []`.** `judge_group` parses a clause before applying `NEAR_MISS_RE`, so the two stem-first grammar clauses are not shadowed by the near-miss rule. (An alarm this seat raised mid-probe on reading the rule order was disproven behaviorally; recorded so no sibling re-chases it.)
- **S2 — the drafted round-78 capabilities row cell (worktree `SCORECARD.md` row 660) verbatim, with the committed `c1-at-base.json` receipt bytes and the pinned lane rev fetched into the probe repo → `findings []`, 4 bound clauses, 0 mismatches.** The real record cell as drafted stays clean under every genuine rule.
- **N1 — same record minus the instrument pin → `receipt_auth`: "no instrument path+sha256".**
- **N2 — same record, wrong claimed value (`1 mismatches`) → `value_mismatch`, mismatch_count 1.**

Conclusion: `scan_record` is not over-tightened — a correct, authenticated minimal record passes clean, and each refusal rule still fires when its guard is violated.

## Findings

- **None blocking.** Every R78-C1 measured counter re-derives, every refusal fires on the declared rule from the fixture's own bytes, the base arms accept, and the genuine-record probe passes.
- **Low / latent — near-miss stem list omits the plural "atoms".** `NEAR_MISS_RE` (attack-gate.py:75) stems are `mismatch|survivor|atom|pristine|validate|match|matches`; a stem-first typo like `atoms 3` in a verdict cell parses as nothing and is silently skipped (neither refused as a near miss nor bound), while `atom 3` is refused. Compared with `mismatch 0` (refused) this is a small hole in the near-miss net — a fail-silent skip, not a false refusal. Not exercisable at the freeze (`in_scope_cells 0`); routed as a record-prose hygiene note, not a claim defect.
- **Semantics note (informational).** `exit 1` + the four `genuine.defects` at the freeze are the frozen `before` state's signature (the l1 receipts land with the wave); they are not a counter divergence. This seat's receipt is byte-equal to the committed freeze receipt on every compared field.

## Verification gaps / residual risk

- The `all-refuse` and `no-fixtures` controls were compared against the committed freeze receipts, not re-run by this seat (the do-nothing `base-only` control was re-run and refuses 0 of 10).
- `run_base` materialisation copies fixture trees from the worktree; those trees are unmodified at the freeze (verified via `git status` — no entry under `.ufo/waves/round-78/attacks/`), so worktree bytes equal committed bytes. `scan_record` and `judge_receipt_fixture` read only git objects at the measured rev.
- No tools were installed or upgraded (stdlib only); nothing written outside the seat evidence dir and the scratch dir (deleted after the receipts were copied).

Report: `.ufo/waves/round-78/w1/ReviewerC1.md`
