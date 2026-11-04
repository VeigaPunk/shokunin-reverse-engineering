# ScribeLesson — round-78 lesson draft (Mistakes rows + QUALITY criteria)

Drafts: `.ufo/waves/round-78/w1/ScribeLesson/mistakes.md` (ten `## Mistakes` rows, one per attack
class in `tools/round-78/attack-gate.py` `ATTACKS`) and
`.ufo/waves/round-78/w1/ScribeLesson/quality.md` (QUALITY rows 136 and 137, bullet style of rows
116–135). Both are paste-ready and append-only: no filed byte of `corpus/lessons/round-77.md` or
`corpus/QUALITY.md` was touched. Structured findings: `report.json` in the same directory.

Sources read (committed bytes and read-only git): `.ufo/waves/round-77/w1/CriticClaims.md` §1–§2
(and §5); `corpus/lessons/round-77-verifier-spotcheck.md` §2, §6, §8; `tools/round-78/attack-gate.py`
(`ATTACKS`, `bind_clause`, `judge_group`, `auth_findings`, `check_receipt_like`,
`judge_receipt_fixture`, `resolve_field`, `selftest`); `tools/round-77/verdict-bind.py` (`bind`,
`bind_cell`); `tools/round-78/surface-recheck.py` (`RE_JDK`, `parse_record`, `compare`,
`token_grep`); `plans/round-78-claims.md` R78-C1/R78-C2 and the disposition paragraph;
`PROVINCE.md` at `6205ec8c` and at HEAD `93753d88`; the ten fixture trees; the round-78 `pre/`
receipts; `corpus/QUALITY.md` rows 116–135; `.ufo/waves/round-76/w1/ScribeLesson.md` for report shape.

## Findings

1. **The ten rows map one-to-one onto the ten declared rules, and each base arm is the frozen
   instrument's *acceptance*, not a restatement.** `.ufo/waves/round-78/pre/c1-at-base.json` (rev
   `3e6b1efc`) records `fixtures_total 10`, `base_accepted 10`, `refused 10`, `validate.defects []`.
   The per-fixture observations I quote are that receipt's own `base.observed` strings, e.g.
   `a6-dropped-defect → "exit 0, mismatch_count 0"`, `b1-fail-run → "arm clone-run met True: rc 1,
   prefile: FAIL, receipt_defects []"`, `b3-one-key-gate → "arm gate-exits met True: round-78: 1 gate
   receipts, missing []"`. No instrument was re-run for this report.
2. **The dropped-defect class is a code-path fact, quoted with line numbers.** `bind` returns
   `(False, "defect", {"reason": "no_atoms"})` at `verdict-bind.py:203`; `bind_cell` appends to
   `defects` only under `status == "bound" and not ok` (`:394-400`), so the `else` at `:401-402`
   counts the clause `unbound` and leaves `defects []` while `row["status"]` stays `defect`
   (`:391-392`, `:403`). The round-78 collector is `attack-gate.py:405-407` (`unbound_verdict`).
   QUALITY row 136 states the general rule; the corresponding Mistakes row names the same path.
3. **`a5` and `a6` are different classes even though both were "unbound" at round 77.** `a5` is a
   field the closed top-level grammar could not resolve (`nested.json` records
   `arms[0].observed.verdict.forged_detected = false` against the cell's `forged_detected true`);
   the round-78 `resolve_field` walks the whole receipt and binds it uniquely, then typed-compares
   (`value_mismatch`). `a6` is a clause status computed and then dropped. Rows 5 (nested) and 6
   (dropped) keep them apart, and the round-77 spot-check §2 supplies the honest-limit quotation
   for the first.
4. **`grep` for the JDK trap confirms the parse position.** `git show 6205ec8c:PROVINCE.md` carries
   exactly one `openjdk version "…"` occurrence, and it is the stale `21.0.12.1` (line 25); the
   round-78 record (`PROVINCE.md:27` at HEAD `93753d88`) carries exactly one, the live `21.0.13`, while the superseded
   token survives only in the "the 2026-10-20 values were `21.0.12.1`" clause and the table note at
   line 49 — neither in the `openjdk version "…"` form the declared `RE_JDK` selects. That is the
   concrete instance behind QUALITY row 137; the first-match hazard is `parse_record`'s
   `RE_JDK.search(flat)`.
5. **The record repair is measured and the two base mismatches are gone.** On the base receipt
   (`.ufo/waves/round-78/pre/c2-at-base.json`, rev `6205ec8c`) the instrument records
   `checks_total 8`, `matched 6`, `mismatches 2`, `unparsed 0`, `record.jdk_version 21.0.12.1`
   against `live 21.0.13`, and `omp_disable_claim false` against `live.omp_disable true` — exactly
   the two the frozen predicate names. The untracked `.ufo/waves/round-78/l1/scores/c2-at-record.json`
   (rev `218c5aa8`, `checked_at` 2026-11-04T09:12:14-03:00) records `matched 8`, `mismatches 0`,
   `record.jdk_version 21.0.13` against `live 21.0.13`, and `omp_disable_claim true` against
   `live.omp_disable true`: the same eight checks, both repairs applied.
6. **Round-77 routed-defect coverage.** §8 items 8 (`b1`), 9 (`b2`), 10 (`a1`) and §6 item 7 (the
   `c2-nonint-exit-accepted` survivor in `b3`'s `red-receipt-bool-exit`; the grammar limits in
   `a2`/`a3`/`a5`) are represented by rows; §8 item 11's red-fixture duty is visible in
   `attack-gate.py --selftest` (21 cases, `failures=0`, `.ufo/waves/round-78/pre/selftest-c1.json`)
   with `red-qualified-atom`, `red-near-miss`, `red-negated`, `red-ambiguous`, `red-absent-field`,
   `red-type-mismatch`, `red-receipt-auth`, `red-receipt-no-exit`, `red-receipt-bool-exit`,
   `red-receipt-stale-rev` beside the green look-alikes. Rows do not claim more than those cases
   exercise: no selftest case is named for `clean_run`, `gate_receipt_schema`, `gate_receipt_rev` or
   `value_mismatch`, which are fixture-refused (`refused true`) rather than selftest-red.
7. **One class has no round-77 kill-rule sentence to quote.** The dropped-defect class (§1's
   selftest-clause critique lists `no_atoms` among statuses with "no red fixture") was never named as
   a kill rule; the row therefore cites the code path and the selftest-gap paragraph rather than a
   declared sentence. This is a limit of the evidence, not a strengthened claim.
8. **Base revs are not uniform and the rows say so.** The attack gate's base receipt is measured at
   the declaration `3e6b1efc`; the surface base receipt is measured at `6205ec8c`; the record
   repair's receipt is measured at `218c5aa8`. Each citation uses the receipt it names.

## Risks / notes for the landing (L1)

- **`PROVINCE.md` now names a receipt that exists only untracked.** Lines 18–19, 27 and 49 cite
  `.ufo/waves/round-78/l1/scores/c2-at-record.json`; at the observed instant (2026-11-04T09:15:39-03:00,
  HEAD `93753d88`) that file exists in the working tree, untracked, and records `checked_at`
  2026-11-04T09:12:14-03:00, rev `218c5aa8`, `matched 8`, `mismatches 0`, `record.jdk_version 21.0.13`,
  `omp_disable_claim true`. The landing must commit it at the revision the record is measured at, or
  the pointer will not resolve; the sibling `.ufo/waves/round-78/l1/scores/c1-at-record.json` (also
  untracked, rev `218c5aa8`) currently exits 1 with `receipt_auth: absent at the measured revision`
  naming itself, which is exactly that failure. Both files are another seat's in-flight artifacts;
  this seat neither wrote nor edited them.
- **Row 136's "a receipt whose `defects []` coexists with a `status: defect` clause is itself a
  defect" is a rule, not an implemented check.** The round-78 gate collects the status; it does not
  re-read a produced receipt's clause list to detect the coexistence. If the L1 wants the second
  half enforced, it needs its own clause and a red; the row states the rule and cites the
  collector that exists.
- **QUALITY numbering.** `corpus/QUALITY.md` ends at row 135 in the bullet block under
  "Corrections appended — round 34 run-6 (2026-10-25)"; the draft uses 136 and 137 and appends
  under that section. If the landing opens a new section instead, the numbers still hold.
- **`mistakes.md` cells are long single lines** (the lane's table style); a Markdown formatter that
  wraps cells would break the paste. Append as-is.
- **No conflict found** between the frozen claims, the fixtures and the receipts I cite. The only
  discrepancy is item 7 (a class without a declared kill-rule sentence), reported as a limit.
