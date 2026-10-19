# Seat RV-6 — chain c2, reviewer — independent re-run of EX-21's creep audit

Wave `arc3-loop1-round2`, 2026-10-19 | repo HEAD `14b1682` | baseline instrument
(EX-28's committed v10) sha256
`6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b`, 490 lines,
SCOPE rows **20**. Audited landed revision (EX-16's declared "r9 final")
sha256 `df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43`,
601 lines, SCOPE rows **20**.

Task: independently re-run EX-21's creep audit and verify 0 flags; verify the
SCOPE row count unchanged (20 rows). **Verdict: confirmed — 0 creep flags under
four instruments/parses at every revision audited; SCOPE rows 20 → 20, row
table byte-identical (canonical hash `dbfe1c72 8fa44e54…` both sides).** The
last two sentences are measured, not inherited: every number below was produced
by this seat (all commands in `claims/c2/RV-6/logs/`).

## 1. Work performed (evidence pointers)

- Read the frozen claims `claims-frozen.md` (C2 at :34-50; seat rules :66-82)
  and EX-16's landed instrument end-to-end.
- **Baseline sealed before EX-16's edit**: `git show HEAD:…` → blob
  `6f1d19ff…` == working-tree copy at my seat start; 20 rows; ordered canonical
  sha256 `dbfe1c728fa44e5410811f5bfb73a54430e8f4d47fd7db906604a53f8d46da6c`,
  sorted `48b3f220…`; row-line count by raw grep = 20. Copies:
  `claims/c2/RV-6/before/c1-census-v10.py`.
- **Built three-auditor rig** (all receipts under `claims/c2/RV-6/logs/`):
  1. `tools/scope-creep-audit.py` (sha `76aa8507…`) — my own auditor: SCOPE
     extracted via module AST (`ast.literal_eval`), not a line regex; flag set
     restricted to reachable rules (open-ended, EOF-bound, wide added DATED,
     widen-by-add/remove, coverage loss, both class flips).
  2. `tools/creep-fixture-suite.py` (sha `4e48d048…`) — 12-fixture non-vacuity
     suite (`logs/fixture-suite.txt`: **passed=12 failed=0**).
  3. CR-5's round-1 differ, run verbatim (sha
     `e0d2384c1220c4e8e7faf1f98b74118489ab4985e56a10df77c9f40af5438504`, byte-
     identical to the round-1 original) and EX-21's `scope-audit.py` (sha
     `f915cec2e6c2ab462d2655407aba649233bc98a1e66122b71b01a7d777707acc` at
     audit time; compare + invariance modes) plus EX-21's `run-audit.sh`
     end-to-end (`logs/ex21-runner/` at runner sha `0264f419…`;
     `logs/ex21-runner-final/` at runner sha `cbdc59a2…`).
- **Revision trail** (`logs/revision-audit-trail.txt`): the gate file moved
  ≥9 times during this seat — `7b5a0e88` → `1431620f` → `59975ae0` →
  `82fb807e` → `762bfebe` → `3aa7ce91` → `076bd621` → `c95a5cf3` →
  `df9ffdf9` (stable across 2×20 s samples at 12:12). Every sampling that ran
  the audit (1431620f, 82fb807e, 762bfebe, c95a5cf3, df9ffdf9) read 20/20 rows,
  identical canonical hash, 0 flags. Frozen snapshot kept:
  `claims/c2/RV-6/after/c1-census-v10-after.py` (= `df9ffdf9…`).
- Row table consistency at both ends (`logs/row-table-consistency.txt`):
  20 rows, per-file PROVINCE 7 / SKILL 2 / SCORECARD 11, no duplicate
  `(file,start,end)` keys, no row past its file's EOF, every DATED marker_line
  inside its own row, no marker on a CURRENT row — identical before/after.
- Read for context: round-1 `claims/c3/CR-5/tools/scope-diff.py` + H1/H3 patch
  texts (`RV-11`, `CR-5`), EX-16's receipts (`receipts/before|after/`),
  RV-8's seat report.

## 2. Proposed changes

- `claims/c2/RV-6/proposed-creep-rule-fixes.patch.md` — patch TEXT (not
  applied) for three measured instrument defects: (a) coverage-loss blindness
  in CR-5's `scope-diff.py`, (b) its two dead widen branches, (c) EX-21's
  `scope-audit.py` EOF rule parameterized against the census script's own line
  count, plus EX-21's `run-audit.sh` mis-pathed CR-5 leg.
- Own artifacts only: `claims/c2/RV-6/{tools,logs,before,after}/`. This seat
  wrote nothing outside its claim dir and this report (scratch `/var/tmp/rv6-round2`).

## 3. Before → after measurement (the C2 claim's creep clause)

Baseline `6f1d19ff…` (490 lines) → landed `df9ffdf9…` (601 lines),
`logs/close-audit-final.txt`:

```
$ python3 claims/c2/RV-6/tools/scope-creep-audit.py before/c1-census-v10.py .ufo/gates/c1-census-v10.py --root . --expect-rows 20
SCOPE-ROWS before=20 after=20 expected=20 rows_unchanged=YES
CANON before_ordered_sha256=dbfe1c728fa44e54 after_ordered_sha256=dbfe1c728fa44e54
KEYSET identical=YES added_keys=0 removed_keys=0 changed_rows=0
CREEP FLAGS (0): []            AUDIT: clean            exit 0

$ python3 claims/c3/CR-5/tools/scope-diff.py before/c1-census-v10.py .ufo/gates/c1-census-v10.py
rows before=20 after=20 | ADDED (0) | REMOVED (0) | CHANGED (0) | CREEP FLAGS: []   exit 0

$ python3 claims/c2/EX-21/scope-audit.py compare before/c1-census-v10.py .ufo/gates/c1-census-v10.py
scope-literal-sha256  000b74e28bf1017ab24a93d9958f3e8e56cae75d19d9bcec5cce4cc79a1339e2
                      (identical before and after)
rows before=20 after=20 | ADDED (0) | REMOVED (0) | CHANGED (0) | CREEP FLAGS: []   exit 0
DETECTOR CONSTANTS: PIN/VER/PTR/CACHE/REA_GATE/INLINE_MARKER/HOLDING/HOLDING_OK/RECEIPT all [same]

$ python3 claims/c2/EX-21/scope-audit.py invariance before/c1-census-v10.py .ufo/gates/c1-census-v10.py .
INVARIANCE: HOLDS (exit/verdict/counts/live/g2_ok/g11/g7/scope_errors/current_ok_n/historical_n all same) exit 0

$ raw row-line count (grep, parser-independent): 20 (before) / 20 (after)

$ python3 .ufo/gates/c1-census-v10.py        # ordinary run at HEAD, landed revision
UNREADABLE (could-not-evaluate): [] | G2 positive-assertion guard: ok (current-ok loci per file: 17/14/3; floor=1/file)
DECLARED FAIL CLASSES: [] | VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)   exit 0
```

Census JSON comparison before→after (`logs/census-before.json` vs
`logs/census-after.json`, 11 keys): verdict PASS/PASS, loci 6/9/2 and 6/9/2,
current_ok 5/5, historical 5/5, all counters empty — locus counts invariant
across the edit.

EX-16's own receipt declares the same bytes I audited
(`receipts/after/after-sha256.txt`: `df9ffdf9…`, 601 lines, "r9 final,
captured 2026-10-19T12:12:15Z"; `scope-diff.txt`: 0 flags) — my measurement is
an independent reproduction, not a re-citation.

## 4. Attacks / refutations attempted (verdicts)

- **A1 vacuity of my own audit** (round-1 blind-instrument lesson): 12 injected
  signatures — widened DATED end, CURRENT→DATED flip, row added to EOF, widen-
  by-add/remove, DATED start moved earlier, wide added row, row ending exactly
  at SCORECARD's EOF, pure deletion; plus controls (identity, marker-only
  re-key, legitimate +1 renumber r8-precedent, narrow legitimate row). All 12
  behave as declared (`logs/fixture-suite.txt`). Verdict: non-vacuous, no false
  positives on range-neutral re-keys.
- **A2 round-1 differ's widen branches are dead code**: with
  `key=(file,start,end)`, the `changed` loop can never see a bound move.
  Measured F1 (273-326→273-330) and F5 (45-62→44-62): `CHANGED (0)`, flag
  arrives from `widen-by-add/remove`. Verdict: confirmed dead, widening still
  caught; recorded in the patch text.
- **A3 round-1 differ misses coverage loss**: F11 (delete SCORECARD 534-560)
  and F12 (narrow 636-702→636-690) → `CREEP FLAGS: []` (only the non-zero exit
  + REMOVED stanza) — substantive creep for a "0 flags" claim. EX-21's auditor
  and mine both flag `coverage loss`. Verdict: gap confirmed in the round-1
  instrument; closed in mine; patch text filed.
- **A4 EOF-bound blind spot**: added row `SCORECARD.md 1268-1417` (150 lines,
  ends exactly at the file's live EOF) → CR-5 differ `[]`, EX-21 auditor `[]`;
  mine flags `CREEP bound reaches file EOF … (lines=1417)`. Cause: EX-21's rule
  compares `e` against `after["lines"]` — the census script's own line count
  (560/601), not the scoped file's. Verdict: confirmed (`logs/eof-blindspot-probe.txt`);
  no bearing on the landed diff; patch text filed.
- **A5 deletion blind spot in EX-21's runner**: its CR-5 second-opinion leg
  fails on a path error (`$HERE/../cr5-tool/` vs `$HERE/cr5-tool/`) → receipt
  `cr5-scope-diff.out` holds `No such file or directory` + `exit=2`, and the
  runner still exits 0. Reproduced on both runner revisions I ran
  (`0264f419`, `cbdc59a2`). Verdict: their harness leg is vacuous; I re-ran the
  same differ file (sha `e0d2384c…`, byte-identical to round-1's) at my own
  hand → 0 flags, exit 0. Patch text filed.
- **A6 transient mid-edit state**: revision `762bfebe…` (570 lines, sampled
  12:10:13Z) read `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']`,
  `VERDICT: FAIL`, exit 1 at HEAD, and EX-21's invariance read BROKEN (3 diffs:
  exit 0→1, verdict PASS→FAIL, g2_ok True→False) — receipt `logs/r762-qc.txt`.
  Verdict: superseded by the final revision (PASS), but it is the one observed
  state in which the C2 claim's "ordinary runs at HEAD stay PASS 0/0/0/0" clause
  did not hold; recorded with hash + timestamp rather than dropped.
- **A7 audit-vs-self-certification**: the creep verdict here never reads the
  audited instrument's own output — four parsers (my AST parse, EX-21's
  line-regex rows, CR-5's block regex, raw grep count) and three differ
  implementations; the census's own PASS is reported separately in §3. The H4
  self-certification residual named in the frozen C2 claim stays named — an
  external diff audit is not the same as the instrument auditing itself.
- **A8 landing-identity drift** (the round-1 EX-12 lesson): the gate file moved
  ≥9 times during this seat; EX-16's declared hash updated mid-flight
  (`82fb807e` → `df9ffdf9`). Every audit above is pinned to a sha256, never to
  "the working tree". Verdict: managed; the final audited revision equals the
  declaration.

## 5. Blockers / gaps

- **EX-21's seat report had not landed at close** (`seats/` carries no
  `EX-21.md`). My re-run therefore targets their source artifacts, identities
  recorded above; if they revise `scope-audit.py` (sha `f915cec2…` at audit
  time) or `run-audit.sh` after this report, the audit must be re-derived.
- **EX-16's seat report had also not landed**; the landing identity was read
  from `receipts/after/after-sha256.txt` (12:12:15Z).
- The gate file may churn again after my close. Cheap re-check for the parent:
  `sha256sum .ufo/gates/c1-census-v10.py` — if it is not `df9ffdf9…`, re-run
  `claims/c2/RV-6/tools/scope-creep-audit.py <snapshot> .ufo/gates/c1-census-v10.py --root .`
  and require `rows_unchanged=YES`, `after_ordered_sha256=dbfe1c728fa44e54` and
  `CREEP FLAGS (0)`.
- No other blockers; no custody path touched by this seat (read-only), no git
  mutation, no writes outside `claims/c2/RV-6/` and this report.
