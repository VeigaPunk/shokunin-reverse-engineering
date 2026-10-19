# SC-3 seat report — arc3-loop1-round2, chain c2, role scribe

Seat SC-3 | chain c2 | role scribe | 2026-10-19 | repo HEAD `14b1682`
(round-1 records commit; no git mutations by this seat). Incidentally SC-3
filed the round-1 c1 records drafts; this round SC-3 is chain c2.

Task as dispatched: records drafts for the parent (not applied) — LOG entry +
SCORECARD round section for C2, pin-free discipline (no bare version pins, no
pin form, no absolute `path:line`), under `claims/c2/records-drafts/`, two
files.

**Deliverables (both written, not applied)**

- `claims/c2/records-drafts/LOG-entry-draft.md` (12,837 B)
- `claims/c2/records-drafts/SCORECARD-section-draft.md` (10,286 B)
- evidence receipts: `claims/c2/records-drafts/evidence/` (20 files +
  `evidence-manifest.sha256.txt`)

## 1. Work performed (evidence pointers)

Read: frozen claims (`claims-frozen.md`); round-1 tree — H1 patch text
(`arc3-loop1-round1/claims/c3/RV-11/proposed-missing-file-guard.patch.md`), H3
patch text (`…/c3/CR-5/proposed-g2-positive-floor.patch.md`), the c3 verdict's
latent-hole ledger, CN-1's consistency sweep §3b (the pin-injection rule),
SCORECARD measurement recipes + section conventions, LOG entry conventions.

Independently measured, all on scratch copies (the real files were read/hashed
only; scratch under `/dev/shm/sc3` and `/var/tmp`; `/tmp` never used):

- **Before (v10 `6f1d19ff…`, 490 lines, HEAD `14b1682`)**: HEAD run PASS
  `0/0/0/0` exit 0 (`evidence/before-head-baseline.out/.json`); H1a SKILL.md
  absent → silent PASS exit 0, `SKILL.md lines=0 loci=0`
  (`before-h1-skill-absent.out`); H1b SCORECARD.md absent → FAIL exit 1,
  marker-uncheckable (`before-h1-score-absent.out`); H3 all-needles-neutered
  (round-1 CR-5 fixture, sha `24e95a47…`) → all-zero loci, `G2 … ok`, PASS
  exit 0 (`before-h3-blind.out`). Shared instruments at HEAD: probe selftest
  13/13 + `reported findings=0` (`probe-selftest.out`, `probe-head.out`);
  command A 82/82, missing [], dangling [], 13/13, 10.0/10.0
  (`commandA-head.json`); custody 5-path read-only capture 12:02:52Z matching
  VZ-4's independent pre-capture (`custody-sc3-capture.txt`).
- **After (landed gate file)**: the census file moved five times during the
  wave (`82fb807e` → `c95a5cf3` → `df9ffdf9` → `a4c16763` → `d0772ce8`). SC-3
  re-ran the full matrix and the creep audit on the revision measured at close:
  `d0772ce8…`, 610 lines — receipts `evidence/after-*`,
  `evidence/rv6-creep-audit-sc3.out`, `evidence/landed-sha.txt`.
- Poller: `/var/tmp/sc3-poll.log` (60 s cadence) + curated digest in
  `evidence/poll-log.txt`.
- Pin-free self-check: `evidence/pin-free-check.out` — the census's own
  `PIN` / `VER` / `PTR` regexes plus a generic absolute `path:line` probe and
  an any-pin-form probe, run over both draft files → 0 matches, CLEAN. The
  check caught one literal pin-form mention in v1 of the LOG draft (header
  sentence, not pasteable text); it was rewritten and the check re-run.
- Seat reports folded (C2 chain): CR-2, CR-3, EX-11/12/13/14/18/19/20/23/24/25,
  PL-2, RV-3/4/5/6/7/8, SC-2. Their measured facts used: EX-23's
  intermediate-revision regression note, EX-19's neuter matrix + label note,
  EX-14's floor-unit analysis, RV-4's mutation test, RV-6's audit at the final
  revision, EX-25's probe-interplay re-run.

## 2. Proposed changes

The two draft files above are the deliverable (patch-text style: the parent
applies them at the records commit; each carries `[[FILL]]` slots for
parent-only values — dispatch delivery count, custody pre/post pair, C1/C3
bullets, commit shas). No other proposed changes. No real-target writes: the
census gate file was never written by this seat; all runs were on scratch
copies. No `LOG.md` / `SCORECARD.md` / `SHONEN.md` / corpus / SKILL edits; no git
mutations; custody paths untouched (hash/stat reads only).

## 3. Before → after measurement for the C2 claim

Command shape (all runs: `python3 <census-copy> --root <scratch-root>
[--quiet|--json]`; roots built from byte copies of the three scoped files):

| Leg | Before (v10 `6f1d19ff`, HEAD `14b1682`) | After (landed `d0772ce8`, 610 lines) |
|---|---|---|
| ordinary run | `VERDICT: PASS …`, exit 0 | `VERDICT: PASS …`, exit 0; counts unchanged (162/6, 1417/9, 371/2); `DECLARED FAIL CLASSES: []`; `G2 … ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)` |
| SKILL.md absent | silent `PASS` exit 0, `lines=0 loci=0` | `UNREADABLE (could-not-evaluate): ['SKILL.md: FileNotFoundError']` + `DECLARED FAIL CLASSES: ['UNREADABLE']` + `VERDICT: FAIL`, exit 1 |
| SKILL.md EACCES | (same silent class measured by EX-17) | `['SKILL.md: PermissionError']`, FAIL exit 1 |
| all needles neutered | all loci 0, `G2 … ok`, PASS exit 0 | `G2 … SUSPECT (per file 0/0/0)`, `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']`, FAIL exit 1 |
| full-length needle-stripped SKILL.md (SC-3's attack) | silent PASS (not previously measured) | `['BLIND-INSTRUMENT']`, FAIL exit 1 (closes the per-file collapse; the global-floor variant alone swallowed it — EX-14's variant B adopted) |
| creep audit before→after (RV-6's independent AST tool run by SC-3) | — | rows 20 → 20, keyset identical, canonical row digest `dbfe1c728fa44e54` both sides, `CREEP FLAGS (0)`, exit 0 |
| probe / command A (shared instruments) | 13/13 + findings=0; 82/82 13/13 | unchanged at HEAD (sibling seats re-measured post-landing: EX-25 13/13 + findings=0 both modes) |

Calibration: the after-leg ordinary run is PASS because the claim's
"ordinary runs stay PASS" clause must hold; a real intermediate revision
(`076bd621`/`c95a5cf3`, per-file *block* floor) failed it (SKILL.md has 0
current-ok blocks), was caught by EX-23/RV-8 and replaced by the det-level
floor. Verdicts above are the measured landed state; the drafts instruct the
parent to re-measure if the sha has moved (it moved five times during the
wave; `d0772ce8` was current at SC-3's close).

## 4. Attacks / refutations attempted (with verdicts)

- **A1 H1 absent-file** — before: silent PASS reproduced; after: declared
  `UNREADABLE` FAIL. Verdict: hole closed on the measured revision.
- **A2 H3 total blindness** — before: blind PASS reproduced (round-1 fixture
  byte-identical to the one CR-5 used); after: declared `BLIND-INSTRUMENT`
  FAIL. Verdict: closed.
- **A3 per-file collapse at full length** (SC-3's own attack, first measured
  against the interim global-floor revision) — PASS there; FAIL on the final
  revision. Verdict: closed by the det-level per-file floor; my first draft
  text named it wrongly as a residual and was corrected before close.
- **A4 partial-needle blindness** (PIN alone / VER+PTR etc.) — still PASS
  (EX-14 §5, EX-19 A2–A4; the landed header itself names it). Verdict:
  survives; named residual; outside the frozen claim's letter ("zero loci in
  a non-empty scope").
- **A5 G2 label over-claim** — the per-file counts printed as "current-ok
  loci per file" are disposition counts (JSON `current_ok_per_file`) while
  "total loci=17" counts blocks (EX-19 §3; SC-3 concurs from the line).
  Verdict: real, cosmetic; named in the drafts' notes for the reviewer seats.
- **A6 pointer shadowing** (EX-19 side finding: a block carrying a version
  never evaluates its pointer) — reproduced by reading the classify branch;
  block reads INFO, not flagged. Verdict: named debt, not a claim defect.
- **A7 pin-free self-attack** — ran the census's own needles + an absolute
  `path:line` probe + an any-pin-form probe over both drafts; v1 had one
  literal pin-form mention, removed; final files CLEAN (0 matches in all five
  families). Verdict: discipline met, receipt attached.
- **A8 intermediate-revision claim-breaking regression** (block-level floor:
  ordinary HEAD run FAIL) — folded from EX-23 §6 and independently visible in
  the revision chain; the landed revision restores PASS at my own hand
  (`after-t0-present.out`, `after-q0-quiet.out`). Verdict: closed in-wave; the
  drafts pin the measured revision and require a re-check.

## 5. Blockers / gaps

- **Gate-file churn**: the census file was still moving at close
  (`d0772ce8…` measured, 12:18Z). My after-leg is stamped to that revision;
  the drafts carry an explicit parent step — `sha256sum
  .ufo/gates/c1-census-v10.py`, and if it differs, re-run the matrix
  (`claims/c2/RV-6/tools/scope-creep-audit.py` + scratch-root battery, receipt
  shapes in `evidence/after-*`) before pasting. An unrun check has not passed.
- **EX-16's seat report** was not on disk at close (its `receipts/` were the
  source for the landing); some C2 seats' reports (EX-15, EX-17, EX-21, EX-26,
  RV-9/10, VZ-2) were also not landed at my last poll — the drafts cite their
  landed receipts/tools, not their prose.
- **C1/C3 bullets remain shape-only `[[FILL]]`s** by design; custody post-pair
  and the records-commit readings are parent-side.
- Named residuals recorded, not repaired by this seat (not the scribe's
  target): H2, H4, H5/H6, partial-needle blindness, the G2 label over-claim,
  pointer shadowing.
- No blockers to the deliverable itself; both files are complete in draft form
  and pin-free-checked.

Scope discipline: wrote only `seats/SC-3.md` and
`claims/c2/records-drafts/**`; scratch under `/dev/shm` and `/var/tmp` (never
`/tmp`); no git mutations; custody paths read-only; no installs.
