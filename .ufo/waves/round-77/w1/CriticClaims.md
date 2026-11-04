# CriticClaims — round-77 wave 1 — adversarial falsification of R77-C1 / R77-C2

Seat: CriticClaims-19. Instruments verified against the freeze pins
(`verdict-bind.py` 45280392…a9e7, `prefile-receipt.py` 174eedb5…d3fd) before every run.
All runs used the frozen instruments at committed revisions only; fixture commits lived in
scratch repos (`/fast/scratch/hyaku/kaidoku-r77/CriticClaims/FA|FB|FC|FD.*`, toplevel-asserted
before each commit) and were deleted before this report was finalized. Lane writes: this
directory only. Raw receipts: `.ufo/waves/round-77/w1/CriticClaims/receipts/`
(structured verdict: `receipts/../report.json`).

## 0. Baselines — the frozen "before" halves hold exactly

| run | exit | counter | detail |
|---|---|---|---|
| C1 @ base `188562d4` | 1 | `mismatch_count 4` | exactly `capability-row binding` (D24 true→false, mismatch 0→1) and PROVINCE.md line 585 (same two clauses); 21 bound, 9 in-scope, 3 unbound |
| C1 @ freeze `6767a879` | 1 | `mismatch_count 4` | identical population — C1 needs no round-77 artifact |
| C2 @ base `188562d4` | 1 | `arms_ok 4 of 6` | clone-run rc 0 PASS; record-receipt absent; **five** round-76 gate receipts without exit (predicate prose says three — erratum `11f0b19e` already acknowledges) |
| C2 @ freeze `6767a879` | 1 | `arms_ok 4 of 6` | gate-exits correctly refuses an empty set; but clone-run is **met with `rc 1, prefile: FAIL`** (see C2-2) |
| C2 @ tip `11f0b19e` | 1 | `arms_ok 5 of 6` | landing is one filing receipt away from 6/6; gate-exits met (see C2-3) |
| selftests | 0/0 | — | C1 15 cases failures [], C2 13 cases failures [] |
| `ctl-pointer-only` (round-76 record-audit @ base) | 0 | `mismatch_count 0` | 9/9 atoms true while the false annotation stands — the control behaves as claimed |

## 1. R77-C1 — FALSIFIED (over-set). Three independent records score `exit 0, mismatch_count 0` while false

**C1-1 · forged-receipt re-point** (fixture FA, rev `99956ecf…`, `receipts/c1-FA.json`).
Both false cells re-pointed from `.ufo/waves/round-76/l1/scores/c1-at-landing.json` to a
hand-authored `.ufo/waves/round-77/pre/green-r77.json`
(`{"atoms":[{"id":"D24_capability_rows","ok":true}],"mismatch_count":0,...}`) with the same
clauses `(D24 true, mismatch_count 0)`. Result: `exit 0, mismatch_count 0, bound_clauses 21`.
The round-76 receipt still in the same tree records `D24_capability_rows false` /
`mismatch_count 1`. The frozen grammar accepts the construction: `nearest_path` binds the group
to *any* committed `.json`; the instrument has no receipt-authentication clause (no rev pin, no
instrument-sha pin, no digest). This is kill-rule shape "a path from another cell" — declared,
not detected.

**C1-2 · re-punctuation, no new files** (fixture FB, rev `86f1910f…`, `receipts/c1-FB.json`).
Both false cells rewritten `(D24 true, mismatch_count 0)` → `(D24: true, mismatch 0)` plus one
no-op true clause (`, mismatch_count 0`) appended to a green cell. Result: `exit 0,
mismatch_count 0, bound_clauses 18` — the predicate's `bound_clauses >= 18` floor is met while
the false values still stand verbatim in the record against a receipt that says false/1. Why the
grammar accepts it: `QUALIFIER_RE` strips `D24:` and the remainder `true` matches no clause
grammar → prose; `mismatch 0` parses as FIELD with an unknown field → *unbound*, and unbound is
neither a defect nor gated by `ok` (only reported). Only `in_scope_rows >= 11` (9 here — a
quantity the landing raises by adding rows, independent of truth) keeps this fixture from the
full landing shape. This is kill-rule shape "an edited cell that keeps the false value" —
declared, not detected.

**C1-3 · negated cells** (fixture FC, rev `27201f76…`, `receipts/c1-FC.json`). Both cells →
`(the receipt does not record D24 false, and no mismatches were recorded)`. Result: `exit 0,
mismatch_count 0, bound_clauses 17`. Kill-rule shape "a negated cell" — declared, not detected.

**Attacks that fail (counter holds).** `validate defect-free` on an absent validate block →
defect `no_validate`; on a non-defect-free block → `value_mismatch`. Atom shorthand `D24` with
zero or ≥2 matches → `unbound` (`unknown_atom`/`ambiguous_atom`), never a pass. `typed_equal`
blocks the true/1 confusion. A resolving pointer to an *absent* receipt → `absent_receipt`
defect; a bound clause with no JSON pointer → `no_json_receipt` defect.

**Under-set hunt.** (a) Field alias: the *frozen record itself* already carries `mismatch 1`
(PROVINCE line 585, naming `.ufo/waves/round-76/pre/c1-at-base.json`, which has
`mismatch_count 1` and no `mismatch` key) — a reader-true clause that binds nothing; the
mirror-image reader-false `mismatch 0` is equally unbound. The grammar cannot tell them apart.
(b) Qualifier: any `<word>:` prefix is stripped and discarded. (c) Surfaces left unbound by the
frozen scope: rows with first-working round < 73 (30 of 39 rows at base, including the round-72
row asserting `11/11` against a base receipt of 9/11), PROVINCE bullets outside `- **Core — `,
SCORECARD claim-table cells (e.g. the R76-C1 row's `0 mismatches` prose), and all plan files.
The predicate honestly names its scope, so these are documented blind spots — but
`mismatch_count 0` over the frozen scope is not `mismatch_count 0` over the record a reader
reads.

**Selftest clause fails under both readings.** "15 cases carry one red fixture per failure
shape": kill-rule shapes with *no* red fixture — negated cell, clause outside the group,
path-from-another-cell, bound-floor-met-by-prose, mismatch falling via scope-row removal, and
the re-punctuated keep-the-false-value edit; docstring statuses with no red — `no_atoms`,
`no_pristine`, `no_validate` (absent block), `bad_literal`. Two cases (`green-prose`,
`unbound-unknown-field`) actively codify two of the exploited holes as green (they assert
`defects == []`).

**Smallest safe correction (lane precedent exists).** Rounds 70–71 already bind receipts to
`rev` + instrument sha256 in `--check-receipt` ("a field-consistent forgery is rejected", A10
transplant rejection). Apply the same pattern here: each named receipt must carry
`rev == measured rev` and `instrument.sha256 ==` the frozen pin, else defect; count unbound
verdict-shaped clauses as defects (the landing can legitimately reach `unbound 0` by re-wording
the wild `mismatch 1` into a binding `mismatch_count 1`); add the missing red fixtures. That
makes C1 fixable, not inherently fragile.

## 2. R77-C2 — FALSIFIED (over-set). `arms_ok 6 of 6, exit 0` reached at a revision where no gate ever ran

**C2-1 · forged battery** (fixture FD, rev `2959d7e2…`, `receipts/c2-FD.json`). Two committed
files: a hand-written filing receipt — internally consistent (correct stdout digest, `passed`
following from exit+verdict, four-key `env_keys`, argv naming the gate) but with
`rev = 188562d4` (stale, not the measured revision) — and `gate-at-tip.json` = `{"exit": 0}`.
Result: `exit 0, arms_ok 6 of 6, ok true, validate defect-free`. Two kill-rule shapes are
violated undetected:

- "a filing receipt whose rev is not the filing revision" — the A2 arm calls
  `check_receipt(receipt)` **without** `expect_rev`; the rev-binding machinery exists (A6 and
  the CLI use it) but A2 never does.
- A3's gate receipts have no stdout, no digest, no argv clause — a one-key JSON satisfies
  "every gate receipt … carrying its exit". The routed-defect-3 repair is satisfiable by a fake.

**C2-2 · A1 accepts a FAIL run.** At the untouched freeze the battery's clone-run arm is met
`true` with observed `rc 1, prefile: FAIL` (`receipts/c2-freeze.json`). `met = rc in {0,1} and
verdict-line and clean-receipt` — an arm whose expected observation is "a clean clone run" is
met by a failing run. Kill-rule shape "an arm met for a reason other than its expected
observation", live on the frozen state, no fixture needed.

**C2-3 · A3 met by the wrong gate (live at tip `11f0b19e`).** The landed round-77 gate receipts
(`gate-at-freeze.json`, `gate-at-record.json`) record argv of
`tools/round-29/freeze-gate.py` — not the claim's named filing gate
`tools/round-29/prefile-check.sh` — and A3, which checks only that a `gate-*.json` carries an
int exit, is met by them (`receipts/c2-tip.json`). The claim's surface is "the filing gate
invocation and the receipts that retain it"; the newest round dir's receipts retain a different
instrument.

**Attacks that fail (counter holds).** Empty gate set refused (freeze: 0 round-77 gate receipts
→ unmet). `exit=0` inside prose refused (A3's txt path anchors `^exit=N$`). Digest not covering
stdout refused; stale `passed` refused (re-derived from exit+verdict); non-int exit refused;
`env_keys` four-key allowlist enforced; reds A4–A6 refused by construction.

**Smallest safe correction.** A2: `check_receipt(receipt, expect_rev=rev)` (one line). A3:
require gate receipts to pass `check_receipt` — argv naming `prefile-check.sh`, digest over
stdout — or pin their digests. A1: met requires `token == "PASS"`. Selftest reds for: A1-FAIL
accepted, stale-rev filing receipt, empty gate set.

## 3. Coupling — separability confirmed, and insufficient

- C1 at freeze (no round-77 gate receipts, no filing receipt): `exit 1, mismatch_count 4`,
  population byte-identical to base. C1 at FD (forged C2 receipts present): still
  `mismatch_count 4, exit 1`. C1 never reads C2's artifacts.
- C2 at FB (both false annotations standing): `exit 1, arms_ok 4 of 6` — identical to base and
  freeze. C2 never reads SCORECARD/PROVINCE cells.

The claims' causal-separability section is accurate. But both counters are individually
forgeable (§1, §2), so separability of the counters does not protect the round's verdicts.

## 4. Verdicts

| claim | verdict | falsified by | survives |
|---|---|---|---|
| R77-C1 | **FALSIFIED (over-set)** | FA, FB, FC fixtures — three record states score `exit 0, mismatch_count 0` while the record is false; bound floor met at exactly 18 by a no-op clause | the before-arm is exact (exit 1, mismatch 4, exactly the two labels, 21/9); selftest runs 15/15 green; ctl-pointer-only behaves as claimed |
| R77-C2 | **FALSIFIED (over-set)** | FD fixture — `arms_ok 6 of 6, exit 0` with a stale-rev forged filing receipt and a one-key gate receipt; A1-FAIL acceptance live at the freeze; A3 met by freeze-gate.py receipts live at tip | the before-arm is exact (arms_ok 4; five-not-three already erratum'd); selftest 13/13 green; empty-set and prose-exit shapes refused; check_receipt's clause re-derivation is honest |

Both claims are *fixable*: every hole above has a named one-to-three-line correction, and the
receipt-authentication pattern the C1 fix needs already exists in-lane (rounds 70–71).

## 5. Risks / notes for the L1

- The `in_scope_rows >= 11` floor is quantitative, not truth-bound: it is satisfiable by adding
  rows regardless of annotation honesty; do not read it as an integrity check.
- The landing's remaining step (commit `prefile-at-filing.json`) will turn C2 green at tip even
  though A2 would accept a stale-`rev` receipt — land the A2 `expect_rev` fix before or with the
  filing receipt.
- Scratch fixture repos were deleted; every fixture is reproducible from the edits quoted in
  `report.json` (each is a one-string replacement in the two false cells / two committed files).
- No tools installed; pacman pause respected. No lane file outside `.ufo/waves/round-77/w1/CriticClaims/`
  was written; no git mutation outside scratch fixture repos.
