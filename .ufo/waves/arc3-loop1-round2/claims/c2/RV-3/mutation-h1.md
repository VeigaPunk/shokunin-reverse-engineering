# Mutation test — H1 absent-file guard is load-bearing (chain c2, seat RV-3)

Seat RV-3 (reviewer, chain c2), arc3-loop1-round2, 2026-10-19. Primary artifact
(`.ufo/waves/arc3-loop1-round2/claims/c2/RV-3/mutation-h1.md`).

**Question.** The closed C2 claim says the census FAILs with a declared class when a
scoped file is absent. A FAIL that arrives for some *other* reason would make the
claim true by accident. This artifact tests the guard itself: revert ONLY the H1
guard on a scratch copy of the landed instrument and check that the round-1 silent
PASS returns. If it does, the guard is load-bearing; if the mutant still FAILs, H1 is
not what closes the hole.

## Instrument under test (identity)

| Item | Value |
|---|---|
| Path | `.ufo/gates/c1-census-v10.py` (EX-16's real target; this seat wrote nothing there) |
| sha256 (pinned) | `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` |
| Size / mtime | 31,906 B; 2026-10-19 09:19:52 −03; hash re-confirmed unchanged at 09:25 −03 |
| `main()` block digest | `2ae7ecd68a073987ed397e96137d0e7493fb1dbd74d48e2643696720d1ba2a61` (sha256 of `def main():` … end of file) — this block is **byte-identical** across landings `df9ffdf9`, `a4c16763`, `d0772ce8`, so the mutation result is invariant to the churn that produced them |
| Pre-landing (v10) | `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b` (23,939 B) |
| Landing churn seen | `1431620f…` → `2a89793a…` → `65442158…` → `9373964c…` → `a455391e…` → `82fb807e…` → `df9ffdf9…` → `a4c16763…` → `d0772ce8…` (EX-16 edited through the window; the last two deltas are header-stanza text only — `main()` unchanged. The battery was run against `82fb807e`, `df9ffdf9`, `a4c16763` and the pinned `d0772ce8`; every H1-relevant row is identical in all four) |

H1 as landed (`main()` line refs into the pinned file):

- `:514` `out, counts, filelines, unreadable = {}, {}, {}, []`
- `:518-521` `except OSError as ex:` → `:520` `unreadable.append("%s: %s" % (f, type(ex).__name__))`,
  counts read `{"lines": None, "loci": None}`, `filelines[f] = None`
- `:524-529` rows-beyond-declared-EOF check (G19) → second `unreadable.append(…)` site at `:526`
- `:567` `declared = (["UNREADABLE"] if unreadable else []) + …`
- `:569` verdict term `… and g2_ok and (not unreadable)`
- `:575` `--json` carries `"unreadable"` / `"declared_fail_classes"`
- `:597` `print("UNREADABLE (could-not-evaluate): %r" % unreadable)`

H3 as landed (`:566` `g2_ok = h3_ok`, positive per-readable-file floor) is untouched by
every mutant below; `m-h3` reverts only that line.

## Method

All work on scratch copies under `/var/tmp/rv3-mutation` (never `/tmp`, never the real
target; no git mutations). `tools/mutate-h1-v2.py` locates each H1 anchor and aborts
if an anchor does not occur exactly once, so a silent mis-edit is not possible. Four
independent cuts:

| Mutant | Cut | Diff size vs landed |
|---|---|---|
| `m-term` | drop ONLY the verdict term `and (not unreadable)` | 4 changed lines |
| `m-eof` | drop ONLY the G19 rows-beyond-EOF site (OSError catch kept) | 9 |
| `m-full` | revert the whole H1 class (both collection sites, verdict term, report line, JSON field, declared-class entry) → v10 H1 semantics | 24 |
| `m-h3` | revert ONLY H3 (`g2_ok = h3_ok` → the v10 disjunctive form); H1 intact | 4 |

Fixtures: fresh copies of the three scoped files from HEAD plus one mutated file —
`fixture-full` (control), `fixture-noskill` (SKILL.md absent, the primary scenario),
`fixture-emptyskill` (0-byte), `fixture-shortskill` (10 lines < declared max 20),
`fixture-dirskill` (SKILL.md is a directory), `fixture-permskill` (mode 000),
`fixture-noprovi`, `fixture-noscore`, `fixture-allabsent`, and round-1's own attack
roots `atk-silent` / `atk-undecl`.

## Results (pinned `d0772ce8`; full matrix `receipts/landed-run/battery-matrix.txt`)

Primary scenario — SKILL.md absent:

| Instrument | Exit | Verdict | UNREADABLE class |
|---|---|---|---|
| v10 (pre-landing baseline) | 0 | PASS | not emitted |
| **landed** | **1** | **FAIL** | `['SKILL.md: FileNotFoundError']` |
| `m-term` (verdict term only) | 0 | PASS | `['SKILL.md: FileNotFoundError']` (reported, inert) |
| `m-eof` | 1 | FAIL | `['SKILL.md: FileNotFoundError']` |
| `m-full` (whole H1 class) | **0** | **PASS** | not emitted; `SKILL.md lines=0 loci=0` |
| `m-h3` (H3 reverted, H1 intact) | 1 | FAIL | `['SKILL.md: FileNotFoundError']` |

**Verdict: the H1 guard is load-bearing.** Reverting only the H1 class returns the run
to the round-1 defect exactly — exit 0,
`VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`,
`SKILL.md lines=0 loci=0`, `SCOPE-ERRORS (marker assertions): []`. On RV-11's own
round-1 fixture the mutant's report body is identical to the round-1 receipt
`RV-11/scratch/atk-missing.out` except for the two lines H3 introduced (the G2 line's
per-file counts; `DECLARED FAIL CLASSES: []`) — `m-full-r1-atkmissing.txt` vs
`landed-r1-atkmissing.txt`.

Supporting measurements:

- Ordinary run at HEAD (real root): `VERDICT: PASS … exit 0`, `UNREADABLE []`,
  `DECLARED FAIL CLASSES []` — the guard costs nothing when every file is present
  (`receipts/landed-run/landed-at-head.txt`).
- `--json` channel: landed absent-SKILL → exit 1, `verdict=FAIL`,
  `declared_fail_classes=['UNREADABLE']`, `SKILL.md {lines: null, loci: null}`;
  `m-full` → exit 0, `verdict=PASS`, classes `[]`, `SKILL.md {lines: 0, loci: 0}`.
  The mutation restores the silent pass in both channels, so the claim's exit-code
  semantics ride on H1, not on the text report alone.
- Truncation subclass: landed FAILs on 0-byte and short SKILL.md
  (`SKILL.md: 0 lines < declared max 20`, `… 10 lines < declared max 20`) where v10
  read PASS. `m-eof` shows that site is *redundant* with H3's per-file floor: with it
  removed those fixtures still FAIL, but as `BLIND-INSTRUMENT` (`UNREADABLE []`).
- Non-OSError shapes: directory-as-file → `IsADirectoryError`, mode 000 →
  `PermissionError`; both declared UNREADABLE and both reverted to PASS by `m-full`.

## Attacks / refutations attempted

- **A1 — mutant could be a blanket PASS.** Refuted: `m-full` still FAILs exit 1 on
  `atk-undecl`, `noprovi`, `noscore`, `allabsent`; it matches v10's verdict on every
  fixture except the two truncation fixtures, where the extra FAIL comes from H3's
  per-file floor (`BLIND-INSTRUMENT`), a different guard.
- **A2 — the FAIL might be a side effect of another guard.** Refuted by `m-h3`:
  reverting the H3 floor with H1 intact keeps absent-SKILL at FAIL with the
  `FileNotFoundError` class.
- **A3 — the guard might exist but not gate the verdict.** Demonstrated real by
  `m-term`: the same guard that collects, reports and serializes `unreadable` reads
  PASS exit 0 once its verdict term is dropped. The load-bearing link is the term at
  `:569`; a future edit that keeps the report but drops the term would silently
  reopen the hole.
- **A4 — absence may be covered twice, hiding a broken H1.** Refuted: for a missing
  file the per-file floor is exempt (`filelines[f] is None`), so absence is carried by
  H1 alone — proved by A1.
- **A5 — round-1 receipt reproduction.** Confirmed modulo the two H3-introduced lines
  (diff above).
- **A6 — churn may invalidate the pin.** Refuted by digest: `main()` is byte-identical
  (`2ae7ecd6…`) across the last three landings, and the battery was re-run green on
  the newest of them; a moved anchor makes `mutate-h1-v2.py` abort instead of
  silently mutating the wrong code.

## Residuals named (not closed by this test)

- Partial per-needle blindness keeps `loci > 0` and still reads PASS — the H4
  self-certification residual, stated in the landed header; the external
  locus/scope audit remains its certificate.
- A file that is present, readable and *longer* than declared is governed by the
  UNDECLARED class, not H1; not exercised here.
- This test pins one hash and one block digest. If EX-16 edits the instrument again,
  re-run `tools/landed-battery-v2.sh` (≈3 s); the harness aborts loudly on a moved
  anchor, so no silent reuse is possible.

## Receipts (under `claims/c2/RV-3/`)

- `receipts/landed-run/battery-matrix.txt` — 11 fixtures × 6 instruments: exit codes,
  verdicts, UNREADABLE lists.
- `receipts/landed-run/rcpt/` — the 66 per-run quiet receipts.
- `receipts/landed-run/diff-landed-vs-{m-term,m-eof,m-full,m-h3}.diff` — exact
  mutation footprints.
- `receipts/landed-run/{landed,m-full}-r1-atkmissing.txt` — round-1 origin
  reproduction (RV-11's `atk-missing` root).
- `receipts/landed-run/{landed,m-full}-noskill.json` — JSON-channel pair.
- `receipts/landed-run/landed-at-head.txt` — ordinary run at HEAD.
- `receipts/landed-run/landed-sha256.txt` — instrument sha256 + `main()` block digest;
  `instrument-sha256.txt`, `mutation-footprint.txt`.
- `receipts/model-run/` — pre-landing model-phase battery (round-1 H1 patch text
  applied to v10 on scratch) with `MANIFEST.sha256`; superseded by the landed run but
  kept as the projection.
- `tools/mutate-h1-v2.py`, `tools/landed-battery-v2.sh` (landed shape);
  `tools/mutate-h1.py`, `tools/run-suite.sh` (model shape).
