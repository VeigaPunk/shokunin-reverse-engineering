# RV-11 — AFTER state (post EX-28), measured

Instrument sha256 chain for `.ufo/gates/c1-census-v10.py` on 2026-10-19:

| when (UTC) | sha256 | note |
|---|---|---|
| before (HEAD) | `36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48` | blob `1091d95`, round-8 version |
| 10:15-10:17 | `8e5f34954bbbc77c0d3a2ce4428116b24350ced4941982a04f20125f6ee567d4` | first EX-28 edit (seen at watcher start 10:17:01Z, not captured) |
| 10:18:01 | `c39beccc0c80dda76c7e11ad159f30fa9ac36c353093dbeeb115f2f92c5e85b6` | mid-edit: `VERDICT: FAIL … SCOPE-ERRORS ['PROVINCE.md:40 marker line outside its own declared range 45-62 (G18)']` — G18 fired on the not-yet-re-keyed row (`after/census-after.out`) |
| 10:18:24 onward | `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b` | settled: PASS (this file) |

## After-state run (settled instrument)

```
$ sha256sum .ufo/gates/c1-census-v10.py
6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b
$ python3 .ufo/gates/c1-census-v10.py            # exit 0
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1336 loci=9
SKILL.md       lines=371  loci=2
SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

Full output: `after/census-after-final.out` (+ `after/census-after-rerun.out`).
Verdict unchanged from before (PASS→PASS); loci counts identical (6/9/2).

## What EX-28 changed (from `after/census-after-101824.diff`, +60/-3)

1. Header stanza: E22 disposition (finding does not reproduce at HEAD; discharged by
   re-key; four-capture digest `3b677b8e…`; v9 stays red at HEAD by construction) +
   three refused alternatives with measured causes (tail expansion = fail-open
   laundering; retiring `:619/:620`; re-classing CURRENT→DATED as creep).
2. One SCOPE row re-keyed, bounds untouched:
   `("PROVINCE.md", 45, 62, "DATED", 40, r"verified on this host 2026-10-13")` →
   `("PROVINCE.md", 45, 62, "DATED", 45, r"2026-10-13")`.
3. New guard G18 in `assert_markers`: marker line must lie inside the range it dates.

## Reviewer verification of the change

- **G18 is live, not vacuous** — falsification on a scratch copy
  (`scratch/census-g18-miskeyed.py`, row `119-131` mis-keyed to `ml=118`):
  `SCOPE-ERRORS ['PROVINCE.md:118 marker line outside its own declared range
  119-131 (G18)', …]`, `VERDICT: FAIL`, exit 1 → `after/g18-falsification.out`.
- **Range-neutral re-key** — the diff touches exactly one SCOPE line and no bound
  (45,62 unchanged); no row added, none retired.
- **Re-keyed marker resolves** — `PROVINCE.md:45` is the `rea` CLI table row
  carrying `(2026-10-13 receipt)`; SCOPE-ERRORS `[]` confirms the marker matches.
  Observation (not a defect): the marker now sits on one table row's receipt text
  rather than the table intro (line 40, `… verified on this host 2026-10-13.`,
  which lies in the 40-43 row); G18's requirement is met and the DATED
  justification is still receipt text.
- **Old readings unaffected** — matched-pair checks re-run: the new instrument at
  HEAD PASSes; gated-tail injection still caught (FAIL undeclared=1, exit 1,
  `after/atk-undecl-after.out`); absent-`SKILL.md` silent PASS still present
  (exit 0, `after/atk-missing-after.out`) — the hardening in
  `proposed-missing-file-guard.patch.md` remains open, by design advisory.
- **Header claims spot-checked**: the `3b677b8e…` four-capture digest (verified
  independently, 5-way), and the v9@HEAD `undeclared=2` + `:635` marker reading
  (verified in `e22-reproduction.md` §1-§2).
- EX-28's own seat report / claim artifacts had not landed at this capture
  (48 seat reports present; `claims/c3/EX-28/` empty) — this after-state is
  measured from the instrument file itself, which is what the claim turns on.
