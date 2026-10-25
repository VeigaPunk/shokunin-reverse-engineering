# R35Audit08 — C1 README/PROVINCE section-scoping audit (advisory)

Seat: R35Audit08 (leaf, w1). Scope: claim C1's `PROVINCE.md` / `corpus/README.md`
clauses only. Read-only; no lane writes besides this report. Frozen artifacts
examined: `plans/round-35-claims.md`, `.ufo/waves/round-35/claims-canonical.json`,
`tools/round-35/c1-coverage-counter.py` (frozen sha `e28792c7…`), live
`PROVINCE.md`, `corpus/README.md`.

## What the frozen instrument actually enforces (`c1-coverage-counter.py` `check()`)

- `province` (lines 132–136): whole-file substring scan of root `PROVINCE.md`
  for each dated stem `2026-10-25-r35-jsc2js-mapper-contract`,
  `2026-10-25-r35-jsc2js-release-inventory` (filename minus `.md`).
- `readme` (lines 137–140): whole-file substring scan of `corpus/README.md`
  for each **full filename including the `.md` suffix**.
- No heading check (no `## Round-35 additions to Core`, no `## Coverage map`),
  no table-row check, no link to the `.jsc` Frontier bullet, no section scope.

## Findings

1. **Scoping gap (under-constraint / false-pass risk)** — the predicate and plan
   require placement in the *Round-35 Core-addition table* (`PROVINCE.md`) and the
   *coverage map* (`corpus/README.md`); the counter only requires the strings
   anywhere in each file. A mention in the Frontier bullet, a footer, or the
   README `## Knowledge` table would score `province`/`readme` green. The "land on
   the `.jsc -> source mapping` frontier" clause has no machine check at all
   (presence only).
2. **README house-style mismatch (false-negative risk)** — every existing
   `corpus/README.md` row (Coverage map lines 15–88, Knowledge lines 93+) lists
   entries **without** `.md`. The counter demands the `.md`-suffixed filename;
   it even builds its green fixture with `.md` in the README row. An implementer
   following the lane's own convention fails `readme` at the measured revision
   despite a correct coverage-map row → honest-stop via kill rule on a
   convention mismatch, not on missing work.
3. **Asymmetric literalness** — `PROVINCE.md` passes whether the row writes the
   stem or the full `.md` filename (stem is a substring of the filename);
   `README.md` passes only with `.md`. Plain `in` matching also means any longer
   string containing the dated stem/filename (e.g. a descriptor, a variant stem)
   satisfies the check.
4. **Base-state evidence (control sanity)** — no `## Round-35` section exists in
   `PROVINCE.md` (headings end at Round-32); grep for the dated stems/filenames
   in `PROVINCE.md` and `corpus/README.md` yields zero hits (only `.jsc` /
   "jsc2js-style" wording appears in the Frontier bullets). At base both checks
   fail as the red control requires; `entry_missing` fails first regardless.
5. **Assimilation substrate** — `merge/kaidoku/` and `considerthese/` do not
   exist in this lane (plan line 14 correctly predicted the latter). Prep
   captures exist at `.ufo/waves/round-35/prep/jsc-sources/`
   (`jsc2js-readme.md`, `releases-page1.json`, `releases-page7.json`).

## Commands / output

- `grep 'Round-35|\.jsc|jsc2js' PROVINCE.md` → only Frontier bullets (`:147-148`),
  no round-35 section, no stems.
- `grep 'jsc2js' .` → hits confined to `.ufo/` session transcripts/wave scratch
  and the Frontier-bullet wording; none contain the dated stems.
- `grep '^#{1,4} ' PROVINCE.md` → `## Core` (38), `## Frontier` (73),
  `## Adjacent` (97), dated additions incl. `## Round-32 additions to Core` (353);
  no round-35 heading.
- `read corpus/README.md` → coverage-map rows all list entries without `.md`.

## Advisory

- Counter and kill rule are frozen; do not alter them (predicates/scope frozen).
  The wave executor must therefore write the exact literal forms: dated stems in
  a `## Round-35 additions to Core` table row, and the full `.md` filenames in a
  `## Coverage map` row (deviation from README house style is required to pass).
- The score will certify presence, not section placement or frontier landing.
  If the C1 after-state's *section scoping* must be verified, that is a separate,
  unfrozen documentation/quality check — the machine score cannot carry it.
- First falsifications recorded: (a) the instrument cannot fail a misplaced
  mention, so a green score is weaker than the declared after-state;
  (b) the instrument will fail a convention-conformant README row, so a red
  score is not proof the coverage-map intent was unmet.
