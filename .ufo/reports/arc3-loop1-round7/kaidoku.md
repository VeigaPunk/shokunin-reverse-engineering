# arc3-loop1-round7 — kaidoku-shokunin — round report

**Schedule slot:** R7 — 16–32 seats, zai lane `glm-5.3-flash`.
**Executed as:** 24 seats on `openai-codex/gpt-6-luna-max` — the zai lane is
usage-exhausted; the operator directive substitutes luna-max for all remaining
zai slots (R7, R8, R11) through the end of the session. All 24 reports
delivered.
**Work commit:** `7deeb36`. **Records commit:** this commit.

## Work performed

- **C1 — operability: the `ptr_check` blind spot (R2 residual) — adjudicated
  PARTIAL.** The wave confirmed the blind spot is real (every seat + every
  verdict: the baseline gate reads PASS while never evaluating the `:18`
  pointer — `ptr_check` is unreachable on a pin-carrying clause) AND that a
  working extension is buildable (EX-1's digest-checked candidate and RV-2's
  anchor variant each PASS on a clean scratch tree and FAIL `UNRESOLVED`/
  `STALE` on a re-keyed dead pointer, G21 + the 19-key JSON contract intact).
  **The landing is genuinely blocked:** the frozen claim named `config.toml
  :3298` while the live `PROVINCE.md:18` pointer is `:3546` (the 2026-10-19
  re-read) — and `ptr_check` on the live target reads `stale`. No patch can
  read "clean PASS on the current tree" without either anchoring a receipt the
  receipt doesn't carry (the custody receipt stores a whole-config sha, not
  the target line's content) or failing the live tree. Withheld honestly;
  recorded in `claims/c1/C1-ADJUDICATION.md`. The clean fix is a re-receipt
  of the current pin line in the same commit that lands the instrument
  extension.
- **C2 — coverage: the `ev_` Evidence-ID formula Unknown closed.**
  `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md` (EX-3's
  entry — the verdicts converged on it over EX-6's path-only draft and the
  Vyper optimizer candidate): the id is `ev_` + lowercase sha256 of UTF-8
  canonical JSON over the semantic projection, per the `rea-agents@6.4.0`/
  `6.7.0` package source; path-bearing fields (`parameters.path`,
  `normalized_result.artifact.path`, `locations[0].path`) affect the id while
  display-only `subject.name`/`local_path` do not; all 8 envelopes recomputed
  to their claimed ids. Map token landed; command A 85 → 86.
- **C3 — calibration: pacman archive inventory re-derived.** Live count
  **1350** `.pkg.tar.zst` (six independent seat counts + the verdicts, all
  agree) vs the dated 1556 receipt — delta **−206**, cache eviction,
  retention-varying inventory, not a capability change. Adjudicated no-edit
  on the dated corpus value; append-only erratum landed on the pacman entry
  recording the delta + the `PROVINCE.md:50` unqualified-count residual.

## Landed changes

- `7deeb36` — work commit: the `ev_` corpus entry, the EVM map token, the
  pacman erratum, the C1 adjudication record, and the committed wave tree
  `.ufo/waves/arc3-loop1-round7/` (24 seat artifacts).
- This records commit — SCORECARD section, LOG entry, this report.

## Before → after measurements

| claim | before | after | evidence | measured at |
|---|---|---|---|---|
| C1 operability | `ptr_check` unreachable on pin-carrying clauses (blind spot confirmed) | mechanism proven + candidate patches catch seeded faults; landing withheld on the stale-live-pointer discrepancy | `claims/c1/C1-ADJUDICATION.md` | `7deeb36` |
| C2 coverage | corpus 85; `ev_` formula a named Unknown | 86 files; formula derived for both pins | command A `mapped` | `7deeb36` → 86/86 |
| C3 calibration | dated 1556 count; no live re-derivation | 1350 measured first-hand; dated receipt preserved | `ls /var/cache/pacman/pkg/*.pkg.tar.zst \| wc -l` | `7deeb36` |

Gate confirmations at `7deeb36`: census `PASS` + `G21 register 14 rows,
errors []`; citation-drift `findings=0` both modes; custody `CLEAN 28/28`;
PROVINCE 162 lines.

## Axis verdicts (per-axis, no scalar)

| axis | verdict | evidence |
|---|---|---|
| coverage | **improved** | 85→86; the `ev_` formula Unknown closed |
| calibration | **improved** | live delta measured; dated receipt preserved |
| operability | unchanged | mechanism proven; landing withheld (honest partial) |
| depth | unchanged | 15 → 15 |
| freshness | unchanged | pacman drift recorded; dated value preserved |
| adjacency | unchanged | PROVINCE boundary untouched |

Admission: C2 and C3 verified by measurement; C1 is an honest partial — its
falsifiable half met (mechanism proven) but its acceptance half unsatisfiable
as written (the claim's own pointer had already drifted). The round is
**admitted** on the two verified claims + the recorded partial; no axis
harmed.

## The honest partial (why withholding was the right call)

The instrument extension is provably buildable — but the claim's acceptance
criterion was written against a receipt anchor that had already drifted. The
correct move was to name the blocker and withhold the patch: landing a fake
anchor or a failing gate would both be dishonest, and the clean fix
(re-receipt the current pin line in the same commit) is a different action.
This is the discipline the arc exists to train.

## Carried debt (named, not smoothed)

1. **C1 `ptr_check` extension** — mechanism proven; needs a re-anchored
   receipt of the *current* pin line before the instrument can grade it.
2. `PROVINCE.md:50`'s unqualified pacman count (read-as-current = stale).
3. Mid-leg faithful retest — still operator-gated (~20 GiB host cost).
4. Register append-past-:162 residual (named in PL-4's patch text).
5. `.ufo/waves/arc2-loop1-round10/C3.md` still dirty; `/tmp` quota standing.

## SHONEN

- `[~]` SKILL.md real decision tables / cited sources — rule #15 landed r6;
  no new rule this round; no named non-author verifier.
- `[~]` end-to-end domain task executed and logged — the `ev_` formula
  derivation is a new measured task; logged.
- `[~]` instructions executable without oral context — the C1 adjudication
  records the exact blocking condition + the clean fix.
- `[~]` no cross-domain bleed — PROVINCE boundary untouched; all changes
  scope-internal.
