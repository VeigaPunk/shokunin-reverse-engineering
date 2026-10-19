# arc3-loop1-round9 — kaidoku-shokunin — round report

**Schedule slot:** R9 — 32–64 seats, `openai-codex/gpt-6-luna-max`.
**Executed as:** the scheduled provider, no substitution. All 48 reports
delivered.
**Work commit:** `eb5a2c4`. **Records commit:** this commit.

## Work performed

- **C1 — freshness: the `PROVINCE.md:50` perishable-value residual repaired
  same-line** (162 held). "pacman `.pkg.tar.zst` corpus 1556 signed archives"
  now carries the dated qualifier + the live delta + the dated `available:true`
  clause: `cache: 1,556 signed archives (2026-10-13 snapshot); current cache:
  1,350 archive files, each with a matching .sig sidecar (arc3-loop1-round9
  recount; −206 vs snapshot)`. PL-3's measured text; the row's other
  perishables adjudicated (the `available:true` is a session-scoped value, now
  dated to the survey, not read as a fresh check — no live REA session this
  round). **The wave also caught a second pre-existing gate FAIL**
  (`SCORECARD.md:1834`, the r8 section's `6.7.0` pin outside the 1759-1813
  scope row); the scope re-key to `1759-1870` (then `1759-1924` once this
  section landed) fixes it — the instrument now reads PASS with the row's
  loci evaluated.
- **C2 — coverage: the viaIR final-selector-miss residual closed.**
  `corpus/knowledge/2026-10-19-arc3-r9-viair-fallback-miss.md` (EX-8's entry —
  the strongest of the C2 drafts): byte-level evidence that the `SUB`-leg
  mismatch branch at PC `0xc2`/`0xcf` distinguishes the no-fallback revert
  path (`PUSH0; DUP1; REVERT` at PCs `0x15-0x17`) from the payable-fallback
  storage-write path (`CALLVALUE` → `SSTORE` slot 2 → `STOP`); 15/15
  selectors at both variants, both pins. Map token landed; command A 87→88.
- **C3 — calibration: the pin-line drift class characterized end-to-end.**
  The pin is the **sole** `rea-agents@` match at `:4126`; the ptr extension
  evaluates it `current-ok`. **The class is position-sensitive, not
  content-sensitive** (measured on synthetic fixtures: a one-line insertion
  *above* the pin reads `stale`; a duplicate pin line stays `current-ok` —
  the receipt's content hash binds the line's bytes, but the line number is
  what drifts). Recorded append-only on the r8 receipt.

## Landed changes

- `eb5a2c4` — work commit: the SCORECARD scope re-key, `PROVINCE.md:50`
  dated+live repair, the viaIR fallback-miss entry + map token, the receipt
  drift-class note, and the committed wave tree `.ufo/waves/arc3-loop1-round9/`
  (48 seat artifacts).
- This records commit — SCORECARD section, LOG entry, this report.

## Before → after measurements

| claim | before | after | evidence | measured at |
|---|---|---|---|---|
| C1 freshness | `PROVINCE.md:50` unqualified perishable count (stale if read as current); gate FAILs on undeclared r8 section | dated + live-delta repair; scope re-key; instrument PASS | `grep -n "1556" PROVINCE.md` + `c1-census-v10.py --root .` | `eb5a2c4` |
| C2 coverage | corpus 87; viaIR fallback-miss a named residual | 88 files; residual closed | command A `mapped` | `eb5a2c4` → 88/88 |
| C3 calibration | pin drift class measured but not characterized | position-sensitivity measured end-to-end; recorded on receipt | `.ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt` | `eb5a2c4` |

Gate confirmations at `eb5a2c4`: census `PASS (stale=0 ambiguous=0
undeclared=0 unresolved=0)` + `G21 register 14 rows, errors []` + live `:4126`
`current-ok`; citation-drift `findings=0` both modes; custody `CLEAN 28/28`;
PROVINCE 162 lines.

## Axis verdicts (per-axis, no scalar)

| axis | verdict | evidence |
|---|---|---|
| freshness | **improved** | `PROVINCE.md:50` dated + live-delta; scope re-key; instrument PASS |
| coverage | **improved** | 87→88; viaIR fallback-miss residual closed |
| calibration | **improved** | drift class characterized; position-sensitivity measured |
| depth | unchanged | 15 → 15 |
| operability | unchanged | census PASS + G21 + ptr `current-ok`; probe 0/0 |
| adjacency | unchanged | PROVINCE boundary untouched |

Admission: all three claims verified by measurement; no axis harmed →
**admitted**.

## The recurring scope-drift class (now the steady state)

Each round's wave catches the prior round's own scope drift — the r7 and r8
SCORECARD sections each went undeclared the moment they landed, because a new
round section pushes past the declared DATED bound. The fix folds into the
same commit that lands the claim. This is exactly the instrument-driven
correction loop the arc exists to train: the gate is the tripwire, the wave
is the auditor, the landing is the fix.

## Carried debt (named, not smoothed)

1. Register append-past-:162 residual (named in PL-4's patch text).
2. Mid-leg faithful retest — still operator-gated (~20 GiB host cost).
3. The `available:true` class stays dated, not re-probed (no live REA
   session this round).
4. `.ufo/waves/arc2-loop1-round10/C3.md` still dirty; `/tmp` quota standing.

## SHONEN

- `[~]` SKILL.md real decision tables / cited sources — rules #1-15; no new
  rule this round; no named non-author verifier.
- `[~]` end-to-end domain task executed and logged — the viaIR fallback-miss
  leg is a new measured task; logged.
- `[~]` instructions executable without oral context — the scope-drift
  correction loop + the drift-class characterization are recorded.
- `[~]` no cross-domain bleed — PROVINCE boundary untouched; all changes
  scope-internal.
