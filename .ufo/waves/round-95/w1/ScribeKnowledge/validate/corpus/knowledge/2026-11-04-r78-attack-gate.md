source: S292 — https://docs.python.org/3/library/stdtypes.html — Python 3.15.2 docs, Numeric Types, line 441; opened 2026-11-04
verified-at: 2026-11-04
recheck: 180d

# A receipt's integer field is not satisfied by a boolean, and an instrument must refuse the shapes it names

## The typed comparison rests on the language, not on an accident

The docs state the relation the guard depends on: "In addition, Booleans are a subtype of integers."
(`stdtypes.html`, snapshot line 441, 814 496 B, sha256 `16f072e1…`). So
`isinstance(receipt["exit"], int)` alone accepts `True`; the receipt contract has to say
`isinstance(x, int) and not isinstance(x, bool)`. Both instruments do
(`tools/round-77/prefile-receipt.py` `check_receipt`; `tools/round-78/attack-gate.py`
`check_receipt_like`), and the selftest carries the red (`red-receipt-bool-exit`, exact string
`exit is not an integer: True`). The row grounds the guard, not the receipt schema: JSON's own value
taxonomy is S289, held at round 77.

## A computed `defect` status that is never collected is not a check

Round 77's binder classifies a clause as `bound`, `unbound` or `defect`, and `bind_cell` appends
only the third kind's *reason* to no list at all: the status is computed and dropped, so a clause
whose atom table is absent (`no_atoms`) leaves `defects []`, `mismatch_count 0` and `ok true` when
any other clause binds. The round-78 fixture `a6-dropped-defect` is the shape: `(D24 true,
mismatch_count 0)` against a receipt with no `atoms` array is accepted at exit 0 by
`tools/round-77/verdict-bind.py`, and `tools/round-78/attack-gate.py`'s `unbound_verdict` refuses it
(evidence: `.ufo/waves/round-78/pre/c1-at-base.json`, fixture `dropped-defect`, base
`exit 0, mismatch_count 0`, gate reason `{"reason": "no_atoms"}`). The rule is general: a status an
instrument computes is either scored or it is decoration.

## What the gate does not establish

`receipt_auth` binds a receipt's `rev` and `instrument.sha256` to the blob at that rev: a reader can
re-derive that the receipt names the instrument bytes the lane holds at that commit. It does not
authenticate the author — a hand-written receipt that copies a real rev and a real instrument digest
still passes auth and is caught only by a value clause that disagrees with it. Signed receipts stay
Frontier (`PROVINCE.md`, round-78 Still Frontier).

## Instrument behaviour, on committed bytes

- Ten attack classes, one fixture each, under `.ufo/waves/round-78/attacks/`; the generator is
  committed beside them (`gen-fixtures.py`) and the gate's `materialise()` rebuilds each fixture as a
  two-commit repo so a receipt's rev resolves to a commit that really carries the pinned blob.
- Base arm: the frozen round-77 instruments accept all ten (`base_accepted 10`, measured, not
  asserted: `.ufo/waves/round-78/l1/scores/c1-at-record.json`).
- After arm: the gate refuses all ten by their declared rules, and the real record is clean under
  every rule (`genuine.mismatch_count 0`, `genuine.defects []`).
- Controls: `base-only` refuses 0 of 10; `all-refuse` forces a genuine defect; `no-fixtures` scores
  0 base acceptances (`.ufo/waves/round-78/pre/controls/`).
