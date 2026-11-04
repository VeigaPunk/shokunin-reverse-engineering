# Round 77 — a claimed verdict is re-derived from the receipt it names, and the prefile gate keeps a receipt

Base: `188562d43e3cc58b217ad7aa763fb296c5b8a0b7`.
Declaration: `819cf30e2fc35d91a69df1b2a42a025741c7d0ef`.
Freeze: `6767a879c6a3f386a9c3fc9d332c794f2d9ea914`.
Contract: `plans/round-77-claims.md` and `.ufo/waves/round-77/claims.json`.
Axes: calibration (R77-C1, the annotation verdict bound to its receipt) and operability (R77-C2, the filing gate's retained receipt).

## Gate

Every source below was opened this round with one GET each; snapshots, byte counts and sha256s are in
`.ufo/waves/round-77/l1/sources/`. Quotes are literal contiguous excerpts with their snapshot line.

| source / decision | URL | accessed | located quote (≤25 words) | digestion |
|---|---|---|---|---|
| S289, RFC 8259 section 3 Values, admit (mined) | https://www.rfc-editor.org/rfc/rfc8259.txt | 2026-11-04 (HTTP 200, 28 360 B, sha256 `61a5378f4255c720…`) | "A JSON value MUST be an object, array, number, or string, or one of" (16 words; section 3 Values, line 298) | JSON's three literal names (`false`, `null`, `true`) are not numbers, so a claimed `true` cannot satisfy a field holding `1`: the typed comparison in `verdict-bind.py` rests on this value taxonomy, not on Python's `True == 1`. The row does not claim schema conformance or REA Evidence authority. |
| S290, GNU Bash Reference Manual, admit (mined) | https://www.gnu.org/software/bash/manual/bash.html | 2026-11-04 (HTTP 200, 1 040 954 B, sha256 `78d0eefbe60cfe73…`) | "Bash itself returns the exit status of the last command" (11 words; section 3.7.5 Exit Status, line 4435) | A shell returns the last command's exit status, so a wrapper that runs the gate and records the shell's exit records the gate's own verdict. The row grounds the field, never the gate's correctness. |
| S291, `ast.literal_eval`, reject | https://docs.python.org/3/library/ast.html | 2026-11-04 (HTTP 200, 362 493 B, sha256 `8cacd731a2e0af73…`) | "Evaluate an expression node or a string containing only a Python literal or" (15 words; `ast.literal_eval`, line 2760) | REJECTED: the annotation grammar is not a Python literal grammar; `literal_eval` accepts Python-only spellings (`True`, `None`) the records never use and would widen the grammar past the JSON literals the receipts hold. Flip: the annotation grammar becomes a Python literal grammar. Consumer search (QUALITY row 36): `grep -c 'literal_eval' tools/round-77/verdict-bind.py` → 0. |

**Census.** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` at round start: exit 0,
194 rows, 23 W04 warnings (`.ufo/waves/round-77/l1/census-start.txt`). At round end: exit 0, 197 rows
(`l1/census-end.txt`). Three rows enter (S289 mined, S290 mined, S291 rejected); no existing row's
`status`/`recheck`/`used-by` changes.

**Spot-check (non-author).** The round-76 closure's outside document is the round's population, and the
round-77 non-author spot-check re-opens the sample this lesson records; its verdicts are in
`corpus/lessons/round-77-verifier-spotcheck.md` (filed by the closure session, not by this lane).

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| **record-vs-receipt** — a verdict written beside a resolving pointer was never read by the atom built to police the record. Three files said `c1-at-landing.json (D24 true, mismatch_count 0)` while the receipt records `exit 1`, `mismatch_count 1`, `D24 false`; `D24_capability_rows` was green because it checked that the path resolves, never what the cell claims. | `corpus/lessons/round-76-verifier-spotcheck.md` §6 items 1 and 5; `.ufo/waves/round-77/pre/c1-at-base.json` (4 defects, 21 bound clauses, 9 in-scope rows); `pre/controls-c1.json` (`ctl-pointer-only`: round-76 audit 0 mismatches on the same record) | `none` at write time — the atom's grammar had no notion of a claimed value, so the defect class could re-enter through the atom built to catch it | `tools/round-77/verdict-bind.py` with a closed 8-form grammar, 15 selftest cases and two red fixtures naming the exact false annotation; the fix is shown able to fail by `red-false-annotation` (2 defects on the same bytes that round 76 passed) and by the two do-nothing controls, neither of which reaches the target |

A second, smaller mistake was found **inside this round, before the freeze**: the first `red-of-total` selftest
case called `make_receipt(arms_total=2)` and the binder looked for `arms_ok_total`, so the case failed for the
wrong reason (the clause was unbound rather than mismatched). The fix maps `*_ok` fields to `*_total`, and the
case now fails for its declared reason. Class: **fixture for the wrong reason** — a red case that is red because
the code cannot see the field proves nothing about the comparison; captured by the selftest itself.

## Routed-defect disposition (round-76 spot-check §6)

| # | routed defect | disposition |
|---|---|---|
| 1 | the landing receipt is cited as green in three files | closed: the R76-C1 after-cell, the `capability-row binding` row and the PROVINCE round-76 evidence line now cite `c1-at-tip.json` and state the landing receipt's 1 by construction; R77-C1's counter re-derives both in-scope cells at the landing |
| 2 | tip-receipt revision prose is loose in the filed report | closed by an appended correction in `LOG.md` naming each receipt's own revision (`c1-at-tip.json`/`c2-at-tip.json` at `1ab1e164`, `gate-at-tip.txt` at `862c48a8`); the filed report stays byte-identical |
| 3 | the gate-at-tip "exit 0" is not in its receipt | closed: round-77's gate receipts are JSON carrying `exit`, and R77-C2's `gate-exits` arm requires every gate receipt in the newest round dir to carry one |
| 4 | the prefile check retains no receipt | closed: `tools/round-77/prefile-receipt.py --filing` writes `l1/scores/prefile-at-filing.json` (argv, rev, exit, verdict line, stdout digest, four-key env), cited in the report |
| 5 | D24 checks that the path resolves, not the verdict beside it | closed by R77-C1: the verdict is re-derived from the receipt the cell names, with two red fixtures |
