# RevengerInstruments — what the round-77 instruments do, and what the round-78 gate can see

Seat `RevengerInstruments`, round 78 wave 1. Read-only on the lane; every byte measured from a
named revision. Receipt: `acceptance.json` (same directory), per-class instrument output under
`receipts/`, drivers `probe.py` and `limits.py`.

Frozen state used: base `6205ec8c`, declaration `3e6b1efc` (the ten fixture trees), freeze
`ffcb47d1` (claims.json, gate pin `780089e3…`). Instrument blobs read at the freeze:
`verdict-bind.py` `45280392ff6c59e4c96041544720f055952a11a088769e24cb04207db932a9e7`,
`prefile-receipt.py` `174eedb56369414f5e4310afa9fe5ee6400e5145e4801452c9d21a7abac2d3fd` — both
equal to the worktree at the time of the run (`instruments_match_frozen: true`). The lane advanced
six times while the seat ran (`ffcb47d1 → 218c5aa8 → 59a92fbd → 3bb87162 → 713da191 → 9de14dd6`);
the record-level numbers below name `9de14dd6`, and the fixture table is revision-independent.

**Method.** An independent materialiser (`probe.py`, no code imported from the round-78 gate for
the measurement path) reads each fixture with `git show 3e6b1efc:<path>`, writes it into a private
two-commit repo under `--work`, substitutes `@HEAD@`, verifies `rev-parse --show-toplevel` is that
repo before every commit, and runs the pinned round-77 instrument with a four-key environment.
Acceptance is read from the instrument's own receipt, not from the gate: `record_clean` =
`exit 0` and `mismatch_count 0`; `arm:<name>` = that arm's `met`.

## 1. Acceptance table — ten of ten accepted

| # | class | instrument | base field | accepted | receipt field that proves it |
|---|---|---|---|---|---|
| 1 | `receipt-unauth` | verdict-bind | `record_clean` | yes | `exit 0`, `mismatch_count 0`; two bound rows: `D24 true` (claimed/actual true), `mismatch_count 0` (0/0), path `green-forged.json` |
| 2 | `qualified-atom` | verdict-bind | `record_clean` | yes | `exit 0`, `mismatch_count 0`, `bound_clauses 1`; only `D24 true` bound; `mismatch 0` recorded `unbound/unknown_field`; `D24: true` vanished (not even unbound) |
| 3 | `near-miss-field` | verdict-bind | `record_clean` | yes | `exit 0`, `mismatch_count 0`, `bound_clauses 1`; `mismatch 0` is `unbound/unknown_field` |
| 4 | `negated-verdict` | verdict-bind | `record_clean` | yes | `exit 0`, `mismatch_count 0`, `bound_clauses 1`; the English negation is not in the clause rows at all |
| 5 | `nested-hidden-mismatch` | verdict-bind | `record_clean` | yes | `exit 0`, `mismatch_count 0`; `forged_detected true` is `unbound/unknown_field`; nested `false` never read |
| 6 | `dropped-defect` | verdict-bind | `record_clean` | yes | `exit 0`, `mismatch_count 0`, `unbound_clauses 1`; the clause row itself carries `status: "defect"`, `reason: "no_atoms"`, yet `defects: []` |
| 7 | `unclean-clone-run` | prefile-receipt | `arm:clone-run` | yes | arm `clone-run` `met true`, `observed: "rc 1, prefile: FAIL, receipt_defects []"` (arms_ok 4/6) |
| 8 | `stale-filing-rev` | prefile-receipt | `arm:record-receipt` | yes | arm `record-receipt` `met true`, `observed: "exit 0, defects []"` with `rev 000…0` |
| 9 | `gate-receipt-schema` | prefile-receipt | `arm:gate-exits` | yes | arm `gate-exits` `met true`, `observed: "round-78: 1 gate receipts, missing []"` for `{"exit": 0}` |
| 10 | `gate-receipt-stale-rev` | prefile-receipt | `arm:gate-exits` | yes | same arm, `met true`; the receipt's `rev 000…0` is never read |

Cross-check: the gate's own `--battery` at `9de14dd6`/gate `a86f6d4d` reports
`fixtures_total 10, base_accepted 10, refused 10, ok true, exit 0`, `genuine.mismatch_count 0`,
`genuine.defects []`, `validate {defects [], fixtures 10}` — it agrees with this table.

## 2. The code path that lets each class through

Line numbers are the freeze blobs (`tools/round-77/*.py`).

**verdict-bind.py**

- class 1 `receipt-unauth` — `Resolver.receipt` (:118-136) does `git show rev:path` + `json.loads`
  and returns the dict; `bind` (:197-222) compares `atoms[id].ok` (:201-215) or `receipt[field]`
  (:216-222); `audit` sets `ok = not defects and bound > 0` (:447). Nothing reads `rev` or
  `instrument`, so a hand-authored receipt with the claimed values passes. *Refuses if* a claimed
  value differs, the file is absent at rev, or the binder required a 40-hex rev plus a pin that
  re-derives.
- class 2 `qualified-atom` — `QUALIFIER_RE` (:74) strips `D24:` and leaves `true`; `parse_clause`
  (:156-175) matches none of the seven regexes and returns `None`; :368 drops every `None`.
  `mismatch 0` also parses to `None` (`MISMATCH_RE` :81 wants `0 mismatches`). Only `D24 true`
  binds. *Refuses if* the surviving clause is false, or the qualifier stripping is removed.
- class 3 `near-miss-field` — same drop at :368; `FIELD_RE` (:77) needs `field value` with a bare
  field name, so `mismatch 0` is not a field clause. *Refuses if* the spelling is defined and the
  value differs, or an unparsable clause counted as a defect.
- class 4 `negated-verdict` — the English clause is `None` at :156-175 and dropped at :368; the
  binder has no negation rule. *Refuses if* a prose clause produced a defect.
- class 5 `nested-hidden-mismatch` — the field branch only looks at `receipt[field]` (:216-222);
  a nested key is `unbound/unknown_field` (:217), and `bind_cell` (:377, :402) counts unbound,
  never a defect. *Refuses if* nested keys were resolved and the nested `false` compared.
- class 6 `dropped-defect` — `atoms` absent returns `(False, "defect")` (:201-203), but `bind_cell`
  only routes `status == "bound"` into defects (:394-402); the defect status is counted as unbound
  and :447 sees `not defects`. *Refuses if* the `defect` status were routed into `defects`.

**prefile-receipt.py**

- class 7 `unclean-clone-run` — A1 (:214-223) `ok = exit in (0,1) and prefile_line is not None and
  not check_receipt(receipt)`; a `FAIL` run at rc 1 is a valid receipt. *Refuses if* `exit == 0`
  and `prefile: PASS` were required.
- class 8 `stale-filing-rev` — A2 (:226-239) calls `check_receipt(receipt)` without `expect_rev`;
  `rev` is compared only when `expect_rev` is given (:158-160). *Refuses if*
  `expect_rev=rev` were passed (the routed one-line fix).
- class 9 `gate-receipt-schema` — A3 (:241-276) accepts any `gate-*.json` dict with an integer
  `exit` (:265-266), else an `^exit=(-?\d+)$` text grep (:268). A one-key `{"exit": 0}` is met.
  *Refuses if* A3 applied the full receipt contract.
- class 10 `gate-receipt-stale-rev` — A3 never reads `rev`. *Refuses if* a 40-hex rev that is an
  ancestor of the measured rev were required.

## 3. The two mutation survivors

Both were reconstructed by patching the freeze blob and running the frozen selftest on the mutant.

### 3.1 `c1-rev-show-to-worktree` — **not closed by the round-78 gate**

Mutation: `show()` reads `Path(root, path).read_text()` instead of `git show rev:path`.

Reproduced: the mutated file passes the 15-case selftest (`exit 0`, `failures []`) — the selftest
never calls `show()`; every case injects a fake resolver.

Consequence, measured in a private repo:

| step | run | exit | `mismatch_count` |
|---|---|---|---|
| rev A, worktree clean | original | 1 | 1 |
| rev A, worktree clean | mutant | 1 | 1 |
| rev A, worktree dirty (`M PROVINCE.md`) | mutant | **0** | **0** |
| rev B, worktree clean | original | 0 | 0 |

The mutant emits a receipt naming **rev A** with `mismatch_count 0`; its `instrument.sha256` is
the blob at A (pin matches). Filed at rev B and cited from `PROVINCE.md`, the round-78 gate at
`a86f6d4d` returns `auth_findings []` and `scan_record {bound 1, mismatch 0, findings []}`, i.e.
**`sees_the_mutation: false`**; the frozen gate (`780089e3`) agrees. Re-running the *original*
instrument at the receipt's own rev A exits 1 with `mismatch_count 1`, so the provenance claim is
false and no rule checks it — `receipt_auth` hashes the instrument blob at that rev, and
`scan_record` reads the receipt at the *measured* rev.

### 3.2 `c2-nonint-exit-accepted` — **closed as a shape at the record, not as a mutation**

Mutation: the `isinstance(exit, int) and not bool` guard is deleted. The mutant passes the frozen
13-case selftest (`exit 0`, `failures []`) — there is no case for a non-int exit.

| crafted `exit` | frozen `check_receipt` | mutant |
|---|---|---|
| `0.0` (float) | `exit is not an integer: 0.0` (exit 1) | **no defects (exit 0)** |
| `false` (bool, `passed true`) | `exit is not an integer: False` | **no defects (exit 0)** |
| `"0"` (string) | `exit is not an integer: '0'` | still refused, by the `passed`/exit cross-check |

The gate's re-implemented `check_receipt_like` refuses all three, its selftest carries
`red-receipt-bool-exit`, and `gate_receipt_schema` refuses a filed gate receipt with `exit: "0"`
(measured: finding `exit is not an integer: '0'`). So the *shape* is closed at the record; the
mutation is not detected, and the round-77 suite still has 13 cases and still accepts both
surviving shapes.

## 4. The honest limit set — what neither instrument nor the gate can see

1. **No re-derivation at the receipt's own rev.** Both read receipts at the *measured* rev;
   `auth_findings` reads only the instrument blob at `receipt.rev`. A receipt that names an older
   rev is never compared with that rev's bytes (measured: §3.1).
2. **No instrument re-execution.** `receipt_auth` is a digest chain (rev + instrument sha), not a
   measurement; a receipt produced from a tree that differs from its named rev is admitted.
3. **The named receipt is never validated.** verdict-bind validates only its own output (:449);
   the gate binds fields and auth. Measured (`limits.py`): a named receipt whose own `--validate`
   exits 1 (`cells absent or empty`) is accepted by verdict-bind (`exit 0`, `bound 2`) and by the
   gate's scan (`bound 2`, `findings []`).
4. **Prose and no-group verdicts.** A group with no parsable clause is `prose` (:368-372) and adds
   no defect; the gate skips groups that are neither receipt-anchored nor parsable.
5. **No array-element path.** verdict-bind binds top-level keys only; the gate resolves a key at
   any depth but only when it is unique. `fixtures[3].refused true` cannot be expressed; the
   post-freeze fix binds the top-level aggregate instead.
6. **Scope divergence.** verdict-bind: rows with a numeral ≥ 73 in the round cell (`\d+`) plus
   every Core bullet. Gate: rows with a *bare* numeral ≥ 78 (`^\d+$`) plus only Core bullets
   naming round-78 paths. On the same record the binder binds **37** clauses over 13 rows; the
   gate's genuine scan binds **12** over 4 cells. The gate's clean verdict speaks for about a
   third of the record's bound clauses.
7. **No population floor.** `ok = not defects and bound > 0` (:447); the gate records but does not
   threshold the population. Deleting the inconvenient cell is green in both; the floors (18+, 11+)
   live only in the claims' predicates.
8. **The base arm reads the worktree.** `materialise` copies `Path(root, FIXTURE_ROOT, …)` and
   `run_base` runs `Path(lane_root, PINNED_INSTRUMENTS[…])`, while receipts are read at rev. A
   dirty worktree changes what the base arm measures. This probe pins both (fixtures by
   `git show 3e6b1efc`, instruments by sha equality).
9. **`env_keys` is a shape check.** It is the sorted non-empty keys from a four-key allowlist; a
   secret placed in `HOME`/`TMPDIR` is inside the allowlist. No env values are recorded anywhere
   in this seat's receipts.

## 5. Divergences found while reconstructing

- **The frozen gate over-refuses the defined token.** `near_miss_field` is tested before the
  grammar in `780089e3`, so `validate defect-free` is reported as an undefined spelling, and
  `refused` is ambiguous (it occurs in every fixture entry). On the record at `9de14dd6` the
  frozen gate reports **2 findings, 5 bound**; the landed gate `a86f6d4d` (commit `01768ac5`)
  reports **0 findings, 12 bound**. Both revisions are disclosed in
  `claims.json instrument_supersessions`.
- **`clean_run` reads the filing receipt, not the clone-run arm its class names.**
  `judge_receipt_fixture` loads `FILING` for rule `clean_run`; b1's base arm is `clone-run`. The
  fixture is still refused (b1's filing receipt is the same failing run), so the battery is green,
  but the rule does not exercise the arm the class declares.
- **Freeze pin vs landed gate.** `claims.json instruments` still names `780089e3…` while the
  landed file is `a86f6d4d…`. The difference is declared (two supersession entries), so it is a
  disclosed supersession, not silent drift — but a reader comparing only the pin map would name the
  older blob.

## 6. Bounds honoured

No lane file was edited; the only writes are this directory
(`.ufo/waves/round-78/w1/RevengerInstruments/`). No `git`/`jj` mutation outside the private
fixture repos under `/fast/scratch/hyaku/kaidoku-r78/RevengerInstruments/` (each verified with
`rev-parse --show-toplevel` before every commit, and the scratch tree is removed at exit). No
environment dump and no config secret values: receipts carry argv, digests, verdict lines and key
names only.
