# arc3-loop1-round10 — kaidoku-shokunin — round report

**Schedule slot:** R10 — 32–64 seats, `devin/deepseek-v4-1-flash-max`.
**Executed as:** 48 seats on `openai-codex/gpt-6-luna-max` (the devin lane is
exhausted, operator substitution). All 48 reports delivered.
**Work commit:** `9c1d1fe`. **Records commit:** this commit.

## Work performed

- **C1 — coverage: a second verb family's `ev_` Evidence-ID formula closed.**
  `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md` (EX-4's
  entry — the verdicts converged on it over the Vyper multi-target drafts):
  `inspect_rust_binary` is path-sensitive because its semantic projection
  carries `parameters.path`, `normalized_result.artifact.path`, and an
  `artifact-path` location (`dist/application/rust/RustBinaryService.js:55-80`);
  all four envelope IDs recomputed to their claimed values; display fields
  (`subject.name`/`local_path`) excluded. Map token landed on the Rust row;
  command A 88 → 89.
- **C2 — depth: rule #16 landed** (SC-2's "Co-land every truth dependency" —
  the verdicts' majority pick): before repairing a statement whose truth
  depends on another deliverable, name the dependency and land the complete
  set in one commit; a scratch projection is not a landed result. Cites the
  r4 Vyper-wording↔C1 coupling and the r8 receipt↔extension coupling —
  the lesson those landings earned. `rule_blocks` 15 → 16, all 16 resolved.
- **C3 — operability: the G21 register's append-past-:162 residual closed.**
  PL-3's unregistered-bullet guard applied to `c1-census-v10.py` (sha
  `e4fb740c…` → `d6b4deaa…`): `FRONTIER_SECTIONS` + a bullet-start check
  flags any `[-*+]` bullet inside a Frontier section that no G21 row keys.
  Measured: a seeded bullet appended at :163 now FAILs
  `FRONTIER-UNEVALUABLE`; clean tree PASS, 14 rows asserted, errors `[]`.

## Landed changes

- `9c1d1fe` — work commit: the `inspect_rust_binary` corpus entry + Rust map
  token, rule #16 in `SKILL.md`, the G21 unregistered-bullet guard, and the
  committed wave tree `.ufo/waves/arc3-loop1-round10/` (48 seat artifacts).
- This records commit — SCORECARD section, LOG entry, this report, plus the
  scope re-key to EOF (the recurring class).

## Before → after measurements

| claim | before | after | evidence | measured at |
|---|---|---|---|---|
| C1 coverage | corpus 88; `inspect_rust_binary` ev_ formula a named Unknown | 89 files; formula closed for a second verb family | command A `mapped` | `9c1d1fe` → 89/89 |
| C2 depth | `rule_blocks` 15 | `rule_blocks` 16, all 16 resolved | command A `rule_blocks` + `citation_resolved_rules` | `9c1d1fe` → 16/16 |
| C3 operability | a seeded bullet past :162 reads PASS silently (register's named residual) | seeded bullet FAILs `FRONTIER-UNEVALUABLE` | `c1-census-v10.py --root .` on clean vs seeded scratch | `9c1d1fe` |

Gate confirmations at `9c1d1fe`: census `PASS (stale=0 ambiguous=0
undeclared=0 unresolved=0)` + `G21 register 14 rows, errors []` + the
unregistered-bullet guard + live `:4126` `current-ok`; citation-drift
`findings=0` both modes; custody `CLEAN 28/28`; PROVINCE 162 lines.

## Axis verdicts (per-axis, no scalar)

| axis | verdict | evidence |
|---|---|---|
| coverage | **improved** | 88→89; second verb family's ev_ formula closed |
| depth | **improved** | 15→16 rules; coupled-landing discipline codified |
| operability | **improved** | register append residual closed; seeded bullet caught |
| freshness | unchanged | corpus errata hold; no staleness reintroduced |
| calibration | unchanged | 10 → 10 |
| adjacency | unchanged | PROVINCE boundary untouched |

Admission: all three claims verified by measurement; no axis harmed →
**admitted**.

## The codified disciplines (the arc's steady state)

Three recurring disciplines are now craft rules: parsed-and-empty ≠
byte-absence (#15), co-land every truth dependency (#16), and
instrument-graded vs clause-audited (the G21 register + its new append
guard). Each was earned by a landing that carried a coupling or a residual
the seats measured. The wave kept the standard: every before-state measured,
every landing re-derived at the commit.

## Carried debt (named, not smoothed)

1. Mid-leg faithful retest — still operator-gated (~20 GiB host cost).
2. The `available:true` class stays dated, not re-probed.
3. `.ufo/waves/arc2-loop1-round10/C3.md` still dirty; `/tmp` quota standing.

## SHONEN

- `[~]` SKILL.md real decision tables / cited sources — rule #16 landed this
  round; no named non-author verifier.
- `[~]` end-to-end domain task executed and logged — the second verb family's
  ev_ derivation is a new measured task; logged.
- `[~]` instructions executable without oral context — the coupled-landing
  rule + the register guard are self-documenting.
- `[~]` no cross-domain bleed — PROVINCE boundary untouched; all changes
  scope-internal.
