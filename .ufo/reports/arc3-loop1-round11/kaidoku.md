# arc3-loop1-round11 — kaidoku-shokunin — round report

**Schedule slot:** R11 — 32 seats, zai `glm-5.3-flash` at MAX effort.
**Executed as:** 32 seats on `openai-codex/gpt-6-luna-max` (zai lane
usage-exhausted, operator substitution). All 32 reports delivered.
**Work commit:** `5ee13b3`. **Records commit:** this commit.

## Work performed

- **C1 — coverage: a third verb family's `ev_` Evidence-ID formula closed.**
  `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md`
  (CR-2's entry — the verdicts' plurality + CN-1/VZ-2 corroboration):
  `inspect_artifact` is path-sensitive on the *outer* id because the semantic
  projection nests the inventory Evidence inside `normalized_result`
  (`dist/domain/artifactInspection.js:111-155`); the nested
  `inventory_artifact` id is path-stable while the outer id changes on a
  same-basename alternate path. All four envelope IDs recomputed; same-path
  repeat stable. Map token landed on the Evidence-model row; command A 89→90.
- **C2 — freshness: three receipts re-derived first-hand, all honest.**
  Ghidra **34 features / 39 processors** (delta 0/0 — the r4 "35" miscount
  stays corrected); pacman **1,350 archives + 1,350 sig sidecars** (delta 0
  vs the r9 live count, −206 vs the dated 1556); ASAR **12** within the
  searched roots (host-wide completeness bounded by the unreadable
  `/opt/containerd` subtree). No errata needed — the dated values hold.
- **C3 — calibration: the `available:true` class re-derived.** A fresh
  `binary_session {}` reports the provider group `rea-artifact-graph`
  `available:true` (covering `inspect_artifact`/`extract_artifact`), while
  the targetless per-tool entries read `available:false` /
  `reason:"target_required"` — the provider group is available, per-tool
  readiness needs a target. The attached Kimi session is
  `unknown`/`config_drift`. Recorded append-only on the pacman entry.

## Landed changes

- `5ee13b3` — work commit: the `inspect_artifact` corpus entry + Evidence-
  model map token, the pacman availability scope note, and the committed
  wave tree `.ufo/waves/arc3-loop1-round11/` (32 seat artifacts).
- This records commit — SCORECARD section, LOG entry, this report, plus the
  scope re-key to EOF (the recurring class).

## Before → after measurements

| claim | before | after | evidence | measured at |
|---|---|---|---|---|
| C1 coverage | corpus 89; `inspect_artifact` ev_ formula a named Unknown | 90 files; third verb family closed | command A `mapped` | `5ee13b3` → 90/90 |
| C2 freshness | dated Ghidra/pacman/asar values un-re-derived | three receipts measured first-hand; dated values hold | `ls Ghidra/{Features,Processors}`, `ls /var/cache/pacman/pkg/*.pkg.tar.zst`, asar census | `5ee13b3` |
| C3 calibration | `available:true` a dated session-scope value | provider-group `available:true` vs targetless per-tool `target_required` measured | fresh `binary_session {}` output | `5ee13b3` |

Gate confirmations at `5ee13b3`: census `PASS (stale=0 ambiguous=0
undeclared=0 unresolved=0)` + `G21 register 14 rows, errors []` + the
unregistered-bullet guard + live `:4126` `current-ok`; citation-drift
`findings=0` both modes; custody `CLEAN 28/28`; PROVINCE 162 lines.

## Axis verdicts (per-axis, no scalar)

| axis | verdict | evidence |
|---|---|---|
| coverage | **improved** | 89→90; third verb family's ev_ formula closed |
| freshness | **improved** | three receipts re-derived; dated values hold |
| calibration | **improved** | `available:true` scope re-derived; provider-vs-per-tool distinction measured |
| depth | unchanged | 16 → 16 |
| operability | unchanged | census PASS + G21 + guard + ptr `current-ok`; probe 0/0 |
| adjacency | unchanged | PROVINCE boundary untouched |

Admission: all three claims verified by measurement; no axis harmed →
**admitted**.

## The `ev_` domain (three verb families now)

The arc has now derived the Evidence-ID formula for three verb families —
`inspect-evm-interface` (r7), `inspect_rust_binary` (r10), `inspect_artifact`
(r11). Each is path-sensitive by *its own* semantic projection, not by a
universal rule: the EVM family's path fields live in
`normalized_result.artifact.path`/`locations`, the Rust family's in
`parameters.path`/`normalized_result.artifact.path`, and the artifact
family's outer id is path-sensitive only because its projection nests the
path-bearing inventory Evidence. The lesson is now codified: compare cross-
seat ids by the decoded `bytecode.sha256` + function payload, never by the
`ev_` id — and the path-sensitivity is a *per-verb projection* property, not
a domain constant.

## Carried debt (named, not smoothed)

1. Mid-leg faithful retest — still operator-gated (~20 GiB host cost).
2. ASAR host-wide count bounded by the unreadable `/opt/containerd` subtree.
3. Kimi-session availability unverified (`config_drift`).
4. `.ufo/waves/arc2-loop1-round10/C3.md` still dirty; `/tmp` quota standing.

## SHONEN

- `[~]` SKILL.md real decision tables / cited sources — rules #1-16; no new
  rule this round; no named non-author verifier.
- `[~]` end-to-end domain task executed and logged — the third verb family's
  ev_ derivation is a new measured task; logged.
- `[~]` instructions executable without oral context — the provider-vs-per-
  tool availability distinction + the nested-evidence path-sensitivity are
  recorded.
- `[~]` no cross-domain bleed — PROVINCE boundary untouched; all changes
  scope-internal.
