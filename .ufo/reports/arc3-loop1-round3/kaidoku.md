# arc3-loop1-round3 — kaidoku round report

Date: 2026-10-19. Wave: 64 seats frozen pre-dispatch on
`alibaba-token-plan/deepseek-v4.1-flash` (token-plan key 1). **Provider
interruption:** the token-plan lane hit its monthly quota mid-run at 43 reports;
per the operator directive the remaining seats re-dispatched on the devin lane
(`devin/deepseek-v4-1-flash-max`) — 18 of 21 backfilled, final census **62/64**
(EX-14 and SC-3 reports pending; both artifact trees complete). Substitution
recorded with cause; per-lane delivery quoted in the wave summary.

## Work performed

- C1 (coverage, owned): optimizer-enabled + non-ERC-20-shaped carriers compiled
  with the reused, receipt-pinned solc; probes on two pins with planted-set
  reconciliation, same-source optimizer-off controls, decoy/false-positive hunts
  (incl. K=22/25 large-dispatch attack carriers), rerun id-stability, wrong-
  encoding traps, and cross-seat re-derivations (`claims/c1/`).
- C2 (operability, fleet): four named holes closed in the custody tool
  (`claims/c2/`), each with before/after injection evidence, sabotage-arm
  load-bearing proofs, the round-2 regression matrix re-run, and a revised-tool
  live pair.
- C3 (freshness, fleet): probe-table extension (`claims/c3/`) — the arc3
  citation census as acceptance test, needle-quality review, rule-#11
  conformance, non-vacuity drills, and the C2↔C3 collision analysis + re-anchor.
- Cross: consistency sweep, records fold (pin-free, projection-tested),
  custody corroboration, integrator first-hand re-verification of every
  after-state (`claims/cross/`).

## Landed changes

- `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md` — new entry,
  seven reviewer fix sets applied pre-landing (work commit `c418be0`).
- `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` — append-only erratum.
- `corpus/README.md` — additive EVM-row token (line-neutral).
- `SKILL.md` — custody-pair registry row revised (UNEVALUABLE class, 22 cases).
- `.ufo/gates/custody-pair/` — hardened tool (`7cd19c3c…`) + README (`f30df42e…`).
- `.ufo/gates/citation-drift/pointer-table.json` + `expected.json` — 57 entries
  (+26), quoted 5, re-anchored precedence needle, R1 closure, digest re-pin.
- Wave tree committed; one stray `.pyc` removed in a hygiene commit (`5be4a26`).

## Before → after measurements

- C1: command A 82/82 → **83/83** at the work commit (missing [], dangling [],
  14/14 rules, 10.0/10.0; prior 82 byte-identical). K/K selector recovery with
  zero extras on 8 carrier families across two pins; optimizer on/off sets
  identical; binary-search dispatch layouts held to K=25 without truncation.
- C2: selftest 15 → 22 (sabotage arms prove every new case load-bearing); the
  four injections reproduce as declared classes (EACCES fail-open MATCH →
  UNEVALUABLE 14; clobber → refusal; gate-unrecognized → USAGE 2 with the
  unaccounted-paths list; traceback → USAGE 2); round-2 matrix 41/41 hold; live
  pair MATCH 5/5.
- C3: table 31 → 57 entries (+26, 0 removed/modified); quoted 4 → 5; the arc3
  citation census 12/12 covered; probe findings=0 both modes at the work
  commit; selftest 13/13 unchanged; digest pin == landed table.
- Custody: 4/5 byte-identical across the wave; the Kimi client config's pre-wave
  operator-side drift recorded (12:57:45Z); zero in-window drift on the pair.

## SHONEN

- [~] SKILL.md real decision tables — 14/14 rules resolvable at the work commit;
  the registry states the custody tool's real exit map; verifier: none non-author.
- [~] End-to-end domain task executed and logged — the optimizer-leg probe chain
  end-to-end with cross-pin controls; verifier: none non-author.
- [~] Executable without oral context — the r3 entry's recheck re-derived by
  three independent seats (byte-identical envelopes); the custody selftest runs
  verbatim (22 cases); verifier: none non-author.
- [~] No cross-domain bleed — RESULT-class entries, no Core promotion, safety
  verdicts untouched; verifier: none non-author.

## Notes for the next round

- Round 4 per schedule: hyper lane, 32–64 seats (fallback devin — which, with
  token-plan exhausted, is now the standing deepseek-flash substitute per the
  operator directive).
- Named debt: custody residuals (sidecar scope, mkdir guard, stanza-counted
  coverage, both-sides-absent MATCH declared-design ruling); census H2/H4/H5/H6;
  EX-12's control-expectation delta; EX-14/SC-3 reports pending; the pre-existing
  dirty `arc2-loop1-round10/C3.md`; host `/tmp` quota (standing).
