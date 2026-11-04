# ScoutRouted — round-78 wave 1 — the round-77 routed-defect closure map

Seat: ScoutRouted. Read-only. Lane writes: this directory only.
Instruments run at base `6205ec8c575fb070243c0c40e34a2b0daacde46a` (the frozen base):
`tools/round-78/attack-gate.py` (selftest 21 cases, 0 failures; sha256 `780089e3…d173`) and
`tools/round-78/surface-recheck.py` (selftest 12 cases, 0 failures; sha256 `e7ea1717…1a13`).
Both instruments in this lane are at committed revisions; no lane file was edited.

## 0. Sources enumerated

- `.ufo/waves/round-77/w1/CriticClaims.md` (§1–§5; its own findings C1-1…C1-3, C2-1…C2-3).
- `corpus/lessons/round-77-verifier-spotcheck.md` §6 (items 1–7) and §8 (items 8–12), read in full.
- `plans/round-78-claims.md:20-30` (the disposition sentence) and `:60-66` (the C1 predicate's
  red-case list).
- Measured: `python3 -B tools/round-78/attack-gate.py --root . --rev 6205ec8c… --work <scratch>
  --battery` → `fixtures_total 10, base_accepted 10, refused 10`, `genuine.mismatch_count 0`,
  `validate defects []`, exit 1 (the four genuine record defects are the still-missing filing and
  gate receipts); `tools/round-78/surface-recheck.py --battery` → `checks_total 8, matched 6,
  mismatches 2` (`jdk-version`, `omp-rea-disable`), exit 1. Receipts: `c1-battery-base.json`,
  `c2-battery-base.json`.

## 1. Closure map — all 12 routed items

`closed_by` is the artifact that closes the item; `pointer` is the file and line.

| id | claim (one line) | closed_by | pointer |
|---|---|---|---|
| §6-1 | Wave accounting overstates returned evidence ("10 seats returned evidence") | record-only (unclaimed) | `LOG.md:4601`; numbers §3 below |
| §6-2 | Landed-changes table misattributes the C2 controls to `1d84253a` | record-only (unclaimed) | `git diff-tree --name-only -r 1d84253a` (6 paths, no `c2-*`) vs `37f5d069` (`pre/controls/c2-forged-arms.json`, `c2-gate-alone.json`) |
| §6-3 | Two round-77 mistakes are prose, not `## Mistakes` rows | record-only (unclaimed) | `plans/round-78-claims.md:135-137` promises `corpus/lessons/round-78.md`; file absent at base |
| §6-4 | The C2 revision-binding receipts do not retain `exit` | record-only (unclaimed); no instrument covers them | `attack-gate.py:592-594` globs only `gate-*.json`; `prefile-rev-binding-{at-filing,stale}.json` keys are `["defects","validate"]` only |
| §6-5 | The forged-arms control does not retain its defects | record-only (unclaimed) | `.ufo/waves/round-77/pre/controls/c2-forged-arms.json` keys have no `defects`; round-78 controls are `c1-{base-only,all-refuse,no-fixtures}`, `c2-token-grep` |
| §6-6 | `Stale-lane` line lacks the required statement (progressing vs silent) | record-only (unclaimed) | no round-78 artifact |
| §6-7a | Survivor `c1-rev-show-to-worktree` (no `show()` selftest case) | R78-C1 **partial**: every base arm reads a fixture repo through `git show` at a non-HEAD rev | `attack-gate.py:173-236` (`materialise`), `:224-246` (`run_base`); no selftest case for it |
| §6-7b | Survivor `c2-nonint-exit-accepted` (string/bool `exit`) | R78-C1: `check_receipt_like` refuses any non-int and any bool | `attack-gate.py:537-539`; selftest `red-receipt-no-exit` `:818`, `red-receipt-bool-exit` `:822` |
| §6-7c | Near-miss cells `(D24: true)`, `(mismatch 0)` | R78-C1: `qualified_atom`, `near_miss_field` | `attack-gate.py:72-73` (fixture `a2-repunctuated`), `:74-75` (`a3-near-miss`); selftest `:789`, `:793` |
| §6-7d | Nested-field unbound clauses `forged_detected true` / `sole true` | R78-C1: `value_mismatch`, `unbound_verdict` | `attack-gate.py:78-79` (`a5-nested-field`), `:80-81` (`a6-dropped-defect`); selftest `red-ambiguous` `:801`, `red-absent-field` `:805`, look-alike `green-nested-unique` `:775` |
| §8-8 | A1 accepts a failing gate run | R78-C1: `clean_run` + `b1-fail-run` (battery red only; no selftest case) | `attack-gate.py:82-83`, judge `:566-577`; base arm observed `rc 1, prefile: FAIL` **met True**, then refused |
| §8-9 | A2 does not enforce the filing revision | R78-C1: `filing_rev` + `b2-stale-filing`; selftest covers `expect_rev` only | `attack-gate.py:84-86`, judge `:578-591`, selftest `red-receipt-stale-rev` `:825` |
| §8-10 | No receipt authentication in C1 | R78-C1: `receipt_auth` + `a1-forged-receipt`, applied to the genuine record too | `attack-gate.py:70-71`, `auth_findings` `:492-510`, genuine rule set `:683-684`, selftest `:830`, `:833` |
| §8-11 | Selftest reds for the kill-rule cautions | R78-C1 **partial**: negated and re-punctuated reds exist; "clause outside the group" and the authenticated-foreign-receipt variant are open (§2) | `:797` (negated), `:789` (qualified); predicate narrowed at `plans/round-78-claims.md:60-66`, but no SCORECARD round-78 row exists |
| §8-12 | Settle the wave before filing | process duty, discharged for round 77 | base `6205ec8c` commits 17 inherited `CriticClaims` files (`git show --stat 6205ec8c`) |

## 2. What is not closed, and why

**Record-only, carried unclaimed (6):** §6-1 … §6-6. They are prose/report repairs that land in
the round-78 report and `corpus/lessons/round-78.md`; no instrument can close them, and at base
none is repaired. Specifically still open in the tree:

- §6-4: `.ufo/waves/round-77/l1/scores/prefile-rev-binding-at-filing.json` and `-stale.json` still
  carry only `validate` + `defects`; `exit` is absent (`python3 -c` keys above). The new
  `gate_receipt_schema` rule does **not** reach them — it globs `.*/gate-[^/]*\.json`
  (`attack-gate.py:592-594`).
- §6-5: `c2-forged-arms.json` has `exit 1`, `ok false`, `arms`, `validate` — no `defects` key, so
  the "two validator defects" the round-77 report cites are still not retained.
- §6-3: `corpus/lessons/round-78.md` does not exist at base (the promises are at
  `plans/round-78-claims.md:135`), so the two prose mistakes have no row yet.

**Open instrument shapes (2), demonstrated with the gate's own machinery** (`probe-open-shapes.json`;
probe builds fixture trees under scratch and calls `materialise` + `scan_record` +
`FIXTURE_RULES`, so the reading is the instrument's, not a re-implementation):

- `p1-foreign-authentic-receipt` — a cell names a receipt that is genuine and self-pinned
  (`rev` 40-hex, `instrument.sha256` re-derives) but records *another cell's* verdict:
  `in_scope_cells 1, groups 1, bound_clauses 2, mismatch_count 0, findings []`, all five rules
  refuse nothing (`receipt_auth false`). `receipt_auth` proves authenticity, not ownership: no
  rule checks that the receipt path is the cell's own or that its `rev` is the measured one. This
  is the §8-11 "path from another cell" caution, closed only for the hand-authored variant (a1).
- `p2-clause-outside-group` — the verdict clauses written outside the parentheses:
  `in_scope_cells 1, groups 0, bound_clauses 0, mismatch_count 0, findings []`. `scan_record`
  iterates `GROUP_RE` only (`attack-gate.py:449-452`), so a clause outside a group is invisible.
  The C1 predicate's red list (`plans/round-78-claims.md:60-66`) does not name this shape, so the
  narrowing half of §8-11 is also incomplete — and the SCORECARD carries no round-78 row yet to
  carry it.

**Partial selftest arms:** §8-8 and §8-9 are closed at battery level but have no selftest case
exercising `clean_run` / `filing_rev` judges; §6-7a has no `git show`-on-fixture selftest case even
though every base arm exercises that path.

**Calibration caveat for R78-C1 at base.** The genuine record scan is *vacuous at base*:
`genuine.record = {in_scope_cells 0, groups 0, bound_clauses 0}` because `SCOPE_MIN_ROUND = 78`
(`attack-gate.py:47,414-427`) and no round-78 capability row exists yet. So `genuine.mismatch_count 0`
at base says nothing about the record, and `receipt_auth` never runs on a real cell until the L1
lands the round-78 rows. The four `genuine.defects` at base are the pre-filing state (no filing
receipt, no gate receipt); the predicate's "`genuine.defects []`" is only meaningful once those
land. A reader must not take the base exit-1 arm as evidence either way about the record.

**R78-C2 closes none of the 12.** `surface-recheck.py`'s eight checks
(`:205,209,215,219,223,227` — `{devin,omp,kimi}-rea-pin`, `omp-rea-disable`, `ghidra-version`,
`ghidra-dir`, `jdk-version`, `java-home`) name no routed item; its contribution is the measured
drift (`mismatches 2`) and the surface instrument, not routed closure.

## 3. Wave accounting — measured, not quoted

Command: `python3 -c` over `.ufo/waves/round-77/r77-w1-results.json`.

| quantity | value |
|---|---|
| `seats` field / `results` length | 12 / 12 |
| seats with non-empty `output` | **10** (`ScoutSurfaces, ConnectorCross, ExecC1Grammar, ExecControls, ReviewerC2, CriticClaims, MutationTester, SentinelScope, ScribeSources, RevengerRecord`) |
| seats with zero-byte `output` | **2** (`ExecC2Receipt`, `ReviewerC1`) |
| non-empty but progress-only (<1 KB, no report) | **2** (`CriticClaims` 766 B, `SentinelScope` 372 B) |
| substantive `*.md` reports at filing | **8** (all of the above minus those two) |
| substantive `*.md` reports now | **9** (base `6205ec8c` committed `CriticClaims.md`, 11 584 B) |
| seat dirs under `w1/` | **9**; `CriticClaims/` was empty at filing, carries 16 files after the base commit; `SentinelScope` has no dir |

Report sentence (`LOG.md:4601`): "10 seats returned evidence (all files under
`.ufo/waves/round-77/w1/`), 2 died with zero-byte output". The 10 matches the non-empty count, but
"returned evidence" is true for 8 of those 10: two returned progress notes only. The "2 died"
half is exact. The sentence is therefore numerically right on seats and output bytes and wrong on
the category — the §6-1 finding stands, and the corrected form is "8 substantive reports, 2
progress-only seats, 2 zero-byte dead seats" at filing (9 substantive after the base commit).

## 4. Verdict

- R78-C1's ten rules cover §8-8, §8-9, §8-10, §6-7b, §6-7c, §6-7d fully, §6-7a and §8-11
  partially; measured `base_accepted 10 of 10`, `refused 10 of 10`, every refusal by the declared
  rule (per-fixture reasons in `c1-battery-base.json`).
- Six routed items are record-only and still unlanded at base; two instrument shapes
  (foreign-authentic receipt, clause outside the group) remain open and are demonstrated above.
- R78-C2 is orthogonal to the routed queue: measured `mismatches 2` for exactly the two named
  values, `jdk-version` record `21.0.12.1` vs live `21.0.13`, `omp-rea-disable` record claim
  `False` vs live `True`.

Confidence: high on every file:line and on the measured counters (both receipts reproduce and
validate defect-free); the two open shapes are reproduced by the gate's own functions, so they are
observations of the instrument, not inference.
