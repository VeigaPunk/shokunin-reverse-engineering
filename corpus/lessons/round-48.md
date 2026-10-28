# Round 48 — lessons

Lane `kaidoku`, round 48, attempt 1. Base `61b87d742032e65fca9c38267d7d6ed7e555edad`.
Declared freeze `0f06251bf6a3a6964c715f67243d4df12e854258` — a disclosed series A1–A4
(see `plans/round-48-claims.md` and the disclosures below).

## Gate

| row | source | accessed | located quote (≤25 words) | decision |
|---|---|---|---|---|
| S145 | https://plato.stanford.edu/entries/popper/ (SEP, *Karl Popper*, §2 The Problem of Demarcation; sha256 `2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207`) | 2026-10-28 | "if a theory is incompatible with possible empirical observations it is scientific; conversely, a theory which is compatible with all such observations" | **admit** (tier A, `mined`). Province check: the row grounds the lane's *instrument* discipline — a clause that cannot fail is not a check — which is the class A1–A4 each belong to; it makes no claim about any RE surface, and it is cited by this lesson only, not by a knowledge entry. |
| S146 | https://man7.org/linux/man-pages/man3/sysexits.h.3.html | 2026-10-28 | none — HTTP 404 (196-byte body, sha256 `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`) | **reject** (tier C, `rejected`). Reason: unreachable at this URL, so no locator exists to quote; `unreachable` is not fabrication, but it is also not evidence. Flip: open `man 3 sysexits` locally or the FreeBSD handbook page and quote the `EX_USAGE` line; then the row can ground exit 2 as a usage refusal. |

The admitted row grounds the round's own defect class rather than a reverse-engineering
surface, so it adds no coverage-map ground and no knowledge entry; the round's coverage
proxy stays where it was.

## Mistakes

- **M48-1 · `vacuous-clause` · evidence `plans/round-48-claims.md` amendment A1 and
  `.ufo/waves/round-48/controls/ctl-c2-a1-before.json` (`axis_score_cells {}` with
  `axis_score_bad []`) · captured-by `none`** — the record counter's axis-score parser
  read the evidence cell where it meant the score cell. The score-cell clause therefore
  examined no rows, while the separate `axes_atoms` count did not reveal that the score
  values were unparsed. **Fix:** read the score cell directly, expose `axis_score_cells`
  in the receipt, and compare the cell's current value against the first fraction. The
  same round found additional instrument-input defects in A2–A8; the rule for the next
  round is: **before freezing, run the candidate on one complete green artefact and each
  forgery; for every clause, record the exact input cell it reads and a concrete
  counterexample.** A clause or battery that has not run on a green candidate remains
  unproven.

## Freeze series (disclosed, not folded)

| amendment | defect | red-before |
|---|---|---|
| A1 | the axis-score parser read the evidence cell; no score cells were examined | `controls/ctl-c2-a1-before.json` |
| A2 | the exit-0 classifier rejected the legitimate `0=met with failing empty` description | 16-row diagnostic at A1 bytes; `plans/round-48-claims.md` A2 |
| A3 | the census clause compared a derived object with a committed list | `controls/ctl-c1-a3-simulation.json` |
| A4 | the classifier accepted `0=not met`; the registry parser skipped a row with spaces after `|` | `w1/C1Gold.md`, `w1/CritAxis.md` |
| A5 | the C1 battery fixture omitted census claim inputs; C2 correction heading matched quoted prose | preflight receipts recorded in the A5 disclosure |
| A6 | C1 battery fixture omitted census tool paths | preflight receipt recorded in the A6 disclosure |
| A7 | score-cell mutation read the committed card; quote and axes-correction mutants were no-ops; gold tautology lacked the seat token | `controls/ctl-c2-a7-before.json` |
| A8 | gold tautology dropped a wrapped seats sentence; quote mutation targeted a section without a quote | preflight counterexample recorded in the A8 disclosure |

## Routed defects (for round 49)

- **R48-CL1 — worktree-sourced gate helper (HIGH, C2OracleLimit).** `record2.py` loads
  `record.py` from the committed revision, but both it and the oracle resolve
  `tools/round-46/gate.py` from the invoking worktree. The seat's stub attack on
  `record.py` did not move the verdict; no gate-tamper exploit was measured. Pin the
  helper's bytes and add an isolated worktree-tamper arm.
- **R48-CL2 — lexical class is not source truth (HIGH, MutC1Rows).** A segment beginning
  `0=met` and then stating that exit 0 means failure still classifies as success. This
  was measured by the seat's scratch probe; the counter asserts presence/polarity of
  class words but does not compare a registry description with the named tool's actual
  behavior. Bind the row to a source-derived exit contract or explicitly narrow its claim.
- **R48-CL3 — quote correction may cite an unrelated receipt (MEDIUM, MutC2Corr).** The
  seat identified a possible cross-round receipt-laundering path in `_quote_correction`;
  it is source inspection only, not a measured green exploit. Build a fixture with a
  wrong quote in round 47 and a matching value only in a different round's receipt.
- **R48-CL4 — structural floor is bounded, not record completeness (MEDIUM, CritClaims).**
  One seat/path/revision atom and one claim ID per section do not prove that all claimed
  work is recorded. Preserve the bounded language; do not promote this floor to a
  completeness guarantee.
- **R48-CL5 — battery skips when the genuine card is red (MEDIUM, C2Battery).** The
  measured pre-landing control skips all five mutant verdicts when a structural clause
  fails. Keep the after-state battery receipt green, and consider an independent mutation
  runner that can assess mutants even when the genuine card fails.

