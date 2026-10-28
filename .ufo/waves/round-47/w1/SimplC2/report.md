# SimplC2 — YAGNI pass on `tools/round-47/record.py` (R47-C2)

Seat: leaf simplifier. Lane `kaidoku-shokunin`, round 47. Counter measured at the declared
freeze `07d2894eabe88c326e9036262f20ad02662c860d` (`record.py` sha256
`abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7`, 603 lines, byte-identical
at `HEAD` and in the worktree). The lane tree was read-only: every mutation ran on a scratch
copy or on a card text fed to `evaluate_text`. Receipts and fixtures in this directory
(`manifest.json`, `at-*.json`, `cli-*.json`, `card-matrix.json`, `probe2.json`, `fixtures/`).

Frozen-clause findings (F1–F3) are in `SimplC2.md`; this file answers the two assigned
questions and carries the keep/cut table.

## Q1 — is the `axes` class necessary for the calibration claim? **Yes — keep.**

1. **Contract.** Frozen predicate clause 2 requires all five classes and `collect_axes` is the
   only producer of `axes` atoms, and the only code anywhere in the counter that reads
   `## Owned axes`. Delete the class and every card fails clause 2
   (`no atoms of class(es) ['axes']`).
2. **Before-state.** Two of the four named before-mismatches in `ctl-c2-0-do-nothing.json` are
   axes atoms: `coverage 133/133` against derived `138/138`, `depth 20/20` against `23/23`.
   Without the class the do-nothing control would name two record defects, not four.
3. **Discrimination.** Forging only the current table's head (`138/138` → `199/199`;
   `card-matrix.json` case `axes-head-forged-199`) exits 1, `mismatches 1 != 0`. With the axes
   derivation bypassed (`mut/bypass`) the same card exits 0 — no other class reads that table,
   so this derivation is the sole guard.
4. **Not merely self-consistent.** At the freeze `depth_pair` derives `24/24` and
   `tools/round-47/exact.py --profile v3` reports `rule_blocks 24` (independent parser, same
   section); `coverage_pair` derives `138/138` and the shell recipe
   `git ls-tree -r --name-only <rev> corpus/knowledge | grep -c '\.md$'` prints `138`, with 138
   unique `2026-10-NN-*` tokens in the README coverage map. The axes numbers agree with two
   independent measurements.
5. **Cost.** ≈56 of 603 lines: `collect_axes` 13, `coverage_pair` 9, `depth_pair` 23,
   `axis_pairs` 3, the `derive` branch 7, four regexes. 9% of the file to cover the one claim
   surface the other four classes cannot see — the price is proportionate.

**Counter-finding (report, do not cut).** Clause 2 *as implemented* is self-referential:
`CLASSES` is the counter's own tuple, so removing the class from the tuple as well leaves the
counter green. The `mut/cut` variant exits 0 at the freeze and its receipt differs from
`cli-base.json` only in `atoms 41→39`, the vanished `atoms_by_class.axes`, and
`verified 40→38` (`cli-cut.json`, sha256 `e4b92ec1af2b8815…`). A receipt therefore cannot be
cited as evidence that "classes covers all five"; only the claim's prose binds it.

## Q2 — is `CORR_MIN = 2` a real floor or a formality? **Real as a count, a formality as a repair floor.**

- **Not implied by clause 1.** The landing card minus the seats correction line exits 1 with
  `failing: ["corrections 1 < 2"]` and nothing else; the identical card under `CORR_MIN = 1`
  exits 0 (`card-matrix.json` cases `corrections-1-landing-minus-seats` and
  `corrections-1-minus-seats-CORR_MIN-1`). The constant is the sole discriminator there, so it
  is not vacuous.
- **It counts lines, not repairs.** At the freeze the receipt reads `corrections 2`,
  `exempted 1`: the seats line exempts nothing (round-45 has scrolled out of the last-two
  window; A3's historical allowance) and the window line is the only repair.
- **Fully satisfiable by decoration.** A card with *zero* repairs — the round-46 window sentence
  rewritten in place with a concrete pair that reproduces as empty, both original correction
  lines neutralised, two true historical `seats` corrections added (round-43 `2 waves, 64 seats
  total`, round-44 `2 waves, 79 seats total`) — exits 0 with `exempted []`
  (`card-matrix.json` case `zero-repair-two-decorative`). The counter cannot tell "two
  re-derived corrections" from "two true sentences about old rounds", and it has no clause
  binding the claim's append-only discipline: silently rewriting the false sentences instead of
  appending corrections scores green.
- **Tuned to the landing.** 2 is exactly the number of *parsed* correction lines the landing
  wrote — the card carries 4, the parser sees 2 (F1 in `SimplC2.md`). `CORR_MIN = 3` would fail
  the landing; the constant equals the artefact it measures.
- **Contract.** Frozen clause 3 says `corrections >= 2`, so the counter must keep it. Keep, and
  state in the landing evidence that correction #1 is historical and repairs nothing.

## Keep/cut table

| # | item | lines (at the freeze) | verdict | evidence |
|---|---|---|---|---|
| 1 | `axes` machinery: `collect_axes` (173–185), `coverage_pair` (104–112), `depth_pair` (115–137), `axis_pairs` (140–142), `derive` axes branch (223–229), `AXIS_ROW`/`FRAC`/`HARD_REF`/`CRAFT` | 104–185, 223–229 | **keep** | Q1 items 1–5; forged head red, bypass green; 24/24 and 138/138 cross-checked |
| 2 | second `if cls == "axes"` branch inside `corrects()` | 292–299 (8) | **cut** | unreachable twice: `CORR` (line 50) never yields `axes`, and the first `axes` branch returns before it; it also reads an undefined `atom` (latent `NameError`). Cut proved inert: 8-line diff, CLI receipt at the freeze byte-identical to base (`d366b080…`), `--selftest` 10/10 byte-identical (`8d722cc1…`) |
| 3 | first `if cls == "axes"` branch inside `corrects()` | 280–289 (10) | **cut *or* revive** | dead only because of the parser (F1). The code is correct: widening `CORR` to `(seats\|window\|path\|rev\|axes)` makes the landing parse 4 corrections, all re-derived (`corrections_bad []`, exit 0) and makes a false `199/199` axes correction red (`corrections_bad 1`, exit 1). Frozen bytes → report to L1, do not edit |
| 4 | `CORR_AXES` | 43 (1) | **cut with #2/#3** | only those two branches read it |
| 5 | unused locals `SELF` (32), `CLAIMS` (33), `corr_body` (325), `exempt_keys` (326), `known_pairs` (328) | 5 | **cut** | `ast` walk: zero loads. `known_pairs` is the residue of the A1-deleted window-pair clause; `corr_body` is the unused half of `corrections()`'s return |
| 6 | unused parameters: `collect(files, root, rev)` (145), `window_empty(rev)` (90), `selftest(with_battery)` / `run(with_battery)` (559) | 6 slots | **cut** | zero loads; signature-only weight |
| 7 | `CORR_MIN = 2` | 37 | **keep** | Q2; contract clause 3. Flag: counts lines, not repairs |
| 8 | `EXEMPT_MAX = 3` | 36 | **keep** | observed `exempted 1`, slack 2. Note: one `window` correction exempts *every* placeholder-window atom in scope (a placeholder added to the round-47 section is exempted by the round-46 correction, exit 0) — clause 4 permits it, the cap bounds it |
| 9 | `--selftest` | 546–560 | **keep flag** | unusable standalone: argparse exits 2 without `--root/--rev`; with them, 10 cases / 0 failures |
| 10 | `run_battery` root..tip forgery (A2) | 400–451 | **keep** | `correction_forgeries 3 / forgeries_green 0` in every receipt; the root..tip choice is what makes the forgery non-empty |

Net: 24 lines of dead code (items 2–5: 8 + 10 + 1 + 5) and 6 dead parameter slots are
removable with zero behavioural change — item 3 only under the current parser; items 2, 4, 5
are dead under any parser, and item 3 is the code the frozen clause 3 presumes exists.

## Tradeoff

Cutting #2/#4/#5 is free — proved byte-identical receipts — and removes the only latent
`NameError` in the file. Cutting #3 is *not* free under a future amendment that repairs the
parser, which is exactly the amendment F1 argues for; the two facts should be decided together
by L1, not by a simplifier acting on frozen bytes.
