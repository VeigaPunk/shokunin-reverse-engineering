# arc3-loop1-round8 — kaidoku-shokunin — round report

**Schedule slot:** R8 — 16–32 seats, zai lane `glm-5.3-flash`.
**Executed as:** 24 seats on `openai-codex/gpt-6-luna-max` (the second zai
slot — lane usage-exhausted, operator substitution). All 24 reports
delivered.
**Work commits:** `53fcf0c` (the coupled landing) + `227443e` (the probe
wording fix). **Records commit:** this commit.

## Work performed

- **C1 — operability: the `ptr_check` blind spot (R2 residual) closed, done
  right.** EX-1's candidate applied to `.ufo/gates/c1-census-v10.py` (sha
  `80027570…` → `e4fb740c…`): the `if not occ` suppression removed so
  `path:line` pointers are collected even in pin-carrying clauses; a new
  DATED-scope SCORECARD row (1759-1813) fixes the pre-existing undeclared
  FAIL the wave caught (the r7 section's `6.4.0`/`6.7.0` loci at :1776-1783);
  DATED-scope stale pointers class `historical` (preserving the
  receipt-stamped adjudication). **Measured:** the live `:4126` pointer
  evaluates `current-ok` on the clean tree; a re-keyed dead pointer (`:3546`)
  FAILs `stale=1` on a scratch tree; G21 register, the 19-key JSON contract,
  and all prior counters intact. This resolves the r7 adjudicated-partial —
  the mechanism that was provably buildable but unlandable on a stale anchor
  now lands on a real one.
- **C2 — freshness: PROVINCE pin pointer re-anchored in the same commit.**
  `:3546` → `:4126` — the live `rea-agents@6.7.0` line, re-derived this
  round (`:3546` had already drifted to a Copilot model block; the perishable
  `path:line` class drifts on every operator edit). Receipt at
  `.ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt` carrying the live
  line's content sha (`eb237377…` ex-LF / `eb1c7da7…` incl-LF) so the next
  drift is detectable. The probe's `prov18-stamp-named` needle (`17:55:49Z
  receipt`) restored contiguous in `227443e` after the first rewrite dropped
  it — a wording defect the instrument caught, exactly what it's for.
- **C3 — coverage: the Vyper non-default-optimizer Unknown closed.**
  `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md`
  (EX-8's entry — the most complete re-derived evidence): `--no-optimize`
  compiles an EQ/ISZERO compare chain (8 `PUSH4` legs, offsets `PUSH4 pc +
  12` → `CALLVALUE`); `-O codesize` compiles a packed selector/target table
  (no opcode-boundary `PUSH4`, a 61-byte tail of 7-byte records → all
  `JUMPDEST`s, all reported offsets the shared `DUP1`); explicit `-O none`
  ≡ `--no-optimize` resolved (the r7 discrepancy). Map token landed; command
  A 86 → 87.

## Landed changes

- `53fcf0c` — work commit: the gate ptr extension + scope re-key, PROVINCE
  `:3546`→`:4126`, the receipt, the Vyper corpus entry + map token, and the
  committed wave tree `.ufo/waves/arc3-loop1-round8/` (24 seat artifacts).
- `227443e` — the prov18 receipt-stamp wording fix (the probe's needle
  restored contiguous).
- This records commit — SCORECARD section, LOG entry, this report.

## Before → after measurements

| claim | before | after | evidence | measured at |
|---|---|---|---|---|
| C1 operability | `ptr_check` unreachable on pin-carrying clauses; gate FAILs on the undeclared r7 section | live `:4126` pointer `current-ok`; dead re-key `stale=1` FAIL; undeclared FAIL fixed; gate PASS | `c1-census-v10.py --root .` + scratch seeded re-key | `53fcf0c` |
| C2 freshness | `PROVINCE.md:18` cites `:3546` (stale — holds a Copilot block) | cites `:4126` (live `rea-agents@6.7.0`); receipt carries the content sha | `grep -n 'rea-agents@' ~/.kimi-code/config.toml` → `4126:` | `227443e` |
| C3 coverage | corpus 86; Vyper optimizer-forms a named Unknown | 87 files; Unknown closed | command A `mapped` | `53fcf0c` → 87/87 |

Gate confirmations at `227443e`: census `PASS (stale=0 ambiguous=0
undeclared=0 unresolved=0)` + `G21 register 14 rows, errors []` + the live
`:4126` pointer evaluated `current-ok`; citation-drift `findings=0` both
modes; custody `CLEAN 28/28`; PROVINCE 162 lines.

## Axis verdicts (per-axis, no scalar)

| axis | verdict | evidence |
|---|---|---|
| operability | **improved** | `ptr_check` blind spot closed on a real anchor; undeclared FAIL fixed |
| freshness | **improved** | pointer re-anchored to live line; receipt landed; needle restored |
| coverage | **improved** | 86→87; Vyper optimizer-forms Unknown closed |
| depth | unchanged | 15 → 15 |
| calibration | unchanged | 10 → 10 |
| adjacency | unchanged | PROVINCE boundary untouched |

Admission: all three claims verified by measurement; no axis harmed →
**admitted**.

## The resolved partial (r7 → r8)

The r7 C1 claim was adjudicated partial: the mechanism was buildable but the
acceptance anchor (`:3298`/`:3546`) had already drifted, so "clean PASS" was
unsatisfiable. R8's coupled landing is the adjudication's named fix — the
receipt, the extension, and the re-anchor in one commit, so the instrument
can grade a *real* pointer. This is the discipline the arc trains: a claim
whose own premise drifted gets a measured fix, not a forced pass.

## Carried debt (named, not smoothed)

1. Register append-past-:162 residual (named in PL-4's patch text).
2. Mid-leg faithful retest — still operator-gated (~20 GiB host cost).
3. The perishable pin-line class will drift again — now detectable via the
   receipt's content hash.
4. `.ufo/waves/arc2-loop1-round10/C3.md` still dirty; `/tmp` quota standing.

## SHONEN

- `[~]` SKILL.md real decision tables / cited sources — rules #1-15; no new
  rule this round; no named non-author verifier.
- `[~]` end-to-end domain task executed and logged — the Vyper optimizer
  forms are a new measured task; logged.
- `[~]` instructions executable without oral context — the coupled-landing
  recipe is recorded (receipt + extension + re-anchor in one commit).
- `[~]` no cross-domain bleed — PROVINCE boundary untouched; gate + receipt
  changes are scope-internal.
