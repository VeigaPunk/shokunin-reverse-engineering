# MutTriV6 — round 52 wave 1 (build+attack)

**Verdict: the v6 mutation battery is specified with every expectation MEASURED (not
asserted) over the frozen 126-envelope corpus and a fixture scope. Four findings change
what the L1 freezes — one is a defect in the claim's own before-arm command, one is a
width defect in the v6 row's key that the corpus cannot witness, one is a census-clause
arithmetic the freeze will fail by exactly 7, and one is the carryover numbers moving
by +1.**

Deliverables: `.ufo/waves/round-52/w1/MutTriV6/battery.md` (the spec),
`probe/` (7 probe scripts), `evidence.json`, `design-dependence.json`,
`two-scope-witness.json`, `census-width.json`, `receipts.tsv` (18 receipts: command,
exit code, stdout sha256, UTC).

No REA, no `--data-run`, no carrier download, no network, no lane write outside this seat
directory, no git mutation in the lane or the fleet repo.

## The four findings that change what the L1 freezes

1. **The claim's before-arm command cannot resolve its own table.**
   `plans/round-52-claims.md:209` says the before-arm runs "with `--table
   tools/round-50-c3` (the v5 table bytes)". Measured: `tools/round-50-c3/` contains
   **only** `sqfs-triage-v5.py` and `__pycache__` — **no table file** (receipt R12). The
   v5 table bytes live in `SKILL.md` at the base revision (marker
   `<!-- sqfs-triage-table v5 -->`, line 550). **The `--table` argument must name a file,
   not a directory**, or the before-arm command is unrunnable as written.

2. **The v6 row's key is wider than the reader census it rests on, and the corpus cannot
   witness it.** The frozen census is **fixture-level**: `squashfs_v3_ddwrt` is **6/7
   NO-READER** — one of the seven measured ddwrt fixtures **has** a reader
   (`tools/round-50-c3/sqfs-triage-v5.py:150-156`). The v6 new row keys on the **family**
   `squashfs_v3_ddwrt`, so it prescribes `preserve-unresolved` for **every** ddwrt FAILED
   body, including the reader-backed one — **suppressing a cross-read the census says is
   executable**, the mirror image of the defect v6 fixes. Measured: the corpus carries
   **15** ddwrt envelopes but exactly **1** ddwrt FAILED body (the no-reader variant,
   receipt R10d), and on a synthetic reader-backed ddwrt FAILED body the v6 table
   answers `legacy-body-unreadable`/`preserve-unresolved` where v5 answered
   `cross-read-legacy`. The audit's census is family-level too, so **D2 cannot
   cross-check it** — table and audit share the assumption. The battery carries width
   mutants (M18/M19) that are corpus-vacuous, and the selftest must carry a synthetic
   reader-backed-ddwrt FAILED fixture asserting the new row does **not** swallow it.
   R52-C2's own wording ("a family with no validated independent reader") does not
   support a family-level ddwrt key either. **The L1 must decide this before the freeze.**

3. **The census clause fails by exactly the number of new registry rows unless the
   census artifact is derived from the *staged* freeze `SKILL.md`.** Measured at the
   claims base `ab0eafe…`: registry **56** = `census3.json` **56**, `census_outside` `[]`,
   `census3.py --check` exit 0 (receipts R04, R11) — so the round-51 landing already
   closed the 13 → 0 drift, and the round-52 claim's "census_outside 0 both sides" is a
   **no-regression** clause, not a re-derivation. But the r52 freeze adds **7** registry
   rows (`gap-rule.json`, `c1-counter.py`, `c1-controls.py`, `c1-run.sh`,
   `fetch-vendor.py`, `sqfs-triage-v6.py`, `misroot-sweep.sh`), and with
   `tools/round-51/census3.json` unchanged the freeze scores **`census_outside` = 7**.
   Measured remedy: regenerating the census from the **staged** freeze `SKILL.md` yields
   62 paths and `census_outside` = `[]`, exit 0. **Derive it from the staged freeze, not
   the pre-freeze HEAD.** Related: with `tools/round-48/census2.json` as the active
   artifact the drift is now **14**, not 13 (receipt R06) — the 14th is
   `tools/round-51/census3.py`, registered by round 51 itself.

4. **Two of the four round-50 carryover controls change their numbers under v6, each by
   +1, and freezing the old numbers fires the kill rule spuriously.** Measured by scoring
   the committed round-50 control surfaces with the v6 evaluator (receipt R07):
   **do-nothing 19 → 20** and **action-swapped 51 → 52**; **guard-deleted 26 → 26** and
   **junk 126 → 126** hold. The +1 *is* the ddwrt route change itself
   (`dmg_Z3_v3ddwrt_inode_table`). The v5 evaluator reproduces the committed receipts
   exactly (19/26/51/126), so the baseline is confirmed. **Freeze 20 and 52.**
   A second hazard in the same area: the committed `ctl-junk.skill.md` is a **v4-marker
   document with duplicate `clean` labels**, which the frozen v5 parser **refuses**
   (exit 2) — the junk control must be regenerated with unique labels or it is
   unscoreable as a mismatch red.

## Two more measured facts the L1 needs

* **Precedence decides whether a required control has a corpus witness.** The claim
  names "the ddwrt glob broadened back into `legacy-body-failure`" as a required red
  mutant. Under the design where the legacy row's cell **drops** ddwrt and the new row
  sits **below** it, that mutant flips **both** detectors (1/1). Under the alternative
  (legacy cell keeps ddwrt, new row above), it is a **complete no-op** (0/0) — the guard
  around it is dead. **Freeze the first design.** Its price, measured: deleting the new
  row flips D1 (1) but **not** D2 (0) — the audit does not witness that mutant, so the
  claim must not say the audit covers it.
* **Two everywhere-no-op mutants must be excluded with their reasons stated** (the
  equal-action swap, and a `squashfs_v3*` widening), and **five mutants are
  corpus-vacuous** (fixture-only witnesses): the new row deleted, its failing-handler
  cell widened, its gap-kind `+` suffix, the `no-reader-failure` row deleted, and the
  two width widenings. **A corpus-only selftest would score all five GREEN.** v5's
  `corpus_control` already reports a `vacuous` flag per scope — the v6 selftest must keep
  both scopes and extend the roll-up to D2.

  Measured classification over 21 mutants, design A
  (`.ufo/waves/round-52/w1/MutTriV6/mutant-classification.json`): **11 RED-CORPUS,
  4 CORPUS-VACUOUS, 4 NO-OP, 2 PARSE-REFUSED**; with the 12th fixture
  (`v3ddwrt-multigap`) added, the gap-kind mutant moves from NO-OP to CORPUS-VACUOUS →
  **11 / 5 / 3 / 2**. The three no-ops are each expected by construction: the new row
  moved above the legacy row (immaterial once the legacy cell drops ddwrt — the *cell
  content* is load-bearing, not the order), the equal-action swap, and the `squashfs_v3*`
  widening (never consulted — the legacy row above claims the v3 FAILED bodies).

## Not run (honest limits)

* **No v6 instrument exists yet**, so the three **code-level** guards (audit deleted,
  census deleted, the audit's own census flipped) are **specified, not executed**. The
  r51 draft at `.ufo/waves/round-51/w1/ExecTriV6/sqfs-triage-v6.py` is **not** a v6
  implementation: it still reads the **v5** marker and carries no `legacy-body-unreadable`
  row, no audit and no census clause. Every other expectation is measured against a
  **probe** that ports the frozen v5 parser/evaluator and layers the v6 row + evaluator +
  audit on top; the port must reproduce these numbers with its own code.
* No REA, no data run, no download, no network, no `npx rea-agents`.
* No lane file modified; no git mutation in the lane or the fleet repo. The fleet repo
  shows `M .scratch/goal-20261029-hyaku-run12.md` and `M .ufo/l0-questions.md`, and the
  lane shows `M .ufo/waves/round-50/w3/ScribeEntryC1.md` — **all three predate this
  seat's session** (mtimes 05:56, 08:00, 07:53 vs 11:03 at the check) and are other
  seats'/operator's work. This seat wrote **only** under
  `.ufo/waves/round-52/w1/MutTriV6/` and its scratch (receipts R14, R15).
* Not run: C1's instruments (`gap-rule.json`, counter v2, controls, fetcher) — out of
  this seat's scope.

## Tools

None installed, none upgraded — the whole battery ran on the lane's own frozen v5
instrument (`sha256 f29eb92073dfff0c…`) plus the stdlib. No `uv tool`, no `npx`, no
`~/.local/bin` write.
