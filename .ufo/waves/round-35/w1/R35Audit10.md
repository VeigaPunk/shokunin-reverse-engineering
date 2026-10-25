# R35Audit10 — calibration axis fit challenge (advisory, read-only)

Role: leaf audit seat. Item: **Challenge calibration axis fit**; milestone
"Build evidence and first falsifications". No lane writes were made; nothing
was executed beyond read-only git reads. Counters were **not** run (following
the round-34 verifier precedent, PROTOCOL §Gate standard: verify committed
evidence, never execute a sibling's gate) — all verdicts below derive from
immutable git objects, the committed control receipts, and static analysis of
the frozen counter source.

## Evidence base

| Check | Evidence | Result |
|---|---|---|
| Instrument pins match the tree | `sha256sum` of both counters + plan at `3ecf4298` vs `claims-canonical.json` instruments map | C1 `e28792c7…`, C2 `576c14dd…`, plan `45b644a4…` — all match |
| Canonical freeze used by controls | `controls/c1-do-nothing.json` / `controls/c2-do-nothing.json`: `freeze=2323d197`, `revision=aa04633a` (base) | red receipts committed before data (commit `3ecf4298`), exit 1 each |
| Census content | `.ufo/waves/round-35/assimilation/census-start.txt` | `rows=106`, `EXIT=0`, exactly 9 `W04` lines; base `corpus/SOURCES.md` has exactly 106 S-rows — content is truthful |
| Census ordering | `git log` — census committed at `d2729cba` (16:05:46 −03:00); **no** `corpus/SOURCES.md` change exists in `aa04633a..HEAD` | ordering will hold if the first SOURCES edit lands after `d2729cba`; D-1 currently fails only as `D1_no_sources_change_after_base` (control state) |
| D-2 state | `corpus/lessons/round-35.md` absent; `w1-settle.json` present, `w2-settle.json` absent | both must be created by the wave |
| D-3 state | r34b entry header `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` has `sources:`/`author:`/`status:`/`revisions:` but no `source:`/`verified-at:`/`recheck:` lines | trio genuinely missing; the existing `sources: S106` line does **not** match the counter's `^source\s*:` regex |
| D-4 state | `SKILL.md` is byte-identical at base and HEAD (same sha256 `d8d4783e…`) | see F1/F2 below |
| Process | `corpus/claim-freezes.tsv` round-35 row present, `FLAGGED INSTRUMENT_ABSENT,INSTRUMENT_REVISED`; `freeze-status.md` documents the failed freeze-gate run | honest disclosure; setup-order defect, not a claim measure |

## Findings (first falsifications)

**F1 — D-4 exact-heading mismatch (will block a clean score with the current
heading).** The counter looks for the exact section string `### Round-34
run-6 instrument registry` (`EIGHT_CELL_SECTIONS`, exact equality `l.rstrip()
== sec`). The real heading in `SKILL.md` is `### Round-34 run-6 instrument
registry — the shortcut-replay gate (stopped capability)` (line 1209). Exact
match fails ⇒ `D4_section_missing` persists even after every run-6 row is
reformatted. The wave must rename the heading (drop the suffix) or D-4 can
never pass. Note the run-6 table itself is currently the five-column shape
(`tool | purpose | command | exit codes | selftest`, lines 1213–1219) the
defect flags — it must become 8 cells.

**F2 — D-4 scan over-covers non-registry tables (will keep failing after the
registry rows are correct).** The section scan counts **every** `|`-line from
`### Round-32 instrument registry` (line 1066) until the next `##`/`###` line
(`## Round-33 instrument status…`, line 1086). Within that span, the archived
**residual-witness registry** (a 4-column table, lines 1081–1084) is counted
as registry rows: committed control receipt already shows
`D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4`. The
Round-32 instrument registry itself is already fully 8-cell compliant at base
and HEAD. Fix options (all structural, none implied by the literal D-4
defect): give the residual table its own `### Residual witness registry`
heading (so the scan stops), or convert the archived 4-column table to 8
columns (changes historical evidence presentation). Without one of these,
D-4 stays red no matter what happens to the registry rows.

**F3 — D-1 ordering is commit-boundary coarse.** If a census were committed in
the *same* commit as the first `corpus/SOURCES.md` change, `commit_time(…) ==
first_change_time(…)` ⇒ check passes, although the fix intent is "capture the
start census **before** the first registry edit". Currently moot (census was
pre-committed at `d2729cba`), but the frozen check cannot detect same-commit
bundling.

**F4 — D-1 warning count is not enforced.** Predicate says "9 W04 warnings";
the counter only requires the substring `W04`. A receipt with 1 W04 line would
pass. (Today's committed census genuinely has 9.)

**F5 — D-3 "appended" is not enforced.** The counter checks trio presence
anywhere in the file, not append position, and does not require the receipt
paths named in the routed fix. A rewritten entry with the trio inserted at the
top would pass D-3; the spotcheck fix explicitly says "do not rewrite the
entry".

**F6 — D-2 checks are substring-loose.** `AAdjacencyCite` and `31/32` need
only appear anywhere in the lesson; the correction sentence shape and the
"unreported, not settled" wording are not asserted. Settle receipts are
checked for presence/int fields only — totals are cross-checked against the
lesson's seat line, which is the one substantive consistency anchor.

## Calibration axis fit

The C2 claim fits the SCORECARD calibration proxy's disclosed definition —
"failure-selected completeness" /  obligations aligned, not unbiased
accuracy — as a *record-reconciliation* claim: closing the four verifier-routed
record defects is the same family as the round-1 nine obligations. Caveats
for the score step: (a) the counter verifies internal record presence and
consistency only — nothing cross-checks against an outside truth (real seat
reports on disk, actual census run); (b) the claim is binary, not ratio
scored; (c) F1/F2 mean a "clean" D-4 requires SKILL.md restructuring beyond
the literal defect, so a red C2 at the measured revision may reflect
instrument shape rather than non-closure. None of this changes the frozen
predicate or kill rule — it only says what a C2 verdict can and cannot mean.

## Limits

- Counters not executed (gate standard); verdicts are static/committed-evidence.
- No files written except this report; no VCS mutation; no `/fast/scratch`
  access; no delegation (no labrat spawned — nothing to run).
- `corpus/considerthese/` does not exist (plan's one-line expectation holds).
- Two unreachable commits (`35fc7bd1`, `eceb6d9e`) contain earlier copies of
  the controls/canonical files; not reachable from `main`, not scored.
