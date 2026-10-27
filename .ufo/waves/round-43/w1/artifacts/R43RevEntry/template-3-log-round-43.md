# Template 3 — LOG round-43 entry

Mirrors the round-42 LOG entry (`LOG.md:3174-3185` at base `6b9e64fe`).
Entries append at the END of LOG.md. Heading format:
`## Round 43 — 2026-10-27 (KaidokuR43)` then blank line and bold-lead bullets.

```markdown
## Round 43 — 2026-10-27 (KaidokuR43)

- **Claims:** R43-C1 depth (triage table v4 re-scored on a fresh freeze-seeded held-out set under a generator that refuses to declare a tuple its own `--run` did not observe — QUALITY 85, routed R42-CL1), R43-C2 coverage (the 18 host-local `corpus/SOURCES.md` rows become resolvable from in-lane copies — routed R41-CL3/R42-CL3). Frozen `<<L1:FREEZE>>` (`plans/round-43-claims.md`).
- **Wave 1** (<<L1:N>> seats, `.ufo/waves/round-43/w1/`): <one or two clauses: generator refusal design + dry runs, S135 opening, local-source copy verification, assimilation re-grounding, quarantine hand-check.>
- **Data:** C2 held-out 78 envelopes (27 named classes × 2 + 24 combos) seeded by the freeze, produced by `tools/round-43/heldout-gen-v4r43.py --seed <<L1:FREEZE>> --run` (L1-run post-freeze); manifest records `generator.tuple_check` all-equal. C2 local-source: 17 in-lane copies under `corpus/evidence/round-43/local-sources/` plus the map `corpus/evidence/local-sources.json`.
- **Scores at `<<L1:REV>>`:** C1 `matched <<L1:matched>>` of 78, `observed_features_match_declared` true, exit `<<L1:exit>>`; C2 gate exit 0, `rows_failed []`, `rows_total <<L1:N>>` (`.ufo/waves/round-43/l1/scores/`).
- **Re-verification (freshness):** <what was re-opened/re-fetched this round: e.g. the S135 URL re-opened by the R43SrcLicense seat (HTTP 200, 1068 B, sha256 `67303bbd…`); the 18 host objects re-hashed against the copies.>
- **Frontier step:** SOURCES 134 → 135 (S135); census exit 0 at start and end (`census-start.txt` at round start; end census recorded at landing); assimilation admit `sasquatch-prebuilt-package-inventory` (re-grounded per `w1/R42Assim.md`'s ADMIT, ≥1 reject stays on record in the lesson Gate); quarantine slice 5 rows hand-checked; `considerthese/`: absent (report line).
- **Tool install:** <none, or name tool/version/channel/reason per the operator tooling-authorization rule; wave-1 seats installed nothing by default.>
```

Format notes:
- The round-42 entry's bullet order is Claims / Wave 1 / Data / Scores at `<rev>` /
  Re-verification (freshness) / Frontier step / Tool install. Keep it.
- The lesson line for round 42 lives in the SCORECARD header paragraph
  (`Lesson corpus/lessons/round-42.md`), not as a LOG bullet — keep that split.
- The LOG entry names the freeze, the wave size and the evidence dirs exactly;
  measured numbers come only from committed receipts.
- `considerthese/`: the round-42 entry logged assimilation none-adopted; the
  round-43 claims file records `considerthese/`: absent as a report line — put
  it in the Frontier step bullet as written above.
